CONFIG = dict(
    num=1881, title='插入后的最大值', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='字符串贪心 · 找第一个插入位置（Go 原文转写）',
    tags=['灵神题单', '贪心与思维', '难度分 1381'],
    code='''
class Solution:
    def maxValue(self, n: str, x: int) -> str:
        y = chr(ord('0') + x)
        i = 0
        if n[0] != '-':
            while i < len(n) and n[i] >= y:
                i += 1
        else:
            i = 1
            while i < len(n) and n[i] <= y:
                i += 1
        return n[:i] + y + n[i:]
''',
    call='Solution().maxValue("-135792", 6)',
    expect="-1356792",
    views=[
        dict(type='text', fn=lambda S: (f"插入位置 `i = {S['i']}`：左边 `{S['n'][:S['i']]}` 保持不动，右边 `{S['n'][S['i']:]}` 后移" if 'i' in S and S['_line'] >= 5 else f"在 `n = {S['n']}` 里插入数字 `{S['x']}`"), size=26),
        dict(type='string', var='n', pointers={'i': 'pink'}, h=260,
             color=lambda S, idx, v: 'green' if 'i' in S and idx < S['i'] and idx > 0 or ('i' in S and idx == 0 and S['n'][0] != '-' and S['i'] > 0) else None),
    ],
    watch=['x', 'y', ('i', 'i', 'pink')],
    captions={
        'y = chr': '把数字 `x = {x}` 变成字符 `y = {y!r}`，这样才能和 `n` 的每一位直接比较',
        'if n[0] != ': lambda S, B, r: ('`n[0]` 不是负号 → ==正数==：要让大的数字排在高位' if S.n[0] != '-' else '`n[0]` 是负号 → ==负数==：绝对值越小越大，要让小的数字排在高位'),
        'while i < len(n) and n[i] >= y': lambda S, B, r: (f"`n[{S.i}] = '{S.n[S.i]}' >= '{S.y}'` → 左边这一位不比 `x` 小，==x 还得往后放==" if S.i < len(S.n) and S.n[S.i] >= S.y else (f'`i = {S.i}` 走到末尾 → 插在最后' if S.i >= len(S.n) else f"`n[{S.i}] = '{S.n[S.i]}' < '{S.y}'` → ==插在这里，让更大的 x 占住这一位=="),),
        'while i < len(n) and n[i] <= y': lambda S, B, r: (f"`n[{S.i}] = '{S.n[S.i]}' <= '{S.y}'` → 这一位不比 `x` 大，==x 还得往后放==" if S.i < len(S.n) and S.n[S.i] <= S.y else (f'`i = {S.i}` 走到末尾 → 插在最后' if S.i >= len(S.n) else f"`n[{S.i}] = '{S.n[S.i]}' > '{S.y}'` → ==插在这里，让更小的 x 占住这一位==")),
        'i += 1': '`i` → {i}',
        'i = 1': '跳过负号，从下标 `1` 开始找',
        'return n[:i]': '拼接 `n[:{i}]` + `{y}` + `n[{i}:]` = =={ret}==',
    },
    cards=dict(
        one_liner='找第一个"比 x 小"（正数）或"比 x 大"（负数）的位置插入',
        complexity='时间 `O(n)`，空间 `O(n)`（拼接新字符串）',
        problem=['大整数 `n` 用字符串表示，可能是负数',
                 '在任意位置（不能在负号左边）插入数字 `x`，使数值最大',
                 '示例：`n = "-13", x = 2` → `"-123"`'],
        quote='对于正数，插入位置左侧的数字都必须 ≥ x；对于负数，插入位置左侧的数字都必须 ≤ x',
        quote_src='—— 灵茶山艾府题解',
        idea=['正数：高位越大越好，只要左边都 ≥ x，就一直往右走',
              '负数：高位越小越好，只要左边都 ≤ x，就一直往右走',
              '停下的位置就是插入点，一次遍历即可'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n)`，空间 `O(n)`',
                 '易错点：负数要从下标 1 开始，不能插在负号左边',
                 '`>=`、`<=` 带等号：相等时继续右移（如 `231` 插 `2` 得 `2321`）'],
    ),
)
