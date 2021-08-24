def food(api, date):
    if not api.is_current_week(date):
        return []
    if not api.is_weekday(date):
        return []
    if not api.soup:
        return []

    response = api.requests.get('https://bastardburgers.com/se/restaurants/sodra-larmgatan/')
    soup = api.soup(response.content, 'html.parser')
    today_element = soup.find("div", {"class": "w-full mb-6"})
    text = list(filter(lambda ln: ln, today_element.get_text().splitlines()))
    
    burger_name = text[1]
    burger_description = ' '.join(text[2:-1])

    return [api.food(burger_name, burger_description)]

def name():
    return "Bastard Burgers"
