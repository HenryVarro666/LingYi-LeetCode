CONFIG = dict(
    num=1389, title='按既定顺序创建目标数组', difficulty='Easy', category='模拟',
    author='yiduobo', technique='模拟 · 按下标插入',
    code='''
class Solution(object):
    def createTargetArray(self, nums, index):

        res = []
        n = len(nums)
        for i in range(n):
            if i == index[i]:
                res.append(nums[i])
            else:
                res = res[:index[i]] + [nums[i]] + res[index[i]:]
        
        return res
''',
    call='Solution().createTargetArray([0,1,2,3,4], [0,1,2,2,1])',
    expect=[0,4,1,3,2],
    views=[
        dict(type='array', var='nums', label='nums', h=120, pointers={'i': 'blue'}),
        dict(type='array', var='index', label='index', h=120, pointers={'i': 'blue'}),
        dict(type='array', var='res', label='res（目标数组）', h=140, color=lambda S, i, v: 'green' if 'i' in S and 'index' in S and i == S['index'][S['i']] else None),
    ],
    watch=['i', ('nums[i]', "nums[i] if 'i' in S else ''", 'blue'), ('index[i]', "index[i] if 'i' in S else ''", 'pink')],
    captions={
        'res = []': '目标数组一开始是空的',
        'for i in range': lambda S, B, r: (f'依次处理第 `{S.i}` 个数' if not ('i' in B and B['i'] == S.i) else '5 个数都插完了'),
        'if i == index[i]': lambda S, B, r: (f'`index[{S.i}] = {S.index[S.i]}` 等于当前长度 `{S.i}` → 插到末尾就行' if S.i == S.index[S.i] else f'`index[{S.i}] = {S.index[S.i]}` ≠ 当前长度 `{S.i}` → 要插到中间，后面的数后移'),
        'res.append': '末尾追加 `{nums[i]}` → `{res}`',
        'res = res[:': '在位置 `{index[i]}` 插入 `{nums[i]}`：前半 + `[{nums[i]}]` + 后半 → `{res}`',
        'return res': '全部插完，目标数组 `{res}`',
    },
    cards=dict(
        one_liner='按 index 一个个把 nums 插进目标数组',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`target` 初始为空，依次把 `nums[i]` 插入到位置 `index[i]`',
                 '后面的元素向右移动，返回最终数组',
                 '示例：`nums=[0,1,2,3,4]`，`index=[0,1,2,2,1]` → `[0,4,1,3,2]`'],
        quote='正经做法应该是使用平衡二叉树……不过题目数组的规模很小，我在这里直接使用的朴素算法。',
        quote_src='—— yiduobo 题解原文',
        idea=['数组规模很小，直接模拟即可',
              '`index[i]` 刚好等于当前长度，就是追加',
              '否则用切片拼接：`res[:k] + [x] + res[k:]`'],
        summary=['时间 `O(n^2)`：每次切片拼接是 `O(n)`',
                 '正经做法：平衡树（按下标作 key）可做到 `O(n log n)`',
                 '题目保证 `index[i] <= i`，所以插入位置总是合法',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
