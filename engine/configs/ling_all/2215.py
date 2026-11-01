CONFIG = dict(
    num=2215, title='找出两数组的不同', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='两个哈希集合（Go 原文转写）', tags=[],
    code='''
class Solution:
    def findDifference(self, nums1: List[int], nums2: List[int]) -> List[List[int]]:
        set1, set2 = {}, {}
        for v in nums1:
            set1[v] = True
        for v in nums2:
            set2[v] = True
        a, b = [], []
        for v in set1:
            if not set2.get(v):
                a.append(v)
        for v in set2:
            if not set1.get(v):
                b.append(v)
        return [a, b]
''',
    call='Solution().findDifference([1,2,3,3], [1,1,2,4])',
    expect=[[3], [4]],
    views=[
        dict(type='array', var='nums1', label='nums1', h=110),
        dict(type='array', var='nums2', label='nums2', h=110),
        dict(type='map', var='set1', label='set1', fmt=lambda k, v: f'{k}', h=120),
        dict(type='map', var='set2', label='set2', fmt=lambda k, v: f'{k}', h=120),
        dict(type='array', var='a', label='a：只在 nums1', h=110),
        dict(type='array', var='b', label='b：只在 nums2', h=110),
    ],
    watch=['v', ('a', 'a', 'green'), ('b', 'b', 'orange')],
    captions={
        'set1[v] = True': '`{v}` 放进 set1，重复的数只记一次',
        'set2[v] = True': '`{v}` 放进 set2，重复的数只记一次',
        'a, b = [], []': '两个结果列表先留空',
        'for v in set1': '遍历 set1 里的每个不同数字：`v = {v}`',
        'if not set2.get(v)': lambda S, B, r: f'`{S.v}` 在 set2 里吗？' + ('不在 → 它是 nums1 独有' if not S.set2.get(S.v) else '在 → 两边都有，跳过'),
        'a.append(v)': '`{v}` 只出现在 nums1 → 加入 `a`：{a}',
        'for v in set2': '再遍历 set2 里的每个不同数字：`v = {v}`',
        'if not set1.get(v)': lambda S, B, r: f'`{S.v}` 在 set1 里吗？' + ('不在 → 它是 nums2 独有' if not S.set1.get(S.v) else '在 → 两边都有，跳过'),
        'b.append(v)': '`{v}` 只出现在 nums2 → 加入 `b`：{b}',
        'return [a, b]': '两个列表打包返回：`{ret}`',
    },
    cards=dict(
        one_liner='先各自去重成集合，再互相查有没有',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['给两个数组，返回 `[nums1 独有的不同数, nums2 独有的不同数]`',
                 '示例：`[1,2,3]`、`[2,4,6]` → `[[1,3],[4,6]]`',
                 '本视频：`[1,2,3,3]`、`[1,1,2,4]` → `[[3],[4]]`'],
        quote='func findDifference(nums1, nums2 []int) [][]int { set1, set2 := map[int]bool{}, map[int]bool{} ... }',
        quote_src='—— 灵茶山艾府题解（Go 代码）',
        idea=['用 map 当集合：键是数字，重复写入不影响结果',
              '遍历 set1，不在 set2 的进 `a`；遍历 set2，不在 set1 的进 `b`',
              '遍历的是集合，所以结果天然不重复'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`map[int]bool` → `dict`）',
                 '时间 `O(n+m)`，空间 `O(n+m)`',
                 '易错：要遍历去重后的集合，别遍历原数组，否则 `3` 会被加两次',
                 'Go 的 map 遍历顺序随机，题目允许任意顺序；Python 里按插入顺序'],
    ),
)
