# Lab 13: SQL

## SQL Basics

### Creating Tables

You can create SQL tables either from scratch or from existing tables.

The following statement creates a table by specifying column names and values without referencing another table. Each `SELECT` clause specifies the values for one row, and `UNION` is used to join rows together. The `AS` clauses give a name to each column; it need not be repeated in subsequent rows after the first.

```
CREATE TABLE [table_name] AS
  SELECT [val1] AS [column1], [val2] AS [column2], ... UNION
  SELECT [val3]             , [val4]             , ... UNION
  SELECT [val5]             , [val6]             , ...;
```

Let's say we want to make the following table called `big_game` which records the scores for the Big Game each year. This table has three columns: `berkeley`, `stanford`, and `year`.

![image-20211220215026426](https://cdn.jsdelivr.net/gh/Christina0031/article_imgs/imgs/image-20211220215026426.png)

We could do so with the following `CREATE TABLE` statement:

```
CREATE TABLE big_game AS
  SELECT 30 AS berkeley, 7 AS stanford, 2002 AS year UNION
  SELECT 28,             16,            2003         UNION
  SELECT 17,             38,            2014;
```

### Selecting From Tables

More commonly, we will create new tables by selecting specific columns that we want from existing tables by using a `SELECT` statement as follows:

```
SELECT [columns] FROM [tables] WHERE [condition] ORDER BY [columns] LIMIT [limit];
```

Let's break down this statement:

- `SELECT [columns]` tells SQL that we want to include the given columns in our  output table; `[columns]` is a comma-separated list of column names, and `*`  can be used to select all columns
- `FROM [table]` tells SQL that the columns we want to select are from the  given table; see the [joins section](https://cs61a.org/lab/lab13/) to see how to select  from multiple tables
- `WHERE [condition]` filters the output table by only including rows whose  values satisfy the given `[condition]`, a boolean expression
- `ORDER BY [columns]` orders the rows in the output table by the given  comma-separated list of columns
- `LIMIT [limit]` limits the number of rows in the output table by the integer  `[limit]`

> *Note:* We capitalize SQL keywords purely because of style convention. It makes queries much easier to read, though they will still work if you don't capitalize keywords.

Here are some examples:

Select all of Berkeley's scores from the `big_game` table, but only include scores from years past 2002:

```
sqlite> SELECT berkeley FROM big_game WHERE year > 2002;
28
17
```

Select the scores for both schools in years that Berkeley won:

```
sqlite> SELECT berkeley, stanford FROM big_game WHERE berkeley > stanford;
30|7
28|16
```

Select the years that Stanford scored more than 15 points:

```
sqlite> SELECT year FROM big_game WHERE stanford > 15;
2003
2014
```

### SQL operators

Expressions in the `SELECT`, `WHERE`, and `ORDER BY` clauses can contain one or more of the following operators:

- comparison operators: `=`, `>`, `<`, `<=`, `>=`, `<>` or `!=` ("not equal")
- boolean operators: `AND`, `OR`
- arithmetic operators: `+`, `-`, `*`, `/`
- concatenation operator: `||`

Here are some examples:

Output the ratio of Berkeley's score to Stanford's score each year:

```
sqlite> select berkeley * 1.0 / stanford from big_game;
0.447368421052632
1.75
4.28571428571429
```

Output the sum of scores in years where both teams scored over 10 points:

```
sqlite> select berkeley + stanford from big_game where berkeley > 10 and stanford > 10;
55
44
```

Output a table with a single column and single row containing the value "hello world":

```
sqlite> SELECT "hello" || " " || "world";
hello world
```

## Joins

To select data from multiple tables, we can use joins. There are many types of joins, but the only one we'll worry about is the inner join. To perform an inner join on two on more tables, simply list them all out in the `FROM` clause of a `SELECT` statement:

```
SELECT [columns] FROM [table1], [table2], ... WHERE [condition] ORDER BY [columns] LIMIT [limit];
```

We can select from multiple different tables or from the same table multiple times.

Let's say we have the following table that contains the names of head football coaches at Cal since 2002:

```
CREATE TABLE coaches AS
  SELECT "Jeff Tedford" AS name, 2002 as start, 2012 as end UNION
  SELECT "Sonny Dykes"         , 2013         , 2016        UNION
  SELECT "Justin Wilcox"       , 2017         , null;
```

When we join two or more tables, the default output is a [cartesian product](https://en.wikipedia.org/wiki/Cartesian_product). For example, if we joined `big_game` with `coaches`, we'd get the following:

![image-20211220215050300](https://cdn.jsdelivr.net/gh/Christina0031/article_imgs/imgs/image-20211220215050300.png)

If we want to match up each game with the coach that season, we'd have to compare columns from the two tables in the `WHERE` clause:

```
sqlite> SELECT * FROM big_game, coaches WHERE year >= start AND year <= end;
17|38|2014|Sonny Dykes|2013|2016
28|16|2003|Jeff Tedford|2002|2012
30|7|2002|Jeff Tedford|2002|2012
```

The following query outputs the coach and year for each Big Game win recorded in `big_game`:

```
sqlite> SELECT name, year FROM big_game, coaches
...>        WHERE berkeley > stanford AND year >= start AND year <= end;
Jeff Tedford|2003
Jeff Tedford|2002
```

In the queries above, none of the column names are ambiguous. For example, it is clear that the `name` column comes from the `coaches` table because there isn't a column in the `big_game` table with that name.  However, if a column name exists in more than one of the tables being joined, or if we join a table with itself, we must disambiguate the column names using *aliases*.

For examples, let's find out what the score difference is for each team between a game in `big_game` and any previous games. Since each row in this table represents one game, in order to compare two games we must join `big_game` with itself:

```
sqlite> SELECT b.Berkeley - a.Berkeley, b.Stanford - a.Stanford, a.Year, b.Year
...>        FROM big_game AS a, big_game AS b WHERE a.Year < b.Year;
-11|22|2003|2014
-13|21|2002|2014
-2|9|2002|2003
```

In the query above, we give the alias `a` to the first `big_game` table and the alias `b` to the second `big_game` table. We can then reference columns from each table using dot notation with the aliases, e.g. `a.Berkeley`, `a.Stanford`, and `a.Year` to select from the first table.

## SQL Aggregation

Previously, we have been dealing with queries that process one row at a time. When we join, we make pairwise combinations of all of the rows. When we use `WHERE`, we filter out certain rows based on the condition. Alternatively, applying an [aggregate function](http://www.sqlite.org/lang_aggfunc.html) such as `MAX(column)` combines the values in multiple rows.

By default, we combine the values of the *entire* table. For example, if we wanted to count the number of flights from our `flights` table, we could use:

```
sqlite> SELECT COUNT(*) from FLIGHTS;
13
```

What if we wanted to group together the values in similar rows and perform the aggregation operations within those groups? We use a `GROUP BY` clause.

Here's another example. For each unique departure, collect all the rows having the same departure airport into a group. Then, select the `price` column and apply the `MIN` aggregation to recover the price of the cheapest departure from that group. The end result is a table of departure airports and the cheapest departing flight.

```
sqlite> SELECT departure, MIN(price) FROM flights GROUP BY departure;
AUH|932
LAS|50
LAX|89
SEA|32
SFO|40
SLC|42
```

Just like how we can filter out rows with `WHERE`, we can also filter out groups with `HAVING`. Typically, a `HAVING` clause should use an aggregation function. Suppose we want to see all airports with at least two departures:

```
sqlite> SELECT departure FROM flights GROUP BY departure HAVING COUNT(*) >= 2;
LAX
SFO
SLC
```

Note that the `COUNT(*)` aggregate just counts the number of rows in each group. Say we want to count the number of *distinct* airports instead. Then, we could use the following query:

```
sqlite> SELECT COUNT(DISTINCT departure) FROM flights;
6
```

This enumerates all the different departure airports available in our `flights` table (in this case: SFO, LAX, AUH, SLC, SEA, and LAS).



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

# Survey Data

## Survey Data

Last week, we asked you and your fellow students to complete a brief online survey through Google Forms, which involved relatively random but fun questions. In this lab, we will interact with the results of the survey by using SQL queries to see if we can find interesting things in the data.

First, take a look at `data.sql` and examine the table defined in it. Note its structure. You will be working with the two tables in this file.

The first is the table `students`, which is the main results of the survey. Each column represents a different question from the survey, except for the first column, which is the time of when the result was submitted. This time is a unique identifier for each of the rows in the table. The last several columns all correspond to the last question on the survey (more details below.)

| Column Name  | Question                                                     |
| ------------ | ------------------------------------------------------------ |
| `time`       | The unique timestamp that identifies the submission          |
| `number`     | What's your favorite number between 1 and 100?               |
| `color`      | What is your favorite color?                                 |
| `seven`      | Choose the number 7 below. Options:   7 Choose this option instead seven the number 7 below. I find this question condescending |
| `song`       | If you could listen to only one of these songs for the rest of your life, which would it be?   Options:   "Smells Like Teen Spirit" by Nirvana "Shelter" by Porter Robinson "Clair de Lune" by Claude Debussy "Dancing Queen" by ABBA "Down With The Sickness" by Disturbed "Everytime We Touch" by Cascada "All I want for Christmas is you" by Mariah Carey "STAY" by The Kid LAROI, Justin Bieber "Old Town Road" by Lil Nas X "Turntables" by Janelle Monáe "Shake It Off" by Taylor Swift |
| `date`       | Pick a day of the year!                                      |
| `pet`        | If you could have any animal in the world as a pet, what would it be? |
| `instructor` | Choose your favorite photo of John DeNero                    |
| `smallest`   | Try to guess the smallest unique positive INTEGER that anyone will put! |

The second table is `numbers`, which is the results from the survey in which students could select more  than one option from the numbers listed, which ranged from 0 to 10 and included  2021, 2022, 9000, and 9001. Each row has a time (which is again a unique  identifier) and has the value `'True'` if the student selected the column or `'False'`  if the student did not.  The column names in this table are the following strings, referring to each possible  number: `'0'`, `'1'`, `'2'`, `'4'`, `'5'`, `'6'`, `'7'`, `'8'`, `'9'`, `'10'`, `'2021'`, `'2022'`, `'9000'`, `'9001'`

Since the survey was anonymous, we used the timestamp that a survey was submitted as a unique identifier.  A time in `students` matches up with a time in `numbers`. For example, a row in `students` whose `time` value is `"11/17/2021 10:52:40"` matches up with the row in `numbers` whose `time` value is `"11/17/2021 10:52:40"`. These entries come from the same Google form submission and thus belong to the same student.

> *Note*: If you are looking for your personal response within the data, you may have noticed that some of your answers are slightly different from what you had inputted. In order to make SQLite accept our data, and to optimize for as many matches as possible during our joins, we did the following things to clean up the data:
>
> - `color` and `pet`: We converted all the strings to be completely lowercase.
> - For some of the more "free-spirited" responses, we escaped the special  characters so that they could be properly parsed.

You will write all of your solutions in the starter file `lab13.sql` provided. As with other labs, you can test your solutions with OK. In addition, you can use either of the following commands:

```
python3 sqlite_shell.py < lab13.sql
python3 sqlite_shell.py --init lab13.sql
```

# Questions

### Q1: What Would SQL print?

> Note: there is no submission for this question

First, load the tables into sqlite3.

```
$ python3 sqlite_shell.py --init lab13.sql
```

Before we start, inspect the schema of the tables that we've created for you:

```
sqlite> .schema
```

This tells you the name of each of our tables and their attributes.

Let's also take a look at some of the entries in our table. There are a lot of entries though, so let's just output the first 20:

```
sqlite> SELECT * FROM students LIMIT 20;
```

If you're curious about some of the answers students put into the Google form, open up `data.sql` in your favorite text editor and take a look!

For each of the SQL queries below, think about what the query is looking for, then try running the query yourself and see!

```
sqlite> SELECT * FROM students LIMIT 30; -- This is a comment. * is shorthand for all columns!
11/17/2021 10:52:40|3|black|the number 7 below.|Smells Like Teen Spirit|10/31|dog|2|1
11/17/2021 10:55:28|28|blue|7|Clair De Lune|8/20|dog|2|4
11/17/2021 11:06:35|99|white|seven|Smells like Teen Spirit|6/5|cheetah|3|1
11/17/2021 11:09:04|42|green|7|Shelter|9/16|capybara|4|1
11/17/2021 11:12:56|8|purple|7|Old Town Road|5/15|squirrell|4|26
11/17/2021 11:19:53|23|gern|seven|Dancing Queen|7/23|megladon|1|1
11/17/2021 11:27:34|88|red|You're not the boss of me!|Dancing Queen|7/11|deer|1|1
11/17/2021 11:31:44|23|purple|the number 7 below.|Old Town Road|5/23|porcupine|3|48
11/17/2021 11:55:11|12|white|You're not the boss of me!|Shake It Off|5/3|cat|5|44
11/17/2021 11:57:34|16|black|7|STAY|1/1|snake|5|19
11/17/2021 11:59:48|27|pink|7|Dancing Queen|8/13|dolphin|4|37
11/17/2021 12:04:38|5|orange|7|Clair De Lune|10/18|tiger|4|412
11/17/2021 12:14:37|99|forest green|7|STAY|12/31|cat|1|13
11/17/2021 12:16:43|38|blue|the number 7 below.|All I want for Christmas|11/11|elephant|1|28
11/17/2021 12:19:45|88|turquoise|Choose this option instead|STAY|4/16|dragon|2|17
11/17/2021 12:23:14|7|green|You're not the boss of me!|Shelter|4/6|cat|1|234
11/17/2021 12:26:03|69|ocean blue|You're not the boss of me!|Shelter|11/19|schnauzer dog|5|57
11/17/2021 12:30:12|9|deep blue|7|Shake It Off|1/3|horse|2|37
11/17/2021 12:32:54|42|pink|the number 7 below.|Shelter|10/27|cat|2|16
11/17/2021 12:35:33|13|green|Choose this option instead|Smells like Teen Spirit|7/12|penguin|4|7
11/17/2021 12:48:31|17|green|the number 7 below.|Clair De Lune|7/13|dog|1|38
11/17/2021 12:51:43|21|green|7|Everytime We Touch|9/2|owl monkey|1|59
11/17/2021 12:51:50|28|purple|seven|Dancing Queen|1/1|tiger|4|1
11/17/2021 12:59:11|69|red|7|STAY|1/1|tiger|5|1
11/17/2021 13:04:12|3.1415962|yellow|seven|Smells like Teen Spirit|1/1|penguin !|1|13
11/17/2021 13:04:27|72|black|7|Dancing Queen|12/25|bear|5|34
11/17/2021 13:05:09|7|purple|7|Everytime We Touch|12/27|tucan|2|57
11/17/2021 13:05:14|17|blue|7|All I want for Christmas|8/30|cat|1|12
11/17/2021 13:07:02|6|black|the number 7 below.|Clair De Lune|11/11|owl|5|90
11/17/2021 13:13:55|2|blue|7|Shake It Off|5/8|dog|4|47
sqlite> SELECT color FROM students WHERE number = 7;
green
purple
blue
green
blue
green
purple
blue
electric blue
orange
blue
white
blue
purple
blue
blue
green
green
black
orange
matt
purple
sqlite> SELECT song, pet FROM students WHERE color = "blue" AND date = "12/25";
Clair De Lune|owl
STAY|sea otter
Clair De Lune|dog
All I want for Christmas|fox
Smells like Teen Spirit|giraffe
Shake It Off|cat
STAY|dog
```

Remember to end each statement with a `;`! To exit out of SQLite, type `.exit` or `.quit` or hit `Ctrl-C`.

### Q2: Go Bears! (And Dogs?)

Now that we have learned how to select columns from a SQL table, let's filter the results to see some more interesting results!

It turns out that 61A students have a lot of school spirit: the most popular favorite color was `'blue'`. You would think that this school spirit would carry over to the pet answer, and everyone would want a pet bear! Unfortunately, this was not the case, and the majority of students opted to have a pet `'dog'` instead. That is the more sensible choice, I suppose...

Write a SQL query to create a table that contains both the column `color` and the column `pet`, using the keyword `WHERE` to restrict the answers to the most popular results of color being `'blue'` and pet being `'dog'`.

You should get the following output:

```
sqlite> SELECT * FROM bluedog;
blue|dog
blue|dog
blue|dog
blue|dog
blue|dog
blue|dog
blue|dog
blue|dog
blue|dog
blue|dog
blue|dog
blue|dog
blue|dog
blue|dog
blue|dog
blue|dog
```

```
CREATE TABLE bluedog AS
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";
```

This isn't a very exciting table, though. Each of these rows  represents a different student, but all this table can really tell us is how many students both like the color blue and want a dog as a pet,  because we didn't select for any other identifying characteristics.  Let's create another table, `bluedog_songs`, that looks just like `bluedog` but also tells us how each student answered the `song` question.

You should get the following output:

```
sqlite> SELECT * FROM bluedog_songs;
blue|dog|Clair De Lune
blue|dog|Shake It Off
blue|dog|Old Town Road
blue|dog|Dancing Queen
blue|dog|Old Town Road
blue|dog|Clair De Lune
blue|dog|Dancing Queen
blue|dog|Clair De Lune
blue|dog|STAY
blue|dog|Old Town Road
blue|dog|Shake It Off
blue|dog|STAY
blue|dog|Clair De Lune
blue|dog|Clair De Lune
blue|dog|STAY
blue|dog|Clair De Lune
```

```
CREATE TABLE bluedog_songs AS
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";
```

This distribution of songs actually largely represents the  distribution of song choices that the total group of students made, so  perhaps all we've learned here is that there isn't a correlation between a student's favorite color and desired pet, and what song they could  spend the rest of their life listening to. Even demonstrating that there is no correlation still reveals facts about our data though!

#### Answer

```
CREATE TABLE bluedog AS
  SELECT color, pet FROM students WHERE color = 'blue' AND pet = 'dog';

CREATE TABLE bluedog_songs AS
  SELECT color, pet, song FROM students WHERE color = 'blue' AND pet = 'dog';
```

### Q3: The Smallest Unique Positive Integer

Who successfully managed to guess the smallest unique positive integer value? Let's find out!

Write an SQL query to create a table with the columns `time` and `smallest` which contains the timestamp for each submission that made a unique guess for the smallest unique positive integer - that is, only one person put that number for their guess of the smallest unique integer. Also include their guess in the output.

> *Hint:* Think about what attribute you need to `GROUP BY`. Which groups do we want to keep after this? We can filter this out using a `HAVING` clause. If you need a refresher on aggregation, see the topics section.

The submission with the timestamp corresponding to the minimum value of this table is the timestamp of the submission with the smallest unique positive integer!

#### Answer

```sql
CREATE TABLE smallest_int_having AS
  SELECT time, smallest FROM students GROUP BY smallest HAVING COUNT(smallest) = 1;
  -- or HAVING COUNT(*) = 1;
```

### Q4: Matchmaker, Matchmaker

Did you take 61A with the hope of finding a new group of friends? Well you're in luck! With all this data in hand, it's easy for us to find your perfect match. If two students want the same pet and have the same taste in music, they are clearly meant to be friends! In order to provide some more information for the potential pair to converse about, let's include the favorite colors of the two individuals as well!

In order to match up students, you will have to do a join on the `students` table with itself. When you do a join, SQLite will match every single row with every single other row, so make sure you do not match anyone with themselves, or match any given pair twice!

> **Important Note:** When pairing the first and second person, make sure that the first person responded first (i.e. they have an earlier `time`). This is to ensure your output matches our tests.
>
> *Hint:* When joining table names where column names are the same, use dot notation to distinguish which columns are from which table: `[table_name].[column name]`. This sometimes may get verbose, so it’s stylistically better to give tables an alias using the `AS` keyword. The syntax for this is as follows:
>
> ```
> SELECT <[alias1].[column name1], [alias2].[columnname2]...>
>     FROM <[table_name1] AS [alias1],[table_name2] AS [alias2]...> ...
> ```
>
> The query in the [football example](https://cs61a.org/lab/lab13/#joins) from earlier uses this syntax.

Write a SQL query to create a table that has 4 columns:

- The shared preferred `pet` of the pair
- The shared favorite `song` of the pair
- The favorite `color` of the first person
- The favorite `color` of the second person

#### Answer

```
CREATE TABLE matchmaker AS
  SELECT a.pet, a.song, a.color, b.color FROM students AS a, students AS b WHERE a.pet = b.pet AND a.song = b.song AND a.time < b.time;
```

### Q5: Sevens

Let's take a look at data from both of our tables, `students` and `numbers`, to find out if students that really like the number 7 also chose `'7'` for the obedience question. Specifically, we want to look at the students that fulfill the below conditions:

Conditions:

- reported that their favorite number (column `number` in `students`) was 7
- have `'True'` in column `'7'` in `numbers`, meaning they checked the number `7` during the survey

In order to examine rows from both the `students` and the `numbers` table, we will need to perform a join.

How would you specify the `WHERE` clause to make the `SELECT` statement only consider rows in the joined table whose values all correspond to the same student? If you find that your output is massive and overwhelming, then you are probably missing the necessary condition in your `WHERE` clause to ensure this.

> *Note:* The columns in the `numbers` table are strings with the associated number, so you must put quotes around the column name to refer to it. For example if you alias the table as `a`, to get the column to see if a student checked 9001, you must write `a.'9001'`.

**Write a SQL query to create a table with just the column `seven` from `students`, filtering first for students who said their favorite number (column `number`) was 7 in the `students` table and who checked the box for seven (column `'7'`) in the `numbers` table.**

The first 10 lines of this table should look like this:

```
sqlite> SELECT * FROM sevens LIMIT 10;
seven
7
7
7
7
the number 7 below.
the number 7 below.
7
the number 7 below.
7
```

#### Answer

```sql
CREATE TABLE sevens AS
  SELECT seven FROM students, numbers WHERE students.time = numbers.time AND students.number = 7 AND numbers."7" ="True";
```

#### Solution

```sql
CREATE TABLE sevens AS
  SELECT s.seven FROM students AS s, numbers AS c WHERE s.number = 7 AND c.'7' = 'True' AND s.time = c.time;
```

### Q6: Average Difference

Let's try to find the average absolute difference between every person's favorite number `number` and their guess at the smallest number anyone will put, `smallest`, rounded to the closest number.

For example, suppose two students put the following:

```
| number | smallest |
| ------ | -------- |
| 10     | 1        |
| 2      | 3        |
```

Then, average absolute difference is (abs(10-1) + abs(2-3)) / 2 = 5.0.

Create a table that contains one row with one value, the rounded  value of the average absolute difference between every person's favorite number and their guess at the smallest value.

> Hints:
>
> - `abs` is a `sqlite3` function that returns the absolute value of the argument.
> - `round` is a function that rounds the value of the argument.
> - `avg` is a function that returns the average value in a set.

#### Answer

```sql
CREATE TABLE avg_difference AS
  SELECT round(avg(abs(number - smallest))) FROM students;
  -- SELECT round(avg(abs(number - smallest))) as avg_difference FROM students;
```