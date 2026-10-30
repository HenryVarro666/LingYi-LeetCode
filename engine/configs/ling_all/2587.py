CONFIG = dict(
    num=2587, title='重排数组以得到最大前缀分数', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='降序排序 · 前缀和',
    tags=['贪心与思维', '从最小/最大开始贪心', '难度分 1337'],
    code='''
class Solution:
    def maxScore(self, nums: List[int]) -> int:
        nums.sort(reverse=True)
        return sum(s > 0 for s in accumulate(nums))
''',
    call='Solution().maxScore([2,-1,0,1,-3,3,-3])',
    expect=6,
    views=[
        dict(type='array', var='nums', label='nums（降序后）',
             color=lambda S, i, v: ('green' if v > 0 else 'pink') if S['_line'] >= 4 and v != 0 else None,
             h=220),
        dict(type='text', fn=lambda S: ('前缀和 = ' + ', '.join(str(x) for x in accumulate(S['nums'])) if 'nums' in S and S['_line'] >= 4 else '先把大的放前面'), size=26),
    ],
    watch=[('nums', 'nums', 'blue')],
    captions={
        'nums.sort': '==负数放后面==：它会拖累后面所有前缀和；负数里绝对值小的靠前。降序排序：`{nums}`',
        'return sum': lambda S, B, r: ('前缀和 `' + str(list(accumulate(S.nums))) + '`，其中 `>0` 的有 ==' + str(r) + '== 个'),
    },
    cards=dict(
        after=[dict(heading='为什么降序就对', lines=['正数从大到小：前缀和涨得最快、不会提前掉下去', '接着是 `0`，不改变前缀和', '然后负数从大到小（绝对值小的先）：前缀和降得最慢', '例：`[3,2,1,0,-1,-3,-3]` 前缀和 `3,5,6,6,5,2,-1`，只有最后一项 `<= 0`']),
               dict(heading='复杂度与实现', lines=['瓶颈是排序 `O(n log n)`', '`accumulate` 一次扫描求前缀和，`O(n)`', '`sum(布尔值)` 直接数出正数前缀和个数'])],
        one_liner='负数放最后、绝对值小的靠前，前缀和能正更久',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['可以任意重排 `nums`，`prefix[i]` 是前 `i+1` 个数之和',
                 '分数 = `prefix` 中正整数的个数，求最大分数',
                 '示例：`[2,-1,0,1,-3,3,-3]` → `6`'],
        quote='对于一个负数来说，它后面的前缀和都会把这个负数加进去。',
        quote_src='—— 灵茶山艾府题解',
        idea=['负数尽量放后面，这样前面的前缀和不受它影响',
              '绝对值小的负数排在负数的前面，前缀和更晚才变负',
              '这正是降序排序，再数 `> 0` 的前缀和'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '一行写法：`sum(s > 0 for s in accumulate(nums))`',
                 '前缀和一旦 `<= 0` 就不会再变正，所以直接数 `> 0` 的个数也正确',
                 '易错：`0` 也不算正数'],
    ),
)
