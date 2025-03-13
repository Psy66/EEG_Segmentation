# gui.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from edf_processor import EDFProcessor
from config.settings import settings

def create_gui():
    """
    Создает графический интерфейс для обработки EDF-файлов.

    :return: Корневое окно приложения.
    """
    # Создание главного окна
    root = tk.Tk()
    root.title("EDF Segment Processor")
    root.geometry("1700x700")

    # Настройка стилей для кнопок и фреймов
    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", background="#ccc")
    style.configure("TFrame", background="#f0f0f0")

    # Главный фрейм для размещения элементов интерфейса
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Фрейм для настроек (минимальная длительность сегмента)
    settings_frame = ttk.Frame(main_frame)
    settings_frame.pack(fill=tk.X, pady=(0, 10))

    # Поле для ввода минимальной длительности сегмента
    ttk.Label(settings_frame, text="Мин. длительность сегмента (сек):").pack(side=tk.LEFT, padx=5)
    min_duration_entry = ttk.Entry(settings_frame, width=10)
    min_duration_entry.insert(0, str(settings.MIN_SEGMENT_DURATION))  # Установка значения по умолчанию
    min_duration_entry.pack(side=tk.LEFT, padx=5)

    def apply_min_duration():
        """
        Применяет минимальную длительность сегмента, введенную пользователем.
        """
        try:
            min_duration = float(min_duration_entry.get())
            if min_duration <= 0:
                raise ValueError("Длительность должна быть больше 0.")
            settings.MIN_SEGMENT_DURATION = min_duration  # Обновление значения в настройках
            messagebox.showinfo("Успех", f"Минимальная длительность установлена: {min_duration} сек.")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    # Кнопка для применения минимальной длительности
    ttk.Button(settings_frame, text="Применить", command=apply_min_duration).pack(side=tk.LEFT, padx=5)

    # Поле вывода текста (ScrolledText)
    output_area = scrolledtext.ScrolledText(main_frame, width=100, height=25, wrap=tk.WORD)
    output_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

    def copy_text(event=None):
        """
        Копирует выделенный текст из поля вывода в буфер обмена.

        :param event: Событие (необязательно).
        """
        try:
            selected_text = output_area.get(tk.SEL_FIRST, tk.SEL_LAST)
            root.clipboard_clear()
            root.clipboard_append(selected_text)
        except tk.TclError:
            pass  # Если текст не выделен, ничего не делаем

    # Привязка комбинации клавиш Ctrl+C к функции копирования
    output_area.bind("<Control-c>", copy_text)
    output_area.bind("<Control-C>", copy_text)

    # Фрейм для кнопок
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X)

    # Создание экземпляра EDFProcessor для обработки данных
    processor = EDFProcessor(output_area)

    def select_file():
        """
        Открывает диалоговое окно для выбора EDF-файла и загружает его метаданные.
        """
        file_path = filedialog.askopenfilename(
            title="Выберите файл EDF",
            filetypes=[("EDF files", "*.edf"), ("All files", "*.*")]
        )
        if file_path:
            try:
                processor.load_metadata(file_path)  # Загрузка метаданных
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))  # Вывод ошибки, если что-то пошло не так

    # Кнопка "Открыть файл EDF"
    btn_open = ttk.Button(button_frame, text="Открыть файл EDF", command=select_file)
    btn_open.pack(side=tk.LEFT, padx=5, pady=5)

    # Кнопка "Разбить на сегменты"
    btn_process = ttk.Button(button_frame, text="Разбить на сегменты", command=processor.process)
    btn_process.pack(side=tk.LEFT, padx=5, pady=5)

    # Кнопка "Выход"
    btn_exit = ttk.Button(button_frame, text="Выход", command=root.destroy)
    btn_exit.pack(side=tk.RIGHT, padx=5, pady=5)

    return root

if __name__ == "__main__":
    # Запуск приложения
    app = create_gui()
    app.mainloop()