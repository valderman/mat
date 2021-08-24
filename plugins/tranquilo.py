import re

def food(api, date):
    if not api.is_current_week(date):
        return []
    if not api.is_today(date):
        raise NotImplementedError("Tranquilo currently only supports menus for today")
    if not api.soup:
        return []

    response = api.requests.get('https://tranquilo.se')
    soup = api.soup(response.content, 'html.parser')
    today = soup.find(id = "todays-lunch").select(
        'li:has(> h1:-soup-contains(Dagens))')[0]
    types = today.find_all("h3")
    descriptions = today.find_all("p")[1:]
    for (food_type, description) in zip(types, descriptions):
        yield api.food(None, description.get_text().strip())

def name():
    return "Tranquilo"
