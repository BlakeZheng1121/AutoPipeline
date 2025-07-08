import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

class BuildJenkinsProject:
    """登入 Jenkins 並建置專案 S053"""
    def run(self, context):
        load_dotenv()

        JENKINS_URL = os.getenv("JENKINS_URL")
        JENKINS_USER = os.getenv("JENKINS_USER")
        JENKINS_PASS = os.getenv("JENKINS_PASS")

        if not all([JENKINS_URL, JENKINS_USER, JENKINS_PASS]):
            print("[BuildJenkinsProject] 請確認 .env 檔已正確設置")
            return False

        options = Options()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)

        try:
            print("[BuildJenkinsProject] 開啟 Jenkins...")
            driver.get(JENKINS_URL)
            time.sleep(2)

            # 移動滑鼠到登入按鈕並點擊
            login_btn = driver.find_element(By.LINK_TEXT, "登入")
            ActionChains(driver).move_to_element(login_btn).click().perform()
            wait.until(EC.presence_of_element_located((By.NAME, "j_username")))

            # 自動輸入帳號密碼
            driver.find_element(By.NAME, "j_username").send_keys(JENKINS_USER)
            driver.find_element(By.NAME, "j_password").send_keys(JENKINS_PASS)
            driver.find_element(By.NAME, "Submit").click()
            # 等待登入後首頁載入
            project_selector = 'a[href*="job/S053/"]'
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, project_selector)))

            # 點擊 S053 專案並確認已進入頁面
            project = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, project_selector)))
            project.click()
            wait.until(EC.presence_of_element_located((By.LINK_TEXT, "建置專案")))

            # 點擊建置
            build_btn = driver.find_element(By.LINK_TEXT, "建置專案")
            build_btn.click()
            print("[BuildJenkinsProject] 已觸發建置 S053！")
            time.sleep(5)

        except Exception as e:
            print(f"[BuildJenkinsProject] 發生錯誤: {e}")
        finally:
            input("[BuildJenkinsProject] 任務完成，按 Enter 關閉瀏覽器...")
            driver.quit()

        return True
