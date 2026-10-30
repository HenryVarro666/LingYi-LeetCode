CONFIG = dict(
    num=1877, title='数组中最大数对和的最小值', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='排序 + 最大配最小',
    tags=['灵神题单', '难度分 1301'],
    code='''
class Solution(object):
    def minPairSum(self, nums):

        nums = sorted(nums)
        n = len(nums)
        res = 0
        for index in range(n // 2):
            res = max(res, nums[index] + nums[n - index - 1])
        
        return res
''',
    call='Solution().minPairSum([5,6,2,4,1,6])',
    expect=9,
    views=[
        dict(type='text', fn=lambda S: (f"配对 `({S['nums'][S['index']]}, {S['nums'][S['n']-S['index']-1]})`，和 ==`{S['nums'][S['index']]+S['nums'][S['n']-S['index']-1]}`==，目前最大数对和 `{S['res']}`" if 'index' in S and 'res' in S and S['_line'] >= 7 else '')),
        dict(type='array', var='nums', h=300, pointers={'index': 'blue', 'n-index-1': 'pink'},
             color=lambda S, i, v: ('blue' if i == S['index'] else 'pink' if i == S['n'] - S['index'] - 1 else None) if 'index' in S and 'res' in S else None),
    ],
    watch=['n', ('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'nums = sorted': '先排序：`{nums}`，最小的在最左，最大的在最右',
        'n = len': '`n = {n}`，共 `{n // 2}` 对',
        'res = 0': '`res` 记录目前最大的数对和',
        'for index': lambda S, B, r: (f'第 `{S.index}` 对：左数第 `{S.index}` 个配右数第 `{S.index}` 个' if S.index != B.get('index') else '所有数对都配完了，循环结束'),
        'res = max': '`{nums[index]} + {nums[n-index-1]}` = {nums[index] + nums[n-index-1]}，`res = max({B.res}, …) = {res}`',
        'return res': '最大数对和的最小值 `{res}`',
    },
    cards=dict(
        one_liner='最大的数配最小的数，两头向中间配对',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['把长度为偶数的数组分成若干数对，每个数恰好用一次',
                 '数对和 `a + b`，要让最大的数对和尽量小',
                 '示例：`[3,5,2,3]` → `7`；本视频：`[5,6,2,4,1,6]` → `9`'],
        quote='设ma和mi为最大值和最小值，ma与x配对，mi与y配对，有 mi + y <= x + y <= ma + x。改成 ma 和 mi 配对，得到 ma + mi 以及 x + y，都不超过 ma + x。',
        quote_src='—— yiduobo 题解原文',
        idea=['设最大数 `ma` 配 `x`，最小数 `mi` 配 `y`', '换成 `ma` 配 `mi`、`x` 配 `y`：两个和都不超过原来的 `ma + x`', '去掉这一对，剩下的同理 → 两头往中间配'],
        summary=['时间 `O(n log n)`，`sorted` 另开数组，空间 `O(n)`',
                 '配对下标：`index` 与 `n - index - 1`',
                 '`res` 初值 0 即可，因为数对和都是正数',
                 '原文为 Python 2 写法，整数除法 `n / 2` 已改为 `n // 2`'],
    ),
)
