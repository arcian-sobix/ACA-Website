import asyncio
import logging
from bot.core.bot import bot
from bot.core.config import settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    """Start the bot with proper error handling"""
    try:
        await bot.start(settings.DISCORD_TOKEN)
    except KeyboardInterrupt:
        await bot.close()
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())