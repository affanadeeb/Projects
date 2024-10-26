#include "headers.h"

int exec_pwd()
{
    // printf("You entered Present Working Directory\n");
    char* path = (char*) malloc(sizeof(char)*std_path_sz);
    getcwd(path, std_path_sz);
    printf("pwd : %s\n", path);
    return 1;
}