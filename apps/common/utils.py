# coding: utf-8


def to_bool(value):
    return value in {True, 'True', 'true', 'yes', '1', 1}


def parse_env_list(s, sep='|', limit=-1):
    return [item.strip() for item in s.split(sep, limit) if item.strip()]


def parse_env_mapping(s):
    return dict(item.split('::', 1) for item in parse_env_list(s))

