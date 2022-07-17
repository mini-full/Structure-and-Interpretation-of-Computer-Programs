# Lab 0: Getting Started

## Introduction

This lab explains how to use your own computer to complete assignments for CS 61A and introduces some of the basics of Python.

## Setup

### Install a terminal

### Install Python 3

### Install a text editor

- [Visual Studio Code](https://inst.eecs.berkeley.edu/~cs61a/fa20/articles/vscode.html)
- [Atom](https://inst.eecs.berkeley.edu/~cs61a/fa20/articles/atom.html)
- [Sublime Text 3](https://inst.eecs.berkeley.edu/~cs61a/fa20/articles/sublime.html)
- [Emacs](https://inst.eecs.berkeley.edu/~cs61a/fa20/articles/emacs.html)
- [Vim](https://inst.eecs.berkeley.edu/~cs61a/fa20/articles/vim.html)

## Using the terminal

The important part is that the prompt shows `$` (indicating Bash) or `PS` (PowerShell). If you see `C:\Users\Oski>` but no `PS` before it, you're in the Command Prompt! Do *not* use that! Close it, and launch Git-Bash or PowerShell instead. (Do *not* launch Git-CMD.)

Try running `echo "$HOME"`. Verify that it displays the path to your home directory.

#### Python Interpreter

## Organizing your files (UNIX tutorial)

### Terminology

- **Terminal**: a program that allows users to enter commands to  control the computer

- **Prompt**: displays certain information every time the terminal is  ready to receive new commands. For example, your prompt might look  something like this:

  ```
  user@computer~$
  ```

  Usually, prompts will tell you your current directory (in the example  above, the current directory is `~`)

- **Directory**: the same thing as a folder. Directories can contain  files as well as other directories

- **Parent directory**: the directory that is immediately above the  current directory (i.e. one directory up). This is represented in  UNIX as two dots, `..`

- **Current directory**: the directory that we are currently looking  at. This is represented in UNIX as a single dot, `.`

- **Home directory**: the top-level directory that contains all of your  files and sub-directories. This is represented in UNIX as a tilde,  `~`.

### Directories
* `ls`: list the files and folders inside of the current
  directory
* `mkdir`: make a new directory. For example, `mkdir lab0` creates a directory called `lab0`
* `cd`: change directories. For example, `cd lab0` changes directories to `lab0`
* `rm -r`: remove a specified directory. For example, `rm -r lab0` removes the `lab0` directory and all files and subdirectories inside it.

### Files
* `cat`: displays the contents of a file on the screen. For example, `cat unix.txt` shows the contents of the file `unix.txt`
* `mv`: moves a file/directory to another file/directory. For example, `mv file1 file2` moves the contents of `file1` into a (possibly new) file called `file2`. When moving one file to another, we are effectively renaming the file!
* `cp`: copies a file to another file/directory. For example, `cp file1 file2` copies the contents of `file1` into a file named `file2`.
* `rm`: removes a file. For example, `rm file1` deletes the file called `file1`.

### Miscellaneous
* `echo`: displays words on the screen
* `man`: displays manual pages for a specified command

### Getting Help

If you ever come across a terminal command with which you are unfamiliar, you can use a command called `man`:

```
man ls
```

The `man` command will show the **man**ual pages (reference pages) for another command. In the example above, we ask the terminal to show the manual pages for the `ls` command. As you skim through the manual pages, you'll notice that `ls` can do a lot more than just list the contents of a directory! `man` is a great way to learn more about new commands and even commands that you think you already know.

> **Note**: Some school computers do not have the `man` command installed, so you might get an error. That's okay -- if `man` ever fails, Google is your friend!

## Python Basics

### Expressions and statements

Programs are made up of expressions and statements. An *expression* is a piece of code that evaluates to some value and a *statement* is one or more lines of code that make something happen in a program.

When you enter a Python expression into the interactive Python interpreter, its value will be displayed. As you read through the following examples, try out some similar expressions on your own Python interpreter, which you can start up by typing this in your terminal:

```
python3
```

> Remember, if you are using Windows and the `python3` command doesn't work, try using `python` or `py`. See the [install Python 3](https://inst.eecs.berkeley.edu/~cs61a/fa20/lab/lab00/#install-python-3) section for more info and ask for help if you get stuck!

### Primitive expressions

Primitive expressions only take one step to evaluate. These include numbers and booleans, which just evaluate to themselves.

```
>>> 3
3
>>> 12.5
12.5
>>> True
True
```

### Arithmetic expressions

Numbers may be combined with mathematical operators to form compound expressions. In addition to the `+` operator (addition), the `-` operator (subtraction), the `*` operator (multiplication) and the `**` operator (exponentiation),  there are three division-like operators to remember:

- Floating point division (`/`): divides the first number number by the second,  evaluating to a number with a decimal point *even if the numbers divide evenly*.
- Floor division (`//`): divides the first number by the second and then rounds down, evaluating to an integer.
- Modulo (`%`): evaluates to the positive remainder left over from division.

Parentheses may be used to group subexpressions together; the entire expression is evaluated in PEMDAS order.

```
>>> 7 / 4
1.75
>>> (2 + 6) / 4
2.0
>>> 7 // 4        # Floor division (rounding down)
1
>>> 7 % 4         # Modulus (remainder of 7 // 4)
3
```

### Assignment statements

An assignment statement consists of a name and an expression. It changes the state of the program by evaluating the expression to the right of the `=` sign and *binding* its value to the name on the left.

```
>>> a = (100 + 50) // 2
```

Now, if we evaluate `a`, the interpreter will display the value 75.

```
>>> a
75
```

## Doing the assignment

### Unlocking tests

One component of lab assignments is to predict how the Python interpreter will behave.

Enter the following in your terminal to begin this section:

```
python3 ok -q python-basics -u
```

### Understanding problems

Labs will also consist of function writing problems. Open up `lab00.py` in your text editor. You can type `open .` on MacOS or `start .` on Windows to open the current directory in your Finder/File Explorer. Then double click or right click to open the file in your text editor. You should see something like this:

```
def twenty_twenty():
    """Come up with the most creative expression that evaluates to 2020,
    using only numbers and the +, *, and - operators.

    >>> twenty_twenty()
    2020
    """
    return ______
```

The lines in the triple-quotes `"""` are called a **docstring**, which is a description of what the function is supposed to do. When writing code in 61A, you should always read the docstring!

The lines that begin with `>>>` are called **doctests**. Recall that when using the Python interpreter, you write Python expressions next to `>>>` and the output is printed below that line. Doctests explain what the function does by showing actual Python code. It answers the question: "If we input this Python code, what should the expected output be?"

In `twenty_twenty`,

- The docstring tells you to "come up with the most creative expression that  evaluates to 2020," but that you can only use numbers and arithmetic operators  `+` (add), `*` (multiply), and `-` (subtract).
- The doctest checks that the function call `twenty_twenty()` should  return the number 2020.

> You should not modify the docstring, unless you want to add your own tests! The only part of your assignments that you'll need to edit is the code.

### Writing code

You can open VS Code in your current working directory via command line:

```
code .
```

#### VS Code Keyboard Shortcuts

VS Code has many, many keyboard shortcuts. Here are a few useful ones! (for Mac users, replace all the `Ctrl` sequences with `cmd`)

- `Ctrl-`` : open an integrated terminal in VS Code
- `Ctrl-s` : saves the current file
- `Ctrl-x` : cuts the entire line your cursor is on
- `Ctrl-v` : pastes the entire line you cut in the line above your  cursor OR pastes the selected text in place
- `Ctrl-z` : undo
- `Ctrl-shift-z` : redo
- `tab` : indent a line or a group of lines
- `shift-tab` : dedent a line or a group of lines
- `Ctrl-d` : highlights the current word. For every  `Ctrl-d` you type after this first word, it will highlight every next  instance of the word. This allows you to easily rename variables with  multiple cursors! (Play around with this one, it's fun and very practical!)
- `Ctrl-tab` : moves you to the next tab (`Ctrl` on Mac as well)
- `Ctrl-shift-tab` : moves you to the previous tab (`Ctrl` on Mac as well)
- `Ctrl-f` : search for a word
- `Ctrl-shift-f` : searches through all tabs

### Running tests

In CS 61A, we will use a program called `ok` to test our code. `ok` will be included in every assignment in this class.

> For quickly generating ok commands, you can now use the [ok command generator](https://links.cs61a.org/ok-help).

- `lab00.py`: the starter file you just edited
- `ok`: our testing program
- `lab00.ok`: a configuration file for Ok

Now, let's test our code to make sure it works. You can run `ok` with this command:

```
python3 ok
```

While `ok` is the primary assignment "autograder" in CS 61A, you may find it useful at times to write some of your own tests in the form of [doctests](https://inst.eecs.berkeley.edu/~cs61a/fa20/lab/lab00/#understand-the-question). Then, you can try them out using the `-m doctest` [option for Python](#Appendix: Useful Python command line options)).

After writing some code, you can test your code with `ok` in various ways.

To test a specific question, use the `-q` option with the name of the question:

```
python3 ok -q <question>
```

You can run all the tests with the following command:

```
python3 ok
```

By default, only tests that **fail** will appear. If you want to see how you did on all tests, you can use the `-v` option:

```
python3 ok -v
```

If you do not want to send your progress to our server or you have any problems logging in, add the `--local` flag to block all communication:

```
python3 ok --local
```

More information on Ok is available [here](https://inst.eecs.berkeley.edu/~cs61a/fa20/articles/using-ok.html). You can also use the `--help` flag:

```
python3 ok --help
```

This flag works just like it does for UNIX commands we used earlier.

#### Adding your own tests

https://inst.eecs.berkeley.edu/~cs61a/fa20/articles/using-ok.html#adding-your-own-tests

## Appendix: Useful Python command line options

When running a Python file, you can use options on the command line to inspect your code further. Here are a few that will come in handy. If you want to learn more about other Python command-line options, take a look at the [documentation](https://docs.python.org/3.8/using/cmdline.html).

- Using no command-line options will run the code in the file you provide and return you to the command line.

  ```
  python3 
  ```

- **`-i`**: The `-i` option runs your Python script, then opens an interactive session. In an interactive session, you run Python code line by line and get  immediate feedback instead of running an entire file all at once. To exit,  type `exit()` into the interpreter prompt. You can also use the keyboard shortcut `Ctrl-D` on Linux/Mac machines or `Ctrl-Z Enter` on Windows.

  If you edit the Python file while running it interactively, you will need to exit and restart the interpreter in order for those changes to take effect.

  ```
  python3 -i 
  ```

- **`-m doctest`**: Runs [doctests](https://docs.python.org/3/library/doctest.html) in a particular file. Doctests are  surrounded by triple quotes (`"""`) within functions.

  Each test in the file consists of `>>>` followed by some Python code and  the expected output (though the `>>>` are not seen in the output of the  doctest command).

  ```
   python3 -m doctest 
  ```

