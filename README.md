# 🃏 AceTrack AI: The Grand Casino Edition

AceTrack AI is a professional-grade computer vision application designed for real-time playing card recognition and Blackjack Hi-Lo strategy analysis. By leveraging the power of **YOLOv11** and a custom **Temporal Majority Voting** algorithm, it provides high-accuracy tracking even with low-confidence model inferences or environmental noise.

---

## 🚀 Key Features

* **YOLOv11 Core:** Utilizes state-of-the-art object detection for instantaneous card labeling.
* **Temporal Majority Voting:** A robust logic layer that aggregates detections over a 1.2s sliding window to eliminate noise and handle diagonal corner duplication.
* **Smart Shoe Management:** Real-time inventory tracking with support for multi-deck (1-8 decks) configurations.
* **Casino-Grade UI:** A premium, dark-themed dashboard inspired by professional blackjack tables, built with `CustomTkinter`.
* **Hi-Lo Strategy Automation:** Real-time running count calculation based on recognized cards.
* **Debounced Recognition:** Implements a temporal lock (cooldown) to prevent redundant counts of the same physical card.

---

## 🛠️ Technical Stack

* **AI/Vision:** Ultralytics (YOLOv11), OpenCV
* **UI Framework:** CustomTkinter, Pillow (PIL)
* **Logic:** NumPy, Collections (Counter)
* **Language:** Python 3.9+

---

## 📦 Quick Start & Installation

To get the analytics engine running on your local machine, execute the following steps:

1. Clone the Repository:
   git clone https://github.com/zer0dayf/AceTrack-AI.git
   cd AceTrack-AI

2. Install Dependencies:
   pip install -r requirements.txt

3. Deploy Model Weights:
   Ensure your trained 'best.pt' file is placed in the root directory.

4. Launch the Application:
   python main.py

---

## 🧠 The "Voting" Engine Logic

In real-world environments, AI models often fluctuate in confidence scores. AceTrack AI doesn't rely on a single frame. Instead:

* **Buffer:** It stores every detection in a short-term temporal buffer.
* **Windowing:** It only analyzes detections from the last 1.2 seconds.
* **Consensus:** A card is only "Recognized" if its label reaches a specific frequency quota (Majority Voting).
* **Locking:** Once recognized, that specific card class is placed in a 4-second cooldown to prevent double-counting.

---

## 🖥️ User Interface Overview

* **Live Stream:** Real-time feed with YOLO bounding box overlays and Casino-themed visuals.
* **Analytics History:** Chronological log of recognized cards and inventory status.
* **Running Count:** High-visibility Hi-Lo score with dynamic color-coding (Red/Green) inside a premium Felt-Green frame.
* **Shoe Config:** On-the-fly deck count adjustment for accurate inventory tracking.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

> **Disclaimer:** This tool is intended for educational and research purposes only. Use of automated tools in regulated casino environments is strictly prohibited.
