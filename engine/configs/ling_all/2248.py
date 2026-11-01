CONFIG = dict(
    num=2248, title='多个数组求交集', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表计数（Go 原文转写）', tags=[],
    code='''
class Solution:
    def intersection(self, nums: List[List[int]]) -> List[int]:
        ans = []
        cnt = Counter()
        for a in nums:
            for v in a:
                cnt[v] += 1
        for v, c in cnt.items():
            if c == len(nums):
                ans.append(v)
        ans.sort()
        return ans
''',
    call='Solution().intersection([[3,1,2],[2,3,1,4],[3,2,5]])',
    expect=[2, 3],
    views=[
        dict(type='text', fn=lambda S: ('正在统计数组 `' + str(S['a']) + '`' if 'a' in S else '') + (('，当前元素 `v` = ==' + str(S['v']) + '==') if 'v' in S and S['_line'] in (7, 8) else ''), h=90),
        dict(type='map', var='cnt', h=330, label='cnt（出现在几个数组里）'),
        dict(type='array', var='ans', h=170, label='ans'),
    ],
    watch=['a', 'v', 'c', ('len(nums)', 'len(nums)', 'blue')],
    captions={
        'cnt = Counter()': '用哈希表 `cnt` 记录每个数出现的次数',
        'cnt[v] += 1': '`{v}` 在数组内不重复，所以它出现一次就代表又多了一个数组包含它：`cnt[{v}] = {cnt[v]}`',
        'if c == len(nums)': lambda S, B, r: (f'`{S.c} == {len(S.nums)}`：每个数组里都有 `{S.v}` → 成立' if S.c == len(S.nums) else f'`{S.c} != {len(S.nums)}`：有数组缺了 `{S.v}` → 不要'),
        'ans.append': '`{v}` 出现次数等于数组个数，加入答案 → `{ans}`',
        'ans.sort()': '哈希表遍历顺序不保证有序，题目要升序 → 排序 `{ans}`',
        'return ans': '交集（升序）：`{ret}`',
    },
    cards=dict(
        one_liner='元素在每个数组都不重复，次数 = 数组个数就是交集',
        complexity='时间 `O(L + m log m)`（L 为总长度），空间 `O(L)`',
        problem=['二维数组 `nums`，每个子数组内元素互不相同',
                 '返回在==所有==数组里都出现过的数，升序',
                 '示例：`[[3,1,2],[2,3,1,4],[3,2,5]]` → `[2, 3]`'],
        quote='由于 nums[i] 所有元素均不相同，利用这一性质，用哈希表统计每个元素的出现次数，最后遍历哈希表，返回所有次数等于 n 的元素',
        quote_src='—— 灵茶山艾府题解',
        idea=['同一数组里没有重复 → 出现次数 = 包含它的数组个数',
              '次数等于 `len(nums)` 就说明每个数组都有它',
              '哈希表无序，最后要 `sort`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python：`map[int]int` → `Counter`，`sort.Ints` → `ans.sort()`',
                 '复杂度：时间 `O(L + m log m)`，空间 `O(L)`，m 为答案长度',
                 '易错点：依赖「子数组内不重复」这一性质，否则同一数组重复数会被多算',
                 '别忘了排序，Go 的 map 遍历是随机顺序'],
    ),
)
