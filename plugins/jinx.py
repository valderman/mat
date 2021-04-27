def food(api, date):
    if not api.is_current_week(date):
        return []
    if not api.soup:
        return []

    response = api.requests.get('https://www.foodora.se/en/restaurant/s8sq/jinx-dynasty')
    soup = api.soup(response.content, 'html.parser')
    text = list(map(lambda ln: ln.strip(), soup.get_text().splitlines()))

    def find_dish(dish_name):
        start_line = text.index(dish_name)
        return text[start_line+3].strip()

    def describe_dish(dish_text):
        dish = dish_text.split(',')[0]
        description = dish_text[len(dish)+2:]
        return api.food(dish, description.capitalize())

    def get_menu_items(menu_lines):
        lines = list(reversed(menu_lines))
        while lines:
            dish = lines.pop()
            description = lines.pop()
            lines.pop()
            yield api.food(dish, description)

    try:
        meat = find_dish(u"Lunch Kött")
        vegan = find_dish(u"Lunch Vegan")
        return map(describe_dish, [meat, vegan])
    except:
        return []

def name():
    return "Jinx"
