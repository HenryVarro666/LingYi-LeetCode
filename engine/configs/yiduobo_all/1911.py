def _top(S):
    if 'index' not in S:
        return '贪心：答案的第 1 个数是第一个山峰，第 2 个数是第一个山谷，依次类推'
    i = S['index']
    nums = S['nums']
    if i >= len(nums):
        return f'扫描结束：`res = {S["res"]}`'
    need = '山峰（往下掉就取正）' if S['l'] % 2 == 0 else '山谷（往上爬就取负）'
    return f'已选 `{S["l"]}` 个数，现在找==下一个{need}==；`now = {S["now"]}`'


CONFIG = dict(
    num=1911, title='最大子序列交替和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='贪心 · 依次取山峰山谷',
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
    call='Solution().maxAlternatingSum([6,2,1,2,4,5])',
    expect=10,
    views=[
        dict(type='text', fn=_top, size=26, h=70),
        dict(type='array', var='nums', label='nums（末尾补了一个 0）', cell=100, h=300,
             pointers={'index': 'blue', 'index - 1': 'pink'},
             color=lambda S, i, v: ('blue' if i == S.get('index') else 'pink' if i == S.get('index', 0) - 1 and 'index' in S else None)),
        dict(type='text', fn=lambda S: f'交替和 `now` = =={S["now"]}==，已取 `{S["l"]}` 个数（偶数个数时找山峰，奇数个时找山谷）' if 'l' in S else '', size=24, h=60),
    ],
    watch=[('index', 'index', 'blue'), ('l', 'l', 'purple'), ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    captions={
        'now = 0': '`now`：当前选出的子序列的交替和',
        'l = 0': '`l`：已经选了几个数；==偶数个==时要找山峰，==奇数个==时要找山谷',
        'nums.append(0)': '末尾补一个 `0`：这样最后一段上升的山峰也会被当成“下降”而计入答案',
        'res = 0': '`res` 记录每次取到山峰后的最大交替和',
        'for index in range': lambda S, B, r: (f'看相邻两个数 `nums[{S.index - 1}] = {S.nums[S.index - 1]}` 和 `nums[{S.index}] = {S.nums[S.index]}`' if S.get('index') != B.get('index') or 'index' not in B else '扫描完毕'),
        'if l & 1': lambda S, B, r: ('`l` 是奇数：上一个选的是山峰，现在==找山谷==' if S.l & 1 else '`l` 是偶数：现在==找山峰=='),
        'if nums[index] > nums[index - 1]': '`{nums[index]} > {nums[index - 1]}` → ' + '{"开始上升，前一个数就是山谷" if nums[index] > nums[index - 1] else "还在下降，山谷还没到"}',
        'if nums[index] < nums[index - 1]': '`{nums[index]} < {nums[index - 1]}` → ' + '{"开始下降，前一个数就是山峰" if nums[index] < nums[index - 1] else "还在上升，山峰还没到"}',
        'now -= nums[index - 1]': '山谷 `{nums[index - 1]}` 取负：`now` = {B.now} − {nums[index - 1]} = =={now}==',
        'now += nums[index - 1]': '山峰 `{nums[index - 1]}` 取正：`now` = {B.now} + {nums[index - 1]} = =={now}==',
        'res = max': '山峰刚加入，更新答案：`res = max({B.res}, {now}) = {res}`',
        'l += 1': '又选了一个数：`l` → {l}',
        'return res': '最大交替和 `{res}`',
    },
    cards=dict(
        one_liner='第一个数取第一个山峰，第二个取第一个山谷，依次扫描',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['交替和：偶数下标的和 减去 奇数下标的和',
                 '求 `nums` 的任意子序列的==最大交替和==（子序列下标重新编号）',
                 '示例：`[6,2,1,2,4,5]` → `10`，最优子序列 `[6,1,5]`'],
        quote='看上去应该是动态规划的题目，不过我在这里用的是贪心法。……答案中的第一个数是nums的第一个山峰。',
        quote_src='—— yiduobo 题解原文',
        idea=['若第一个数选在山峰之前，山峰处必为正，前面部分两两配对都 ≤ 0，不如不要',
              '若第一个数选在山峰之后，用“山峰、山谷、它”三个数一定更优',
              '第二个数同理是第一个山谷；剩下的后缀又回到同一个问题'],
        result='`6 − 1 + 5 = 10`：山峰 6，山谷 1，山峰 5 ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '末尾补 `0`：否则最后一段上升的峰值会丢掉',
                 '只在==取到山峰后==更新 `res`；取山谷后不更新',
                 '原文为 Python 2 风格写法，Python 3 下无需修改即可运行',
                 '对比灵神的状态机 DP：这里用贪心直接跳过 DP'],
    ),
)
