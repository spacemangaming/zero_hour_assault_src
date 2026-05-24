import requests
from events import process_events
from speech import speak
import globals as g
def download_file(url):
    file_name = url.split('/')[-1]
    last_percentage = 0
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length'))
    with open(file_name, 'wb') as file:
        downloaded = 0
        for data in response.iter_content(chunk_size=65536):
            process_events()
            file.write(data)
            downloaded += len(data)
            percentage = (downloaded / total_size) * 100
            if round(last_percentage)!=round(percentage):
                last_percentage=round(percentage)
                speak(str(round(percentage))+"%")
                try: g.p.play_stationary("update_progres_bar.ogg").handle.pitch+=round(percentage)
                except: pass