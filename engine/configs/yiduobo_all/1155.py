def _win(S):
    j, f, ln = S.get('j'), S.get('f'), S.get('_line')
    if j is None or ln not in (10, 11, 12, 13, 14):
        return None
    if ln in (10, 11):
        return (max(0, j - f), j - 1)      # 当前 now = g[j-f .. j-1] 之和
    return (max(0, j - 1 - f), j - 2)      # 向左挪一格后的窗口


def _formula(S):
    j, f, ln = S.get('j'), S.get('f'), S.get('_line')
    if j is None or ln not in (10, 11, 12, 13, 14):
        return '`g[j]` = 已掷骰子数下总和为 `j` 的方案数；`now` = 窗口 `g[j-f .. j-1]` 之和'
    if ln in (10, 11):
        return f'`g[{j}] = now` = `g[{max(0, j - f)}..{j - 1}]` 之和'
    return f'窗口左移一格：减去 `g[{j - 1}]`，补上 `g[{j - f - 1}]`'


CONFIG = dict(
    num=1155, title='掷骰子等于目标和的方法数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='一维 DP · 滑动窗口求和',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1654'],
    code='''
class Solution(object):
    def numRollsToTarget(self, d, f, target):

        mod = 10 ** 9 + 7
        g = [0] * (target + 1)
        g[0] = 1
        for i in range(d):
            now = sum(g[max(0, target - f) : target]) % mod
            for j in range(target, 0, -1):
                g[j] = now
                now -= g[j - 1]
                if j - f - 1 >= 0:
                    now += g[j - f - 1]
                now = (now + mod) % mod
            g[0] = 0
            
        return g[target]
''',
    call='Solution().numRollsToTarget(2, 4, 5)',
    expect=4,
    views=[
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='array', var='g', label='g[j]：已掷出若干骰子，总和为 j 的方案数', h=300, cell=84,
             pointers={'j': 'blue'}, window=(lambda S: (_win(S) or (None, None))[0], lambda S: (_win(S) or (None, None))[1]),
             color=lambda S, i, v: 'green' if i == S['target'] else None),
    ],
    max_steps=90,
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('now', 'now', 'cyan'), ('g[target]', 'g[target]', 'green')],
    captions={
        'g = [0]': '`g[j]`：总和为 `j` 的方案数，共 `target + 1 = {target + 1}` 格',
        'g[0] = 1': '没掷骰子时，总和 0 有 ==1 种==方案（空）',
        'for i in range': lambda S, B, r: (f'掷第 `{S.i + 1}` 个骰子（共 `d = {S.d}` 个）' if S.i != B.get('i') or 'now' not in B else f'`{S.d}` 个骰子都掷完了'),
        'now = sum': '先算 `j = target` 的窗口和：`now = sum(g[{max(0, target - f)}:{target}])` = =={now}==',
        'for j in range': lambda S, B, r: (f'`j = {S.j}`：==从大到小==枚举，窗口里的 g 还是上一轮的值' if S.get('j') != B.get('j') or S.j == S.target
                                           else '这一轮 `j` 都更新完了'),
        'g[j] = now': '`g[{j}] = now` = =={now}==：窗口 `g[{max(0, j - f)}..{j - 1}]` 的和',
        'now -= g[j - 1]': '`j` 减 1 后窗口右端少了 `g[{j - 1}]`：`now` → {now}',
        'if j - f - 1 >= 0': lambda S, B, r: (f'`j - f - 1 = {S.j - S.f - 1} >= 0`：左边还有新进入窗口的格子' if S.j - S.f - 1 >= 0
                                              else f'`j - f - 1 = {S.j - S.f - 1} < 0`：左边越界，不用补'),
        'now += g[j - f - 1]': '补上新进入窗口的 `g[{j - f - 1}]`：`now` → {now}',
        'now = (now + mod) % mod': '`now` 取模并保证非负 → {now}',
        'g[0] = 0': '掷过骰子后，总和 0 不可能：`g[0] = 0`（只在第一轮之前它才是 1）',
        'return g[target]': '`g[{target}]` = =={ret}==',
    },
    cards=dict(
        one_liner='g 一维滚动，sum 看成滑动窗口，O(1) 更新',
        complexity='时间 `O(d·target)`，空间 `O(target)`',
        problem=['`d` 个骰子，每个有 `f` 个面（1 到 `f`），总和恰为 `target` 的方案数，对 `10^9+7` 取模',
                 '示例：`n=2, k=6, target=7` → `6`',
                 '本视频：`d=2, f=4, target=5` → `4`'],
        quote='对比两个式子可以发现实际上后面的项中减去了g[i - 1][j - 1]然后加上g[i - 1][j - f - 1]，因此在这里可以使用一个变量维护后面这些项的和。',
        quote_src='—— yiduobo 题解原文',
        idea=['`g[i][j] = sum(g[i-1][j-k])`，`1 <= k <= min(f, j)`',
              '只依赖上一轮 → 从 `target` 往下枚举 `j`，去掉 `i` 这一维',
              '`g[j]` 与 `g[j-1]` 的和式只差头尾各一项 → 用 `now` 做滑动窗口',
              '初值 `g[0] = 1`，第一轮后要把 `g[0]` 改回 `0`'],
        summary=['时间 `O(d·target)`，空间 `O(target)`',
                 '易错：每一轮结束要 `g[0] = 0`',
                 '易错：`now` 要取模并加 `mod` 防负数；`j - f - 1` 越界时不补',
                 '对比灵神：灵神把每个骰子减 1 再做前缀和相减；这里直接用一个窗口和变量'],
    ),
)
