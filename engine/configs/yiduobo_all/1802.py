def _arr(S):
    n = S['n']
    k = S.get('res')
    if k is None:
        return [0] * n
    return [max(1, k - abs(i - S['index'])) for i in range(n)]


def _sum_txt(S):
    if 'res' not in S:
        return ''
    a = _arr(S)
    return f"若 `nums[index] = {S['res']}`，数组 `{a}`，和 = ==`{sum(a)}`== ，上限 `maxSum = {S['maxSum']}`"


CONFIG = dict(
    num=1802, title='有界数组中指定下标处的最大值', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='数学：山峰形 + 分三种情况解 k',
    tags=['二分算法'],
    code='''
class Solution(object):
    def maxValue(self, n, index, maxSum):

        b1 = index
        b2 = n - index - 1
        if b1 > b2:
            b1, b2 = b2, b1
        
        res = int((maxSum * 2 + b1 * b1 + b2 * b2 + b1 + b2) / (2.0 * (b1 + b2 + 1)))
        if res >= b2 + 1:
            return res
        
        res = int(sqrt(2 * (maxSum - n + b1 * b1 + b1) + 0.25) + 0.5 - b1)
        if res >= b1 + 1:
            return res
        
        res = int(sqrt(maxSum - n))
        if (res + 1) * (res + 1) == maxSum - n:
            res += 1
        res += 1
        return res
''',
    setup='from math import sqrt',
    call='Solution().maxValue(6, 1, 10)',
    expect=3,
    views=[
        dict(type='bars', var=_arr, label='按当前 res 摆出的最省数组（山峰形，其余补 1）', pointers={'index': 'pink'}, h=360, cell=90,
             color=lambda S, i, v: 'pink' if i == S['index'] else None, vmax=6),
        dict(type='text', h=90, size=28, fn=_sum_txt),
        dict(type='text', h=70, size=30, fn=lambda S: f"离两端的格子数：较小 `b1 = {S['b1']}`，较大 `b2 = {S['b2']}`" if 'b1' in S and 'b2' in S else ''),
    ],
    watch=[('n', 'n'), ('index', 'index', 'pink'), ('maxSum', 'maxSum', 'cyan'), ('b1', 'b1', 'blue'), ('b2', 'b2', 'purple'), ('res', 'res', 'green')],
    captions={
        'b1 = index': '`index` 左边有 `b1 = {b1}` 个格子',
        'b2 = n - index - 1': '右边有 `b2 = n − index − 1 = {b2}` 个格子',
        'if b1 > b2': lambda S, B, r: ('左边格子更多 → 交换，保证 `b1 ≤ b2`' if S.b1 > S.b2 else f'已经 `b1 = {S.b1} ≤ b2 = {S.b2}`，不用交换'),
        'b1, b2 = b2, b1': '两侧对称，交换后 `b1 = {b1}`，`b2 = {b2}`',
        'res = int((maxSum * 2': '情况 3（k 最大，两侧格子都不够）：解 `(b1+b2+1)k − (b1²+b1+b2²+b2)/2 ≤ maxSum` → `res = {res}`',
        'if res >= b2 + 1': lambda S, B, r: (f'`{S.res} >= {S.b2}+1`：确实比两侧都长 → 情况 3 成立，答案就是它' if S.res >= S.b2 + 1 else f'`{S.res} < {S.b2}+1`：没越过较长一侧，情况 3 不成立，换情况 2'),
        'return res': '`k = {res}` 就是答案',
        'res = int(sqrt(2 * (maxSum': '情况 2（b1 < k ≤ b2）：短侧不够、长侧够，配方得 `k = sqrt(…) + 0.5 − b1` → `res = {res}`',
        'if res >= b1 + 1': lambda S, B, r: (f'`{S.res} >= {S.b1}+1`：越过了短侧 → 情况 2 成立' if S.res >= S.b1 + 1 else f'`{S.res} < {S.b1}+1`：没越过短侧，换情况 1'),
        'res = int(sqrt(maxSum - n))': '情况 1（两侧都够）：`(k−1)² + n ≤ maxSum` → `res = {res}`',
        '(res + 1) * (res + 1)': '处理开方取整的边界',
        'res += 1': '再加 1 还原成 `k`：`res = {res}`',
    },
    cards=dict(
        one_liner='最省的形状是山峰：1…k…1，其余全 1',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['长度 `n` 的正整数数组，相邻差 ≤ 1，总和 ≤ `maxSum`',
                 '在下标 `index` 处让 `nums[index]` 最大，返回这个最大值',
                 '示例：`n=6, index=1, maxSum=10` → `3`（`[2,3,2,1,1,1]`）'],
        quote='为了使得nums[index]最大，且相邻数的插值最多为1，那么理想情况就是 [1, 1, 1, ..., 1, 2, 3, ..., k - 1, k, k - 1, ..., 3, 2, 1, ..., 1, 1, 1] 这种形式，其中k就是对应的nums[index]。',
        quote_src='—— yiduobo 题解原文',
        idea=['山峰形最省：中间 `2k−1` 个数和为 `k²`，其余补 1',
              '`index` 靠边时一侧位置不够，要分三种情况列不等式',
              '三种情况 k 越来越大，所以按 3 → 2 → 1 的顺序，找到合法的就返回'],
        summary=['时间 `O(1)`，直接解不等式，不用二分',
                 '易错：情况 2、3 的合法性要用 `res >= b + 1` 检验',
                 '原文为 Python 2 写法，`sqrt` 来自 math，已在 setup 里 `from math import sqrt`；`/ 2.0` 本身是浮点除法无需改',
                 '常规做法：二分 k + 等差数列求和检查，本题是数学直解'],
    ),
)
