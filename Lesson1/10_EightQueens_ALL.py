def fitness(individual):
    """Calculate the fitness of an individual.
    The fitness is defined as the number of non-conflicting
    pairs of queens. The maximum fitness for 8 queens is 28,
    which occurs when no queens threaten each other."""

    non_conflicts = 0
    for i in range(len(individual)):
        for j in range(i + 1, len(individual)):
            if individual[i] != individual[j] and abs(i - j) != abs(
                individual[i] - individual[j]
            ):
                non_conflicts += 1
    return non_conflicts

def to_oct_list(n: int) -> list[int]:
    """Convert a decimal number to a list of its octal digits."""

    oct_digits = []
    temp = n
    # 不断取模8得到低位
    for _ in range(8):
        oct_digits.append(temp % 8)
        temp = temp // 8
    return oct_digits


# 测试示例
if __name__ == "__main__":
    non_conflicts = 28
    total = 0
    for i in range(8**8):
        individual = to_oct_list(i)
        if fitness(individual) == non_conflicts:
            total += 1
    print(f"Total valid solutions: {total}")
