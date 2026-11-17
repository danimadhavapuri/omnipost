import httpx
from datetime import datetime
from app.schemas import PlatformResult
from app.platforms.base import BasePlatform
from app import config


class MastodonPlatform(BasePlatform):
    platform_name = "Mastodon"

    def post(self, message: str) -> PlatformResult:
        now = datetime.now()
        try:
            if not config.MASTODON_ACCESS_TOKEN or config.MASTODON_ACCESS_TOKEN == "placeholder":
                return PlatformResult(
                    platform=self.platform_name,
                    status="failed",
                    public_access=False,
                    error="Mastodon access token is not configured"
                )

            headers = {
                "Authorization": f"Bearer {config.MASTODON_ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }
            data = {"status": message}

            response = httpx.post(
                f"{config.MASTODON_BASE_URL}/api/v1/statuses",
                headers=headers,
                json=data,
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