def _formula(S):
    if 'now' not in S or 'index' not in S:
        return '先求总和 `s`，再逐个枚举分割点'
    i, n, s, now = S['index'], S['n'], S['s'], S['now']
    if S['_line'] not in (13, 15, 16, 17, 18):
        return f'把 `nums[{i}]` 并入左半边：前缀和 `now = {now}`'
    if i == n - 1:
        return f'右半边为空，平均值记 0：`diff = {s} // {n}` = =={S["diff"]}=='
    return f'左 `{now} // {i + 1}` = {now // (i + 1)}，右 `{s - now} // {n - i - 1}` = {(s - now) // (n - i - 1)}，差 =={S["diff"]}=='


CONFIG = dict(
    num=2256, title='最小平均差', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='总和减前缀和 · 一趟枚举分割点',
    tags=['灵神题单', '动态规划', '难度分 1395'],
    code='''
class Solution(object):
    def minimumAverageDifference(self, nums):

        s = sum(nums)
        n = len(nums)

        min_diff = None
        res = None
        now = 0
        for index, num in enumerate(nums):
            now += num
            if index == n - 1:
                diff = s // n
            else:
                diff = abs(now // (index + 1) - (s - now) // (n - index - 1))
            if min_diff is None or min_diff > diff:
                min_diff = diff
                res = index
        
        return res
''',
    call='Solution().minimumAverageDifference([2,5,3,9,5,3])',
    expect=3,
    views=[
        dict(type='text', fn=_formula, size=26),
        dict(type='array', var='nums', label='nums（蓝 = 左半边 now，粉 = 右半边 s − now）', h=300,
             pointers={'index': 'blue'},
             color=lambda S, i, v: (('blue' if i <= S['index'] else 'pink') if 'index' in S and 'now' in S else None),
             ),
        dict(type='text', fn=lambda S: (f"目前最小平均差 `min_diff = {S['min_diff']}`，在下标 `res = {S['res']}`" if S.get('min_diff') is not None else ''), size=26),
    ],
    watch=[('s', 's'), ('n', 'n'), ('index', 'index', 'blue'), ('now', 'now', 'cyan'), 'diff', ('min_diff', 'min_diff', 'orange'), ('res', 'res', 'green')],
    captions={
        's = sum': '`s` = 数组总和 =={s}==：后缀和 = `s − 前缀和`，不用再算一遍',
        'min_diff = None': '`min_diff` 初始为 `None`：表示还没有任何候选',
        'res = None': '`res` 记录最优下标',
        'now = 0': '`now` 维护前缀和',
        'for index, num': lambda S, B, r: (f'枚举分割点：左半边 = `nums[0..{S.index}]`' if S.get('now', 0) < S.s else '所有分割点都枚举完了'),
        'now += num': '先把 `nums[{index}]` 加进前缀和：`now = {now}`',
        'if index == n - 1': lambda S, B, r: ('`index == n - 1`：右半边没有元素，==不能除以 0==' if S.index == S.n - 1
                                              else f'`index = {S.index}` 不是最后一个，右半边有 `{S.n - S.index - 1}` 个数'),
        'diff = s // n': '右半边平均值直接记为 0，所以 `diff = s // n` = =={diff}==',
        'diff = abs': '`|{now} // {index+1} − {s-now} // {n-index-1}|` = `|{now // (index+1)} − {(s-now) // (n-index-1)}|` = =={diff}==',
        'if min_diff is None': lambda S, B, r: (f'`diff = {S.diff}`，还没有候选 → ==成为第一个答案==' if S.min_diff is None
                                                else f'`min_diff = {S.min_diff}` 比 `diff = {S.diff}` {"大 → ==更新==" if S.min_diff > S.diff else "不大 → 保留（相等取下标小的）"}'),
        'min_diff = diff': '`min_diff` 更新为 =={min_diff}==',
        'res = index': '`res = {res}`：目前最优下标',
        'return res': '平均差最小的下标是 =={res}==',
    },
    cards=dict(
        one_liner='后缀和 = 总和 − 前缀和，只需维护一个前缀和',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['下标 `i` 的平均差 = 前 `i+1` 个数的平均值与后 `n-i-1` 个数的平均值之差的绝对值（均向下取整）',
                 '后半部分为空时平均值视为 0；返回平均差最小的下标，相同取最小的',
                 '示例：`[2,5,3,9,5,3]` → `3`'],
        quote='这个后缀和可以通过数组总和减去前缀和得到，因此实际上需要求解的只有一个前缀和。',
        quote_src='—— yiduobo 题解原文',
        idea=['区间长度好求：左边 `index+1`，右边 `n-index-1`',
              '先算总和 `s`，枚举分割点时用 `now` 累加前缀和，右边和就是 `s - now`',
              '用 `diff` 与 `min_diff` 比较，严格更小才更新，保证下标最小'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`index == n - 1` 时右半边长度为 0，==不能做除法==，直接记 0',
                 '更新用严格 `>`，相等时保留更小的下标',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
