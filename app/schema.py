import enum
from enum import auto
from functools import cached_property

from pydantic import BaseModel, computed_field

class GeminiModels(str, enum.Enum):
    TWO_FLASH = "gemini-2.0-flash"
    TWO_POINT_FIVE_FLASH = "gemini-2.5-flash"
    TWO_POINT_FIVE_PRO = "gemini-2.5-pro"
    THREE_FLASH_PREVIEW = "gemini-3-flash-preview"
    THREE_POINT_ONE_FLASH_LITE = "gemini-3.1-flash-lite"
    THREE_POINT_ONE_PRO_PREVIEW = "gemini-3.1-pro-preview"
    THREE_POINT_FIVE_FLASH = "gemini-3.5-flash"
    THREE_PRO_PREVIEW = "gemini-3-pro-preview"
