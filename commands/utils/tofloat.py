import re
import math

pattern = r'[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ? [π]?'


class ToFloat(float):

    def __new__(cls, number: str):
        def r(x): return x.replace("pi", "π") if "pi" != x != "π" else "1π"
        number = "/".join(map(r, number.split("/")))

        rx1 = re.compile(pattern, re.VERBOSE)
        rx2 = re.compile(f"{pattern}/{pattern}", re.VERBOSE)

        return super().__new__(cls, cls.check(rx1, rx2, number))

    @staticmethod
    def check(rx1, rx2, number):
        for p in rx1, rx2:
            if "".join(p.findall(number)) == number:
                return eval("/".join(map(lambda x: f"({x})", number.replace("π", f" *{math.pi}").split("/"))))


if __name__ == "__main__":
    print(ToFloat("1/3"))      # 0.3333333333333333#
    print(ToFloat("4.1/2.4"))  # 1.7083333333333333
    print(ToFloat("1"))        # 1.0
    print(ToFloat("2.5"))      # 2.5
    print(ToFloat("2pi"))      # 6.283185307179586
    print(ToFloat("2π/pi"))    # 2.0
    print(ToFloat("pi"))       # 3.141592653589793
