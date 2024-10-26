#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/utsname.h>
#include <pwd.h>
#include <ctype.h>
#include <sys/wait.h>
#include <dirent.h>
#include <sys/stat.h>
#include <fcntl.h>

// ---Definings ---
#define std_cmd_sz 100
#define std_path_sz 200
#define correct_cmd 1
#define incorrect_cmd 0
#define foreground 1
#define background 0
#define successful 1
#define MAX_HISTORY 20
#define COMMAND_LENGTH 256
#define HISTORY_FILE "history.txt"
#define DEFAULT_DISPLAY 10

// --- Functions ---
int execute(char* command_bunch, char* home_dir, int* exit_code, char* previous_dir);
char* get_name();
char* get_home_dir();
char* fetch_dir(char* home_dir);
void cut_string(char *str, int length_to_cut);
char *remove_extra_spaces(char *str);
void exec_iso_cmd(char* command, char* home_dir, int* exit_code, char* previous_dir);
int exec_hello();
int exec_cmd_list();
int exec_cd(char* command, char* home_dir, char* previous_dir);
void rearrange(char* path, char* token, char* home_dir, char* previous_dir);
void remove_slash(char* path);
int exec_pwd();
int exec_echo(char* command);
void store_commands(char* filename, char* command);
int exec_history();