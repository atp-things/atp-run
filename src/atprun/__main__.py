from pprint import pprint

from atptools import DictDefault

default_config_path: str = "./.atprun.yml"


def main() -> None:
    print("atprun:", "Start")

    config: DictDefault = DictDefault()
    config.from_file(path=default_config_path)

    print("config")
    pprint(object=config)

    print("atprun:", "End")
    return None


if __name__ == "__main__":
    main()
