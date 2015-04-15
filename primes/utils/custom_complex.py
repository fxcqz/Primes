from functools import total_ordering


@total_ordering
class CustomComplex(complex):
    """Wrapper class for complex type.

    Implements various comparative operators (==, <, <=, >, >=) in order for
    complex numbers to be compared and ordered.

    Extends built-in complex type.
    """
    def __eq__(self, other):
        """Implements == operator."""
        return abs(self) == abs(other) \
                and self.real == other.real \
                and self.imag == other.imag

    def __lt__(self, other):
        """Implements < operator."""
        return abs(self) < abs(other)

    def __le__(self, other):
        """Implements <= operator."""
        return abs(self) <= abs(other)

    def __gt__(self, other):
        """Implements > operator."""
        return abs(self) > abs(other)

    def __ge__(self, other):
        """Implements >= operator."""
        return abs(self) >= abs(other)
