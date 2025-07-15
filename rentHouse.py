import os
from selenium import webdriver
from bs4 import BeautifulSoup
import time
url = 'https://www.zumper.com/apartments-for-rent/vancouver-bc/university-endowment-lands'
def scrape_rent_listings(link, max_price, bed_count, wait_time):

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get(link)
    time.sleep(wait_time)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.quit()

    listings = []
    items = soup.find_all('div', class_='css-1c1kacq')

    for item in items:
        beds_tag = item.find('p', class_='ListingCardContentSection_bedsRangeText__BF7nu ListingCardContentSection_bedsRangeTextLargeCard__98N9Z')
        price_tag = item.find('p', class_='ListingCardContentSection_longTermPrice__TkxdS ListingCardContentSection_longTermPriceLargeCard__jcX43')
        title_tag = item.find('div', class_='ListingCardContentSection_detailLinkText__kjqHB')

        if beds_tag and price_tag and title_tag:
            try:
                beds_text = beds_tag.text.lower().strip()
                if f"{bed_count} bed" in beds_text:
                    price_number = int(price_tag.text.strip().replace('$', '').replace(',', ''))
                    if price_number <= max_price:
                        listings.append({
                            'title': title_tag.text.strip(),
                            'beds': beds_text,
                            'price': price_number
                        })
            except ValueError:
                continue

    return listings


print(scrape_rent_listings(url,4000, 2,20))