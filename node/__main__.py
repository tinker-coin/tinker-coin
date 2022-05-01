import os
import sys
import logging

# Setup module paths
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

print("Main")
print(sys.path)

logger = logging.getLogger(__name__)


def main(argv):
    setup_logger('--debug' in argv)
    logger.debug("Starting Node. Args: %s", argv)
    current_dir = os.path.abspath(os.curdir)
    logger.debug("Current Directory: %s", current_dir)
    start_node(working_dir=current_dir)


def start_node(working_dir):
    from module.dependencyinjector import DependencyInjector
    config_file = os.path.join(working_dir, "config.json")
    logger.debug("Config file: %s", config_file)
    di = DependencyInjector(config_file=config_file,
                            working_dir=working_dir,
                            code_root=os.path.dirname(os.path.abspath(__file__)))
    di.app.start()


def setup_logger(debug):
    # Configure main logger
    main_logger = logging.getLogger("")
    main_logger.setLevel(logging.DEBUG if debug else logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    main_logger.addHandler(handler)


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main(sys.argv)
