import requests
import time
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# API 請求相關設定
URL = "https://maplestory.beanfun.com/main?handler=BulletinProxy"
HEADERS = {
    "accept": "*/*",
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://maplestory.beanfun.com",
    "priority": "u=1, i",
    "referer": "https://maplestory.beanfun.com/main?section=mBulletin",
    "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "x-csrf-token": "CfDJ8N5WPr6Y241KvDQ5Q5Dp0OJJ0eWn4UgwOnEpX5VH5-dFu_vSWAC4LuEVyMqLo3eSMGPsPIG2TPWbgVpioTh4NW_65zHuwPUX_ap00CJCwyBt-6J5PweDBRJ-y9-lEs7jXsRXVozacHdmnUTiAeAGLNg",
    "x-requested-with": "XMLHttpRequest"
}
COOKIES = {
    "_tracingid_v1.4.0": "7fc657e32f5458a2433cb34969e22034",
    "web_tracing_id": "7fc657e32f5458a2433cb34969e22034",
    "__utmz": "192187193.1723082872.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
    "__BWtransf": "c1723434083403x628e759e8",
    "__BWfp": "c1723434083403x628e759e8",
    "_ga_FMPR5TD4S3": "GS1.1.1723530186.3.1.1723530192.54.0.0",
    "__BW_798-1210W44Y0RCD8AR": "1723530187.1723530191.1723530192",
    "_hjSessionUser_1878324": "eyJpZCI6IjgzZjQ3NjRkLTBlMTItNTdlNS1hOTZkLWVhZjM4NjBjY2FkNSIsImNyZWF0ZWQiOjE3MjM2MTI5NjY1NjUsImV4aXN0aW5nIjp0cnVlfQ==",
    "__utma": "192187193.1080461785.1723016741.1727228918.1727401574.25",
    "bfEnv": "TW;Production",
    "bfWebToken": "1e57333f489346f69fb56e4393d0f68e",
    "bfUID": "C875A470308C95966107CE026877C89D66C18B85D8CF2F03B26FF72C938F028677FD81D471908383",
    ".AspNetCore.Antiforgery.SVSW8BVrGmw": "CfDJ8N5WPr6Y241KvDQ5Q5Dp0OI5wQUq5vCcEZHy4MIE5QDtAQZU1kPrJeVvD4P26QFP_Fj1nTOYMObinxeBDgiAL34wJ_Vu-DLepFbm_gJc1IsOMYFGT69N-FaCHc61fUNLs3ibEd7CiUR5dpYvAWJswyA",
    "bfTD": "547498D764FB9D6930FCAA80D5709F75F08B166FB3E0DF46F149A4683FEA37CBC08F9977F63BFE46BB38D4DF70807315881363D60DB911BF39C25F28736E8BC4DAC7BC146E056A667F4342AC63853902B37622D5F8171ED201A0FFA9FFB1A7D345FCB8A048373C47E0C8E4976B87D87540A558E7F23E95207DA1F00483B823DE6F70ED43769A9516C8CE0C48D498D6E3DED6599D76D5787FBAC4B92D83E3E9D9D"
}
DATA = "Kind=0&Page=1&method=0&PageSize=10"

# 從環境變數獲取 SMTP 設定
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_APP_PASSWORD = os.getenv("SMTP_APP_PASSWORD")

# 獲取當天日期 (格式: YYYY/MM/DD)
def get_today_date():
    return datetime.now().strftime("%Y/%m/%d")

# 發送 Email
def send_email(title):
    msg = MIMEText(f"檢測到符合條件的公告: {title}", "plain", "utf-8")
    msg["Subject"] = "MapleStory 開機公告通知"
    msg["From"] = SMTP_USERNAME
    msg["To"] = SMTP_USERNAME

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_APP_PASSWORD)
            server.send_message(msg)
            print(f"郵件發送成功: {title}")
            return True
    except Exception as e:
        print(f"郵件發送失敗: {e}")
        return False

# 主程式
def main():
    while True:
        today = get_today_date()
        try:
            response = requests.post(URL, headers=HEADERS, cookies=COOKIES, data=DATA)
            response.raise_for_status()  # 檢查是否有 HTTP 錯誤
            json_data = response.json()
            
            # 獲取所有公告列表
            announcements = json_data.get("data", {}).get("myDataSet", {}).get("table", [])
            
            # 遍歷當天的公告
            found_opening = False
            for announcement in announcements:
                if announcement["startDate"] == today:  # 只檢查今天發表的公告
                    print(f"檢查今天公告: {announcement['title']}")
                    # 檢查是否為「開機公告」且不包含「延後」
                    if "開機公告" in announcement["title"] and "延後" not in announcement["title"]:
                        print(f"找到符合條件的公告: {announcement['title']}")
                        if send_email(announcement["title"]):
                            found_opening = True
                            break  # 找到後跳出內層迴圈
                    elif "開機公告" in announcement["title"] and "延後" in announcement["title"]:
                        print(f"檢測到延後開機公告，已忽略: {announcement['title']}")
            
            # 如果找到開機公告並成功發送郵件，停止程式
            if found_opening:
                print("程式即將停止...")
                break
            else:
                print("目前沒有符合條件的開機公告")
        
        except requests.RequestException as e:
            print(f"請求失敗: {e}")
        except (IndexError, KeyError) as e:
            print(f"解析回應失敗: {e}")
        except Exception as e:
            print(f"未知錯誤: {e}")

        # 每 30 秒執行一次
        time.sleep(30)

if __name__ == "__main__":
    if not SMTP_USERNAME or not SMTP_APP_PASSWORD:
        print("錯誤: 請設定環境變數 SMTP_USERNAME 和 SMTP_APP_PASSWORD")
    else:
        print("開始監控 MapleStory 公告...")
        main()
