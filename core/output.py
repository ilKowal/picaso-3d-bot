import json
from core.storage import Event, EventDescription
from core.storage_cache import description_cache
from typing import NamedTuple
from core.printer.parser import PrinterStatus

class SplitTime(NamedTuple):
    hours: int
    minutes: int
    seconds: int

def split_time(time: int) -> SplitTime:
    seconds = time % 60
    minutes = (time // 60) % 60
    hours = time // 3600
    return SplitTime(hours, minutes, seconds)

def take_description(event: Event) -> EventDescription:
    cached = description_cache.get(event.code)
    if cached:
        return EventDescription(
            hex_code=cached.hex_code,
            time=event.time.strftime('%H:%M:%S %d.%m.%Y'),
            code=cached.code,
            description=cached.description
        )
    else:
        description_cache.add_unknown_code(event.code)
        return EventDescription(
            hex_code=event.code,
            time=event.time.strftime('%H:%M:%S %d.%m.%Y'),
            code='Unknown',
            description='Unknown'
        )
        
def take_log(status: PrinterStatus) -> str:
    message = 'Журнал:\n'
    log = status.logs
    for event in log:
        event_descripion = take_description(event)
        if log.index(event) < (log.__len__() - 1):
            message = message + f'{event_descripion.code} - "{event_descripion.description}" в {event_descripion.time}\n'
        else:
            message = message + f'{event_descripion.code} - "{event_descripion.description}" в {event_descripion.time}'
    return message

def take_temperature(status: PrinterStatus) -> str:
    temperature = status.temperature
    message = f'''Датчики температуры:
Сопло 1 - {round(temperature.nozzle_1, 1)}°C
Сопло 2 - {round(temperature.nozzle_2,1)}°C
Платформа - {round(temperature.bed, 1)}°C
Камера - {round(temperature.chamber, 1)}°C
Радиатор - {round(temperature.radiator, 1)}°C'''

    return message

def take_time(status: PrinterStatus) -> str:
    remaining_time = split_time(status.remaining_time_sec)
    message = f'Осталось {remaining_time.hours} ч {remaining_time.minutes} мин {remaining_time.seconds} с'
    return message

def take_progress(status: PrinterStatus) -> str:
    message = f'Готово {status.progress}%' 
    return message

def take_status(status: PrinterStatus) -> str:
    temperature = status.temperature
    remaining_time = split_time(status.remaining_time_sec)
    message = f'''Печать {status.filename}:
Готово {status.progress}%
Осталось {remaining_time.hours} ч {remaining_time.minutes} мин {remaining_time.seconds} с
Датчики температуры:
Сопло 1 - {round(temperature.nozzle_1, 1)}°C
Сопло 2 - {round(temperature.nozzle_2, 1)}°C
Платформа - {round(temperature.bed, 1)}°C
Камера - {round(temperature.chamber, 1)}°C
Радиатор - {round(temperature.radiator, 1)}°C'''
    return message