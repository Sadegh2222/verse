import subprocess

def download_song(query):
    try:
        # اجرای SpotDL برای دانلود آهنگ
        result = subprocess.run(["spotdl", query], capture_output=True, text=True, timeout=60)
        return result.stdout  # مسیر فایل دانلود شده
    except Exception as e:
        return str(e)
