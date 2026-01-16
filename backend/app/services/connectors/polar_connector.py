"""Polar AccessLink API connector implementation."""

from typing import Dict, List, Optional, Any
from datetime import datetime
import httpx

from app.services.connectors.base_connector import BaseConnector
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class PolarConnector(BaseConnector):
    """Connector for Polar AccessLink API (OAuth 2.0)."""

    def __init__(self):
        super().__init__()
        self.provider_name = "polar"
        self.base_url = "https://www.polaraccesslink.com/v3"
        self.auth_url = "https://flow.polar.com/oauth2"

    async def get_authorization_url(self, state: str, redirect_uri: str) -> str:
        """
        Generate Polar OAuth authorization URL.

        Args:
            state: CSRF token
            redirect_uri: Callback URL

        Returns:
            Authorization URL
        """
        params = {
            'client_id': settings.POLAR_CLIENT_ID,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'accesslink.read_all',
            'state': state
        }

        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        url = f"{self.auth_url}/authorization?{query_string}"

        logger.info("polar_auth_url_generated", state=state)
        return url

    async def exchange_code(self, code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access tokens.

        Args:
            code: Authorization code

        Returns:
            Dict containing tokens and user info
        """
        try:
            response = await self.client.post(
                f"{self.auth_url}/token",
                data={
                    'grant_type': 'authorization_code',
                    'code': code,
                    'client_id': settings.POLAR_CLIENT_ID,
                    'client_secret': settings.POLAR_CLIENT_SECRET
                },
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )

            response.raise_for_status()
            data = response.json()

            # Get user info
            user_id = data.get('x_user_id', '')

            logger.info("polar_token_exchange_success", user_id=user_id)

            # Register user (required by Polar AccessLink API)
            await self._register_user(data['access_token'], user_id)

            return {
                'access_token': data['access_token'],
                'refresh_token': None,  # Polar doesn't use refresh tokens
                'expires_at': None,  # Tokens don't expire
                'user_id': user_id,
                'user_info': {
                    'id': user_id,
                    'member_id': data.get('x_user_id')
                }
            }

        except httpx.HTTPStatusError as e:
            logger.error("polar_token_exchange_failed", status=e.response.status_code, error=e.response.text)
            raise Exception(f"Polar token exchange failed: {e.response.text}")

    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Polar tokens don't expire, so this is a no-op.

        Args:
            refresh_token: Not used

        Returns:
            Empty dict
        """
        logger.info("polar_token_refresh_skipped", reason="tokens_no_expiry")
        return {}

    async def _register_user(self, access_token: str, user_id: str) -> bool:
        """
        Register user with Polar AccessLink (required step).

        Args:
            access_token: Access token
            user_id: Polar user ID

        Returns:
            True if successful
        """
        try:
            response = await self.client.post(
                f"{self.base_url}/users",
                json={'member-id': user_id},
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }
            )

            # 200 = registered, 409 = already registered (both OK)
            if response.status_code in [200, 409]:
                logger.info("polar_user_registered", user_id=user_id)
                return True
            else:
                logger.warning("polar_user_registration_failed", status=response.status_code)
                return False

        except Exception as e:
            logger.error("polar_user_registration_error", error=str(e))
            return False

    async def get_activities(
        self,
        access_token: str,
        after: Optional[datetime] = None,
        before: Optional[datetime] = None,
        page: int = 1,
        per_page: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get user exercise list.

        Polar AccessLink uses a transaction-based system:
        1. Create transaction
        2. List exercises in transaction
        3. Commit transaction

        Args:
            access_token: Access token
            after: Not used (Polar doesn't support date filtering)
            before: Not used
            page: Not used
            per_page: Not used

        Returns:
            List of exercises
        """
        try:
            # Step 1: Create transaction
            transaction_response = await self.make_request(
                method='POST',
                url=f"{self.base_url}/users/exercises/transactions",
                access_token=access_token
            )

            transaction_id = transaction_response.get('transaction-id')
            resource_uri = transaction_response.get('resource-uri')

            if not transaction_id:
                logger.warning("polar_no_new_exercises")
                return []

            # Step 2: List exercises
            exercises_response = await self.make_request(
                method='GET',
                url=resource_uri,
                access_token=access_token
            )

            exercises = exercises_response.get('exercises', [])
            logger.info("polar_exercises_fetched", count=len(exercises), transaction_id=transaction_id)

            # Step 3: Commit transaction (to mark as read)
            await self.client.put(
                f"{self.base_url}/users/exercises/transactions/{transaction_id}",
                headers={'Authorization': f'Bearer {access_token}'}
            )

            return exercises

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 204:
                # No new exercises available
                logger.info("polar_no_new_exercises")
                return []
            logger.error("polar_exercises_fetch_failed", status=e.response.status_code)
            raise

    async def get_activity_detail(
        self,
        access_token: str,
        activity_id: str
    ) -> Dict[str, Any]:
        """
        Get detailed exercise information.

        Args:
            access_token: Access token
            activity_id: Polar exercise ID (URL)

        Returns:
            Detailed exercise data
        """
        try:
            # activity_id is actually a full URL in Polar API
            response = await self.make_request(
                method='GET',
                url=activity_id,
                access_token=access_token
            )

            logger.info("polar_exercise_detail_fetched")
            return response

        except Exception as e:
            logger.error("polar_exercise_detail_failed", error=str(e))
            raise

    async def get_activity_streams(
        self,
        access_token: str,
        activity_id: str
    ) -> Dict[str, Any]:
        """
        Get exercise samples (time-series data).

        Args:
            access_token: Access token
            activity_id: Exercise URL

        Returns:
            Sample data
        """
        try:
            # Get exercise detail which includes samples URL
            exercise = await self.get_activity_detail(access_token, activity_id)
            samples_url = exercise.get('samples')

            if not samples_url:
                logger.warning("polar_no_samples_available")
                return {}

            response = await self.make_request(
                method='GET',
                url=samples_url,
                access_token=access_token
            )

            logger.info("polar_samples_fetched")
            return response

        except Exception as e:
            logger.error("polar_samples_fetch_failed", error=str(e))
            return {}

    def normalize_activity(self, raw_activity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize Polar exercise to Trainlytics format.

        Args:
            raw_activity: Raw Polar exercise data

        Returns:
            Normalized activity data
        """
        # Polar uses ISO format for dates
        start_time_str = raw_activity.get('start-time', '')
        start_date = datetime.fromisoformat(start_time_str.replace('Z', '+00:00')) if start_time_str else datetime.utcnow()

        return {
            'provider': 'POLAR',
            'provider_activity_id': raw_activity.get('id', ''),

            # Basic info
            'name': f"Polar {raw_activity.get('sport', 'Exercise')}",
            'description': None,
            'activity_type': self._normalize_activity_type(raw_activity.get('sport', '')),
            'sport_type': raw_activity.get('sport'),

            # Date & Time
            'start_date': start_date,
            'timezone': None,

            # Metrics
            'duration_seconds': self._parse_duration(raw_activity.get('duration', '')),
            'distance_meters': raw_activity.get('distance'),
            'moving_time_seconds': None,

            # Elevation
            'elevation_gain_meters': raw_activity.get('ascent'),
            'elevation_loss_meters': raw_activity.get('descent'),

            # Heart Rate
            'avg_heart_rate': raw_activity.get('heart-rate', {}).get('average'),
            'max_heart_rate': raw_activity.get('heart-rate', {}).get('maximum'),

            # Power
            'avg_power': None,
            'max_power': None,
            'normalized_power': None,

            # Speed
            'avg_speed_mps': None,
            'max_speed_mps': None,

            # Other
            'avg_cadence': None,
            'avg_temperature': None,
            'calories': raw_activity.get('calories'),

            # GPS
            'start_latlng': None,
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

    def _normalize_activity_type(self, polar_sport: str) -> str:
        """Map Polar sport types to Trainlytics types."""
        type_mapping = {
            'RUNNING': 'RUN',
            'CYCLING': 'RIDE',
            'SWIMMING': 'SWIM',
            'WALKING': 'WALK',
            'HIKING': 'HIKE',
            'FITNESS': 'WORKOUT',
            'STRENGTH_TRAINING': 'WORKOUT',
        }
        return type_mapping.get(polar_sport.upper(), 'OTHER')

    def _parse_duration(self, duration_str: str) -> Optional[int]:
        """
        Parse Polar duration format (PT1H30M45S) to seconds.

        Args:
            duration_str: ISO 8601 duration string

        Returns:
            Duration in seconds
        """
        if not duration_str or not duration_str.startswith('PT'):
            return None

        try:
            duration_str = duration_str[2:]  # Remove 'PT'
            hours = minutes = seconds = 0

            if 'H' in duration_str:
                hours_str, duration_str = duration_str.split('H')
                hours = int(hours_str)

            if 'M' in duration_str:
                minutes_str, duration_str = duration_str.split('M')
                minutes = int(minutes_str)

            if 'S' in duration_str:
                seconds_str = duration_str.split('S')[0]
                seconds = int(float(seconds_str))

            return hours * 3600 + minutes * 60 + seconds

        except Exception as e:
            logger.warning("polar_duration_parse_failed", duration=duration_str, error=str(e))
            return None

    def _assess_data_quality(self, activity: Dict[str, Any]) -> str:
        """Assess data quality."""
        has_duration = activity.get('duration') is not None
        has_distance = activity.get('distance') is not None
        has_hr = activity.get('heart-rate', {}).get('average') is not None

        if has_duration and has_distance and has_hr:
            return 'FULL'
        elif has_duration:
            return 'PARTIAL'
        else:
            return 'MINIMAL'

    def _detect_available_metrics(self, activity: Dict[str, Any]) -> Dict[str, bool]:
        """Detect available metrics."""
        return {
            'duration': activity.get('duration') is not None,
            'distance': activity.get('distance') is not None,
            'heart_rate': activity.get('heart-rate', {}).get('average') is not None,
            'power': False,
            'cadence': False,
            'elevation': activity.get('ascent') is not None,
            'temperature': False,
            'gps': False,
            'calories': activity.get('calories') is not None
        }

    async def handle_webhook(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Polar doesn't support webhooks.
        Data must be pulled via transactions.

        Args:
            payload: Not used

        Returns:
            None
        """
        logger.warning("polar_webhooks_not_supported")
        return None
