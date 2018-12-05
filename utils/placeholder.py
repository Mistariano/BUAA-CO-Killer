import random


class Placeholder:
    def __init__(self, value=None, range=None, radix='dec'):
        """

        :param value:
        :param range:
        :param radix: 'dec' for signed decimal, 'hex' for unsigned hexadecimal
        """

        if not range:
            range = 'reg'
        assert range in ['reg', 3, 4, 5, 14, 15, 16, 32] or isinstance(range, list)
        assert radix.lower() in ['dec', 'hex']
        self.range = range
        self.value = value
        self.radix = radix.lower()

    def compile(self):
        if self.value:
            return self.value
        radix = self.radix
        return self._get_rand_hex() if radix == 'hex' else self._get_rand_dec()

    def _get_rand_hex(self):
        range = self.range
        h1 = random.choice('0123456789abcdef')
        h2 = random.choice('0123456789abcdef')
        h3 = random.choice('0123456789abcdef')
        h4 = random.choice('0123456789abcdef')
        if range == 16:
            return '0x' + h1 + h2 + h3 + h4
        else:
            h5 = random.choice('0123456789abcdef')
            h6 = random.choice('0123456789abcdef')
            h7 = random.choice('0123456789abcdef')
            h8 = random.choice('0123456789abcdef')
            return '0x' + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8

    def _get_rand_dec(self):
        range = self.range
        if range == 'reg':  # for registers
            res = random.randrange(1, 32)
            while res in [28, 29]:
                res = random.randrange(1, 32)  # 28 is gp and 29 is sp
            return res
        max_ = 2 ** range
        min_ = -2 ** range
        return random.randrange(min_, max_)
