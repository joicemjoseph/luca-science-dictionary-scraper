import requests
from bs4 import BeautifulSoup
import json
class ReqXcptn(BaseException):
    pass

def fetch_body(url):
    try:
        resp = requests.get(url)
    except requests.ConnectionError as e:
        raise requests.RequestException(str(e))
    
    if resp.status_code != 200:
        raise requests.RequestException("Pani pali")

    return resp.content

def get_words(body):
    soup = BeautifulSoup(body, "html.parser")
    row = soup.find_all("tr")
    words = []
    for entry in row:
        out = {}
        e = entry.find_all("td")
        try:
            out["english"] = {"word": e[0].find("a").string, "link": e[0].find("a").get("href")}
        except Exception as w:
            print(str(w))
            print(str(entry))
            continue
        try:
            out["malayalam"] = {"word": e[1].find("a").string, "link": e[1].find("a").get("href")}
        except Exception as w:
            print(str(w))
            print(str(entry))
            continue
        try:
            out["meaning"] = e[2].string
        except Exception as w:
            print(str(w))
            print(str(entry))
            continue
        words.append(out)

    return words

# def parse_request(body):
#     soup = BeautifulSoup(body, "html.parser")
#     posts = soup.find_all(class_="post-thumbnail")

# Luca have 10 pages of content.
base_url = "https://luca.co.in/science-words/?cpage={0}"

out = list()
for i in range(1,302):
    url = base_url.format(i)
    print(url)

    try:
        body = fetch_body(url)
    except requests.RequestException as e:
        print(str(e))

    out += get_words(body)


with open("out.json", "w+", encoding='utf-8') as f:
    json.dump(out, f, indent = 4, sort_keys=True, ensure_ascii=False)
