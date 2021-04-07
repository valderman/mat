## Mat!
"What's for lunch" script for restaurants around Grönsakstorget, Gothenburg

### Dependencies
bs4, requests, importlib and argparse

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
