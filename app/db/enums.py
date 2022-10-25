from enum import Enum


class NotificationType(str, Enum):
    base = 'base'
    quest_request = 'quest_request'
