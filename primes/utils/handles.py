# GENERATORS
import primes.generator.prime
import primes.generator.gaussian
import primes.generator.pairs

# VISUALISATIONS
import primes.visualisation.ulam.ulam
import primes.visualisation.sacks.sacks
import primes.visualisation.cloud.cloud
import primes.visualisation.plaincomplex.plaincomplex
import primes.visualisation.simplegrid.simplegrid
import primes.visualisation.wireframe.wireframe


"""Provides handles to all generators and visualisations as live objects.

Attributes:
    generators -- Dict of all dataset generators.
    visualisations -- Dict of all visualisations.
"""
generators = {"Primes": primes.generator.prime,
              "Gaussians": primes.generator.gaussian,
              "Prime Pairs": primes.generator.pairs}

visualisations = {"Ulam Spiral": primes.visualisation.ulam.ulam.UlamSpiral,
                  "Sacks Spiral": primes.visualisation.sacks.sacks.SacksSpiral,
                  "Data Cloud": primes.visualisation.cloud.cloud.PrimeCloud,
                  "Complex Plane": primes.visualisation.plaincomplex.plaincomplex.PlainComplex,
                  "Simple Grid": primes.visualisation.simplegrid.simplegrid.SimpleGrid,
                  "Wireframe": primes.visualisation.wireframe.wireframe.Wireframe}
