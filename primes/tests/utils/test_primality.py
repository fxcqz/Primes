from nose.tools import *
import primes.utils.primality as p


def test_primality():
    assert_true(p.is_prime(2))
    assert_false(p.is_prime(6))
    assert_true(p.is_prime(99991))
