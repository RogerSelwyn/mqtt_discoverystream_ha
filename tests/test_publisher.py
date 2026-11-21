"""Regression tests for scheduled discovery recovery."""

# ruff: noqa: PT009, PT027, SLF001

import asyncio
from datetime import timedelta
import unittest
from unittest.mock import AsyncMock, Mock, patch

from custom_components.mqtt_discoverystream_alt.const import CONF_REPUBLISH_TIME
from custom_components.mqtt_discoverystream_alt.publisher import Publisher
from homeassistant.exceptions import HomeAssistantError


class TestScheduledPublish(unittest.IsolatedAsyncioTestCase):
    """Keep retries running without swallowing cancellation."""

    def setUp(self):
        """Avoid registering HA listeners in these callback tests."""
        self.publisher = Publisher.__new__(Publisher)
        self.publisher._hass = Mock()
        self.interval = timedelta(minutes=5)
        self.publisher._conf = {CONF_REPUBLISH_TIME: self.interval}
        self.publisher.async_publish_discovery_state = AsyncMock()
        schedule_patch = patch("custom_components.mqtt_discoverystream_alt.publisher.async_call_later")
        self.addCleanup(schedule_patch.stop)
        self.schedule = schedule_patch.start()
        logger_patch = patch("custom_components.mqtt_discoverystream_alt.publisher._LOGGER")
        self.addCleanup(logger_patch.stop)
        self.logger = logger_patch.start()

    async def test_success_schedules_next_publish(self):
        """A normal run retains the configured interval."""
        await self.publisher._async_schedule_publish(None)

        self.publisher.async_publish_discovery_state.assert_awaited_once_with()
        self.schedule.assert_called_once_with(
            self.publisher._hass,
            self.interval,
            self.publisher._async_schedule_publish,
        )
        self.logger.exception.assert_not_called()

    async def test_mqtt_failure_then_recovery(self):
        """A failed TaskGroup must not prevent the next successful run."""
        self.publisher.async_publish_discovery_state.side_effect = [
            ExceptionGroup("publish failed", [HomeAssistantError("MQTT disconnected")]),
            None,
        ]

        await self.publisher._async_schedule_publish(None)
        self.schedule.assert_called_once()
        self.logger.exception.assert_called_once()

        callback = self.schedule.call_args.args[2]
        await callback(None)

        self.assertEqual(self.publisher.async_publish_discovery_state.await_count, 2)
        self.assertEqual(self.schedule.call_count, 2)
        self.assertEqual(self.schedule.call_args.args[1], self.interval)

    async def test_cancellation_does_not_schedule_retry(self):
        """Shutdown cancellation propagates without registering another timer."""
        self.publisher.async_publish_discovery_state.side_effect = asyncio.CancelledError

        with self.assertRaises(asyncio.CancelledError):
            await self.publisher._async_schedule_publish(None)

        self.schedule.assert_not_called()
        self.logger.exception.assert_not_called()
