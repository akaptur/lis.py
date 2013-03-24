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

def programize(tokens):
    return ['(', 'begin'] + tokens + [')']

def parse_tokens(tokens):
    if tokens == []:
        raise Exception('EOF')
    tok = tokens.pop(0)
    if tok == '(':
        new_list = []
        while tokens[0] != ')':
            new_list.append(parse_tokens(tokens))
        tokens.pop(0)
        return new_list
    elif tok == ')':
        raise Exception('Unexpected ")"')
    else:
        return atom(tok)


# EVALUATOR ============================

def lookup(name, env):
    for n, v in env:
        if n == name:
            return v
    raise Exception('unknown variable "{}"'.format(name))

def eval_in_env(exp, env):
    if exp == 'null':
        return []
    elif isinstance(exp, str):
        return lookup(exp, env)
    if not isinstance(exp, list):
        return exp
    # FUNCTIONS
    elif exp[0] == '+':
        params = exp[1:]
        total = 0
        for p in params:
            total += eval_in_env(p, env)
        return total
    elif exp[0] == '*':
        params = exp[1:]
        total = 1
        for p in params:
            total *= eval_in_env(p, env)
        return total
    elif exp[0] == '-':
        params = exp[1:]
        # TODO: FIX THIS - only takes two arguments
        print(params[0], params[1])
        return eval_in_env(params[0], env) - eval_in_env(params[1], env)
    elif exp[0] == '/':
        params = exp[1:]
        # TODO: FIX THIS - only takes two arguments
        print(params[0], params[1])
        return eval_in_env(params[0], env) / eval_in_env(params[1], env)
    elif exp[0] == '=':
        (_, x, y) = exp
        return eval_in_env(x, env) == eval_in_env(y, env)
    elif exp[0] == '<':
        (_, x, y) = exp
        return eval_in_env(x,env) < eval_in_env(y,env)
    elif exp[0] == '>':
        (_, x, y) = exp
        return eval_in_env(x,env) > eval_in_env(y,env)
    # CORE LANGUAGE
    elif exp[0] == 'if':
        (_, pred, exp_true, exp_false) = exp
        if eval_in_env(pred, env):
            return eval_in_env(exp_true, env)
        else:
            return eval_in_env(exp_false, env)
    elif exp[0] == 'let':
        (_, pairs, e) = exp
        new_env = env
        for p in pairs:
            name, val = p[0], p[1]
            new_env = [(name, eval_in_env(val, env))] + new_env
        return eval_in_env(e, new_env)
    elif exp[0] == 'define':
        # just a simple mofification of the current env
        (_, name, e) = exp
        env.insert(0, (name, eval_in_env(e, env)))
    elif exp[0] == 'lambda':
        # needs to return a closure
        #(_, params, body) = exp
        return ['closure', exp, list(env)] # ensure the env won't be mutated
    elif exp[0] == 'display':
        print(eval_in_env(exp[1], env))
    # LISTS
    elif exp[0] == 'cons':
        (_, a, lst) = exp
        return [eval_in_env(a, env)] + eval_in_env(lst, env)
    elif exp[0] == 'car':
        (_, lst) = exp
        return eval_in_env(lst, env)[0]
    elif exp[0] == 'cdr':
        (_, lst) = exp
        return eval_in_env(lst, env)[1:]
    elif exp[0] == 'list':
        return [eval_in_env(a, env) for a in exp[1:]]
    elif exp[0] == 'null?':
        return eval_in_env(exp[1], env) == []
    # FUNCTION EVALUATION
    else:
        # first element should be a variable pointing to a function
        # or a lambda expression
        func = exp[0]
        closure = eval_in_env(func, env)
        args = exp[1:]
        args = [eval_in_env(a, env) for a in args]
        (_, f, closure_env) = closure
        (_, params, body) = f
        if isinstance(func, str):
            new_env = [(func, closure)] + list(zip(params, args)) + closure_env
        else:
            new_env = list(zip(params, args)) + closure_env
        return eval_in_env(body, new_env)


def eval_loop(program):
    env = []
    for exp in program:
        if exp == 'begin':
            continue
        else:
            eval_in_env(exp, env)


# RUN INTERPRETER ======================

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('source', nargs = 1, help='source text file')
    args = parser.parse_args()

    try:
        source = open(args.source[0], 'r')
        tokens = list(tokenize(source))
        source.close()
        program = parse_tokens(programize(tokens))
    except:
        print('Invalid source file')
    eval_loop(program)
