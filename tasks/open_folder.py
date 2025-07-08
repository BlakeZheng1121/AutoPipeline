import os
import platform
import subprocess

class OpenFolder:
    """打開使用者電腦的資料夾"""
    def run(self, context):
        folder_path = context.get("folder_path") if context else None
        if not folder_path:
            folder_path = os.path.expanduser("~")
        if not os.path.isdir(folder_path):
            print(f"[OpenFolder] 目錄不存在: {folder_path}")
            return False
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(folder_path)
            elif system == "Darwin":
                subprocess.Popen(["open", folder_path])
            else:
                subprocess.Popen(["xdg-open", folder_path])
            return True
        except Exception as e:
            print(f"[OpenFolder] 打開資料夾失敗: {e}")
            return False
