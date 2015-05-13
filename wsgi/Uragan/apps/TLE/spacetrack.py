# -*- coding: utf-8 -*-
""" Functional implementation of SpaceTrack API requests
"""

import requests
from datetime import date, datetime


_url_base = "https://www.space-track.org/"
_url_login = "ajaxauth/login"
_url_logout = "ajaxauth/logout"
_url_request = "basicspacedata/query/class/tle/format/json/NORAD_CAT_ID/"  # 25544
_url_request_postfix = "/orderby/EPOCH%20desc/limit/1"


def tle_query_build(latest=False, order_by='EPOCH', sort='desc', norad_id='25544', date_range=(0, 0), last=None):
    print(date_range)
    print(type(date_range[0]) is date)
    if latest:
        return ('https://www.space-track.org/basicspacedata/query/class/tle_latest/'
                'ORDINAL/1/'
                'NORAD_CAT_ID/{norad_id}/'
                'orderby/{order_by}%20{sort}/'.format(norad_id=norad_id,
                                                      order_by=order_by,
                                                      sort=sort))
    if last:
        return ('https://www.space-track.org/basicspacedata/query/class/tle_latest/'
                'ORDINAL/1--{last}/'
                'NORAD_CAT_ID/{norad_id}/'
                'orderby/{order_by}%20{sort}/'.format(last=last,
                                                      norad_id=norad_id,
                                                      order_by=order_by,
                                                      sort=sort))
    if type(date_range) is tuple:
        if (type(date_range[0]) is date) and (type(date_range[1]) is date):
            return ('https://www.space-track.org/basicspacedata/query/class/tle/'
                    'EPOCH/{date_min}--{date_max}/'
                    'NORAD_CAT_ID/{norad_id}/'
                    'orderby/{order_by}%20{sort}/'.format(date_min=min(date_range),
                                                          date_max=max(date_range),
                                                          norad_id=norad_id,
                                                          order_by=order_by,
                                                          sort=sort))


def login(credentials=None):
    """ Retrieves a cookie for making requests to the SpaceTrack API, given valid credentials.
    """
    if not _valid_credentials(credentials):
        return False
    url = _url_base + _url_login
    r = requests.post(url, data=credentials)
    if r.status_code == requests.codes.ok:
        cookie = r.cookies.get_dict()
        return cookie
    else:
        print(("error:", "login:", r.text))
        return False


def logout(cookie):
    """ Expires provided SpaceTrack cookie.
    """
    url = _url_base + _url_logout
    r = requests.get(url, cookies=cookie)
    if r.text == '"Successfully logged out"':
        return True
    return False


def request(cookie, norad_id=None, spacetrack_query=None):
    """ Makes request for latest TLE of norad_id satellite.

        If called with a non-None spacetrack_query, it will make that request instead.
    """
    if spacetrack_query is None and norad_id is not None:
        url = _url_base + _url_request + str(norad_id) + _url_request_postfix
    elif spacetrack_query is not None:
        url = _url_base + spacetrack_query
    else:
        return {'huh?': 'no request.'}
    r = requests.get(url, cookies=cookie)
    return r.json()


def _valid_credentials(credentials):
    """ Checks if credentials provided is sane.
    """
    if isinstance(credentials, dict):
        if 'identity' in credentials and 'password' in credentials:
            return True
    return False


def request_sequence(credentials, norad_id=None, spacetrack_query=None):
    """ Handles a complete login, request, logout cycle and returns full TLE json.
    """
    cookie = login(credentials=credentials)
    r = request(cookie, norad_id, spacetrack_query=spacetrack_query)
    logout(cookie)
    return r


if __name__ == '__main__':
    credentials = {'identity': 'nikita.koshelev@gmail.com', 'password': 'K0SHeLeV21101994'}
    query = tle_query_build(date_range=(date(2015, 5, 9), date.today()))
    print(query)
    r = request_sequence(credentials, spacetrack_query=query)
    result = set((datetime.strptime(tle['EPOCH'], '%Y-%m-%d %H:%M:%S'), tle['TLE_LINE0'][2:], tle['TLE_LINE1'], tle['TLE_LINE1']) for tle in r)
    for tle in sorted(result, reverse=True):
        print(tle)

