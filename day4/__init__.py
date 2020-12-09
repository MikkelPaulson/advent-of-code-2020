"""https://adventofcode.com/2020/day/4"""

import re


def part1(stdin, stderr):
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

    def validate(passport):
        for key in ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"):
            if key not in passport:
                return False

        return True

    for passport in passports:
        stderr.write(f"{passport}\n")
        if validate(passport):
            valid_passports += 1

    return str(valid_passports)


def part2(stdin, stderr):
    """
    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not.
    """

    passports = parse(stdin)

    patterns = {
        k: re.compile(v) for k, v in {
            "byr": r"19[2-9][0-9]|200[0-2]",
            "iyr": r"201[0-9]|2020",
            "eyr": r"202[0-9]|2030",
            "hgt": r"1([5-8][0-9]|9[0-3])cm|(59|6[0-9]|7[0-6])in",
            "hcl": r"#[0-9a-f]{6}",
            "ecl": r"amb|blu|brn|gry|grn|hzl|oth",
            "pid": r"[0-9]{9}",
        }.items()
    }

    def validate(passport):
        for key, pattern in patterns.items():
            if key not in passport:
                stderr.write(f"Missing {key}\n")
                return False

            if not pattern.fullmatch(passport[key]):
                stderr.write(f"Invalid {key}\n")
                return False

        stderr.write("Valid\n")
        return True

    valid_passports = 0
    for passport in passports:
        stderr.write(f"{passport}\n")
        if validate(passport):
            valid_passports += 1

    return str(valid_passports)


def parse(stdin):
    """Parse a raw passport input."""

    return [
        dict(
            x.split(":")
            for x in re.split(r"[\n ]", y)
        )
        for y in stdin.read().strip().split("\n\n")
    ]
