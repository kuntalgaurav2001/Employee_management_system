from django.apps import AppConfig
from typing import Any


class PeoplesConfig(AppConfig):
    default_auto_field: Any = "django.db.models.BigAutoField"
    name = "peoples"
