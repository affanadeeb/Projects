#include "headers.h"

int main(){
    char *user = get_name();                          
    char *home_dir = get_home_dir();                   
    char* previous_dir = (char*) malloc (sizeof(char) * std_path_sz);
    char* history_file = "history.txt";

    int exit_code = 0;                                  
    while(1){
        if(exit_code == 1)
            break;

        char* working_dir = fetch_dir(home_dir);        
        printf("%s : %s > ", user, working_dir);        

        char* command = (char*) malloc (sizeof(char) * std_cmd_sz);
        fgets(command, std_cmd_sz, stdin);              // Command Input --------- 
        command[strlen(command) - 1] = '\0';

        char* temp_command = strdup(command);

        store_commands(history_file, temp_command);          // Storing commands for History

        execute(command, home_dir, &exit_code, previous_dir);   // Executing the command

        free(command);        
        free(temp_command);                                  
    }
    printf("\n\nThanks For Using Our Shell Program...\n\n");    
    return 0;
}