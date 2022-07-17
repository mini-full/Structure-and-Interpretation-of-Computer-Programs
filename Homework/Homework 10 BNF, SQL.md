# Homework 10: BNF, SQL

## Usage

First, check that a file named `sqlite_shell.py` exists alongside the assignment files. If you don't see it, or if you encounter problems with it, scroll down to the Troubleshooting section to see how to download an official precompiled SQLite binary before proceeding.

You can start an interactive SQLite session in your Terminal or Git Bash with the following command:

```
python3 sqlite_shell.py
```

While the interpreter is running, you can type `.help` to see some of the commands you can run.

To exit out of the SQLite interpreter, type `.exit` or `.quit` or press `Ctrl-C`.  Remember that if you see `...>` after pressing enter, you probably forgot a `;`.

You can also run all the statements in a `.sql` file by doing the following: (Here we're using the `lab13.sql` file as an example.)

1. Runs your code and then exits SQLite immediately afterwards.

   ```
   python3 sqlite_shell.py < lab13.sql
   ```

2. Runs your code and then opens an interactive SQLite session, which is  similar to running Python code with the interactive `-i` flag.

   ```
   python3 sqlite_shell.py --init lab13.sql
   ```

# Questions

## BNF

### Regex Parser

Previously in CS61A you studied regular expressions (regex), a  grammar for pattern matching in strings. In this question you will  create a BNF grammar for parsing through regular expression patterns,  which we will denote as an `rstring`. Below, we've defined the following skeleton for `rstring` grammar:

```
rstring: "r\"" regex* "\""

?regex: character | word

character: LETTER | NUMBER
word: WORD

%ignore /\s+/
%import common.LETTER
%import common.NUMBER
%import common.WORD
```

The current implementation is very limited, and can only support  alphanumeric patterns which directly match the input. In the following  questions, you will implement support for a limited subset of regular  expression features.

> NOTE: for the purposes of testing, we require that your syntax trees match the doctests'. Be sure to define all expressions as noted in the question, and prefix all extra expressions not mentioned in the question with a `?` (such as `?rstring`).

### Q1: Grouping and Pipes

In this question, you will add support for grouping and piping.

Recall that grouping allows for an entire regular expression to be  treated as a single unit, and piping allows for a pattern to match an  expression on either side. Combined, these will let us create patterns  which match multiple strings!

Define the `group` and `pipe` expressions in your grammar.

1. A **`group`** consists of any `regex` expression surrounded by parentheses (`()`).
2. A **`pipe`** operator consists of a `regex` expression, followed by a pipe (`|`) character, and lastly followed by another `regex` expression.

For example, `r"apples"` would match exactly the phrase  "apples" in an input. If we wanted our pattern from before to match  "oranges" as well, we could expand our `rstring` to do so using groupings and pipes: `r"(apples)|(oranges)"`.

> Hint: note that `group`s and `pipe`s are valid `regex` expressions on their own! You may need to update a previously defined expression.

### Q2: Classes

Now, we will add support for character classes.

Recall that character classes allow for the pattern to match any singular `character` defined within the class. The class itself consists either of individual `character`s, or `range`s of `characters`.

Specifically, we define the following:

1. A **`range`** consists of either `NUMBER`s or `LETTER`s separated by a hyphen (`-`).
2. A **`class`** expression consists of any number of `character`s or character `range`s surrounded by square brackets (`[]`).

Note that for this question, a range may only consist of either `NUMBER`s or `LETTER`s; this means that while `[0-9]` and `[A-Z]` are valid ranges, `[0-Z]` would not be a valid range. In addition, the `character`s and `range`s in a `class` may appear in any order and any number of times. For example, `[ad-fc0-9]`, `[ad-f0-9c]`, `[a0-9d-fc]`, and `[0-9ad-fc]` are all valid classes.

### Q3: Quantifiers

Lastly, we will add support for quantifiers.

Recall that quantifiers allow for a pattern to match a specified number of a unit.

Specifically, we define the following:

1. A **`plus_quant`** expression consists of a `group`, a `character`, or a `class`, followed by a plus symbol (`+`).
2. A **`star_quant`** expression consists of a `group`, a `character`, or a `class`, followed by a star symbol (`*`).
3. A **`num_quant`** expression consists of either a `group`, a `character`, or a `class`, followed by one of the following:
   1. a `NUMBER` enclosed in curly braces (`{}`);
   2. a range of `NUMBER`s (separated by a comma (`,`), which may potentially be open on only one side. For example, `{2,7}`, `{2,}`, and `{,7}` are valid numeric quantifiers. `{,}` is not valid.

> Hint: these three quantifiers share many similarities. Consider defining additional expressions in this question!

Use Ok to test your code:

```
python3 ok -q regex_grouping
python3 ok -q regex_classes
python3 ok -q regex_quantifiers
```

After completing this question, your implementation is complete! Be sure that it still passes any previous tests as well.

#### Answer

```
?start: rstring

rstring: "r\"" regex* "\""

?regex: character | word | group | pipe | class | plus_quant | star_quant | num_quant

character: LETTER | NUMBER
word: WORD

group: "(" regex* ")"
pipe: regex "|" regex 

range: (NUMBER "-" NUMBER) | (LETTER "-" LETTER) 
class: "[" (character | range )* "]"

?mul_regex: character | group | class
plus_quant: mul_regex "+"
star_quant: mul_regex "*"
num_quant: mul_regex "{" ((NUMBER) | (NUMBER "," NUMBER ) | ("," NUMBER) | (NUMBER ",")) "}"

%ignore /\s+/
%import common.LETTER
%import common.NUMBER
%import common.WORD
```

#### Solution

```
rstring: "r\"" regex* "\""

?regex: group | pipe | character | word | class | quant

group: "(" regex ")"
pipe: regex "|" regex

class: "["(range | character)+"]"
range: (LETTER "-" LETTER) | (NUMBER "-" NUMBER)

?quant: num_quant | star_quant | plus_quant
?quantifiable: group | character | class
num_quant: quantifiable ("{" (NUMBER | (NUMBER? "," NUMBER) | (NUMBER "," NUMBER?)) "}")
star_quant: quantifiable "*"
plus_quant: quantifiable "+"

character: LETTER | NUMBER
word: WORD

%ignore /\s+/
%import common.LETTER
%import common.NUMBER
%import common.WORD
```

`class: "["(range | character)+"]"`

`quant`

## SQL

### Dog Data

In each question below, you will define a new table based on the following tables.

```
CREATE TABLE parents AS
  SELECT "abraham" AS parent, "barack" AS child UNION
  SELECT "abraham"          , "clinton"         UNION
  SELECT "delano"           , "herbert"         UNION
  SELECT "fillmore"         , "abraham"         UNION
  SELECT "fillmore"         , "delano"          UNION
  SELECT "fillmore"         , "grover"          UNION
  SELECT "eisenhower"       , "fillmore";

CREATE TABLE dogs AS
  SELECT "abraham" AS name, "long" AS fur, 26 AS height UNION
  SELECT "barack"         , "short"      , 52           UNION
  SELECT "clinton"        , "long"       , 47           UNION
  SELECT "delano"         , "long"       , 46           UNION
  SELECT "eisenhower"     , "short"      , 35           UNION
  SELECT "fillmore"       , "curly"      , 32           UNION
  SELECT "grover"         , "short"      , 28           UNION
  SELECT "herbert"        , "curly"      , 31;

CREATE TABLE sizes AS
  SELECT "toy" AS size, 24 AS min, 28 AS max UNION
  SELECT "mini"       , 28       , 35        UNION
  SELECT "medium"     , 35       , 45        UNION
  SELECT "standard"   , 45       , 60;
```

Your tables should still perform correctly even if the values in these tables change. For example, if you are asked to list all dogs with a name that starts with h, you should write:

```
SELECT name FROM dogs WHERE "h" <= name AND name < "i";
```

Instead of assuming that the `dogs` table has only the data above and writing

```
SELECT "herbert";
```

The former query would still be correct if the name `grover` were changed to `hoover` or a row was added with the name `harry`.

### Q4: Size of Dogs

The Fédération Cynologique Internationale classifies a standard poodle as over 45 cm and up to 60 cm. The `sizes` table describes this and other such classifications, where a dog must be over the `min` and less than or equal to the `max` in `height` to qualify as a `size`.

Create a `size_of_dogs` table with two columns, one for each dog's `name` and another for its `size`.

The output should look like the following:

```
sqlite> select * from size_of_dogs;
abraham|toy
barack|standard
clinton|standard
delano|standard
eisenhower|mini
fillmore|mini
grover|toy
herbert|mini
```

#### Answer

```sql
-- The size of each dog
CREATE TABLE size_of_dogs AS
  SELECT name, size FROM dogs, sizes WHERE height > min AND height <= max;
```

#### Solution

```sql
  SELECT name, size FROM dogs, sizes
    WHERE height > min AND height <= max;
```

### Q5: By Parent Height

Create a table `by_parent_height` that has a column of the names of all dogs that have a `parent`, ordered by the height of the parent from tallest parent to shortest parent.

For example, `fillmore` has a parent (`eisenhower`) with height 35, and so should appear before `grover` who has a parent (`fillmore`) with height 32. The names of dogs with parents of the same height should appear together in any order. For example, `barack` and `clinton` should both appear at the end, but either one can come before the other.

```
sqlite> select * from by_parent_height;
herbert
fillmore
abraham
delano
grover
barack
clinton
```

#### Answer

```sql
-- All dogs with parents ordered by decreasing height of their parent
CREATE TABLE by_parent_height AS
  SELECT child FROM parents, dogs WHERE parent = name ORDER BY height DESC;
```

#### Solution

```sql
  SELECT child FROM parents, dogs WHERE name = parent ORDER BY -height;
```

### Q6: Sentences

There are two pairs of siblings that have the same size. Create a table that contains a row with a string for each of these pairs.  Each string should be a sentence describing the siblings by their size.

Each sibling pair should appear only once in the output, and siblings should be listed in alphabetical order (e.g. `"barack plus clinton..."` instead of `"clinton plus barack..."`), as follows:

```
sqlite> select * from sentences;
The two siblings, barack plus clinton have the same size: standard
The two siblings, abraham plus grover have the same size: toy
```

> *Hint*: First, create a helper table containing each pair of siblings. This will make comparing the sizes of siblings when constructing the main table easier.
>
> **Hint**: If you join a table with itself, use `AS` within the `FROM` clause to give each table an alias.
>
> **Hint**: In order to concatenate two strings into one, use the `||` operator.

#### Answer

```sql
-- Filling out this helper table is optional
CREATE TABLE siblings AS
  SELECT a.child AS smaller, b.child AS greater 
    FROM parents AS a, parents AS b 
      WHERE a.parent = b.parent AND a.child < b.child;

-- Sentences about siblings that are the same size
CREATE TABLE sentences AS
  SELECT "The two siblings, " || smaller || " plus " || greater || " have the same size: " || a.size 
    FROM siblings, size_of_dogs AS a, size_of_dogs AS b 
      WHERE a.name = smaller AND b.name = greater AND a.size = b.size;
```

#### Solution

```sql
-- Filling out this helper table is optional
CREATE TABLE siblings AS
  SELECT a.child AS first, b.child AS second FROM parents AS a, parents AS b
    WHERE a.parent = b.parent AND a.child < b.child;

-- Sentences about siblings that are the same size
CREATE TABLE sentences AS
  SELECT "The two siblings, " || first || " plus " || second || " have the same size: " || a.size
    FROM siblings, size_of_dogs AS a, size_of_dogs AS b
    WHERE a.size = b.size AND a.name = first AND b.name = second;
```

Roughly speaking, there are two tasks we need to solve here:

**Figure out which dogs are siblings**

A sibling is someone you share a parent with. This will probably involve the `parents` table.

It might be tempting to join this with `dogs`, but there isn't any extra information provided by a dogs table that we need at this time. Furthermore, we still need information on sibling for a given dog, since the `parents` table just associates each dog to a parent.

The next step, therefore, is to match all children to all other children by joining the parents table to itself. The only rows here that make sense are the rows that represent sibling relationships since they share the same parent.

Remember that we want to avoid duplicates! If dog A and B are siblings, we don't want both A/B and B/A to appear in the final result. We also definitely don't want A/A to be a sibling pair. Enforcing ordering on the sibling names ensures that we don't have either issue.

**Construct sentences based on sibling information**

After determining the siblings, constructing the sentences just requires us to get the size of each sibling. We could join on the `dogs` and `sizes` tables as we did in an earlier problem, but there's no need to redo that work. Instead, we'll reuse our `size_of_dogs` table to figure out the size of each sibling in each pair.