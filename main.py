import asyncio
from core.printer.poller import poll_printer
from bot.bot import start_bot

async def main():
    task_polling = asyncio.create_task(poll_printer(interval_sec=5))
    task_bot = asyncio.create_task(start_bot())
    await asyncio.gather(task_polling, task_bot)  

if __name__ == '__main__':
    asyncio.run(main())