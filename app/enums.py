from enum import Enum


class PlatformEnum(Enum):
    WEB = 'web'
    EMAIL = 'email'


class EventEnum(Enum):
    OPEN = 'open'
    CLICK_BUTTON_1 = 'click_button_1'
    CLICK_BUTTON_2 = 'click_button_2'
