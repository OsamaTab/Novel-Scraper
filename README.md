📚 Universal Web Novel to EPUB Scraper
A powerful, Dockerized web scraping tool and Web App that automatically downloads web novels and converts them into beautifully formatted EPUB files for your e-reader.

Built with FastAPI, Botasaurus, and EbookLib, this scraper includes a built-in queue system, a real-time Web UI, and advanced Cloudflare bypass capabilities.

✨ Features
Web Interface: No command line needed to scrape! Manage your downloads through a sleek, dark-mode web dashboard.

Universal Scraping: Smart JavaScript extraction automatically adapts to different website layouts (works on NovelBin, FanMTL, and more).

Cloudflare Bypass: Uses stealth headless Chromium and human-pacing sleep cycles to navigate past aggressive anti-bot protections.

Job Queue System: Safely queue up multiple books. The dedicated background worker processes them one at a time so your server never runs out of memory.

Custom Book Covers: Upload a local image file directly through the Web UI to embed it as the EPUB cover.

Author & Metadata: Add custom author names to your generated EPUBs.

Persistent Library: Keeps a history of all your downloaded books so you can access them anytime.

🛠️ Prerequisites
To run this project, you only need one thing installed on your computer:

Docker (Docker Desktop recommended for Mac/Windows)

🚀 Installation & Setup
1. Clone or download this repository
Make sure all files (main.py, api.py, index.html, requirements.txt, and Dockerfile) are in the same folder.

2. Open your terminal in the project folder

3. Build the Docker Image
This will download the required Python environment and headless browser. (Note: This may take a few minutes).

Bash
docker build -t novel-scraper-api .
4. Run the Application
Start the container using the command below.
⚠️ Crucial: The --shm-size="2g" flag is required! Chromium needs this extra shared memory to process large novels without crashing.

Bash
docker run -p 8000:8000 --shm-size="2g" -v $(pwd):/app novel-scraper-api
(Note: The -v $(pwd):/app flag syncs your local folder to the container, ensuring your downloaded .epub files and jobs_history.json are saved permanently to your computer!)

📖 How to Use
Once the container is running, open your web browser and go to: http://localhost:8000

Paste the URL of Chapter 1 of the novel you want to scrape.

Enter the Novel Name and (optionally) the Author.

(Optional) Click "Choose File" to upload a cover image from your computer.

Click Start Scraping!

The UI will show you exactly how many chapters have been scraped in real-time. Once the scraper reaches the end of the novel (or hits an insurmountable security block), it will automatically package everything it grabbed and a green Download button will appear in your Library.

⚠️ Troubleshooting
The scraper stopped randomly and said "Cloudflare block": Some websites have extremely strict anti-bot systems. Wait a few hours, or connect to a VPN to get a fresh IP address, and try again. The scraper automatically saves its progress, so it will resume right where it left off!

Docker Architecture Errors (Mac vs. Windows): If the image was built on an Apple Silicon (M-series) Mac, it may not run natively on Windows without rebuilding. Run docker build -t novel-scraper-api . on the target machine to ensure the correct architecture is used.

Failed to connect to Chrome URL: You likely forgot to include the --shm-size="2g" flag in your run command. Stop the container and run it again with the flag.

📜 Disclaimer
This tool is for personal, educational use only. Please respect the servers of the websites you are scraping. Heavy scraping can incur server costs for the website owners.