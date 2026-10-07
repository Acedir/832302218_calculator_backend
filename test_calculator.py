from calculator import calculate, CalcError

cases = [
    ("12+8", 20),
    ("1+2*3", 7),
    ("(1+2)*3", 9),
    ("10/2+7", 12),
    ("8-3*2", 2),
    ("-5+8", 3),
    ("3*-2", -6),
    ("1.5+2.5", 4),
    ("2*(3+4)-5", 9),
    ("10/(2+3)", 2),
]

for expr, expected in cases:
    got = calculate(expr)
    status = "OK " if got == expected else "FAIL"
    print(f"[{status}] {expr} = {got}  (期望 {expected})")

# 错误用例
error_cases = ["1/0", "1++", "(1+2", "1+2)", "abc", "", "1..2"]
for expr in error_cases:
    try:
        calculate(expr)
        print(f"[FAIL] {expr!r} 应该报错但没有")
    except CalcError as e:
        print(f"[OK ] {expr!r} -> 报错：{e}")