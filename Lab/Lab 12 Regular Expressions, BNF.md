# Lab 12: Regular Expressions, BNF

# Topics

Consult this section if you need a refresher on the material for this lab. It's okay to skip directly to the questions and refer back here  should you get stuck.

## Regular Expressions

Regular expressions are a way to describe sets of strings that meet  certain criteria, and are incredibly useful for pattern matching.

The simplest regular expression is one that matches a sequence of characters, like `aardvark` to match any "aardvark" substrings in a string.

However, you typically want to look for more interesting patterns. We recommend using an online tool like [regexr.com](https://regexr.com/) for trying out patterns, since you'll get instant feedback on the match results.

### Character classes

A character class makes it possible to search for any one of a set of characters. You can specify the set or use pre-defined sets.

| Class    | Description                                                  |
| -------- | ------------------------------------------------------------ |
| `[abc]`  | Matches a, b, or c                                           |
| `[a-z]`  | Matches any character between a and z                        |
| `[^A-Z]` | Matches any character that is not between A and Z.           |
| `\w`     | Matches any "word" character. Equivalent to `[A-Za-z0-9_]`   |
| `\d`     | Matches any digit. Equivalent to `[0-9]`.                    |
| `[0-9]`  | Matches a single digit in the range 0 - 9. Equivalent to `\d` |
| `\s`     | Matches any whitespace character (spaces, tabs, line breaks). |
| `.`      | Matches any character besides new line.                      |

Character classes can be combined, like in `[a-zA-Z0-9]`.

### Combining patterns

There are multiple ways to combine patterns together in regular expressions.

| Combination | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| `AB`        | A match for A followed immediately by one for B.  Example: `x[.,]y` matches "x.y" or "x,y" |
| `A|B`       | Matches either A or B.  Example: `\d+|Inf` matches either a sequence containing 1 or more digits **or** "Inf" |

A pattern can be followed by one of these quantifiers to specify how many instances of the pattern can occur.

| Quantifier | Description                                                  |
| ---------- | ------------------------------------------------------------ |
| `*`        | 0 or more occurrences of the preceding pattern.  Example: `[a-z]*` matches any sequence of lower-case letters or the empty string. |
| `+`        | 1 or more occurrences of the preceding pattern.  Example: `\d+` matches any non-empty sequence of digits. |
| `?`        | 0 or 1 occurrences of the preceding pattern.  Example: `[-+]?` matches an optional sign. |
| `{1,3}`    | Matches the specified quantity of the preceding pattern. {1,3}  will match from 1 to 3 instances. {3} will match exactly 3 instances.  {3,} will match 3 or more instances.   Example: `\d{5,6}` matches either 5 or 6 digit numbers. |

### Groups

Parentheses are used similarly as in arithmetic expressions, to create groups. For example, `(Mahna)+` matches strings with 1 or more "Mahna", like "MahnaMahna". Without the parentheses, `Mahna+` would match strings with "Mahn" followed by 1 or more "a" characters, like "Mahnaaaa".

### Anchors

- `^`
  - Matches the beginning of a string.  Example: `^(I|You)` matches I or You at the start of a string.
- `$`
  - Normally matches the empty string at the end of a string or just before a newline at the end of a string.  Example: `(\.edu|\.org|\.com)$` matches .edu, .org, or .com at the end of a string.
- `\b`
  - Matches a "word boundary", the beginning or end of a word.  Example: `s\b` matches s characters at the end of words.

### Special characters

The following special characters are used above to denote types of patterns:

```
\ ( ) [ ] { } + * ? | $ ^ .
```

That means if you actually want to match one of those characters, you have to *escape* it using a backslash. For example, `\(1\+3\)` matches "(1 + 3)".

### Using regular expressions in Python

Many programming languages have built-in functions for matching  strings to regular expressions. We'll use the [Python re module] in 61A, but you can also use similar functionality in SQL, JavaScript, Excel,  shell scripting, etc.

The search method searches for a pattern anywhere in a string:

```
re.search(r"(Mahna)+", "Mahna Mahna Ba Dee Bedebe")
```

That method returns back a match object, which is considered truth-y in Python and can be inspected to find the matching strings.

For more details, please consult the [re module documentation](https://docs.python.org/3/library/re.html) or the [re tutorial](https://docs.python.org/3/howto/regex.html).

## BNF

Backus-Naur Form (BNF) is a syntax for describing a [context-free grammar](https://en.wikipedia.org/wiki/Context-free_grammar). It was invented for describing the syntax of programming languages, and is still commonly used in documentation and language parsers. EBNF is a dialect of BNF which contains some convenient shorthands.

An EBNF grammar contains symbols and a set of recursive production  rules. In 61A, we are using the Python Lark library to write EBNF  grammars, which has a few specific rules for grammar writing.

There are two types of symbols: Non-terminal symbols can expand into non-terminals (including  themselves) or terminals. In the Python Lark library, non-terminal  symbols are always lowercase. Terminal symbols can be strings or regular expressions. In Lark,  terminals are always uppercase.

Consider these two production rules:

```
numbers: INTEGER | numbers "," INTEGER
INTEGER: /-?\d+/
```

The symbol `numbers` is  a non-terminal with a recursive production rule. It corresponds to either an `INTEGER` terminal or to the `numbers` symbol (itself) plus a comma plus an `INTEGER` terminal. The `INTEGER` terminal is defined using a regular expression which matches any number of digits with an optional - sign in front.

This grammar can describe strings like:

```
10
10,-11
10,-11,12
```

And so on, with any number of integers in front.

A grammar should also specify a start symbol, which corresponds to  the whole expression being parsed (or the whole sentence, for a spoken  language).

For the simple example of comma-separated numbers, the start symbol could just be the numbers terminal itself:

```
?start: numbers
numbers: numbers "," INTEGER | INTEGER
INTEGER: /-?\d+/
```

EBNF grammars can use these shorthand notations for specifying how many symbols to match:

| EBNF Notation  | Meaning            | Pure BNF Equivalent       |
| -------------- | ------------------ | ------------------------- |
| item*          | Zero or more items | items: \| items item      |
| item+          | One or more items  | items: item \| items item |
| [item]   item? | Optional item      | optitem: \| item          |

Lark also includes a few handy features:

- You can specify tokens to complete ignore by using the ignore directive at the bottom of a grammar. For example, `%ignore /\s+/` ignores all whitespace (tabs/spaces/new lines).
- You can import pre-defined terminals for common types of data to  match. For example, %import common.NUMBER imports a terminal that matches any integer or decimal number.

Using all of that, here's an EBNF grammar that corresponds to the Calculator language:

```
start: calc_expr?
calc_expr: NUMBER | calc_op
calc_op: "(" OPERATOR calc_expr* ")"
OPERATOR: "+" | "-" | "*" | "/"

%ignore /\s+/
%import common.NUMBER
```

You can paste that into code.cs61a.org and then input Calculator  expressions in the interpreter to see their parse trees. Try it!

# Questions

## Regular Expressions

### Q1: Calculator Ops

Write a regular expression that parses strings written in the 61A Calculator language and returns any expressions which have two numeric operands, leaving out the parentheses around them.

```
import re

def calculator_ops(calc_str):
    """
    Finds expressions from the Calculator language that have two
    numeric operands and returns the expression without the parentheses.

    >>> calculator_ops("(* 2 4)")
    ['* 2 4']
    >>> calculator_ops("(+ (* 3 (+ (* 2 4) (+ 3 5))) (+ (- 10 7) 6))")
    ['* 2 4', '+ 3 5', '- 10 7']
    >>> calculator_ops("(* 2)")
    []
    """
    return re.findall(__________, calc_str)
```

#### Answer

```python
    return re.findall(r'[*+-/]\s*\d+\s*\d+', calc_str)
```

#### Solution

```python
    # Since hyphen is a special character inside [], it must be escaped
    return re.findall(r"\(([+\-/*]\s+\d+\s+\d+)\)", calc_str)

    # Alternate solution: hyphen must be at either beginning or end inside []
    return re.findall(r"\(([-+*/]\s+\d+\s+\d+)\)", calc_str)
```

## BNF

### Q2: Calculator BNF

Consider this BNF grammar for the Calculator language:

```
?start: calc_expr

?calc_expr: NUMBER | calc_op

calc_op: "(" OPERATOR calc_expr* ")"

OPERATOR: "+" | "-" | "*" | "/"

%ignore /\s+/
%import common.NUMBER
```

Let's understand and modify the functionality of this BNF with a few questions.

Use Ok to test your understanding:

```
---------------------------------------------------------------------
ebnf-grammar > Suite 1 > Case 1
(cases remaining: 4)

Q: Which aspects of the Calculator language are supported by this grammar?
Choose the number of the correct choice:
0) Variables can be defined and used as operands.
1) The division operator requires at least two arguments.
2) The subtraction operator requires at least one argument.
3) Each of the operands can itself be a Calculator expression.
? 3
-- OK! --

---------------------------------------------------------------------
ebnf-grammar > Suite 1 > Case 2
(cases remaining: 3)

Q: Which of the following expressions would NOT be parsable according to that BNF?
Choose the number of the correct choice:
0) (1 + 2)
1) (+ 1)
2) (+ 1 (+ 2 3))
3) (+)
4) (+ 1 2 3)
5) (+ 1 2)
? 0
-- OK! --

---------------------------------------------------------------------
ebnf-grammar > Suite 1 > Case 3
(cases remaining: 2)

Q: Which line of the BNF should we modify to add support for calculations using a modulus operator, like (% 15 5)?
Choose the number of the correct choice:
0) ?calc_expr: NUMBER | calc_op
1) calc_op: "(" OPERATOR calc_expr* ")"
2) start: calc_expr
3) OPERATOR: "+" | "-" | "*" | "/"
? 3
-- OK! --

---------------------------------------------------------------------
ebnf-grammar > Suite 1 > Case 4
(cases remaining: 1)

Q: Does the BNF grammar provide enough information to create a working interpreter for this version of the Calculator language?
Choose the number of the correct choice:
0) Yes, but only if we feed this grammar into a program that was written in the Calculator language itself.
1) Yes, if we feed this grammar into a program that understands BNF grammars, it will be able to parse Calculator expressions and output the result.
2) No, this grammar does not provide enough information for the parsing or evaluation step, it is useful mostly as documentation.
3) No, this grammar gives enough information for parsing a Calculator expression, but it does not provide enough information to evaluate it.
? 0
-- Not quite. Try again! --

? 1
-- Not quite. Try again! --

? 3
-- OK! --
```

### Q3: Linked List BNF

> For the next two problems, you can test your code on [code.cs61a.org](https://code.cs61a.org/) by adding the following line at the beginning before the problem's skeleton code:
>
> ```
> ?start: link
> -- replace link with tree_node for the next question
> ```

In this problem, we're going to define a BNF that parses integer Linked Lists created in Python. We won't be handling `Link.empty`.

For reference, here are some examples of Linked Lists:

*Your implementation should be able to handle nested Linked Lists, such as the third example below.*

- `Link(2)`
- `Link(12, Link(2))`
- `Link(5, Link(7, Link(Link(8, Link(9)))))`

```
link: "null"

?link_first: "null"

?link_rest: "null"

%ignore /\s+/
%import common.NUMBER
```

#### Answer

去除"null"

```
?start: link

link: "null" | "Link(" link_first ["," link_rest] ")"

?link_first: "null" | NUMBER | link

?link_rest: "null" | link

%ignore /\s+/
%import common.NUMBER
```

#### Solution

```
link: "Link(" link_first link_rest? ")"

?link_first: link|NUMBER

?link_rest: ", " link

%ignore /\s+/
%import common.NUMBER
```

### Q4: Tree BNF

Now, we will define a BNF to parse Trees with integer leaves created in Python.

Here are some examples of Trees:

*Your implementation should be able to handle Trees with no branches and one or more branches.*

- `Tree(2)`
- `Tree(6, [Tree(1), Tree(3, [Tree(1), Tree(2)])])`

```
tree_node: "null"

?label: "null"

branches: "null"

%ignore /\s+/
%import common.NUMBER
```

#### Answer

```
?start: tree_node

tree_node: "Tree(" label branches? ")"

?label: NUMBER

branches: "," "[" tree_node ["," tree_node]* "]"

%ignore /\s+/
%import common.NUMBER
```

#### Solution

```
tree_node: "Tree(" label branches? ")"

?label: NUMBER

branches:", [" (tree_node ",")* tree_node "]"

%ignore /\s+/
%import common.NUMBER
```

