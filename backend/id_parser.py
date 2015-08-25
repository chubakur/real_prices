import re

with open('UPDATE_PRICES.log') as _f:
    pattern = re.compile('u\'queryId\': u\'(.{36})\'')
    text = _f.read()
    ids = pattern.findall(text)
    hist = dict()
    for i in ids:
        if i in hist:
            hist[i] += 1
        else:
            hist[i] = 1
    for k, v in hist.items():
        if v != 7:
            print k, v
