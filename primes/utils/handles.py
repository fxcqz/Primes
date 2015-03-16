# GENERATORS
import primes.generator.prime
import primes.generator.gaussian

# VISUALISATIONS
import primes.visualisation.ulam.ulam
import primes.visualisation.sacks.sacks


generators = {"Primes": primes.generator.prime,
              "Guassians": primes.generator.gaussian}

visualisations = {"Ulam Spiral": primes.visualisation.ulam.ulam.UlamSpiral,
                  "Sacks Spiral": primes.visualisation.sacks.sacks.SacksSpiral}
