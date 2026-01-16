"""Strava API connector implementation."""

from typing import Dict, List, Optional, Any
from datetime import datetime
import httpx

from app.services.connectors.base_connector import BaseConnector
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class StravaConnector(BaseConnector):
    """Connector for Strava API v3."""

    def __init__(self):
        super().__init__()
        self.provider_name = "strava"
        self.base_url = "https://www.strava.com/api/v3"
        self.auth_url = "https://www.strava.com/oauth"

    async def get_authorization_url(self, state: str, redirect_uri: str) -> str:
        """
        Generate Strava OAuth authorization URL.

        Args:
            state: CSRF token for security
            redirect_uri: Callback URL

        Returns:
            Authorization URL
        """
        params = {
            'client_id': settings.STRAVA_CLIENT_ID,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'activity:read_all,activity:write,profile:read_all',
            'state': state,
            'approval_prompt': 'auto'
        }

        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        url = f"{self.auth_url}/authorize?{query_string}"

        logger.info("strava_auth_url_generated", state=state)
        return url

    async def exchange_code(self, code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access tokens.

        Args:
            code: Authorization code from OAuth callback

        Returns:
            Dict containing tokens and athlete info
        """
        try:
            response = await self.client.post(
                f"{self.auth_url}/token",
                json={
                    'client_id': settings.STRAVA_CLIENT_ID,
                    'client_secret': settings.STRAVA_CLIENT_SECRET,
                    'code': code,
                    'grant_type': 'authorization_code'
                }
            )

            response.raise_for_status()
            data = response.json()

            logger.info("strava_token_exchange_success", athlete_id=data['athlete']['id'])

            return {
                'access_token': data['access_token'],
                'refresh_token': data['refresh_token'],
                'expires_at': data['expires_at'],
                'user_id': str(data['athlete']['id']),
                'user_info': {
                    'id': data['athlete']['id'],
                    'username': data['athlete']['username'],
                    'firstname': data['athlete']['firstname'],
                    'lastname': data['athlete']['lastname'],
                    'profile': data['athlete'].get('profile'),
                    'profile_medium': data['athlete'].get('profile_medium'),
                    'city': data['athlete'].get('city'),
                    'state': data['athlete'].get('state'),
                    'country': data['athlete'].get('country')
                }
            }

        except httpx.HTTPStatusError as e:
            logger.error("strava_token_exchange_failed", status=e.response.status_code)
            raise Exception(f"Strava token exchange failed: {e.response.text}")

    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh expired access token.

        Args:
            refresh_token: Refresh token

        Returns:
            Dict containing new tokens
        """
        try:
            response = await self.client.post(
                f"{self.auth_url}/token",
                json={
                    'client_id': settings.STRAVA_CLIENT_ID,
                    'client_secret': settings.STRAVA_CLIENT_SECRET,
                    'refresh_token': refresh_token,
                    'grant_type': 'refresh_token'
                }
            )

            response.raise_for_status()
            data = response.json()

            logger.info("strava_token_refreshed")

            return {
                'access_token': data['access_token'],
                'refresh_token': data['refresh_token'],
                'expires_at': data['expires_at']
            }

        except httpx.HTTPStatusError as e:
            logger.error("strava_token_refresh_failed", status=e.response.status_code)
            raise Exception(f"Strava token refresh failed: {e.response.text}")

    async def get_activities(
        self,
        access_token: str,
        after: Optional[datetime] = None,
        before: Optional[datetime] = None,
        page: int = 1,
        per_page: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get list of athlete activities.

        Args:
            access_token: Access token
            after: Start date filter
            before: End date filter
            page: Page number
            per_page: Results per page (max 200)

        Returns:
            List of activity summaries
        """
        params = {
            'page': page,
            'per_page': min(per_page, 200)
        }

        if after:
            params['after'] = int(after.timestamp())
        if before:
            params['before'] = int(before.timestamp())

        try:
            response = await self.make_request(
                method='GET',
                url=f"{self.base_url}/athlete/activities",
                access_token=access_token,
                params=params
            )

            logger.info(
                "strava_activities_fetched",
                count=len(response) if isinstance(response, list) else 0,
                page=page
            )

            return response if isinstance(response, list) else []

        except Exception as e:
            logger.error("strava_activities_fetch_failed", error=str(e))
            raise

    async def get_activity_detail(
        self,
        access_token: str,
        activity_id: str
    ) -> Dict[str, Any]:
        """
        Get detailed activity information.

        Args:
            access_token: Access token
            activity_id: Strava activity ID

        Returns:
            Detailed activity data
        """
        try:
            response = await self.make_request(
                method='GET',
                url=f"{self.base_url}/activities/{activity_id}",
                access_token=access_token,
                params={'include_all_efforts': 'true'}
            )

            logger.info("strava_activity_detail_fetched", activity_id=activity_id)
            return response

        except Exception as e:
            logger.error("strava_activity_detail_failed", activity_id=activity_id, error=str(e))
            raise

    async def get_activity_streams(
        self,
        access_token: str,
        activity_id: str
    ) -> Dict[str, Any]:
        """
        Get activity streams (detailed time-series data).

        Args:
            access_token: Access token
            activity_id: Strava activity ID

        Returns:
            Stream data keyed by type
        """
        stream_types = [
            'time', 'distance', 'latlng', 'altitude',
            'velocity_smooth', 'heartrate', 'cadence',
            'watts', 'temp', 'moving', 'grade_smooth'
        ]

        params = {
            'keys': ','.join(stream_types),
            'key_by_type': 'true'
        }

        try:
            response = await self.make_request(
                method='GET',
                url=f"{self.base_url}/activities/{activity_id}/streams",
                access_token=access_token,
                params=params
            )

            logger.info("strava_streams_fetched", activity_id=activity_id)
            return response

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.warning("strava_streams_not_available", activity_id=activity_id)
                return {}
            raise

    async def get_athlete_profile(self, access_token: str) -> Dict[str, Any]:
        """
        Get authenticated athlete's profile.

        Args:
            access_token: Access token

        Returns:
            Athlete profile data
        """
        try:
            response = await self.make_request(
                method='GET',
                url=f"{self.base_url}/athlete",
                access_token=access_token
            )

            logger.info("strava_athlete_profile_fetched", athlete_id=response.get('id'))
            return response

        except Exception as e:
            logger.error("strava_athlete_profile_failed", error=str(e))
            raise

    async def get_athlete_stats(self, access_token: str, athlete_id: str) -> Dict[str, Any]:
        """
        Get athlete statistics.

        Args:
            access_token: Access token
            athlete_id: Athlete ID

        Returns:
            Athlete statistics
        """
        try:
            response = await self.make_request(
                method='GET',
                url=f"{self.base_url}/athletes/{athlete_id}/stats",
                access_token=access_token
            )

            logger.info("strava_athlete_stats_fetched", athlete_id=athlete_id)
            return response

        except Exception as e:
            logger.error("strava_athlete_stats_failed", athlete_id=athlete_id, error=str(e))
            raise

    def normalize_activity(self, raw_activity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize Strava activity to Trainlytics format.

        Args:
            raw_activity: Raw Strava activity data

        Returns:
            Normalized activity data
        """
        return {
            'provider': 'STRAVA',
            'provider_activity_id': str(raw_activity['id']),

            # Basic info
            'name': raw_activity['name'],
            'description': raw_activity.get('description'),
            'activity_type': self._normalize_activity_type(raw_activity['type']),
            'sport_type': raw_activity.get('sport_type'),

            # Date & Time
            'start_date': datetime.fromisoformat(raw_activity['start_date'].replace('Z', '+00:00')),
            'timezone': raw_activity.get('timezone'),

            # Metrics
            'duration_seconds': raw_activity.get('elapsed_time'),
            'distance_meters': raw_activity.get('distance'),
            'moving_time_seconds': raw_activity.get('moving_time'),

            # Elevation
            'elevation_gain_meters': raw_activity.get('total_elevation_gain'),

            # Heart Rate
            'avg_heart_rate': raw_activity.get('average_heartrate'),
            'max_heart_rate': raw_activity.get('max_heartrate'),

            # Power
            'avg_power': raw_activity.get('average_watts'),
            'max_power': raw_activity.get('max_watts'),
            'normalized_power': raw_activity.get('weighted_average_watts'),

            # Speed
            'avg_speed_mps': raw_activity.get('average_speed'),
            'max_speed_mps': raw_activity.get('max_speed'),

            # Other
            'avg_cadence': raw_activity.get('average_cadence'),
            'avg_temperature': raw_activity.get('average_temp'),
            'calories': raw_activity.get('calories'),

            # GPS
            'start_latlng': raw_activity.get('start_latlng'),
            'end_latlng': raw_activity.get('end_latlng'),

            # Flags
            'is_manual': raw_activity.get('manual', False),
            'shared_with_coach': True,

            # Data quality
            'data_quality': self._assess_data_quality(raw_activity),
            'available_metrics': self._detect_available_metrics(raw_activity),

            # Raw data
            'raw_data': raw_activity
        }

    def _normalize_activity_type(self, strava_type: str) -> str:
        """Map Strava activity types to Trainlytics types."""
        type_mapping = {
            'Run': 'RUN',
            'TrailRun': 'RUN',
            'VirtualRun': 'RUN',
            'Ride': 'RIDE',
            'VirtualRide': 'RIDE',
            'GravelRide': 'RIDE',
            'MountainBikeRide': 'RIDE',
            'EBikeRide': 'RIDE',
            'Swim': 'SWIM',
            'Workout': 'WORKOUT',
            'WeightTraining': 'WORKOUT',
            'Crossfit': 'WORKOUT',
            'Walk': 'WALK',
            'Hike': 'HIKE',
        }
        return type_mapping.get(strava_type, 'OTHER')

    def _assess_data_quality(self, activity: Dict[str, Any]) -> str:
        """Assess the quality of activity data."""
        has_distance = activity.get('distance') is not None
        has_duration = activity.get('elapsed_time') is not None
        has_hr = activity.get('average_heartrate') is not None
        has_power = activity.get('average_watts') is not None
        has_gps = activity.get('start_latlng') is not None

        if has_distance and has_duration and (has_hr or has_power) and has_gps:
            return 'FULL'
        elif has_distance and has_duration:
            return 'PARTIAL'
        else:
            return 'MINIMAL'

    def _detect_available_metrics(self, activity: Dict[str, Any]) -> Dict[str, bool]:
        """Detect which metrics are available in the activity."""
        return {
            'duration': activity.get('elapsed_time') is not None,
            'distance': activity.get('distance') is not None,
            'heart_rate': activity.get('average_heartrate') is not None,
            'power': activity.get('average_watts') is not None,
            'cadence': activity.get('average_cadence') is not None,
            'elevation': activity.get('total_elevation_gain') is not None,
            'temperature': activity.get('average_temp') is not None,
            'gps': activity.get('start_latlng') is not None,
            'calories': activity.get('calories') is not None
        }

    async def handle_webhook(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process Strava webhook events.

        Webhook payload format:
        {
            "object_type": "activity",
            "aspect_type": "create|update|delete",
            "owner_id": 12345,
            "object_id": 67890,
            "subscription_id": 123,
            "event_time": 1549560669
        }

        Args:
            payload: Webhook payload

        Returns:
            Processed webhook data or None
        """
        object_type = payload.get('object_type')
        aspect_type = payload.get('aspect_type')
        owner_id = payload.get('owner_id')
        object_id = payload.get('object_id')

        if object_type != 'activity':
            logger.warning("strava_webhook_ignored", object_type=object_type)
            return None

        logger.info(
            "strava_webhook_received",
            aspect_type=aspect_type,
            owner_id=owner_id,
            object_id=object_id
        )

        return {
            'action': aspect_type,
            'provider_user_id': str(owner_id),
            'provider_activity_id': str(object_id),
            'event_time': payload.get('event_time')
        }

    async def deauthorize(self, access_token: str) -> bool:
        """
        Revoke access to athlete's Strava data.

        Args:
            access_token: Access token to revoke

        Returns:
            True if successful
        """
        try:
            response = await self.client.post(
                f"{self.auth_url}/deauthorize",
                headers={'Authorization': f'Bearer {access_token}'}
            )

            response.raise_for_status()
            logger.info("strava_deauthorization_success")
            return True

        except Exception as e:
            logger.error("strava_deauthorization_failed", error=str(e))
            return False
