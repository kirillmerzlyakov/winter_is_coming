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
AKSIOMA = ''


def main():
    reader()
    create_dict()
    find_eaqual()
    find_less()
    find_greather()
    print_const() 

    write_table(TABLE, sys.argv[2], ROW, COLUMN, COL_WIDTH)
    write_grammar_type('W', sys.argv[2])
    # print(is_cycle())


def reader():
    global TERM, NETERM, WORDS, RULES, AKSIOMA
    with open(sys.argv[1], 'rb') as f:
        for line in f:
            s = line.decode()
            arr = s.split()
            if len(arr) > 1:
                term = arr[0]
                if not(term in NETERM):
                    NETERM.append(term)
                rule = arr[1]
                for e in rule:
                    if e.islower() and not(e in TERM):
                        TERM.append(e)
                RULES.append((term, rule))
            if len(arr) == 1:
                WORDS.append(arr[0])
    AKSIOMA = NETERM[0]
    TERM.sort()


def create_dict():
    global TERM, NETERM, ROW, TABLE, COLUMN, COL_WIDTH
    ROW = NETERM + TERM + [BOLT_START]
    COLUMN = NETERM + TERM + [BOLT_END]
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
        TABLE[x][y] = rel + TABLE[x][y]


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
    set_relation(BOLT_START, AKSIOMA, '<')    
    find_less_for_bolt(AKSIOMA, set(AKSIOMA))


def find_less_for_bolt(s, used):
    for e in RULES:
        l = e[0]
        r = e[1][0]
        if l == s:
            set_relation(BOLT_START, r, '<')
            if isNeterm(r):
                print(used)
                if r in used:
                    return
                used.add(r)
                find_less_for_bolt(r, used)


def find_greather():
    eq_rules = []
    for x in ROW:
        for y in COLUMN:
            if '=' in TABLE[x][y] and isNeterm(x):
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
    set_relation(AKSIOMA, BOLT_END, '>')
    find_greather_for_bolt(AKSIOMA, set(AKSIOMA))
    

def find_greather_for_bolt(s, used):
    for e in RULES:
        l = e[0]
        r = e[1][-1]
        if l == s:
            set_relation(r, BOLT_END, '>')
            if isNeterm(r):
                if r in used:
                    return
                used.add(r)
                find_greather_for_bolt(r, used)


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

def is_cycle():
    cur_not_terminal = 'S'
    stack = [cur_not_terminal]
    used = {cur_not_terminal}
    is_cycle = False

    while stack and is_cycle == False:
        cur = stack.pop()
        rules = [rule[1] for rule in filter(
            lambda pair:pair[0] == cur_not_terminal 
            and len(pair[1]) == 1 
            and isNeterm(pair[1]), RULES)
            ]
        for not_term in rules:
            if not_term not in used:
                used.add(not_term)
                stack.append(not_term)
            else:
                is_cycle = True
                break
    return is_cycle

def has_cell_all_relations():
    for x in TABLE:
        for y in TABLE[x]:
            if len(TABLE[x][y]) == 3:
                return True 
    return False


def does_weak_condition_performed(left_nt, right_nt):
    substr_after_left_nt = set()
    for rule in RULES:
        if left_nt in rule[1]:
            substr_after_left_nt.add(rule[1][rule[1].find(left_nt):])
    right_nt_rules = [rule[1] for rule in filter(lambda pair: pair[0] == right_nt, RULES)]
    if substr_after_left_nt.intersection(right_nt_rules):
        return False
    return True


def is_simple_precedence():
    return not is_cycle() and isReversible() and one_relation()


def is_weak_precedence():
    if is_cycle():
        return False
    if not isReversible():
        return False
    if has_cell_all_relations():
        return False
    
    relation_le_with_rigth_not_term = []
    for x in TABLE:
        for y in TABLE[x]:
            if '<' in TABLE[x][y] and '=' in TABLE[x][y] and isNeterm(y):
                relation_le_with_rigth_not_term.append((x, y))
    
    is_weak = True

    for pair in relation_le_with_rigth_not_term:
        is_weak = is_weak and does_weak_condition_performed(*pair)
    return is_weak
    

def get_type_of_grammer():
    if is_simple_precedence():
        return 'S'
    if is_weak_precedence():
        return 'W'
    return 'N'


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
    print('AKSIOMA: ', AKSIOMA)
    print()
    print_table()
    print(get_type_of_grammer())


if __name__ == '__main__':
    main()
