"""https://adventofcode.com/2020/day/4"""

import re


def part1(stdin, stdout, stderr):
    """
    ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
    byr:1937 iyr:2017 cid:147 hgt:183cm

    iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
    hcl:#cfa07d byr:1929

    hcl:#ae17e1 iyr:2013
    eyr:2024
    ecl:brn pid:760753108 byr:1931
    hgt:179cm

    hcl:#cfa07d eyr:2025 pid:166559648
    iyr:2011 ecl:brn hgt:59in

    Count the number of valid passports - those that have all required fields.
    Treat cid as optional. In your batch file, how many passports are valid?
    """

    passports = parse(stdin)

    valid_passports = 0
    required_keys = ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid")

    def validate(passport):
        for key in required_keys:
            if key not in passport:
                return False

        return True

    for passport in passports:
        stderr.write(f"{passport}\n")
        if validate(passport):
            valid_passports += 1

    stdout.write(f"{valid_passports}\n")


def parse(stdin):
    """Parse a raw passport input."""

    return [
        dict(
            x.split(":")
            for x in re.split(r"[\n ]", y)
        )
        for y in stdin.read().strip().split("\n\n")
    ]
