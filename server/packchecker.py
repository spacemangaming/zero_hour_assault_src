import time
import requests
import os
class Timer:
    def __init__(self):
        self.start_time = time.time()

    def restart(self):
        self.start_time = time.time()

    @property
    def elapsed(self):
        return int((time.time() - self.start_time) * 1000)

def main():
    check_timer = Timer()
    while True:
        time.sleep(5)
        if check_timer.elapsed >= 10000:
            check_timer.restart()
            try: response = requests.get("https://nbmstudios.com/zitemdata.txt")
            except:
                os.system("systemctl restart apache2")
                continue
            body = response.text
            if body and "<title>" not in body:
                lines = body.split("\n")
                with open("zitemdata.txt", "wb") as download:
                    download.write(body.encode())


if __name__ == "__main__":
    main()
