CONFIG = dict(
    num=3266, title='K 次乘运算后的最终数组 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='堆模拟到一圈 + 整圈快速幂',
    tags=['难度分 2509'],
    code='''
class Solution(object):
    def getFinalState(self, nums, k, multiplier):

        if multiplier == 1:
            return nums

        n = len(nums)
        ma = max(nums)
        heap = []
        for index, v in enumerate(nums):
            heapq.heappush(heap, [v, index])
        
        while k > 0 and heap[0][0] * multiplier <= ma:
            v, index = heapq.heappop(heap)
            v *= multiplier
            k -= 1
            heapq.heappush(heap, [v, index])
        
        rnd = k // n
        k %= n

        for _ in range(k):
            v, index = heapq.heappop(heap)
            v *= multiplier
            heapq.heappush(heap, [v, index])
        
        def quickPow(base, p, mod):
            if p == 0:
                return 1
            if p == 1:
                return base % mod
            
            x = quickPow(base, p // 2, mod)
            x *= x
            x %= mod
            if p % 2 == 1:
                x *= base
                x %= mod
            
            return x
        
        mod = 10 ** 9 + 7
        mul = quickPow(multiplier, rnd, mod)
        res = [0] * n
        for v, index in heap:
            res[index] = v * mul % mod
        
        return res
''',
    call='Solution().getFinalState([2,1,3,5,6], 16, 2)',
    expect=[32, 32, 24, 20, 24],
    views=[
        dict(type='text', h=60, fn=lambda S: (
            f"堆顶 `{S['heap'][0][0]}` × {S['multiplier']} = `{S['heap'][0][0] * S['multiplier']}`，与 ma = `{S['ma']}` 比较："
            + (' ==≤ ma== → 还能操作' if S['heap'][0][0] * S['multiplier'] <= S['ma'] else ' ==> ma== → 已进入循环')
            if 'heap' in S and 'ma' in S and S['heap'] and 'rnd' not in S else '')),
        dict(type='array', var='nums', label='nums', h=140),
        dict(type='heap', var='heap', label='heap = [值, 下标]', fmt=lambda t: f'{t[0]}@{t[1]}', top_color='blue', h=130),
        dict(type='array', var='res', label='res（最终答案）', h=140,
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=[('k', 'k', 'orange'), ('n', 'n'), ('ma', 'ma', 'pink'),
           ('rnd', lambda S: S.get('rnd', ''), 'cyan'), ('mul', lambda S: S.get('mul', ''), 'green')],
    captions={
        'if multiplier == 1': '`multiplier == 1`？乘 1 数组不会变 → 不成立，继续',
        'ma = max': '记下最大值 `ma = {ma}`：目标是让每个数都落进 `(ma/mul, ma]` 这一档',
        'heapq.heappush(heap, [v, index])': lambda S, B, r: (
            f'`[{S.v}, {S.index}]` 入堆：值相同按下标排，满足「最靠前」' if 'rnd' not in S and 'res' not in S
            else f'把 `{S.v}`（下标 {S.index}）乘 mul 后放回堆'),
        'while k > 0 and': lambda S, B, r: (
            f'堆顶 `{S.heap[0][0]} × {S.multiplier} = {S.heap[0][0] * S.multiplier}`'
            + (f' ≤ ma = `{S.ma}`，这个数乘一次后仍不超过最大值 → 继续模拟' if S.k > 0 and S.heap[0][0] * S.multiplier <= S.ma
               else f' > ma = `{S.ma}`：所有数都满足 `x ≤ ma < x × mul`，==后面按固定顺序轮流操作==' if S.k > 0 else '，k 用完')),
        'v, index = heapq.heappop(heap)': lambda S, B, r: f'弹出最小的 `{S.v}`（下标 {S.index}）',
        'v *= multiplier': '乘上 `multiplier`：`v = {v}`',
        'k -= 1': '用掉一次操作，`k` = {k}',
        'rnd = k // n': '循环里每个数恰好各操作一次，所以整圈数 `rnd = k // n = {rnd}`',
        'k %= n': '不足一圈的 `k % n = {k}` 次，直接用堆再模拟',
        'for _ in range(k)': '剩下 `{k}` 次零散操作：谁最小就乘谁',
        'def quickPow': '定义快速幂：整圈数 `rnd` 可能高达 10^9，不能一圈一圈乘',
        'mod = 10': '`mod = 10^9 + 7`',
        'mul = quickPow': '每个数都要乘 `multiplier^rnd` = `{multiplier}^{rnd}`，取余后 `mul = {mul}`',
        'res = [0] * n': '`res` 按原下标放最终值',
        'for v, index in heap': '遍历堆里的 `(值, 原下标)`',
        'res[index] = v * mul % mod': '`res[{index}] = {v} × {mul} % mod = {res[index]}`',
        'return res': '返回 `{ret}`',
        'if p == 0': '`p == 0`：任何数的 0 次方是 1',
        'if p == 1': '`p == 1`：直接返回 `base % mod`',
        'x = quickPow': '先递归算一半次数 `p // 2`，得到 `x`',
        'x *= x': '平方得 `base^(2×(p//2))`',
        'if p % 2 == 1': '`p` 是奇数吗？奇数还要再乘一个 `base`',
    },
    max_steps=110,
    cards=dict(
        one_liner='先模拟到所有数「同一档」，之后整圈轮流，一圈乘一次 mul',
        complexity='时间 `O(n log n log ma)`，空间 `O(n)`',
        problem=['`nums` 每次取最小值（并列取下标最小）乘 `multiplier`，共做 `k` 次，最后对 `10^9+7` 取余',
                 '`n` 最大 `10^4`，`k` 最大 `10^9`，直接模拟不行',
                 '本视频：`[2,1,3,5,6]`，`k=16`，`multiplier=2` → `[32,32,24,20,24]`'],
        quote='一旦对于nums中所有的nums[index]都满足nums[index] <= ma且nums[index] * mul > ma，接下来就会轮流执行操作，换言之，从这里开始将出现长度为n的循环操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['两个数 `a ≤ b < a×mul`：操作次数相同先动 a，a 多一次就轮到 b → ==交替==',
              '堆顶 `× mul` 超过 `ma` 时，全体进入这一档：用堆把它们逐个推进去，每个数最多 `log(ma)` 次',
              '剩 `k`：整圈 `rnd = k // n` → 全体乘 `mul^rnd`（快速幂）；零头 `k % n` 次再用堆模拟'],
        summary=['时间：模拟阶段 `O(n log n log ma)`，快速幂 `O(log rnd)`',
                 '易错点：先特判 `multiplier == 1`，否则 while 永远不会结束',
                 '零头操作要在整圈乘法之前做完（先模拟，最后统一乘 `mul`）',
                 '循环条件是 `堆顶×mul <= ma`，与灵神「堆顶 < mx」略有不同，终点是同一个状态',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需改动（题解里 3264 题的暴力写法未演示）'],
    ),
)
