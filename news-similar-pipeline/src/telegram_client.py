import os, requests

BOT = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

def send_message(text: str, disable_preview: bool = False):
    if not BOT or not CHAT_ID:
        print("[telegram] missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID; printing instead:\n", text)
        return {"ok": False}
    url = f"https://api.telegram.org/bot{BOT}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": disable_preview,
    }
    try:
        r = requests.post(url, json=payload, timeout=30)
        return r.json()
    except Exception as e:
        print("[telegram] error:", e)
        return {"ok": False}
