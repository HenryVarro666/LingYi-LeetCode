def _good_prefix(m):
    cnt = {}
    a = 1
    while a ** 3 * 2 <= 10 ** 6:
        for b in range(a, 101):
            v = a ** 3 + b ** 3
            if v <= 10 ** 6:
                cnt[v] = cnt.get(v, 0) + 1
        a += 1
    return sorted(x for x, c in cnt.items() if c > 1)[:m]


GOOD10 = _good_prefix(10)


def _reps(x):
    out = []
    a = 1
    while 2 * a ** 3 <= x:
        r = x - a ** 3
        b = round(r ** (1 / 3))
        if b >= a and b ** 3 == r:
            out.append((a, b))
        a += 1
    return out


def _txt(S):
    g = GOOD10
    if 'i' not in S:
        return '预处理好了全部 `10^9` 以内的好整数（共 ==1554== 个，升序），前几个如下'
    i, n = S['i'], S['n']
    if i == 0:
        return f'没有好整数 `<= {n}`'
    x = g[i - 1]
    reps = ' = '.join(f'{a}³+{b}³' for a, b in _reps(x))
    return f'最后一个 `<= {n}` 的是 `{x}` = {reps}'


CONFIG = dict(
    num=3890, title='可由多种立方和构造的整数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='预处理 + 二分查找前缀',
    tags=[],
    code='''
MX = 1_000_000_000
cnt = defaultdict(int)
a = 1
while a * a * a * 2 <= MX:
    b = a
    while (s := a * a * a + b * b * b) <= MX:
        cnt[s] += 1
        b += 1
    a += 1

good_integers = sorted(x for x, c in cnt.items() if c > 1)  # 1554 个

class Solution:
    def findGoodIntegers(self, n: int) -> List[int]:
        i = bisect_right(good_integers, n)
        return good_integers[:i]
''',
    call='Solution().findGoodIntegers(40000)',
    expect=[1729, 4104, 13832, 20683, 32832, 39312],
    views=[
        dict(type='text', h=110, size=28, fn=_txt),
        dict(type='array', var=GOOD10, label='good_integers（只画前 10 个；绿 = <= n）', cell=150, h=240,
             pointers={'i': 'blue'},
             color=lambda S, k, v: 'green' if 'n' in S and v <= S['n'] else None,
             dim=lambda S, k, v: 'n' in S and v > S['n']),
    ],
    watch=['n', ('i', 'i', 'blue')],
    captions={
        'i = bisect_right': lambda S, B, r: (
            f"二分找第一个 `> n` 的位置：`bisect_right(good_integers, {S.n})` = =={S.i}==，"
            f"所以下标 `0 .. {S.i - 1}` 的数都 `<= n`"),
        'return good_integers[:i]': '前缀 `good_integers[:{i}]` 就是答案：{ret}',
    },
    cards=dict(
        one_liner='先预处理全部好整数，再二分切出 <= n 的前缀',
        complexity='查询 `O(log G)`（`G = 1554`），预处理不计入',
        problem=['好整数 `x`：至少两组不同的正整数对 `(a, b)`，`a <= b`，`x = a³ + b³`',
                 '返回 `<= n` 的所有好整数，升序',
                 '本视频：`n = 40000` → `[1729, 4104, 13832, 20683, 32832, 39312]`'],
        quote='枚举 a=1,2,… 和 b=a,a+1,…，用哈希表统计 10^9 以内的 a^3+b^3 的出现次数。把出现次数大于 1 的 a^3+b^3 添加到答案中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`n` 最大 `10^9`，所以所有可能的 `a³+b³` 一次性枚举出来：`a` 不超过 ~800，`b` 不超过 1000',
              '`b` 从 `a` 开始（`a <= b`），`2a³ > MX` 时外层 `a` 就可以停了',
              '次数 `> 1` 的和是好整数，排序后每次查询只要二分出第一个 `> n` 的位置，取前缀'],
        before=[dict(heading='预处理（类外，不在逐步演示里）',
                     lines=['`cnt[s]` 统计和 `s = a³ + b³` 出现次数，例如 `1729` 出现 2 次',
                            '`while (s := ...) <= MX` 用海象运算符，边算边判断',
                            '`sorted(x for x, c in cnt.items() if c > 1)` 得到 ==1554== 个好整数'])],
        summary=['查询时间 `O(log G)`（切片另算），空间 `O(1)`；预处理 `~4×10^5` 次枚举',
                 '`b` 从 `a` 开始，`a = b` 也算一组（`2a³`）',
                 '`bisect_right` 找第一个 `> n` 的位置，前缀 `[:i]` 就是答案',
                 '预处理放在类外，所有测试用例只做一次'],
    ),
)
