import sys
from writer import *

TERM = []
NETERM = []
WORDS = []
BOLT_START = '^'
BOLT_END = '$'
DOT = '.'
ROW = []
COLUMN = []
OPERATIONS = {'empty': '*', 'greather': '>', 'less': '<', 'equal': '='}
TABLE = {}
COL_WIDTH = {}
RULES = []


def main():
    reader()
    create_dict()
    find_eaqual()
    find_less()
    find_greather()
    print_const() 

    write_table(TABLE, sys.argv[2], ROW, COLUMN, COL_WIDTH)
    write_grammar_type('W', sys.argv[2])


def reader():
    global TERM, NETERM, WORDS, RULES
    with open(sys.argv[1], 'rb') as f:
        for line in f:
            s = line.decode()
            arr = s.split()
            if len(arr) > 1:
                term = arr[0]
                if not(term in TERM):
                    TERM.append(term)
                rule = arr[1]
                for e in rule:
                    if e.islower() and not(e in NETERM):
                        NETERM.append(e)
                RULES.append((term, rule))
            if len(arr) == 1:
                WORDS.append(arr[0])
    NETERM.sort()


def create_dict():
    global TERM, NETERM, ROW, TABLE, COLUMN, COL_WIDTH
    ROW = TERM + NETERM + [BOLT_START]
    COLUMN = TERM + NETERM + [BOLT_END]
    for e in COLUMN:
        COL_WIDTH[e] = 1
    for x in ROW:
        TABLE[x] = {}
        for y in COLUMN:
            TABLE[x][y] = DOT


def calculate_column_width():
    for x in ROW:
        for y in COLUMN:
            COL_WIDTH[y] = max(len(TABLE[x][y]), COL_WIDTH[y])


def print_table():
    global TABLE, ROW, COLUMN, COL_WIDTH
    print('  ', end='')
    for e in COLUMN:
        print(e.ljust(COL_WIDTH[e]+1, ' '), end='')
    print()
    for x in ROW:
        print(x + ' ', end='')
        for y in COLUMN:
            print(TABLE[x][y].ljust(COL_WIDTH[y]+1, ' '), end='')
        print()


def find_eaqual():
    for rule in RULES:
        s = rule[1]
        if len(s) < 2: 
            continue
        for e in range(len(s)-1):
            TABLE[s[e]][s[e+1]] = '='


def get_first(s):
    first = []
    for rule in RULES:
        term = rule[0]
        if term != s:
            continue
        first.append(rule[1][0])
    return first


def get_last(s):
    last = []
    for rule in RULES:
        term = rule[0]
        if term != s:
            continue
        last.append(rule[1][-1])
    return last


def set_relation(x, y, rel):
    if rel in TABLE[x][y]:
        return
    if TABLE[x][y] == DOT: 
        TABLE[x][y] = rel
    else:
        TABLE[x][y] += rel


def find_less():
    eq_rules = []
    for x in ROW:
        for y in COLUMN:
            if '=' in TABLE[x][y] and isNeterm(y):
                eq_rules.append((x, y))
    for e in eq_rules:
        first = get_first(e[1])
        for x in first:
            set_relation(e[0], x, '<')
    set_relation(BOLT_START, 'S', '<')    
    find_less_for_bolt('S')


def find_less_for_bolt(s):
    for e in RULES:
        l = e[0]
        r = e[1][0]
        if l == s:
            set_relation(BOLT_START, r, '<')
            if isNeterm(r):
                find_less_for_bolt(r)


def find_greather():
    eq_rules = []
    for x in ROW:
        for y in COLUMN:
            if '=' in TABLE[x][y] and (isNeterm(x) or isNeterm(x) and isNeterm(y)):
                eq_rules.append((x, y))
    for e in eq_rules:
        left = get_last(e[0])
        right = []
        if isNeterm(e[1]):
            right = get_first(e[1])
        else:
            right = [e[1]]
        for l in left:
            for r in right:
                set_relation(l, r, '>')
    set_relation('S', BOLT_END, '>')
    find_greather_for_bolt('S')
    

def find_greather_for_bolt(s):
   for e in RULES:
        l = e[0]
        r = e[1][-1]
        if l == s:
            set_relation(r, BOLT_END, '>')
            if isNeterm(r):
                find_greather_for_bolt(r)


def isNeterm(s):
    return s.isupper()


def isReversible():
    arr1 = []
    arr2 = set()
    for e in RULES:
        arr1.append(e[1])
        arr2.add(e[1])
    return len(arr1) == len(arr2)


def one_relation():
    max_rel = 1
    for e in COL_WIDTH:
        max_rel = max(max_rel, COL_WIDTH[e])
    return max_rel == 1


def print_const():
    calculate_column_width()  
    print('TERM: ', TERM)
    print('NETERM: ', NETERM)
    print('WORDS: ', WORDS)
    print('ROW: ', ROW)
    print('COLUMN: ', COLUMN)
    print('RULES: ', RULES)
    print('COL_WIDTH: ', COL_WIDTH)
    print('REVERSIBLE: ', isReversible())
    print('ONERELATIONS: ', one_relation())
    print()
    print_table()


if __name__ == '__main__':
    main()
