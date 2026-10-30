CONFIG = dict(
    num=3689, title='最大子数组总值 I', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='最大差值子数组重复选 k 次',
    tags=['灵神题单', '难度分 1371'],
    code='''
class Solution:
    def maxTotalValue(self, nums: List[int], k: int) -> int:
        return (max(nums) - min(nums)) * k
''',
    call='Solution().maxTotalValue([4,2,5,1], 3)',
    expect=12,
    views=[
        dict(type='array', var='nums', h=240, label='nums（绿 = 最大值，红 = 最小值）',
             color=lambda S, i, v: ('green' if v == max(S['nums']) else 'red' if v == min(S['nums']) else None) if 'nums' in S else None),
        dict(type='text', fn=lambda S: f"`(max − min) × k` = `({max(S['nums'])} − {min(S['nums'])}) × {S['k']}` = =={(max(S['nums'])-min(S['nums']))*S['k']}==" if 'nums' in S else ''),
    ],
    watch=['k', ('max', 'max(nums)', 'green'), ('min', 'min(nums)', 'red')],
    captions={
        'return': '最大值 `{max(nums)}`，最小值 `{min(nums)}`：整个数组的差 `{max(nums) - min(nums)}` 是任何子数组的上限，重复选 `{k}` 次 → =={ret}==',
    },
    cards=dict(
        one_liner='子数组可重复选：把最大差值的那个选 k 次',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['选恰好 `k` 个子数组，可重叠，也可重复选同一个',
                 '子数组的值 = 最大值 − 最小值，求总值最大',
                 '示例：`[4,2,5,1]`，`k = 3` → `12`'],
        quote='由于同一个子数组可以重复选，所以最优解是，把差值最大的子数组重复选 k 次。子数组的最大差值，等于 nums 的最大值减去 nums 的最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['重复选不受限制 → 每次都选当前最好的',
              '子数组越长，max 越大、min 越小 → 整个数组差值最大',
              '答案 = `(max − min) × k`'],
        after=[dict(heading='为什么整个数组最大', lines=['子数组越长，最大值只增不减，最小值只减不增', '所以任何子数组的值 `<=` 整个数组的值', '例：`[4,2,5,1]` 整体值 `5-1=4`，三次共 `12`', '`k` 次重复选取，每次都取到上限'])],
        before=[dict(heading='先看一个小例子', lines=['`nums = [1,3,2]`，`k = 2`', '最大的子数组值：`3 − 1 = 2`（整个数组）', '同一个子数组选两次：`2 + 2 = 4`', '不必去找别的子数组，重复选就行'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先找“每次选什么最好”，再乘 k',
                 '思考题：同时求 max 和 min 最多 3N/2 次比较（成对比较），见 CF730B'],
    ),
)
