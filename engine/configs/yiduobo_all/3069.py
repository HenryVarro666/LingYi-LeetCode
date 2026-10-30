CONFIG = dict(
    num=3069, title='将元素分配到两个数组中 I', difficulty='Easy', category='模拟',
    author='yiduobo', technique='按题意模拟', tags=[],
    code='''
class Solution(object):
    def resultArray(self, nums):

        arr1 = [nums[0]]
        arr2 = [nums[1]]
        for v in nums[2:]:
            if arr1[-1] > arr2[-1]:
                arr1.append(v)
            else:
                arr2.append(v)
        
        return arr1 + arr2
''',
    call='Solution().resultArray([5,4,3,8,2,9,1])',
    expect=[5, 3, 9, 1, 4, 8, 2],
    views=[
        dict(type='array', var='nums', h=170, label='nums（黄 = 当前 v）', color=lambda S, i, v: 'yellow' if S.get('v') == v and S['_line'] >= 7 else None),
        dict(type='array', var='arr1', h=170, label='arr1', color=lambda S, i, v: 'blue' if i == len(S['arr1']) - 1 else None),
        dict(type='array', var='arr2', h=170, label='arr2', color=lambda S, i, v: 'pink' if i == len(S['arr2']) - 1 else None),
    ],
    watch=[('v', 'v', 'yellow'), ('arr1[-1]', 'arr1[-1] if arr1 else None', 'blue'), ('arr2[-1]', 'arr2[-1] if arr2 else None', 'pink')],
    captions={
        'arr1 = [': '`arr1` 先放 `nums[0] = {arr1[0]}`',
        'arr2 = [': '`arr2` 先放 `nums[1] = {arr2[0]}`',
        'for v in nums[2:]': '从 `nums[2]` 往后逐个处理',
        'if arr1[-1] > arr2[-1]': '对比两个数组最后一个元素：`{arr1[-1]}` vs `{arr2[-1]}` → {"==arr1 更大，v 加入 arr1==" if arr1[-1] > arr2[-1] else "==arr2 更大，v 加入 arr2=="}',
        'arr1.append': '`{v}` 加入 `arr1` → `{arr1}`',
        'arr2.append': '`{v}` 加入 `arr2` → `{arr2}`',
        'return arr1': '两个数组首尾相连：`{arr1}` + `{arr2}` = ==`{ret}`==',
    },
    cards=dict(
        one_liner='分配方案固定，照着题目一步步模拟',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['前两个数分别放进 `arr1`、`arr2`，之后每个数放进末尾更大的那个数组',
                 '最后把 `arr2` 接在 `arr1` 后面',
                 '示例：`[5,4,3,8]` → `[5,3,4,8]`；本视频：`[5,4,3,8,2,9,1]`'],
        quote='先分别初始化arr1和arr2中的元素为nums[0]和nums[1]，接下来从nums[2]开始向后遍历，每一轮对比arr1和arr2中最后这个元素的大小并将当前元素加入到对应的数组中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['分配规则简单且固定，不需要任何技巧',
              '前两个数先定好，之后每轮只比较两个末尾',
              '末尾大的数组收下当前元素'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`arr1[-1] > arr2[-1]` 才进 `arr1`，否则进 `arr2`',
                 '遍历从 `nums[2:]` 开始，前两个数已经放好',
                 '原文为 Python 2 风格，仅 class 写法不同，代码未改动'],
    ),
)
