DEFAULT_SSID: str = "addYourself"
DEFAULT_PASSWORD: str = "addYourself"

secrets = {
    'ssid': DEFAULT_SSID,
    'pw': DEFAULT_PASSWORD
}

if secrets["ssid"] == DEFAULT_SSID or secrets["pw"] == DEFAULT_PASSWORD:
    raise ValueError("Change secrets.py SSID and password values to match your network credentials")
