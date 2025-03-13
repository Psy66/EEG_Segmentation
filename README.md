# 🧠 EDF Segment Processor

![EDF Segment Processor](https://img.shields.io/badge/Version-1.0.0-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)

**EDF Segment Processor** is a graphical application designed to process and analyze EDF (European Data Format) files. It allows users to load EDF files, extract metadata, split recordings into segments based on events, and visualize the results.

---

## ✨ Features

- **📂 Open EDF Files**: Load EDF files and extract metadata.
- **🖋️ Segment EDF Data**: Split EDF recordings into segments based on event annotations.
- **📊 Display Metadata**: Show detailed information about the EDF file, including channel details, events, and subject information.
- **⚙️ Customizable Settings**: Set a minimum segment duration for filtering.
- **📋 Structured Output**: Display segment data in a clear, tabular format.
- **📄 Copy Output**: Easily copy text from the output area using `Ctrl+C`.

---

## 🛠️ Installation

1. Ensure you have **Python 3.8** or higher installed.
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python gui.py
   ```

---

## 🖥️ Usage

1. Launch the application.
2. Use the **"Open EDF File"** button to load an EDF file.
3. View metadata, channel information, and event details in the output area.
4. Set the **minimum segment duration** (in seconds) using the input field and click **"Apply"**.
5. Click **"Split into Segments"** to process the EDF file and display the segmented data.
6. Use `Ctrl+C` to copy text from the output area.

---

## 📦 Dependencies

- `tkinter`: For creating the graphical interface.
- `mne`: For reading and processing EDF files.
- `matplotlib`: For visualizing montages.
- `numpy`: For numerical operations.

---

## 📜 License

This project is licensed under the **MIT License**. For details, see the [LICENSE](LICENSE) file.

---

## 👨‍💻 Author

**Tim Liner**  
📧 Email: [psy66@narod.ru](mailto:psy66@narod.ru)

---

## ❓ Support

If you have any questions or suggestions, please contact me at [psy66@narod.ru](mailto:psy66@narod.ru).  
Your feedback and ideas will help make this project better! 🚀
```
