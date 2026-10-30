CONFIG = dict(
    num=1911, title='最大子序列交替和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='贪心 · 山峰山谷',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1786'],
    code='''
class Solution(object):
    def maxAlternatingSum(self, nums):
        now = 0
        l = 0
        nums.append(0)
        res = 0
        for index in range(1, len(nums)):
            if l & 1:
                if nums[index] > nums[index - 1]:
                    now -= nums[index - 1]
                    l += 1
            else:
                if nums[index] < nums[index - 1]:
                    now += nums[index - 1]
                    res = max(res, now)
                    l += 1

        return res
''',
    call='Solution().maxAlternatingSum([6, 2, 1, 2, 4, 5])',
    expect=10,
    views=[
        dict(type='array', var='nums', label='nums（末尾补的 0 保证最后一个山峰也能算进来）', h=210, cell=80,
             pointers={'index': 'blue'}, window=('index', 'index'),
             color=lambda S, i, v: 'green' if 'index' in S and i == S['index'] - 1 and S['l'] % 2 == 1 and S['_line'] in (11, 12, 13, 14) else None),
        dict(type='text', h=80, size=26,
             fn=lambda S: ('' if 'now' not in S else f"当前交替和 `now = {S['now']}`，已取 `{S['l']}` 个数，下一个要找==" + ('山谷（下降后回升）' if S['l'] % 2 else '山峰（上升后下降）') + '==')),
    ],
    watch=[('index', 'index', 'blue'), ('l（已取个数）', 'l', 'purple'), ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    captions={
        'now = 0': '`now` 是当前选出序列的交替和',
        'l = 0': '`l` 记录已经选了几个数：偶数个 → 下一个找山峰，奇数个 → 下一个找山谷',
        'nums.append(0)': '末尾补一个 0：最后一段单调递增也会有一个“下降”，最后的山峰不会丢',
        'res = 0': '`res` 保存最大交替和',
        'for index in range': '看相邻两数 `nums[{index-1}]` 和 `nums[{index}]`',
        'if l & 1': lambda S, B, r: ('`l` 是奇数：刚取了山峰，现在找山谷' if S.l & 1 else '`l` 是偶数：现在找山峰'),
        'if nums[index] > nums[index - 1]': lambda S, B, r: (f'`{S.nums[S.index]} > {S.nums[S.index-1]}` 成立：回升了，`{S.nums[S.index-1]}` 是山谷，可以取' if S.nums[S.index] > S.nums[S.index-1]
                                                              else f'`{S.nums[S.index]} > {S.nums[S.index-1]}` 不成立：还在下降，山谷在后面，继续看'),
        'now -= nums[index - 1]': '山谷 `{nums[index-1]}` 取负号：`now = {now}`',
        'if nums[index] < nums[index - 1]': lambda S, B, r: (f'`{S.nums[S.index]} < {S.nums[S.index-1]}` 成立：下降了，`{S.nums[S.index-1]}` 是山峰，可以取' if S.nums[S.index] < S.nums[S.index-1]
                                                              else f'`{S.nums[S.index]} < {S.nums[S.index-1]}` 不成立：还在上升，山峰在后面，继续看'),
        'now += nums[index - 1]': '山峰 `{nums[index-1]}` 取正号：`now = {now}`',
        'res = max': '每加入一个山峰就更新答案：`res = max({B.res}, {now}) = {res}`',
        'l += 1': lambda S, B, r: f'已取 `l = {S.l}` 个数，接下来找' + ('山谷' if S.l & 1 else '山峰'),
        'return res': '一趟扫描结束，答案 `{ret}`',
    },
    cards=dict(
        one_liner='不用 DP：依次取第一个山峰、第一个山谷……',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['交替和 = 偶数下标之和 − 奇数下标之和',
                 '求 `nums` 任意子序列的==最大交替和==',
                 '示例：`[6,2,1,2,4,5]` → `10`（子序列 `[6,1,5]`）'],
        quote='答案中的第一个数必然是nums中第一个山峰的值……答案中的第二个数必然是nums中的第一个山谷。',
        quote_src='—— yiduobo 题解原文',
        idea=['先证明：答案第一个数是第一个山峰；第二个数是第一个山谷',
              '之后剩下的后缀又回到同样的问题，所以一趟扫描交替取峰、谷',
              '每加入一个山峰就更新答案；末尾补 `0` 以免漏掉最后一个山峰'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Python 2 风格写法，在 Python 3 下无需改动，只删去了类型说明与多余空行',
                 '易错：必须在 `nums` 末尾补 `0`，否则结尾递增的数组会丢掉最后的山峰',
                 '对比 DP：灵神用选/不选的两个状态转移，这里靠贪心证明省掉状态'],
    ),
)
