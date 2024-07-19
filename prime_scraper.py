"""
In the task details for this assessment, I am required to navigate to the Amazon Daily Deals 
page at https://www.amazon.com/deals. The instructions mention that the top of this page should feature 
a section titled "Member-Only Prime Deals." However, when I visit the provided link, I only see "Today's 
Deals" at the top of the page, with a side scroll bar. It is possible that Amazon has updated the layout 
of this page.

After researching other pages, I discovered a page that closely aligns with the assessment's instructions: 
https://www.amazon.com/b?ie=UTF8&node=16205654011. This page displays featured deals at the top, 
accompanied by a side-scrolling section. 
"""

from playwright.sync_api import sync_playwright

def prime_scraper():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://www.amazon.com/b?ie=UTF8&node=16205654011')
        
        items = []
        products = page.query_selector_all('.a-carousel-card')

        for product in products:
            link_element = product.query_selector('.a-link-normal')
            name_element = product.query_selector('.a-truncate-full')
            list_price_element = product.query_selector('.a-price.a-text-price .a-offscreen')
            discounted_price_element = product.query_selector('.a-price.dcl-product-price-new .a-offscreen')

            if not (discounted_price_element): # Check is discount exists for product. Skip iteration if discounted price does not exist. 
                continue

            link = link_element.get_attribute('href')
            name = name_element.inner_text() 
            list_price = list_price_element.inner_text() 
            discounted_price = discounted_price_element.inner_text() 

            items.append({
                'discounted-price': discounted_price,
                'list-price': list_price,
                'product-link': f"https://www.amazon.com{link}",
                'product-name': name
            })

        browser.close()
        return items

if __name__ == '__main__':
    items = prime_scraper()
    for item in items:
        print(item)
