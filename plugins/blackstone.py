__days = [
    u"Måndag",
    u"Tisdag",
    u"Onsdag",
    u"Torsdag",
    u"Fredag",
    u"Hjärtligt välkomna! – Vännerna på Blackstone Steakhouse"
]

def food(api, date):
    if not api.is_current_week(date):
        return []
    if not api.is_weekday(date):
        return []
    if not api.soup:
        return []

    response = api.requests.get('https://www.blackstonesteakhouse.se/goteborg/')
    soup = api.soup(response.content, 'html.parser')
    text = soup.get_text().splitlines()

    current_week = date.isocalendar()[1]
    week_text = f"Vår Lunchmeny V. {current_week}"
    if not week_text in text:
        return []

    today = __days[date.isoweekday() - 1]
    today_line = text.index(today)

    end_text = __days[date.isoweekday()]
    end_line = text.index(end_text)

    todays_menu = text[today_line+1 : end_line]
    dishes = list(filter(lambda ln: ln and ln[0].isupper(), todays_menu))

    def describe_dish(dishes):
        (dish, next_dish) = dishes
        dish_line = todays_menu.index(dish)
        next_dish_line = todays_menu.index(next_dish)
        return api.food(dish, ' '.join(todays_menu[dish_line+1 : next_dish_line]))

    return list(map(describe_dish, zip(dishes, dishes[1:] + [''])))

def name():
    return "Blackstone"
