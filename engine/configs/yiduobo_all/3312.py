CONFIG = dict(
    num=3312, title='查询排序后的最大公约数', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='类筛法 · 倍数个数 + 手写二分',
    tags=['灵神题单·数学算法', '难度分 2533'],
    code='''
class Solution(object):
    def gcdValues(self, nums, queries):

        ma = max(nums)
        freq = [0] * (ma + 1)
        mul = [0] * (ma + 1)
        pairs = [0] * (ma + 1)

        for v in nums:
            freq[v] += 1
        
        n = len(nums)
        pairs[1] = n * (n - 1) // 2

        for v in range(ma, 1, -1):
            mul[v] = freq[v]
            for x in range(v + v, ma + 1, v):
                mul[v] += freq[x]
                pairs[v] -= pairs[x]
            
            pairs[v] += mul[v] * (mul[v] - 1) // 2
            pairs[1] -= pairs[v]

        s = [0]
        for v in range(1, ma + 1):
            s.append(s[-1] + pairs[v])
            
        res = []
        for q in queries:
            left = 1
            right = ma
            while left < right:
                mid = (left + right) // 2
                if s[mid] >= q + 1:
                    right = mid
                else:
                    left = mid + 1
            
            res.append(left)
        
        return res
''',
    call='Solution().gcdValues([2, 3, 4], [2])',
    expect=[2],
    views=[
        dict(type='array', var='freq', label='freq[x]：x 在 nums 中出现的次数', cell=84, h=150,
             pointers={'x': 'pink'}, color=lambda S, i, v: 'cyan' if v else None),
        dict(type='array', var='mul', label='mul[v]：nums 中 v 的倍数有几个', cell=84, h=150,
             pointers={'v': 'blue'}, color=lambda S, i, v: 'yellow' if v else None),
        dict(type='array', var='pairs', label='pairs[v]：gcd 恰好为 v 的数对个数', cell=84, h=150,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='array', var='s', label='s[v]：gcd ≤ v 的数对个数', cell=84, h=150,
             pointers={'left': 'blue', 'right': 'pink', 'mid': 'yellow'}),
    ],
    watch=[('v', 'v', 'blue'), ('x', 'x', 'pink'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), 'res'],
    skip=['freq = [0]', 'mul = [0]', 'pairs = [0]', 'res = []', 'n = len(nums)'],
    captions={
        'ma = max': '值域上界 `ma = {ma}`：gcdPairs 里的值都在 `1..{ma}`，不用把 `n(n-1)/2` 个数对真的算出来',
        'for v in nums': '先统计 `freq`：每个数出现几次',
        'freq[v] += 1': '`freq[{v}] = {freq[v]}`',
        'pairs[1] = n': '先假设所有 `{n}×({n}−1)/2 = {pairs[1]}` 个数对 gcd 都是 1，后面逐个减掉 gcd 更大的',
        'for v in range(ma, 1': '==从大到小==枚举 `v`：`pairs[v]` 要减去 `pairs[2v], pairs[3v]...`，必须先算大的',
        'mul[v] = freq[v]': '`mul[v]` 从 `v` 本身开始数：`{mul[v]}`',
        'for x in range(v + v': '像筛法一样枚举 `v` 的更大倍数 `x = {x}`',
        'mul[v] += freq[x]': '`{x}` 出现 `{freq[x]}` 次 → `mul[{v}] = {mul[v]}`',
        'pairs[v] -= pairs[x]': '`gcd = {x}` 的数对也是 `{v}` 的倍数，但 gcd 不是 `{v}` → `pairs[{v}] -= {pairs[x]}` → `{pairs[v]}`',
        'pairs[v] += mul': '`mul = {mul[v]}` 个倍数两两组合：`{mul[v]}×({mul[v]}−1)//2 = {mul[v]*(mul[v]-1)//2}` 对 → `pairs[{v}] = {pairs[v]}`',
        'pairs[1] -= pairs[v]': '这 `{pairs[v]}` 对的 gcd 是 `{v}`，不是 1，从 `pairs[1]` 里扣掉 → `pairs[1] = {pairs[1]}`',
        24: '`s` 从 0 开始做前缀和：`s[v]` = gcd ≤ v 的数对个数',
        26: '`s[{v}] = {s[v]}`',
        'for q in queries': '处理询问 `q = {q}`：要在 `s` 里找到最小的 `v`，使 `s[v] ≥ q + 1`',
        'left = 1': '二分区间 `[left, right] = [1, {ma}]`',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`，继续二分' if S.left < S.right else f'`left = right = {S.left}` → 找到答案'),
        'mid = (left + right)': '`mid = {mid}`',
        'if s[mid] >= q + 1': lambda S, B, r: (f'`s[{S.mid}] = {S.s[S.mid]} ≥ q+1 = {S.q + 1}` → 前 `{S.mid}` 个值已经覆盖第 `q` 个 → 答案在左边（含 mid）' if S.s[S.mid] >= S.q + 1 else f'`s[{S.mid}] = {S.s[S.mid]} < q+1 = {S.q + 1}` → 还没覆盖到 → 答案在右边'),
        'right = mid': '`right = {right}`',
        'left = mid + 1': '`left = {left}`',
        'res.append(left)': '`gcdPairs[{q}] = {left}`，`res = {res}`',
        'return res': '全部询问答完：`{res}`',
    },
    cards=dict(
        one_liner='数对太多存不下：只数每个 gcd 值出现了几次，再二分',
        complexity='时间 `O(M log M + q log M)`，空间 `O(M)`',
        problem=['`gcdPairs`：所有数对的 gcd 升序排列，长度 `n(n−1)/2` 非常大',
                 '对每个询问返回 `gcdPairs[q]`',
                 '示例：`nums=[2,3,4]`，`gcdPairs=[1,1,2]`；`queries=[2]` → `[2]`'],
        quote='最大公约数为v的数对，等于所有为v的倍数的数两两组合形成的数对数量，减去最大公约数为2v、3v、...、kv的数对的数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用 `mul[v]` 数出 `v` 的倍数个数，组成 `mul×(mul−1)//2` 对',
              '这些数对的 gcd 是 `v` 的倍数，减去 `pairs[2v]...pairs[kv]`',
              '和筛法一样，所以 `v` 要从大到小处理；`pairs[1]` 最后用总数减去其他得到'],
        summary=['时间 `O(M log M)` 建表，每个询问手写二分 `O(log M)`',
                 '二分条件 `s[mid] >= q + 1`：第 `q` 个（从 0 数）至少要被前 `mid` 个值覆盖',
                 '易错点：`v=1` 单独处理（总数减去其他），循环不含 1',
                 '原文已是 Python 3 可运行写法（`//` 本来就是整除），没有改动',
                 '对比灵神：灵神用 `bisect_right` + `accumulate`，yiduobo 手写二分，且单独维护 `mul`'],
    ),
)
