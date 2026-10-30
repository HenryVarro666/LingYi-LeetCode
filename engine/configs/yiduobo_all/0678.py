def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '未匹配左括号数的可能范围 [min, max]（绿框 = 范围）', 24, T['muted'], bold=True)
    if 'ma' not in S:
        return
    ma, mi = S['ma'], S['mi']
    N = 5
    cell = min(120, (x1 - x0 - 80) / (N + 1))
    sx = x0 + 50
    base = y0 + 150
    for k in range(N + 1):
        X = sx + k * cell
        cv.rect((X + 4, base, X + cell - 4, base + 70), fill=T['panel2'], r=8)
        cv.text((X + cell / 2, base + 35), k, 30, T['dim'], anchor='mm', bold=True)
    if ma >= 0:
        lo, hi = max(mi, 0), min(ma, N)
        cv.rect((sx + lo * cell, base - 6, sx + (hi + 1) * cell, base + 76), fill=T['green'], alpha=90, r=10)
        cv.text((sx + lo * cell + cell / 2, base - 20), f'min={mi}', 24, T['cyan'], anchor='mb', bold=True)
        cv.text((sx + hi * cell + cell / 2, base + 90), f'max={ma}', 24, T['orange'], anchor='mt', bold=True)
    else:
        cv.text((sx, base + 100), f'max = {ma} < 0：右括号太多，无解', 26, T['red'], bold=True)


def _how(S, B, ret):
    return f"char = `{S['char']}`"


CONFIG = dict(
    num=678, title='有效的括号字符串', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='贪心 · 维护左括号数量的上下界',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def checkValidString(self, s):

        ma = mi = 0
        for char in s:
            if char == '(':
                ma += 1
                mi += 1
            elif char == ')':
                ma -= 1
                mi -= 1
                if mi < 0:
                    mi = 0
            else:
                ma += 1
                mi -= 1
                if mi < 0:
                    mi = 0

            if ma < 0:
                return False

        if mi > 0:
            return False

        return True
''',
    call="Solution().checkValidString('(*))')",
    expect=True,
    views=[
        dict(type='string', var='s', label='s', h=170),
        dict(type='custom', draw=_draw, h=300),
        dict(type='text', size=26, h=56, fn=lambda S: f"当前字符 `{S['char']}`" if 'char' in S else ''),
    ],
    watch=[('max', 'ma', 'orange'), ('min', 'mi', 'cyan'), 'char'],
    captions={
        'ma = mi = 0': '`ma` = 最多可能有几个未匹配的 `(`，`mi` = 最少可能有几个，开始都是 0',
        "if char == '('": lambda S, B, r: f"读到 `{S['char']}`：" + ('是左括号' if S['char'] == '(' else '不是左括号'),
        'ma += 1\n                mi += 1': '左括号：未匹配数量上下界都 +1',
        'ma -= 1': '右括号：最多、最少都要用掉一个 `(`',
        'mi -= 1': '`mi` 减 1：`mi` = {mi}',
        'if mi < 0': lambda S, B, r: (f"`mi = {S['mi']} < 0`：最少未匹配数不能为负 → 要拉回 0" if S['mi'] < 0 else f"`mi = {S['mi']} ≥ 0`，不用调整"),
        13: '`mi` 拉回 0：负数说明有富余的 `*` 或右括号过多，可让之前的 `*` 当空串/左括号来消化，最少数量最低就是 0',
        'if ma < 0': lambda S, B, r: (f"`ma = {S['ma']} < 0`：就算所有 `*` 都当左括号，左括号还是不够 → 无解" if S['ma'] < 0 else f"`ma = {S['ma']} ≥ 0`：左括号还够，继续"),
        'if mi > 0': lambda S, B, r: (f"`mi = {S['mi']} > 0`：至少还剩 {S['mi']} 个左括号没法匹配 → False" if S['mi'] > 0 else f"`mi = 0`：存在一种取法恰好全部匹配"),
        'return True': '`mi` 为 0，可以匹配 → 返回 `True`',
    },
    cards=dict(
        one_liner='不猜每个星号，只维护左括号数量的最大和最小可能',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串只含 `(`、`)`、`*`，`*` 可当 `(`、`)` 或空串',
                 '判断字符串是否是有效括号字符串',
                 '示例：`"(*))"` → `True`；`"*)("` → `False`'],
        quote='使用两个变量max和min来记录当前最多可能有多少个左括号，以及最少可能有多少个左括号。',
        quote_src='—— yiduobo 题解原文',
        idea=['`(`：上下界都 +1；`)`：上下界都 -1',
              '`*`：最多当 `(` 所以 `ma+1`，最少当 `)` 所以 `mi-1`',
              '`ma < 0` 一定失败；`mi < 0` 就拉回 0；结束时 `mi` 必须为 0'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`mi` 小于 0 要置 0，不能直接失败',
                 '`mi != 0` 说明右括号不够，例如 `*)(`：`ma` 1→0→1，`mi` 0→0→1',
                 '原文变量叫 `max`/`min`，代码里是 `ma`/`mi`，避免覆盖内置函数'],
    ),
)
