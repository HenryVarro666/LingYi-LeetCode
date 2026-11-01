def _txt(S):
    if 'ans' not in S:
        return ''
    cur = f"当前读到 `{S['a']}/{S['b']}`，" if 'a' in S else ''
    return f"{cur}累计 `ans` = =={S['ans'].numerator}/{S['ans'].denominator}=="


CONFIG = dict(
    num=592, title='分数加减运算', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='有理数类逐个累加（Go 原文转写）',
    code='''
class Solution:
    def fractionAddition(self, expression: str) -> str:
        ans = Fraction(0, 1)
        for a, b in re.findall(r'([+-]?\\d+)/(\\d+)', expression):
            a, b = int(a), int(b)
            ans += Fraction(a, b)
        return f'{ans.numerator}/{ans.denominator}'
''',
    setup='import re\nfrom fractions import Fraction',
    call='Solution().fractionAddition("-1/2+1/3-1/4+1/6")',
    expect='-1/4',
    views=[
        dict(type='string', var='expression', label='expression（按 ±分子/分母 逐个读出）', cell=60, h=170),
        dict(type='text', fn=_txt, size=36, h=120),
    ],
    watch=[('a', 'a', 'blue'), ('b', 'b', 'pink'), ('ans', 'str(ans)', 'green')],
    captions={
        'ans = Fraction': '`ans` 从有理数 `0/1` 开始，Fraction 会自动约分',
        'for a, b in': lambda S, B, ret: (f"读出下一个分数：分子 `{S.a}`（带符号），分母 `{S.b}`" if 'a' in S and S.get('a') != B.get('a') or 'a' not in B
                                           else '分数都读完了'),
        'a, b = int': '转成整数：`a = {a}`，`b = {b}`',
        'ans += Fraction': '`ans` 加上 `{a}/{b}` → =={ans.numerator}/{ans.denominator}==（已自动化成最简）',
        'return': '读不到分数了，返回 `ans` 的字符串形式 `{ret}`（整数也会是 `x/1`）',
    },
    cards=dict(
        one_liner='直接用有理数类累加，约分、通分都交给它',
        complexity='时间 `O(n)`（n 为分数个数，忽略大整数运算），空间 `O(1)`',
        problem=['给字符串 `expression`，由 `±分子/分母` 组成，计算加减结果',
                 '结果必须是最简分数；整数也要写成 `x/1`',
                 '示例：`"-1/2+1/2+1/3"` → `"1/3"`；本视频：`"-1/2+1/3-1/4+1/6"` → `"-1/4"`'],
        quote='ans := big.NewRat(0, 1) ……  fmt.Fscanf(in, "%d/%d", &a, &b) …… ans.Add(ans, big.NewRat(a, b))',
        quote_src='—— 灵茶山艾府题解（Go 代码）',
        idea=['`%d/%d` 能把带符号的分子和分母一次读出来，减号当作负的分子，不用手写分隔',
              '每读一个分数，就加到 `ans` 上；有理数类内部自动通分、约分',
              '读不到分数就结束，`ans.String()` 直接是最简分数'],
        summary=['原文为 Go，已按原逻辑转写为 Python：`big.Rat` → `Fraction`，`Fscanf("%d/%d")` → `re.findall` 逐个读出，`import` 放在 setup 里',
                 '原文是死循环读到 `n == 0` 返回，转写后改成遍历所有匹配，效果相同',
                 '时间 `O(n)`，空间 `O(1)`',
                 '易错：整数结果也要输出 `x/1`，`Fraction` 的分母恒为 1，正好满足',
                 '同类题：需要精确分数运算时优先考虑有理数类'],
    ),
)
