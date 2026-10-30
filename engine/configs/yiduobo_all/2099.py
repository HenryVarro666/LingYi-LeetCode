CONFIG = dict(
    num=2099, title='找到和最大的长度为 K 的子序列', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='降序下标 + 集合标记',
    tags=['贪心', '排序', '难度分 1447'],
    code='''
class Solution(object):
    def maxSubsequence(self, nums, k):

        n = len(nums)
        order = sorted(range(n), key=lambda d:-nums[d])
        chosen = set(order[:k])
        res = []
        for index in range(n):
            if index in chosen:
                res.append(nums[index])
        
        return res
''',
    call='Solution().maxSubsequence([-1,5,3,-2,4,3], 3)',
    expect=[5, 3, 4],
    views=[
        dict(type='array', var='nums', h=200, label='nums', pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if 'chosen' in S and i in S['chosen'] else None),
        dict(type='set', var='chosen', h=120, label='chosen（入选下标）'),
        dict(type='array', var='res', h=130, label='res'),
    ],
    watch=[('k', 'k', 'blue')],
    captions={
        'order = sorted': '把下标按 `nums` 从大到小排：`order` = {order}，前 `k` 个就是最大的 `k` 个数的位置',
        'chosen = set': '前 `{k}` 个下标放进集合：`chosen` = {chosen}，查询是否入选只要 `O(1)`',
        'if index in chosen': '下标 `{index}` 在 `chosen` 里吗？→ {"在，保留" if index in chosen else "不在，跳过"}',
        'res.append': '按原顺序遍历，保证子序列顺序不变：`res` = {res}',
        'return res': '顺序和原数组一致：=={ret}==',
    },
    cards=dict(
        one_liner='最大的 K 个下标放进集合，再按原顺序扫描',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['在 `nums` 中选长度为 `k` 的子序列，使和最大',
                 '子序列保持原相对顺序，返回任意一个',
                 '示例：`[-1,-2,3,4]`，`k=3` → `[-1,3,4]`'],
        quote='题目要求找出和最大的长度为K的子序列，那么显然应该选择数组中最大的K个数，于是只需将数组从大到小排序后选择top K的数即可。',
        quote_src='—— yiduobo 题解',
        idea=['和最大 → 选最大的 `K` 个数',
              '排序下标而不是数值，这样不会丢掉位置信息',
              '`chosen` 记下入选位置，再从头扫一遍，按原顺序收集'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '排序用 `-nums[d]` 当 key 实现降序',
                 '最后一遍按下标顺序扫描，才能保证子序列顺序',
                 '数值相同时选哪个都对，答案可能与示例顺序不同但和一样'],
    ),
)
