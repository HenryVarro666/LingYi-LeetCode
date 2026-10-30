CONFIG = dict(
    num=2956, title='找到两个数组中的公共元素', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希集合',
    code='''
class Solution:
    def findIntersectionValues(self, nums1: List[int], nums2: List[int]) -> List[int]:
        set1 = set(nums1)
        set2 = set(nums2)
        return [sum(x in set2 for x in nums1),
                sum(x in set1 for x in nums2)]
''',
    call='Solution().findIntersectionValues([4,3,2,3,1], [2,2,5,2,3,6])',
    expect=[3, 4],
    views=[
        dict(type='array', var='nums1', label='nums1', h=170,
             color=lambda S, i, v: 'green' if 'set2' in S and v in S['set2'] else None),
        dict(type='array', var='nums2', label='nums2', h=170,
             color=lambda S, i, v: 'green' if 'set1' in S and v in S['set1'] else None),
        dict(type='set', var='set1', h=110),
        dict(type='set', var='set2', h=110),
    ],
    watch=['set1', 'set2'],
    captions={
        'set1 = ': '`nums1` 去重放进集合 `set1` = {sorted(set1)}，之后判断“在不在”只要 `O(1)`',
        'set2 = ': '`nums2` 去重放进集合 `set2` = {sorted(set2)}',
        'sum(x in set2': lambda S, B, ret: ('`answer = [{}, {}]`：两边都按下标数，重复值要重复计'.format(*ret) if ret is not None else '数 `nums1`：值在 `set2` 中的下标（绿色格子）共 =={}== 个，重复值每个下标都算'.format(sum(x in S['set2'] for x in S['nums1']))),
        'sum(x in set1': lambda S, B, ret: '数 `nums2`：值在 `set1` 中的下标（绿色格子）共 =={}== 个'.format(sum(x in S['set1'] for x in S['nums2'])),
    },
    cards=dict(
        one_liner='转成哈希集合，O(1) 判断每个元素在不在对方里',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['`answer1`：`nums1` 中有多少个下标，其值在 `nums2` 里出现过',
                 '`answer2`：反过来数 `nums2`',
                 '示例：`[4,3,2,3,1]` 和 `[2,2,5,2,3,6]` → `[3,4]`'],
        quote='把数组转成哈希集合，就可以 O(1) 判断元素是否在数组中了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先各建一个集合 `set1`、`set2`',
              '再遍历原数组（不是集合），每个下标命中就 +1，所以重复元素会被重复数'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '易错：要遍历原数组而不是集合，否则会漏掉重复值的下标数',
                 '`sum(布尔值 for ...)` 利用 True = 1 计数'],
    ),
)
