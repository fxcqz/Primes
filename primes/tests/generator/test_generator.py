from nose.tools import *
import os
import numpy
import primes.generator.generator as generator
import primes.generator.prime as prime
import primes.generator.gaussian as gaussian


def test_constructor():
    g = generator.Generator()
    assert_is_not_none(g)
    assert_equals(g.minimum, 0)
    assert_equals(g.maximum, 1)
    assert_equals(g.data, [])

def test_data_files_from_dir():
    g = generator.Generator()
    g.path = "./data/"
    assert_equals(g.data_files_from_dir(), ["1.dat"])

def test_read_cache():
    g = generator.Generator(maximum=10)
    g.path = "./data/"
    data = g.read_cache()
    assert_equals(list(data), [2, 3, 5, 7])
    data = g.read_cache()
    assert_equals(list(data)[-1], 7)

def test_complex_range():
    g = generator.Generator()
    r = g.complex_range(complex(-5, -5), complex(5, 5))
    assert_equals(len(r), 100)
    assert_equals(r[0], complex(-5, -5))
    assert_equals(r[-1], complex(4, 4))

def test_not_in_cache():
    g = generator.Generator(maximum=10)
    g.path = "./data/"
    g.data = g.read_cache()
    assert_equals(g.not_in_cache(), ([0, 1], [8, 9, 10]))

def test_complex_not_in_cache():
    g = generator.Generator(complex(-2, -2), complex(2, 2))
    g.path = "./data/"
    g.datatype = complex
    g.data = [complex(0, 0)]
    assert_equals(g.not_in_cache(), ([complex(-2, -2), complex(-2, -1), complex(-1, -2), complex(-1, -1)], [complex(1, 1), complex(1, 2), complex(2, 1), complex(2, 2)]))

def test_next_filename():
    g = generator.Generator()
    assert_equals(g.next_filename("./data/"), "2.dat")

# PRIME GENERATOR ##############################################################
def test_prime_constructor():
    g = prime.Generator()
    assert_equals(g.path, "primes/generator/data/primes/")

def test_is_prime():
    g = prime.Generator()
    assert_equals(g.is_prime(2), True)
    assert_equals(g.is_prime(56599), True)
    assert_equals(g.is_prime(54362732), False)

def test_j_increment():
    g = prime.Generator(maximum=10)
    assert_equals(g.j_increment(1), range(1, 11))
    assert_equals(g.j_increment(5), [])

def test_prime_generate():
    g = prime.Generator(maximum=10)
    g.path = "./data/"
    g.generate()
    assert_equals(list(g.data), [2, 3, 5, 7])

def test_prime_big_generate():
    g = prime.Generator(maximum=100000)
    g.path = "./data/"
    g.generate()
    os.remove("data/2.dat")
    for n in g.data:
        assert_true(g.is_prime(n))
    assert_equals(g.data[-1], 99991)

# GAUSSIAN GENERATOR ###########################################################
def test_gaussian_constructor():
    g = gaussian.Generator()
    # remove dirs created by prime gen call in gaussian constructor
    # ... ugly i know
    os.remove("primes/generator/data/primes/1.dat")
    os.removedirs("primes/generator/data/primes")
    assert_equals(g.path, "primes/generator/data/gaussians/")
    assert_equals(g.datatype, complex)
    assert_equals(g.threshold, 300)
    assert_equals(g.primes, [2])

def test_is_gaussian_prime():
    g = gaussian.Generator(minimum=complex(-5, -5), maximum=complex(5, 5))
    os.remove("primes/generator/data/primes/1.dat")
    os.removedirs("primes/generator/data/primes")
    assert_false(g.is_gaussian_prime(complex(0, 0)))
    assert_true(g.is_gaussian_prime(complex(-5, -4)))

def test_gaussian_generate():
    g = gaussian.Generator(minimum=complex(-5, -5), maximum=complex(5, 5))
    os.remove("primes/generator/data/primes/1.dat")
    os.removedirs("primes/generator/data/primes")
    g.generate()
    assert_equals(len(g.data), 40)
    assert_true(complex(-5, -4) in g.data)
    os.remove("primes/generator/data/gaussians/1.dat")
    os.removedirs("primes/generator/data/gaussians")
