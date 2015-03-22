import sys
import logging
import primes.utils.logger as logm
import primes.generator.prime as prime
import primes.generator.gaussian as gaussian
import primes.generator.pairs as pair
import primes.visualisation.ulam.ulam as ulam
import primes.visualisation.sacks.sacks as sacks
import primes.visualisation.cloud.cloud as cloud
import primes.visualisation.plaincomplex.plaincomplex as plaincomplex
import primes.ui.ngui as gui
import time


def main():
    #u = ulam.UlamSpiral(pair.Generator, {"min": 0, "max": 62750, "width": 250, "height": 250, "colour": (0, 255, 0, 255), "bgcolour": (0, 0, 0, 255)})
    #u.generator.set_gap(2)
    #s = sacks.SacksSpiral(prime.Generator, {"min": 0, "max": 20000, "width": 250, "height": 250, "colour": (0, 255, 0, 255), "bgcolour": (0, 0, 0, 255)})
    #c = cloud.PrimeCloud(prime.Generator, {"min": 0, "max": 200000, "width": 400, "height": 400, "colour": (0, 255, 0, 255), "bgcolour": (0, 0, 0, 255)})
    #p = plaincomplex.PlainComplex(gaussian.Generator, {"min": complex(-100,-100), "max": complex(100,100), "width": 400, "height": 400, "colour": (0, 255, 0, 255), "bgcolour": (0, 0, 0, 255)})
    #start = time.time()
    #s.to_image("test.png")
    #u.to_image("test.png")
    #c.to_image("test.png")
    #p.to_image("test.png")
    #print time.time() - start, "seconds"
    gui.run(sys.argv)


if __name__ == '__main__':
    logm.setup_logging()
    logger = logging.getLogger(__name__)
    main()
