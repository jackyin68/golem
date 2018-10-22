from os import path

from golem.core.common import get_golem_path
from golem.docker.environment import DockerEnvironment

class MonitorTaskEnvironment(DockerEnvironment):
    DOCKER_IMAGE = "golemfactory/base"
    DOCKER_TAG = "1.2"
    ENV_ID = "monitor"
    APP_DIR = path.join(get_golem_path(), 'apps', 'monitor')
    SCRIPT_NAME = "docker_monitortask.py"
    SHORT_DESCRIPTION = "Monitor PoC"
