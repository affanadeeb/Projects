#include "headers.h"

int execute(char* command_bunch, char* home_dir, int* exit_code, char* previous_dir)
{
    char* copy_command = (char*) malloc (sizeof(char) * std_cmd_sz);
    strcpy(copy_command, command_bunch);
    char* trimmed_command = copy_command;
    if (copy_command[5] != '"')
    {
        trimmed_command = remove_extra_spaces(copy_command);
    }
    exec_iso_cmd(trimmed_command, home_dir, exit_code, previous_dir);
    return 0;
}

char* get_name()
{
    char *username = (char*) malloc (sizeof(char) * 100);

    // username
    uid_t uid = getuid();
    struct passwd *pw = getpwuid(uid);
    if (pw) {
        strcpy(username, pw->pw_name);
    }

    strcat(username, "@");

    // system name
    struct utsname sysinfo;
    if (uname(&sysinfo) == 0) {
        strcat(username, sysinfo.nodename);
    }

    return username;
}

char* get_home_dir(){
    char *cwd = (char*) malloc (sizeof(char) * std_path_sz);
    if (getcwd(cwd, std_path_sz) != NULL) {
        return cwd;
    }
    exit(0);
}

void cut_string(char *str, int length_to_cut) {
    int original_length = strlen(str);
    if (length_to_cut >= original_length) {
        bzero(str, original_length);
    } else {
        for (int i = length_to_cut; i <= original_length; i++) {
            str[i - length_to_cut] = str[i];
        }
    }
}

char* fetch_dir(char* home_dir){
    int home_len = strlen(home_dir);
    char* present_dir = get_home_dir();

    if(strncmp(present_dir, home_dir, home_len) == 0)
    {
        char *new = (char*) malloc (sizeof(char) * std_path_sz);
        bzero(new, std_path_sz);
        new[0] = '~';
        cut_string(present_dir, home_len);
        strcat(new, present_dir);
        return new;
    }
    else
        return present_dir;
}

char *remove_extra_spaces(char *str) {
    char *dest = str;
    char *data = str;
    while (*data != '\0') {
        while (isspace((unsigned char)*data) && isspace((unsigned char)*(data + 1))) {
            data++;
        }
        *dest++ = *data++;
    }
    *dest = '\0';
    return str;
}
