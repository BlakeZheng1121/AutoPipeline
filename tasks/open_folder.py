import os
import platform
import subprocess

class OpenFolder:
    """打開使用者電腦的資料夾，並自動點擊其中的 Downloads"""

    def run(self, context):
        folder_path = context.get("folder_path") if context else None
        if not folder_path:
            folder_path = os.path.expanduser("~")

        if not os.path.isdir(folder_path):
            print(f"[OpenFolder] 目錄不存在: {folder_path}")
            return False

        downloads_path = os.path.join(folder_path, "Downloads")

        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(folder_path)
                if os.path.isdir(downloads_path):
                    os.startfile(downloads_path)
            elif system == "Darwin":
                subprocess.Popen(["open", folder_path])
                if os.path.isdir(downloads_path):
                    subprocess.Popen(["open", downloads_path])
            else:
                subprocess.Popen(["xdg-open", folder_path])
                if os.path.isdir(downloads_path):
                    subprocess.Popen(["xdg-open", downloads_path])

            return True
        except Exception as e:
            print(f"[OpenFolder] 打開資料夾失敗: {e}")
            return False
