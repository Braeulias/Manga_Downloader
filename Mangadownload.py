#!/usr/bin/env python3



from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
from reportlab.pdfgen import canvas
import requests
import os
import platform


os.environ['TERM'] = 'xterm'  # or another appropriate terminal type like 'vt100'


def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def fetch_all_chapters(manga_id):
    chapters = []
    limit = 100  # Adjust based on what the API allows
    offset = 0
    while True:
        chapters_response = requests.get(f"{base_url}/manga/{manga_id}/feed", params={
            "translatedLanguage[]": ["en"],
            "limit": limit,
            "offset": offset,
            "order[chapter]": "asc",
            "includeFuturePublishAt": 0  # Only show chapters published up to now
        })
        chapters_data = chapters_response.json()



        if chapters_response.status_code == 200 and 'data' in chapters_data:
            fetched_chapters = chapters_data['data']
            chapters.extend(fetched_chapters)

            if len(fetched_chapters) < limit:
                break
            offset += limit
        else:
            print(f"Failed to fetch chapters. ERROR: {chapters_response.status_code}")
            print(chapters_data.get('errors', []))  # Print out any errors for debugging
            break  # Break the loop if there's an error
    return chapters


def download_image(image_url, path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            file.write(response.content)
        return path
    return None

def download_chapter_images_and_create_pdf(chapter_id, manga_title, chapter_number, quality='data'):
    response = requests.get(f"https://api.mangadex.org/at-home/server/{chapter_id}")
    if response.status_code == 200:
        chapter_info = response.json()
        base_url = chapter_info['baseUrl']
        hash_code = chapter_info['chapter']['hash']
        file_names = chapter_info['chapter'][quality]

        downloads_path = os.path.expanduser('~/Downloads')
        sanitized_manga_title = manga_title.replace('/', '_').replace('\\', '_')
        chapter_dir_name = f"{sanitized_manga_title}_Chapter_{chapter_number}"
        chapter_download_path = os.path.join(downloads_path, chapter_dir_name)
        os.makedirs(chapter_download_path, exist_ok=True)

        pdf_path = os.path.join(chapter_download_path, f"{chapter_dir_name}.pdf")
        c = canvas.Canvas(pdf_path)

        # Concurrently download images
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(download_image, f"{base_url}/{quality}/{hash_code}/{file_name}", os.path.join(chapter_download_path, file_name)): file_name for file_name in file_names}
            for future in as_completed(future_to_url):
                file_name = future_to_url[future]
                try:
                    temp_img_path = future.result()
                    if temp_img_path:
                        # Open image to add to PDF
                        with Image.open(temp_img_path) as img:
                            img_width, img_height = img.size
                            c.setPageSize((img_width, img_height))
                            c.drawImage(temp_img_path, 0, 0)
                            c.showPage()
                        # Optionally delete the image file after adding to PDF
                        os.remove(temp_img_path)
                        print(f"Added {file_name} to PDF")
                except Exception as exc:
                    print(f"{file_name} generated an exception: {exc}")

        # Save PDF
        c.save()
        print(f"Chapter saved as PDF at {pdf_path}")
    else:
        print(f"Failed to fetch chapter info. Status code: {response.status_code}")




clear_screen()
title = input("Enter the manga title you want to search for: ")

base_url = "https://api.mangadex.org"

response = requests.get(f"{base_url}/manga", params={"title": title})
if response.status_code == 200:
    data = response.json()

    mangas = []
    if 'data' in data:
        for index, manga in enumerate(data['data'], start=1):
            manga_id = manga['id']
            manga_attributes = manga['attributes']
            manga_title = manga_attributes['title'].get('en', 'No title available')

            author_ids = [rel['id'] for rel in manga['relationships'] if rel['type'] in ['author', 'artist']]
            author_names = []

            for author_id in author_ids:
                author_response = requests.get(f"{base_url}/author/{author_id}")
                author_data = author_response.json()
                if 'data' in author_data:
                    author_attributes = author_data['data']['attributes']
                    author_names.append(author_attributes['name'])

            authors = ", ".join(author_names)

            print("\n" + "="*50)
            print(f"Manga #{index}:")
            print("="*50)

            print(f"Manga ID: {manga_id}")
            print(f"Manga Title: {manga_title}")
            print(f"Author(s)/Artist(s): {authors}")
            print(f"Description: {manga_attributes['description'].get('en', 'No description available')}")
            print(f"Status: {manga_attributes['status']}")

            mangas.append((index, manga))

    else:
        print("No data found.")
else:
    print(f"No data found. ERROR: {response.status_code}")


try:
    select_index = int(input("\nType the number (index) of the Manga you want to select: ")) - 1
    selected_manga = mangas[select_index][1]  # Get the manga dictionary by index

    clear_screen()

    manga_id = selected_manga['id']
    manga_attributes = selected_manga['attributes']
    manga_title = manga_attributes['title'].get('en', 'No title available')

    # Fetch all chapters in English
    chapters = fetch_all_chapters(manga_id)

    print("\n" + "="*100)
    print("Selected Manga Details:")
    print("="*100)

    print(f"Manga ID: {manga_id}")
    print(f"Manga Title: {manga_title}")
    print(f"Status: {manga_attributes['status']}")

    if chapters:
        print("\nChapters available in English:")
        for chapter in chapters:
            chapter_id = chapter['id']
            chapter_attributes = chapter['attributes']
            chapter_title = chapter_attributes.get('title', 'No title')
            chapter_number = chapter_attributes.get('chapter', 'N/A')
            print(f"Chapter {chapter_number}: {chapter_title} ")
    else:
        print("No chapters found for this manga in English.")
except IndexError:
    print("Invalid selection. Please run the script again and select a valid index.")
except ValueError:
    print("Invalid input. Please enter a number.")

chapter_number = input("Enter the chapter number you want to download: ")
for chapter in chapters:
    if chapter['attributes']['chapter'] == chapter_number:
        print(f"Chapter {chapter_number} selected. Title: {chapter['attributes'].get('title', 'No title')}")
        confirm = input("Confirm download? (yes/no): ")
        if confirm.lower() in ['yes', '']:
            download_chapter_images_and_create_pdf(chapter['id'], chapter['attributes'].get('title', 'No title'), chapter_number)
        else:
            print("Download cancelled.")
        break
else:
    print("Chapter not found.")
