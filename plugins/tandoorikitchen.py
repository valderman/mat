__days = [
    u"Måndag:",
    u"Tisdag:",
    u"Onsdag:",
    u"Torsdag:",
    u"Fredag:"
]

def food(api, date):
    if not api.is_weekday(date):
        return []
    if not api.soup:
        return []

    response = api.requests.get('https://eattandoori.se/lunch.html')
    soup = api.soup(response.content, 'html.parser')

    menu_id = 'v-pills-home3' if api.week_of(date) else 'v-pills-profile3'
    raw_text = soup.find(id = menu_id).get_text()
    stripped_lines = map(lambda ln: ln.strip(), raw_text.splitlines())
    text = list(filter(lambda ln: ln, stripped_lines))

    today = __days[date.isoweekday() - 1]
    today_line = text.index(today)

    if date.isoweekday() == 5:
        menu_text = text[today_line+1 :]
    else:
        end_text = __days[date.isoweekday()]
        end_line = text.index(end_text)
        menu_text = text[today_line+1 : end_line]

    # Filter out menu item numbers
    todays_menu = list(filter(lambda ln: not ln.isupper(), menu_text))

    def get_dishes(menu):
        items = list(reversed(menu))
        while items:
            yield api.food(items.pop(), items.pop())

    return list(get_dishes(todays_menu))

def name():
    return "Tandoori Kitchen"
