# 📚 Universal Web Novel to EPUB Scraper

![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)

> A powerful, Dockerized web scraping tool and Web App that automatically downloads web novels and converts them into beautifully formatted `.epub` files for your e-reader.

Built with **FastAPI**, **Botasaurus**, and **EbookLib**, this scraper includes a built-in queue system, a real-time Web UI, and advanced Cloudflare bypass capabilities.

---

## 📸 Preview
![Web UI Screenshot](assets/web-ui-screenshot.png)

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

### Method 1: Using the Pre-built Release (Fastest)
If you downloaded the `novel-scraper-api.tar.gz` from the [Releases page](https://github.com/OsamaTab/Novel-Scraper/releases), you don't need to build anything.

1. **Load the image:**
   ```bash
   docker load -i novel-scraper-api.tar.gz
   ```
2. **Run the container:**
   ```bash
   docker run -p 8000:8000 --shm-size="2g" novel-scraper-api
   ```

---

### Method 2: The Docker Way (Manual Build)
Docker handles everything in an isolated container! No need to install Python or Chrome locally.

1. **Clone this repository.**
2. **Build the Docker Image:** Open your terminal in the root folder and run:
   ```bash
   docker build -t novel-scraper-api -f app/Dockerfile .
   ```
3. **Run the container (replace v1.0.4 with your actual tag):**
   ```bash
   docker run -p 8000:8000 --shm-size="2g" novel-scraper-api:v1.0.4
   ```

---

### Method 3: Local Python Setup (Manual Installation)
If you prefer to run the scraper directly on your machine:

1. **Navigate to the app folder:**
   ```bash
   cd app
   ```
2. **Create and Activate a Virtual Environment:**
   * **Windows:** `python -m venv venv` && `venv\Scripts\activate`
   * **Mac/Linux:** `python3 -m venv venv` && `source venv/bin/activate`
3. **Install Requirements:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Application:**
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

## ⚖️ License

Copyright (c) 2026 Osama.

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**. 

**Summary of Terms:**
- ✅ **Personal Use**: You are free to use, copy, and modify this for your own use.
- ✅ **Attribution**: You must give credit to the original author.
- ❌ **No Commercial Use**: You may NOT sell this software, use it for profit, or include it in any commercial service.

For commercial licensing or business inquiries, please reach out via GitHub.