import json
from typing import NamedTuple

class Config(NamedTuple):
    bot_token: str
    ip: str
    port: int
    ignore_list: list[str]
    once_list: list[str]
    refresh_list: list[str]

def read_config():
    with open('data/config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
    return Config(**config)

def add_ignore_code(code):
    config = read_config()._asdict()
    ignore_list = config['ignore_list']
    if code not in config['ignore_list']:
        ignore_list: list = ignore_list.append(code)
        update_config(config, ignore_list=ignore_list)

def remove_ignore_code(code):
    config = read_config()._asdict()
    ignore_list: list = config['ignore_list']
    try:
        ignore_list.remove(code)
    except:
        pass
    update_config(config, ignore_list=ignore_list)


def reset_ignore_list():
    config = read_config()._asdict()
    ignore_list : list = config['ignore_list']
    for code in config['once_list']:
        if code in ignore_list:
            ignore_list.remove(code)
    update_config(config, ignore_list=ignore_list)

def update_ip(new_ip: str):
    config = read_config()._asdict()
    update_config(config, ip=new_ip)

def update_config(config: dict, **updates):

    for key, value in updates.items():
        if key not in config:
            raise KeyError(f'"{key}" is not a valid config field.')
        config[key] = value

    with open('data/config.json', 'w', encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False, indent=4)
    return Config(**config)
