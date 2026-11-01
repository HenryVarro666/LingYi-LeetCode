CONFIG = dict(
    num=2089, title='找出数组排序后的目标下标', difficulty='Easy', category='二分算法',
    author='yiduobo', technique='排序后一趟遍历', tags=[],
    code='''
class Solution(object):
    def targetIndices(self, nums, target):

        res = []
        for index, num in enumerate(sorted(nums)):
            if num == target:
                res.append(index)
        
        return res
''',
    call='Solution().targetIndices([1,2,5,2,3], 2)',
    expect=[1, 2],
    views=[
        dict(type='array', var=lambda S: sorted(S['nums']), label='sorted(nums)（蓝箭头 = index）', cell=96, h=260,
             pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if i in S.get('res', []) else None),
        dict(type='array', var=lambda S: S.get('res'), label='res（目标下标）', cell=70, h=150),
    ],
    watch=[('index', 'index', 'blue'), ('num', 'num'), ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 用来收集目标下标',
        'for index, num': '排序后第 `{index}` 个数是 `{num}`',
        'if num == target': '`{num} == {target}` → {"==是目标，记录下标=="  if num == target else "不是目标，跳过"}',
        'res.append': '把下标 `{index}` 加入 `res` → `{res}`',
        'return res': '遍历完，目标下标为 ==`{ret}`==',
    },
    cards=dict(
        one_liner='先排序，再一趟遍历把等于 target 的下标收集起来',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`nums` 非递减排序后，找出所有等于 `target` 的下标',
                 '示例：`[1,2,5,2,3]`，`target = 2` → `[1,2]`',
                 '没有目标就返回空列表'],
        quote='比较基础的题目。按题目要求将数组排序，然后一趟遍历找到所有等于target的下标即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`sorted(nums)` 得到排序后的数组，下标按递增顺序遍历',
              '遇到等于 `target` 的位置就把 `index` 加进 `res`',
              '`res` 天然是递增的，符合题目要求'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错点：要对排序后的数组取下标，不是原数组',
                 '用 `sorted(nums)` 不改动原数组',
                 '灵神的计数写法可以做到 `O(n)`'],
    ),
)
