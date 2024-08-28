---

# MangaDownloader

MangaDownloader is a command-line Python application that utilizes the MangaDex API to download manga chapters and compile them into PDF format. This tool is designed for manga enthusiasts who want to keep a local collection or enjoy reading offline. Users can download individual chapters or entire manga series with ease.

## Features

- **Download Individual Chapters:** Specify a chapter to download it as a neatly compiled PDF.
- **Download Entire Manga:** Automate the download of all available chapters of a manga.
- **Interactive CLI:** Provides a user-friendly command-line interface to search for manga, choose specific chapters, or download entire series.
- **Concurrent Downloads:** Utilizes multi-threading to download images concurrently, speeding up the process.
- **Clear and Informative Output:** Includes progress bars and detailed messages about the download process and any errors encountered.

## Prerequisites

Before running MangaDownloader, ensure you have Python 3 and pip installed on your system. The tool also requires the following Python libraries:
- `PIL` for image handling
- `reportlab` for creating PDF files
- `requests` for making HTTP requests
- `tqdm` for displaying progress bars

## Installation

To install MangaDownloader, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Braeulias/Manga_Downloader.git
   cd MangaDownloader
   ```

2. **Install required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To start using MangaDownloader, navigate to the repository's directory and execute the script:

```bash
python Mangadownload.py
```

You will be prompted to enter the title of the manga. After selecting the desired manga from the search results, you can choose to download a specific chapter or all chapters available.

### Example Commands

- **Download a specific chapter:**

  ```bash
  Enter the chapter number you want to download, or '*' to download all: 5
  ```

- **Download all chapters of a manga:**

  ```bash
  Enter the chapter number you want to download, or '*' to download all: *
  Confirm download of all chapters? (yes/no) [default: yes]: yes
  ```

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

The API belongs to Mangadex, and so do all files. The Mangas are owned by the publishers, and all the rights belong to them. Therefore support them

---
