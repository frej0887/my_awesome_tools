import webbrowser
from random import shuffle

PRODUCTION_TYPES = ["production", "prod", "1"]
LOCAL_TYPES = ["development", "local", "localhost", "dev", "2"]
PLAYWRIGHT_TYPES = ["playwright", "1337", "leet", "3"]

url_prod = lambda keyword_id: f"https://app.accuranker.com/keywords/ranks/{keyword_id}/raw_html/"
url_local = lambda keyword_id: f"http://localhost.dk:8000/keywords/ranks/{keyword_id}/raw_html/"
url_playwright = lambda keyword, dev: f"http://localhost:1337/google/scrape_serp?keyword={keyword}&device={dev}"

description = f"""
Tool for opening multiple scrapes.
Can be used for production ranks, local ranks or pages in playwright.

Opening type possibilities:
{PRODUCTION_TYPES[0].title()}: {", ".join(PRODUCTION_TYPES)}
{LOCAL_TYPES[0].title()}: {", ".join(LOCAL_TYPES)}
{PLAYWRIGHT_TYPES[0].title()}: {", ".join(PLAYWRIGHT_TYPES)}

"""

PLAYWRIGHT_TEXT = """
Device types for playwright:
Desktop: 1
Mobile: 2
Both: 0 (doubles the amount of opens)
"""

break_text = """------------------------------------------------\n\n\n\n"""

url_template_dict = {x: url_prod for x in PRODUCTION_TYPES} | {x: url_local for x in LOCAL_TYPES} | {x: url_playwright for x in PLAYWRIGHT_TYPES}


if __name__ == "__main__":
    device = '0'
    amount_used = 0
    print(description)
    open_type = input("Opening type: ").strip()

    if not open_type or not open_type in url_template_dict.keys():
        print("Invalid opening type, try again")
        print(break_text)
        exit(1)

    if open_type in PLAYWRIGHT_TYPES:
        print(PLAYWRIGHT_TEXT)
        while True:
            device = input("Device: ").strip()
            if device:
                break
            else:
                print("Invalid device, try again")
                print(break_text)

    print("Input the ids you want to sample from")
    keywords = []
    while True:
        inp = input()
        if inp == "":
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            break
        keywords.append(inp.strip())

    shuffle(keywords)
    while True:

        amount_asked_to_open = input("Amount of scrapes to open: ").strip()
        try:
            amount_asked_to_open = int(amount_asked_to_open)
            assert amount_asked_to_open > 0
        except ValueError:
            print("Invalid amount, try again")
            print(break_text)
            continue
        if amount_asked_to_open > 100:
            print(f"You are opening {amount_asked_to_open} scrapes, are you sure? (y/n)")
            confirm = input().strip()
            if confirm.lower() == 'y':
                pass
            elif confirm.lower() == 'n':
                print("Try again")
                print(break_text)
                continue
            else:
                print("Invalid input, try again")
                print(break_text)
                continue

        if len(keywords) < amount_used + amount_asked_to_open:
            print(f"There are not that many ids to open. The last unused will be opened")

        print("Opening the ids...\n")
        for rank_id in keywords[amount_used:min(len(keywords), amount_used + amount_asked_to_open)]:
            if open_type in PLAYWRIGHT_TYPES:
                if device == '0':
                    webbrowser.open_new_tab(url_template_dict[open_type](rank_id, 1))
                    webbrowser.open_new_tab(url_template_dict[open_type](rank_id, 2))
                else:
                    webbrowser.open_new_tab(url_template_dict[open_type](rank_id, device))
            else:
                webbrowser.open_new_tab(url_template_dict[open_type](rank_id))
        amount_used += amount_asked_to_open
