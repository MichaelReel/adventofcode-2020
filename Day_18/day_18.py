#!/env/python3

import re

text_file = open("Day_18/input", "r")
problems = [x.strip() for x in text_file.readlines()]

# Part 01
operator_re = r'\s(?P<op>[+*])\s'
operand_re = r'(?P<operand>\d+)'
add_multi = re.compile(r'^(?P<rest>.*)' + operator_re + operand_re + r'$')
solution = re.compile(r'^' + operand_re + r'$')


def solve_problem_p1(problem: str) -> int:
    # Check if we have the solution already
    if solution.match(problem):
        return int(problem)
    # Work right to left and recurse on parentheses
    operand: int
    operator: str
    rest: str
    match = add_multi.match(problem)
    if match:
        props = match.groupdict()
        operand = int(props['operand'])
        operator = props['op']
        rest = props['rest']
    elif problem[-1] == ')':
        # match paratheses and recurse the content in total
        paras = 0
        for ind in range(len(problem)-1, -1, -1):
            paras -= 1 if problem[ind] == '(' else 0
            paras += 1 if problem[ind] == ')' else 0
            if paras == 0:
                operand = solve_problem_p1(problem[ind+1:-1])
                return solve_problem_p1(problem[:ind] + str(operand))

    if operator == '+':
        return solve_problem_p1(rest) + operand
    elif operator == '*':
        return solve_problem_p1(rest) * operand


total = 0
for problem in problems:
    result = solve_problem_p1(problem)
    total += result
    # print("{} => {}".format(problem, result))

print("Part 01: Sum of solutions = {}".format(total))


# Part 02
multi_re = re.compile(r'^(?P<left>.*)\s\*\s(?P<right>.*)$')
add_re = re.compile(r'^(?P<left>.*)\s\+\s(?P<right>.*)$')


def solve_problem_p2(problem: str) -> int:
    # Check if we have the solution already
    if solution.match(problem):
        return int(problem)

    # Solve all parentheses first
    if '(' in problem:
        start = problem.find('(')
        paras = 0
        for ind in range(start, len(problem)):
            paras += 1 if problem[ind] == '(' else 0
            paras -= 1 if problem[ind] == ')' else 0
            if paras == 0:
                left = problem[:start]
                mid = solve_problem_p2(problem[start + 1: ind])
                right = problem[ind + 1:]
                return solve_problem_p2(left + str(mid) + right)

    multi_match = multi_re.match(problem)
    add_match = add_re.match(problem)
    if multi_match:
        left = solve_problem_p2(multi_match.groupdict()['left'])
        right = solve_problem_p2(multi_match.groupdict()['right'])
        return left * right
    elif add_match:
        left = solve_problem_p2(add_match.groupdict()['left'])
        right = solve_problem_p2(add_match.groupdict()['right'])
        return left + right

    print("dafeck: " + problem)


total = 0
for problem in problems:
    result = solve_problem_p2(problem)
    total += result
    # print("{} => {}".format(problem, result))

print("Part 02: Sum of solutions = {}".format(total))
