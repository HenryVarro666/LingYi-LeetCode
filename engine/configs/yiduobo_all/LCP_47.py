CONFIG = dict(
    num='LCP 47', title='入场安检', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='背包方案数 · 滚动数组',
    tags=['动态规划'],
    code='''
class Solution(object):
    def securityCheck(self, capacities, k):

        f = [0] * (k + 1)
        f[0] = 1
        mod = 10 ** 9 + 7
        for c in capacities:
            for j in range(k, c - 2, -1):
                f[j] += f[j - (c - 1)]
                if f[j] >= mod:
                    f[j] -= mod
        
        return f[k]
''',
    call='Solution().securityCheck([4,3,2,2], 6)',
    expect=2,
    skip=['f = [0]', 'mod = ', 'for j in range', 'if f[j] >= mod', 'f[j] -= mod'],
    views=[
        dict(type='array', var='capacities', label='capacities：每个房间可留下 c − 1 人', h=150, cell=70),
        dict(type='array', var='f', label='f[j]：恰好留下 j 名游客的方案数', h=190, cell=80, pointers={'j': 'blue'},
             color=lambda S, i, v: 'yellow' if 'c' in S and 'j' in S and S['_line'] >= 9 and i == S['j'] - (S['c'] - 1) else None),
        dict(type='text', fn=lambda S: (f"房间容量 `c = {S['c']}`：留下 `{S['c'] - 1}` 人 → `f[j] += f[j − {S['c'] - 1}]`" if 'c' in S else '目标：留下 `k` 名游客（题目里的 k 号观众前面有 k 人）'), size=24, h=60),
    ],
    watch=['c', 'j', ('k', 'k', 'pink'), ('f[k]', 'f[k]', 'green')],
    captions={
        'f[0] = 1': '一个房间都不选，留下 0 人的方案有 ==1== 种',
        'f[j] += f[j - (c - 1)]': '`f[{j}]` = 不留 `{B.f[j]}` + 留下 `{c-1}` 人 `f[{j-(c-1)}] = {f[j-(c-1)]}` → =={f[j]}==（倒序 j，每个房间只用一次；没超过 mod 就不用减）',
        'f[j] -= mod': '`f[j] -= mod`，保持在模数以内',
        'return f[k]': '留下 `k` 人的方案数 = =={ret}==',
    },
    cards=dict(
        one_liner='每个房间：留下 c−1 人，或者不留；数方案',
        complexity='时间 `O(N·k)`，空间 `O(k)`',
        problem=['若干安检室，可设成队列或栈',
                 '求有多少种设置，使编号 `k` 的观众第一个通过最后一个安检室',
                 '示例：`capacities=[4,3,2,2]`，`k=6` → `2`'],
        quote='题目给出了若干个房间，其中第i个房间可以选择留下capacities[i] - 1名游客，或者不留下任何游客。问最终留下k - 1名游客的方案数量。这是一个典型的背包问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['转成背包：房间 i 留下 `capacities[i]−1` 人（栈），或不留人（队列）',
              '`f[i][j] = f[i-1][j] + f[i-1][j-(capacities[i]-1)]`',
              '只依赖上一轮，倒序 `j` 滚动成一维，加法后超过 mod 就减一次'],
        summary=['时间 `O(N·k)`，空间 `O(k)`',
                 '易错：`j` 倒序到 `c - 2`（含 `c - 1`），每个房间只能用一次',
                 '易错：`f[j] += ...` 后用 `if f[j] >= mod: f[j] -= mod` 代替 `%`，两个数都 < mod 所以够用',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神 `x -= 1` 后循环到 `x`，用 `%` 取模'],
    ),
)
