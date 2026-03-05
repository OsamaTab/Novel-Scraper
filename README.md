# 📚 Universal Web Novel to EPUB Scraper

![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)

> A powerful, Dockerized web scraping tool and Web App that automatically downloads web novels and converts them into beautifully formatted `.epub` files for your e-reader.

Built with **FastAPI**, **Botasaurus**, and **EbookLib**, this scraper includes a built-in queue system, a real-time Web UI, and advanced Cloudflare bypass capabilities.

---

## ✨ Features

* 🖥️ **Web Interface:** No command line needed to scrape! Manage your downloads through a sleek, dark-mode web dashboard.
* 🧠 **Universal Scraping:** Smart JavaScript extraction automatically adapts to different website layouts (works on NovelBin, FanMTL, and more).
* 🛡️ **Cloudflare Bypass:** Uses stealth headless Chromium and human-pacing sleep cycles to navigate past aggressive anti-bot protections.
* ⏳ **Job Queue System:** Safely queue up multiple books. The dedicated background worker processes them one at a time so your server never runs out of memory.
* 🎨 **Custom Book Covers:** Upload a local image file directly through the Web UI to embed it as the EPUB cover.
* ✍️ **Author & Metadata:** Add custom author names to your generated EPUBs.
* 📚 **Persistent Library:** Keeps a history of all your downloaded books so you can access them anytime.

---

## 🛠️ Prerequisites

To run this project, you only need one thing installed on your computer:
* 🐳 [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Recommended for Mac/Windows)

---

## 🚀 Installation & Setup

### Method 1: The Docker Way (Recommended & Easiest)
You do **not** need to install Python, Botasaurus, or Chrome on your computer. Docker handles everything in an isolated container!

**1. Clone or download this repository** Make sure all files are in the same folder.

**2. Build the Docker Image** Open your terminal in the folder and run this command. Docker will automatically install all the Python libraries (`requirements.txt`) inside the container for you.
```bash
docker build -t novel-scraper-api .

### Method 2: Using Python
Method 2: Local Python Setup (Manual Installation)

If you prefer to run the scraper directly on your machine without Docker, follow these steps to set up your environment and install the dependencies.

1. Create a Virtual Environment
Open your terminal in the project folder and create an isolated environment to keep your system clean.

Bash
python -m venv venv
2. Activate the Environment
Activate the virtual environment so your terminal uses the local project settings.

Mac/Linux: source venv/bin/activate

Windows: venv\Scripts\activate

3. Install Python Libraries
Install all the necessary tools (Botasaurus, FastAPI, EbookLib, etc.) using the requirements file.

Bash
pip install -r requirements.txt
4. Run the Application
Start the FastAPI server. Once running, you can access the Web UI at http://localhost:8000.

Bash
uvicorn api:app --host 0.0.0.0 --port 8000
📖 How to Use
Once the container (or local server) is running, open your web browser and go to: http://localhost:8000.

Paste the URL of Chapter 1 of the novel you want to scrape.

Enter the Novel Name and (optionally) the Author.

(Optional) Click "Choose File" to upload a cover image from your computer.

Click Start Scraping!

⚠️ Troubleshooting
🛑 The scraper stopped randomly and said "Cloudflare block": Some websites have extremely strict anti-bot systems. Wait a few hours, or connect to a VPN to get a fresh IP address, and try again. The scraper automatically saves its progress, so it will resume right where it left off!

💻 Docker Architecture Errors (Mac vs. Windows): If the image was built on an Apple Silicon (M-series) Mac, it may not run natively on Windows without rebuilding. Run docker build -t novel-scraper-api . on the target machine to ensure the correct architecture is used.

💥 Failed to connect to Chrome URL: You likely forgot to include the --shm-size="2g" flag in your run command. Stop the container and run it again with the flag.

📜 Disclaimer
This tool is for personal, educational use only. Please respect the servers of the websites you are scraping. Heavy scraping can incur server costs for the website owners.
