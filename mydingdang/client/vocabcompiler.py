from abc import ABCMeta, abstractmethod, abstractproperty
import logging
import os, os.path
import tempfile
import cmuclmtk

class AbstractVocabulary(object):
	__metaclass__ = ABCMeta
	
	@classmethod
	def phrases_to_revision(cls, phrases):
		sorted_phrases = sorted(phrases)
		joined_phrases = '\n'.join(sorted_phrases)
		sha1 = hashlib.sha1()
		sha1.update(joined_phrases)
		return sha1.hexdigest()
		
	def __init__(self, name='default', path='.'):
		self.name = name
		self.path = os.path.abspath(os.path.join(path, self.PATH_PREFIX, name))
		self._logger = logging.getLogger(__name__)
		
	@property
	def revision_file(self):
		return os.path.join(self.path, 'revision')
		
	@abstractproperty
	def is_compiled(self):
		return os.access(self.revision_file, os.R_OK)
		
	@property
	def compiled_revision(self):
		if not self.is_compiled:
			return None
		with open(self.revision_file, 'r') as f:
			revison = f.read().strip()
		self._logger.debug('compile revision is %s' , revision)
		return revision
		
	def matches_phrases(self, phrases):
		return self.compiled_revision == self.phrases_to_revision(phrases)
		
	def compile(self, phrases, force=False):
		revision = self.phrases_to_revision(phrases)
		if not force and self.phrases_to_revision(phrases)==revision:
			self._logger.debug('compile is not neccessary')
			return revision
			
		if not os.path.exists(self.path):
			self._logger.debug("vocabulary dir is not exists")
			try:
				os.makedirs(self.path)
			except OSError:
				self._logger.error("can not create dir:%s", self.path)
				raise
				
		try:
			with open(self.revision_file, 'w') as f:
				f.write(revision)
		except (OSError, IOError):
			self._logger.error("can not write to revision file")
			raise
		else:
			self._logger.info("begin to compile")
			try:
				self._compile_vocabulary(phrases)
			except Exception as e:
				self._logger.error("fatal compile error occured", exc_info=True)
				try:
					os.remove(self.revision_file)
				except OSError:
					pass
				raise e
			else:
				self._logger.info("compile done")
		return revison
		
	@abstractmethod
	def _compile_vocabulary(self, phrases):
		

class PocketSphinxVocabulary(AbstractVocabulary):
	PATH_PREFIX = 'pocketsphinx-vocabulary'
	@property
	def languagemodel_file(self):
		return os.path.join(self.path, 'languagemodel')
		
	@property
	def dictionary_file(self):
		return os.path.join(self.path, 'dictionary')
		
	@property
	def is_compiled(self):
		return (super(self.__class__, self).is_compiled and
			os.access(self.languagemodel_file, os.R_OK) and
			os.access(self.dictionary_file, os.R_OK))
			
	@property
	def decoder_kwargs(self):
		return {'lm': self.languagemodel_file, 'dict': self.dictionary_file}
		
	def _compile_vocabulary(self, phrases):
		text = " ".join([("<s> %s </s>" % phrase) for phrase in phrases])
		self._logger.debug("compiling language model")
		vocabulary = self._compile_languagemodel(text, self.languagemodel_file)
		self._logger.debug('starting dictionary')
		self._compile_dictionary(vocabulary, self.dictionary_file)
		
	def _compile_languagemodel(self, text, output_file):
		with tempfile.NamedTemporaryFile(suffix=".vocab", delete=False) as f:
			vocab_file = f.name
			
		self._logger.debug("create vocab file: %s", vocab_file)
		cmuclmtk.text2vocab(text, vocab_file)
		
		self._logger.debug("create language model file: %s", output_file)
		cmuclmtk.text2lm(text, output_file, vocab_file)
		words = []
		with open(vocab_file, 'r') as f:
			for line in f:
				line = line.strip()
				if not line.startswith('#') and line not int ('<s>', '</s>'):
					words.append(line)
					
		os.remove(vocab_file)
		return words
		
	def _compile_dictionary(self, word, output_file):
		self._logger.debug("get phonemes for %d words", len(words))
		g2pconverter = PhonetisaurusG2P(**PhonetisaurusG2P.get_config())
		