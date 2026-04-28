# 🚀 Manga-Sync: Custom ETL Pipeline

A custom-built Python ETL pipeline engineered to bypass lazy-loaded media sites, extract digital assets, package them into `.cbz` archives, and securely deploy them to a remote server via SFTP.

## 🏗️ System Architecture & Technical Specifications

This project abandons generic scraping tools in favor of a highly specialized, three-phase ETL architecture:

### [E] Extract (`extractor.py`)
* **Anti-Bot Evasion:** Implements HTTP User-Agent spoofing to masquerade as a macOS Safari browser, effectively bypassing basic 403 Forbidden blocks.
* **Lazy-Loading Bypass:** Uses `BeautifulSoup4` to traverse the DOM tree. Instead of capturing Base64 SVG placeholders in standard `src` tags, it programmatically hunts for authentic image URLs hidden within `data-src`, `data-lazy-src`, and `data-original` attributes.
* **In-Flight Normalization:** Streams raw binary data directly to disk (`wb` mode) while applying strict zero-padding algorithms (e.g., `001.jpg`) to ensure correct lexicographical reading order for media servers.

### [T] Transform (`transformer.py`)
* **Packaging:** Utilizes Python's native `shutil.make_archive` for optimized directory compression into ZIP format.
* **Format Conversion:** Executes an atomic `os.replace` operation to rename the `.zip` container to the Comic Book Zip (`.cbz`) standard, safely overwriting legacy files without raising OS-level exceptions.

### [L] Load (`loader.py`)
* **Secure Transport:** Establishes an encrypted SSH/SFTP tunnel utilizing the `paramiko` library (Transport and SFTPClient).
* **Automated Injection:** Authenticates via environment variables and streams the final `.cbz` payload directly into a remote Pikapods/Komga container, effectively eliminating manual FTP client uploads.

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Core Dependencies:** `requests`, `beautifulsoup4`, `paramiko`, `python-dotenv`
* **Standard Libraries:** `os`, `shutil`

## 🚀 Quick Start

### 1. Environment Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory based on the `.env.example` template to securely pass your credentials to the orchestrator:
```text
SFTP_HOST=your_host_ip
SFTP_PORT=22
SFTP_USER=your_username
SFTP_PASS=your_secure_password
```

### 3. Execution
Run the orchestrator script to initialize the ETL flow. The console will prompt you for the target URL, series name, and chapter number.
```bash
python3 main.py
```

## 👤 Author
**Juan Felipe Guerrero Vanegas (Pipe)**