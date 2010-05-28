

import random
from model import UrlRecord, PjSession, HitCounter
from sessutils import get_pjsession_obj

def generate_short_url(domain):
	vokal = 'aoeui'
	vokaldbl = ('ai','oi','io')
	konsonan = 'lrcgypdhtnsqjkbmwvz'
	konsdbl = ('nt','rs','tm','ks','mn','rk')
	rvok = [random.choice(tuple(vokal) + vokaldbl) for i in xrange(2)]
	rkons = [random.choice(tuple(konsonan) + konsdbl) for i in xrange(2)]

	rmix = ''.join(reduce(lambda a,b: a+b,zip(rvok,rkons)))

	kosa_kata = (
	'anv', 'dit', 'sit','fak','luc',
	'ariv','nat','ram','bas','fat','mur'
	)
	
	code = "%s%s%s" % (random.choice(kosa_kata),rmix,random.choice(vokal))
	
	return (code,"http://%s/%s" % (domain,code))

def add_url( key, ori, gen, code ):
	
	ps = get_pjsession_obj(key)
	ps.put()
	
	rec = UrlRecord()
	
	rec.code = code
	rec.orig_url = ori
	rec.gen_url = gen
	rec._session = ps
	
	rec.put()
	
def get_urlrec( ori = None, code = None ):
	
	assert( ori or code )
	
	rv = None
	q = UrlRecord.all()
	if ori:
		rv = q.filter("orig_url =", ori)
	elif code:
		rv = q.filter("code =", code)
		
	if rv:
		if rv.count() > 0:
			return rv.get()
		
	return None

def hit_url( code, url_referer, agent ):
	rec = get_urlrec(code = code)
	if rec:
		h = HitCounter(_url_record=rec, url_referer = url_referer, agent = agent)
		h.put()

def ori_url_exists( url ):
	return get_urlrec( ori = url ) is not None


def get_urlcode( gen ):
	return gen[gen.rfind("/") + 1:]

def format_url( domain, code ):
	return "http://%s/%s" % (domain,code)

