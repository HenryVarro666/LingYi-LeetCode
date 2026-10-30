CONFIG = dict(
    num=453, title='最小操作次数使数组元素相等', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='等价转化 · 全减到最小值',
    tags=['灵神题单'],
    code='''
class Solution:
    def minMoves(self, nums: List[int]) -> int:
        return sum(nums) - min(nums) * len(nums)
''',
    call='Solution().minMoves([1,2,3,5,4])',
    expect=10,
    views=[
        dict(type='array', var='nums', label='nums', h=260,
             color=lambda S, i, v: 'green' if v == min(S['nums']) else None),
        dict(type='text', fn=lambda S: f"总和 `{sum(S['nums'])}` − 最小值 `{min(S['nums'])}` × 个数 `{len(S['nums'])}` = =={sum(S['nums']) - min(S['nums']) * len(S['nums'])}==", size=34),
        dict(type='text', fn=lambda S: '每个数都要减到最小值：' + ' + '.join(f"({v}−{min(S['nums'])})" for v in S['nums']) + f" = =={sum(v - min(S['nums']) for v in S['nums'])}==", size=30),
    ],
    watch=[('sum(nums)', 'sum(nums)', 'blue'), ('min(nums)', 'min(nums)', 'green'), ('len(nums)', 'len(nums)', 'orange')],
    captions={
        'return sum': '把 `n-1` 个数加 1，等价于 1 个数减 1；所有数都减到最小值 `{min(nums)}`：`{sum(nums)} − {min(nums)} × {len(nums)}` = =={ret}==',
    },
    cards=dict(
        before=[dict(heading='先看示例怎么走', lines=['`[1,2,3]` → `[2,3,3]` → `[3,4,3]` → `[4,4,4]`，共 3 次', '换成「每次把一个数减 1」：`[1,2,3]` → `[1,1,3]` → `[1,1,2]` → `[1,1,1]`，也是 3 次', '两种操作的次数一样，但后者只改一个数，好算得多']),
                dict(heading='为什么降到最小值最优', lines=['数只能变小，所以最终值 `<= min(nums)`', '每个数至少要减 `nums[i] - 最终值` 次，最终值越小越亏', '所以取最终值 = `min(nums)`，总次数 = `sum(nums) - min(nums) * n`'])],
        one_liner='n-1 个数加 1，等价于 1 个数减 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次操作让 `n-1` 个元素加 `1`，求让所有元素相等的最少操作次数',
                 '示例：`[1,2,3]` → `3`',
                 '本视频：`[1,2,3,5,4]` → `10`'],
        quote='把 `n-1` 个数都增加 `1`，等价于把 `1` 个数减少 `1`。',
        quote_src='—— 灵茶山艾府题解',
        idea=['题目只要求最后相等，不要求等于某个值，所以可以省略「全体加 1」',
              '操作变成：每次选一个数减 1，数只会变小，必须都降到 `<= min`',
              '都降到最小值 `m` 最省：次数 = `sum(nums) - m * n`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '关键是等价转化：加 n-1 个 ≈ 减 1 个，别去模拟',
                 '易错：不需要排序，也不需要找目标值，最小值就是终点',
                 '同类思路：把「改 n-1 个」转成「改 1 个」的相对变化'],
    ),
)
