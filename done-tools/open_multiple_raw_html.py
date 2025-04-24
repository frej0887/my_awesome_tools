import webbrowser
from random import shuffle

PRODUCTION_TYPES = ["production", "prod", "1"]
LOCAL_TYPES = ["development", "local", "localhost", "dev", "2"]
PLAYWRIGHT_TYPES = ["playwright", "1337", "leet", "3"]

url_prod = lambda keyword_id: f"https://app.accuranker.com/keywords/ranks/{keyword_id}/raw_html/"
url_local = lambda keyword_id: f"http://localhost.dk:8000/keywords/ranks/{keyword_id}/raw_html/"
url_playwright = lambda keyword, device: f"http://localhost:1337/google/scrape?keyword={keyword}&device={device}"

description = f"""
Tool for opening multiple scrapes.
Can be used for production ranks, local ranks or pages in playwright.
Put the rank ids in input.txt, one per line (just copy directly from DataGrip).

Opening types possibilities:
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

opening_types = {x: url_prod for x in PRODUCTION_TYPES} | {x: url_local for x in LOCAL_TYPES} | {x: url_playwright for x in PLAYWRIGHT_TYPES}


while True:
    print(description)
    open_type = input("Opening type: ").strip()
    if not open_type or not open_type in opening_types.keys():
        print("Invalid opening type, try again")
        print(break_text)
        continue

    open_amount = input("Amount of scrapes to open: ").strip()
    try:
        open_amount = int(open_amount)
        assert open_amount > 0
    except ValueError:
        print("Invalid amount, try again")
        print(break_text)
        continue
    if open_amount > 100:
        print(f"You are opening {open_amount} scrapes, are you sure? (y/n)")
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

    if open_type in PLAYWRIGHT_TYPES:
        print(PLAYWRIGHT_TEXT)
        device = input("Device: ").strip()
        if not device:
            print("Invalid device, try again")
            print(break_text)
            continue
        with open("input.txt", "r") as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
            if len(lines) < open_amount:
                print(f"There are not that many ids to open. All the {len(lines)} given ids will be opened")
            shuffle(lines)
            for rank_id in lines[:open_amount]:
                if open_type in PLAYWRIGHT_TYPES:
                    if device == '0':
                        webbrowser.open_new_tab(opening_types[open_type](rank_id, 1))
                        webbrowser.open_new_tab(opening_types[open_type](rank_id, 2))
                    else:
                        webbrowser.open_new_tab(opening_types[open_type](rank_id, device))
        print(break_text)
        continue

    with open("input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
        if len(lines) < open_amount:
            print(f"There are not that many ids to open. All the {len(lines)} given ids will be opened")
        shuffle(lines)
        for rank_id in lines[:open_amount]:
            webbrowser.open_new_tab(opening_types[open_type](rank_id))
    print(break_text)
