# edf_processor.py
import mne
from mne.viz import plot_montage
import montage_manager
import tkinter as tk
from config.settings import settings
from modules.event_processor import EventProcessor
from modules.table_formatter import TableFormatter
from modules.logger import setup_logger

# Logger setup
logger = setup_logger()

class EDFProcessor:
    def __init__(self, output_widget):
        """
        Initializes the EDF file processor.

        :param output_widget: Widget for text output (e.g., ScrolledText).
        """
        self.seg_dict = {}  # Dictionary to store segments
        self.output_widget = output_widget  # Widget for outputting information
        self.raw = None  # EDF file data
        self.events = None  # Events from annotations
        self.event_id = None  # Event identifiers

    def load_metadata(self, file_path):
        """
        Loads metadata from an EDF file.

        :param file_path: Path to the EDF file.
        """
        try:
            # Clear the output field before loading new data
            self.output_widget.delete(1.0, tk.END)

            # Load data from the EDF file
            self.raw = mne.io.read_raw_edf(file_path, preload=True)

            # Remove the ECG channel if it exists
            if 'ECG  ECG' in self.raw.ch_names:
                self.raw.drop_channels(['ECG  ECG'])
                self.output_widget.insert(tk.END, "ECG channel removed.\n")

            # Get events from annotations
            self.events, self.event_id = mne.events_from_annotations(self.raw)

            # Get subject information
            subject_info = self.raw.info.get('subject_info', {})
            output_lines = self.format_subject_info(subject_info)

            # Add information about the number of channels and sampling frequency
            num_channels = len(self.raw.ch_names)
            output_lines.append(f"Number of channels: {num_channels}\n")
            output_lines.append(f"Sampling frequency: {self.raw.info['sfreq']} Hz\n")

            # Apply montage (if available)
            montage = montage_manager.MontageManager.get_montage(num_channels)
            if montage:
                self.raw.set_montage(montage)
                self.output_widget.insert(tk.END, "Montage successfully applied.\n")
                # Visualize the montage in 3D
                fig = plot_montage(
                    montage,
                    kind='topomap',
                    show_names=True,  # Show channel names
                    sphere='auto',  # Automatically adjust sphere parameters
                    scale=1.2  # Increase point size
                )

            else:
                self.output_widget.insert(tk.END, "Montage not applied: unsuitable number of channels.\n")

            # Output channel and event information
            output_lines.append(self.display_channel_names())
            output_lines.append(self.get_event_info())
            self.output_widget.insert(tk.END, ''.join(output_lines))

        except Exception as e:
            # Log the error and display a message
            logger.error(f"Failed to load metadata: {str(e)}", exc_info=True)  # Added exc_info for details
            self.output_widget.insert(tk.END, f"Error: {str(e)}\n")
            raise Exception(f"Failed to load metadata: {str(e)}")

    @staticmethod
    def format_subject_info(subject_info):
        """
        Formats subject information into a readable format.

        :param subject_info: Dictionary containing subject information.
        :return: List of strings with formatted information.
        """
        first_name = subject_info.get('first_name', 'Not specified')
        middle_name = subject_info.get('middle_name', 'Not specified')
        last_name = subject_info.get('last_name', 'Not specified')
        full_name = f"{first_name} {middle_name} {last_name}".strip()
        birthday = subject_info.get('birthday', 'Not specified')
        sex_description = {1: "Male", 0: "Female"}.get(subject_info.get('sex'), "Not specified")
        meas_date = subject_info.get('meas_date', 'Not specified')

        return [
            f"Full Name: {full_name}\n",
            f"Date of Birth: {birthday}\n",
            f"Sex: {sex_description}\n",
            f"Study Date: {meas_date}\n"
        ]

    def display_channel_names(self):
        """
        Formats and returns channel information as a table.

        :return: String containing the table and channel parameter descriptions.
        """
        channels_info = self.raw.info['chs']
        table = TableFormatter.format_channel_info(channels_info)
        description = """
        Parameter Legend:
        1. Channel Name: Name of the channel (e.g., 'EEG F3').
        2. Logical Number: Logical number of the channel.
        3. Scan Number: Scan number of the channel.
        4. Calibration: Calibration coefficient (used for conversion to physical units).
        5. Range: Range of channel values (maximum and minimum).
        6. Unit Multiplier: Unit multiplication factor.
        7. Units: Measurement units (e.g., 'uV' for microvolts).
        8. Coordinate System: Coordinate system to which the coordinates belong.
        9. Coil Type: Coil type (not always relevant for EEG).
        10. Channel Type: Type of channel (e.g., 'EEG', 'EOG', 'ECG').
        11. Loc X, Loc Y, Loc Z: Channel coordinates in 3D space.
        """
        return f"\nChannel Information:\n{table}\n{description}\n"

    def get_event_info(self):
        """
        Returns event information as a table.

        :return: String containing the event table.
        """
        if self.events is None:
            return "No events available in annotations.\n"
        return f"\nNumber of events: {len(self.events)}\nEvent List:\n{TableFormatter.format_event_info(self.events, self.raw.info['sfreq'], self.event_id)}\n"

    def add_seg(self, s_idx, e_idx, raw, evts, ev_id):
        """
        Adds a segment to the segment dictionary.

        :param s_idx: Index of the start event.
        :param e_idx: Index of the end event.
        :param raw: EDF file data.
        :param evts: List of events.
        :param ev_id: Event identifiers.
        """
        s_t = self.events[s_idx, 0] / raw.info['sfreq']
        e_t = self.events[e_idx, 0] / raw.info['sfreq'] if e_idx is not None else raw.times[-1]

        # Skip segments shorter than the minimum duration
        if e_t - s_t < settings.MIN_SEGMENT_DURATION:
            return

        # Get the name of the current and next event
        evt_code = self.events[s_idx, 2]
        evt_name = EventProcessor.get_event_name(evt_code, ev_id)
        next_evt = "End" if e_idx is None else EventProcessor.get_event_name(self.events[e_idx, 2], ev_id)

        # Generate a unique segment name
        seg_name = EventProcessor.generate_segment_name(evt_name, self.seg_dict.keys())

        # Create the segment
        seg_data = raw.copy().crop(tmin=s_t, tmax=e_t)
        self.seg_dict[seg_name] = dict(
            start_time=s_t,
            end_time=e_t,
            current_event=evt_name,
            next_event=next_evt,
            data=seg_data
        )

    def process(self):
        """
        Processes the EDF file data and splits it into segments.
        """
        # Clear the output field before starting processing
        self.output_widget.delete(1.0, tk.END)

        if self.raw is not None:
            self.output_widget.insert(tk.END, "Starting processing...\n")

            # Check for sufficient number of events
            if len(self.events) < 2:
                self.output_widget.insert(tk.END, "Insufficient events to extract segments.\n")
                return

            # Split into segments
            for i in range(len(self.events) - 1):
                self.add_seg(i, i + 1, self.raw, self.events, self.event_id)

            # Add the last segment
            self.add_seg(len(self.events) - 1, None, self.raw, self.events, self.event_id)

            # Output the results
            self.output_results()

        else:
            logger.error("Please select an EDF file for processing first.")
            raise Exception("Please select an EDF file for processing first.")

    def output_results(self):
        """
        Outputs the processing results (dictionary structure and segment data).
        """
        # Output the dictionary structure
        structure_data = [
            ["Key", "Key", "Type", "Example Value"],
            ["*seg_name*", "", "", ""],
            ["", "", "", ""],
            ["", "start_time", "float", "0.60"],
            ["", "end_time", "float", "15.00"],
            ["", "current_event", "str", "Fon"],
            ["", "next_event", "str", "OG"],
            ["", "data", "RawEDF", "RawEDF Object"]
        ]
        structure_table = TableFormatter.format_table(structure_data, headers="firstrow")
        self.output_widget.insert(tk.END, "Segment Dictionary Structure:\n")
        self.output_widget.insert(tk.END, structure_table + "\n\n")

        # Prepare data for the segment table
        table_data = []
        valid_segments_count = 0
        for seg_name, t in self.seg_dict.items():
            duration = t['end_time'] - t['start_time']
            if duration >= settings.MIN_SEGMENT_DURATION:
                table_data.append([
                    seg_name,
                    f"{t['start_time']:.3f}",
                    f"{t['end_time']:.3f}",
                    t['current_event'],
                    t['next_event'],
                    f"{duration:.3f}"
                ])
                valid_segments_count += 1

        # Output segment data
        headers = ["Segment", "Start", "End", "From", "To", "Duration"]
        table = TableFormatter.format_table(table_data, headers)
        self.output_widget.insert(tk.END, f"Number of segments with duration >= {settings.MIN_SEGMENT_DURATION} sec: {valid_segments_count}\n")
        self.output_widget.insert(tk.END, "Segment Data:\n")
        self.output_widget.insert(tk.END, table + "\n")