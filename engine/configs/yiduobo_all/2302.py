CONFIG = dict(
    num=2302, title='统计得分小于 K 的子数组数目', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='前缀和 + 同向双指针（枚举起点）',
    tags=['灵神题单·滑动窗口与双指针', '难度分 1808'],
    code='''
class Solution(object):
    def countSubarrays(self, nums, k):

        f = [nums[0]]
        for num in nums[1:]:
            f.append(f[-1] + num)
        
        p = -1
        while p + 1 < len(nums) and f[p + 1] * (p + 2) < k:
            p += 1

        res = p + 1
        for index in range(1, len(nums)):
            p = max(p, index - 1)
            while p + 1 < len(nums) and (f[p + 1] - f[index - 1]) * (p - index + 2) < k:
                p += 1
            res += p - index + 1
        
        return res
''',
    call='Solution().countSubarrays([2,1,4,3,5], 10)',
    expect=6,
    views=[
        dict(type='array', var='nums', label='nums（框 = 起点 index 到终点 p）', pointers={'index': 'blue', 'p': 'pink'},
             window=(lambda S: S.get('index', 0), lambda S: S.get('p', -1)), cell=100, h=250),
        dict(type='array', var='f', label='f（前缀和：f[i] = nums[0..i] 之和）', pointers={'p': 'pink'}, cell=100, h=250),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"起点 {S['index']}：`p` = {S['p']}，合法子数组 `{S['p']-S['index']+1}` 个，`res` = {S['res']}"
                           if 'index' in S and 'p' in S and 'res' in S else
                           (f"从起点 0 出发，最远终点 `p` = {S['p']}" if 'p' in S else ''))),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink'), ('res', 'res', 'green')],
    captions={
        'f = [nums[0]]': '`f` 存前缀和，之后任意区间和 = `f[r] - f[l-1]`，`O(1)` 求出',
        'f.append': '`f[-1] + {num}` → 前缀和追加 `{f[-1]}`',
        'p = -1': '`p` 是当前起点能到的最远终点，先设为 -1（还没有）',
        'while p + 1 < len(nums) and f[p + 1]': lambda S, B, r: (f'试把终点推到 `{S.p + 1}`：分数 `{S.f[S.p+1]} × {S.p+2}` = {S.f[S.p+1] * (S.p+2)} < `{S.k}` → 可以，继续右移'
                                                         if S.p + 1 < len(S.nums) and S.f[S.p + 1] * (S.p + 2) < S.k
                                                         else f'终点 `{S.p + 1}` 已越界或分数 ≥ `{S.k}` → 起点 0 的最远终点是 `p = {S.p}`'),
        'p += 1': '终点推到 `p = {p}`',
        'res = p + 1': '起点 0 的合法子数组：终点 `0..{p}`，共 `{p + 1}` 个 → `res = {res}`',
        'for index in range': '起点右移到 `index = {index}`，单调性：终点不会比上一轮更靠左',
        'p = max(p': '`p = max(p, index - 1)`：上一轮的 `p` 可以直接继承；若 `p` 落在起点左侧就从 `index-1` 重新开始，现在 `p = {p}`',
        'while p + 1 < len(nums) and (f': lambda S, B, r: (
            (lambda sc: f'试把终点推到 `{S.p + 1}`：分数 `({S.f[S.p+1]} − {S.f[S.index-1]}) × {S.p - S.index + 2}` = {sc} < `{S.k}` → 可以，继续右移'
             if sc < S.k else f'分数 `({S.f[S.p+1]} − {S.f[S.index-1]}) × {S.p - S.index + 2}` = {sc} ≥ `{S.k}` → 停，最远终点 `p = {S.p}`')(
                (S.f[S.p+1] - S.f[S.index-1]) * (S.p - S.index + 2))
            if S.p + 1 < len(S.nums) else f'终点已到数组末尾 → 最远终点 `p = {S.p}`'),
        'res += p - index + 1': '起点 {index} 的合法终点 `{index}..{p}`，共 `{p} - {index} + 1` = =={p - index + 1}== 个 → `res = {res}`',
        'return res': '所有起点加起来一共 `{res}`',
    },
    cards=dict(
        one_liner='先用前缀和 O(1) 求分数，再让终点只右移不回头',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['分数 = 子数组之和 × 长度。数正整数数组里分数 ==严格小于 k== 的子数组个数',
                 '示例：`nums=[2,1,4,3,5]`，`k=10` → `6`'],
        quote='对于一个确定了起点的子数组而言，如果这个子数组的终点越靠后，那么最终的得分就越大。',
        quote_src='—— yiduobo 题解原文',
        idea=['先做前缀和 `f`，已知起点和终点就能 `O(1)` 求分数',
              '枚举起点 `index`，找满足分数小于 k 的最远终点 `p`，贡献 `p - index + 1`',
              '起点 +1 后最远终点只会更靠右 → 不用二分，在上一轮的 `p` 上继续右移（二分是 `O(n log n)`）'],
        summary=['时间 `O(n)`：`p` 只增不减；空间 `O(n)` 存前缀和',
                 '`p = max(p, index - 1)`：避免终点落在起点左边',
                 '`f[index - 1]` 在 `index = 1` 起才使用，起点 0 单独处理',
                 '原文已是 Python 3 可运行写法，代码未改动',
                 '对比灵神：灵神进窗口加和、出窗口减和，不需要前缀和；yiduobo 枚举起点 + 前缀和'],
    ),
)
