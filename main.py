import asyncio
import schedule
from telegram import Bot
import requests
import json
import pandas as pd
import pytz
from datetime import datetime
import time
import yaml
from tabulate import tabulate
from binance.client import Client

with open("./config/config.yml", "r") as ymlfile:
	cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)


TELEGRAM_BOT_TOKEN_hungdv_bot = cfg['telethon']['TELEGRAM_BOT_TOKEN_hungdv_bot']
TELEGRAM_CHAT_ID_Bot_Order_HungAI = cfg['telethon']['TELEGRAM_CHAT_ID_Bot-Order-HungAI']
YOUR_API_KEY = cfg['binance']['YOUR_API_KEY']
YOUR_API_SECRET = cfg['binance']['YOUR_API_SECRET']



coin_list = [{'symbol': 'BTC'},
 {'symbol': 'ETH'},
 {'symbol': 'XRP'},
 {'symbol': 'BNB'},
 {'symbol': 'LTC'},
 {'symbol': 'DOGE'},
 {'symbol': 'APT'},
 {'symbol': 'SOL'},
 {'symbol': 'MATIC'},
 {'symbol': 'ADA'},
 {'symbol': 'DOT'},
 {'symbol': 'ETC'},
 {'symbol': 'LINK'},
 {'symbol': 'OP'},
 {'symbol': 'FTM'},
 {'symbol': 'BCH'},
 {'symbol': 'APE'},
 {'symbol': 'EOS'},
 {'symbol': 'AVAX'},
 {'symbol': 'CRV'},
 {'symbol': 'SAND'},
 {'symbol': 'DYDX'},
 {'symbol': 'FIL'},
 {'symbol': 'TRX'},
 {'symbol': 'GALA'},
 {'symbol': 'ATOM'},
 {'symbol': 'AXS'},
 {'symbol': 'NEAR'},
 {'symbol': 'GMT'},
 {'symbol': 'LDO'},
 {'symbol': 'GRT'},
 {'symbol': '1000SHIB'},
 {'symbol': 'MANA'},
 {'symbol': 'AAVE'},
 {'symbol': 'CHZ'},
 {'symbol': 'UNI'},
 {'symbol': 'MASK'},
 {'symbol': 'SUSHI'},
 {'symbol': 'WAVES'},
 {'symbol': 'ZIL'},
 {'symbol': 'DASH'},
 {'symbol': 'XMR'},
 {'symbol': '1000LUNC'},
 {'symbol': 'SXP'},
 {'symbol': 'ROSE'},
 {'symbol': 'MAGIC'},
 {'symbol': 'MINA'},
 {'symbol': 'HOOK'},
 {'symbol': 'EGLD'},
 {'symbol': 'XLM'},
 {'symbol': 'ALGO'},
 {'symbol': 'PEOPLE'},
 {'symbol': 'LRC'},
 {'symbol': 'THETA'},
 {'symbol': 'SNX'},
 {'symbol': 'ICP'},
 {'symbol': 'ZEC'},
 {'symbol': 'FET'},
 {'symbol': 'HBAR'},
 {'symbol': 'ZEN'},
 {'symbol': 'STG'},
 {'symbol': 'FXS'},
 {'symbol': 'ENS'},
 {'symbol': 'IMX'},
 {'symbol': 'LUNA2'},
 {'symbol': 'MKR'},
 {'symbol': 'OCEAN'},
 {'symbol': 'RNDR'},
 {'symbol': 'KLAY'},
 {'symbol': 'DUSK'},
 {'symbol': 'FLOW'},
 {'symbol': '1INCH'},
 {'symbol': 'ENJ'},
 {'symbol': 'RUNE'},
 {'symbol': 'KSM'},
 {'symbol': 'XTZ'},
 {'symbol': 'COMP'},
 {'symbol': 'YFI'},
 {'symbol': 'REN'},
 {'symbol': 'TRB'},
 {'symbol': 'NEO'},
 {'symbol': 'INJ'},
 {'symbol': 'LIT'},
 {'symbol': 'VET'},
 {'symbol': 'AR'},
 {'symbol': 'SKL'},
 {'symbol': 'BAND'},
 {'symbol': 'STORJ'},
 {'symbol': 'ONE'},
 {'symbol': 'AUDIO'},
 {'symbol': 'CELO'},
 {'symbol': 'JASMY'},
 {'symbol': 'HIGH'},
 {'symbol': 'CVX'},
 {'symbol': 'RSR'},
 {'symbol': 'GAL'},
 {'symbol': 'KAVA'},
 {'symbol': 'KNC'},
 {'symbol': 'ANKR'},
 {'symbol': 'BAT'},
 {'symbol': 'CHR'},
 {'symbol': 'IOTA'},
 {'symbol': 'SFP'},
 {'symbol': 'CELR'},
 {'symbol': 'UNFI'},
 {'symbol': 'C98'},
 {'symbol': 'MTL'},
 {'symbol': 'QTUM'},
 {'symbol': 'RVN'},
 {'symbol': 'REEF'},
 {'symbol': 'WOO'},
 {'symbol': 'RLC'},
 {'symbol': 'COTI'},
 {'symbol': 'ZRX'},
 {'symbol': 'ALICE'},
 {'symbol': 'ALPHA'},
 {'symbol': 'OMG'},
 {'symbol': 'BTCDOM'},
 {'symbol': 'BAKE'},
 {'symbol': 'LPT'},
 {'symbol': 'FLM'},
 {'symbol': 'BLZ'},
 {'symbol': 'OGN'},
 {'symbol': 'HOT'},
 {'symbol': 'GTC'},
 {'symbol': 'ONT'},
 {'symbol': 'BAL'},
 {'symbol': 'ATA'},
 {'symbol': 'IOST'},
 {'symbol': 'ASTR'},
 {'symbol': 'IOTX'},
 {'symbol': 'HNT'},
 {'symbol': 'LINA'},
 {'symbol': 'CTK'},
 {'symbol': 'ANT'},
 {'symbol': 'CTSI'},
 {'symbol': 'SPELL'},
 {'symbol': 'ICX'},
 {'symbol': 'DAR'},
 {'symbol': 'QNT'},
 {'symbol': 'STMX'},
 {'symbol': 'XEM'},
 {'symbol': 'API3'},
 {'symbol': 'DENT'},
 {'symbol': 'DGB'},
 {'symbol': 'NKN'},
 {'symbol': 'BEL'},
 {'symbol': 'ARPA'},
 {'symbol': 'TOMO'},
 {'symbol': 'FOOTBALL'},
 {'symbol': '1000XEC'},
 {'symbol': 'T'},
 {'symbol': 'DEFI'}]


