import json, os, logging, os.path
from abc import ABCMeta, abstractmethod
import dingdangpath

class AbstractSTTEngine(object):
	__metaclass__ = ABCMeta
	VOCABULARY_TYPE = None
	
	@classmethod
	def get_config() :
		return {}
		
	@classmethod
	def get_instance(cls, vocabulary_name, phrases):
		profile = cls.get_config()
		if cls.VOCABULARY_TYPE:
			vocabulary = cls.VOCABULARY_TYPE(vocabulary_name, path=dingdangpath.config('vocabularies'))
			if not vocabulary.matches_phrases(phrases):
				vocabulary.compile(phrases)
			profile['vocabulary'] = vocabulary
		instance = cls(**profile)
		return instance
		
	@classmethod
	def get_passive_instance(cls):
		phrases = vocabcompiler.get_keyword_phrases()
		return cls.get_instance('keyword', phrases)
		
	@classmethod
	def get_active_instance(cls):
		phrases = vocabcompiler.get_all_phrases()
		return cls.get_instance('default', phrases)
		
	@classmethod
	def get_music_instance(cls):
		phrases = vocabcompiler.get_all_phrases()
		return cls.get_instance('music', phrases)
		
	@classmethod
	@abstractmethod
	def is_available(cls):
		return True
		
	@abstractmethod
	def transcribe(self, fp):
		pass
		
	@classmethod
	def transcribe_keyword(self, fp):
		pass
		
		
class PocketSphinxSTT(AbstractSTTEngine):
	SLUG = 'sphinx'
	VOCABULARY_TYPE = vocabcompiler.PocketSphinxVocabulary
	
def get_engines():
	def get_subclasses(cls):
		subclasses = set()
		for subclass in cls.__subclasses__():
			subclasses.add(subclass)
			subclasses.update(get_subclasses(subclass))
		return subclasses
	return [ stt_engine for stt_engine in list(get_subclasses(AbstractSTTEngine)) if hasattr(stt_engine, 'SLUG') and stt_engine.SLUG ]
	
def get_engine_by_slug(slug=None):
	if not slug or type(slug) is not str:
		raise TypeError("invalid slug %s", slug)
		
	selected_engines = filter(lambda engine : hasattr(engine, 'SLUG') and engine.SLUG==slug, get_engines())
	
	if len(selected_engines) == 0:
		raise ValueError("no stt engine found for slug %s" % slug)
	else:
		engine = selected_engines[0]
		if not engine.is_available():
			raise ValueError("stt engine %s is not available" % slug)
		return engine
		
		