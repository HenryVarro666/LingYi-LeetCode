CONFIG = dict(
    num=1492, title='n 的第 k 个因子', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='枚举到 sqrt(n) + 记录大因子',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution(object):
    def kthFactor(self, n, k):
        
        q = []
        now = 1
        while now * now <= n:
            if n % now == 0:
                k -= 1
                if k == 0:
                    return now

                if n // now != now:
                    q.append(n // now)
                
            now += 1
        
        if len(q) < k:
            return -1

        q.reverse()
        return q[k - 1]
''',
    call='Solution().kthFactor(12, 5)',
    expect=6,
    views=[
        dict(type='text', fn=lambda S: (f"`now = {S['now']}`，`now × now = {S['now']*S['now']}` ≤ `{S['n']}`：还在 sqrt(n) 以内；还差第 ==`{S['k']}`== 个" if 'now' in S and S['now']*S['now'] <= S['n'] else ('枚举完 sqrt(n) 以内的小因子' if 'now' in S else '')), size=26),
        dict(type='array', var='q', h=200, label='q：已发现的大因子 n // now（从大到小）',
             color=lambda S, i, v: 'green' if i == len(S['q']) - 1 else None),
    ],
    watch=['n', ('k（还差几个）', 'k', 'yellow'), ('now', 'now', 'blue')],
    captions={
        'q = []': '`q` 专门存放大于 sqrt(n) 的那一半因子',
        'now = 1': '从 `now = 1` 开始枚举，只枚举到 sqrt(n)',
        'while now * now <= n': lambda S, B, r: (f'`{S.now} × {S.now} = {S.now*S.now} <= {S.n}`：继续' if S.now*S.now <= S.n else f'`{S.now} × {S.now} = {S.now*S.now} > {S.n}`：小因子枚举完，转去看 `q`'),
        'if n % now == 0': lambda S, B, r: (f'`{S.n} % {S.now} == 0` → `{S.now}` 是因子（先数它，再看是不是第 k 个）' if S.n % S.now == 0 else f'`{S.n} % {S.now} != 0`，不是因子'),
        'k -= 1': '找到一个小因子，还差 `{k}` 个',
        'if k == 0': lambda S, B, r: ('`k == 0`：刚好是第 k 个，直接返回' if S.k == 0 else f'`k = {S.k}`，还没到第 k 个'),
        'return now': '第 k 个因子就是 `{now}`',
        'if n // now != now': lambda S, B, r: (f'配对因子 `{S.n} // {S.now} = {S.n // S.now}` 与 `now` 不同 → 要记下来' if S.n // S.now != S.now else '`n // now == now`：完全平方数，同一个因子，不能重复记'),
        'q.append': '大因子 `{n // now}` 先存进 `q`，以后倒着数',
        'now += 1': '`now` → {now}',
        'if len(q) < k': lambda S, B, r: (f'`len(q) = {len(S.q)} < k = {S.k}`：因子总数不够 → 返回 -1' if len(S.q) < S.k else f'`len(q) = {len(S.q)} >= k = {S.k}`：大因子够数，答案在 `q` 里'),
        'q.reverse()': '`q` 是从大到小存的，反转后变成从小到大：`{q}`',
        'return q[k - 1]': '小因子已用掉一部分，剩下的 `k` 对应 `q[k-1] = {q[k-1]}`',
    },
    cards=dict(
        one_liner='枚举到 sqrt(n)，每个小因子顺手记下它的配对大因子',
        complexity='时间 `O(sqrt(n))`，空间 `O(sqrt(n))`',
        problem=['给两个正整数 `n` 和 `k`，把 `n` 的所有因子从小到大排好，返回第 `k` 个；不足 `k` 个返回 `-1`',
                 '示例：`n = 12, k = 3` → `3`（因子 1,2,3,4,6,12）',
                 '本视频：`n = 12, k = 5` → `6`'],
        quote='直接从1到sqrt(n)枚举n的所有因此。对于当前值now，若n模now等于0，说明now是n的一个因子。除此之外，也说明n / now同样是n的一个因子，那么还需要使用一个数组将这些大于sqrt(n)的因子储存起来。',
        quote_src='—— yiduobo 题解原文',
        idea=['`now` 是因子，`n // now` 也是因子：一次枚举拿到一对',
              '小因子按顺序数，数到第 `k` 个就返回；数不到就看 `q`',
              '`q` 里是从大到小存的，反转后第 `k - 1` 个就是答案'],
        summary=['时间 `O(sqrt(n))`，空间 `O(sqrt(n))`',
                 '完全平方数：`now * now == n` 时只记一次，不能把 `q` 重复加',
                 '`k` 在循环里被一路减小，最后用的是「剩下的 k」',
                 '原文为 Python 2 写法，`/` 做整数除法已改为 `//`，并删去了多余说明'],
    ),
)
