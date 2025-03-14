# modules/table_formatter.py
import numpy as np
from tabulate import tabulate
from config.settings import settings
from modules.event_processor import EventProcessor

class TableFormatter:
    @staticmethod
    def format_table(data, headers):
        """Formats data into a table."""
        return tabulate(data, headers, tablefmt=settings.TABLE_FORMAT)

    @staticmethod
    def format_channel_info(channels_info):
        """Formats channel information."""
        data = []
        for channel in channels_info:
            loc = channel['loc']
            loc_x, loc_y, loc_z = '-', '-', '-'

            if len(loc) >= 3 and all(isinstance(x, (float, int)) for x in loc[:3]) and not np.isnan(loc[:3]).any():
                loc_x, loc_y, loc_z = loc[:3]

            channel_data = [
                channel['ch_name'],
                channel['logno'],
                channel['scanno'],
                channel['cal'],
                channel['range'],
                channel['unit_mul'],
                channel['unit'],
                channel['coord_frame'],
                channel['coil_type'],
                channel['kind'],
                loc_x,
                loc_y,
                loc_z
            ]
            data.append(channel_data)

        headers = [
            "Channel Name", "Logical Number", "Scan Number", "Calibration", "Range",
            "Unit Multiplier", "Unit", "Coordinate Frame", "Coil Type", "Channel Type",
            "Loc X", "Loc Y", "Loc Z"
        ]

        return TableFormatter.format_table(data, headers)

    @staticmethod
    def format_event_info(events, sfreq, event_id):
        """Formats event information."""
        table_data = []
        for s_idx in range(len(events)):
            time_index = events[s_idx, 0]
            event_id_value = events[s_idx, 2]
            evt_name = EventProcessor.get_event_name(event_id_value, event_id)
            time_seconds = time_index / sfreq
            table_data.append([
                f"{time_seconds:.2f}",
                event_id_value,
                evt_name
            ])

        headers = ["Time (sec)", "Event ID", "Description"]
        return TableFormatter.format_table(table_data, headers)