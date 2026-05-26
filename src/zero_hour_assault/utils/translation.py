from file_directories import file_get_contents
import globals as g
from rotation import getdir, dir_to_string
from deep_translator import GoogleTranslator
from security import file_decrypt
translator_instance = GoogleTranslator()
from security import file_decrypt,file_encrypt
def google_get_translation_languages():
	try:
		return translator_instance.get_supported_languages()
	except:
		return []

def google_translate(source_language, destination_language, text):
	try:
		language_map = translator_instance.get_supported_languages(True)
		translator_instance.source = language_map[source_language]
		translator_instance.target = language_map[destination_language]
		return translator_instance.translate(text)
	except:
		return

def translate(txt):
	if g.lang=="en": return txt
	if txt in g.transcache: return g.transcache[txt]
	orig_txt=txt
	if g.lngdata=="":
		try: file_decrypt("lang/"+g.lang+".lng",g.langkey)
		except: pass
		try: g.lngdata=file_get_contents("lang/"+g.lang+".lng","r","utf-8")
		except: pass
		try: file_encrypt("lang/"+g.lang+".lng",g.langkey)
		except: pass
	for line in g.lngdata.split("\n"):
		if line=="": continue
		pair=line.split("=")
		if len(pair)<2: return txt
		if len(pair)>3: return txt
		if len(pair)==2 and pair[0].lower()==txt.lower(): txt = pair[1]
		if len(pair)==3 and pair[2]=="substr" and txt.find(pair[0])>-1: txt = txt.replace(pair[0],pair[1],-1)
		if len(pair)==3 and pair[2]!="substr": return txt
	if orig_txt!=txt: g.transcache[orig_txt]=txt
	return txt
