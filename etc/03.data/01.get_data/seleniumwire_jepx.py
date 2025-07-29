from seleniumwire import webdriver  # selenium-wireを使う
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


# #####リクエストを表示######
time.sleep(3)
for request in driver.requests:
    if request.response:
        print("📡 URL:", request.url)
        print("📨 Method:", request.method)
        print("📥 Status:", request.response.status_code)
        print("📄 Content-Type:", request.response.headers.get('Content-Type'))
        print("-" * 40)


driver.quit()



# Created TensorFlow Lite XNNPACK delegate for CPU.
# 📡 URL: http://clients2.google.com/time/1/current?cup2key=9:Z_igaSu60fNLV0Uyfa9k2GdijF62ptZAeDHuqKVyOdg&cup2hreq=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: application/json; charset=utf-8
# ----------------------------------------
# 📡 URL: https://accounts.google.com/ListAccounts?gpsia=1&source=ChromiumBrowser&json=standard
# 📨 Method: POST
# 📥 Status: 200
# 📄 Content-Type: application/json; charset=utf-8
# ----------------------------------------
# 📡 URL: https://safebrowsingohttpgateway.googleapis.com/v1/ohttp/hpkekeyconfig?key=AIzaSyA2KlwBX3mkFo30om9LUFYQhpqLoa_BNhE
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: application/ohttp-keys
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/electricpower/market-data/spot/
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: text/html
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/css/jquery-ui.css
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: text/css
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/css/normalize.css
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: text/css
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/css/data-page.css
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: text/css
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/css/common.css
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: text/css
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/img/common/ico-globe.png
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: image/png
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/img/common/logo.png
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: image/png
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/img/common/filters@2x.png
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: image/png
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/js/jquery-3.6.0.min.js
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: application/javascript
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/img/common/ico-mail.png
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: image/png
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/js/jquery-migrate.js
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: application/javascript
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/js/highstock.js
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: application/javascript
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/js/modules/export-data.js
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: application/javascript
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/js/modules/exporting.js
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: application/javascript
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/js/indicators.js
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: application/javascript
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/js/modules/accessibility.js
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: application/javascript
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/js/jquery-ui.min.js
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: application/javascript
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/js/moment.js
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: application/javascript
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/js/moment-ja.js
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: application/javascript
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/js/script.js
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: application/javascript
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/js/graph-common.js
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: application/javascript
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/js/spot_summary.js
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: application/javascript
# ----------------------------------------
# 📡 URL: https://fonts.googleapis.com/css2?family=Noto+Sans&family=Oswald:wght@400;500&display=swap
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: text/css; charset=utf-8
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/img/common/ico-bullet.png
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: image/png
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/img/common/filter-close@2x.png
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: image/png
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/img/common/triangle_w.png
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: image/png
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/img/common/ico-calender@2x.png
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: image/png
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/img/common/ico-check@2x.png
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: image/png
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/img/common/nav-bg@2x.png
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: image/png
# ----------------------------------------
# 📡 URL: https://fonts.gstatic.com/s/oswald/v56/TK3IWkUHHAIjg75cFRf3bXL8LICs1_Fv40pKlN4NNSeSASz7FmlWHYg.woff2
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: font/woff2
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/img/common/ico-download@2x.png
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: image/png
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/img/favicon.ico
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: image/x-icon
# ----------------------------------------
# 📡 URL: https://content-autofill.googleapis.com/v1/pages/ChVDaHJvbWUvMTM4LjAuNzIwNC4xNjkSIAlq8WbFS5vmvhIFDZSQkvoSBQ2UkJL6ITuhblj_QlRg?alt=proto
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: text/plain
# ----------------------------------------
# 📡 URL: https://android.clients.google.com/checkin
# 📨 Method: POST
# 📥 Status: 200
# 📄 Content-Type: application/x-protobuffer
# ----------------------------------------
# 📡 URL: https://android.clients.google.com/c2dm/register3
# 📨 Method: POST
# 📥 Status: 301
# 📄 Content-Type: text/plain; charset=UTF-8
# ----------------------------------------
# 📡 URL: https://android.clients.google.com/c2dm/register3
# 📨 Method: POST
# 📥 Status: 200
# 📄 Content-Type: text/plain; charset=UTF-8
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/js/get_graph_year.php?dir=spot_summary
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: text/html; charset=UTF-8
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/js/get_graph_year.php?dir=spot_index
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: text/html; charset=UTF-8
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/img/common/modal-close@2x.png
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: image/png
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/img/common/ico-down@2x.png
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: image/png
# ----------------------------------------
# 📡 URL: https://www.jepx.jp/_download.php?timestamp=1753621430192
# 📨 Method: POST
# 📥 Status: 200
# 📄 Content-Type: application/octet-stream; name=spot_summary_2024.csv
# ----------------------------------------
# 📡 URL: https://optimizationguide-pa.googleapis.com/v1:GetModels?key=AIzaSyA2KlwBX3mkFo30om9LUFYQhpqLoa_BNhE
# 📨 Method: POST
# 📥 Status: 200
# 📄 Content-Type: application/x-protobuf
# ----------------------------------------
# 📡 URL: https://optimizationguide-pa.googleapis.com/downloads?name=1679317318&target=OPTIMIZATION_TARGET_LANGUAGE_DETECTION
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: text/html; charset=UTF-8
# ----------------------------------------
# 📡 URL: https://optimizationguide-pa.googleapis.com/downloads?name=1745312779&target=OPTIMIZATION_TARGET_NOTIFICATION_PERMISSION_PREDICTIONS
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: text/html; charset=UTF-8
# ----------------------------------------
# 📡 URL: https://optimizationguide-pa.googleapis.com/downloads?name=5&target=OPTIMIZATION_TARGET_PAGE_TOPICS_V2
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: text/html; charset=UTF-8
# ----------------------------------------
# 📡 URL: https://optimizationguide-pa.googleapis.com/downloads?name=1745311339&target=OPTIMIZATION_TARGET_GEOLOCATION_PERMISSION_PREDICTIONS
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: text/html; charset=UTF-8
# ----------------------------------------
# 📡 URL: https://optimizationguide-pa.googleapis.com/downloads?name=1751987362&target=OPTIMIZATION_TARGET_CLIENT_SIDE_PHISHING
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: text/html; charset=UTF-8
# ----------------------------------------
# 📡 URL: https://optimizationguide-pa.googleapis.com/downloads?name=1696268326&target=OPTIMIZATION_TARGET_OMNIBOX_URL_SCORING
# 📨 Method: GET
# 📥 Status: 200
# 📄 Content-Type: text/html; charset=UTF-8
# ----------------------------------------