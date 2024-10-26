#include "headers.h"

// counting commands
int* count_commands(char* filename, char* command) {
    static int result[2];
    result[0] = 0;
    result[1] = 0;
    char* buffer = NULL;
    size_t len = 0;
    char* last_cmd = NULL;
    FILE* fp;

    fp = fopen(filename, "r");
    if (fp == NULL) {
        return result;
    }

    last_cmd = (char*)calloc(COMMAND_LENGTH, sizeof(char));
    if (last_cmd == NULL) {
        fclose(fp);
        return result;
    }

    while (getline(&buffer, &len, fp) != -1) {
        buffer[strcspn(buffer, "\n")] = 0;
        strncpy(last_cmd, buffer, COMMAND_LENGTH - 1);
        result[0]++;  
    }

    // Removing newline from command before comparison
    char temp_cmd[COMMAND_LENGTH];
    strncpy(temp_cmd, command, COMMAND_LENGTH - 1);
    temp_cmd[strcspn(temp_cmd, "\n")] = 0;

    if (strcmp(temp_cmd, last_cmd) == 0) {
        result[1] = 1; 
    }

    free(buffer);
    free(last_cmd);
    fclose(fp);
    return result;
}

void free_history(char** history, int count) {
    if (history) {
        for (int i = 0; i < count; i++) {
            free(history[i]);
        }
    }
}

// allocating history array
char** allocate_history(int size) {
    char** history = (char**)malloc(size * sizeof(char*));
    if (!history) {
        return NULL;
    }

    for (int i = 0; i < size; i++) {
        history[i] = (char*)malloc(COMMAND_LENGTH * sizeof(char));
        if (!history[i]) {
            free_history(history, i);  
            free(history);             
            return NULL;
        }
    }
    return history;
}

// storing commands in history
void store_commands(char* filename, char* command) {
    strcat(command, "\n");
    int* status = count_commands(filename, command);
    int valid = status[1];

    char** history = allocate_history(MAX_HISTORY);
    if (!history) {
        fprintf(stderr, "Memory allocation failed\n");
        return;
    }

    int count = 0;
    char* buffer = NULL;
    size_t len = 0;
    FILE* fp = fopen(filename, "r");

    // Reading existing history
    if (fp) {
        while (getline(&buffer, &len, fp) != -1 && count < MAX_HISTORY) {
            strncpy(history[count % MAX_HISTORY], buffer, COMMAND_LENGTH - 1);
            history[count % MAX_HISTORY][COMMAND_LENGTH - 1] = '\0';
            count++;
        }
        fclose(fp);
        free(buffer);
    }

    // Storing new command if it is not duplicate
    if (!valid && count < MAX_HISTORY) {
        strncpy(history[count], command, COMMAND_LENGTH - 1);
        history[count][COMMAND_LENGTH - 1] = '\0';
        count++;
    } else if (!valid) {
        // Shifting all leftover entries and add new command at the end
        for (int i = 0; i < MAX_HISTORY - 1; i++) {
            strcpy(history[i], history[i + 1]);
        }
        strncpy(history[MAX_HISTORY - 1], command, COMMAND_LENGTH - 1);
        history[MAX_HISTORY - 1][COMMAND_LENGTH - 1] = '\0';
    }

    // Writing back to file
    fp = fopen(filename, "w");
    if (fp) {
        for (int i = 0; i < count; i++) {
            fwrite(history[i], sizeof(char), strlen(history[i]), fp);
        }
        fclose(fp);
    }

    free_history(history, MAX_HISTORY);
    free(history);
}

int exec_history() {
    char** history = allocate_history(MAX_HISTORY);
    if (!history) {
        fprintf(stderr, "Memory allocation failed\n");
        return 0;
    }

    FILE* fp = fopen(HISTORY_FILE, "r");
    if (!fp) {
        printf("No commands in history.\n");
        free_history(history, MAX_HISTORY);
        free(history);
        return 0;
    }

    int count = 0;
    char* buffer = NULL;
    size_t len = 0;

    while (getline(&buffer, &len, fp) != -1 && count < MAX_HISTORY) {
        strncpy(history[count], buffer, COMMAND_LENGTH - 1);
        history[count][COMMAND_LENGTH - 1] = '\0';
        count++;
    }

    free(buffer);
    fclose(fp);

    int num_to_print = (count < DEFAULT_DISPLAY) ? count : DEFAULT_DISPLAY;
    int start = count - num_to_print;
    
    for (int i = 0; i < num_to_print; i++) {
        printf("%d  %s", start + i + 1, history[start + i]);
    }

    free_history(history, MAX_HISTORY);
    free(history);
    return 1;
}