import sys

def write_table(table, filename, rows, columns, col_width):
    result = '  '
    for e in columns:
        result += e.ljust(col_width[e]+1, ' ')
    result += '\r\n'
    for x in rows:
        result += x + ' '
        for y in columns:
            result += table[x][y].ljust(col_width[y]+1, ' ')
        result += '\r\n'
    with open(filename, 'wb') as f:
        f.write(result.encode())


def write_grammar_type(type_g, filename):
    with open(filename, 'ab') as f:
        f.write(type_g.encode())

