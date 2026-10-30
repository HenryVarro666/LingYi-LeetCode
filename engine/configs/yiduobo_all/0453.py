CONFIG = dict(
    num=453, title='最小操作次数使数组元素相等', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='相对大小 · 减到最小值',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def minMoves(self, nums):

        return sum(nums) - min(nums) * len(nums)
''',
    call='Solution().minMoves([4,1,3,2])',
    expect=6,
    views=[
        dict(type='bars', var='nums', h=330,
             color=lambda S, i, v: 'green' if v == min(S['nums']) else None),
        dict(type='text', fn=lambda S: f"每个元素降到最小值 `{min(S['nums'])}`：需要 " + ' + '.join(str(v - min(S['nums'])) for v in S['nums']) + f" = =={sum(S['nums']) - min(S['nums']) * len(S['nums'])}==", size=30),
    ],
    watch=[('sum(nums)', 'sum(nums)', 'blue'), ('min(nums)', 'min(nums)', 'green'), ('len(nums)', 'len(nums)', 'orange')],
    captions={
        'return sum': '每个元素降到最小值：`sum − min × len` = `{sum(nums)} − {min(nums)} × {len(nums)}` = =={ret}==',
    },
    cards=dict(
        before=[dict(heading='换个角度看操作', lines=['`[1,2,3]` 做一次操作：`[2,3,3]`，最大的两个 +1', '把所有数再 −1：`[1,2,2]`，其实只有 `3` 变成了 `2`', '相对大小上，就是「剩下的那一个数减 1」']),
                dict(heading='为什么减到最小值', lines=['每次只能让一个元素减 1，要全部相等', '最小的元素已经不用动，其他元素都要降到它', '总次数 = 每个元素与最小值差的和']),],
        one_liner='只看相对大小：n-1 个加 1 就是剩下 1 个减 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次让 `n-1` 个元素加 `1`，求让数组所有元素相等的最少操作次数',
                 '示例：`[1,2,3]` → `3`',
                 '本视频：`[4,1,3,2]` → `6`'],
        quote='每个元素的绝对大小并不重要，只需要考察相对大小。对于使n - 1个元素增加1，在相对大小的角度上就可以认为是让剩下的那一个元素减去1。',
        quote_src='—— yiduobo 题解原文',
        idea=['最后只要求元素相等，所以看相对大小就够了',
              '于是题目变成：每次选一个元素减 1，要让所有元素相等',
              '全部减到最小值最少：总次数 = 总和 − 最小值 × 个数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '一行代码：`sum(nums) - min(nums) * len(nums)`',
                 '易错：别真的去模拟 n-1 个加 1，换个角度就是减 1',
                 '原文为 Python 2 风格，除代码前的空行外无需修改'],
    ),
)
