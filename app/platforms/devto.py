import httpx
from datetime import datetime
from app.schemas import PlatformResult
from app.platforms.base import BasePlatform
from app import config


class DevtoPlatform(BasePlatform):
    platform_name = "Dev.to"

    def post(self, message: str) -> PlatformResult:
        now = datetime.now()
        try:
            if not config.DEVTO_API_KEY or config.DEVTO_API_KEY == "placeholder":
                return PlatformResult(
                    platform=self.platform_name,
                    status="failed",
                    public_access=False,
                    error="Dev.to API key is not configured"
                )

            headers = {
                "api-key": config.DEVTO_API_KEY,
                "Content-Type": "application/json"
            }

            # Dev.to creates an article/post with the message
            payload = {
                "article": {
                    "title": f"Update from OmniPost - {now.strftime('%b %d, %Y')}",
                    "published": True,
                    "body_markdown": message,
                    "tags": ["tech", "productivity"]
                }
            }

            response = httpx.post(
                "https://dev.to/api/articles",
                headers=headers,
                json=payload,
                timeout=15.0
            )

            if response.status_code in [200, 201]:
                res_data = response.json()
                return PlatformResult(
                    platform=self.platform_name,
                    status="success",
                    posted_url=res_data.get("url"),
                    public_access=True,
                    date=now.strftime("%Y-%m-%d"),
                    time=now.strftime("%H:%M:%S"),
                    error=None
                )
            else:
                return PlatformResult(
                    platform=self.platform_name,
                    status="failed",
                    public_access=False,
                    error=f"HTTP {response.status_code}: {response.text}"
                )

        except Exception as e:
            return PlatformResult(
                platform=self.platform_name,
                status="failed",
                public_access=False,
                error=str(e)
            )