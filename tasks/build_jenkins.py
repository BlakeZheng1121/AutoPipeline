import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
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
            # 頁面開啟後將視窗最大化
            driver.maximize_window()
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
            # 僅點擊 href 完全等於 job/S053/ 的連結
            project_selector = 'a[href="job/S053/"]'
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, project_selector)))

            # 點擊 S053 專案展開選單
            project = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, project_selector))
            )
            project.click()

            # 選擇「帶參數建置」並等待頁面跳轉
            current_url = driver.current_url
            param_build = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "帶參數建置"))
            )
            param_build.click()
            print("[BuildJenkinsProject] 已選擇帶參數建置，等待頁面載入...")
            wait.until(EC.url_changes(current_url))
            new_url = driver.current_url
            print(f"[BuildJenkinsProject] 跳轉後網址: {new_url}")
            driver.get(new_url)

            # 等待參數頁面載入後再尋找下拉式選單
            wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "tr.jenkins-form-item")
                )
            )

            rows = driver.find_elements(By.CSS_SELECTOR, "tr.jenkins-form-item")
            print(f"[BuildJenkinsProject] 找到 {len(rows)} 個下拉式選單")
            for row in rows:
                try:
                    name_elem = row.find_element(By.CSS_SELECTOR, "td.setting-name")
                    name = name_elem.text.strip()
                except Exception:
                    name = "(unknown)"

                try:
                    select_elem = row.find_element(By.TAG_NAME, "select")
                    options = [o.text.strip() for o in select_elem.find_elements(By.TAG_NAME, "option")]
                except Exception:
                    options = []

                print(f"[BuildJenkinsProject] 選單名稱: {name}，內容: {options}")

        except Exception as e:
            print(f"[BuildJenkinsProject] 發生錯誤: {e}")
        finally:
            input("[BuildJenkinsProject] 任務完成，按 Enter 關閉瀏覽器...")
            driver.quit()

        return True
