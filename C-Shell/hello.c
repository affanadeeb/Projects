#include "headers.h"

int exec_hello()
{
    char *username = (char*) malloc (sizeof(char) * 10);

    // Get the username
    uid_t uid = getuid();
    struct passwd *pw = getpwuid(uid);
    if (pw) {
        strcpy(username, pw->pw_name);
    }
    printf("\n\nHello Mr: %s, You are now using ::: | Affan's C Shell | :::\n\n", username);
    return successful;
}