def get_data(period_minutes, coin_name):
    url = "https://www.binance.com/bapi/futures/v1/public/future/data/long-short-account-ratio"

    payload = json.dumps({
      "name": coin_name,
      "periodMinutes": period_minutes
    })
    headers = {
    'authority': 'www.binance.com',
    'accept': '*/*',
    'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'bnc-uuid': '0f9f1d98-ceb6-46ba-8363-f27e1a94b3c9',
    'clienttype': 'web',
    'content-type': 'application/json',
    'cookie': 'cid=FOkTE3kc; _gid=GA1.2.942196494.1683285277; bnc-uuid=0f9f1d98-ceb6-46ba-8363-f27e1a94b3c9; source=organic; campaign=www.google.com; theme=dark; userPreferredCurrency=USD_USD; sajssdk_2015_cross_new_user=1; BNC_FV_KEY=331c9cf43301ac27bd74de48d43ac2bdb446b23c; BNC_FV_KEY_EXPIRE=1683306878257; OptanonAlertBoxClosed=2023-05-05T11:14:52.332Z; lang=en; _ga=GA1.2.1147159997.1683285277; _ga_3WP50LGEEC=GS1.1.1683285278.1.1.1683285372.59.0.0; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22187eb9efe042416-08f1ac243d8637-1d525634-1296000-187eb9efe0525df%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg3ZWI5ZWZlMDQyNDE2LTA4ZjFhYzI0M2Q4NjM3LTFkNTI1NjM0LTEyOTYwMDAtMTg3ZWI5ZWZlMDUyNWRmIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22187eb9efe042416-08f1ac243d8637-1d525634-1296000-187eb9efe0525df%22%7D; OptanonConsent=isGpcEnabled=0&datestamp=Fri+May+05+2023+18%3A16%3A12+GMT%2B0700+(Gi%E1%BB%9D+%C4%90%C3%B4ng+D%C6%B0%C6%A1ng)&version=202211.1.0&isIABGlobal=false&hosts=&consentId=91180826-a037-445d-9b2a-7f830dbc41d6&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0002%3A1&geolocation=VN%3BHN&AwaitingReconsent=false',
    'csrftoken': 'd41d8cd98f00b204e9800998ecf8427e',
    'device-info': 'eyJzY3JlZW5fcmVzb2x1dGlvbiI6IjkwMCwxNDQwIiwiYXZhaWxhYmxlX3NjcmVlbl9yZXNvbHV0aW9uIjoiODI3LDE0NDAiLCJzeXN0ZW1fdmVyc2lvbiI6Ik1hYyBPUyAxMC4xNS43IiwiYnJhbmRfbW9kZWwiOiJ1bmtub3duIiwic3lzdGVtX2xhbmciOiJ2aS1WTiIsInRpbWV6b25lIjoiR01UKzciLCJ0aW1lem9uZU9mZnNldCI6LTQyMCwidXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMTIuMC4wLjAgU2FmYXJpLzUzNy4zNiIsImxpc3RfcGx1Z2luIjoiUERGIFZpZXdlcixDaHJvbWUgUERGIFZpZXdlcixDaHJvbWl1bSBQREYgVmlld2VyLE1pY3Jvc29mdCBFZGdlIFBERiBWaWV3ZXIsV2ViS2l0IGJ1aWx0LWluIFBERiIsImNhbnZhc19jb2RlIjoiYmU5ZDFlOTYiLCJ3ZWJnbF92ZW5kb3IiOiJHb29nbGUgSW5jLiAoQXBwbGUpIiwid2ViZ2xfcmVuZGVyZXIiOiJBTkdMRSAoQXBwbGUsIEFwcGxlIE0xLCBPcGVuR0wgNC4xKSIsImF1ZGlvIjoiMTI0LjA0MzQ0OTY4NDc1MTk4IiwicGxhdGZvcm0iOiJNYWNJbnRlbCIsIndlYl90aW1lem9uZSI6IkFzaWEvU2FpZ29uIiwiZGV2aWNlX25hbWUiOiJDaHJvbWUgVjExMi4wLjAuMCAoTWFjIE9TKSIsImZpbmdlcnByaW50IjoiYTE0MjkyZjAyMjRmNDNiZWFhZjA0NGJjYjFhNTRhZWQiLCJkZXZpY2VfaWQiOiIiLCJyZWxhdGVkX2RldmljZV9pZHMiOiIifQ==',
    'fvideo-id': '331c9cf43301ac27bd74de48d43ac2bdb446b23c',
    'lang': 'en',
    'origin': 'https://www.binance.com',
    'referer': 'https://www.binance.com/en/futures/funding-history/perpetual/4',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'x-passthrough-token': '',
    'x-trace-id': '87af25ec-1c43-4854-9380-5c20337f6a73',
    'x-ui-request-trace': '87af25ec-1c43-4854-9380-5c20337f6a73'}

    response = requests.request("POST", url, headers=headers, data=payload)

    data = response.json()["data"]

    df = pd.DataFrame({
        "Timestamp": data["xAxis"],
        "Long/Short Ratio": data["series"][0]["data"],
        "Long Account": data["series"][1]["data"],
        "Short Account": data["series"][2]["data"]
    })

    timezone = pytz.timezone("Asia/Ho_Chi_Minh")
    df["Time (Vietnam)"] = pd.to_datetime(df["Timestamp"], unit='ms').dt.tz_localize(pytz.UTC).dt.tz_convert(timezone)

    # Sắp xếp lại DataFrame theo thứ tự giảm dần của Timestamp
    df = df.sort_values(by="Timestamp", ascending=False)

    # Reset index sau khi sắp xếp lại
    df = df.reset_index(drop=True)

     # Kiểm tra giá trị đầu tiên của Long/Short Ratio
    first_ratio = df.loc[0, 'Long/Short Ratio']
    first_long_account = df.loc[0, 'Long Account']
    first_short_account = df.loc[0, 'Short Account']

    chg_percent = (df.loc[0, 'Long/Short Ratio'] - df.loc[1, 'Long/Short Ratio']) / df.loc[1, 'Long/Short Ratio']

    data = [coin_name, first_ratio, f"{round(chg_percent*100, 2)}%", f"{first_long_account}", f"{first_short_account}"]

    return data


