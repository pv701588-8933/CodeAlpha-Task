import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
CATALOGUE_URL = "https://books.toscrape.com/catalogue/"

books = []

def get_soup(url):
    """Fetch HTML with correct headers."""
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    return BeautifulSoup(r.text, "html.parser")


def make_full_url(link):
    """Convert relative link to full URL."""
    if link.startswith("http"):
        return link

    # Remove ../../ or ../../../ or ../
    cleaned = link.replace("../../../", "").replace("../../", "").replace("../", "")

    return CATALOGUE_URL + cleaned


def scrape_book_details(book_url):
    """Scrape book details from inside page."""
    soup = get_soup(book_url)

    try:
        description = soup.select_one("#product_description + p").text.strip()
    except:
        description = "No description"

    try:
        upc = soup.select_one("table tr:nth-of-type(1) td").text
    except:
        upc = "N/A"

    return {
        "description": description,
        "upc": upc
    }


def scrape_books():
    """Scrape all books from page 1."""
    global books
    books = []

    print("Scraping started...\n")

    soup = get_soup(BASE_URL)
    product_list = soup.select(".product_pod")

    for item in product_list:
        title = item.h3.a["title"]
        price = item.select_one(".price_color").text.strip()
        rating = item.p["class"][1]

        img = item.find("img")["src"].replace("../..", "")
        img_url = BASE_URL + img

        # Fixing the book link
        link = make_full_url(item.h3.a["href"])

        # Get details
        details = scrape_book_details(link)

        books.append({
            "title": title,
            "price": price,
            "rating": rating,
            "image_url": img_url,
            "url": link,
            "description": details["description"],
            "upc": details["upc"]
        })

    print(f"Scraping complete ✔  Total books scraped: {len(books)}\n")


def filter_by_price(max_price):
    print(f"\nBooks cheaper than £{max_price}:")
    found = False

    for b in books:
        price_value = float(b["price"].replace("£", ""))
        if price_value <= max_price:
            print(f"- {b['title']} (£{price_value})")
            found = True

    if not found:
        print("No books found in this price range.")


def filter_by_rating(star):
    print(f"\nBooks with {star}-star rating:")
    found = False

    for b in books:
        if b["rating"].lower() == star.lower():
            print(f"- {b['title']} ({b['rating']})")
            found = True

    if not found:
        print("No books found with this rating.")


def search_by_title(keyword):
    print(f"\nBooks containing '{keyword}':")
    found = False

    for b in books:
        if keyword.lower() in b["title"].lower():
            print(f"- {b['title']}")
            found = True

    if not found:
        print("No matching books found.")


def menu():
    """Interactive filtering menu."""
    while True:
        print("\n-------------------------")
        print("   Choose a filter option")
        print("-------------------------")
        print("1. Filter by price")
        print("2. Filter by rating")
        print("3. Search by title")
        print("4. Exit")

        choice = input("Enter your choice (1–4): ")

        if choice == "1":
            price = float(input("Enter max price (example: 20): "))
            filter_by_price(price)

        elif choice == "2":
            print("Available ratings: One, Two, Three, Four, Five")
            star = input("Enter rating: ")
            filter_by_rating(star)

        elif choice == "3":
            kw = input("Enter keyword to search: ")
            search_by_title(kw)

        elif choice == "4":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    scrape_books()
    menu()
