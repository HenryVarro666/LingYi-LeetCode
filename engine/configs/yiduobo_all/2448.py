def _txt(S):
    if 'now' in S and 'pre_k' in S and 'b' in S and S['_line'] in (16, 17, 18):
        return (f"`右 {S['suf_b']}−{S['suf_k']}×{S['b']} + 左 {S['pre_k']}×{S['b']}−{S['pre_b']}` = =={S['now']}==")
    if 'pre_k' in S:
        return f"左边已处理：`pre_k = {S['pre_k']}`，`pre_b = {S['pre_b']}`；右边：`suf_k = {S['suf_k']}`，`suf_b = {S['suf_b']}`"
    if 'suf_k' in S:
        return f"先求总和：`suf_k = {S['suf_k']}`（cost 之和），`suf_b = {S['suf_b']}`（b×k 之和）"
    return ''


def _cur(S, i, v):
    return 'yellow' if 'b' in S and 'k' in S and 'pre_k' in S and S['sorted_info'][i] == (S['b'], S['k']) else None


CONFIG = dict(
    num=2448, title='使数组相等的最小开销', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='枚举目标值 + 前后缀和',
    tags=['贪心与思维', '难度分 2005'],
    code='''
class Solution(object):
    def minCost(self, nums, cost):

        sorted_info = sorted(zip(nums, cost))
        suf_k = suf_b = 0
        for b, k in sorted_info:
            suf_k += k
            suf_b += b * k
        
        res = None

        pre_b = pre_k = 0
        for b, k in sorted_info:
            suf_k -= k
            suf_b -= b * k
            now = suf_b - suf_k * b + pre_k * b - pre_b
            if res is None or res > now:
                res = now

            pre_k += k
            pre_b += b * k

        return res
''',
    call='Solution().minCost([1,3,5,2], [2,3,1,14])',
    expect=8,
    views=[
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='array', var=lambda S: [b for b, k in S['sorted_info']] if 'sorted_info' in S else None, h=215,
             label='b = nums（排序后）', color=_cur),
        dict(type='array', var=lambda S: [k for b, k in S['sorted_info']] if 'sorted_info' in S else None, h=215,
             label='k = cost', color=_cur),
    ],
    watch=['suf_k', 'suf_b', 'pre_k', 'pre_b', ('now', 'now', 'yellow'), ('res', 'res', 'green')],
    captions={
        'sorted_info =': '把 `nums` 和 `cost` 组合，按 `nums` 从小到大排序：`{sorted_info}`',
        'suf_k += k': '`suf_k` 累加 cost → {suf_k}',
        'suf_b += b * k': '`suf_b` 累加 `b×k = {b*k}` → {suf_b}',
        'res = None': '`res` 先空着，等算出第一个候选值',
        'suf_k -= k': '把 `b = {b}` 从右侧挪出来：`suf_k` → {suf_k}',
        'suf_b -= b * k': '`suf_b` → {suf_b}，现在右边只剩比 `b` 大的数',
        'now =': '目标取 `x = {b}`：右边降到 b 花 `{suf_b} − {suf_k}×{b}`，左边升到 b 花 `{pre_k}×{b} − {pre_b}`，合计 =={now}==',
        'if res is None': lambda S, B, r: f'`now = {S.now}`，' + ('首个候选，直接记下' if S.res is None or B.res is None else f'`res = {B.res}`' + (' 更大 → 更新' if B.res > S.now else ' 更小 → 不变')),
        'pre_k += k': '`b = {b}` 进入左侧：`pre_k` → {pre_k}',
        'pre_b += b * k': '`pre_b` → {pre_b}',
        'return res': '最优目标值已在 nums 中，最小开销 =={res}==',
    },
    cards=dict(
        one_liner='最优目标必在 nums 里：逐个试，前后缀和 O(1) 算开销',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每次可把 `nums` 中任一元素 ±1，第 `i` 个元素的开销是 `cost[i]`',
                 '求让所有元素相等的最小总开销',
                 '示例：`nums=[1,3,5,2], cost=[2,3,1,14]` → `8`'],
        quote='这是若干个绝对值函数的叠加，也就是说这必然是个开口向上的凸函数。更进一步的，可以明确最终的x必然就等于nums中的某一个数。',
        quote_src='—— yiduobo 题解原文',
        idea=['总开销 `c = Σ |x − b[i]|·k[i]` 是绝对值函数叠加，分段为一次函数 → 极值点只在 `b[i]`',
              '排序后逐个枚举 `x = b[i]`，用 `k`、`k·b` 的前缀和与后缀和算出 `c`',
              '`c = 右侧(Σkb − x·Σk) + 左侧(x·Σk − Σkb)`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`res` 用 `None` 作初值，避免写大数',
                 '后缀和先算总和，每轮减去当前项；前缀和每轮结束再加上当前项，顺序别错',
                 '对比灵神：他用加权中位数一次找到目标；这里枚举所有候选并取最小',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
