import json
import os
from pathlib import Path

import jsonpickle
from kivy.metrics import dp

def isjson(f=None):
    try:
        ret = json.load(open(f, 'r'))
        return ret
    except ValueError:
        return None


def save(fname=None, root=None, tosave=None):
    if not os.path.exists(fname):
        Path(fname).touch()
    if os.path.isfile(fname):
        with open(fname, 'w') as file:
            line = []
            for i in root.children:
                if type(i) is tosave:
                    line.append(i._getstate())
            file.write(jsonpickle.encode(line))


def load(fname=None, root=None, toload=None):
    with open(fname, 'r') as file:
        zz = jsonpickle.decode(file.read())
        for i in zz:
            w = toload(i)
            w.size = (dp(w.size[0]), dp(w.size[1]))
            w.pos = (dp(w.pos[0]), dp(w.pos[1]))
            root.add_widget(toload(i))
