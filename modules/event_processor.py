# modules/event_processor.py

class EventProcessor:
    @staticmethod
    def get_event_name(evt_code, ev_id):
        """Возвращает имя события по его коду."""
        return next((name for name, code in ev_id.items() if code == evt_code), "Unknown")

    @staticmethod
    def format_event(time_index, sfreq, event_id_value, event_id):
        """Форматирует информацию о событии."""
        evt_name = EventProcessor.get_event_name(event_id_value, event_id)
        return f"Время: {time_index / sfreq:.2f} сек., ID события: {event_id_value}, Описание: {evt_name}\n"

    @staticmethod
    def generate_segment_name(base_name, existing_names):
        """Генерирует уникальное имя для сегмента."""
        seg_name = base_name
        counter = 1
        while seg_name in existing_names:
            seg_name = f"{base_name}_{counter}"
            counter += 1
        return seg_name