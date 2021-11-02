import datetime
import json
from functools import reduce

__days = [
    "Måndag",
    "Tisdag",
    "Onsdag",
    "Torsdag",
    "Fredag"
]

__weekly_headers = [
    "Alltid på Platz",
    "Veckans Schnitzel",
    "Veckans vegetariska"
]
def name():
    return "Schnitzelplatz"
    
def food(api, date):
    def collapse_paragraphs(ps):
        return dict(map(
            lambda kv: (
                kv[0], 
                reduce(
                    lambda acc, s: acc + " " +  s, 
                    kv[1], 
                    ""
                ).replace("\n", " ")
            ), 
            ps.items()))

    def categorize(menu_soup):
        menu = {}
        current_index = None
        for item in menu_soup:
            if item.name == "h4":
                current_index = item.get_text()
            elif item.name == "p": 
                if not current_index in menu:
                    menu[current_index] = []
                menu[current_index].append(item.get_text())
        return menu



    if (not api.is_current_week(date) 
            or not api.is_weekday(date) 
            or not api.soup):
        return []

    response = api.requests.get('https://schnitzelplatz.se/lunch/')
    soup = api.soup(response.content, 'html.parser')

    food_menu = soup.find_all("div", {"class", "foodmenu section-padding--medium"})[0].find_all()
    parsed_menu = collapse_paragraphs(categorize(food_menu))

    # Assert that all expected headings exists in the parsed menu
    assert all(heading in parsed_menu 
        for heading in __days + __weekly_headers)

    return [
        api.food("Alltid på Platz: ", parsed_menu["Alltid på Platz"]),
        api.food("Veckans Schnitzel: ", parsed_menu["Veckans Schnitzel"]),
        api.food("Veckans Vegetariska: ", parsed_menu["Veckans vegetariska"]),
        api.food("Dagens: ", parsed_menu[__days[date.weekday()]])
    ]
