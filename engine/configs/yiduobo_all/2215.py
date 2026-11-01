CONFIG = dict(
    num=2215, title='找出两数组的不同', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='集合去重 + 互查', tags=[],
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
    call='Solution().findDifference([1,2,3,3], [1,1,2,4])',
    expect=[[3], [4]],
    views=[
        dict(type='array', var='nums1', label='nums1', h=110),
        dict(type='array', var='nums2', label='nums2', h=110),
        dict(type='set', var='set1', label='set1', fmt=lambda x: str(x), h=110),
        dict(type='set', var='set2', label='set2', fmt=lambda x: str(x), h=110),
        dict(type='text', fn=lambda S: ('结果 res：' + str(S['res'])) if 'res' in S else '', size=34, h=70),
    ],
    watch=['num', ('res', 'res', 'green')],
    captions={
        'set1 = set': '`nums1` 放进集合 set1：重复的 3 被合并',
        'set2 = set': '`nums2` 放进集合 set2：重复的 1 被合并',
        'res = [[], []]': '`res[0]` 放 nums1 独有的，`res[1]` 放 nums2 独有的',
        'for num in set1': '枚举 set1 的每个数：`num = {num}`',
        'if num not in set2': lambda S, B, r: f'`{S.num}` 在 set2 里出现过吗？' + ('没有 → 要记录' if S.num not in S.set2 else '出现过 → 跳过'),
        'res[0].append': '`{num}` 记入 `res[0]`：{res[0]}',
        'for num in set2': '换成枚举 set2 的每个数：`num = {num}`',
        'if num not in set1': lambda S, B, r: f'`{S.num}` 在 set1 里出现过吗？' + ('没有 → 要记录' if S.num not in S.set1 else '出现过 → 跳过'),
        'res[1].append': '`{num}` 记入 `res[1]`：{res[1]}',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='两个集合互相查：对方没有的就是答案',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['返回 `[nums1 中不在 nums2 的不同数, nums2 中不在 nums1 的不同数]`',
                 '示例：`[1,2,3,3]`、`[1,1,2,2]` → `[[3],[]]`',
                 '本视频：`[1,2,3,3]`、`[1,1,2,4]` → `[[3],[4]]`'],
        quote='将两个数组的数分别放入两个集合中，然后分别枚举两个集合中的每个数字，检测其是否在另一个集合中出现过并根据出现情况更新答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`set()` 一步完成去重，不用自己判断重复',
              '`num not in set2` 是 `O(1)` 的哈希查询',
              '枚举集合而不是数组，每个数只会处理一次'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '易错：必须先去重；直接枚举数组会把重复数字重复加入',
                 '代码与原文一致，无需改动（本题没有 Python 2 专有写法）'],
    ),
)
