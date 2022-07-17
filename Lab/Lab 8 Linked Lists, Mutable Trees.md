# Lab 8: Linked Lists, Mutable Trees

# Topics

## Linked Lists

We've learned that a Python list is one way to store sequential values. Another type of list is a linked list. A Python list stores all of its elements in a single object, and each element can be accessed by using its index. A linked list, on the other hand, is a recursive object that only stores two things: its first value and a reference to the rest of the list, which is another linked list.

We can implement a class, `Link`, that represents a linked list object.  Each instance of `Link` has two instance attributes, `first` and `rest`.

```
class Link:
    """A linked list.

    >>> s = Link(1)
    >>> s.first
    1
    >>> s.rest is Link.empty
    True
    >>> s = Link(2, Link(3, Link(4)))
    >>> s.first = 5
    >>> s.rest.first = 6
    >>> s.rest.rest = Link.empty
    >>> s                                    # Displays the contents of repr(s)
    Link(5, Link(6))
    >>> s.rest = Link(7, Link(Link(8, Link(9))))
    >>> s
    Link(5, Link(7, Link(Link(8, Link(9)))))
    >>> print(s)                             # Prints str(s)
    <5 7 <8 9>>
    """
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is not Link.empty:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        string = '<'
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + '>'
```

A valid linked list can be one of the following:

1. An empty linked list (`Link.empty`)
2. A `Link` object containing the first value of the linked list and a reference to the rest of the linked list

What makes a linked list recursive is that the `rest` attribute of a single `Link` instance is another linked list! In the big picture, each `Link` instance stores a single value of the list.  When multiple `Link`s are linked together through each instance's `rest` attribute, an entire sequence is formed.

> *Note*: This definition means that the `rest` attribute of any `Link` instance *must* be either `Link.empty` or another `Link` instance! This is enforced in `Link.__init__`, which raises an `AssertionError` if the value passed in for `rest` is neither of these things.

To check if a linked list is empty, compare it against the class attribute `Link.empty`. For example, the function below prints out whether or not the link it is handed is empty:

```
def test_empty(link):
    if link is Link.empty:
        print('This linked list is empty!')
    else:
        print('This linked list is not empty!')
```

## Mutable Trees

We define a tree to be a recursive data abstraction that has a `label` (the value stored in the root of the tree) and `branches` (a list of trees directly underneath the root).

Previously we implemented trees by using a functional data abstraction, with the `tree` constructor function and the `label` and `branches` selector functions. Now we implement trees by creating the `Tree` class. Here is part of the class included in the lab.

```
class Tree:
    """
    >>> t = Tree(3, [Tree(2, [Tree(5)]), Tree(4)])
    >>> t.label
    3
    >>> t.branches[0].label
    2
    >>> t.branches[1].is_leaf()
    True
    """
    def __init__(self, label, branches=[]):
        for b in branches:
            assert isinstance(b, Tree)
        self.label = label
        self.branches = list(branches)

    def is_leaf(self):
        return not self.branches
```

Even though this is a new implementation, everything we know about the functional tree data abstraction remains true.  That means that solving problems involving trees as objects uses the same techniques that we developed when first studying the functional tree data abstraction (e.g. we can still use recursion on the branches!).  **The main difference, aside from syntax, is that tree objects are mutable.**

Here is a summary of the differences between the tree data abstraction implemented as a functional abstraction vs. implemented as class:

| -                            | Tree constructor and selector functions                      | Tree class                                                   |
| ---------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Constructing a tree          | To construct a tree given a `label` and a list of `branches`, we call `tree(label, branches)` | To construct a tree object given a `label` and a list of `branches`, we call `Tree(label, branches)` (which calls the `Tree.__init__` method). |
| Label and branches           | To get the label or branches of a tree `t`, we call `label(t)` or `branches(t)` respectively | To get the label or branches of a tree `t`, we access the instance attributes `t.label` or `t.branches` respectively. |
| Mutability                   | The functional tree data abstraction is immutable because we cannot assign values to call expressions | The `label` and `branches` attributes of a `Tree` instance can be reassigned, mutating the tree. |
| Checking if a tree is a leaf | To check whether a tree `t` is a leaf, we call the convenience function `is_leaf(t)` | To check whether a tree `t` is a leaf, we call the bound method `t.is_leaf()`. This method can only be called on `Tree` objects. |

Implementing trees as a class gives us another advantage: we can specify how we want them to be output by the interpreter by implementing the `__repr__` and `__str__` methods.

