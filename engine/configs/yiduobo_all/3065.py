CONFIG = dict(
    num=3065, title='超过阈值的最少操作数 I', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历计数', tags=[],
    code='''
class Solution(object):
    def minOperations(self, nums, k):

        res = 0
        for v in nums:
            if v < k:
                res += 1
        
        return res
''',
    call='Solution().minOperations([2,11,10,1,3,9,12], 10)',
    expect=4,
    views=[
        dict(type='array', var='nums', h=300, label='nums（红 = 小于 k，要删）',
             color=lambda S, i, v: 'red' if v < S['k'] else 'green'),
    ],
    watch=['k', ('v', 'v', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计需要删掉的数的个数',
        'for v in nums': lambda S, B, r: ('`nums` 取完了，循环结束' if B.get('v') == S.v and S.v == S.nums[-1] and B.get('res') == S.res and S.get('v') is not None and B.get('_line') == 5 else f'依次取出 `v = {S.v}`'),
        'if v < k': '`{v} < {k}`？{"==是==，它比阈值小，必须删掉" if v < k else "否，已经够大，不用删"}',
        'res += 1': '又多一个要删的数：`res = {res}`',
        'return res': '遍历完了，一共要删 `{res}` 个',
    },
    cards=dict(
        one_liner='每次只能删最小的，所以就是数一数有几个比 k 小',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次操作可以删掉 `nums` 中的最小元素',
                 '求让所有元素都 `>= k` 的最少操作次数',
                 '示例：`[2,11,10,1,3]`，`k = 10` → `3`；本视频：`[2,11,10,1,3,9,12]` → `4`'],
        quote='每次操作只能删去数组中最小的数，而要求计算的是需要多少轮操作才能使得数组中的所有数都大于等于k，那么只需一趟遍历，统计数组中小于k的数的数目即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['每轮删最小值，小的数会被一个个删光',
              '直到剩下的都 `>= k` 为止，被删的正好是所有 `< k` 的数',
              '所以一趟遍历，遇到 `v < k` 就让 `res` 加一'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '无需排序，也不用真的删除',
                 '易错：只统计严格小于 k 的数',
                 '原文为 Python 2 风格，仅 class 写法不同，代码未改动'],
    ),
)
