CONFIG = dict(
    num=3190, title='使所有元素都可以被 3 整除的最少操作数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='遍历计数',
    tags=[],
    code='''
class Solution(object):
    def minimumOperations(self, nums):

        res = 0
        for v in nums:
            if v % 3 != 0:
                res += 1
        
        return res
''',
    call='Solution().minimumOperations([1,2,3,4,6,8])',
    expect=4,
    views=[
        dict(type='array', var='nums', h=260, label='nums',
             color=lambda S, i, v: 'green' if v % 3 == 0 else 'orange'),
        dict(type='text', fn=lambda S: (f"当前 `v = {S['v']}`，`{S['v']} % 3 = {S['v'] % 3}`" if 'v' in S else ''), size=30, h=110),
    ],
    watch=[('v', 'v', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录需要操作的元素个数，从 0 开始',
        'for v in nums': lambda S, B, r: ('`nums` 里的数都看完了，退出循环' if 'v' in B and B['v'] == S['v'] else f'取出下一个数 `v = {S.v}`'),
        'if v % 3 != 0': lambda S, B, r: (f'`{S.v} % 3 = {S.v % 3}` ≠ 0：模 3 余 {S.v % 3}，加一或减一都只要 ==一次操作==' if S.v % 3
                                          else f'`{S.v} % 3 = 0`：已经是 3 的倍数，不用操作'),
        'res += 1': '这个数要操作一次：`res` → {res}',
        'return res': '遍历完，一共 `{res}` 个数需要操作',
    },
    cards=dict(
        one_liner='是 3 的倍数不用动，否则恰好操作一次',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次操作把某个元素加 1 或减 1',
                 '求让数组所有元素都是 `3` 的倍数的最少操作次数',
                 '示例：`[1,2,3,4]` → `3`；本视频：`[1,2,3,4,6,8]` → `4`'],
        quote='对于模3余1这种情况，将这个数减去1就行了，而对于模3余2这种情况，则只需要将这个数加上1。',
        quote_src='—— yiduobo 题解原文',
        idea=['整数只有三种：3 的倍数、模 3 余 1、模 3 余 2',
              '余 1 就减 1，余 2 就加 1，==各需一次==',
              '遍历 `nums`，不是 3 的倍数就让答案加 1'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '判断条件写 `v % 3 != 0`，别漏掉 0 的情况',
                 '原文代码本身就是 Python 3 可运行，未做修改',
                 '对比灵神：灵神一行 `sum(x % 3 != 0 for x in nums)`，yiduobo 用显式循环计数'],
    ),
)
