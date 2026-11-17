import httpx
from datetime import datetime
from app.schemas import PlatformResult
from app.platforms.base import BasePlatform


class DPastePlatform(BasePlatform):
    platform_name = "Dpaste"

    def post(self, message: str) -> PlatformResult:
        now = datetime.now()
        try:
            data = {
                "content": message,
                "syntax": "text",
                "expiry_days": 30,
                "title": "OmniPost Public Message"
            }

            response = httpx.post(
                "https://dpaste.org/api/",
                data=data,
                timeout=15.0
            )

            if response.status_code in [200, 201]:
                # Dpaste returns the URL directly in response body as plain text
                paste_url = response.text.strip().replace('"', '')
                return PlatformResult(
                    platform=self.platform_name,
                    status="success",
                    posted_url=paste_url,
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