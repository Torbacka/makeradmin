from logging import INFO

from dotenv import dotenv_values, find_dotenv
from rocky.config import Config, Dict, Env

from service.logging import logger


class DotEnvFile(Dict):
    """ Config reader to read from docker .env file. """
    
    def __init__(self, name=None, **kwargs):
        filename = find_dotenv()
        if not filename:
            logger.info("could not find .env file, skipping")
            env = {}
        else:
            logger.info(f"loading .env file from {filename}")
            env = dotenv_values()
        
        super().__init__(env, name=name or filename, **kwargs)


default = Dict(name="default", src=dict(
    MYSQL_HOST='localhost',
    MYSQL_PORT=3306,
    MYSQL_USER='makeradmin',
    MYSQL_DB='makeradmin',
    MEMBERSHIP_URL='http://membership',
    SHOP_URL='http://backend',
    MEMBER_URL='http://backend',
    MESSAGES_URL='http://messages',
    EMAIL_DISPATCHER_URL='http://email-dispatcher',
    MULTIACCESS_SYNC_URL='http://multiaccesssync',
))
env = Env()
dot_env = DotEnvFile()

config = Config(env, dot_env, default, log_level=INFO)


def get_mysql_config():
    host = config.get('MYSQL_HOST')
    port = int(config.get('MYSQL_PORT'))
    db = config.get('MYSQL_DB')
    user = config.get('MYSQL_USER')
    pwd = config.get('MYSQL_PASS', log_value=False)
    if not pwd: raise Exception("config MYSQL_PASS is required")
    
    return dict(host=host, port=port, db=db, user=user, pwd=pwd)