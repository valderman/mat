import re

def food(api, date):
    if not api.is_today(date):
        return []
    if not api.soup:
        return []

    response = api.requests.get('http://www.restaurangsolrosen.se')
    soup = api.soup(response.content, 'html.parser')
    menu = soup.find(id = "righttextarea")

    def format_food(food_type, food_description):
        if food_type == "Lasagne":
            return f"{food_description} lasagne"
        else:
            return food_description

    def get_dishes(element):
        types = element.find_all(class_ = "greybold")
        descriptions = element.find_all("td")
        for (food_type, description) in zip(types, descriptions):
            type_text = re.sub("Dagens ([^:]+): \d+ kr", "\\1", food_type.get_text().strip())
            description_text = description.get_text().strip()

            # Sallad is always the same
            if type_text != "Sallad":
                yield api.food(format_food(type_text, description_text), None)

    return get_dishes(menu)

def name():
    return "Solrosen"