trading_pairs = []

def get_trading_pairs(api_key, api_secret):
    global trading_pairs
    client = Client(api_key, api_secret)
    futures_exchange_info = client.futures_exchange_info()
    trading_pairs = [{'symbol': info['symbol']} for info in futures_exchange_info['symbols']]
        

async def send_notification(notification_message):
    telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN_hungdv_bot)
    await telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID_Bot_Order_HungAI, text=notification_message, parse_mode="markdown")
    
    
    
async def main():
    period_minutes_list = [60]
    table = []
    tasks = []
    for coin in trading_pairs[:]:
        try:
            coin_name = coin['symbol']
            for period_minutes in period_minutes_list:
                data = get_data(period_minutes=period_minutes, coin_name=f"{coin_name}")
                first_ratio = data[1]
                chg_percent = data[2]
                if (first_ratio > 4 or first_ratio < 0.7) and (True): # Điều kiện tùy chỉnh của bạn
                    table.append(data)
        except:
            print(coin)
            
    headers = ["Ticker", "Ratio", "Chg %", "Long", "Short"]
    sorted_table = sorted(table, key=lambda x: x[1])
    TABLE = tabulate(sorted_table, headers, tablefmt="pipe")
    timezone = pytz.timezone("Asia/Ho_Chi_Minh")
    current_time = datetime.now(tz=timezone)
    notification_message = f"📌Thời điểm: {current_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    notification_message += TABLE
    
    await send_notification(notification_message)

def run_main():
    asyncio.run(main())
    
# Lên lịch cập nhật danh sách trading_pairs mỗi lần chạy main
def update_trading_pairs():
    global trading_pairs
    trading_pairs = get_trading_pairs(api_key=YOUR_API_KEY, api_secret=YOUR_API_SECRET)
    
    
# Hàm main sẽ gọi trước hàm update_trading_pairs để cập nhật danh sách trading_pairs, sau đó chạy main
async def main_with_update():
    update_trading_pairs()
    await main()
    
run_main()

# Lên lịch chạy hàm main_with_update mỗi 1 giờ
schedule.every(60).minutes.do(run_main)

while True:
    schedule.run_pending()
    time.sleep(1)