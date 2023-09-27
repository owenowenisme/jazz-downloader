import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import concurrent.futures

threads = []
def fetch_score(id):
    url = f'https://www.sheetmusicplus.com/title/{id}'  
    image_url = f'https://d29ci68ykuu27r.cloudfront.net/items/{id}/cover_images/cover-large_file.png'
    try:
        response = requests.get(url)
        content = response.content.decode()
        if response.status_code == 200:
            # Get the HTML content from the response

            soup = BeautifulSoup(content, 'html.parser')
            h1tag=soup.find('h1')
            score_title = h1tag.get_text(separator="\n",strip=True).split('\n')[0]
            print(score_title)
        else:
                score_title=id
                print(f"Failed to retrieve HTML. Status code: {response.status_code}")

        response = requests.get(image_url)
        if response.status_code == 200:
            image_data = response.content
            image = Image.open(BytesIO(image_data))
            image.save(score_title+".png")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
     

max_threads = 10  

with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
    futures = {executor.submit(fetch_score, id): id for id in range(21882250,21882300+1)}

    for future in concurrent.futures.as_completed(futures):
        url = futures[future]
        try:
            future.result() 
        except Exception as e:
            print(f"Failed to fetch data from {url}: {e}")

print("All tasks have finished.")
