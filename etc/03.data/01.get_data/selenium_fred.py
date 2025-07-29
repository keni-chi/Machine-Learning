# pip install selenium webdriver-manager


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# ヘッドレスモード（ブラウザを表示せずに実行）
options = Options()
options.add_argument("--headless")  # ブラウザを非表示
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# ドライバーの起動
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ページを開く
url = "https://fred.stlouisfed.org/series/DCOILWTICO"  # ← スクレイピングしたいURLをここに書く
driver.get(url)

# JavaScriptのレンダリングを待機（適宜調整）
time.sleep(5)

# ページのHTMLを取得
html = driver.page_source

# ファイルに保存
with open("rendered_page_fred.html", "w", encoding="utf-8") as f:
    f.write(html)

# ブラウザを閉じる
driver.quit()

