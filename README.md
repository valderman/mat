## Mat!
"What's for lunch" script for restaurants around Grönsakstorget, Gothenburg

## Usage
```bash
./mat.py -p <plugin directory>
```

If no plugin directory is specified, `$HOME/.mat` is used if it exists.
If it doesn't, `./plugins` is used instead.

### Dependencies
* For everything: `algebraic-data-types`
* For restaurants with PDF menus (Bee): `PyMuPDF`
* For restaurants with JSON "menus" (Jinx): `json`
* For all other restaurants: `bs4`
* To build website: [Pandoc](https://pandoc.org)

### Troubleshooting
* Not all restaurants show up!
    - Make sure you have installed all the above dependencies
      (using `pip install <dependency>` or similar).
    - Some plugins don't support menus for other dates than today.

### Supported restaurants
* [Barabicu](https://barabicu.se)
* [Bastard Burgers](https://bastardburgers.com/se/restaurants/sodra-larmgatan/)
* [Bee](https://beebar.se/goteborg/)
* [Blackstone](https://blackstonesteakhouse.se/goteborg/)
* [Jinx](https://www.jinxfoodtruck.com)
* [Schnitzelplatz](https://schnitzelplatz.se/)
* [Solrosen](http://www.restaurangsolrosen.se)
* [Tranquilo](https://tranquilo.se)

### Generating an HTML menu
To generate a styled and somewhat interactive HTML menu, use `mat.py` and [Pandoc](https://pandoc.org)
with the provided wrapper script:
```bash
./build-site.sh
```

### Contributing
Is your favourite restaurant missing?
[File a bug report](https://github.com/valderman/mat/issues/new)
or submit a pull request!

### Plugin API
Plugins need to export two functions:
* `name()`, returning the name of the restaurant as a string, and
* `food(api, date)`, returning a list of `Food` objects representing
  the restaurants offerings on the given date.

`Food` objects are created using the function
`api.food(dish, dish_description)`.
Description may be `None`.

For convenience, `api` also contains the following:
* `soup`: reexport of `bs4.BeautifulSoup` if available, otherwise `None`
* `pdf`: reexport of `fitz` from `PyMuPDF` if available, otherwise `None`
* `json`: reexport of `json` from `json` if available, otherwise `None`
* `requests`: reexport of `requests`
* `is_today(date)`: returns `True` if `date` is today's date
* `is_current_week(date)`: returns `True` if `date` is in the current week
* `is_weekday(date)`: returns `True` if `date` is a weekday (ignoring holidays)
