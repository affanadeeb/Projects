
# Affan's C Shell

Welcome to **Affan's C Shell**, a custom shell program implemented in C. This shell provides a set of built-in commands similar to those found in common Linux shells. The shell also includes a history tracking feature, allows navigation through directories, and supports common commands like `echo`, `pwd`, `cd`, and more.

## Table of Contents
- [Affan's C Shell](#affans-c-shell)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Commands](#commands)
    - [Supported Commands](#supported-commands)
  - [Usage](#usage)
    - [Examples](#examples)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Instructions](#instructions)
  - [Makefile](#makefile)
  - [Sample Session](#sample-session)

---

## Features

1. **Custom Shell Prompt**:
   - Displays in the format `<username@system_name : current_directory>`.
   - In my case it displays `affan@affan-ThinkPad-L14-Gen-4 : ~ > `
   - Dynamically shows the current working directory.
   
2. **Built-in Commands**:
   - **`hello`**: Greets the user with a welcome message.
   - **`echo`**: Displays the text passed as an argument with normalized spaces.
   - **`pwd`**: Displays the current working directory.
   - **`cd`**: Changes the current directory with advanced handling of:
     - `cd ~`: Changes to the home directory.
     - `cd -`: Changes to the previous directory.
     - `cd ..`: Moves up one directory.
     - Handles errors such as invalid directories or too many arguments.

3. **History**:
   - Tracks and stores up to 20 commands.
   - Prevents duplicate consecutive commands from being stored.
   - Persists command history across sessions in `history.txt`.
   - The `history` command displays the last 10 commands executed.

4. **Error Handling**:
   - Displays appropriate error messages for commands with incorrect syntax or missing directories.
   - Prevents incorrect usage of `cd` with multiple arguments (e.g., `cd test check`).

---

## Commands

### Supported Commands

1. **`hello`**: 
   - Usage: `hello`
   - Outputs a personalized greeting to the user.

2. **`cl`**:
   - Usage: `cl`
   - Lists all the available commands in the shell.

3. **`echo`**:
   - Usage: `echo [text]`
   - Prints the provided text as it is when in " " and with multiple spaces/tabs reduced to a single space when given as normal text i.e without double quotes.

4. **`pwd`**:
   - Usage: `pwd`
   - Prints the full path of the current working directory.

5. **`cd`**:
   - Usage: `cd [directory]`
   - Changes the current directory to the specified path.
   - `cd ~`: Moves to the home directory.
   - `cd -`: Moves to the previous directory.
   - `cd ..`: Moves one level up.
   - `cd .`: Remains in same directory
   - Handles invalid directories and prevents multiple arguments (e.g., `cd test check` gives an error).

6. **`history`**:
   - Usage: `history`
   - Displays the last 10 commands executed in the current session, stored persistently across sessions in `history.txt`.

---

## Usage

### Examples

1. **Starting the Shell**:
   ```bash
   ./a.out
   ```

2. **Running Commands**:
   - `hello`: Outputs a welcome message.
   - `echo "all the best"`: Outputs `all the best`.
   - `pwd`: Outputs the current directory path.
   - `cd test`: Changes to the `test` directory.
   - `history`: Displays the last 10 commands.

3. **Directory Navigation**:
   - `cd ~`: Moves to the home directory.
   - `cd ..`: Moves one directory up.
   - `cd -`: Moves to the previous directory.
   - `cd test/check`: Moves to the nested directory `check` inside `test`.
   - `cd test check`: Outputs an error (`cd: too many arguments`).

4. **History Example**:
   - After executing several commands, typing `history` displays the last 10 commands, such as:
     ```bash
     11 hello
     12 cl
     13 echo all the best
     14 echo "hi there"
     15 echo "hi there hello"
     16 pwd
     17 cd test
     18 cd test/check
     19 cd ..
     20 history
     ```

---

## Installation

### Prerequisites

- A working C compiler (`gcc`).
- Linux/Unix environment for running the shell.

### Instructions

1. **Compile the Program**:
   ```bash
   make
   ```

2. **Run the Shell**:
   ```bash
   ./a.out
   ```

---

## Makefile
To compile the project, simply run:

```bash
make
```
Then we will run 
```bash
./prog.out
```

---
## Sample Session

Below is a sample usage example demonstrating the usage of **C Shell**:

After successfully compiling the shell using the Makefile, here’s an example of how the shell works:

1. **Start the shell:**
   ```bash
   ./a.out
   ```

2. **Example Commands:**

   An example showing various commands being executed in this **Custom C Shell**.

   ```bash
   affan@affan-ThinkPad-L14-Gen-4:~/Downloads/2022102054$ make
   gcc -Wall -g -o prog.out main.c functions.c execute_cmd.c command_list.c hello.c cd.c pwd.c echo.c history.c
   ```

   **Starting the shell:**
   ```bash
   affan@affan-ThinkPad-L14-Gen-4:~/Downloads/2022102054$ ./prog.out 
   ```

   **Command session:**
   ```bash
   affan@affan-ThinkPad-L14-Gen-4 : ~ > hello

   Hello Mr: affan, You are now using ::: | Affan's C Shell | :::

   affan@affan-ThinkPad-L14-Gen-4 : ~ > cl
   -----------------------
   1. hello
   2. cl
   3. echo
   4. pwd (present working directory)
   5. cd (change directory)
   6. history (view past commands)
   -----------------------
   ```

   **Using the `echo` command:**
   ```bash
   affan@affan-ThinkPad-L14-Gen-4 : ~ > echo all the       best
   all the best
   ```
   ```bash
   affan@affan-ThinkPad-L14-Gen-4 : ~ > echo "hi there"
   hi there
   ```
   ```bash
   affan@affan-ThinkPad-L14-Gen-4 : ~ > echo "hi   there   hello"
   hi      there   hello
   ```
   ```bash
   affan@affan-ThinkPad-L14-Gen-4 : ~ > echo hi there      hello    
   hi there hello
   ```
   ```bash
   affan@affan-ThinkPad-L14-Gen-4 : ~ > echo "all the       best"
   all the       best
   ```

   **Using `pwd` to display the current directory:**
   ```bash
   affan@affan-ThinkPad-L14-Gen-4 : ~ > pwd
   pwd : /home/affan/Downloads/2022102054
   ```



**Changing directories with `cd`:**

```bash

affan@affan-ThinkPad-L14-Gen-4 : ~ > cd test

Final Path: /home/affan/Downloads/2022102054/test

```


**Navigating to a subdirectory with `cd`:**

```bash

affan@affan-ThinkPad-L14-Gen-4 : ~/test > cd check

Final Path: /home/affan/Downloads/2022102054/test/check

```


**Navigating back with `cd ..`:**

```bash

affan@affan-ThinkPad-L14-Gen-4 : ~/test/check > cd ..

Final Path: /home/affan/Downloads/2022102054/test

```


**Switching to the previous directory with `cd -`:**

```bash

affan@affan-ThinkPad-L14-Gen-4 : ~/test > cd -

Final Path: /home/affan/Downloads/2022102054/test/check

```


**Returning to the home directory with `cd ~`:**

```bash

affan@affan-ThinkPad-L14-Gen-4 : ~/test/check > cd ~

Final Path: /home/affan/Downloads/2022102054

```


**Testing a directory path with `cd test`:**

```bash

affan@affan-ThinkPad-L14-Gen-4 : ~ > cd test

Final Path: /home/affan/Downloads/2022102054/test

```


**Return to the default directory with `cd`:**

```bash

affan@affan-ThinkPad-L14-Gen-4 : ~/test > cd

Final Path: /home/affan/Downloads/2022102054

```


**Handling errors with `cd` (too many arguments):**

```bash

affan@affan-ThinkPad-L14-Gen-4 : ~ > cd test check

cd: too many arguments

Command cd is unsuccessful

```

   **Using history to view past commands:**
   ```bash
   affan@affan-ThinkPad-L14-Gen-4 : ~ > history
   11  hello
   12  cl
   13  echo all the        best
   14  echo "hi there"
   15  echo "hi    there   hello"
   16  echo hi there       hello
   17  pwd
   18  cd test
   19  cd test check
   20  history
   ```

This section shows the way to interact with the shell, showing the built-in commands like `hello`, `echo`, `pwd`, `cd`, and `history`.

---