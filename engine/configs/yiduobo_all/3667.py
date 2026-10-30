CONFIG = dict(
    num=3667, title='按绝对值排序数组', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='sorted + key=abs',
    tags=[],
    code='''
class Solution(object):
    def sortByAbsoluteValue(self, nums):
        
        return sorted(nums, key=lambda d:abs(d))
''',
    call='Solution().sortByAbsoluteValue([-7, 3, -1, 5, -4, 2, 0])',
    expect=[0, -1, 2, 3, -4, 5, -7],
    views=[
        dict(type='array', var='nums', label='nums（原数组）', cell=90, h=170),
        dict(type='text', h=110, size=32,
             fn=lambda S: '排序的键：`abs(d)` = ==' + ', '.join(str(abs(x)) for x in S['nums']) + '=='),
        dict(type='text', h=110, size=32,
             fn=lambda S: '按键从小到大：==' + ', '.join(str(x) for x in sorted(S['nums'], key=abs)) + '=='),
    ],
    watch=['nums'],
    captions={
        'return sorted': '`sorted` 用 `abs(d)` 作排序键，不改 `nums` 本身：键依次是 `{[abs(x) for x in nums]}`，结果 ==`{ret}`==（键相同的保持原顺序，排序稳定）',
    },
    cards=dict(
        one_liner='一行 sorted，排序的键换成绝对值',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给整数数组 `nums`，按 ==绝对值== 非递减排序后返回',
                 '本视频：`[-7,3,-1,5,-4,2,0]` → `[0,-1,2,3,-4,5,-7]`'],
        quote='按照题目要求，直接调用sort，并使用lambda表达式来排就行了，比较条件为abs(x)。',
        quote_src='—— yiduobo 题解原文',
        idea=['`sorted(nums, key=...)` 比较的是键，不是元素本身',
              '键取 `abs(d)`：`-4` 和 `4` 在排序时等价',
              '`sorted` 是稳定排序，绝对值相同的保持原来的先后'],
        after=[dict(heading='逐步看 sorted 做了什么', lines=['先对每个元素算键 `abs(d)`：`[7,3,1,5,4,2,0]`', '再按键从小到大排列元素：`0,-1,2,3,-4,5,-7`', '`-4` 和 `4` 键相同，谁在前取决于原数组顺序（稳定排序）', '整个过程不改原数组，只返回新列表'])],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`sorted` 返回新列表；`nums.sort(key=abs)` 才是原地排序',
                 '`key=lambda d:abs(d)` 可以直接简写成 `key=abs`',
                 '绝对值相同的数，顺序由原数组决定（题目没要求特殊处理）'],
    ),
)
