def _calc(S):
    if 'y' not in S or 'x' not in S:
        return '先数出两个字符串里每个字母的个数 `c1`、`c2`'
    x, y, c, d, c1, c2 = S['x'], S['y'], S['c'], S['d'], S['c1'], S['c2']
    if x == y:
        return f"交换 `{x}` 和 `{y}`：不变，`len(c1)` = {len(c1)}，`len(c2)` = {len(c2)}"
    a = len(c1) - (c == 1) + (y not in c1)
    b = len(c2) - (d == 1) + (x not in c2)
    return (f"交换后 word1 的种类：`{len(c1)}` − {int(c == 1)} + {int(y not in c1)} = =={a}==；"
            f"word2：`{len(c2)}` − {int(d == 1)} + {int(x not in c2)} = =={b}==")


CONFIG = dict(
    num=2531, title='使字符串中不同字符的数目相等', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='枚举两种字母 + 只算种类数变化', tags=[],
    code='''
class Solution:
    def isItPossible(self, word1: str, word2: str) -> bool:
        c1 = Counter(word1)
        c2 = Counter(word2)
        for x, c in c1.items():
            for y, d in c2.items():
                if y == x:  # 无变化
                    if len(c1) == len(c2):
                        return True
                elif len(c1) - (c == 1) + (y not in c1) == \\
                     len(c2) - (d == 1) + (x not in c2):  # 基于长度计算变化量
                    return True
        return False
''',
    call="Solution().isItPossible('abcc', 'aab')",
    expect=True,
    views=[
        dict(type='string', var='word1', label='word1', cell=80, h=190),
        dict(type='map', var='c1', label='c1（word1 的字母计数）', fmt=lambda k, v: f"'{k}': {v}", h=130, font=30),
        dict(type='string', var='word2', label='word2', cell=80, h=190),
        dict(type='map', var='c2', label='c2（word2 的字母计数）', fmt=lambda k, v: f"'{k}': {v}", h=130, font=30),
        dict(type='text', fn=_calc, size=26, h=120),
    ],
    skip=[10],
    watch=[('x', 'x', 'blue'), ('c', 'c'), ('y', 'y', 'pink'), ('d', 'd')],
    captions={
        'c1 = Counter': '`c1`：word1 里每个字母出现几次，`len(c1)` 就是不同字母数',
        'c2 = Counter': '`c2`：word2 同理。字母只有 26 种，所以可以直接枚举「换哪两种字母」',
        'for x, c in': '枚举 word1 里要换出去的字母 `x = {x}`（出现 {c} 次）',
        'for y, d in': lambda S, B, r: ('word2 的字母都试完了，回到外层换下一个 `x`' if 'y' in B and B.y == S.y and B.x == S.x
                                        else f'枚举 word2 里要换过来的字母 `y = {S.y}`（出现 {S.d} 次）'),
        'if y == x': lambda S, B, r: (f'`y == x`（都是 `{S.x}`）：交换后两边种类都不变' if S.y == S.x
                                     else f'`y = {S.y}` ≠ `x = {S.x}`：交换会改变种类数，转去算变化量'),
        'if len(c1) == len(c2)': '没变化时，只要本来 `len(c1) = {len(c1)}` 与 `len(c2) = {len(c2)}` ==相等==就成立：{"成立" if len(c1) == len(c2) else "不成立"}',
        11: lambda S, B, r: (
            f'word1 种类 `{len(S.c1)} − {int(S.c == 1)} + {int(S.y not in S.c1)}` = {len(S.c1) - (S.c == 1) + (S.y not in S.c1)}；'
            f'word2 种类 `{len(S.c2)} − {int(S.d == 1)} + {int(S.x not in S.c2)}` = {len(S.c2) - (S.d == 1) + (S.x not in S.c2)}'
            f' → =={"相等" if len(S.c1) - (S.c == 1) + (S.y not in S.c1) == len(S.c2) - (S.d == 1) + (S.x not in S.c2) else "不相等"}=='),
        'return False': '枚举完所有字母组合都不行 → `False`',
        9: '没变化且种类数本来就相等 → 返回 ==True==',
        12: '交换 `{x}`、`{y}` 后两边不同字母数相等 → 返回 ==True==',
    },
    cards=dict(
        one_liner='只有 26 种字母：枚举换哪两种，不用真的交换',
        complexity='时间 `O(n+m+26²)`，空间 `O(26)`',
        problem=['各选一个下标交换 `word1[i]` 与 `word2[j]`，==恰好一次==',
                 '问能否让两个字符串的不同字符数相等',
                 '示例：`abcc`、`aab` → `true`'],
        quote='只有 26 种字母，写一个 26² 的暴力枚举。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x` 个数为 1：换走后 word1 少一种；`y` 不在 word1：换来后多一种',
              'word2 同理：`y` 个数为 1 少一种，`x` 不在 word2 多一种',
              '`x == y` 时不变，直接比 `len(c1)` 与 `len(c2)`'],
        summary=['时间 `O(n+m+|Σ|²)`，空间 `O(|Σ|)`，`|Σ| = 26`',
                 '枚举的是 `c1`、`c2` 里真实存在的字母，所以交换一定合法',
                 '==恰好一次==交换：`x == y` 也算一次，别漏掉这种情形',
                 '原文的 `Counter` 由运行环境预置'],
    ),
)
