CONFIG = dict(
    num=2215, title='找出两数组的不同', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='两个集合互相检测',
    tags=[],
    code='''
class Solution(object):
    def findDifference(self, nums1, nums2):

        set1 = set(nums1)
        set2 = set(nums2)
        res = [[], []]
        for num in set1:
            if num not in set2:
                res[0].append(num)
        
        for num in set2:
            if num not in set1:
                res[1].append(num)
        
        return res
''',
    call='Solution().findDifference([1,2,3,3,5], [2,4,6,4])',
    expect=[[1, 3, 5], [4, 6]],
    views=[
        dict(type='array', var='nums1', label='nums1', color=lambda S, i, v: 'yellow' if S.get('num') == v and S['_line'] in (7, 8, 9) else None, h=130),
        dict(type='array', var='nums2', label='nums2', color=lambda S, i, v: 'yellow' if S.get('num') == v and S['_line'] in (11, 12, 13) else None, h=130),
        dict(type='set', var='set1', label='set1（nums1 去重）', fmt=lambda x: str(x), h=110),
        dict(type='set', var='set2', label='set2（nums2 去重）', fmt=lambda x: str(x), h=110),
        dict(type='text', h=90, size=34, fn=lambda S: f"`res` = ==[{S['res'][0]}, {S['res'][1]}]==" if 'res' in S else '`res` 还没有创建'),
    ],
    watch=[('num', 'num', 'yellow'), ('res[0]', 'res[0]', 'green'), ('res[1]', 'res[1]', 'orange')],
    captions={
        'set1 = set(nums1)': '`nums1` 放进集合：==去重==，并且查找只要 O(1) → `{sorted(set1)}`',
        'set2 = set(nums2)': '`nums2` 也放进集合 → `{sorted(set2)}`',
        'res = [[], []]': '`res[0]` 放只在 nums1 的数，`res[1]` 放只在 nums2 的数',
        'for num in set1': '枚举 `set1` 里的每个数：`num = {num}`',
        'if num not in set2': lambda S, B, r: (f'`{S.num}` 不在 set2 里 → ==只属于 nums1==' if S.num not in S.set2
                                               else f'`{S.num}` 在 set2 里 → 两边都有，不算'),
        'res[0].append(num)': '`{num}` 记入 `res[0]` → `{res[0]}`',
        'for num in set2': '换到 `set2`，反过来检查：`num = {num}`',
        'if num not in set1': lambda S, B, r: (f'`{S.num}` 不在 set1 里 → ==只属于 nums2==' if S.num not in S.set1
                                               else f'`{S.num}` 在 set1 里 → 两边都有，不算'),
        'res[1].append(num)': '`{num}` 记入 `res[1]` → `{res[1]}`',
        'return res': '两个方向都检查完，返回 `{res}`',
    },
    cards=dict(
        one_liner='先各自去重成集合，再互相查有没有',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['返回两个列表：只在 `nums1` 里的不同整数、只在 `nums2` 里的不同整数',
                 '示例：`[1,2,3]`、`[2,4,6]` → `[[1,3],[4,6]]`',
                 '本视频：`[1,2,3,3,5]`、`[2,4,6,4]` → `[[1,3,5],[4,6]]`'],
        quote='将两个数组的数分别放入两个集合中，然后分别枚举两个集合中的每个数字，检测其是否在另一个集合中出现过并根据出现情况更新答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['集合自带去重，题目要求“不同”的整数正好用得上',
              '枚举 set1 的数，不在 set2 → 放进 `res[0]`',
              '再枚举 set2 的数，不在 set1 → 放进 `res[1]`'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '题目允许任意顺序，所以直接遍历集合即可，不用排序',
                 '易错：不要直接遍历数组，否则重复的数会被记入多次',
                 '原文为 Python 2 风格，只删去了类型说明，代码一字未改'],
    ),
)
