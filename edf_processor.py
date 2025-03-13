# edf_processor.py
import mne
from mne.viz import plot_montage
import matplotlib.pyplot as plt
from numpy.ma.core import angle

import montage_manager
import tkinter as tk
from config.settings import settings
from modules.event_processor import EventProcessor
from modules.table_formatter import TableFormatter
from modules.logger import setup_logger

# Настройка логгера
logger = setup_logger()

class EDFProcessor:
    def __init__(self, output_widget):
        """
        Инициализация обработчика EDF-файлов.

        :param output_widget: Виджет для вывода текста (например, ScrolledText).
        """
        self.seg_dict = {}  # Словарь для хранения сегментов
        self.output_widget = output_widget  # Виджет для вывода информации
        self.raw = None  # Данные EDF-файла
        self.events = None  # События из аннотаций
        self.event_id = None  # Идентификаторы событий

    def load_metadata(self, file_path):
        """
        Загружает метаданные из EDF-файла.

        :param file_path: Путь к EDF-файлу.
        """
        try:
            # Очистка поля вывода перед загрузкой новых данных
            self.output_widget.delete(1.0, tk.END)

            # Загрузка данных из EDF-файла
            self.raw = mne.io.read_raw_edf(file_path, preload=True)

            # Удаление канала ECG, если он есть
            if 'ECG  ECG' in self.raw.ch_names:
                self.raw.drop_channels(['ECG  ECG'])
                self.output_widget.insert(tk.END, "Канал ECG удален.\n")

            # Получение событий из аннотаций
            self.events, self.event_id = mne.events_from_annotations(self.raw)

            # Получение информации о субъекте
            subject_info = self.raw.info.get('subject_info', {})
            output_lines = self.format_subject_info(subject_info)

            # Добавление информации о количестве каналов и частоте дискретизации
            num_channels = len(self.raw.ch_names)
            output_lines.append(f"Количество каналов: {num_channels}\n")
            output_lines.append(f"Частота дискретизации: {self.raw.info['sfreq']} Гц\n")

            # Применение монтажа (если доступен)
            montage = montage_manager.MontageManager.get_montage(num_channels)
            if montage:
                self.raw.set_montage(montage)
                self.output_widget.insert(tk.END, "Монтаж успешно применен.\n")
                # Визуализация монтажа в 3D
                fig = plot_montage(
                    montage,
                    kind='topomap',
                    show_names=True,  # Показать названия каналов
                    sphere='auto',  # Автоматически подобрать параметры сферы
                    scale=1.2  # Увеличить размер точек

                )

            else:
                self.output_widget.insert(tk.END, "Монтаж не применен: неподходящее количество каналов.\n")

            # Вывод информации о каналах и событиях
            output_lines.append(self.display_channel_names())
            output_lines.append(self.get_event_info())
            self.output_widget.insert(tk.END, ''.join(output_lines))

        except Exception as e:
            # Логирование ошибки и вывод сообщения
            logger.error(f"Не удалось загрузить метаданные: {str(e)}", exc_info=True)  # Добавлено exc_info для деталей
            self.output_widget.insert(tk.END, f"Ошибка: {str(e)}\n")
            raise Exception(f"Не удалось загрузить метаданные: {str(e)}")

    @staticmethod
    def format_subject_info(subject_info):
        """
        Форматирует информацию о субъекте в читаемый вид.

        :param subject_info: Словарь с информацией о субъекте.
        :return: Список строк с отформатированной информацией.
        """
        first_name = subject_info.get('first_name', 'Не указано')
        middle_name = subject_info.get('middle_name', 'Не указано')
        last_name = subject_info.get('last_name', 'Не указано')
        fio = f"{first_name} {middle_name} {last_name}".strip()
        birthday = subject_info.get('birthday', 'Не указано')
        sex_description = {1: "Мужчина", 0: "Женщина"}.get(subject_info.get('sex'), "Не указано")
        meas_date = subject_info.get('meas_date', 'Не указано')

        return [
            f"ФИО: {fio}\n",
            f"Дата рождения: {birthday}\n",
            f"Пол: {sex_description}\n",
            f"Дата исследования: {meas_date}\n"
        ]

    def display_channel_names(self):
        """
        Форматирует и возвращает информацию о каналах в виде таблицы.

        :return: Строка с таблицей и описанием параметров каналов.
        """
        channels_info = self.raw.info['chs']
        table = TableFormatter.format_channel_info(channels_info)
        description = """
        Легенда параметров:
        1. Имя канала: Имя канала (например, 'EEG F3').
        2. Лог. номер: Логический номер канала.
        3. Номер скана: Номер сканирования канала.
        4. Калибровка: Коэффициент калибровки (используется для преобразования в физическую величину).
        5. Диапазон: Диапазон значений канала (максимум и минимум).
        6. Множ. единиц: Фактор умножения единиц измерения.
        7. Единицы: Единицы измерения (например, 'uV' для микровольт).
        8. Система координат: Система координат, к которой относятся координаты.
        9. Тип катушки: Тип катушки (не всегда актуально для EEG).
        10. Тип канала: Вид канала (например, 'EEG', 'EOG', 'ECG').
        11. Loc X, Loc Y, Loc Z: Координаты канала в 3D-пространстве.
        """
        return f"\nИнформация о каналах:\n{table}\n{description}\n"

    def get_event_info(self):
        """
        Возвращает информацию о событиях в виде таблицы.

        :return: Строка с таблицей событий.
        """
        if self.events is None:
            return "Нет доступных событий в аннотациях.\n"
        return f"\nКоличество событий: {len(self.events)}\nСписок событий:\n{TableFormatter.format_event_info(self.events, self.raw.info['sfreq'], self.event_id)}\n"
    def add_seg(self, s_idx, e_idx, raw, evts, ev_id):
        """
        Добавляет сегмент в словарь сегментов.

        :param s_idx: Индекс начального события.
        :param e_idx: Индекс конечного события.
        :param raw: Данные EDF-файла.
        :param evts: Список событий.
        :param ev_id: Идентификаторы событий.
        """
        s_t = self.events[s_idx, 0] / raw.info['sfreq']
        e_t = self.events[e_idx, 0] / raw.info['sfreq'] if e_idx is not None else raw.times[-1]

        # Пропуск сегментов короче минимальной длительности
        if e_t - s_t < settings.MIN_SEGMENT_DURATION:
            return

        # Получение имени текущего и следующего события
        evt_code = self.events[s_idx, 2]
        evt_name = EventProcessor.get_event_name(evt_code, ev_id)
        next_evt = "End" if e_idx is None else EventProcessor.get_event_name(self.events[e_idx, 2], ev_id)

        # Генерация уникального имени сегмента
        seg_name = EventProcessor.generate_segment_name(evt_name, self.seg_dict.keys())

        # Создание сегмента
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
        Обрабатывает данные EDF-файла и разбивает их на сегменты.
        """
        # Очистка поля вывода перед началом обработки
        self.output_widget.delete(1.0, tk.END)

        if self.raw is not None:
            self.output_widget.insert(tk.END, "Начинается процесс обработки...\n")

            # Проверка на достаточное количество событий
            if len(self.events) < 2:
                self.output_widget.insert(tk.END, "Недостаточно событий для извлечения сегментов.\n")
                return

            # Разбиение на сегменты
            for i in range(len(self.events) - 1):
                self.add_seg(i, i + 1, self.raw, self.events, self.event_id)

            # Добавление последнего сегмента
            self.add_seg(len(self.events) - 1, None, self.raw, self.events, self.event_id)

            # Вывод результатов
            self.output_results()

        else:
            logger.error("Сначала выберите файл EDF для обработки.")
            raise Exception("Сначала выберите файл EDF для обработки.")

    def output_results(self):
        """
        Выводит результаты обработки (структуру словаря и данные сегментов).
        """
        # Вывод структуры словаря
        structure_data = [
            ["Ключ", "Ключ", "Тип", "Пример значения"],
            ["*seg_name*", "", "", ""],
            ["", "", "", ""],
            ["", "start_time", "float", "0.60"],
            ["", "end_time", "float", "15.00"],
            ["", "current_event", "str", "Fon"],
            ["", "next_event", "str", "OG"],
            ["", "data", "RawEDF", "Объект RawEDF"]
        ]
        structure_table = TableFormatter.format_table(structure_data, headers="firstrow")
        self.output_widget.insert(tk.END, "Структура словаря сегментов:\n")
        self.output_widget.insert(tk.END, structure_table + "\n\n")

        # Подготовка данных для таблицы сегментов
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

        # Вывод данных сегментов
        headers = ["Сегмент", "Начало", "Конец", "От", "До", "Длительность"]
        table = TableFormatter.format_table(table_data, headers)
        self.output_widget.insert(tk.END, f"Количество сегментов с длительностью >= {settings.MIN_SEGMENT_DURATION} сек: {valid_segments_count}\n")
        self.output_widget.insert(tk.END, "Данные сегментов:\n")
        self.output_widget.insert(tk.END, table + "\n")