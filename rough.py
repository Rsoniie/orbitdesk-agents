import requests
from bs4 import BeautifulSoup

def print_secret_message(url):
  response = requests.get(url)
  response.raise_for_status()

  soup = BeautifulSoup(response.text, "html.parser")
  rows = soup.find_all("tr")

  points = {}
  max_x = max_y = 0

  for row in rows[1:]:
    cells = row.find_all(["td", "th"])

    if len(cells) < 3:
      continue

    try:
      x = int(cells[0].get_text(strip=True))
      char = cells[1].get_text(strip=True)
      y = int(cells[2].get_text(strip=True))

    except ValueError:
      continue

    points[(x, y)] = char
    max_x = max(max_x, x)
    max_y = max(max_y, y)

  for y in range(max_y, -1, -1):
    line=""
    for x in range(max_x+1):
      line+=points.get((x, y), " ")
    print(line)
    


url = "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"
print_secret_message(url)