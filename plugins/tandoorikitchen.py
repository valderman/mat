__days = [
    u"Måndag:",
    u"Tisdag:",
    u"Onsdag:",
    u"Torsdag:",
    u"Fredag:",
    u"Hjärtligt välkomna! – Vännerna på Blackstone Steakhouse"
]

def food(api, date):
    response = api.requests.get('https://eattandoori.se/lunch.html')
    soup = api.soup(response.content, 'html.parser')

    menu_id = 'v-pills-home3' if date.isocalendar().week % 2 else 'v-pills-profile3'
    raw_text = soup.find(id = menu_id).get_text()
    stripped_lines = map(lambda ln: ln.strip(), raw_text.splitlines())
    text = list(filter(lambda ln: ln, stripped_lines))

    if date.isoweekday() > 5:
        return []

    today = __days[date.isoweekday() - 1]
    today_line = text.index(today)

    end_text = __days[date.isoweekday()]
    end_line = text.index(end_text)

    # Filter out menu item numbers
    todays_menu = list(filter(lambda ln: not ln.isupper(), text[today_line+1 : end_line]))

    def describe_dish(dish_text):
        (dish, description) = dish_text
        return api.food(dish, description)

    return list(map(describe_dish, zip(todays_menu, todays_menu[1:])))

def name():
    return "Tandoori Kitchen"
