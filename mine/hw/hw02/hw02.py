from operator import add, mul, sub

square = lambda x: x * x

identity = lambda x: x

triple = lambda x: 3 * x

increment = lambda x: x + 1


HW_SOURCE_FILE = __file__


def product(n, term):
    """Return the product of the first n terms in a sequence.
    n -- a positive integer
    term -- a function that takes one argument to produce the term

    >>> product(3, identity)  # 1 * 2 * 3
    6
    >>> product(5, identity)  # 1 * 2 * 3 * 4 * 5
    120
    >>> product(3, square)    # 1^2 * 2^2 * 3^2
    36
    >>> product(5, square)    # 1^2 * 2^2 * 3^2 * 4^2 * 5^2
    14400
    >>> product(3, increment) # (1+1) * (2+1) * (3+1)
    24
    >>> product(3, triple)    # 1*3 * 2*3 * 3*3
    162
    """
    
    i,ret=1,1
    while i<=n:
        ret*=term(i)
        i+=1
    return ret



def square(x):
    return x * x


def accumulate(combiner, base, n, term):
    """Return the result of combining the first n terms in a sequence and base.
    The terms to be combined are term(1), term(2), ..., term(n).  combiner is a
    two-argument commutative function.

    >>> accumulate(add, 0, 5, identity)  # 0 + 1 + 2 + 3 + 4 + 5
    15
    >>> accumulate(add, 11, 5, identity) # 11 + 1 + 2 + 3 + 4 + 5
    26
    >>> accumulate(add, 11, 0, identity) # 11
    11
    >>> accumulate(add, 11, 3, square)   # 11 + 1^2 + 2^2 + 3^2
    25
    >>> accumulate(mul, 2, 3, square)    # 2 * 1^2 * 2^2 * 3^2
    72
    >>> accumulate(lambda x, y: x + y + 1, 2, 3, square)
    19
    >>> accumulate(lambda x, y: 2 * (x + y), 2, 3, square)
    58
    >>> accumulate(lambda x, y: (x + y) % 17, 19, 20, square)
    16
    """
    i=1
    while i<=n:
        base=combiner(base,term(i))
        i+=1
    return base


def summation_using_accumulate(n, term):
    """Returns the sum of term(1) + ... + term(n). The implementation
    uses accumulate.

    >>> summation_using_accumulate(5, square)
    55
    >>> summation_using_accumulate(5, triple)
    45
    >>> from construct_check import check
    >>> # ban iteration and recursion
    >>> check(HW_SOURCE_FILE, 'summation_using_accumulate',
    ...       ['Recursion', 'For', 'While'])
    True
    """
    return accumulate(add,0,n,term)


def product_using_accumulate(n, term):
    """An implementation of product using accumulate.

    >>> product_using_accumulate(4, square)
    576
    >>> product_using_accumulate(6, triple)
    524880
    >>> from construct_check import check
    >>> # ban iteration and recursion
    >>> check(HW_SOURCE_FILE, 'product_using_accumulate',
    ...       ['Recursion', 'For', 'While'])
    True
    """
    return accumulate(mul,1,n,term)


def compose1(func1, func2):
    """Return a function f, such that f(x) = func1(func2(x))."""
    def f(x):
        return func1(func2(x))
    return f


def make_repeater(func, n):
    """Return the function that computes the nth application of func.

    >>> add_three = make_repeater(increment, 3)
    >>> add_three(5)
    8
    >>> make_repeater(triple, 5)(1) # 3 * 3 * 3 * 3 * 3 * 1
    243
    >>> make_repeater(square, 2)(5) # square(square(5))
    625
    >>> make_repeater(square, 4)(5) # square(square(square(square(5))))
    152587890625
    >>> make_repeater(square, 0)(5) # Yes, it makes sense to apply the function zero times!
    5
    """
    #这是注释
    if n==0:
        return identity
    else:
        ret=identity
        while n>0:
            n-=1
            ret=compose1(func,ret)
        return ret



def zero(f):
    return lambda x: x


def successor(n):
    return lambda f: \
        lambda x: \
            f(n(f)(x))
    # f:f(x)=f(n(f)(x))
    #如果n是zero,返回的就是lambda f: lambda x:f(x)
    # successor(zero)(f)是一个函数，输入x，返回f(x)
    # successor(zero)是一个函数，输入一个函数f，返回一个函数“输入x，返回f(x)”
    # successor(successor(zero))是一个函数，输入一个函数f，返回一个函数：“输入x，返回f(one(f)(x))”
    # (这个 f(one(f)(x)) 对x应用函数“输入x，返回f(x)”，再将其套到f里面，即 f(f(x)) 。)
    # 所以 successor(successor(zero)) 最终的效果就是输入f，返回一个函数：“输入f，返回f(f(x))”
    
def one(f):
    """Church numeral 1: same as successor(zero)"""
    def fx(x):
        return f(x)
    return fx
        


def two(f):
    """Church numeral 2: same as successor(successor(zero))"""
    def ff(x):
        return f(f(x))
    return ff


three = successor(two)


def church_to_int(n):
    """Convert the Church numeral n to a Python integer.

    >>> church_to_int(zero)
    0
    >>> church_to_int(one)
    1
    >>> church_to_int(two)
    2
    >>> church_to_int(three)
    3
    """

    def add1(x):
        return x+1
    add_n = n(add1)
    return add_n(0)
    #n(add1)这个函数，其实就是把add()套用n遍。
    

def add_church(m, n):
    """Return the Church numeral for m + n, for Church numerals m and n.

    >>> church_to_int(add_church(two, three))
    5
    """
    # m对应数M，n对应数N
    # m(f)相当于把f套用M遍
    i=0
    while i<church_to_int(n):
        m=successor(m) #步进
        i+=1
    return m
    


def mul_church(m, n):
    """Return the Church numeral for m * n, for Church numerals m and n.

    >>> four = successor(three)
    >>> church_to_int(mul_church(two, three))
    6
    >>> church_to_int(mul_church(three, four))
    12
    """
    def product(f):
        return m(n(f))
    return product


def pow_church(m, n):
    """Return the Church numeral m ** n, for Church numerals m and n.

    >>> church_to_int(pow_church(two, three))
    8
    >>> church_to_int(pow_church(three, two))
    9
    """
    i=0
    base=one
    while i<church_to_int(n): #即使n是zero也是能ac的
        i+=1
        base=mul_church(base,m)
    return base

