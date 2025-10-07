import trafilatura

def extract(url: str) -> dict:
    try:
        downloaded = trafilatura.fetch_url(url, no_ssl=True)
        if not downloaded:
            return {"text": "", "ok": False}
        res = trafilatura.extract(downloaded, include_comments=False, include_formatting=False)
        if not res:
            return {"text": "", "ok": False}
        return {"text": res.strip(), "ok": True}
    except Exception:
        return {"text": "", "ok": False}
