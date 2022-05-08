import re
from fractions import Fraction

pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'


class ToFloat(float):

    def __new__(cls, number: str):
        rx1 = re.compile(pattern, re.VERBOSE)
        rx2 = re.compile(f"{pattern}/{pattern}", re.VERBOSE)

        if "".join(rx1.findall(number)) == number or "".join(rx2.findall(number)) == number:
            return super().__new__(cls, Fraction(eval(number)).limit_denominator())


if __name__ == "__main__":
    print(ToFloat("1/3"))      # 0.3333333333333333
    print(ToFloat("4.1/2.4"))  # 1.7083333333333333
    print(ToFloat("1"))        # 1.0
    print(ToFloat("2.5"))      # 2.5
