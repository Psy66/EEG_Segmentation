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

## 👨‍💻 Author

**Timur Petrenko**  
📧 Email: [psy66@narod.ru](mailto:psy66@narod.ru)

---

## 📚 Citation

If you use this tool in your research, please consider citing it as follows:

```
Petrenko, Timur. EDF Segment Processor. 2025. Available on GitHub: https://github.com/Psy66/EEG_Segmentation.
```

---

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### 📢 Important Note

This application is intended for educational and research purposes only. Use it at your own risk. The author does not take any responsibility for potential issues or damages caused by the use of this software.

---
