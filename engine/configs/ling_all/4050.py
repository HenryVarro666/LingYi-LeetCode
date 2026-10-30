CODE = '''
MX = 13
f = [inf] * MX
f[0] = -1

s = i = 1
while s < MX:
    for j in range(s, MX):
        f[j] = min(f[j], f[j - s] + i + 1)
    i += 1
    s += i

class Solution:
    def minDays(self, n: int) -> int:
        return f[n]
'''.strip('\n')


def _fv(S):
    f = S.get('f')
    return None if f is None else [('∞' if x == float('inf') else x) for x in f]


def _fm(x):
    return '∞' if x == float('inf') else str(x)


def _txt(S):
    if 'f' not in S:
        return '用三角形数当物品：体积 `s = 1+2+…+i`，代价 `i + 1` 天（含前面的跳过）'
    if 'j' in S and 'i' in S and S.get('_line') == 8:
        return f"`f[{S['j']}] = min(f[{S['j']}], f[{S['j'] - S['s']}] + {S['i']} + 1)`"
    if 'n' in S:
        return f"预处理完毕，查表 `f[{S['n']}]`"
    return '`f[0] = -1`：第一段连胜前不需要跳过，抵消统一多算的 1 天'


def _col(S, k, v):
    if 'j' not in S or 's' not in S or S.get('_line') not in (8, 9, 10):
        return None
    if k == S['j']:
        return 'green'
    if k == S['j'] - S['s']:
        return 'blue'
    return None


def _cap(S, B, ret):
    j, s, i = S.j, S.s, S.i
    old, sel = B.f[j], B.f[j - s] + i + 1
    tail = f'选更少 → `f[{j}]` 变成 =={_fm(S.f[j])}==' if sel < old else f'不选更好（或一样）→ `f[{j}]` 保持 =={_fm(S.f[j])}=='
    return f'不选：`f[{j}] = {_fm(old)}`；选 `{s}`：`f[{j - s}] + {i + 1} = {_fm(sel)}` → {tail}'


CONFIG = dict(
    num=4050, title='得到恰好 N 分的最少天数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='完全背包（三角形数）',
    code=CODE,
    setup=f'CODE = {CODE!r}\ndel MX, f, i, j, s',
    call="exec(compile(CODE, '<solution>', 'exec'), globals())\nSolution().minDays(12)",
    expect=7,
    views=[
        dict(type='text', fn=_txt, size=28, h=70),
        dict(type='array', var=_fv, label='f[j] = 恰好得 j 分的最少天数', color=_col,
             pointers={'j': 'green', 'j - s': 'blue'}, pointer_labels={'j - s': 'j-s'}, cell=70, h=260),
    ],
    watch=[('i', 'i', 'orange'), ('s', 's', 'orange'), ('j', 'j', 'green'), ('j-s', 'j - s', 'blue')],
    skip=['for j in', 'i += 1', 's += i'],
    max_steps=80,
    captions={
        'MX = 13': '原文 `MX = 100_001`（题目 `n <= 10^5`），在类外预处理一次；演示取 `MX = {MX}`，只算到 `n = 12`',
        'f = [inf]': '先设全部为 ==∞==（凑不出来）',
        'f[0] = -1': '`f[0] = -1`：用一个三角形数花费 `i+1` 天，第一个其实只花 `i` 天，初值 -1 正好抵消',
        's = i = 1': '`i` 是连胜天数，`s = i(i+1)/2` 是连胜 `i` 天得到的分数（三角形数），从 `1` 开始',
        'while s < MX': lambda S, B, ret: (f'三角形数 `s = {S.s}`（连胜 `{S.i}` 天，代价 `{S.i + 1}` 天）：`j` 从 `{S.s}` ==从小到大==枚举，可重复选'
                                          if S.s < S.MX else f'`s = {S.s}` 已超过范围，预处理结束') if 'MX' in S else '',
        'f[j] = min': _cap,
        'return f[n]': '查表 `f[{n}]` = =={ret}==（`6 + 6`：连胜 3 天，跳 1 天，再连胜 3 天）',
    },
    cards=dict(
        one_liner='三角形数当物品，每件代价 i+1 天：完全背包',
        complexity='预处理 `O(N√N)`，`N = 10^5`；查询 `O(1)`',
        problem=['每天可以得分或跳过：连胜第 k 天得 k 分，跳过一天连胜清零',
                 '求恰好得到 `n` 分的最少天数（含跳过的天数）',
                 '示例：`n = 9` → `6`（`1+2+3`，跳过，`1+2`）；本视频演示 `n = 12` → `7`'],
        quote='本题和 279. 完全平方数 几乎一样……完全平方数 x^2 改成了三角形数……每使用一个三角形数，要花费 x+1 天。特殊情况：使用第一个三角形数花费 x 天。',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['每段连胜 `i` 天得 `i(i+1)/2` 分，段与段之间至少隔 1 天跳过',
              '把三角形数当物品：体积 `s`，代价 `i + 1`，每种可无限使用',
              '令 `f[0] = -1`，第一段多算的 1 天就被抵消，统一成“每件 `i+1` 天”'],
        summary=['预处理 `O(N√N)`，三角形数只有约 `√(2N)` 个',
                 '易错点：代价是 `i + 1`，不是 `i`；`f[0]` 要设为 `-1`',
                 '完全背包内层 `j` 从小到大，才能重复选同一个物品',
                 '本视频把常数 `MX` 由 100_001 改成 13，其余代码逐字照搬',
                 '方法二：把和看成节点、三角形数看成边，用 Dijkstra 求 0 到 n 的最短路'],
    ),
)
