from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Chromeの設定（ダウンロードフォルダ指定）
download_dir = "/path/to/save"  # ← 保存先を指定
options = Options()
# options.add_argument("--headless")
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# ドライバー起動
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.jepx.jp/electricpower/market-data/spot/")

# モーダルを開く（「データダウンロード」ボタンをクリック）
time.sleep(2)
download_button = driver.find_element(By.CLASS_NAME, "dl-button")
download_button.click()

# モーダル内のセレクトボックスで「2024年度」を選択
time.sleep(1)
select_box = driver.find_element(By.ID, "dl-select--spot_summary")
for option in select_box.find_elements(By.TAG_NAME, "option"):
    if "2024年度" in option.text:
        option.click()
        break

# ダウンロードボタンをクリック
submit_button = driver.find_element(By.CSS_SELECTOR, "form[action*='_download.php'] button")
submit_button.click()

# ダウンロード待機（環境によって調整）
time.sleep(5)


driver.quit()