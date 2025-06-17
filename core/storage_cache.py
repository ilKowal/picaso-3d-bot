from core.storage import load_events_description, update_events_description, EventDescription

class EventDescriptionCache:
    def __init__(self):
        self._events = load_events_description()

    def get(self, code: str) -> EventDescription | None:
        event = self._events.get(code)
        if event:
            return EventDescription(
                hex_code=code,
                time=None,
                code=event['code'],
                description=event['description']
            )
        return None

    def add_unknown_code(self, code: str):
        new_desc = EventDescription(hex_code=code)
        update_events_description(new_desc)
        self._events = load_events_description()

description_cache = EventDescriptionCache()
