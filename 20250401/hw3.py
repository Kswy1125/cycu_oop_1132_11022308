import requests
import html
from bs4 import BeautifulSoup

# 設定 User-Agent 避免被封鎖
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_bus_arrival_time(stop_name: str):
    """
    根據輸入的車站名稱，顯示幾分鐘後公車會到達。
    """
    # 公車動態資訊的 URL (替換為實際的動態資訊 URL)
    url = "https://pda5284.gov.taipei/MQS/RouteDyna?routeid=10417"  # 替換為實際的動態資訊 URL

    try:
        # 發送 GET 請求
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # 找到所有車站的動態資訊
        stops = soup.find_all("tr", class_=["ttego1", "ttego2", "tteback1", "tteback2"])

        # 測試：列出所有 <tr> 的內容，檢查結構
        print("檢查 HTML 結構：")
        for stop in stops:
            print(stop.prettify())

        # 遍歷車站，尋找匹配的車站名稱
        for stop in stops:
            td_list = stop.find_all("td")
            if td_list and len(td_list) > 1:  # 確保有多個 <td>，避免索引錯誤
                current_stop_name = html.unescape(td_list[0].text.strip())  # 第一個 <td> 是車站名稱
                print(f"檢查車站名稱: {current_stop_name}")
                if stop_name.strip() in current_stop_name:  # 比對車站名稱
                    # 提取到站時間資訊
                    arrival_time = html.unescape(td_list[-1].text.strip())  # 假設到站時間在最後一個 <td>
                    print(f"車站: {current_stop_name}，到站時間: {arrival_time}")
                    return

        print(f"找不到車站: {stop_name} 的到站資訊。")

    except requests.exceptions.RequestException as e:
        print(f"❌ 無法取得公車動態資訊: {e}")

# 測試函數
if __name__ == "__main__":
    stop_name = input("請輸入車站名稱: ")
    get_bus_arrival_time(stop_name)