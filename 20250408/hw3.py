import requests
import csv

def fetch_bus_route_data(route_id, output_file):
    """
    從臺北市公開網站抓取公車路線資料，並輸出為 CSV 格式。
    
    :param route_id: 公車代碼，例如 '0100000A00'
    :param output_file: 輸出的 CSV 檔案名稱
    """
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"
    
    try:
        # 發送 GET 請求
        response = requests.get(url)
        response.raise_for_status()  # 檢查請求是否成功
        
        # 檢查回應內容是否為有效的 JSON
        try:
            data = response.json()
        except ValueError:
            print("伺服器回傳的內容不是有效的 JSON 格式。回應內容如下：")
            print(response.text)
            return
        
        # 解析 JSON 資料
        stops = data.get("Stops", [])
        
        # 檢查是否有資料
        if not stops:
            print("無法取得公車站點資料，請檢查公車代碼是否正確。")
            return
        
        # 開啟 CSV 檔案進行寫入
        with open(output_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # 寫入標題列
            writer.writerow(["arrival_info", "stop_number", "stop_name", "stop_id", "latitude", "longitude"])
            
            # 寫入每個站點的資料
            for stop in stops:
                arrival_info = stop.get("ArrivalTime", "未知")
                stop_number = stop.get("StopSequence", "未知")
                stop_name = stop.get("StopName", "未知")
                stop_id = stop.get("StopID", "未知")
                latitude = stop.get("Latitude", "未知")
                longitude = stop.get("Longitude", "未知")
                
                writer.writerow([arrival_info, stop_number, stop_name, stop_id, latitude, longitude])
        
        print(f"公車路線資料已成功儲存至 {output_file}")
    
    except requests.exceptions.RequestException as e:
        print(f"無法取得資料，請檢查網路連線或公車代碼是否正確。錯誤訊息: {e}")
    except Exception as e:
        print(f"發生錯誤: {e}")

# 測試函數
if __name__ == "__main__":
    route_id = input("請輸入公車代碼 (例如 '0100000A00'): ")
    output_file = "bus_route_data.csv"
    fetch_bus_route_data(route_id, output_file)