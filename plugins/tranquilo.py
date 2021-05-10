import re

def __present_food(api, day_menu):
    types = day_menu.find_all("h3")
    descriptions = day_menu.find_all("p")[1:]
    for (food_type, description) in zip(types, descriptions):
        yield api.food(
            food_type.get_text().strip(), 
            description.get_text().strip())

def food(api, date):
    if not api.is_current_week(date):
        return []
    if not (api.is_today(date) or api.is_tomorrow(date)):
        return []
    if not api.soup:
        return []

    response = api.requests.get('https://tranquilo.se')
    soup = api.soup(response.content, 'html.parser')
    if api.is_today(date):
        today = soup.find(id = "todays-lunch").select(
            'li:has(> h1:-soup-contains(Dagens))')[0]
        return __present_food(api, today)
    elif api.is_tomorrow(date):
        tomorrow = soup.find(id = "todays-lunch").select(
            'li:has(> h1:-soup-contains(Dagens)) + li')[0]
        return __present_food(api, tomorrow)
    


def name():
    return "Tranquilo"
