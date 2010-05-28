
import os
from marshal import to_xml, marshal


def abspath(module_file_name, path):
    return os.path.join(os.path.dirname(module_file_name), path)


def jsondata( **datas ):
    '''Mempermudah transfer json data dari server ke client
    '''
    return marshal( datas,"json" )


def return_data(data_type, **datas):
    
    if data_type == 'json':
        return marshal(datas,"json")
    else:
        # default is xml
        return to_xml( datas )
        
import re
_valid_url_c = re.compile(r"^https?\://.*?\..*")

def valid_url(url):
    return _valid_url_c.match(url) is not None
    
