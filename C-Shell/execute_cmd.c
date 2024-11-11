#include "headers.h"

void exec_iso_cmd(char* command, char* home_dir, int* exit_code, char* previous_dir)
{
    int action = 0;
    if(strncmp(command, "hello", 5) == 0)               // Hello message
        action = exec_hello();
    else if(strncmp(command, "cl", 2) == 0)             // Commands List
        action = exec_cmd_list();
    else if(strncmp(command, "cd", 2) == 0)           // Changing Directory
        action = exec_cd(command, home_dir, previous_dir);
    else if(strncmp(command, "pwd", 3) == 0)            // Present working DIrectory
        action = exec_pwd();
    else if(strncmp(command, "echo", 4) == 0)           // Echo Command
        action = exec_echo(command);
    else if(strncmp(command, "history", 7) == 0)        // history command
        action = exec_history();
    else if(strncmp(command, "exit", 4) == 0)           // Exit shell command
        *exit_code = 1;
    else
        printf("Please enter the correct command\n");

    if(*exit_code == 0 && action != successful)
    {
        printf("Command %s is unsuccessful\n", command);
    }
}