from dump_to_json import dump_to_json


def main() -> None:
    dht_temp: int = 8
    ntc_temp: int = 14
    json_filename: str = "temps.json"
    dump_to_json(json_filename, dht_temp, ntc_temp)
    return


if __name__ == "__main__":
    main()
