#!/usr/bin/env python

import re, datetime

try:
    import simplejson as json
except:
    try:
        import json
    except:
        from django.utils import simplejson as json

class MarshalException(Exception):
    pass

_marshal_xml_reg = {}

def _list_to_xml(name,obj,indent=''):
    
    rv = []
    for v in obj:
        objtype = type(v)
        if objtype is dict:
            rv.append('%s<%s>' % (indent,name))
            rv.append( _dict_to_xml(v,indent + '  ') )
            rv.append('%s</%s>' % (indent,name))
        elif objtype is list:
            rv.append('%s<%s>' % (indent,name))
            rv.append( _list_to_xml(name,v,indent + '  ') )
            rv.append('%s</%s>' % (indent,name))
        else:
            rv.append( '%s<%s>%s</%s>' % (indent,name,v,name) )
            
    return '\n'.join(rv)

def _dict_to_xml(obj,indent=''):
    
    rv = []
    
    for k, v in obj.iteritems():
        objtype = type(v)
        if objtype is dict:
            rv.append('%s<%s>' % (indent,k))
            rv.append( _dict_to_xml(v, indent + '  ') )
            rv.append('%s</%s>' % (indent,k))
        elif objtype is list:
            rv.append('%s<%s>' % (indent,k))
            rv.append( _list_to_xml(k,v, indent + '  ') )
            rv.append('%s</%s>' % (indent,k))
        else:
            rv.append( '%s<%s>%s</%s>' % (indent,k,v,k) )
            
    return '\n'.join(rv)
    
_marshal_xml_reg[list] = _list_to_xml
_marshal_xml_reg[dict] = _dict_to_xml

def to_xml(obj):
    for k in _marshal_xml_reg:
        if isinstance(obj, k):
            return _marshal_xml_reg[k](obj)
    raise MarshalException, 'Invalid marshal type %s, %s' % (k, obj)
    
def marshal(data, format="xml"):
    
    if format == "xml":
        return to_xml(data)
    elif format == "json":
        return json.dumps(data)
    raise MarshalException, "Invalid format type: %s" % format


    