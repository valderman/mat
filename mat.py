#!/bin/env python3
import requests
import importlib.machinery
import datetime
from datetime import timedelta
import argparse
import os
import sys
import traceback

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
    def __init__(self, name, dishes=[], error=None, errorTrace=None):
        self.name = name
        self.dishes = dishes
        self.error = error
        self.errorTrace = errorTrace

class FoodAPI:
    soup = BeautifulSoup
    requests = requests
    pdf = fitz
    food = Food

    def is_today(self, date):
        return date == datetime.date.today()

    def is_current_week(self, date):
        return date.isocalendar().week == datetime.date.today().isocalendar().week

    def is_weekday(self, date):
        return date.isoweekday() <= 5

foodAPI = FoodAPI()

def plugin_directory():
    home_directory = os.getenv('HOME')
    dot_mat = os.path.join(home_directory, MAT_DIR)
    if os.path.isdir(dot_mat):
        return dot_mat
    else:
        return "plugins"

def make_resturant(plugin, date):
    name = plugin.name()
    try:
        return Restaurant(name, plugin.food(foodAPI, date))
    except Exception as e:
        return Restaurant(name, error=e, errorTrace=traceback.format_exc())
        

def color_codes(use_color):
    if use_color:
        return ("\033[1m\033[95m", "\033[4m\033[94m", "", "\033[0m")
    else:
        return ("", "", "", "")

class Mat:
    def __init__(self, settings):
        self.settings = settings
        self._plugins = None

    def __print_date_heading(self, date):
        (heading, subheading, _, reset) = self.settings.color_codes
        day = date.strftime("%A")
        datestr = date.strftime("%d-%m-%Y")
        print(f"{subheading}Menu for {heading}{day}{reset} ({datestr})\n")

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

    def describe_error(self, restaurant, title):
        return [
            title, 
            "  Error fetching menu:", 
            f"    {type(restaurant.error).__name__}\n",
            f"{restaurant.errorTrace}"
            ]

    def describe_menu(self, restaurant, date):
        (heading, _, _, reset) = self.settings.color_codes
        title = f"{heading}{restaurant.name}{reset}"
        if(restaurant.error == None):
            lines = [title] + list(map(self.describe_dish, restaurant.dishes))
        else: 
            lines = self.describe_error(restaurant, title)
        return '\n'.join(lines)

    def get_dishes(self, date):
        if not self._plugins:
            self._plugins = self._load_plugins()
        restaurants = map(lambda p: make_resturant(p, date), self._plugins)
        return sorted(filter(
            lambda r: r.dishes or (not self.settings.quiet and r.error != None), 
            restaurants), key = lambda r: r.name)

    def print_menu(self, date):
        if self.settings.tomorrow:
            date += timedelta(days=1)

        self.__print_date_heading(date)
        offerings = map(lambda r: self.describe_menu(r, date), self.get_dishes(date))
        print('\n\n'.join(offerings))

def parse_args():
    parser = argparse.ArgumentParser(description="Show today's food options.")
    parser.add_argument(
        '--tomorrow', '-t',
        dest = 'tomorrow',
        action = 'store_const',
        const = True,
        default = False,
        help = 'show menu for tomorrow instead of today'
    )
    parser.add_argument(
        '--verbose', '-v',
        dest = 'verbose',
        action = 'store_const',
        const = True,
        default = False,
        help = 'show detailed information about food alternatives'
    )
    parser.add_argument(
        '--quiet', '-q',
        dest = 'quiet',
        action = 'store_const',
        const = True,
        default = False,
        help = 'Squelch errors'
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
