def _win(S):
    """当前窗口 [lo, hi]：由 now 的值反推，保证和画面上的窗口和一致"""
    if 'index' not in S:
        return None
    a, i, k, now = S['nums'], S['index'], S['k'], S['now']
    if i < k and S.get('_line') in (4, 5):  # 第一段：窗口从左往右长到 k
        return (0, i) if now == sum(a[:i + 1]) else (0, i - 1)
    if now == sum(a[max(0, i - k + 1):i + 1]):
        return (max(0, i - k + 1), i)
    return (max(0, i - k), i - 1)


def _color(S, i, v):
    if S.get('_line') == 9 and 'index' in S:
        if i == S['index']:
            return 'green'
        if i == S['index'] - S['k']:
            return 'red'
    return None


def P(v):
    return f'({v})' if v < 0 else str(v)


def show(S):
    if 'now' not in S:
        return '先算第一个窗口，再每次右移一格'
    res = S.get('res')
    return f"窗口和 `now = {S['now']}`" + (f"，最大窗口和 `res = {res}`" if res is not None else '')


CONFIG = dict(
    num=643, title='子数组最大平均数 I', difficulty='Easy', category='滑动窗口',
    author='yiduobo', technique='滑动窗口 · 先建窗再平移',
    tags=['字节30天'],
    code='''
class Solution(object):
    def findMaxAverage(self, nums, k):
        now = 0
        for index in range(k):
            now += nums[index]

        res = now
        for index in range(k, len(nums)):
            now += nums[index] - nums[index - k]
            res = max(now, res)

        return res * 1.0 / k
''',
    call='Solution().findMaxAverage([1,12,-5,-6,50,3], 4)',
    expect=12.75,
    views=[
        dict(type='array', var='nums', label='nums（k = 4，青框 = 窗口，绿 = 加入，红 = 移除）', cell=110,
             pointers={'index': 'blue'}, window=(lambda S: (_win(S) or (None, None))[0],
                                                 lambda S: (_win(S) or (None, None))[1]),
             color=_color, h=215),
        dict(type='text', fn=show, size=30, h=80),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    captions={
        'now = 0': '`now` 记录滑动窗口中数字之和',
        'for index in range(k)': lambda S, B, ret: ('先把前 `k` 个数放进窗口' if 'index' not in B else
                                                     ('第一个窗口建好了' if S.index == B.index else f'`index = {S.index}`')),
        'now += nums[index] - nums[index - k]': lambda S, B, ret: (
            f'`now += {S.nums[S.index]} - {P(S.nums[S.index - S.k])}` → `{S.now}`：==一加一减，O(1) 得到新窗口和=='),
        'now += nums[index]': '`nums[{index}] = {nums[index]}` 加入窗口：`now = {now}`',
        'res = now': '第一个窗口 `[0, {k - 1}]` 的和 `{now}` 作为初始答案 `res`',
        'for index in range(k, len': lambda S, B, ret: (f'窗口右移：新加入 `nums[{S.index}]`，移除 `nums[{S.index - S.k}]`'
                                                        if S.index != B.get('index') or B.index < S.k else '已经滑到数组末尾，循环结束'),
        'res = max(now, res)': '`res = max({now}, {B.res}) = {res}`',
        'return res * 1.0 / k': '最大窗口和除以 `k`：`{res} * 1.0 / {k}` = =={ret}==',
    },
    cards=dict(
        one_liner='维护长度为 k 的窗口：加上新进来的，减去刚出去的',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给你整数数组 `nums` 和整数 `k`，找出==长度为 k== 的连续子数组的最大平均数',
                 '示例：`nums = [1,12,-5,-6,50,3]`，`k = 4` → `12.75`',
                 '解释：`(12 - 5 - 6 + 50) / 4 = 51 / 4 = 12.75`'],
        quote='每次将nums[index]加入到滑动窗口中，同时将nums[index - k]从中移除，那么此时滑动窗口中数字之和就要==加上nums[index]然后减去nums[index - k]==。',
        quote_src='—— yiduobo 知乎题解',
        idea=['先用一个循环算出第一个窗口 `[0, k-1]` 的和，作为 `res` 的初值',
              '之后窗口每次右移一格：`now += nums[index] - nums[index - k]`',
              '记录滑动过程中窗口最大的和，==最后除以 k== 就是答案'],
        result='最大窗口和 `51` 出现在下标 1~4，`51 / 4 = 12.75` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`res` 用第一个窗口的和初始化，就不用担心负数时初值取 `0` 出错',
                 '`res * 1.0 / k` 是 Python 2 保证浮点除法的写法，Python 3 下照样正确，未改',
                 '原文删去了文档字符串，其余照搬',
                 '对比灵神：他把「入-更新-出」写在一个循环里，模板更统一'],
    ),
)
