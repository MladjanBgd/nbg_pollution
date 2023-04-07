from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

url = "http://www.amskv.sepa.gov.rs/mob/pregledpodataka.php?stanica=9"

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

driver.get(url)
html = driver.page_source

with open("D:/Mladjan/!k/pollution/dump.html", "w", encoding="utf-8") as f:
    f.write(html)
    f.close()


from bs4 import BeautifulSoup
from lxml import etree


soup = BeautifulSoup(html, "html.parser")
table = soup.find("table", {"id": "pregledtabela"})
trs = table.find_all("tr")

# print("dd.mm. h")
# print("SO2[ug.m-3]PM10[ug.m-3]O3[ug.m-3]NO2[ug.m-3]CO[mg.m-3]PM2.5[ug.m-3]")

import pandas as pd

df = pd.DataFrame(
    columns=[
        "timestamp[dd.mm. h]",
        "SO2[ug.m-3]",
        "PM10[ug.m-3]",
        "O3[ug.m-3]",
        "NO2[ug.m-3]",
        "CO[mg.m-3]",
        "PM2.5[ug.m-3]",
    ]
)

list = []

for tr in trs:
    tds = tr.find_all("td")
    for td in tds:
        # print(td.text)
        val = td.text.strip("'")
        list.append(val)
    print(list)
    if len(list) > 0:
        df.loc[len(df)] = list
    list = []


print(df)
df.to_csv("D:/Mladjan/!k/pollution/dump.csv")
