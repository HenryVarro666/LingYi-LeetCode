def _tip(S):
    if 'h' not in S or 'mx' not in S:
        return ''
    h, mx = S['h'], S['mx']
    if not h:
        return ''
    return f"堆顶 `{h[0][0]}`，原数组最大值 mx = `{mx}`；堆顶 ==< mx== 就继续手动模拟" if h[0][0] < mx else f"堆顶 `{h[0][0]}` ≥ mx = `{mx}`：所有数已挤进 [mx, mx×m) 一圈，之后==轮流操作=="


CONFIG = dict(
    num=3266, title='K 次乘运算后的最终数组 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='最小堆模拟 + 快速幂',
    tags=['难度分 2509'],
    code='''
class Solution:
    def getFinalState(self, nums: List[int], k: int, multiplier: int) -> List[int]:
        if multiplier == 1:  # 数组不变
            return nums

        MOD = 1_000_000_007
        n = len(nums)
        mx = max(nums)
        h = [(x, i) for i, x in enumerate(nums)]
        heapify(h)

        # 模拟，直到堆顶是 mx
        while k and h[0][0] < mx:
            x, i = h[0]
            heapreplace(h, (x * multiplier, i))
            k -= 1

        # 剩余的操作可以直接用公式计算
        h.sort()
        for i, (x, j) in enumerate(h):
            nums[j] = x * pow(multiplier, k // n + (i < k % n), MOD) % MOD
        return nums
''',
    call='Solution().getFinalState([2,1,3,5,6], 14, 2)',
    expect=[16, 16, 24, 20, 24],
    views=[
        dict(type='text', fn=_tip, h=60),
        dict(type='array', var='nums', label='nums（最后写入答案）', h=150,
             color=lambda S, i, v: 'green' if 'i' in S and S.get('_line') == 21 and S.get('j') == i else None),
        dict(type='heap', var='h', label='h = (值, 下标)', fmt=lambda t: f'{t[0]}@{t[1]}', top_color='blue', h=130, font=26),
    ],
    watch=[('k', 'k', 'orange'), ('n', 'n'), ('mx', 'mx', 'pink'), ('k//n', lambda S: S['k'] // S['n'] if 'k' in S and 'n' in S else '', 'cyan')],
    captions={
        'if multiplier == 1': '`multiplier == 1`？乘 1 不变 → 不成立，继续',
        'mx = max': '先记下最大值 `mx = {mx}`：模拟到所有数都追上它为止',
        'h = [(x, i)': '堆里放 `(值, 下标)`：值相同时下标小的先出堆，正好满足「选最前面的」',
        'heapify': '`heapify`：堆顶是最小值',
        'while k and h[0][0] < mx': lambda S, B, r: (
            f'还剩 `k = {S.k}` 次；堆顶 `{S.h[0][0]} < mx = {S.mx}` → 最小的数还没追上 mx，继续手动模拟'
            if S.k and S.h[0][0] < S.mx else
            ('堆顶已经 `≥ mx`：每个数都 ==挤进 [mx, mx×m) 这一圈== → 后面是交替操作，不用再模拟'
             if S.k else '`k = 0`，操作用完')),
        'x, i = h[0]': '取出最小值 `x = {x}`（下标 {i}）',
        'heapreplace': '`heapreplace`：弹出堆顶并压入 `x × multiplier = {x * multiplier}`，比先 pop 再 push 少一次调整',
        'k -= 1': '用掉一次操作，`k` = {k}',
        'h.sort()': lambda S, B, r: f'剩下 `k = {S.k}` 次。把堆==从小到大排好==：之后每一圈都按这个顺序操作每个数各一次',
        'for i, (x, j) in enumerate(h)': lambda S, B, r: f'排名第 `{S.i}` 小的是值 `{S.x}`（原下标 `{S.j}`）',
        'nums[j] = x * pow': lambda S, B, r: (
            f'完整的 `{S.k // S.n}` 圈每个数都乘 `m^{S.k // S.n}`；排名 `{S.i}` {"<" if S.i < S.k % S.n else "≥"} `k % n = {S.k % S.n}` → '
            f'{"==多乘一次==" if S.i < S.k % S.n else "不多乘"}：指数 `{S.k // S.n + (S.i < S.k % S.n)}`，`nums[{S.j}] = {S.nums[S.j]}`'),
        'return nums': '返回最终数组 `{ret}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='数都挤进同一圈后，操作变成「从小到大轮流来」，用快速幂一步到位',
        complexity='时间 `O(n log n log_m U)`，空间 `O(n)`',
        problem=['`nums` 每次取最小值（并列取最前面）乘以 `multiplier`，共 `k` 次，最后每个数对 `10^9+7` 取余',
                 '`k` 最大 `10^9`，不能一次一次模拟',
                 '本视频：`nums=[2,1,3,5,6]`，`k=14`，`multiplier=2`'],
        quote='当两个数接近时，我们会交替操作这两个数，而不会连续操作同一个数。……对于更多的数的情况也同理，当这些数接近时，我们会按照从小到大的顺序依次操作这些数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先用最小堆手动模拟，直到原数组的最大值 `mx` 成为堆顶 → 此后顺序固定',
              '剩 `k` 次：前 `k % n` 小的数多操作一次，共 `k // n + 1` 次，其余 `k // n` 次',
              '操作次数再大也只是乘 `m` 的幂：`pow(multiplier, e, MOD)` 快速幂取模'],
        summary=['时间：每个数至多操作 `O(log_m U)` 次，每次堆操作 `O(log n)`',
                 '易错点：`multiplier == 1` 要先特判，否则 `mx` 永远追不上、循环退化',
                 '只对最后结果取余；模拟阶段值不超过 `mx × m`，不会爆',
                 '排序后 `i < k % n` 决定谁多乘一次，别忘了按原值（含下标）排序',
                 '另有两种写法：直接算出总模拟次数 / 用位长预处理做到 `O(n)`，本视频只演示写法一'],
    ),
)
