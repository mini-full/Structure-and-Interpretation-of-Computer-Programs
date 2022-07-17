# Homework 9: Regular Expressions

# Questions

## RegEx

### Q1: What would RegEx Match?

For each of the following regular expressions, suggest a string that would be fully matched.

> Use Ok to test your knowledge by choosing the best answer for each of the following questions:
>
> ```
> ---------------------------------------------------------------------
> wwrm > Suite 1 > Case 1
> (cases remaining: 3)
> 
> Q: #[a-f0-9]{6}
> Choose the number of the correct choice:
> 0) A hexadecimal color code with 3 letters and 3 numbers
> 1) A hexadecimal color code that starts with letters and ends with numbers, like #gg1234
> 2) Any 6-digit hexadecimal color code, like #fdb515
> 3) Any hexadecimal color code with 0-6 digits
> ? 0
> -- Not quite. Try again! --
> 
> ? 2
> -- OK! --
> 
> ---------------------------------------------------------------------
> wwrm > Suite 1 > Case 2
> (cases remaining: 2)
> 
> Q: (fizz(buzz|)|buzz)
> Choose the number of the correct choice:
> 0) Only fizzbuzz or buzz
> 1) Only fizzbuzzbuzz
> 2) Only fizz
> 3) Only fizzbuzz, fizz, and buzz
> 4) Only fizzbuzz
> ? 3
> -- OK! --
> 
> ---------------------------------------------------------------------
> wwrm > Suite 1 > Case 3
> (cases remaining: 1)
> 
> Q: `[-+]?\d*\.?\d+`
> Choose the number of the correct choice:
> 0) Only signed numbers like +1000, -1.5
> 1) Only signed or unsigned integers like +1000, -33
> 2) Signed or unsigned numbers like +1000, -1.5, .051
> 3) Only unsigned numbers like 0.051
> ? 2
> -- OK! --
> ```

### Q2: Roman Numerals (Failed)

Write a regular expression that finds any string of letters that resemble a Roman numeral and aren't part of another word. A Roman numeral is made up of the letters I, V, X, L, C, D, M and is at least one letter long.

> For the purposes of this problem, don't worry about whether or not a Roman numeral is valid. For example, "VIIIII" is not a Roman numeral, but it is fine if your regex matches it.

```
import re

def roman_numerals(text):
    """
    Finds any string of letters that could be a Roman numeral
    (made up of the letters I, V, X, L, C, D, M).

    >>> roman_numerals("Sir Richard IIV, can you tell Richard VI that Richard IV is on the phone?")
    ['IIV', 'VI', 'IV']
    >>> roman_numerals("My TODOs: I. Groceries II. Learn how to count in Roman IV. Profit")
    ['I', 'II', 'IV']
    >>> roman_numerals("I. Act 1 II. Act 2 III. Act 3 IV. Act 4 V. Act 5")
    ['I', 'II', 'III', 'IV', 'V']
    >>> roman_numerals("Let's play Civ VII")
    ['VII']
    >>> roman_numerals("i love vi so much more than emacs.")
    []
    >>> roman_numerals("she loves ALL editors equally.")
    []
    """
    return re.findall(__________, text)
```

#### Solution

```python
    return re.findall(r"\b([IVXLCDM]+)\b", text)
```

### Q3: CS Classes

On reddit.com, there is an /r/berkeley subreddit for discussions about everything UC Berkeley. However, there is such a large amount of CS-related posts that those posts are auto-tagged so that readers can choose to ignore them or read only them.

Write a regular expression that finds strings that resemble a CS class- starting with "CS", followed by a number, and then optionally followed by "A", "B", or "C". Your search should be case insensitive, so both "CS61A" and "cs61a" would match.

