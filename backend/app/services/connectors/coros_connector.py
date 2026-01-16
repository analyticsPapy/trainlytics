"""Coros API connector implementation."""

from typing import Dict, List, Optional, Any
from datetime import datetime
import hashlib
import hmac
import time
import httpx

from app.services.connectors.base_connector import BaseConnector
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class CorosConnector(BaseConnector):
    """Connector for Coros Open API."""

    def __init__(self):
        super().__init__()
        self.provider_name = "coros"
        self.base_url = "https://open.coros.com/oauth2"
        self.api_url = "https://open.coros.com/api/v1"

    async def get_authorization_url(self, state: str, redirect_uri: str) -> str:
        """
        Generate Coros OAuth authorization URL.

        Args:
            state: CSRF token
            redirect_uri: Callback URL

        Returns:
            Authorization URL
        """
        params = {
            'client_id': settings.COROS_API_KEY,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'training_data:read',
            'state': state
        }

        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        url = f"{self.base_url}/authorize?{query_string}"

        logger.info("coros_auth_url_generated", state=state)
        return url

    async def exchange_code(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access tokens.

        Args:
            code: Authorization code
            redirect_uri: Redirect URI used in authorization

        Returns:
            Dict containing tokens and user info
        """
        try:
            timestamp = str(int(time.time()))
            signature = self._generate_signature(timestamp)

            response = await self.client.post(
                f"{self.base_url}/accesstoken",
                json={
                    'client_id': settings.COROS_API_KEY,
                    'client_secret': settings.COROS_API_SECRET,
                    'code': code,
                    'grant_type': 'authorization_code',
                    'redirect_uri': redirect_uri
                },
                headers={
                    'timestamp': timestamp,
                    'signature': signature
                }
            )

            response.raise_for_status()
            data = response.json()

            if data.get('result') != '0000':
                raise Exception(f"Coros API error: {data.get('message')}")

            token_data = data.get('data', {})
            access_token = token_data.get('access_token')
            refresh_token = token_data.get('refresh_token')
            expires_in = token_data.get('expires_in', 3600)

            # Get user info
            user_info = await self.get_user_profile(access_token)

            logger.info("coros_token_exchange_success", user_id=user_info.get('openId'))

            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'expires_at': int(time.time()) + expires_in,
                'user_id': user_info.get('openId', ''),
                'user_info': user_info
            }

        except httpx.HTTPStatusError as e:
            logger.error("coros_token_exchange_failed", status=e.response.status_code, error=e.response.text)
            raise Exception(f"Coros token exchange failed: {e.response.text}")

    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh expired access token.

        Args:
            refresh_token: Refresh token

        Returns:
            Dict containing new tokens
        """
        try:
            timestamp = str(int(time.time()))
            signature = self._generate_signature(timestamp)

            response = await self.client.post(
                f"{self.base_url}/refresh-token",
                json={
                    'client_id': settings.COROS_API_KEY,
                    'client_secret': settings.COROS_API_SECRET,
                    'refresh_token': refresh_token,
                    'grant_type': 'refresh_token'
                },
                headers={
                    'timestamp': timestamp,
                    'signature': signature
                }
            )

            response.raise_for_status()
            data = response.json()

            if data.get('result') != '0000':
                raise Exception(f"Coros API error: {data.get('message')}")

            token_data = data.get('data', {})
            expires_in = token_data.get('expires_in', 3600)

            logger.info("coros_token_refreshed")

            return {
                'access_token': token_data.get('access_token'),
                'refresh_token': token_data.get('refresh_token'),
                'expires_at': int(time.time()) + expires_in
            }

        except Exception as e:
            logger.error("coros_token_refresh_failed", error=str(e))
            raise

    async def get_user_profile(self, access_token: str) -> Dict[str, Any]:
        """
        Get user profile information.

        Args:
            access_token: Access token

        Returns:
            User profile data
        """
        try:
            response = await self._make_coros_request(
                method='GET',
                url=f"{self.api_url}/userinfo",
                access_token=access_token
            )

            logger.info("coros_user_profile_fetched")
            return response.get('data', {})

        except Exception as e:
            logger.error("coros_user_profile_failed", error=str(e))
            raise

    async def get_activities(
        self,
        access_token: str,
        after: Optional[datetime] = None,
        before: Optional[datetime] = None,
        page: int = 1,
        per_page: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get user sport data list.

        Args:
            access_token: Access token
            after: Start date
            before: End date
            page: Page number
            per_page: Results per page

        Returns:
            List of activities
        """
        params = {
            'page': page,
            'pageSize': min(per_page, 100)
        }

        if after:
            params['startDate'] = after.strftime('%Y%m%d')
        if before:
            params['endDate'] = before.strftime('%Y%m%d')

        try:
            response = await self._make_coros_request(
                method='GET',
                url=f"{self.api_url}/sport/list",
                access_token=access_token,
                params=params
            )

            activities = response.get('data', {}).get('dataList', [])
            logger.info("coros_activities_fetched", count=len(activities), page=page)

            return activities

        except Exception as e:
            logger.error("coros_activities_fetch_failed", error=str(e))
            raise

    async def get_activity_detail(
        self,
        access_token: str,
        activity_id: str
    ) -> Dict[str, Any]:
        """
        Get detailed sport data.

        Args:
            access_token: Access token
            activity_id: Coros sport ID (label_id)

        Returns:
            Detailed activity data
        """
        try:
            response = await self._make_coros_request(
                method='GET',
                url=f"{self.api_url}/sport/detail",
                access_token=access_token,
                params={'labelId': activity_id}
            )

            logger.info("coros_activity_detail_fetched", activity_id=activity_id)
            return response.get('data', {})

        except Exception as e:
            logger.error("coros_activity_detail_failed", activity_id=activity_id, error=str(e))
            raise

    async def get_activity_streams(
        self,
        access_token: str,
        activity_id: str
    ) -> Dict[str, Any]:
        """
        Get sport file data (GPS track and detailed metrics).

        Args:
            access_token: Access token
            activity_id: Coros sport ID (label_id)

        Returns:
            Stream data including GPS track
        """
        try:
            response = await self._make_coros_request(
                method='GET',
                url=f"{self.api_url}/sport/file",
                access_token=access_token,
                params={'labelId': activity_id}
            )

            logger.info("coros_streams_fetched", activity_id=activity_id)
            return response.get('data', {})

        except Exception as e:
            logger.error("coros_streams_fetch_failed", activity_id=activity_id, error=str(e))
            return {}

    def normalize_activity(self, raw_activity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize Coros activity to Trainlytics format.

        Args:
            raw_activity: Raw Coros activity data

        Returns:
            Normalized activity data
        """
        # Coros uses timestamp in seconds
        start_timestamp = raw_activity.get('startTime', 0)
        start_date = datetime.fromtimestamp(start_timestamp) if start_timestamp else datetime.utcnow()

        return {
            'provider': 'COROS',
            'provider_activity_id': raw_activity.get('labelId', ''),

            # Basic info
            'name': raw_activity.get('sportName', 'Coros Activity'),
            'description': None,
            'activity_type': self._normalize_activity_type(raw_activity.get('mode', 0)),
            'sport_type': raw_activity.get('subMode'),

            # Date & Time
            'start_date': start_date,
            'timezone': None,

            # Metrics
            'duration_seconds': raw_activity.get('duration'),
            'distance_meters': raw_activity.get('distance'),
            'moving_time_seconds': None,

            # Elevation
            'elevation_gain_meters': raw_activity.get('totalUp'),
            'elevation_loss_meters': raw_activity.get('totalDown'),

            # Heart Rate
            'avg_heart_rate': raw_activity.get('avgHr'),
            'max_heart_rate': raw_activity.get('maxHr'),

            # Power
            'avg_power': raw_activity.get('avgPower'),
            'max_power': raw_activity.get('maxPower'),
            'normalized_power': None,

            # Speed
            'avg_speed_mps': raw_activity.get('avgPace'),
            'max_speed_mps': raw_activity.get('maxPace'),

            # Other
            'avg_cadence': raw_activity.get('avgCadence'),
            'avg_temperature': None,
            'calories': raw_activity.get('calorie'),

            # GPS
            'start_latlng': None,  # Would need to parse from file
            'end_latlng': None,

            # Flags
            'is_manual': False,
            'shared_with_coach': True,

            # Data quality
            'data_quality': self._assess_data_quality(raw_activity),
            'available_metrics': self._detect_available_metrics(raw_activity),

            # Raw data
            'raw_data': raw_activity
        }

    def _normalize_activity_type(self, mode: int) -> str:
        """
        Map Coros activity mode to Trainlytics types.

        Coros uses numeric mode codes.
        """
        # Common Coros modes (simplified)
        mode_mapping = {
            0: 'RUN',
            1: 'RIDE',
            2: 'SWIM',
            3: 'HIKE',
            4: 'WALK',
            5: 'WORKOUT',
        }
        return mode_mapping.get(mode, 'OTHER')

    def _assess_data_quality(self, activity: Dict[str, Any]) -> str:
        """Assess data quality."""
        has_distance = activity.get('distance') is not None
        has_duration = activity.get('duration') is not None
        has_hr = activity.get('avgHr') is not None

        if has_distance and has_duration and has_hr:
            return 'FULL'
        elif has_distance and has_duration:
            return 'PARTIAL'
        else:
            return 'MINIMAL'

    def _detect_available_metrics(self, activity: Dict[str, Any]) -> Dict[str, bool]:
        """Detect available metrics."""
        return {
            'duration': activity.get('duration') is not None,
            'distance': activity.get('distance') is not None,
            'heart_rate': activity.get('avgHr') is not None,
            'power': activity.get('avgPower') is not None,
            'cadence': activity.get('avgCadence') is not None,
            'elevation': activity.get('totalUp') is not None,
            'temperature': False,
            'gps': False,
            'calories': activity.get('calorie') is not None
        }

    async def handle_webhook(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process Coros webhook.

        Args:
            payload: Webhook payload

        Returns:
            Processed webhook data
        """
        logger.info("coros_webhook_received", payload=payload)

        # Coros webhook format (varies by event)
        return {
            'action': payload.get('event', 'create'),
            'provider_user_id': payload.get('openId', ''),
            'provider_activity_id': payload.get('labelId', ''),
        }

    def _generate_signature(self, timestamp: str) -> str:
        """
        Generate HMAC signature for Coros API requests.

        Args:
            timestamp: Current timestamp string

        Returns:
            HMAC signature
        """
        message = f"{settings.COROS_API_KEY}{timestamp}"
        signature = hmac.new(
            settings.COROS_API_SECRET.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()

        return signature

    async def _make_coros_request(
        self,
        method: str,
        url: str,
        access_token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make authenticated Coros API request.

        Args:
            method: HTTP method
            url: Request URL
            access_token: Access token
            **kwargs: Additional request parameters

        Returns:
            Response data
        """
        timestamp = str(int(time.time()))
        signature = self._generate_signature(timestamp)

        headers = {
            'Authorization': f'Bearer {access_token}',
            'timestamp': timestamp,
            'signature': signature,
            **kwargs.pop('headers', {})
        }

        try:
            response = await self.client.request(
                method=method,
                url=url,
                headers=headers,
                **kwargs
            )

            response.raise_for_status()
            data = response.json()

            if data.get('result') != '0000':
                raise Exception(f"Coros API error: {data.get('message')}")

            return data

        except httpx.HTTPStatusError as e:
            logger.error("coros_request_failed", status=e.response.status_code, error=e.response.text)
            raise
