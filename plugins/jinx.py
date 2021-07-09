from datetime import datetime

def food(api, date):
    if not api.is_current_week(date):
        return []
    if not api.json:
        return []

    def get_json_object():
        response = api.requests.get('https://www.instagram.com/jinxdynasty/?__a=1')
        return api.json.loads(response.content)

    def get_json_menu(json):
        edges = json['graphql']['user']['edge_owner_to_timeline_media']['edges']
        full_items = map(lambda edge: edge['node'], edges)
        all_items = map(build_json_menu_item, full_items)
        return filter(lambda item: item['timestamp'].isoweekday() == 1, all_items)

    def build_json_menu_item(item):
        return {
            'timestamp': datetime.fromtimestamp(item['taken_at_timestamp']),
            'text': item['edge_media_to_caption']['edges'][0]['node']['text']
        }

    def describe_dish(dish_json):
        return api.food(dish_json['text'], dish_json['text'])

    json = get_json_object()
    full_json_menu = get_json_menu(json)
    relevant_json_menu = filter(lambda item: api.is_current_week(item['timestamp']), full_json_menu)
    return map(describe_dish, relevant_json_menu)

def name():
    return "Jinx"