```
import re

def cs_classes(post):
    """
    Returns strings that look like a Berkeley CS class,
    starting with "CS", followed by a number, optionally ending with A, B, or C
    and potentially with a space between "CS" and the number.
    Case insensitive.

    >>> cs_classes("Is it unreasonable to take CS61A, CS61B, CS70, and EE16A in the summer?")
    True
    >>> cs_classes("how do I become a TA for cs61a? that job sounds so fun")
    True
    >>> cs_classes("Can I take ECON101 as a CS major?")
    False
    >>> cs_classes("Should I do the lab lites or regular labs in EE16A?")
    False
    >>> cs_classes("What are some good CS upper division courses? I was thinking about CS 161 or CS 169a")
    True
    """
    return bool(re.search(__________, post))
```

#### Answer

```python
    # return re.findall(r'(CS|cs)\s*(\d+[a-cA-C]?)', post)
    # -->[('CS', '161'), ('CS', '169a')]
    return bool(re.search(r'(CS|cs)\s*(\d+[a-cA-C]?)', post))
```

#### Solution

```python
    return bool(re.search(r"(cs|CS)\s?\d+[a-cA-C]?", post))
```

### Q4: Time for Times

You're given a body of text and told that within it are some times. Write a regular expression which, for a few examples, would match the following:

```
['05:24', '7:23', '23:59', '12:22', '00:00']
```

but would not match these invalid "times"

```
['05:64', '70:23']
```

You may find [non-capturing groups](https://www.regular-expressions.info/brackets.html#noncap) helpful to use for this question.

```
import re

def match_time(text):
    """
    >>> match_time("At 05:24AM, I had sesame bagels with cream cheese before my coffee at 7:23.")
    ['05:24AM', '7:23']
    >>> match_time("At 23:59 I was sound asleep as the time turned to 00:00.")
    ['23:59', '00:00']
    >>> match_time("Mix water in a 1:2 ratio with chicken stock.")
    []
    >>> match_time("At 2:00 I pinged 127.0.0.1:80.")
    ['2:00']
    """
    return re.findall(__________, text)
```

#### Answer

```python
    return re.findall(r'(?:[0-1][0-9]|2[0-3]|[0-9]):[0-5][0-9](?:AM|PM)?', text)
# [0-9] -- \d
```

#### Solution

```python
    return re.findall(r"\b(?:(?:[01]?\d)|(?:2[0123])):[012345]\d(?:[AaPp][Mm])?\b", text)	# \b 
```

### Q5: Most Common Area Code

Write a function which takes in a body of text and finds the most common area code. Area codes must be part of a valid phone number.

To solve this problem, we will first write a regular expression which finds valid phone numbers and captures the area code. See the docstring of `area_codes` for specifics on what qualifies as a valid phone number.

```
import re

def area_codes(text):
    """
    Finds all phone numbers in text and captures the area code. Phone numbers
    have 10 digits total and may have parentheses around the area code, and
    hyphens or spaces after the third and sixth digits.

    >>> area_codes('(111) 111 1111, 1234567890 and 123 345 6789 should be matched.')
    ['111', '123', '123']
    >>> area_codes("1234567890 should, but 54321 and 654 456 78901 should not match")
    ['123']
    >>> area_codes("no matches for 12 3456 7890 or 09876-54321")
    []
    """
    return re.findall(__________, text)
```

#### Answer

```python
    return re.findall(r'\b\(?(\d{3})\)?(?:\s|-)?\d{3}(?:\s|-)?\d{4}\b', text)
```

Now that we can get an area code, we just need to find the most common area code from a list. You may find the [`list.count` method](https://docs.python.org/3/tutorial/datastructures.html) useful.

```
def most_common_code(text):
    """
    Takes in an input string which contains at least one phone number (and
    may contain more) and returns the most common area code among all phone
    numbers in the input. If there are multiple area codes with the same
    frequency, return the first one that appears in the input text.

    >>> most_common_code('(501) 333 3333')
    '501'
    >>> input_text = '''
    ... (123) 000 1234 and 12454, 098-123-0941, 123 451 0951 and 410-501-3021 has
    ... some phone numbers. '''
    >>> most_common_code(input_text)
    '123'
    """
    "*** YOUR CODE HERE ***"
```

#### Answer

```python
    codes = area_codes(text)
    return max(codes, key=codes.count)
```