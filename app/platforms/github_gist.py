import httpx
from datetime import datetime
from app.schemas import PlatformResult
from app.platforms.base import BasePlatform
from app import config


class GitHubGistPlatform(BasePlatform):
    platform_name = "GitHub Gist"

    def post(self, message: str) -> PlatformResult:
        now = datetime.now()
        try:
            if not config.GITHUB_TOKEN:
                return PlatformResult(
                    platform=self.platform_name,
                    status="failed",
                    public_access=False,
                    error="GitHub token is not configured"
                )

            headers = {
                "Authorization": f"Bearer {config.GITHUB_TOKEN}",
                "Accept": "application/vnd.github+json",
                "User-Agent": "omnipost-app"
            }

            payload = {
                "description": "OmniPost - Automated Multi-Platform Broadcast",
                "public": True,
                "files": {
                    "omnipost.txt": {
                        "content": message
                    }
                }
            }

            response = httpx.post(
                "https://api.github.com/gists",
                headers=headers,
                json=payload,
                timeout=15.0
            )

            if response.status_code in [200, 201]:
                res_data = response.json()
                return PlatformResult(
                    platform=self.platform_name,
                    status="success",
                    posted_url=res_data.get("html_url"),
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