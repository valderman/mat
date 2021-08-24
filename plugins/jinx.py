from datetime import datetime
import re

def food(api, date):
    if not api.is_current_week(date):
        return []
    if not api.json:
        return []

    def get_json_object():
        response = api.requests.get('https://op.fd-api.com/api/v5/vendors/s8sq?include=menus')
        return api.json.loads(response.content)

    def get_json_menu(json):
        return json['data']['menus'][0]['menu_categories'][0]['products']

    def build_json_menu_item(item):
        return {
            'timestamp': datetime.fromtimestamp(item['taken_at_timestamp']),
            'text': item['edge_media_to_caption']['edges'][0]['node']['text']
        }

    def describe_dish(dish_json):
        return api.food(dish_json['text'], dish_json['text'])

    json = get_json_object()
    json_menu = get_json_menu(json)
    return map(lambda x: api.food(x['name'], re.sub(r'\n', ' ', x['description'])), json_menu)

def name():
    return "Jinx"
