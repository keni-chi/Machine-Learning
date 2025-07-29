import requests

url = "https://www.jepx.jp/_download.php?timestamp=1753621430192"

headers = {
    "Content-Type": "application/octet-stream; name=spot_summary_2024.csv"
}

response = requests.post(url, headers=headers)

# レスポンスの内容を保存する場合
with open("spot_summary_2024.csv", "wb") as f:
    f.write(response.content)

print("ダウンロード完了:", response.status_code)