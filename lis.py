#! /usr/bin/env python

from collections import namedtuple

# LEXER ================================

def split_word(word):
    current = ''
    for c in word:
        if c == '(' or c == ')':
            if current != '':
                yield current
            yield c
            current = ''
        else:
            current = current + c
    if current != '':
        yield current

def tokenize(lines):
    for line in lines:
        for word in line.split():
            for s in split_word(word):
                yield s


# KEYWORDS and TYPE CONVERSION =========

def atom(token):
    # try to convert token to int or float
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token



# PARSER ===============================

def parse_tokens(tokens):
    if tokens == []:
        raise Error('EOF')
    tok = tokens.pop(0)
    if tok == '(':
        new_list = []
        while tokens[0] != ')':
            new_list.append(parse_tokens(tokens))
        tokens.pop(0)
        return new_list
    elif tok == ')':
        raise Error('Unexpected ")"')
    else:
        return atom(tok)


# EVALUATOR ============================

def eval_in_env(exp, env):
    if isinstance(exp, int):
        return exp
    elif isinstance(exp, float):
        return exp
    elif exp[0] == '+': # may not want a global "+" but it's useful for testing
        args = exp[1:]
        total = 0
        for a in args:
            total += eval_in_env(a, env)
        return total
    elif exp[0] == '<':
        (_, x, y) = exp
        if x < y:
            return True
        else:
            return False
    elif exp[0] == 'if':
        (_, pred, exp_true, exp_false) = exp
        if eval_in_env(pred, env):
            return eval_in_env(exp_true, env)
        else:
            return eval_in_env(exp_false, env)


# RUN INTERPRETER ======================

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('source', nargs = 1, help='source text file')
    args = parser.parse_args()

    try:
        source = open(args.source[0], 'r')
        tokens = list(tokenize(source))
        for t in tokens:
            print(t)
        source.close()
    except:
        print('Invalid source file')
