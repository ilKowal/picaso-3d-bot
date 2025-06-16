from typing import NamedTuple
from datetime import datetime
import struct
import json

class TemperatureReadings(NamedTuple):
    nozzle_1: float
    nozzle_2: float
    chamber: float
    bed: float
    radiator: float

class Event(NamedTuple):
    code: str
    timestamp: int

    @property
    def time(self) -> datetime:
        return datetime.fromtimestamp(self.timestamp)

class PrinterStatus(NamedTuple):
    filename: str
    progress: float
    remaining_time_sec: int
    temperature: TemperatureReadings
    logs: list[Event]

def parse_printer_data(data: bytes) -> PrinterStatus:
    filename_section = data[20:275]
    progress_section = data[279:283]
    rem_time_section = data[291:295]
    temp_section = data[299:319]
    log_section = data[319:379]

    filename = filename_section.split(b'\x00', 1)[0].decode('utf-8')
    progress = round(struct.unpack('<f', progress_section)[0], 2)
    remaining_time_sec = int.from_bytes(rem_time_section, byteorder='little')
    temperature = parse_temperature(temp_section)
    logs = parse_events(log_section)
    return PrinterStatus(
        filename=filename,
        progress=progress,
        remaining_time_sec=remaining_time_sec,
        temperature=temperature,
        logs=logs
    )

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def parse_temperature(data: bytes) -> TemperatureReadings:
    return TemperatureReadings(
        nozzle_1=struct.unpack('<f', data[0:4])[0],
        nozzle_2=struct.unpack('<f', data[4:8])[0],
        chamber=struct.unpack('<f', data[8:12])[0],
        bed=struct.unpack('<f', data[12:16])[0],
        radiator=struct.unpack('<f', data[16:20])[0],
    )

def parse_events(data: bytes) -> list[Event]:
    events = []
    for i in range(0, len(data), 6):
        event_code = data[i:i+2].hex()
        timestamp = data[i+2:i+6]
        if len(timestamp) < 4:
            continue
        timestamp = int.from_bytes(timestamp, 'little')
        events.append(Event(code=event_code, timestamp=timestamp))
    return events