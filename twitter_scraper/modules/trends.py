from requests_html import HTML, HTMLSession

session = HTMLSession()


def get_trends():
    trends = []

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
        "X-Twitter-Active-User": "yes",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "en-US",
    }

    html = session.get("https://twitter.com/i/trends", headers=headers)
    html = html.json()["module_html"]

    html = HTML(html=html, url="bunk", default_encoding="utf-8")

    for trend_item in html.find("li"):
        trend_text = trend_item.attrs["data-trend-name"]

        trends.append(trend_text)

    return trends
