from requests_html import HTML, HTMLSession

session = HTMLSession()


def get_trends():
    trends = []

    html = session.get("https://twitter.com/i/trends").json()["module_html"]
    html = HTML(
        html=html, url="bunk", default_encoding="utf-8"
    )

    for trend_item in html.find('li'):
        trend_text = trend_item.attrs['data-trend-name']

        trends.append(trend_text)
    
    return trends


if __name__ == "__main__":
    print(get_trends())

