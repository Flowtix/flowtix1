import threading
from queue import Queue
from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

import yt_dlp

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]

DOWNLOADS_DIR = Path("temp_downloads")


class VideoTask:
    def __init__(self, url, title, description, tags):
        self.url = url
        self.title = title
        self.description = description
        self.tags = tags


class AtlasUI(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.youtube = None
        self.queue = Queue()

        threading.Thread(target=self.worker, daemon=True).start()

    def log(self, text):
        Clock.schedule_once(lambda dt: setattr(self.ids.log, "text", self.ids.log.text + text + "\n"))

    def connect_youtube(self):
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            self.youtube = build("youtube", "v3", credentials=creds)
            self.log("Connected to YouTube")

        except Exception as e:
            self.log(str(e))

    def fetch_info(self):

        url = self.ids.url.text

        try:
            ydl = yt_dlp.YoutubeDL({"quiet": True})
            info = ydl.extract_info(url, download=False)

            self.ids.title.text = info.get("title", "")
            self.ids.description.text = info.get("description", "")
            self.ids.tags.text = ",".join(info.get("tags", []))

            self.log("Video info fetched")

        except Exception as e:
            self.log(str(e))

    def add_task(self):

        url = self.ids.url.text
        title = self.ids.title.text
        description = self.ids.description.text
        tags = self.ids.tags.text.split(",")

        task = VideoTask(url, title, description, tags)

        self.queue.put(task)

        self.log("Added video to queue")

    def worker(self):

        DOWNLOADS_DIR.mkdir(exist_ok=True)

        while True:

            task = self.queue.get()

            try:

                self.log("Downloading video")

                ydl_opts = {
                    "outtmpl": str(DOWNLOADS_DIR / "%(title)s.%(ext)s"),
                    "format": "best",
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(task.url, download=True)
                    file_path = ydl.prepare_filename(info)

                self.log("Uploading video")

                body = {
                    "snippet": {
                        "title": task.title,
                        "description": task.description,
                        "tags": task.tags,
                        "categoryId": "22",
                    },
                    "status": {
                        "privacyStatus": "private"
                    }
                }

                media = MediaFileUpload(file_path, resumable=True)

                request = self.youtube.videos().insert(
                    part="snippet,status",
                    body=body,
                    media_body=media
                )

                response = None

                while response is None:
                    status, response = request.next_chunk()

                self.log("Upload complete")

                Path(file_path).unlink(missing_ok=True)

            except Exception as e:
                self.log(str(e))

            finally:
                self.queue.task_done()


class AtlasApp(App):

    def build(self):
        return AtlasUI()


AtlasApp().run()