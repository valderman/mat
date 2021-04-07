#!/bin/env python3
import requests
import importlib.machinery
import datetime
import argparse
import os

try:
    from bs4 import BeautifulSoup
except:
    BeautifulSoup = None

try:
    import fitz
except:
    fitz = None

MAT_DIR = '.mat'

class Food:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def pretty(self):
        return f"{self.title}\n  {self.description}"

class Restaurant:
    def __init__(self, name, dishes):
        self.name = name
        self.dishes = dishes

class FoodAPI:
    soup = BeautifulSoup
    requests = requests
    pdf = fitz
    food = Food

def plugin_directory():
    home_directory = os.getenv('HOME')
    dot_mat = os.path.join(home_directory, MAT_DIR)
    if os.path.isdir(dot_mat):
        return dot_mat
    else:
        return "plugins"

def color_codes(use_color):
    if use_color:
        return ("\033[1m\033[95m", "\033[4m\033[94m", "", "\033[0m")
    else:
        return ("", "", "", "")

class Mat:
    def __init__(self, settings):
        self.settings = settings
        self._plugins = None

    def _load_plugins(self):
        directory = self.settings.plugin_directory
        for file in sorted(os.listdir(directory)):
            if file[-3:] == ".py":
                module = file[0:-3]
                path = os.path.join(directory, file)
                loader = importlib.machinery.SourceFileLoader(module, path)
                yield loader.load_module(module)

    def describe_dish(self, dish):
        (_, subheading, body, reset) = self.settings.color_codes
        dish_name = f"  {subheading}{dish.title}{reset}"
        if self.settings.verbose:
            return f"{dish_name}\n    {body}{dish.description}{reset}"
        else:
            return dish_name

    def describe_menu(self, restaurant, date):
        (heading, _, _, reset) = self.settings.color_codes
        title = f"{heading}{restaurant.name}{reset}"
        lines = [title] + list(map(self.describe_dish, restaurant.dishes))
        return '\n'.join(lines)

    def get_dishes(self, date):
        if not self._plugins:
            self._plugins = self._load_plugins()
        restaurants = map(lambda p: Restaurant(p.name(), p.food(FoodAPI, date)), self._plugins)
        return filter(lambda r: r.dishes, restaurants)

    def print_menu(self, date):
        offerings = map(lambda r: self.describe_menu(r, date), self.get_dishes(date))
        print('\n\n'.join(offerings))

def parse_args():
    parser = argparse.ArgumentParser(description="Show today's food options.")
    parser.add_argument(
        '--verbose', '-v',
        dest = 'verbose',
        action = 'store_const',
        const = True,
        default = False,
        help='show detailed information about food alternatives'
    )
    parser.add_argument(
        '--color', '-c',
        dest = 'color_codes',
        action = 'store_const',
        const = color_codes(True),
        default = color_codes(False),
        help='colorize restaurant names, dishes, and descriptions'
    )
    parser.add_argument(
        '--plugin-directory', '-p',
        dest = 'plugin_directory',
        action = 'store',
        default = plugin_directory(),
        help='load restaurant plugins from this directory'
    )

    return parser.parse_args()

mat = Mat(parse_args())
mat.print_menu(datetime.date.today())
