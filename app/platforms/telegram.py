import httpx
from datetime import datetime
from app.schemas import PlatformResult
from app.platforms.base import BasePlatform
from app import config


class TelegramPlatform(BasePlatform):
    platform_name = "Telegram"

    def post(self, message: str) -> PlatformResult:
        now = datetime.now()
        try:
            if not config.TELEGRAM_BOT_TOKEN or config.TELEGRAM_BOT_TOKEN == "placeholder":
                return PlatformResult(
                    platform=self.platform_name,
                    status="failed",
                    public_access=False,
                    error="Telegram bot token is not configured"
                )

            url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {
                "chat_id": config.TELEGRAM_CHAT_ID,
                "text": message,
                "disable_web_page_preview": False
            }

            response = httpx.post(url, json=data, timeout=15.0)

            if response.status_code == 200:
                result = response.json()
                message_id = result.get("result", {}).get("message_id")
                channel = (config.TELEGRAM_CHAT_ID or "").replace("@", "")
                posted_url = f"https://t.me/{channel}/{message_id}"

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