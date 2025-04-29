import json

temps: dict = {
    "dht_temp": 0,
    "ntc_temp": 0
}


def dump_to_json(json_filename: str, dht_temp: int, ntc_temp: int) -> None:
    with open(json_filename, "w") as json_file:
        temps["dht_temp"] = dht_temp
        temps["ntc_temp"] = ntc_temp
        json.dump(temps, json_file, indent=4)
        json_file.close()


if __name__ == "__main__":
    dump_to_json("temps.json", 20, 7);
