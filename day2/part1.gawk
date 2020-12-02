BEGIN { total = 0; }
{
    match($0, /([[:digit:]]+)-([[:digit:]]+) ([[:alpha:]]): ([[:alpha:]]+)/, matches);
    min = matches[1];
    max = matches[2];
    char = matches[3];
    passwd = matches[4];
    match_count = gsub(char, "", passwd);

    (min <= match_count && max >= match_count) ? ++total : 0;
}
END { print total; }
