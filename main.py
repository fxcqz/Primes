import logging
import primes.utils.logger as logm
import primes.generator.prime as prime
import primes.generator.gaussian as gaussian
import primes.visualisation.ulam.ulam as ulam


def main():
    u = ulam.UlamSpiral(prime.Generator, {"min": 0, "max": 62750, "width": 250, "height": 250, "colour": (255, 0, 0, 255), "bgcolour": (0, 0, 0, 255)})
    u.to_image("test.png")
    # TODO: generators work, remove from main and write tests
    #primes = prime.Generator(maximum=62750)
    #primes.generate()
    #primes.to_file()
    #gaussians = gaussian.Generator(minimum=complex(-100, -100), maximum=complex(100, 100))
    #gaussians.generate()
    #gaussians.to_file()


if __name__ == '__main__':
    logm.setup_logging()
    logger = logging.getLogger(__name__)
    main()
