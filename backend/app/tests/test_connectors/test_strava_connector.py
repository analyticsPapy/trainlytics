"""Unit tests for Strava connector."""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

from app.services.connectors.strava_connector import StravaConnector


@pytest.fixture
def strava_connector():
    """Create a Strava connector instance."""
    return StravaConnector()


@pytest.fixture
def mock_strava_activity():
    """Mock Strava activity data."""
    return {
        'id': 123456789,
        'name': 'Morning Run',
        'type': 'Run',
        'sport_type': 'Run',
        'start_date': '2024-01-15T08:00:00Z',
        'timezone': 'America/Los_Angeles',
        'elapsed_time': 3600,
        'moving_time': 3500,
        'distance': 10000.0,
        'total_elevation_gain': 150.0,
        'average_heartrate': 145,
        'max_heartrate': 175,
        'average_watts': 250,
        'max_watts': 400,
        'weighted_average_watts': 270,
        'average_speed': 2.78,
        'max_speed': 4.0,
        'average_cadence': 85,
        'average_temp': 15,
        'calories': 650,
        'start_latlng': [37.7749, -122.4194],
        'end_latlng': [37.7849, -122.4094],
        'manual': False
    }


class TestStravaConnector:
    """Test suite for Strava connector."""

    @pytest.mark.asyncio
    async def test_get_authorization_url(self, strava_connector):
        """Test generation of authorization URL."""
        state = "test_state_123"
        redirect_uri = "http://localhost:8000/callback"

        url = await strava_connector.get_authorization_url(state, redirect_uri)

        assert "https://www.strava.com/oauth/authorize" in url
        assert f"state={state}" in url
        assert f"redirect_uri={redirect_uri}" in url
        assert "response_type=code" in url
        assert "scope=" in url

    @pytest.mark.asyncio
    async def test_exchange_code_success(self, strava_connector):
        """Test successful code exchange for tokens."""
        mock_response = {
            'access_token': 'test_access_token',
            'refresh_token': 'test_refresh_token',
            'expires_at': 1234567890,
            'athlete': {
                'id': 12345,
                'username': 'testuser',
                'firstname': 'Test',
                'lastname': 'User',
                'profile': 'https://example.com/profile.jpg'
            }
        }

        with patch.object(strava_connector.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value = MagicMock(
                status_code=200,
                json=lambda: mock_response
            )
            mock_post.return_value.raise_for_status = MagicMock()

            result = await strava_connector.exchange_code('test_code')

            assert result['access_token'] == 'test_access_token'
            assert result['refresh_token'] == 'test_refresh_token'
            assert result['user_id'] == '12345'
            assert result['user_info']['username'] == 'testuser'

    @pytest.mark.asyncio
    async def test_exchange_code_failure(self, strava_connector):
        """Test failed code exchange."""
        with patch.object(strava_connector.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.raise_for_status = MagicMock(
                side_effect=httpx.HTTPStatusError(
                    "Error",
                    request=MagicMock(),
                    response=MagicMock(status_code=400, text="Bad Request")
                )
            )

            with pytest.raises(Exception, match="Strava token exchange failed"):
                await strava_connector.exchange_code('invalid_code')

    @pytest.mark.asyncio
    async def test_refresh_access_token(self, strava_connector):
        """Test token refresh."""
        mock_response = {
            'access_token': 'new_access_token',
            'refresh_token': 'new_refresh_token',
            'expires_at': 1234567890
        }

        with patch.object(strava_connector.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value = MagicMock(
                json=lambda: mock_response
            )
            mock_post.return_value.raise_for_status = MagicMock()

            result = await strava_connector.refresh_access_token('old_refresh_token')

            assert result['access_token'] == 'new_access_token'
            assert result['refresh_token'] == 'new_refresh_token'

    @pytest.mark.asyncio
    async def test_get_activities(self, strava_connector, mock_strava_activity):
        """Test fetching activities list."""
        mock_response = [mock_strava_activity]

        with patch.object(strava_connector, 'make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            activities = await strava_connector.get_activities(
                access_token='test_token',
                page=1,
                per_page=30
            )

            assert len(activities) == 1
            assert activities[0]['id'] == 123456789
            mock_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_activities_with_date_filter(self, strava_connector):
        """Test fetching activities with date filters."""
        after = datetime(2024, 1, 1)
        before = datetime(2024, 1, 31)

        with patch.object(strava_connector, 'make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = []

            await strava_connector.get_activities(
                access_token='test_token',
                after=after,
                before=before
            )

            call_args = mock_request.call_args
            assert 'params' in call_args.kwargs
            params = call_args.kwargs['params']
            assert 'after' in params
            assert 'before' in params
            assert params['after'] == int(after.timestamp())
            assert params['before'] == int(before.timestamp())

    @pytest.mark.asyncio
    async def test_get_activity_detail(self, strava_connector, mock_strava_activity):
        """Test fetching detailed activity information."""
        with patch.object(strava_connector, 'make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_strava_activity

            activity = await strava_connector.get_activity_detail(
                access_token='test_token',
                activity_id='123456789'
            )

            assert activity['id'] == 123456789
            assert activity['name'] == 'Morning Run'

    @pytest.mark.asyncio
    async def test_get_activity_streams(self, strava_connector):
        """Test fetching activity streams."""
        mock_streams = {
            'time': {'data': [0, 1, 2, 3]},
            'distance': {'data': [0, 100, 200, 300]},
            'heartrate': {'data': [120, 145, 150, 145]},
            'latlng': {'data': [[37.7749, -122.4194], [37.7750, -122.4195]]}
        }

        with patch.object(strava_connector, 'make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_streams

            streams = await strava_connector.get_activity_streams(
                access_token='test_token',
                activity_id='123456789'
            )

            assert 'time' in streams
            assert 'heartrate' in streams
            assert len(streams['time']['data']) == 4

    @pytest.mark.asyncio
    async def test_get_athlete_profile(self, strava_connector):
        """Test fetching athlete profile."""
        mock_profile = {
            'id': 12345,
            'username': 'testuser',
            'firstname': 'Test',
            'lastname': 'User',
            'city': 'San Francisco',
            'state': 'California'
        }

        with patch.object(strava_connector, 'make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_profile

            profile = await strava_connector.get_athlete_profile('test_token')

            assert profile['id'] == 12345
            assert profile['username'] == 'testuser'

    def test_normalize_activity(self, strava_connector, mock_strava_activity):
        """Test activity normalization."""
        normalized = strava_connector.normalize_activity(mock_strava_activity)

        assert normalized['provider'] == 'STRAVA'
        assert normalized['provider_activity_id'] == '123456789'
        assert normalized['name'] == 'Morning Run'
        assert normalized['activity_type'] == 'RUN'
        assert normalized['duration_seconds'] == 3600
        assert normalized['distance_meters'] == 10000.0
        assert normalized['avg_heart_rate'] == 145
        assert normalized['data_quality'] == 'FULL'
        assert normalized['is_manual'] == False

    def test_normalize_activity_type(self, strava_connector):
        """Test activity type normalization."""
        assert strava_connector._normalize_activity_type('Run') == 'RUN'
        assert strava_connector._normalize_activity_type('TrailRun') == 'RUN'
        assert strava_connector._normalize_activity_type('Ride') == 'RIDE'
        assert strava_connector._normalize_activity_type('VirtualRide') == 'RIDE'
        assert strava_connector._normalize_activity_type('Swim') == 'SWIM'
        assert strava_connector._normalize_activity_type('Walk') == 'WALK'
        assert strava_connector._normalize_activity_type('Hike') == 'HIKE'
        assert strava_connector._normalize_activity_type('Unknown') == 'OTHER'

    def test_assess_data_quality_full(self, strava_connector):
        """Test data quality assessment - FULL."""
        activity = {
            'distance': 10000,
            'elapsed_time': 3600,
            'average_heartrate': 145,
            'start_latlng': [37.7749, -122.4194]
        }

        quality = strava_connector._assess_data_quality(activity)
        assert quality == 'FULL'

    def test_assess_data_quality_partial(self, strava_connector):
        """Test data quality assessment - PARTIAL."""
        activity = {
            'distance': 10000,
            'elapsed_time': 3600
        }

        quality = strava_connector._assess_data_quality(activity)
        assert quality == 'PARTIAL'

    def test_assess_data_quality_minimal(self, strava_connector):
        """Test data quality assessment - MINIMAL."""
        activity = {}

        quality = strava_connector._assess_data_quality(activity)
        assert quality == 'MINIMAL'

    def test_detect_available_metrics(self, strava_connector, mock_strava_activity):
        """Test metrics detection."""
        metrics = strava_connector._detect_available_metrics(mock_strava_activity)

        assert metrics['duration'] == True
        assert metrics['distance'] == True
        assert metrics['heart_rate'] == True
        assert metrics['power'] == True
        assert metrics['cadence'] == True
        assert metrics['elevation'] == True
        assert metrics['gps'] == True

    @pytest.mark.asyncio
    async def test_handle_webhook_activity_create(self, strava_connector):
        """Test webhook handling for activity creation."""
        webhook_payload = {
            'object_type': 'activity',
            'aspect_type': 'create',
            'owner_id': 12345,
            'object_id': 67890,
            'subscription_id': 123,
            'event_time': 1549560669
        }

        result = await strava_connector.handle_webhook(webhook_payload)

        assert result is not None
        assert result['action'] == 'create'
        assert result['provider_user_id'] == '12345'
        assert result['provider_activity_id'] == '67890'

    @pytest.mark.asyncio
    async def test_handle_webhook_non_activity(self, strava_connector):
        """Test webhook handling for non-activity events."""
        webhook_payload = {
            'object_type': 'athlete',
            'aspect_type': 'update',
            'owner_id': 12345
        }

        result = await strava_connector.handle_webhook(webhook_payload)

        assert result is None

    @pytest.mark.asyncio
    async def test_deauthorize(self, strava_connector):
        """Test deauthorization."""
        with patch.object(strava_connector.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value = MagicMock()
            mock_post.return_value.raise_for_status = MagicMock()

            success = await strava_connector.deauthorize('test_token')

            assert success == True
            mock_post.assert_called_once()

    @pytest.mark.asyncio
    async def test_make_request_with_token_expired(self, strava_connector):
        """Test request handling when token is expired."""
        with patch.object(strava_connector.client, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value.raise_for_status = MagicMock(
                side_effect=httpx.HTTPStatusError(
                    "Unauthorized",
                    request=MagicMock(),
                    response=MagicMock(status_code=401)
                )
            )

            with pytest.raises(Exception, match="TOKEN_EXPIRED"):
                await strava_connector.make_request(
                    method='GET',
                    url='https://api.strava.com/v3/athlete',
                    access_token='expired_token'
                )

    @pytest.mark.asyncio
    async def test_make_request_rate_limit(self, strava_connector):
        """Test request handling when rate limited."""
        with patch.object(strava_connector.client, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value.raise_for_status = MagicMock(
                side_effect=httpx.HTTPStatusError(
                    "Rate Limited",
                    request=MagicMock(),
                    response=MagicMock(status_code=429)
                )
            )

            with pytest.raises(Exception, match="RATE_LIMIT_EXCEEDED"):
                await strava_connector.make_request(
                    method='GET',
                    url='https://api.strava.com/v3/athlete',
                    access_token='test_token'
                )
