CONFIG = dict(
    num=349, title='两个数组的交集', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='set 去重统计',
    code='''
class Solution(object):
    def intersection(self, nums1, nums2):

        num_set = set()
        for num in nums1:
            num_set.add(num)

        res = []
        for num in nums2:
            if num in num_set:
                res.append(num)
                num_set.remove(num)

        return res
''',
    call='Solution().intersection([4,9,5,9], [9,4,9,8,4])',
    expect=[9, 4],
    views=[
        dict(type='array', var='nums1', label='nums1', h=130),
        dict(type='set', var='num_set', label='num_set（nums1 中出现过的数）', fmt=lambda x: str(x), h=150),
        dict(type='array', var='nums2', label='nums2', h=130),
        dict(type='array', var='res', label='res（结果）', h=130),
    ],
    watch=[('num', 'num', 'blue'), ('res', 'res', 'green')],
    captions={
        'num_set = set()': '先准备一个空集合，不关心出现几次，只关心==出没出现==',
        'num_set.add(num)': '`nums1` 里的 `{num}` 放进集合 → `{num_set}`（重复的自动合并）',
        'res = []': '`res` 用来放交集',
        'for num in nums2': '扫描 `nums2`：现在 `num = {num}`',
        'if num in num_set': lambda S, B, r: (f'`{S.num}` 在集合里 → 两个数组都有' if S.num in S.num_set else f'`{S.num}` 不在集合里 → 不是交集元素，或者已经收过了'),
        'res.append(num)': '收下 `{num}` → `res = {res}`',
        'num_set.remove(num)': '从集合里删掉 `{num}`：这样 `nums2` 里再出现它就不会重复收',
        'return res': '`nums2` 扫完，交集为 `{ret}`',
    },
    cards=dict(
        one_liner='349 不管次数，一个 set 就够了',
        complexity='时间 `O(n+m)`，空间 `O(n)`',
        problem=['求两个数组的交集，结果里每个数只出现一次，顺序不限',
                 '示例：`[1,2,2,1]` 与 `[2,2]` → `[2]`',
                 '本视频：`[4,9,5,9]` 与 `[9,4,9,8,4]` → `[9,4]`'],
        quote='349不需要考虑出现的次数，因此使用set统计一下即可。350则需要使用dict来进行统计。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一遍：把 `nums1` 全部加入集合，重复的自动去掉',
              '第二遍：扫 `nums2`，在集合里就收进 `res`，并立刻从集合删除',
              '删除这一步保证每个数只收一次'],
        summary=['时间 `O(n+m)`，空间 `O(n)`',
                 '易错：忘记 `remove` 会让答案里出现重复的 `9`',
                 '350（要计次数）要换成 dict；若两数组已排序，可用二路归并'],
    ),
)
