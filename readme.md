# HKUST AC Controller 🇭🇰❄️

**A smart controller to save money on your HKUST dorm AC.**

Tired of the time-based AC charges in HKUST dorms? This script helps you save money by automatically cycling your air conditioner, keeping your room cool without running 24/7.

---

## ✨ Features

-   **Automatic Cycling**: Automatically turns the AC on and off at regular intervals.
-   **Customizable Intervals**: Easily set your desired on/off duration (default is 30 minutes).
-   **Simple GUI**: A user-friendly graphical interface, no command-line skills needed.
-   **Cost-Efficient**: Designed specifically to tackle the time-based charging system in HKUST accommodation.

---

## 🚀 Getting Started

### Prerequisites

-   Python 3.13 or newer.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Nook001/HKUST_AC_CONTROLLER.git](https://github.com/Nook001/HKUST_AC_CONTROLLER.git)
    ```
2.  **Navigate to the project root directory**
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🎮 How to Use

1.  **Run the application:**
    ```bash
    python main_window.py
    ```

2.  **Input your Token:**
    Follow the steps below to get your token, then paste it into the application.

3.  **Set Interval & Start:**
    Enter your desired on/off interval in minutes and click "Start". The controller will begin its cycle.

---

## 🔑 How to Get Your Token

Your token is required to authorize control over your AC. Please keep it secure and do not share it with others.

1.  Log in to the [HKUST Accommodation AC Control Website](https://w5.ab.ust.hk/njggt/app/home).
2.  Open the Developer Tools in your browser (usually by pressing `F12`).
3.  Go to the **Network** tab.
4.  Refresh the page to capture network requests.
5.  In the filter box, you can type `ac` to easily find the right request. Click on any request named `ac-balance`, `ac_status`, or `check`.
    
6.  In the new panel that appears, go to the **Headers** tab.
7.  Scroll down to the **Request Headers** section.
8.  Find the `Authorization` header. The value will look like `Bearer eyJhbGciOi...`.
9.  Copy the long string of characters **after** the word `"Bearer "` (you don't need to copy `"Bearer "` itself).

---

## 📄 License

This project is licensed under the MIT License.