import sys, requests, json, re, os
import logging, logging.handlers
import splunk

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import apprise

def setup_logging():
    logger = logging.getLogger('splunk.apprise')    
    SPLUNK_HOME = os.environ['SPLUNK_HOME']
    
    LOGGING_DEFAULT_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log.cfg')
    LOGGING_LOCAL_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log-local.cfg')
    LOGGING_STANZA_NAME = 'python'
    LOGGING_FILE_NAME = "apprise.log"
    BASE_LOG_PATH = os.path.join('var', 'log', 'splunk')
    LOGGING_FORMAT = "%(asctime)s %(levelname)-s\t%(module)s:%(lineno)d - %(message)s"
    splunk_log_handler = logging.handlers.RotatingFileHandler(os.path.join(SPLUNK_HOME, BASE_LOG_PATH, LOGGING_FILE_NAME), mode='a') 
    splunk_log_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
    logger.addHandler(splunk_log_handler)
    splunk.setupSplunkLogger(logger, LOGGING_DEFAULT_CONFIG_FILE, LOGGING_LOCAL_CONFIG_FILE, LOGGING_STANZA_NAME)
    return logger

def check_inputs(config, logger):
    required_fields = ['body']
    
    if not 'url' in config and not 'tag' in config:
        logger.error("A URL or tag needs to be specified.")
        return False

    if 'tag' in config and not 'config' in config:
        logger.error("Using a tag requires setting a configuration file defined in setup.")
        return False
    
    if 'tag' in config and 'config' in config:
        if not os.path.exists(config['config']):
            logger.error("Unable to locate config file {}".format(config['config']))
            return False

    for field in required_fields:
        if not field in config:
            logger.error("No "+field+" specified.")
            return False
        
    return True


if len(sys.argv) > 1 and sys.argv[1] == "--execute":
    logger = setup_logging()
    alert = json.load(sys.stdin)
    if check_inputs(alert['configuration'], logger):
        #load config
        config = alert['configuration']
        

        if 'config' in config and 'tag' in config:
            ac = apprise.AppriseConfig()
            ac.add(config['config'])

            ar = apprise.Apprise()
            ar.add(ac)

            if "title" in config:
                ar.notify(
                    body=config['body'],
                    title=config['title'],
                    tag=config['tag']
                )
            else:
                ar.notify(
                    body=config['body'],
                    tag=config['tag']
                )
        elif 'url' in config:
            ar = apprise.Apprise()
            ar.add(config['url'])

            if "title" in config:
                ar.notify(
                    body=config['body'],
                    title=config['title']
                )
            else:
                ar.notify(
                    body=config['body']
                )

    else:
        logger.error("Invalid configuration detected. Stopped.")
else:
    print("FATAL No execute flag given")
