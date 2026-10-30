CONFIG = dict(
    num=3038, title='相同分数的最大操作数目 I', difficulty='Easy', category='模拟',
    author='yiduobo', technique='步长 2 遍历检测',
    tags=[],
    code='''
class Solution(object):
    def maxOperations(self, nums):

        v = nums[0] + nums[1]
        res = 1
        for index in range(2, len(nums), 2):
            if index + 1 == len(nums) or nums[index] + nums[index + 1] != v:
                break
            res += 1
        
        return res
''',
    call='Solution().maxOperations([3,2,1,4,5,1])',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: (f"目标分数 `v = {S['v']}`，已完成 `{S['res']}` 次" if 'res' in S else '先算前两个数之和，再每隔两格检查一对'), size=28),
        dict(type='array', var='nums', label='nums（蓝 = 当前检测的一对）', cell=96,
             pointers={'index': 'blue', 'index + 1': 'pink'},
             color=lambda S, k, v: ('blue' if ('index' in S and k in (S['index'], S['index'] + 1)) else 'green' if (k < 2 and 'v' in S) else None)),
    ],
    watch=[('v', 'v', 'green'), ('index', 'index', 'blue'), ('res', 'res', 'pink')],
    captions={
        'v = nums': '操作只能碰剩余数组的前两个元素，所以先算出第一对之和 `v = {v}`',
        'res = 1': '第一对肯定可以做，`res = 1`',
        'for index in range': '从下标 2 开始，步长 2，`index = {index}`：检测 `nums[{index}]` 和下一个元素',
        'if index + 1 == len': lambda S, B, ret: (
            f"`index + 1 = {S.index+1}` 已经越界，只剩一个元素 → ==凑不成一对，break==" if S.index + 1 == len(S.nums) else
            (f"`{S.nums[S.index]} + {S.nums[S.index+1]} = {S.nums[S.index]+S.nums[S.index+1]}` ≠ `v = {S.v}` → ==分数不同，break=="
             if S.nums[S.index] + S.nums[S.index+1] != S.v else
             f"`{S.nums[S.index]} + {S.nums[S.index+1]} = {S.v}` == `v` → 这对合法")),
        'res += 1': '这一对和等于 `v`，多做一次操作：`res = {res}`',
        'return res': '返回最多的操作次数 =={ret}==',
    },
    cards=dict(
        one_liner='先算前两个数之和 v，再以步长 2 往后逐对比较',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次删数组最前面两个数，分数 = 两数之和',
                 '==所有操作分数必须相同==，求最多操作次数',
                 '示例：`[3,2,6,1,4]` → `1`'],
        quote='由于题目中的操作只能针对剩余数组的前两个元素进行，因此在这里只需先计算出数组中前两个元素之和v，然后从下标2开始以步长2向后遍历，每次检测当前元素与下一个元素之和是否等于v即可。',
        quote_src='—— yiduobo 题解',
        idea=['操作只能碰前两个，等于把数组切成一对一对',
              '第一对决定 `v`，所以 `res` 从 1 开始',
              '后面每对要么等于 `v` 继续，要么不等或只剩一个就停'],
        result='`5 + 1 = 6 ≠ 5` 停下，`res = 2` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`index + 1` 可能越界，要先判断再取 `nums[index + 1]`（靠 `or` 短路）',
                 '数组至少两个元素，所以 `res` 初值取 1 是安全的'],
    ),
)
