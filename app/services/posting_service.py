from app.schemas import PlatformResult
from app.platforms.mastodon import MastodonPlatform
from app.platforms.telegram import TelegramPlatform
from app.platforms.github_gist import GitHubGistPlatform
from app.platforms.discord import DiscordPlatform
from app.platforms.dpaste import DPastePlatform


def post_to_all_platforms(message: str) -> list[PlatformResult]:
    """
    Automated multi-platform posting to 5 distinct platforms.
    Each platform is isolated: failure in one does not block others.
    """
    platforms = [
        MastodonPlatform(),
        TelegramPlatform(),
        GitHubGistPlatform(),
        DiscordPlatform(),
        DPastePlatform()
    ]

    results = []

    for platform in platforms:
        try:
            res = platform.post(message)
            results.append(res)
        except Exception as err:
            results.append(
                PlatformResult(
                    platform=platform.platform_name,
                    status="failed",
                    public_access=False,
                    error=str(err)
                )
            )

    return results