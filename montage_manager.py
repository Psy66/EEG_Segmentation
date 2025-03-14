# montage_manager.py
import mne
import numpy as np

class MontageManager:
    """
    A class for managing montages (electrode layouts) for EEG data.
    Supports creating montages for 10 and 20 channels.
    """

    @staticmethod
    def create_montage_10_channels():
        """
        Creates a montage for 10-channel EEG.
        Returns a DigMontage object with channel coordinates and names.
        """
        ch_n = ['EEG F3', 'EEG F4', 'EEG C3', 'EEG C4', 'EEG P3', 'EEG P4', 'EEG O1', 'EEG O2', 'EEG A2', 'EEG A1']
        ch_c = np.array([
            [-0.05, 0.0375, 0.06], [0.05, 0.0375, 0.06],  # F3, F4
            [-0.05, 0.0, 0.1], [0.05, 0.0, 0.1],  # C3, C4
            [-0.05, -0.0375, 0.08], [0.05, -0.0375, 0.08],  # P3, P4
            [-0.05, -0.075, 0.05], [0.05, -0.075, 0.05],  # O1, O2
            [0.1, 0.0, -0.002], [-0.1, 0.0, -0.002]  # A2, A1
        ])

        dig_pts = [
            dict(ident=i + 1, ch_name=name, r=coord,
                 kind=mne.io.constants.FIFF.FIFFV_POINT_EEG,
                 coord_frame=mne.io.constants.FIFF.FIFFV_COORD_HEAD)
            for i, (name, coord) in enumerate(zip(ch_n, ch_c))
        ]

        return mne.channels.DigMontage(dig=dig_pts, ch_names=ch_n)

    @staticmethod
    def create_montage_20_channels():
        """
        Creates a montage for 20-channel EEG (without ECG).
        Returns a DigMontage object with channel coordinates and names.
        """
        ch_n = [
            'EEG FP1-A1', 'EEG FP2-A2', 'EEG F3-A1', 'EEG F4-A2',
            'EEG C3-A1', 'EEG C4-A2', 'EEG P3-A1', 'EEG P4-A2',
            'EEG O1-A1', 'EEG O2-A2', 'EEG F7-A1', 'EEG F8-A2',
            'EEG T3-A1', 'EEG T4-A2', 'EEG T5-A1', 'EEG T6-A2',
            'EEG FZ-A2', 'EEG CZ-A1', 'EEG PZ-A2'
        ]

        ch_c = np.array([
            [-0.05, 0.075, 0.05], [0.05, 0.075, 0.05],  # Fp1, Fp2
            [-0.05, 0.0375, 0.06], [0.05, 0.0375, 0.06],  # F3, F4
            [-0.05, 0.0, 0.1], [0.05, 0.0, 0.1],  # C3, C4
            [-0.05, -0.0375, 0.08], [0.05, -0.0375, 0.08],  # P3, P4
            [-0.05, -0.075, 0.05], [0.05, -0.075, 0.05],  # O1, O2
            [-0.075, 0.0375, 0.06], [0.075, 0.0375, 0.06],  # F7, F8
            [-0.075, 0.0, 0.1], [0.075, 0.0, 0.1],  # T3, T4
            [-0.075, -0.0375, 0.08], [0.075, -0.0375, 0.08],  # T5, T6
            [0.0, 0.0375, 0.06],  # Fz
            [0.0, 0.0, 0.1],  # Cz
            [0.0, -0.0375, 0.08]  # Pz
        ])

        dig_pts = [
            dict(ident=i + 1, ch_name=name, r=coord,
                 kind=mne.io.constants.FIFF.FIFFV_POINT_EEG,
                 coord_frame=mne.io.constants.FIFF.FIFFV_COORD_HEAD)
            for i, (name, coord) in enumerate(zip(ch_n, ch_c))
        ]

        return mne.channels.DigMontage(dig=dig_pts, ch_names=ch_n)

    @staticmethod
    def get_montage(num_channels):
        """
        Returns a montage based on the number of channels.

        Parameters:
        ----------
        num_channels : int
            Number of channels (10 or 20).

        Returns:
        -----------
        DigMontage or None
            Montage for the specified number of channels or None if the number is not supported.
        """
        if num_channels in [10, 11]:
            return MontageManager.create_montage_10_channels()
        elif num_channels in [19, 20]:
            return MontageManager.create_montage_20_channels()
        else:
            return None