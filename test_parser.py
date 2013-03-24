
#from lis import Define, Plus, Variable, Const, Lambda
from lis import tokenize, parse_tokens

def test_tokenize():
    source0 = ['(define a 3)']
    tokens0 = list(tokenize(source0))
    source1 = ['(+ 10 25 0)']
    tokens1 = list(tokenize(source1))
    assert tokens0 == ['(', 'define', 'a', '3', ')']
    assert tokens1 == ['(', '+', '10', '25', '0', ')']


# get_list()

def test_parse_define():
    source = ['(define a 3)']
    tokens = list(tokenize(source))
    exp = parse_tokens(tokens)
    assert exp == ['define', 'a', 3]


def test_parse_add():
    source = ['(define a (+ 3 3))']
    tokens = list(tokenize(source))
    exp = parse_tokens(tokens)
    assert exp == ['define', 'a', ['+', 3, 3]]


def test_parse_lambda():
    source = ['(lambda (x y) (+ x y))']
    tokens = list(tokenize(source))
    exp = parse_tokens(tokens)
    assert exp == ['lambda', ['x', 'y'], ['+', 'x', 'y']]


def test_parse_define_lambda():
    source = ['(define add (lambda (x y) (+ x y)))']
    tokens = list(tokenize(source))
    exp = parse_tokens(tokens)
    assert exp == ['define', 'add', ['lambda', ['x', 'y'], ['+', 'x', 'y']]]
