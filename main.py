import sys
import logging
import primes.utils.logger as logm
import primes.ui.gui as gui


def main():
    gui.run(sys.argv)


if __name__ == '__main__':
    logm.setup_logging()
    logger = logging.getLogger(__name__)
    main()
