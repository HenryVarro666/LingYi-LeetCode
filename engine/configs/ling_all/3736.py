CONFIG = dict(
    num=3736, title='最小操作次数使数组元素相等 III', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='全部补到最大值', tags=[],
    code='''
class Solution:
    def minMoves(self, nums: List[int]) -> int:
        return max(nums) * len(nums) - sum(nums)
''',
    call='Solution().minMoves([2,1,3])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: f"目标值 `m = max(nums) = {max(S['nums'])}`，每个数补到 m", size=34, h=90),
        dict(type='array', var='nums', h=260, label='nums',
             color=lambda S, i, v: 'green' if v == max(S['nums']) else None),
        dict(type='text', fn=lambda S: f"总操作 = `m×n − sum` = `{max(S['nums'])}×{len(S['nums'])} − {sum(S['nums'])}` = =={max(S['nums'])*len(S['nums'])-sum(S['nums'])}==", size=34, h=110),
    ],
    watch=[('max(nums)', 'max(nums)', 'green'), ('len(nums)', 'len(nums)', 'blue'), ('sum(nums)', 'sum(nums)', 'cyan')],
    captions={
        'return max': '最大值 `{max(nums)}` × 个数 `{len(nums)}` − 总和 `{sum(nums)}` = =={ret}==：每个数补到最大值，所需次数之和',
    },
    cards=dict(
        one_liner='元素只能变大，所以统一补到最大值最省',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每步可以把任意一个元素 `+1`，求让所有元素相等的最少步数',
                 '示例：`nums = [2,1,3]` → `3`',
                 '本视频：`[2,1,3]`：2 补 1 次，1 补 2 次，3 不动'],
        quote='由于元素只能变大，所以必须都变成 ≥ m 的数，否则无法都相等。都变成 m 是最优的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最大的数不能变小，所以目标至少是 `m = max(nums)`',
              '目标越大每个数补得越多，所以取 ==目标 = m==',
              '每个数要补 `m − nums[i]`，累加就是 `m·n − sum(nums)`'],
        after=[dict(heading='逐个算一遍', lines=['`nums = [2,1,3]`，最大值 `m = 3`',
                                              '`2` 补 `1` 次，`1` 补 `2` 次，`3` 补 `0` 次',
                                              '合计 `1 + 2 + 0 = 3`，等于 `3×3 − 6 = 3`']),
           dict(heading='为什么不能更小', lines=['最大的数不能减小，所以目标至少是 `m`',
                                                 '目标每大 `1`，每个元素都多补 `1` 次',
                                                 '总次数只会变多，所以 `m` 最优'])],
    summary=['时间 `O(n)`：`max` 和 `sum` 各扫一遍，空间 `O(1)`',
                 '易错点：只能增加不能减少，不能取平均数或最小值',
                 '灵神的思考题：改成每次加 1 或 2，需要再考虑奇偶',
                 '一行代码，核心是把「操作次数」转成 `m·n − sum`'],
    ),
)
