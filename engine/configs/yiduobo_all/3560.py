CONFIG = dict(
    num=3560, title='木材运输的最小成本', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='超过 k 就切出一段 k',
    tags=[],
    code='''
class Solution(object):
    def minCuttingCost(self, n, m, k):
        
        res = 0
        if n > k:
            res += k * (n - k)
        if m > k:
            res += k * (m - k)
        return res
''',
    call='Solution().minCuttingCost(10, 8, 6)',
    expect=36,
    views=[
        dict(type='text', h=130, size=32,
             fn=lambda S: f"`n = {S['n']}`，`m = {S['m']}`，载重 `k = {S['k']}`"),
        dict(type='text', h=130, size=32,
             fn=lambda S: f"已累计成本 `res = {S['res']}`" if 'res' in S else ''),
        dict(type='text', h=130, size=32,
             fn=lambda S: (f"`n` 切成 `{S['k']}` 和 `{S['n'] - S['k']}`" if S['n'] > S['k'] else f"`n = {S['n']} ≤ {S['k']}`，不用切") + '；' + (f"`m` 切成 `{S['k']}` 和 `{S['m'] - S['k']}`" if S['m'] > S['k'] else f"`m = {S['m']} ≤ {S['k']}`，不用切")),
    ],
    watch=['n', 'm', 'k', ('res', 'res', 'green')],
    captions={
        'res = 0': '没切之前成本是 `0`',
        'if n > k': lambda S, B, r: (f'`n = {S.n} > k = {S.k}`：装不下，必须切' if S.n > S.k else f'`n = {S.n} ≤ k = {S.k}`：能直接装，不用切'),
        'res += k * (n - k)': '切成 `k` 和 `n−k`，差距越大乘积越小：成本 `{k} × {n - k}`，`res = {res}`',
        'if m > k': lambda S, B, r: (f'`m = {S.m} > k = {S.k}`：装不下，必须切' if S.m > S.k else f'`m = {S.m} ≤ k = {S.k}`：不用切'),
        'res += k * (m - k)': '同理切出 `k`：成本 `{k} × {m - k}`，`res = {res}`',
        'return res': '两根都检查过了，总成本 `{res}`',
    },
    cards=dict(
        one_liner='切得越悬殊，乘积越小：直接切出一段 k',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['两根木材长 `n`、`m`，每辆卡车最多装长度不超过 `k` 的一根',
                 '切长 `x` 为 `y` 和 `x−y` 的成本是 `y × (x−y)`',
                 '本视频：`n=10, m=8, k=6` → `36`'],
        quote='观察cost = y * (x - y)这个式子可以发现，切分的两段长度差越大，cost就越小。',
        quote_src='—— yiduobo 题解原文',
        idea=['木材长度大于 `k` 才需要切',
              '两段都不能超过 `k`，差距最大的切法就是 `k` 和 `x−k`',
              '`n`、`m` 分别判断，超过 `k` 就把 `k × (长度−k)` 累加进答案'],
        after=[dict(heading='用示例验算', lines=['示例 1：`n=6, m=5, k=5`：只有 `n` 超过 `k`，切成 `5` 和 `1`，成本 `5`','示例 2：`4, 4, 6`：都不超过 `k`，`res` 保持 `0`','两根都超过 `k` 的情况分别累加'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '`n`、`m` 都超过 `k` 时要分别累加（题目保证 ≤ 2k）',
                 '原文已是 Python 3 可运行写法，无需修改',
                 '对比灵神：灵神证明只有较长的一根需要切，一行 `max` 搞定'],
    ),
)
