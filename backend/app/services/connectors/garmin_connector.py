"""Garmin Connect API connector implementation."""

from typing import Dict, List, Optional, Any
from datetime import datetime
import httpx
from oauthlib.oauth1 import Client as OAuth1Client

from app.services.connectors.base_connector import BaseConnector
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class GarminConnector(BaseConnector):
    """Connector for Garmin Connect API (OAuth 1.0a)."""

    def __init__(self):
        super().__init__()
        self.provider_name = "garmin"
        self.base_url = "https://apis.garmin.com/wellness-api/rest"
        self.auth_url = "https://connectapi.garmin.com/oauth-service"

    async def get_authorization_url(self, state: str, redirect_uri: str) -> str:
        """
        Generate Garmin OAuth 1.0a authorization URL.

        Args:
            state: CSRF token
            redirect_uri: Callback URL

        Returns:
            Authorization URL with request token
        """
        # Step 1: Get request token
        oauth_client = OAuth1Client(
            client_key=settings.GARMIN_CONSUMER_KEY,
            client_secret=settings.GARMIN_CONSUMER_SECRET,
            callback_uri=redirect_uri
        )

        uri = f"{self.auth_url}/oauth/request_token"
        uri, headers, body = oauth_client.sign(uri, http_method='POST')

        try:
            response = await self.client.post(uri, headers=headers)
            response.raise_for_status()

            # Parse OAuth response
            credentials = dict(param.split('=') for param in response.text.split('&'))
            request_token = credentials.get('oauth_token')
            request_token_secret = credentials.get('oauth_token_secret')

            # Store secret temporarily (in Redis in production)
            # For now, include in state
            encoded_state = f"{state}:{request_token_secret}"

            auth_url = (
                f"{self.auth_url}/oauth/authorize"
                f"?oauth_token={request_token}"
                f"&oauth_callback={redirect_uri}"
            )

            logger.info("garmin_auth_url_generated", request_token=request_token)
            return auth_url

        except Exception as e:
            logger.error("garmin_request_token_failed", error=str(e))
            raise Exception(f"Garmin request token failed: {str(e)}")

    async def exchange_code(self, oauth_token: str, oauth_verifier: str, token_secret: str) -> Dict[str, Any]:
        """
        Exchange OAuth verifier for access tokens.

        Args:
            oauth_token: OAuth token from callback
            oauth_verifier: OAuth verifier from callback
            token_secret: Request token secret (from state)

        Returns:
            Dict containing tokens and user info
        """
        try:
            oauth_client = OAuth1Client(
                client_key=settings.GARMIN_CONSUMER_KEY,
                client_secret=settings.GARMIN_CONSUMER_SECRET,
                resource_owner_key=oauth_token,
                resource_owner_secret=token_secret,
                verifier=oauth_verifier
            )

            uri = f"{self.auth_url}/oauth/access_token"
            uri, headers, body = oauth_client.sign(uri, http_method='POST')

            response = await self.client.post(uri, headers=headers)
            response.raise_for_status()

            # Parse OAuth response
            credentials = dict(param.split('=') for param in response.text.split('&'))
            access_token = credentials.get('oauth_token')
            access_token_secret = credentials.get('oauth_token_secret')

            # Garmin doesn't return user ID in token exchange, get it from profile
            user_profile = await self.get_user_profile(access_token, access_token_secret)

            logger.info("garmin_token_exchange_success")

            return {
                'access_token': access_token,
                'refresh_token': access_token_secret,  # OAuth 1.0a doesn't expire
                'expires_at': None,  # OAuth 1.0a tokens don't expire
                'user_id': user_profile.get('userId', ''),
                'user_info': user_profile
            }

        except Exception as e:
            logger.error("garmin_token_exchange_failed", error=str(e))
            raise Exception(f"Garmin token exchange failed: {str(e)}")

    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        OAuth 1.0a tokens don't expire, so this is a no-op.

        Args:
            refresh_token: Not used

        Returns:
            Empty dict (tokens don't need refreshing)
        """
        logger.info("garmin_token_refresh_skipped", reason="oauth1_no_expiry")
        return {}

    async def get_user_profile(self, access_token: str, access_token_secret: str) -> Dict[str, Any]:
        """
        Get Garmin user profile.

        Args:
            access_token: OAuth access token
            access_token_secret: OAuth access token secret

        Returns:
            User profile data
        """
        try:
            response = await self._make_oauth1_request(
                method='GET',
                url=f"{self.base_url}/user/id",
                access_token=access_token,
                access_token_secret=access_token_secret
            )

            logger.info("garmin_user_profile_fetched")
            return response

        except Exception as e:
            logger.error("garmin_user_profile_failed", error=str(e))
            raise

    async def get_activities(
        self,
        access_token: str,
        access_token_secret: str,
        after: Optional[datetime] = None,
        before: Optional[datetime] = None,
        page: int = 1,
        per_page: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get user activities.

        Args:
            access_token: OAuth access token
            access_token_secret: OAuth access token secret
            after: Start date
            before: End date
            page: Page number
            per_page: Results per page

        Returns:
            List of activities
        """
        params = {
            'uploadStartTimeInSeconds': int(after.timestamp()) if after else None,
            'uploadEndTimeInSeconds': int(before.timestamp()) if before else None,
        }

        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        try:
            response = await self._make_oauth1_request(
                method='GET',
                url=f"{self.base_url}/activities",
                access_token=access_token,
                access_token_secret=access_token_secret,
                params=params
            )

            activities = response if isinstance(response, list) else []
            logger.info("garmin_activities_fetched", count=len(activities))

            return activities

        except Exception as e:
            logger.error("garmin_activities_fetch_failed", error=str(e))
            raise

    async def get_activity_detail(
        self,
        access_token: str,
        access_token_secret: str,
        activity_id: str
    ) -> Dict[str, Any]:
        """
        Get detailed activity information.

        Args:
            access_token: OAuth access token
            access_token_secret: OAuth access token secret
            activity_id: Garmin activity ID

        Returns:
            Detailed activity data
        """
        try:
            response = await self._make_oauth1_request(
                method='GET',
                url=f"{self.base_url}/activities/{activity_id}",
                access_token=access_token,
                access_token_secret=access_token_secret
            )

            logger.info("garmin_activity_detail_fetched", activity_id=activity_id)
            return response

        except Exception as e:
            logger.error("garmin_activity_detail_failed", activity_id=activity_id, error=str(e))
            raise

    async def get_activity_streams(
        self,
        access_token: str,
        access_token_secret: str,
        activity_id: str
    ) -> Dict[str, Any]:
        """
        Garmin API doesn't provide stream data in the same way as Strava.
        Returns empty dict.
        """
        logger.warning("garmin_streams_not_supported", activity_id=activity_id)
        return {}

    def normalize_activity(self, raw_activity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize Garmin activity to Trainlytics format.

        Args:
            raw_activity: Raw Garmin activity data

        Returns:
            Normalized activity data
        """
        return {
            'provider': 'GARMIN',
            'provider_activity_id': str(raw_activity.get('activityId', '')),

            # Basic info
            'name': raw_activity.get('activityName', 'Garmin Activity'),
            'description': raw_activity.get('description'),
            'activity_type': self._normalize_activity_type(raw_activity.get('activityType', '')),
            'sport_type': raw_activity.get('activityType'),

            # Date & Time
            'start_date': datetime.fromtimestamp(raw_activity.get('startTimeInSeconds', 0)),
            'timezone': None,

            # Metrics
            'duration_seconds': raw_activity.get('durationInSeconds'),
            'distance_meters': raw_activity.get('distanceInMeters'),
            'moving_time_seconds': raw_activity.get('activeTimeInSeconds'),

            # Elevation
            'elevation_gain_meters': raw_activity.get('elevationGainInMeters'),
            'elevation_loss_meters': raw_activity.get('elevationLossInMeters'),

            # Heart Rate
            'avg_heart_rate': raw_activity.get('averageHeartRateInBeatsPerMinute'),
            'max_heart_rate': raw_activity.get('maxHeartRateInBeatsPerMinute'),

            # Power
            'avg_power': raw_activity.get('averagePowerInWatts'),
            'max_power': raw_activity.get('maxPowerInWatts'),
            'normalized_power': None,

            # Speed
            'avg_speed_mps': raw_activity.get('averageSpeedInMetersPerSecond'),
            'max_speed_mps': raw_activity.get('maxSpeedInMetersPerSecond'),

            # Other
            'avg_cadence': raw_activity.get('averageRunCadenceInStepsPerMinute'),
            'avg_temperature': None,
            'calories': raw_activity.get('activeKilocalories'),

            # GPS
            'start_latlng': [
                raw_activity.get('startingLatitudeInDegree'),
                raw_activity.get('startingLongitudeInDegree')
            ] if raw_activity.get('startingLatitudeInDegree') else None,
            'end_latlng': None,

            # Flags
            'is_manual': raw_activity.get('manual', False),
            'shared_with_coach': True,

            # Data quality
            'data_quality': self._assess_data_quality(raw_activity),
            'available_metrics': self._detect_available_metrics(raw_activity),

            # Raw data
            'raw_data': raw_activity
        }

    def _normalize_activity_type(self, garmin_type: str) -> str:
        """Map Garmin activity types to Trainlytics types."""
        type_mapping = {
            'RUNNING': 'RUN',
            'CYCLING': 'RIDE',
            'SWIMMING': 'SWIM',
            'WALKING': 'WALK',
            'HIKING': 'HIKE',
            'FITNESS_EQUIPMENT': 'WORKOUT',
            'STRENGTH_TRAINING': 'WORKOUT',
        }
        return type_mapping.get(garmin_type.upper(), 'OTHER')

    def _assess_data_quality(self, activity: Dict[str, Any]) -> str:
        """Assess data quality."""
        has_distance = activity.get('distanceInMeters') is not None
        has_duration = activity.get('durationInSeconds') is not None
        has_hr = activity.get('averageHeartRateInBeatsPerMinute') is not None

        if has_distance and has_duration and has_hr:
            return 'FULL'
        elif has_distance and has_duration:
            return 'PARTIAL'
        else:
            return 'MINIMAL'

    def _detect_available_metrics(self, activity: Dict[str, Any]) -> Dict[str, bool]:
        """Detect available metrics."""
        return {
            'duration': activity.get('durationInSeconds') is not None,
            'distance': activity.get('distanceInMeters') is not None,
            'heart_rate': activity.get('averageHeartRateInBeatsPerMinute') is not None,
            'power': activity.get('averagePowerInWatts') is not None,
            'cadence': activity.get('averageRunCadenceInStepsPerMinute') is not None,
            'elevation': activity.get('elevationGainInMeters') is not None,
            'temperature': False,
            'gps': activity.get('startingLatitudeInDegree') is not None,
            'calories': activity.get('activeKilocalories') is not None
        }

    async def handle_webhook(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process Garmin webhook (push notifications).

        Args:
            payload: Webhook payload

        Returns:
            Processed webhook data
        """
        logger.info("garmin_webhook_received", payload=payload)

        # Garmin sends different webhook formats
        # This is a simplified implementation
        return {
            'action': 'create',
            'provider_user_id': payload.get('userId', ''),
            'provider_activity_id': payload.get('activityId', ''),
        }

    async def _make_oauth1_request(
        self,
        method: str,
        url: str,
        access_token: str,
        access_token_secret: str,
        **kwargs
    ) -> Any:
        """
        Make OAuth 1.0a signed request.

        Args:
            method: HTTP method
            url: Request URL
            access_token: OAuth access token
            access_token_secret: OAuth access token secret
            **kwargs: Additional request parameters

        Returns:
            Response data
        """
        oauth_client = OAuth1Client(
            client_key=settings.GARMIN_CONSUMER_KEY,
            client_secret=settings.GARMIN_CONSUMER_SECRET,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret
        )

        uri, headers, body = oauth_client.sign(url, http_method=method, **kwargs)

        try:
            response = await self.client.request(method, uri, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            logger.error("garmin_request_failed", status=e.response.status_code, error=e.response.text)
            raise
