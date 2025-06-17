import asyncio
from core.printer.parser import parse_printer_data, PrinterStatus, Event
from core.printer.network import send_request 
from core.config import read_config
from core.storage import save_status, load_previous_status, EventDescription
from core.output import take_description
from core.status import get_status
from datetime import datetime
from bot.services.notifier import send_message

config =  read_config()
PRINTER_IP = config.ip
PRINTER_PORT = config.port
REQUEST_BYTES = bytes.fromhex('0100010000000800')

previous_status = load_previous_status()

async def poll_printer(interval_sec: int = 5):
    global previous_status

    while True:
        status = get_status(PRINTER_IP, PRINTER_PORT, REQUEST_BYTES)

        if status == None:
            await asyncio.sleep(interval_sec)
            continue

        # raw_data = send_request(PRINTER_IP, PRINTER_PORT, REQUEST_BYTES)
        # if not raw_data:
        #     print('Ошибка получения данных от принтера')
        #     await asyncio.sleep(interval_sec)
        #     continue

        # try:
        #     status: PrinterStatus = parse_printer_data(raw_data)
        #     save_status(status)
        # except Exception as e:
        #     print(f'Ошибка парсинга: {e}')
        #     await asyncio.sleep(interval_sec)
        #     continue

        if previous_status:
            new_events = extract_new_events(status.logs, previous_status.logs)
        else:
            await asyncio.sleep(interval_sec)
            continue
        if new_events:
            if new_events.__len__() > 1:
                text = ''
            for event in new_events:
                await send_message(f'Новое событие: {event.code} - {event.description} в {event.time}')        

        previous_status = status
        await asyncio.sleep(interval_sec)

def extract_new_events(current: list[Event], previous: list[Event]) -> list[EventDescription]:
    prev_set = {(e.code, e.timestamp) for e in previous}
    return [take_description(e) for e in current if (e.code, e.timestamp) not in prev_set]
