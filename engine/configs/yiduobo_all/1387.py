def _chain(S):
    if 'now' not in S:
        return '每个数 `x` 单独模拟：偶数 `/2`，奇数 `3x+1`，数到 1 为止'
    return f"正在算 `x = {S['x']}` 的权重：`now = {S['now']}`，已走 `{S['step']}` 步" if 'step' in S and 'x' in S else ''


CONFIG = dict(
    num=1387, title='将整数按权重排序', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='暴力模拟每个数 + 二元组排序',
    tags=['灵神题单·动态规划', '灵神题单·数学算法'],
    code='''
class Solution(object):
    def getKth(self, lo, hi, k):

        return sorted([[self.calc(x), x] for x in range(lo, hi + 1)], key=lambda d:(d[0], d[1]))[k - 1][1]
    
    def calc(self, now):
        step = 0
        while now != 1:
            if now % 2 == 0:
                now //= 2
            else:
                now = now * 3 + 1

            step += 1

        return step
''',
    call='Solution().getKth(2, 5, 3)',
    expect=5,
    views=[
        dict(type='text', h=90, fn=_chain),
        dict(type='calls', h=200),
        dict(type='text', h=140, fn=lambda S: (
            '`sorted(..., key=lambda d:(d[0], d[1]))`：先比权重 `d[0]`，相同再比数值 `d[1]`\n'
            '权重 `[(1,2), (7,3), (2,4), (5,5)]` → 排序 `[2,4,5,3]`，第 3 个是 ==5==')),
    ],
    watch=[('now', 'now', 'blue'), ('step', 'step', 'green'), ('lo', 'lo'), ('hi', 'hi'), ('k', 'k')],
    max_steps=90,
    captions={
        'return sorted': lambda S, B, r: ('先对 `lo..hi` 的每个 `x` 调 `calc(x)` 得到 `[权重, x]`，再排序取第 `k` 个' if r is None
                                          else f'排好序，第 `{S.k}` 个的数值 =={r}=='),
        'step = 0': '`step` 计步数，从 0 开始',
        'while now != 1': lambda S, B, r: (f'`now = {S.now}` 不是 1 → 继续变换' if S.now != 1 else f'`now = 1`，停止。权重 `step` = =={S.step}=='),
        'if now % 2 == 0': lambda S, B, r: (f'`{S.now}` 是偶数 → 除以 2' if S.now % 2 == 0 else f'`{S.now}` 是奇数 → 乘 3 加 1'),
        'now //= 2': '`now` 变成 `{now}`',
        'now = now * 3 + 1': '`now = {B.now} × 3 + 1 = {now}`（奇数变换后一定是偶数）',
        'step += 1': '走了一步：`step` → =={step}==',
        'return step': '`calc` 返回权重 =={ret}==',
    },
    cards=dict(
        one_liner='范围很小，直接暴力模拟每个数，二元组排序',
        complexity='时间约 `O(n·L + n log n)`（L 为链长），空间 `O(n)`',
        problem=['权重 = 把 `x` 变成 `1` 的步数：偶数 `x/2`，奇数 `3x+1`',
                 '`[lo, hi]` 按权重升序排，权重相同按数值升序，返回第 `k` 个',
                 '示例：`lo=7, hi=11, k=4` → `7`；本视频：`lo=2, hi=5, k=3` → `5`'],
        quote='由于题目中给出的lo和high范围都很小，那么可以对每个数字计算出变换的步数，然后一趟排序即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`calc(x)` 老老实实模拟到 1，返回步数',
              '做成 `[权重, x]`，用 `key=(d[0], d[1])` 同时满足两个排序规则',
              '作者说明：记忆化能优化，但这里「直接暴力计算」'],
        summary=['时间约 `O(n·L + n log n)`，空间 `O(n)`；本题 `hi ≤ 1000` 足够',
                 '原文为 Python 2 写法，`now /= 2` 已改为 `now //= 2`',
                 '排序时权重在前、数值在后，不要写反',
                 '对比灵神：他用 `@cache` 共享状态并把奇数两步合一；这里每个数从头算'],
    ),
)
