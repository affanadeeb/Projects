#include "headers.h"

int exec_echo(char* command)
{
    char *outfinal = malloc(strlen(command) + 1);
       
    cut_string(command, 5);
    if (command[0] == '"' && command[strlen(command)-1]=='"')
    {
        cut_string(command, 1);
        command[strlen(command)-1] = '\0';
        strcpy(outfinal, command);
    }
    else
    {
        int j=0;
        for (int i = 0; i < strlen(command); i++)
        {
            if (command[i]=='\t')
            {
                command[i]=' ';
            }
            
            if (i > 0 && (command[i] == ' ') && (command[i - 1] == ' '))
            {
                continue;
            }
            outfinal[j++]=command[i];
        }
        outfinal[j] = '\0';
        
    }
    
    printf("%s\n", outfinal);
    free(outfinal);
    return 1;
}