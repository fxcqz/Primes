from functools import total_ordering


@total_ordering
class CustomComplex(complex):
    def __eq__(self, other):
        return abs(self) == abs(other) \
                and self.real == other.real \
                and self.imag == other.imag

    def __lt__(self, other):
        return abs(self) < abs(other)

    def __le__(self, other):
        return abs(self) <= abs(other)

    def __gt__(self, other):
        return abs(self) > abs(other)

    def __ge__(self, other):
        return abs(self) >= abs(other)
