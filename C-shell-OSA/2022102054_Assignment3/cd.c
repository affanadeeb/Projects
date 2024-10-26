#include "headers.h"

int exec_cd(char* command, char* home_dir, char* previous_dir)
{
    if (strcmp(command, "cd") != 0 && strncmp(command, "cd ", 3) != 0) {
        return -1;  // Not valid cd command
    }

    char* tokens[10];
    int token_count = 0;
    char* token = strtok(command, " ");
    while (token != NULL && token_count < 10) {
        tokens[token_count++] = token;
        token = strtok(NULL, " ");
    }

    if (token_count > 2) {
        printf("cd: too many arguments\n");
        return -1;
    }

    char* path = (char*) malloc(sizeof(char) * 1000);
    bzero(path, 1000);  
    char* pre_dir_storer = (char*) malloc(sizeof(char) * std_path_sz);
    getcwd(pre_dir_storer, std_path_sz);

    if (token_count == 1) {
        strcpy(path, home_dir);
    } else {
        rearrange(path, tokens[1], home_dir, previous_dir);
    }

    // Converting to absolute path if it's a relative path
    if (path[0] != '/') {
        char* abs_path = (char*) malloc(sizeof(char) * 1000);
        getcwd(abs_path, 1000);
        strcat(abs_path, "/");
        strcat(abs_path, path);
        strcpy(path, abs_path);
        free(abs_path);
    }

    strcpy(previous_dir, pre_dir_storer);
    printf("Final Path: %s\n", path);

    if (chdir(path) == 0) {
        free(path);
        free(pre_dir_storer);
        return successful;
    } else {
        perror("cd");
        free(path);
        free(pre_dir_storer);
        return -1;
    }
}

void rearrange(char* path, char* token, char* home_dir, char* previous_dir)
{
    if (strcmp(token, ".") == 0) {
        char* cwd = (char*) malloc(sizeof(char) * std_path_sz);
        getcwd(cwd, std_path_sz);
        strcpy(path, cwd);
        free(cwd);
    }
    else if (strcmp(token, "..") == 0) {
        char* cwd = (char*) malloc(sizeof(char) * std_path_sz);
        getcwd(cwd, std_path_sz);
        strcpy(path, cwd);
        free(cwd);
        remove_slash(path);
    }
    else if (strcmp(token, "~") == 0) {
        strcpy(path, home_dir);
    }
    else if (strcmp(token, "-") == 0) {
        strcpy(path, previous_dir);
    }
    else if (token[0] == '~') {
        strcpy(path, home_dir);
        strcat(path, token + 1);  
    }
    else if (token[0] == '/') {
        strcpy(path, token);
    }
    else {
        getcwd(path, std_path_sz);
        strcat(path, "/");
        strcat(path, token);
    }
}

void remove_slash(char* path)
{
    for (int i = strlen(path) - 1; i >= 0; i--) {
        if (path[i] == '/') {
            path[i] = '\0';
            break;
        }
    }
}