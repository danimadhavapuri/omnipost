import httpx
from datetime import datetime
from app.schemas import PlatformResult
from app.platforms.base import BasePlatform
from app import config


class DiscordPlatform(BasePlatform):
    platform_name = "Discord"

    def post(self, message: str) -> PlatformResult:
        now = datetime.now()
        try:
            if not config.DISCORD_WEBHOOK_URL:
                return PlatformResult(
                    platform=self.platform_name,
                    status="failed",
                    public_access=False,
                    error="Discord webhook URL is not configured"
                )

            # Add ?wait=true so Discord returns message details
            webhook_url = config.DISCORD_WEBHOOK_URL
            if "?wait=true" not in webhook_url:
                webhook_url += "?wait=true"

            payload = {
                "content": f"📢 **OmniPost Broadcast**\n{message}",
                "username": "OmniPost Bot"
            }

            response = httpx.post(webhook_url, json=payload, timeout=15.0)

            if response.status_code in [200, 204]:
                channel_id = config.DISCORD_WEBHOOK_URL.split("/webhooks/")[1].split("/")[0]
                posted_url = f"https://discord.com/channels/{channel_id}"
                if response.status_code == 200:
                    res_data = response.json()
                    message_id = res_data.get("id")
                    channel_ref = res_data.get("channel_id", channel_id)
                    posted_url = f"https://discord.com/channels/@me/{channel_ref}/{message_id}"

                return PlatformResult(
                    platform=self.platform_name,
                    status="success",
                    posted_url=posted_url,
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