PAIR_COLORS = ['blue', 'pink', 'green', 'orange', 'purple']


def _pcol(S, i, v):
    if S['_line'] < 4:
        return None
    n = len(S['nums'])
    return PAIR_COLORS[min(i, n - 1 - i) % 5]


def _txt(S):
    nums = S['nums']
    n = len(nums)
    if S['_line'] < 4:
        return '先排序：每轮取的最小、最大，就是排序后首尾一对'
    sums = [nums[i] + nums[n - 1 - i] for i in range(n // 2)]
    pairs = '、'.join(f'`{nums[i]}+{nums[n - 1 - i]}`={s}' for i, s in enumerate(sums))
    return f'每对的和：{pairs} → 去重后有 =={len(set(sums))}== 种'


CONFIG = dict(
    num=2465, title='不同的平均值数目', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='排序 · 首尾配对的和去重',
    tags=[],
    code='''
class Solution:
    def distinctAverages(self, nums: List[int]) -> int:
        nums.sort()
        return len(set(nums[i] + nums[-i - 1] for i in range(len(nums) // 2)))
''',
    call='Solution().distinctAverages([4,1,4,0,3,5])',
    expect=2,
    views=[
        dict(type='text', fn=_txt, size=28, h=110),
        dict(type='array', var='nums', label='nums（同色 = 同一轮删掉的一对）', cell=110, h=220, color=_pcol),
    ],
    watch=[('len(nums)', 'len(nums)', 'blue')],
    captions={
        'nums.sort()': '排序后 `nums = {nums}`：第 `i` 轮删掉的最小值是 `nums[i]`，最大值是 `nums[-i-1]`',
        'return len(set(': lambda S, B, r: (
            '把每对的和放进集合：平均值 = 和 / 2，==和相同 ⇔ 平均值相同==，所以不用除以 2。'
            f'和依次为 `{[S.nums[i] + S.nums[-i - 1] for i in range(len(S.nums) // 2)]}`，去重后 `{r}` 个'),
    },
    cards=dict(
        one_liner='排序后首尾配对，平均值相同等价于两数之和相同',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每轮删掉当前最小值和最大值，计算两数平均值，直到数组为空',
                 '求出现过多少种不同的平均值',
                 '示例：`[4,1,4,0,3,5]` → 平均值 2.5、2.5、3.5 → `2`'],
        quote='排序后，每次取出的最小和最大的数就是 nums[i] 和 nums[n-1-i]。把这两个数的和放入哈希表中（不需要除以 2，因为只计算不同平均值的个数，两个平均值不同，等价于两数之和不同）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后，第 `i` 轮删掉的就是 `nums[i]` 和 `nums[n-1-i]`，不用真的删',
              '平均值只用来比较，直接用 ==和== 代替，省掉除法和浮点数',
              '`set` 去重，答案就是集合大小'],
        after=[dict(heading='为什么不用除以 2', lines=[
            '`(a+b)/2 == (c+d)/2` 当且仅当 `a+b == c+d`',
            '只比较和，整数运算又快又没有浮点误差',
            '示例中三对和 5、5、7，去重得 `{5, 7}`'])],
        result='排序后 `[0,1,3,4,4,5]`：和为 5、5、7，集合 `{5, 7}` → 返回 2',
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错：不需要除以 2，更不要用浮点数比较',
                 '`nums[-i-1]` 就是倒数第 `i+1` 个，等价于 `nums[n-1-i]`',
                 '长度保证是偶数，所以 `len(nums) // 2` 对刚好覆盖所有元素'],
    ),
)
