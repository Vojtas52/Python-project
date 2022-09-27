from requests import Response

# key=url, value=response[200]
cache: dict[str, Response] = {}