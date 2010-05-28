#!/usr/bin/env python

from model import PjSession
from gaeutils import sessions
from google.appengine.ext import db

def get_new_session(ip_addr, agent):
    
    np = PjSession()
    np.ip_address = ip_addr
    np.agent = agent
    np.put()
    
    return str(np.key())

def get_cookie():
    return sessions.Session(writer='cookie',set_cookie_expires=True)
    
def get_pjsession_obj(key):
    try:
        q = db.get(db.Key(key))
    except:
        q = None
    return q
    