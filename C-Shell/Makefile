# Compiler
CC = gcc

# Compiler flags
CFLAGS = -Wall -g

# Source files
SRCS = main.c functions.c execute_cmd.c command_list.c hello.c cd.c pwd.c echo.c history.c

# Header files
HEADERS = headers.h

# Executable file name
EXEC = a.out

# Default rule to build the executable
all: $(EXEC)

# Rule to build the executable
$(EXEC): $(SRCS) $(HEADERS)
	$(CC) $(CFLAGS) -o $(EXEC) $(SRCS)

# Clean up build files
clean:
	rm -f $(EXEC)

# Phony targets
.PHONY: all clean

