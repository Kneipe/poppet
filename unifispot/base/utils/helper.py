from functools import wraps
from flask import redirect,url_for,abort,current_app,request
from flask_security import current_user
from datetime import datetime,date, timedelta
import time 
import random

#Add http to the URL if not already there
def format_url(url):
	if not url.startswith('http') and not url.startswith('https'):
		newurl =  '%s%s' % ('http://', url)
		return newurl
	return url
    



    
def register_api(bp,view,endpoint,url,security_wrap):
    ''' Register API views for a serveradmin element'''
    view_func = security_wrap(view.as_view(endpoint))
    bp.add_url_rule(url, defaults={'id': None},
                     view_func=view_func, methods=['GET',])
    bp.add_url_rule(url, defaults={'id': None}, view_func=view_func, methods=['POST',])
    bp.add_url_rule(url+'<int:id>', view_func=view_func,methods=['GET', 'POST', 'DELETE'])

def pretty_date(dt, default=None):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    Ref: https://bitbucket.org/danjac/newsmeme/src/a281babb9ca3/newsmeme/
    """

    if default is None:
        default = 'just now'

    now = datetime.utcnow()
    diff = now - dt

    periods = (
        (diff.days / 365, 'year', 'years'),
        (diff.days / 30, 'month', 'months'),
        (diff.days / 7, 'week', 'weeks'),
        (diff.days, 'day', 'days'),
        (diff.seconds / 3600, 'hour', 'hours'),
        (diff.seconds / 60, 'minute', 'minutes'),
        (diff.seconds, 'second', 'seconds'),
    )

    for period, singular, plural in periods:

        if not period:
            continue

        if period == 1:
            return u'%d %s ago' % (period, singular)
        else:
            return u'%d %s ago' % (period, plural)

    return default

def get_dates_between(start_date,end_date):
    '''Returns dates in between given datetime objects

    '''
    delta = end_date - start_date
    return [start_date + timedelta(days=x)  for x in range(delta.days + 1)]


def dict_normalise_values(dic):
    ''' Function to convert dictionary values of None to empty string '''

    new_dic = {}
    for key,val in dic.items():
        if  val == None:
            val = ''
        new_dic[key] = val
    return new_dic


def start_of_today(tzone=None):
    pass


def compare_versions(version1,version2):
    '''Compare two versions of format '1.0.0-XXXX' #manjor.minor.patch-CUSTOM

        return 0 if same version
               1 if version1 > version2
               -1 if version1 < version2

    '''
    if version1 == version2:
        return 0
    numeric_v1 = version1.split('-')[0].split('.')
    numeric_v2 = version2.split('-')[0].split('.')
    for idx, val in enumerate(numeric_v1):
        if val > numeric_v2[idx]:
            return 1
        elif val < numeric_v2[idx]:
            return -1



def get_random_integers(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
    
    Each such list is equally likely to occur."""

    dividers = sorted(random.sample(xrange(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]



