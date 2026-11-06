from datetime import datetime, timezone
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

POLICY_URL = "https://4-learn.github.io/ai-event-demo/"


def fetch_regulations(url=POLICY_URL):
    request = Request(url, headers={"User-Agent": "ai-event-demo/1.0"})
    with urlopen(request, timeout=20) as response:
        html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("h1").get_text(strip=True)
    version = soup.find("meta", attrs={"name": "document-version"})["content"]
    fetched_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    regulations = []

    for article in soup.select("article.rule"):
        regulations.append({
            "id": article["id"],
            "title": title,
            "version": version,
            "section": article.find("h2").get_text(strip=True),
            "text": "\n".join(p.get_text(" ", strip=True) for p in article.find_all("p")),
            "source": f"{url.split('#')[0]}#{article['id']}",
            "fetched_at": fetched_at,
        })

    if not regulations:
        raise ValueError("找不到規範條文，請檢查網頁結構")
    return regulations
