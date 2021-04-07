#!/bin/env python3
import requests
import importlib.machinery
import datetime
import argparse
import os
from bs4 import BeautifulSoup

MAT_DIR = '.mat'

class Food:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def pretty(self):
        return f"{self.title}\n  {self.description}"

class FoodAPI:
    soup = BeautifulSoup
    requests = requests
    food = Food

def plugin_directory():
    home_directory = os.getenv('HOME')
    return os.path.join(home_directory, MAT_DIR)

def color_codes(use_color):
    if use_color:
        return ("\033[1m\033[95m", "\033[4m\033[94m", "", "\033[0m")
    else:
        return ("", "", "", "")

class Mat:
    def __init__(self, settings):
        self.settings = settings

    def load_plugins(self):
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

    def describe_menu(self, plugin, date):
        (heading, _, _, reset) = self.settings.color_codes
        restaurant = f"{heading}{plugin.name()}{reset}"
        menu_items = plugin.food(FoodAPI, date)
        lines = [restaurant] + list(map(self.describe_dish, menu_items))
        return '\n'.join(lines)

    def print_menu(self, date):
        offerings = map(lambda p: self.describe_menu(p, date), self.load_plugins())
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
