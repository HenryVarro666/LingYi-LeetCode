CONFIG = dict(
    num=2028, title='找出缺失的观测数据', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='总和相减 + 先平分再补余数',
    tags=[],
    code='''
class Solution(object):
    def missingRolls(self, rolls, mean, n):

        m = len(rolls)
        k = (m + n) * mean - sum(rolls)

        if k < n or k > n * 6:
            return []
        
        res = [k // n] * n
        for index in range(k % n):
            res[index] += 1
        
        return res
''',
    call='Solution().missingRolls([1, 2], 4, 3)',
    expect=[6, 6, 5],
    views=[
        dict(type='text', fn=lambda S: (f"`k = (m+n) × mean − sum(rolls)` = `{S['m'] + S['n']} × {S['mean']} − {sum(S['rolls'])}` = =={S['k']}==" if 'k' in S else f"已知 `rolls = {S['rolls']}`，`mean = {S['mean']}`，缺 `n = {S['n']}` 次"), size=26, h=60),
        dict(type='array', var='rolls', label='rolls（已知的 m 次投掷）', cell=84, h=180),
        dict(type='text', fn=lambda S: (f"合法范围：`n ≤ k ≤ 6n`，即 `{S['n']} ≤ {S['k']} ≤ {6 * S['n']}`" if 'k' in S else ''), size=26, h=60),
        dict(type='array', var='res', label='res（黄框 = 刚 +1 的骰子）', cell=84, h=190,
             color=lambda S, i, v: 'green' if v == S['k'] // S['n'] + 1 else None),
    ],
    watch=['m', 'k', 'index'],
    captions={
        'm = len(rolls)': '已知 `m = {m}` 次投掷',
        'k = (m + n) * mean': '总和 `(m+n) × mean` 减去已知点数和 `sum(rolls)` → 缺失的 `n` 次的总和 `k = {k}`',
        'if k < n or k > n * 6': lambda S, B, r: f"每次投掷最小 1、最大 6：`n = {S.n}` 次总和在 `[{S.n}, {6 * S.n}]`；`k = {S.k}` " + ('在范围内 → 有解' if S.n <= S.k <= 6 * S.n else '越界 → 无解'),
        'return []': '`k` 超出 `[n, 6n]` → 无解',
        'res = [k // n] * n': '先平均分：每个骰子 `k // n = {k // n}`，共 `{n}` 个 → `{res}`',
        'for index in range': lambda S, B, r: ('余数已经补完，循环结束' if 'index' in B and B['index'] == S.index else f'还剩 `k % n = {S.k % S.n}` 点没分，给前 `{S.k % S.n}` 个骰子各加 1：`index = {S.index}`' if 'index' in S else ''),
        'res[index] += 1': '第 `{index}` 个骰子 +1 → `{res}`（剩下的点数一个个补进前面几个）',
        'return res': '分配完毕，总和恰好是 `k = {k}`，返回 `{res}`',
    },
    max_steps=40,
    cards=dict(
        one_liner='缺的总和 k 先平分，余数补到前几个骰子上',
        complexity='时间 `O(m+n)`，空间 `O(n)`',
        problem=['`n+m` 次投掷的平均值是 `mean`，只留下 `m` 次记录',
                 '构造缺失的 `n` 次（点数 1~6），使平均值恰好等于 `mean`',
                 '示例：`rolls=[1,2]`，`mean=4`，`n=3` → `[6,6,5]`（任意合法答案均可）'],
        quote='n次投掷的最小和为n，最大和为n * 6，那么如果k < n或者k > 6 * n，说明无解，否则需要想办法将k分配给这n次投掷。……最简单的一种分配方式自然是平均分配。',
        quote_src='—— yiduobo 题解原文',
        idea=['总和 `(m+n) × mean` 减去已有点数，得到缺失的 `k`',
              '`k` 小于 `n` 或大于 `6n` 都无法分配 → 返回空',
              '先给每个骰子 `k // n`，余下的 `k % n` 点，给前 `k % n` 个骰子各加 1'],
        summary=['时间 `O(m+n)`，空间 `O(n)`（答案数组）',
                 '易错：无解要同时判断 `k < n` 和 `k > 6n` 两种情况',
                 '补余数时每个骰子最多加 1，所以点数不会超过 6',
                 '原文为 Python 2 写法，整数除法 `k / n` 已改为 `k // n`，并删去类型说明文档字符串'],
    ),
)
