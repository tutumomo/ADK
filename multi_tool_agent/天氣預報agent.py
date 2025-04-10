## 🔥天氣預報
import datetime
import requests
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.agents import LlmAgent

from google.adk.models.lite_llm import LiteLlm

# 城市名稱映射字典，將中文城市名映射到英文
CITY_NAME_MAP = {
    "紐約": "New York",
    "倫敦": "London",
    "東京": "Tokyo",
    "北京": "Beijing",
    "上海": "Shanghai",
    "巴黎": "Paris",
    "柏林": "Berlin",
    "悉尼": "Sydney",
    "莫斯科": "Moscow",
    "迪拜": "Dubai",
    "台中": "Taichung",
    "台北": "Taipei",
    "澳門": "Macau",
    "香港": "Hong Kong",
    "新加坡": "Singapore"
    # 可以繼續添加更多常用城市
}

def get_weather(city: str) -> dict:
    """獲取指定城市的當前天氣報告。

    使用weatherapi.com的API獲取實時天氣數據。
    支持中文城市名，內部會自動轉換為英文名。

    參數:
        city (str): 要獲取天氣報告的城市名稱（中文或英文）。

    返回:
        dict: 包含狀態和結果或錯誤信息的字典。
    """
    # API密鑰和基礎URL
    api_key = "你的key"
    base_url = "http://api.weatherapi.com/v1/current.json"

    # 檢查城市名是否需要轉換為英文
    query_city = CITY_NAME_MAP.get(city, city)

    try:
        # 構建API請求
        params = {
            "key": api_key,
            "q": query_city
        }

        # 發送GET請求到天氣API
        response = requests.get(base_url, params=params)

        # 檢查請求是否成功
        if response.status_code == 200:
            # 解析JSON響應
            data = response.json()

            # 提取相關天氣信息
            location = data["location"]["name"]
            country = data["location"]["country"]
            temp_c = data["current"]["temp_c"]
            temp_f = data["current"]["temp_f"]
            condition = data["current"]["condition"]["text"]
            humidity = data["current"]["humidity"]
            wind_kph = data["current"]["wind_kph"]

            # 構建天氣報告（使用原始輸入的城市名）
            report = (
                f"當前{city}({country})的天氣為{condition}，"
                f"溫度{temp_c}°C ({temp_f}°F)，"
                f"濕度{humidity}%，風速{wind_kph}公里/小時。"
            )

            return {
                "status": "success",
                "report": report,
            }
        else:
            # 處理API錯誤
            return {
                "status": "error",
                "error_message": f"無法獲取'{city}'的天氣信息。API響應代碼: {response.status_code}，請檢查城市名稱是否正確。"
            }
    except Exception as e:
        # 處理其他異常
        return {
            "status": "error",
            "error_message": f"獲取'{city}'的天氣信息時出錯: {str(e)}"
        }

def get_current_time(city: str) -> dict:
    """獲取指定城市的當前時間。

    使用weatherapi.com的API獲取城市的時區信息，
    然後根據時區計算當前時間。
    支持中文城市名，內部會自動轉換為英文名。

    參數:
        city (str): 要獲取當前時間的城市名稱（中文或英文）。

    返回:
        dict: 包含狀態和結果或錯誤信息的字典。
    """
    # API密鑰和基礎URL（與天氣API相同）
    api_key = "7dd6adfdddfb4309ab7132443240409"
    base_url = "http://api.weatherapi.com/v1/current.json"

    # 檢查城市名是否需要轉換為英文
    query_city = CITY_NAME_MAP.get(city, city)

    try:
        # 構建API請求
        params = {
            "key": api_key,
            "q": query_city
        }

        # 發送GET請求到API獲取時區信息
        response = requests.get(base_url, params=params)

        # 檢查請求是否成功
        if response.status_code == 200:
            # 解析JSON響應
            data = response.json()

            # 提取時區ID和本地時間
            tz_id = data["location"]["tz_id"]
            localtime = data["location"]["localtime"]

            # 構建時間報告（使用原始輸入的城市名）
            report = f"當前{city}的時間是 {localtime} ({tz_id}時區)"

            return {
                "status": "success",
                "report": report
            }
        else:
            # 處理API錯誤
            return {
                "status": "error",
                "error_message": f"無法獲取'{city}'的時區信息。API響應代碼: {response.status_code}，請檢查城市名稱是否正確。"
            }
    except Exception as e:
        # 處理其他異常
        return {
            "status": "error",
            "error_message": f"獲取'{city}'的時間信息時出錯: {str(e)}"
        }

# 創建根代理
root_agent = Agent(
    name="weather_time_agent",  # 代理名稱
    model="gemini-2.0-flash-exp",  # 使用的模型
    description=(
        "智能助手，可以回答關於各個城市的天氣和時間問題。"
    ),  # 代理描述
    instruction=(
        "我是一個能夠提供城市天氣和時間信息的智能助手。"
        "當用戶詢問某個城市的天氣情況時，使用get_weather工具獲取最新天氣數據。"
        "當用戶詢問某個城市的當前時間時，使用get_current_time工具獲取準確時間。"
        "請以友好的方式回應用戶的詢問，並提供完整的天氣或時間信息。"
        "我能夠理解中文城市名稱，並自動轉換為對應的英文名。"
    ),  # 代理指令（中文版）
    tools=[get_weather, get_current_time],  # 可用工具
)

