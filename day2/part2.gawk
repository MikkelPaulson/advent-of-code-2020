BEGIN { total = 0; }
{
    match($0, /([[:digit:]]+)-([[:digit:]]+) ([[:alpha:]]): ([[:alpha:]]+)/, matches);
    index1 = matches[1];
    index2 = matches[2];
    char = matches[3];
    passwd = matches[4];

    passwd_char1 = substr(passwd, index1, 1);
    passwd_char2 = substr(passwd, index2, 1);

    xor(passwd_char1 == char, passwd_char2 == char) ? ++total : 0;
}
END { print total; }
