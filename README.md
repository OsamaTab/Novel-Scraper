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

1. **Clone or download this repository:** Make sure all files are in the same folder.
2. **Build the Docker Image:** Open your terminal in the folder and run this command:
```bash
docker build -t novel-scraper-api .
```

3. **Run the Container:**
```bash
docker run -p 8000:8000 --shm-size="2g" novel-scraper-api
```

---

### Method 2: Local Python Setup (Manual Installation)

If you prefer to run the scraper directly on your machine without Docker, follow these steps:

1. **Create a Virtual Environment**
```bash
python -m venv venv
```

2. **Activate the Environment**
* **Mac/Linux:** `source venv/bin/activate`
* **Windows:** `venv\Scripts\activate`

3. **Install Python Libraries**
```bash
pip install -r requirements.txt
```

4. **Run the Application**
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

---

## 📖 How to Use
1. Once the container (or local server) is running, open your web browser and go to: **http://localhost:8000**.
2. Paste the URL of **Chapter 1** of the novel you want to scrape.
3. Enter the **Novel Name** and (optionally) the **Author**.
4. (Optional) Click **"Choose File"** to upload a cover image from your computer.
5. Click **Start Scraping!**

---

## ⚠️ Troubleshooting

* 🛑 **Cloudflare block:** Some websites have strict anti-bot systems. Wait a few hours or use a VPN. The scraper saves progress and will resume where it left off!
* 💻 **Architecture Errors:** If building on Mac (M-series) to run on Windows, rebuild the image on the target machine: `docker build -t novel-scraper-api .`
* 💥 **Failed to connect to Chrome:** Ensure you included the `--shm-size="2g"` flag in your run command.

---

## 📜 Disclaimer
This tool is for personal, educational use only. Please respect website terms of service and server costs.
