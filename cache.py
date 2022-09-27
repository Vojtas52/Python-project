from requests import Response

# key=url, value=response[200]
cache: dict[str, Response] = {}

# key = url, value = dictionary
data_backup: dict[str, dict] = {}

data_backup[url]['url' : url]
data_backup[url]['date' : date] # not definied yet
data_backup[url]['mileage' : mileage]
data_backup[url]['yom' : year of manufacture]