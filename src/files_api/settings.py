from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """
    Settings for the files API.

    Pydantic BaseSettings docs: https://docs.pydantic.dev/latest/concepts/pydantic_settings/#usage
    FastAPI guide to managing settings: https://fastapi.tiangolo.com/advanced/settings/
    """
        
    s3_bucket_name: str = Field(default="cloud-course-bucket-ddde")
    root_path: str = "/prod"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"  # Allow extra fields to handle all the environment variables
    )
