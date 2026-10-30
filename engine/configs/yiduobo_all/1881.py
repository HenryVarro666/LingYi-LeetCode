def _top(S):
    if 'index' not in S:
        return f'`n = "{S["n"]}"`，插入 `x = {S["x"]}`：先看正负号'
    i, n, x = S['index'], S['n'], S['x']
    if n[0] == '-':
        return f'负数：绝对值越小数值越大，小数字放高位：`{n[i]}` vs `{x}`'
    return f'正数：较大的数放高位：`{n[i]}` vs `{x}`'


CONFIG = dict(
    num=1881, title='插入后的最大值', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='高位向后扫 · 严格比较',
    tags=['灵神题单', '难度分 1381'],
    code='''
class Solution(object):
    def maxValue(self, n, x):
        if n[0] == '-':
            for index in range(1, len(n)):
                if int(n[index]) > x:
                    return n[:index] + str(x) + n[index:]
        else:
            for index in range(len(n)):
                if int(n[index]) < x:
                    return n[:index] + str(x) + n[index:]

        return n + str(x)
''',
    call='''Solution().maxValue("231", 2)
Solution().maxValue("-13", 2)''',
    expect='-123',
    views=[
        dict(type='text', fn=lambda S: f'`n = "{S["n"]}"`，要插入 `x = {S["x"]}`' + ('（负数）' if S['n'][0] == '-' else '（正数）') if 'n' in S else '', size=28),
        dict(type='string', var='n', label='n（粉 = 当前比较的位置）', cell=84, pointers={'index': 'pink'},
             color=lambda S, i, v: 'pink' if 'index' in S and i == S['index'] else None,
             dim=lambda S, i, v: 'index' in S and i < S['index']),
        dict(type='text', fn=lambda S: (f'比较 `int(n[{S["index"]}]) = {int(S["n"][S["index"]])}` 和 `x = {S["x"]}`：'
                                        + ('负数要找第一个 ==比 x 大==' if S['n'][0] == '-' else '正数要找第一个 ==比 x 小==')) if 'index' in S else '', size=26),
    ],
    watch=['x', ('index', 'index', 'pink')],
    captions={
        "if n[0] == '-'": lambda S, B, r: ('`n[0]` 是负号 → 数值越大 = 绝对值越小，要把==小数字==放高位' if S.n[0] == '-'
                                           else '`n[0]` 不是负号 → 正数，要把==大数字==放高位'),
        'for index in range(1': '负数：从下标 1 开始（符号位左边不能插入）',
        'for index in range(len': '正数：从最高位开始向后扫',
        'if int(n[index]) > x': lambda S, B, r: (f'`{S.n[S.index]} > {S.x}` → 成立：这一位比 x 大，x 插在它前面，高位更小 → 绝对值更小 → 数值更大' if int(S.n[S.index]) > S.x
                                                 else f'`{S.n[S.index]} > {S.x}` 不成立：这位不比 x 大，继续往后' + ('（==相等也不能插==）' if int(S.n[S.index]) == S.x else '')),
        'if int(n[index]) < x': lambda S, B, r: (f'`{S.n[S.index]} < {S.x}` → 成立：x 比这位大，插在这里放到更高位' if int(S.n[S.index]) < S.x
                                                 else f'`{S.n[S.index]} < {S.x}` 不成立：这位不比 x 小，继续往后' + ('（==相等也不能插==）' if int(S.n[S.index]) == S.x else '')),
        'return n[:index]': '在下标 `{index}` 前插入 `{x}`：`{n[:index]}` + `{x}` + `{n[index:]}` = `{ret}`',
        'return n + str(x)': '一路没有遇到可插的位置 → x 放最后：`{ret}`',
    },
    cards=dict(
        one_liner='正数把大数放高位，负数把小数放高位，严格比较',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['大整数 `n` 用字符串表示，可能是==负数==，往里任意位置插一个数字 `x`',
                 '求插入后数值最大的字符串，不能插在负号左边',
                 '示例：`n = "-13"`，`x = 2` → `"-123"`'],
        quote='在这里必须是严格的大于而不是大于等于，举个例子很容易就能说明。对于231而言，如果要插入一个2，那么插入在1的前方可以得到2321，而如果插入到2的前方得到的是2231。',
        quote_src='—— yiduobo 题解原文',
        idea=['正数：从高位开始，第一个比 `x` ==小==的位置就插入',
              '负数：绝对值越小越大，第一个比 `x` ==大==的位置就插入（跳过负号）',
              '相等不插：插在相等的前面，会把后面更值得占位的数挤后'],
        summary=['时间 `O(n)`，空间 `O(n)`（拼接字符串）',
                 '易错：必须==严格==比较，相等时继续往后',
                 '没找到位置就放末尾：`n + str(x)`',
                 '原文代码已是 Python 3 可运行写法，未做修改',
                 '灵神：正数左侧数字都 `>= x`，负数左侧都 `<= x`，本质一致'],
    ),
)