Here is the `__repr__` method:

```
def __repr__(self):
    if self.branches:
        branch_str = ', ' + repr(self.branches)
    else:
        branch_str = ''
    return 'Tree({0}{1})'.format(self.label, branch_str)
```

With this implementation of `__repr__`, a `Tree` instance is displayed as the exact constructor call that created it:

```
>>> t = Tree(4, [Tree(3), Tree(5, [Tree(6)]), Tree(7)])
>>> t
Tree(4, [Tree(3), Tree(5, [Tree(6)]), Tree(7)])
>>> t.branches
[Tree(3), Tree(5, [Tree(6)]), Tree(7)]
>>> t.branches[0]
Tree(3)
>>> t.branches[1]
Tree(5, [Tree(6)])
```

Here is the `__str__` method. You do not need to understand how this function is implemented.

```
def __str__(self):
    def print_tree(t, indent=0):
        tree_str = '  ' * indent + str(t.label) + "\n"
        for b in t.branches:
            tree_str += print_tree(b, indent + 1)
        return tree_str
    return print_tree(self).rstrip()
```

With this implementation of `__str__`, we can pretty-print a `Tree` to see both its contents and structure:

```
>>> t = Tree(4, [Tree(3), Tree(5, [Tree(6)]), Tree(7)])
>>> print(t)
4
  3
  5
    6
  7
>>> print(t.branches[0])
3
>>> print(t.branches[1])
5
  6
```

# Required Questions

## Linked Lists

### Q1: WWPD: Linked Lists

Read over the `Link` class in `lab08.py`. Make sure you understand the doctests.

> Enter `Function` if you believe the answer is `<function ...>`, `Error` if it errors, and `Nothing` if nothing is displayed.
>
> If you get stuck, try drawing out the box-and-pointer diagram for the linked list on a piece of paper or loading the `Link` class into the interpreter with `python3 -i lab08.py`.

```
Link > Suite 1 > Case 1
(cases remaining: 3)

What would Python display? If you get stuck, try it out in the Python
interpreter!

>>> from lab09 import *
>>> link = Link(1000)
>>> link.first
? 1000
-- OK! --

>>> link.rest is Link.empty
? True
-- OK! --

>>> link = Link(1000, 2000)
? Nothing
-- Not quite. Try again! --

? Error
-- OK! --

>>> link = Link(1000, Link())
? Error
-- OK! --

---------------------------------------------------------------------
Link > Suite 1 > Case 2
(cases remaining: 2)

What would Python display? If you get stuck, try it out in the Python
interpreter!

>>> from lab09 import *
>>> link = Link(1, Link(2, Link(3)))
>>> link.first
? 1
-- OK! --

>>> link.rest.first
? 2
-- OK! --

>>> link.rest.rest.rest is Link.empty
? True
-- OK! --

>>> link.first = 9001
>>> link.first
? 9001
-- OK! --

>>> link.rest = link.rest.rest
>>> link.rest.first
? 3
-- OK! --

>>> link = Link(1)
>>> link.rest = link
>>> link.rest.rest.rest.rest.first
? 1
-- OK! --

>>> link = Link(2, Link(3, Link(4)))
>>> link2 = Link(1, link)
>>> link2.first
? 1
-- OK! --

>>> link2.rest.first
? 2
-- OK! --

---------------------------------------------------------------------
Link > Suite 1 > Case 3
(cases remaining: 1)

What would Python display? If you get stuck, try it out in the Python
interpreter!

>>> from lab09 import *
>>> link = Link(5, Link(6, Link(7)))
>>> link                  # Look at the __repr__ method of Link
?
-- Not quite. Try again! --

? Link(5, Link(6, Link(7)))
-- OK! --

>>> print(link)          # Look at the __str__ method of Link
? <5 6 7>
-- OK! --
```

### Q2: Convert Link

Write a function `convert_link` that takes in a linked list and returns the sequence as a Python list. You may assume that the input list is shallow; that is none of the elements is another linked list.

Try to find both an iterative and recursive solution for this problem!

```
def convert_link(link):
    """Takes a linked list and returns a Python list with the same elements.

    >>> link = Link(1, Link(2, Link(3, Link(4))))
    >>> convert_link(link)
    [1, 2, 3, 4]
    >>> convert_link(Link.empty)
    []
    """
    "*** YOUR CODE HERE ***"
```

#### Answer

