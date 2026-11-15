from pydantic import BaseModel, field_validator
from typing import Optional
import re


class PostingRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def validate_message(cls, v):
        # Rule 1: Must not be empty
        if not v or not v.strip():
            raise ValueError("Message cannot be empty.")

        # Rule 2: Max 200 characters
        if len(v) > 200:
            raise ValueError(
                f"Message too long: {len(v)} characters. Maximum allowed is 200."
            )

        # Rule 3: Must contain exactly 1 URL
        url_pattern = r'https?://[^\s]+'
        urls_found = re.findall(url_pattern, v)

        if len(urls_found) == 0:
            raise ValueError(
                "Message must contain exactly 1 URL (starting with http:// or https://)."
            )

        if len(urls_found) > 1:
            raise ValueError(
                f"Message contains {len(urls_found)} URLs. Exactly 1 URL is allowed."
            )

        # Rule 4: Validate the URL format
        url = urls_found[0]
        url_regex = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )
        if not url_regex.match(url):
            raise ValueError(f"The URL '{url}' is not valid.")

        return v


class PlatformResult(BaseModel):
    platform: str
    status: str
    posted_url: Optional[str] = None
    public_access: bool = False
    date: Optional[str] = None
    time: Optional[str] = None
    error: Optional[str] = None


class PostingResponse(BaseModel):
    success: bool
    total_platforms: int
    successful: int
    failed: int
    results: list[PlatformResult]