import json
import os
from botasaurus.browser import browser, Driver
from ebooklib import epub
import random
from urllib.parse import urljoin
import base64

def create_epub(novel_title, author, chapters, output_filename, cover_data=""):
    book = epub.EpubBook()
    book.set_title(novel_title)
    book.set_language('en')
    
    # --- NEW: Add the Author ---
    if author:
        book.add_author(author)
    
    # --- NEW: Decode the Base64 Cover Image ---
    if cover_data:
        try:
            print("Processing uploaded cover image...")
            # The data looks like "data:image/jpeg;base64,/9j/4AAQ..."
            # We split it at the comma to get just the raw code
            header, encoded = cover_data.split(",", 1)
            
            # Figure out if it's a png, jpg, etc.
            ext = header.split(";")[0].split("/")[1]
            
            # Convert text back to image bytes
            cover_bytes = base64.b64decode(encoded)
            book.set_cover(f"cover.{ext}", cover_bytes)
        except Exception as e:
            print(f"Warning: Could not process cover image. {e}")
    
    spine = ['nav']
    toc = []

    for i, (title, content) in enumerate(chapters):
        file_name = f'chap_{i+1}.xhtml'
        chapter = epub.EpubHtml(title=title, file_name=file_name, lang='en')
        
        html_content = f'<h1>{title}</h1>'
        for paragraph in content:
            if paragraph.strip(): 
                html_content += f'<p>{paragraph}</p>'
        
        chapter.content = html_content
        book.add_item(chapter)
        spine.append(chapter)
        toc.append(chapter)

    book.toc = tuple(toc)
    book.add_item(epub.EpubNav())
    book.spine = spine
    
    epub.write_epub(output_filename, book)
    print(f"\nSuccess! Saved to '{output_filename}'.")

@browser(user_agent='pc', profile='novelbin_session')
def scrape_novel(driver: Driver, data):
    job_id = data["job_id"]
    current_url = data["start_url"] # We start exactly on Chapter 1
    novel_name = data["novel_name"]
    author = data.get("author", "")           # Get the author
    wait = data["wait"]
    cover_data = data.get("cover_data", "")   # Get the image data
    
    progress_file = f"{job_id}_progress.jsonl" 
    final_epub_file = f"{job_id}.epub"
    all_chapters = []
    
    if os.path.exists(progress_file):
        with open(progress_file, "r", encoding="utf-8") as f:
            for line in f:
                all_chapters.append(json.loads(line))
        chapter_number = len(all_chapters) + 1 
        # Note: Resuming is trickier with the breadcrumb method unless you also save the LAST scraped URL.
        # For now, this assumes starting fresh.
    else:
        chapter_number = 1
    
    while True:
        print(f"[{job_id}] Scraping Chapter {chapter_number}: {current_url}")
        driver.get(current_url)
        
        # --- 1. UNIVERSAL WAIT ---
        # Commas act as "OR". It waits if ANY of these common wrappers show up.
        universal_content = "#chr-content, .chapter-content, #chapter-content, .reading-content, .text-left"
        
        try:
            driver.wait_for_element(universal_content, wait=8)
        except Exception:
            print(f"[{job_id}] Content delayed. Checking for Cloudflare...")
            driver.sleep(5)
            if "Just a moment" in driver.title or "security" in driver.title.lower() or "Cloudflare" in driver.title:
                print(f"[{job_id}] Cloudflare block. Attempting to wait...")
                driver.sleep(15)
                if "Just a moment" in driver.title or "security" in driver.title.lower():
                    print(f"[{job_id}] Cloudflare hard block remains. Stopping.")
                    break
            else:
                print(f"[{job_id}] Page loaded but no text found. Ending scrape.")
                break

        # --- 2. UNIVERSAL TITLE EXTRACTION ---
        title_js = """
            let titleEl = document.querySelector('.chr-title, .chapter-title, h1, h2, .title');
            return titleEl ? titleEl.innerText.trim() : null;
        """
        title = driver.run_js(title_js)
        if not title:
            title = f"Chapter {chapter_number}"
            
        # --- 3. UNIVERSAL TEXT EXTRACTION ---
        # This smart JS checks for <p> tags first. If none exist, it grabs all raw text and splits it.
        text_js = """
            let wrapper = document.querySelector('#chr-content, .chapter-content, #chapter-content, .reading-content, .text-left');
            if (!wrapper) return null;
            
            let paragraphs = Array.from(wrapper.querySelectorAll('p'));
            if (paragraphs.length > 0) {
                return paragraphs.map(p => p.innerText);
            } else {
                return wrapper.innerText.split('\\n');
            }
        """
        raw_paragraphs = driver.run_js(text_js)
        
        if raw_paragraphs:
            paragraphs = [p for p in raw_paragraphs if p and p.strip()]
        else:
            print(f"[{job_id}] Could not find text. Website structure might have changed.")
            break

        chapter_data = [ f"Chapter {chapter_number}" , paragraphs]
        all_chapters.append(chapter_data)

        with open(progress_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(chapter_data) + "\n")

        # --- 4. UNIVERSAL NEXT BUTTON FINDER ---
        all_links = driver.select_all("a")
        next_url = None
        
        for link in all_links:
            try:
                text = link.text.strip().lower() if link.text else ""
                el_id = link.get_attribute("id") or ""
                el_class = link.get_attribute("class") or ""
                raw_href = link.get_attribute("href")
                
                is_next_btn = (el_id == "next_chap" or "next" in el_class.lower() or 
                               text == "next" or "next chapter" in text or "next →" in text)
                
                if is_next_btn and raw_href and "javascript" not in raw_href:
                    # THE FIX: Stitch the relative URL to the current domain!
                    full_url = urljoin(current_url, raw_href)
                    
                    if full_url != current_url and ("chapter" in full_url.lower() or "page" in full_url.lower() or "_" in full_url):
                        next_url = full_url
                        break
            except Exception:
                continue 
        
        if next_url:
            current_url = next_url
            chapter_number += 1
            if wait:
                custom_human_sleep(driver, 1.5, 4) 
        else:
            print(f"[{job_id}] No 'Next' button found on the page. Stopping.")
            break
        
        # --- ADD THIS MISSING BLOCK ---
    # Make sure this aligns perfectly with the 'while True:' above it!
    if all_chapters:
        print(f"[{job_id}] Packaging {len(all_chapters)} chapters into EPUB...")
        create_epub(novel_name, author, all_chapters, final_epub_file, cover_data)
               
        # Clean up the JSONL file to save disk space
        if os.path.exists(progress_file):
            os.remove(progress_file)
    else:
        print(f"[{job_id}] No chapters were scraped.")
            
def custom_human_sleep(driver, min_sec, max_sec):
    driver.sleep(random.uniform(min_sec, max_sec))