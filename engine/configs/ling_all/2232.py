CONFIG = dict(
    num=2232, title='向表达式添加括号后的最小结果', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='枚举括号位置（Go 原文转写）', tags=[],
    code='''
class Solution:
    def minimizeResult(self, expression: str) -> str:
        ans = ""
        sp = expression.split("+")
        l, r = sp[0], sp[1]
        min = inf
        for i in range(len(l)):  # 枚举左括号插入位置
            a = 1
            if i > 0:
                a = int(l[:i])  # 左括号左边的数（不存在时为 1）
            b = int(l[i:])  # 左括号右边的数
            for j in range(1, len(r) + 1):  # 枚举右括号插入位置
                c = int(r[:j])  # 右括号左边的数
                d = 1
                if j < len(r):
                    d = int(r[j:])  # 右括号右边的数（不存在时为 1）
                res = a * (b + c) * d
                if res < min:
                    min = res
                    ans = f"{l[:i]}({l[i:]}+{r[:j]}){r[j:]}"
        return ans
''',
    call='Solution().minimizeResult("247+38")',
    expect='2(47+38)',
    views=[
        dict(type='string', var='l', label='l（+ 左边）', pointers={'i': 'blue'}, h=170),
        dict(type='string', var='r', label='r（+ 右边）', pointers={'j': 'pink'}, h=170),
        dict(type='text', fn=lambda S: (f"`{S['a']}` × (`{S['b']}` + `{S['c']}`) × `{S['d']}` = =={S['res']}==") if 'res' in S and 'd' in S else '', size=36, h=130),
        dict(type='text', fn=lambda S: ('当前最优：' + (S['ans'] or '（还没有）')) if 'ans' in S else '', size=34, h=80),
    ],
    watch=['i', 'j', 'a', 'b', 'c', 'd', 'res', ('min', 'min', 'green')],
    captions={
        'ans = ""': '`ans` 记录目前最小结果对应的表达式',
        'sp = expression.split': '按 `+` 拆成左右两个数',
        'l, r = sp': '`l = {l}`，`r = {r}`',
        'min = inf': '`min` 记录目前最小值，初始无穷大',
        'for i in range': lambda S, B, r: f'左括号插在 `l` 的第 `{S.i}` 个字符前',
        'a = 1': '`a` 默认 1：左括号左边没有数时相当于乘 1',
        'a = int(l[:i])': '左括号左边的数 `a = {a}`',
        'b = int(l[i:])': '左括号右边的数 `b = {b}`',
        'for j in range': lambda S, B, r: f'右括号插在 `r` 的前 `{S.j}` 个字符之后',
        'c = int': '右括号左边的数 `c = {c}`',
        'd = 1': '`d` 默认 1：右括号右边没有数时相当于乘 1',
        'd = int(r[j:])': '右括号右边的数 `d = {d}`',
        'res = a': '算出 `{a} × ({b} + {c}) × {d}` = =={res}==',
        'if res < min': lambda S, B, r: f'`{S.res} < {S.min if False else B.min}`？' + ('更小 → 更新答案' if S.res < B.min else '不更小 → 跳过'),
        'min = res': '最小值更新为 `{min}`',
        'ans = f': '记下表达式：`{ans}`',
        'return ans': '最小结果的表达式是 `{ret}`',
    },
    cards=dict(
        one_liner='表达式只有十位，直接枚举两个括号的位置',
        complexity='时间 `O(n²)`，空间 `O(n)`',
        problem=['在 `num1+num2` 里加一对括号：左括号在 `+` 左、右括号在 `+` 右',
                 '使 `a×(b+c)×d` 最小，括号外没有数时当作 1',
                 '示例：`"247+38"` → `"2(47+38)"`'],
        quote='for i, min := 0, math.MaxInt64; i < len(l); i++ { // 枚举左括号插入位置 …… for j := 1; j <= len(r); j++ { // 枚举右括号插入位置',
        quote_src='—— 灵茶山艾府题解（Go 代码）',
        idea=['左括号只有 `len(l)` 个位置，右括号只有 `len(r)` 个位置',
              '括号把式子切成 `a`、`b`、`c`、`d` 四段，括号外缺失的段按 1 算',
              '双层枚举，比较乘积，严格更小才更新'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`math.MaxInt64` → `inf`，`Sprintf` → f 字符串）',
                 '时间 `O(n²)`（`n ≤ 10`），空间 `O(n)`',
                 '易错：括号外没有数时是 1 而不是 0；右括号 `j` 从 1 开始，括号里 `c` 不能为空'],
    ),
)
