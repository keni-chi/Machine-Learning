import requests

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=DCOILWTICO&scale=left&cosd=2020-07-21&coed=2025-07-21&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-07-28&revision_date=2025-07-28&nd=1986-01-02"

# headers = {
#     "Content-Type": "application/octet-stream; name=spot_summary_2024.csv"
# }

# response = requests.post(url, headers=headers)
response = requests.get(url)

# レスポンスの内容を保存する場合
with open("fred.csv", "wb") as f:
    f.write(response.content)

print("ダウンロード完了:", response.status_code)