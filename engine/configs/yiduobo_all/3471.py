CONFIG = dict(
    num=3471, title='找出最大的几近缺失整数', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='分类讨论 · Counter 统计出现次数',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def largestInteger(self, nums, k):
        
        if k == len(nums):
            return max(nums)

        cnt = Counter(nums)
        if k == 1:
            res = -1
            for v in cnt:
                if cnt[v] == 1:
                    res = max(res, v)
            return res
        
        res = -1
        if cnt[nums[0]] == 1:
            res = max(res, nums[0])
        if cnt[nums[-1]] == 1:
            res = max(res, nums[-1])
        return res
''',
    call='Solution().largestInteger([3,9,2,1,7], 3)',
    expect=7,
    views=[
        dict(type='array', var='nums', label='nums', cell=90,
             color=lambda S, i, v: 'green' if 'res' in S and v == S['res'] else None),
        dict(type='map', var='cnt', label='cnt（每个数出现的次数）', fmt=lambda k, v: f'{k}: {v}'),
    ],
    watch=[('k', 'k', 'blue'), ('res', 'res', 'green')],
    captions={
        'if k == len': lambda S, B, r: (f'`k = {S.k} == len(nums)`：只有 nums 自己一个子数组，取最大值' if S.k == len(S.nums)
                                        else f'`k = {S.k} ≠ len(nums) = {len(S.nums)}`，继续分类'),
        'cnt = Counter': '统计每个数在 `nums` 中出现的次数',
        'if k == 1': lambda S, B, r: ('`k = 1`：每个元素自成子数组，要出现==恰好 1 次==' if S.k == 1 else f'`k = {S.k}` 在 2 到 n-1 之间：只看首尾'),
        'res = -1': '先假设没有满足的数：`res = -1`',
        'if cnt[nums[0]]': lambda S, B, r: (f'`cnt[{S.nums[0]}] = {S.cnt[S.nums[0]]}`' + (' == 1 → 首元素满足' if S.cnt[S.nums[0]] == 1 else ' ≠ 1 → 首元素也出现在别处，排除')),
        'res = max(res, nums[0])': '用首元素更新：`res` → =={res}==',
        'if cnt[nums[-1]]': lambda S, B, r: (f'`cnt[{S.nums[-1]}] = {S.cnt[S.nums[-1]]}`' + (' == 1 → 尾元素满足' if S.cnt[S.nums[-1]] == 1 else ' ≠ 1 → 尾元素也出现在别处，排除')),
        'res = max(res, nums[-1])': '用尾元素更新：`res` → =={res}==',
        'return res': lambda S, B, r: f'返回 ==`{r}`==',
    },
    cards=dict(
        one_liner='k 在中间时，只有 nums[0] 和 nums[-1] 可能是答案',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`x` 恰好只出现在 `nums` 的一个长为 `k` 的子数组中，称为几近缺失整数',
                 '返回最大的几近缺失整数，没有返回 `-1`',
                 '本视频：`[3,9,2,1,7]`，`k=3` → `7`'],
        quote='当k的值在2到len(nums) - 1之间时，除了nums[0]以及nums[-1]这两个元素之外，其他所有元素都至少出现在两个子数组中，因此这些元素都不可能是最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`k = len(nums)`：只有一个子数组，答案是 `max(nums)`',
              '`k = 1`：一趟统计次数，取出现 1 次的最大值，没有就 `-1`',
              '其余：用 `cnt` 检查 `nums[0]`、`nums[-1]` 是否只出现 1 次，满足就更新答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`Counter` 已预置，直接使用',
                 '原文为 Python 2 风格，代码未改',
                 '对比灵神：灵神用切片 + `in` 判断首尾，yiduobo 先统一用 Counter 统计'],
    ),
)
