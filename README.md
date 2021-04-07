## Mat!
"What's for lunch" script for restaurants around Grönsakstorget, Gothenburg

## Usage
```bash
./mat.py -p <plugin directory>
```

If no plugin directory is specified, `$HOME/.mat` is used if it exists.
If it doesn't, `./plugins` is used instead.

### Dependencies
* For restaurants with PDF menus (Bee): `PyMuPDF`
* For all other restaurants: `bs4`

### Troubleshooting
* Not all restaurants show up!
    - Make sure you have installed all the above dependencies
      (using `pip install <dependency>` or similar).
    - Some plugins don't support menus for other dates than today.

### Supported restaurants
* [Barabicu](https://barabicu.se)
* [Bee](https://beebar.se/goteborg/)
* [Blackstone](https://blackstonesteakhouse.se/goteborg/)
* [Jinx](https://www.jinxfoodtruck.com)
* [Tandoori Kitchen](https://eattandoori.se)

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

For convenience, `api` also contains the following:
* `soup`: reexport of `bs4.BeautifulSoup`
* `requests`: reexport of `requests`
