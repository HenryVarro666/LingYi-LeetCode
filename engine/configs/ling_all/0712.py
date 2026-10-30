S1, S2 = 'sea', 'eat'
ASSIGN = (14, 16)


def _xi(S):
    x = S.get('x')
    return S1.index(x) if isinstance(x, str) and x in S1 else None


def _fcol(S, i, v):
    j = S.get('j')
    if j is None or S.get('_line') not in (12, 13, 14, 16, 17):
        return None
    if i == j + 1:
        return 'yellow'
    line = S.get('_line')
    if line == 14:
        return None
    if line == 16 and i == j:
        return 'blue'
    return None


def _text(S, B):
    line = S.get('_line')
    if 'total' not in S:
        return '删除和最小 ⟺ ==保留和最大==：`答案 = total − 保留和 × 2`'
    if line == 14:
        return f"`{S['x']} == {S['y']}`：两边都保留 → `f[{S['j'] + 1}] = pre + ord('{S['x']}') = {B['pre']} + {S['ord_x']}` = =={S['f'][S['j'] + 1]}=="
    if line == 16:
        j = S['j']
        return f"`{S['x']} ≠ {S['y']}`：`f[{j + 1}] = max(f[{j + 1}], f[{j}]) = max({B['f'][j + 1]}, {S['f'][j]})` = =={S['f'][j + 1]}=="
    return f"`total = {S['total']}`；`f[j+1]`：s1 已扫部分与 `s2[:j+1]` 的==公共子序列最大 ASCII 和=="


CONFIG = dict(
    num=712, title='两个字符串的最小ASCII删除和', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='LCS 变形 · 一维 DP',
    tags=['labuladong', '灵神核心路线'],
    code='''
# 更快的写法见【Python3 手写 max】
class Solution:
    def minimumDeleteSum(self, s1: str, s2: str) -> int:
        m = len(s2)
        total = sum(map(ord, s1)) + sum(map(ord, s2))

        f = [0] * (m + 1)
        for x in s1:
            ord_x = ord(x)
            pre = 0  # f[0]
            for j, y in enumerate(s2):
                tmp = f[j + 1]
                if x == y:
                    f[j + 1] = pre + ord_x
                else:
                    f[j + 1] = max(f[j + 1], f[j])
                pre = tmp
        return total - f[m] * 2
''',
    call=f'Solution().minimumDeleteSum({S1!r}, {S2!r})',
    expect=231,
    skip=['for j, y in', 'ord_x = ord(x)'],
    views=[
        dict(type='string', var='s1', label='s1（黄 = 当前 x）', h=150, cell=80,
             color=lambda S, i, v: 'yellow' if i == _xi(S) else None),
        dict(type='string', var='s2', label='s2', h=190, cell=80, pointers={'j': 'pink'},
             color=lambda S, i, v: 'pink' if i == S.get('j') and S.get('_line') in (12, 13, 14, 16, 17) else None),
        dict(type='text', fn=_text, size=26, h=60),
        dict(type='array', var='f', label='f（一维滚动；黄 = 正在更新的 f[j+1]）', h=200, cell=90, color=_fcol),
    ],
    watch=[('x', 'x', 'yellow'), ('ord_x', 'ord_x'), ('pre', 'pre', 'cyan'), ('tmp', 'tmp'), ('total', 'total', 'green')],
    captions={
        'm = len(s2)': '`m = {m}`',
        'total = sum': '两串所有字符的 ASCII 和：`total = {total}`',
        'f = [0] * (m + 1)': '和 1143 一样的 DP，只是 ==+1 改成 +ASCII==；只留一行',
        'for x in s1': lambda S, B, r: (f"处理 s1 的字符 `x = '{S.x}'`（ASCII {ord(S.x)}）" if B.get('x') != S.get('x') else '两串都扫完'),
        'pre = 0': '`pre` 充当左上角 `f[i][j]`，每行开头是 `f[0] = 0`',
        'tmp = f[j + 1]': "`y = '{y}'`：先把旧的 `f[{j+1}] = {tmp}` 存进 `tmp`，它是下一列的左上角",
        'if x == y': lambda S, B, r: (f"`'{S.x}' == '{S.y}'`：两个字符==都保留==" if S.x == S.y
                                      else f"`'{S.x}' ≠ '{S.y}'`：不能都保留，看删哪个更好"),
        'f[j + 1] = pre + ord_x': '`f[{j+1}] = {B.pre} + {ord_x}` = =={f[j+1]}==：保留和多了一个 `{x}`',
        'f[j + 1] = max(': '`f[{j+1}] = max({B.f[j+1]}, {f[j]})` = =={f[j+1]}==：删 x（上方）或删 y（左方）取较大',
        'pre = tmp': '`pre = {pre}`：交给下一列当左上角',
        'return total': '`{total} − {f[m]} × 2` = =={ret}==：保留部分在两串里各算一次',
    },
    cards=dict(
        one_liner='删得最少 = 留得最多：把 LCS 的 +1 换成 +ASCII',
        complexity='时间 `O(nm)`，空间 `O(m)`',
        problem=['给两个字符串 `s1`、`s2`，删除一些字符使它们相等',
                 '求被删字符 ==ASCII 值之和==的最小值',
                 f'示例 / 本视频：`"{S1}"`、`"{S2}"` → `231`（删 s=115、t=116）'],
        quote='用 s1 和 s2 的 ASCII 值之和，==减去保留的 ASCII 之和的最大值==，就是删除字符的 ASCII 值之和的最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['计算最多保留的 ASCII 之和，方法和 1143. 最长公共子序列一样',
              '`s1[i] = s2[j]` 时都保留：1143 是 `+1`，本题是 `+ord(x)`，最后乘 2',
              '空间优化：一维 `f`，`pre` 记住被覆盖的左上角'],
        summary=['时间 `O(nm)`，空间 `O(m)`',
                 '易错：最后要 `f[m] * 2`，保留的字符在两个串里各出现一次',
                 '易错：`pre`/`tmp` 交接顺序，先存旧值再覆盖',
                 '题解还给了二维 `f` 写法，以及把 `max` 手写成 `elif` 的更快写法'],
    ),
)
