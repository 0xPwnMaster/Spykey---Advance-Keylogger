
<h1 align="center"> SpyKey </h1>
<p align="center"> A Stealthy, Comprehensive, and Modular Monitoring & Data Exfiltration Solution </p>

<p align="center">
  <img alt="Build" src="https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge">
  <img alt="Issues" src="https://img.shields.io/badge/Issues-0%20Open-blue?style=for-the-badge">
  <img alt="Contributions" src="https://img.shields.io/badge/Contributions-Welcome-orange?style=for-the-badge">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</p>
<!-- 
  **Note:** These are static placeholder badges. Replace them with your project's actual badges.
  You can generate your own at https://shields.io
-->

## Table of Contents
- [⭐ Overview](#-overview)
- [✨ Key Features](#-key-features)
- [🛠️ Tech Stack & Architecture](#️-tech-stack--architecture)
- [🚀 Getting Started](#-getting-started)
- [🔧 Usage](#-usage)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)

## ⭐ Overview

SpyKey is a sophisticated, multi-faceted monitoring and data exfiltration tool designed for digital forensics, incident response, and authorized system oversight.

> In today's complex digital landscape, understanding user activity, identifying suspicious behavior, or performing legitimate system audits can be challenging without specialized tools. Traditional monitoring solutions often lack the stealth, comprehensive data capture, and efficient exfiltration capabilities required for deep insights.

SpyKey addresses these challenges by offering a robust, low-footprint solution for capturing keystrokes, application data, browser credentials, and visual snapshots, all meticulously organized and securely exfiltrated. Its modular design ensures adaptability and discrete operation, making it an invaluable asset for authorized security professionals.

**Inferred Architecture:**
SpyKey operates as a standalone, modular client-side agent written primarily in Python. Its architecture is designed for discreet operation, featuring distinct modules for core keylogging, advanced system data collection (e.g., active applications, URLs), comprehensive credential harvesting (potentially via browser interaction or native host), and robust data exfiltration. An integrated installer streamlines deployment, while collected data is temporarily stored locally before secure transmission.

## ✨ Key Features

*   **Advanced Keylogging:** Captures keystrokes with efficient buffering, ensuring minimal system overhead while maintaining a detailed record of user input in `Keylogs.txt`.
*   **Active Application Monitoring:** Dynamically identifies and logs the active application at the time of keypresses, providing crucial context to user activities through `Get_activeapp_data.py`.
*   **Visual Context Capture (Screenshots/Snapshots):** Periodically captures screenshots or snapshots of the active desktop, offering valuable visual evidence alongside textual logs via `Take_ScreenShot.py` and `Take_snapshot.py`.
*   **Browser URL Detection:** Intelligently detects and logs URLs visited in web browsers, enhancing the scope of monitoring for web-based activities using `url_detection.py`.
*   **Comprehensive Credential Harvesting:** Employs sophisticated mechanisms, including potential browser extension techniques (evident from `manifest.json`, `content.js`, `extract_creds.py`, and `cred_logger.py`), to extract and securely store login credentials in `credentials.txt`.
*   **Secure & Efficient Data Exfiltration:** Gathers, compresses (via `zipper` in `Exfilter.py`), and securely transmits all collected data to a remote destination, incorporating connectivity checks for reliable delivery.
*   **Automated Deployment & Setup:** Features an `Installer.py` script capable of automating the installation of necessary dependencies (Python, Git, Python modules) on the target system, streamlining initial setup.

## 🛠️ Tech Stack & Architecture

| Technology                  | Purpose                                        | Why it was Chosen (Inferred)                                                                                                    |
| :-------------------------- | :--------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------ |
| Python                      | Core Application Logic, Automation             | Versatility, extensive libraries for system interaction, rapid development, and cross-platform potential.                       |
| Browser Extensions (JS, HTML, CSS) | Advanced Credential Harvesting                 | To seamlessly integrate with web browsers for advanced credential interception and extraction.                                    |
| PowerShell                  | System-level Installation & Configuration      | For robust, native system configuration and dependency management on Windows environments during automated setup.                  |
| OS-level Libraries (Generic) | Keylogging, Screenshot Capture, System Monitoring | Provides low-level access to system events (keyboard, screen) and resources for comprehensive, discrete data collection.         |
| Compression Libraries (Generic) | Efficient Data Packaging                       | To optimize data transfer efficiency and reduce storage footprint for collected logs and media before exfiltration.            |

## 🚀 Getting Started

To get SpyKey up and running on your system, follow these steps:

### Prerequisites

*   **Python 3.x:** Ensure you have a recent version of Python installed.
*   **Git:** Required for cloning the repository.

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YourUsername/0xPwnMaster-Spykey---Advance-Keylogger-41410dd.git
    cd 0xPwnMaster-Spykey---Advance-Keylogger-41410dd/Spykey/
    ```

2.  **Run the Installer (Recommended):**
    The project includes an `Installer.py` script designed to set up Python, Git, and necessary Python modules automatically.
    ```bash
    python Installer.py
    ```
    *   **Note:** This script may require administrative privileges to install system-level components.

3.  **Manual Installation (Alternative/If Installer Fails):**
    If the installer does not meet your needs or encounters issues, you can manually install the required Python packages. While no `requirements.txt` is provided, based on the functionalities, common libraries would include:
    ```bash
    # Navigate to the Spykey directory if not already there
    # cd 0xPwnMaster-Spykey---Advance-Keylogger-41410dd/Spykey/

    pip install pynput  # For keylogging
    pip install Pillow  # For screenshots
    pip install psutil  # For active app data
    # Other common libraries like requests, etc., might be needed depending on exfiltration method.
    ```

## 🔧 Usage

Once installed, you can run the main SpyKey application.

1.  **Navigate to the SpyKey Directory:**
    ```bash
    cd 0xPwnMaster-Spykey---Advance-Keylogger-41410dd/Spykey/
    ```

2.  **Start the SpyKey Agent:**
    ```bash
    python main.py
    ```

3.  **Collected Data:**
    *   Keylogs will be saved in `Data_02-July/Keylogs_02-July/Keylogs.txt`.
    *   Credentials, if harvested, will likely be in `Data_02-July/Login/credentials.txt` or a similar location depending on the credential collector module's configuration.
    *   Screenshots will be stored in designated folders within the `Data_02-July/` structure.

*   **Note:** The system will operate discreetly in the background. Ensure you have the necessary authorizations before deploying SpyKey.

## 🤝 Contributing

We welcome contributions to SpyKey! If you have suggestions for improvements, new features, or bug fixes, please follow these steps:

1.  **Fork** the repository.
2.  **Create a new branch** for your feature or bug fix: `git checkout -b feature/your-feature-name` or `bugfix/fix-issue`.
3.  **Make your changes** and ensure they adhere to the project's coding standards.
4.  **Commit your changes** with clear, concise messages.
5.  **Push your branch** to your forked repository.
6.  **Open a Pull Request** against the `main` branch of this repository, describing your changes in detail.

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.