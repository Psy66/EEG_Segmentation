# modules/event_processor.py

class EventProcessor:
    @staticmethod
    def get_event_name(evt_code, ev_id):
        """Returns the event name based on its code."""
        return next((name for name, code in ev_id.items() if code == evt_code), "Unknown")

    @staticmethod
    def format_event(time_index, sfreq, event_id_value, event_id):
        """Formats event information."""
        evt_name = EventProcessor.get_event_name(event_id_value, event_id)
        return f"Time: {time_index / sfreq:.2f} sec., Event ID: {event_id_value}, Description: {evt_name}\n"

    @staticmethod
    def generate_segment_name(base_name, existing_names):
        """Generates a unique name for a segment."""
        seg_name = base_name
        counter = 1
        while seg_name in existing_names:
            seg_name = f"{base_name}_{counter}"
            counter += 1
        return seg_name