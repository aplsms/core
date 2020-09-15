"""Clickatell platform for notify component."""
import logging

import requests
import voluptuous as vol

from homeassistant.components.notify import PLATFORM_SCHEMA, BaseNotificationService
from homeassistant.const import CONF_API_KEY, CONF_RECIPIENT, CONF_SENDER, HTTP_OK
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "clickatell"

BASE_API_URL = "https://platform.clickatell.com/messages/http/send"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Required(CONF_API_KEY): cv.string, vol.Required(CONF_RECIPIENT): cv.string, vol.Required(CONF_SENDER): cv.string})


def get_service(hass, config, discovery_info=None):
    """Get the Clickatell notification service."""
    return ClickatellNotificationService(config)


class ClickatellNotificationService(BaseNotificationService):
    """Implementation of a notification service for the Clickatell service."""

    def __init__(self, config):
        """Initialize the service."""
        self.api_key = config[CONF_API_KEY]
        self.recipient = config[CONF_RECIPIENT]
        self.sender = config[CONF_SENDER]

    def send_message(self, message="", **kwargs):
        """Send a message to a user."""
        data = {"apiKey": self.api_key, "to": self.recipient, "from":self.sender, "content": message}

        resp = requests.get(BASE_API_URL, params=data, timeout=5)
        if (resp.status_code != HTTP_OK) or (resp.status_code != 202):
            _LOGGER.error("Error %s : %s", resp.status_code, resp.text)
