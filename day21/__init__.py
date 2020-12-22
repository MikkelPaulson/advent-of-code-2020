"""https://adventofcode.com/2020/day/21"""

import io


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    Determine which ingredients cannot possibly contain any of the allergens in
    your list. How many times do any of those ingredients appear?
    """

    foods = parse(stdin)
    stderr.write(f"foods: {foods}\n")

    allergens = set(identify_allergens(foods).values())
    stderr.write(f"allergens: {allergens}\n")

    return sum([
        len(ingredients - allergens)
        for _, ingredients in foods
    ])


def identify_allergens(foods: list) -> dict:
    """
    Identify the allergens based on the known foods.
    """

    allergens = dict()
    for food_allergens, ingredients in foods:
        for food_allergen in food_allergens:
            if food_allergen in allergens:
                allergens[food_allergen] &= set(ingredients)
            else:
                allergens[food_allergen] = set(ingredients)

    changed = True
    while changed:
        changed = False

        for allergen, ingredients in allergens.items():
            if len(ingredients) == 1:
                for other_allergen, other_ingredients in allergens.items():
                    if other_allergen != allergen and \
                            ingredients.issubset(other_ingredients):
                        other_ingredients -= ingredients
                        changed = True

    return {k: v.pop() for k, v in allergens.items()}


def parse(stdin: io.TextIOWrapper) -> list:
    """
    Parse the input into a list of tuples, the first element being a set of
    allergens and the second a set of ingredients
    """

    result = list()
    for line in stdin.read().strip().splitlines():
        ingredients, allergens = line.strip(")").split(" (contains ")
        result.append((set(allergens.split(", ")), set(ingredients.split())))

    return result
