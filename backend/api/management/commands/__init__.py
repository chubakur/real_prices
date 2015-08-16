import re


digits = re.compile('\d+')


def str_to_number(n):
    try:
        return float(n)
    except ValueError:
        if not n:
            return None
        return float(''.join(digits.findall(n)))
