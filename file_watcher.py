import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# İzlenecek dizin
WATCHED_DIR = '/home/zeynep/bsm/test'  # İzlemek istediğiniz dizini buraya yazın

# JSON dosyasının yolu
LOG_FILE = '/home/zeynep/bsm/logs/changes.json'

# Dosya değişikliklerini kaydeden sınıf
class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Dosya değişikliği tespit edildiğinde çalışacak fonksiyon
        if not event.is_directory:
            self.log_change(event)

    def on_created(self, event):
        # Dosya oluşturulduğunda çalışacak fonksiyon
        if not event.is_directory:
            self.log_change(event)

    def on_deleted(self, event):
        # Dosya silindiğinde çalışacak fonksiyon
        if not event.is_directory:
            self.log_change(event)

    def log_change(self, event):
        # Değişiklik bilgilerini JSON formatında dosyaya yazma
        change = {
            'event_type': event.event_type,  # created, modified, deleted
            'file_path': event.src_path,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # JSON dosyasına yazma
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as file:
                logs = json.load(file)
        else:
            logs = []
        
        logs.append(change)
        
        # Yeni logu dosyaya kaydetme
        with open(LOG_FILE, 'w') as file:
            json.dump(logs, file, indent=4)

# İzleyici başlatma
def start_watcher():
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCHED_DIR, recursive=False)  # Yalnızca belirtilen dizini izle
    observer.start()
    print(f"Watching for changes in: {WATCHED_DIR}")
    
    try:
        while True:
            pass  # Sonsuza kadar çalışacak
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_watcher()
