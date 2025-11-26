import requests
from bs4 import BeautifulSoup
import urllib.parse

BASE = "https://lalafo.kg"
SITEMAP = "https://lalafo.kg/sitemap"

def get_all_sitemap_links():
    r = requests.get(SITEMAP)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # фильтруем только категории Kyrgyzstan
        if href.startswith("/kyrgyzstan/"):
            full = urllib.parse.urljoin(BASE, href)
            links.add(full)
    return sorted(links)

def get_all_leaf_links():
    all = get_all_sitemap_links()
    leafs = filter_leaves(all)
    return leafs

def filter_leaves(urls):
    """
    Оставляем только листовые ссылки:
    убираем url, если есть другой url, начинающийся с этого + "/"
    """
    leaves = []
    for u in urls:
        # считаем, что u — родитель, если есть другой v != u, который начинается с u + '/'
        is_parent = False
        prefix = u.rstrip("/") + "/"
        for v in urls:
            if v != u and v.startswith(prefix):
                is_parent = True
                break
        if not is_parent:
            leaves.append(u)
    return leaves

if __name__ == "__main__":
    all_links = get_all_sitemap_links()
    leaf_links = filter_leaves(all_links)

    for link in leaf_links:
        print(link)
        

