import json
from typing import NamedTuple
from core.printer.parser import PrinterStatus, Event, TemperatureReadings
from datetime import datetime

class EventDescription(NamedTuple):
    hex_code: str
    time: datetime
    code: str = 'Unknown'
    description: str = 'Unknown'

def status_to_dict(status: PrinterStatus) -> dict:
    data = status._asdict()
    data['temperature'] = status.temperature._asdict()
    data['logs'] = [i._asdict() for i in status.logs]
    return data

def status_from_dict(data: dict) -> PrinterStatus:
    logs = [Event(log['code'], log['timestamp']) for log in data['logs']]
    temperature = TemperatureReadings(*[float(data['temperature'][i]) for i in data['temperature']])
    return PrinterStatus(
        data['filename'],
        data['progress'],
        data['remaining_time_sec'],
        temperature,
        logs
    )

def save_status(status: PrinterStatus):
    data = status_to_dict(status)
    with open('data/last_status.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_previous_status() -> PrinterStatus:
    with open('data/last_status.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return status_from_dict(data)

def load_events_description() -> dict[dict]:
    with open('data/events_description.json', 'r', encoding='utf-8') as file:
        events = json.load(file)
    return events

def update_events_description(event: EventDescription):
    events = load_events_description()
    events[f'{event.hex_code}'] = {
        'code': event.code,
        'description': event.description
    }
    with open('data/events_description.json', 'w', encoding='utf-8') as file:
        json.dump(events, file, ensure_ascii=False, indent=4)
     