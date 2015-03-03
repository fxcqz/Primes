import primes.utils.logger as logger
import primes.generator.prime as prime_generator


def main():
    primes = prime_generator.PrimeSieve("primes/generator/data/primes/", maximum=1000)
    primes.to_file()


if __name__ == '__main__':
    logger.setup_logging()
    main()
