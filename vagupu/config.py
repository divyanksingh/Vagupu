import logging

class Config(object):

	def logging(self):
		logger = logging.getLogger('testt')
		hdlr = logging.FileHandler('/var/tmp/test.log')
		formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
		hdlr.setFormatter(formatter)
		logger.addHandler(hdlr) 
		logger.setLevel(logging.DEBUG)
		return logger

configobj = Config()
log = configobj.logging()