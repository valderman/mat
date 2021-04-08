import datetime

__days = [
    "Mondays Lunch",
    "Tuesdays Lunch",
    "Wednesdays Lunch",
    "Thursdays Lunch",
    "Fridays Lunch"
]

def food(api, date):
    if not api.is_current_week(date):
        return []
    if not api.is_weekday(date):
        return []
    if not api.soup:
        return []

    response = api.requests.get('https://barabicu.se')
    soup = api.soup(response.content, 'html.parser')

    li_elements = soup.find_all("li")
    lunch_heading = __days[date.isoweekday()-1]

    # Barabicu don't seem to update the heading in sync with the actual date,
    # so we can't assume "Todays Lunch" is the right heading just because date is today.
    today_elements = list(filter(lambda e: e.get_text().startswith(lunch_heading), li_elements))
    if not today_elements:
        if date == datetime.date.today():
            today_elements = filter(lambda e: e.get_text().startswith("Todays Lunch"), li_elements)
        else:
            return []

    today_element = list(today_elements)[0]
    dishes = filter(lambda e: e.get_text(), today_element.find_all("h3"))
    descriptions = today_element.find_all("p")

    def make_food(dish_description):
        (dish, description) = dish_description
        dirty_dish_name = dish.get_text().split("•")[0]
        cleaned_words = filter(lambda w: w, dirty_dish_name.split(" "))
        dish_name = " ".join(cleaned_words).title()
        return api.food(dish_name, description.get_text())

    return list(map(make_food, zip(dishes, descriptions)))

def name():
    return "Barabicu"