```python
    result = []
    if link is not Link.empty:
        while link.rest is not Link.empty:
            result.append(link.first)
            link = link.rest
        result.append(link.first)
    return result
    # Recursion
    if link is Link.empty:
        return []
    else:
        return [link.first] + convert_link(link.rest)
```

#### Solution

```python
    # Recursive solution
    if link is Link.empty:
        return []
    return [link.first] + convert_link(link.rest)

    # Iterative solution
    def convert_link_iterative(link):
        result = []
        while link is not Link.empty:
            result.append(link.first)
            link = link.rest
        return result
```

## Trees

### Q3: WWPD: Trees

> Use Ok to test your knowledge with the following "What Would Python Display?" questions:
>
> Enter `Function` if you believe the answer is `<function ...>`, `Error` if it errors, and `Nothing` if nothing is displayed. Recall that `Tree` instances will be [displayed the same way they are constructed](https://cs61a.org/lab/lab08/#mutable-trees).

```
---------------------------------------------------------------------
Trees > Suite 1 > Case 1
(cases remaining: 1)

What would Python display? If you get stuck, try it out in the Python
interpreter!

>>> t = Tree(1, Tree(2)) # Enter Function if you believe the answer is <function ...>, Error if it errors, and Nothing if nothing is displayed.
? Nothing
-- Not quite. Try again! --

? Error
-- OK! --

>>> t = Tree(1, [Tree(2)])
>>> t.label
? 1
-- OK! --

>>> t.branches[0]
? Tree(2)
-- OK! --

>>> t.branches[0].label
? 2
-- OK! --

>>> t.label = t.branches[0].label
>>> t
? Tree(2, [Tree(2)])
-- OK! --

>>> t.branches.append(Tree(4, [Tree(8)]))
>>> len(t.branches)
? 2
-- OK! --

>>> t.branches[0]
? Tree(2)
-- OK! --

>>> t.branches[1]
? Tree(4, [Tree(8)])
-- OK! --
```

### Q4: Square

Write a function `label_squarer` that mutates a `Tree` with numerical labels so that each label is squared.

```
def label_squarer(t):
    """Mutates a Tree t by squaring all its elements.

    >>> t = Tree(1, [Tree(3, [Tree(5)]), Tree(7)])
    >>> label_squarer(t)
    >>> t
    Tree(1, [Tree(9, [Tree(25)]), Tree(49)])
    """
    "*** YOUR CODE HERE ***"
```

#### Answer

```python
    t.label = t.label ** 2
    for b in t.branches:	# Solution: for subtree in t.branches
        label_squarer(b)
```

### Q5: Cumulative Mul

Write a function `cumulative_mul` that mutates the Tree `t` so that each node's label becomes the product of its label and all labels in the subtrees rooted at the node.

```
def cumulative_mul(t):
    """Mutates t so that each node's label becomes the product of all labels in
    the corresponding subtree rooted at t.

    >>> t = Tree(1, [Tree(3, [Tree(5)]), Tree(7)])
    >>> cumulative_mul(t)
    >>> t
    Tree(105, [Tree(15, [Tree(5)]), Tree(7)])
    """
    "*** YOUR CODE HERE ***"
```

#### Answer

```python
    for subtree in t.branches:
        if subtree.is_leaf():
            t.label *= subtree.label
        else:
            cumulative_mul(subtree)
            t.label *= subtree.label
            
    # Simplify
    for subtree in t.branches:
        cumulative_mul(subtree)
        t.label *= subtree.label
```

#### Solution

```python
    for b in t.branches:
        cumulative_mul(b)
    total = t.label
    for b in t.branches:
        total *= b.label
    t.label = total
```

### Q6: Add Leaves

Implement `add_d_leaves`, a function that takes in a `Tree` instance `t` and a number `v`.

We define the depth of a node in `t` to be the number of edges from the root to that node. The depth of root is therefore 0.

For each node in the tree, you should add `d` leaves to it, where `d` is the depth of the node. Every added leaf should have a label of `v`. If the node at this depth has existing branches, you should add these leaves to the end of that list of branches.

For example, you should be adding 1 leaf with label `v` to each node at depth 1, 2 leaves to each node at depth 2, and so on.

Here is an example of a tree `t`(shown on the left) and the result after `add_d_leaves` is applied with `v` as 5.

![image-20211209232447686](https://cdn.jsdelivr.net/gh/Christina0031/article_imgs/imgs/image-20211209232447686.png)

> **Hint:** Use a helper function to keep track of the depth!

```
def add_d_leaves(t, v):
    """Add d leaves containing v to each node at every depth d.

    >>> t_one_to_four = Tree(1, [Tree(2), Tree(3, [Tree(4)])])
    >>> print(t_one_to_four)
    1
      2
      3
        4
    >>> add_d_leaves(t_one_to_four, 5)
    >>> print(t_one_to_four)
    1
      2
        5
      3
        4
          5
          5
        5

    >>> t1 = Tree(1, [Tree(3)])
    >>> add_d_leaves(t1, 4)
    >>> t1
    Tree(1, [Tree(3, [Tree(4)])])
    >>> t2 = Tree(2, [Tree(5), Tree(6)])
    >>> t3 = Tree(3, [t1, Tree(0), t2])
    >>> print(t3)
    3
      1
        3
          4
      0
      2
        5
        6
    >>> add_d_leaves(t3, 10)
    >>> print(t3)
    3
      1
        3
          4
            10
            10
            10
          10
          10
        10
      0
        10
      2
        5
          10
          10
        6
          10
          10
        10
    """
    "*** YOUR CODE HERE ***"
```

#### Answer

```python
    def helper(t, d):
        for b in t.branches:
            helper(b, d + 1)
            for _ in range(d):
                b.branches.append(Tree(v))
    return helper(t, 1)	# Don't return 
```

#### Solution

```python
    def add_leaves(t, d):
        for b in t.branches:
            add_leaves(b, d + 1)
        t.branches.extend([Tree(v) for _ in range(d)])
    add_leaves(t, 0)
```

A first thought is to recursively call `add_d_leaves` on each branch to add the leaves to the branches. However, notice that each recursive call would need to know what the current depth is in order to add that many leaves. We could try initializing a variable within the body of the function, but by now we know that in order to keep track of changing values across recursive calls we should use a helper function!

The helper function should take in a tree and a depth value, and we will define it as a function that adds `d` leaves to the branches of the root node, `d + 1` leaves to the branches of each of the root node's branches, and so on:

```
def add_leaves(t, d):
    """Adds a number of leaves to each node in t equivalent to the depth of
    the node, assuming that the root node is at depth d, the children of
    the root node are at depth d + 1, and so on."""
    ...
```

We don't need a parameter for `v` since that value won't change and we can access it from the parent frame. With this function defined as such, we can call `add_leaves` with arguments `t` and 0 to add leaves starting at depth 0.

```
def add_d_leaves(t, v):
    def add_leaves(t, d):
        """Adds a number of leaves to each node in t equivalent to the depth of
        the node, assuming that the root node is at depth d, the children of
        the root node are at depth d + 1, and so on."""
        ...
    add_leaves(t, 0)
```

Inside the helper function, we can now call it recursively on each branch. Each node's branch is one depth level greater than the node itself, so we should update `d` to `d + 1`:

```
def add_leaves(t, d):
    for b in t.branches:
        add_leaves(b, d + 1)
    ...
```

Now that we've made these recursive calls, let's take a step back and look at our progress. Taking the leap of faith, we know that each recursive call should've successfully added the correct number of leaves at each node in each branch. That means that the only step left is to add the correct number of leaves to the current node!

The parameter `d` tells us how many leaves to add at this node. Since we are mutating `t` to add these leaves, we need to mutate the list of `t`'s branches. We know a few different ways to mutatively add elements to a list:`insert`, `append`, and `extend`. Which one makes most sense to use here? Well, we know that we have to add `d` elements to the end of `t.branches`. Index doesn't matter so we can rule out `insert`. `append` is good for adding a single element, while `extend` is useful for adding multiple elements contained in a list, so let's use `extend`!

The input to `extend` should be a list, so how do we create a list with the leaves that we need? The most concise way is with a list comprehension. To create each leaf, we call `Tree(v)`:

```
[Tree(v) for _ in range(d)]
```

Now, we just have to extend `t.branches` by this list:

```
def add_leaves(t, d):
    for b in t.branches:
        add_leaves(b, d + 1)
    t.branches.extend([Tree(v) for _ in range(d)])
```

Do we need an explicitly base case? Let's take a look at what happens when `t` is a leaf. In that case, `t.branches` would be an empty list, so we would not enter the `for` loop. Then, the function will extend `t.branches`, which is an empty list, by a list containing the new leaves. This is exactly the desired result, so no base case is needed!

# Optional Questions

### Q7: Every Other

Implement `every_other`, which takes a linked list `s`. It mutates `s` such that all of the odd-indexed elements (using 0-based indexing) are removed from the list. For example:

```
>>> s = Link('a', Link('b', Link('c', Link('d'))))
>>> every_other(s)
>>> s.first
'a'
>>> s.rest.first
'c'
>>> s.rest.rest is Link.empty
True
```

If `s` contains fewer than two elements, `s` remains unchanged.

> Do not return anything! `every_other` should mutate the original list.

```
def every_other(s):
    """Mutates a linked list so that all the odd-indiced elements are removed
    (using 0-based indexing).

    >>> s = Link(1, Link(2, Link(3, Link(4))))
    >>> every_other(s)
    >>> s
    Link(1, Link(3))
    >>> odd_length = Link(5, Link(3, Link(1)))
    >>> every_other(odd_length)
    >>> odd_length
    Link(5, Link(1))
    >>> singleton = Link(4)
    >>> every_other(singleton)
    >>> singleton
    Link(4)
    """
    "*** YOUR CODE HERE ***"
```

#### Answer

```python
    def remove(link, index):
        if link is Link.empty:
            return Link.empty
        else:
            link.rest = remove(link.rest, index + 1)
            if index % 2 == 1:
                return link.rest
            else:
                return link
    remove(s, 0)
```

#### Solution

```python
	if s is Link.empty or s.rest is Link.empty:
        return
    else:
        s.rest = s.rest.rest
        every_other(s.rest)
```

### Q8: Prune Small

Complete the function `prune_small` that takes in a `Tree` `t` and a number `n` and prunes `t` mutatively. If `t` or any of its branches has more than `n` branches, the `n` branches with the smallest labels should be kept and any other branches should be *pruned*, or removed, from the tree.

```
def prune_small(t, n):
    """Prune the tree mutatively, keeping only the n branches
    of each node with the smallest label.

    >>> t1 = Tree(6)
    >>> prune_small(t1, 2)
    >>> t1
    Tree(6)
    >>> t2 = Tree(6, [Tree(3), Tree(4)])
    >>> prune_small(t2, 1)
    >>> t2
    Tree(6, [Tree(3)])
    >>> t3 = Tree(6, [Tree(1), Tree(3, [Tree(1), Tree(2), Tree(3)]), Tree(5, [Tree(3), Tree(4)])])
    >>> prune_small(t3, 2)
    >>> t3
    Tree(6, [Tree(1), Tree(3, [Tree(1), Tree(2)])])
    """
    while ___________________________:
        largest = max(_______________, key=____________________)
        _________________________
    for __ in _____________:
        ___________________
```

#### Answer

```python
    while len(t.branches) > n:
        largest = max(t.branches, key=lambda x: x.label)
        t.branches.remove(largest)
    for b in t.branches:
        prune_small(b, n)
```

### Fa20 Q6: Reverse Other

Write a function `reverse_other` that mutates the tree such that **labels** on *every other* (odd-depth) level are reversed. For example, `Tree(1,[Tree(2, [Tree(4)]), Tree(3)])` becomes `Tree(1,[Tree(3, [Tree(4)]), Tree(2)])`. Notice that the nodes themselves are *not* reversed; only the labels are.

```
def reverse_other(t):
    """Mutates the tree such that nodes on every other (odd-depth) level
    have the labels of their branches all reversed.

    >>> t = Tree(1, [Tree(2), Tree(3), Tree(4)])
    >>> reverse_other(t)
    >>> t
    Tree(1, [Tree(4), Tree(3), Tree(2)])
    >>> t = Tree(1, [Tree(2, [Tree(3, [Tree(4), Tree(5)]), Tree(6, [Tree(7)])]), Tree(8)])
    >>> reverse_other(t)
    >>> t
    Tree(1, [Tree(8, [Tree(3, [Tree(5), Tree(4)]), Tree(6, [Tree(7)])]), Tree(2)])
    """
    "*** YOUR CODE HERE ***"
```

![image-20211210153831848](https://cdn.jsdelivr.net/gh/Christina0031/article_imgs/imgs/image-20211210153831848.png)

![image-20211210154221513](https://cdn.jsdelivr.net/gh/Christina0031/article_imgs/imgs/image-20211210154221513.png)

### Fall 2018 Midterm 2 Question 6

![image-20211210161616623](https://cdn.jsdelivr.net/gh/Christina0031/article_imgs/imgs/image-20211210161616623.png)

<img src="https://cdn.jsdelivr.net/gh/Christina0031/article_imgs/imgs/image-20211210161628243.png" alt="image-20211210161628243" style="zoom: 50%;" />

