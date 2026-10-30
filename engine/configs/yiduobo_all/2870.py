CONFIG = dict(
    num=2870, title='使数组为空的最少操作次数', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='频次统计 + 模 3 讨论',
    tags=['灵神题单', '难度分 1392'],
    code='''
class Solution(object):
    def minOperations(self, nums):

        freq = {}
        for v in nums:
            freq[v] = freq.get(v, 0) + 1
        
        res = 0
        for v in freq:
            if freq[v] == 1:
                return -1
            else:
                res += freq[v] //3
                if freq[v] % 3 != 0:
                    res += 1
        
        return res
''',
    call='Solution().minOperations([2,3,3,2,2,4,2,3,4])',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums', h=190,
             color=lambda S, i, v: 'yellow' if 'v' in S and 'res' not in S and v == S['v'] else None),
        dict(type='map', var='freq', label='freq：每个数的出现次数 k', fmt=lambda k, v: f'{k}: {v}', h=250),
        dict(type='text', h=110, size=30, fn=lambda S: f"k = {S['freq'][S['v']]}：`k // 3` = {S['freq'][S['v']]//3}，k % 3 = {S['freq'][S['v']]%3}" if 'res' in S and S.get('v') in S['freq'] else ''),
    ],
    watch=['v', ('res', 'res', 'green')],
    captions={
        'freq[v] = freq.get': '数字 `{v}` 的次数 +1 → `{freq[v]}`',
        'for v in nums': '扫描数字 `{v}`',
        'if freq[v] == 1': lambda S, B, r: ('只出现 1 次，删 2 或删 3 都凑不出 → 返回 -1' if S.freq[S.v] == 1 else f'`k = {S.freq[S.v]}`，不是 1，有办法删完'),
        'res += freq[v]': '尽量多删 3：`k // 3 = {freq[v] // 3}` 次 → `res = {res}`',
        'if freq[v] % 3': lambda S, B, r: (f'`{S.freq[S.v]} % 3 = {S.freq[S.v] % 3}`，剩余部分还要 1 次（余 1 时少删一次 3，凑 4 = 2+2，也是 +1）'
                                           if S.freq[S.v] % 3 != 0 else '整除，全用删 3，不需要额外操作'),
        'res += 1': '额外 +1 次 → `res = {res}`',
        'return res': '所有数字都删完，最少 `{res}` 次操作',
    },
    cards=dict(
        one_liner='尽量执行删 3，余数再补一次',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次可删除 2 个或 3 个==相等==的元素，求清空数组的最少操作次数，不行返回 `-1`',
                 '示例：`[2,3,3,2,2,4,2,3,4]` → `4`'],
        quote='为了使得操作次数最少，那么就应该尽量执行删3操作，在这里就需要对k模3的结果进行讨论。',
        quote_src='—— yiduobo 题解原文',
        idea=['不同数字分开考虑，一趟遍历统计出现次数 `k`',
              '`k` 模 3 余 0：`k/3` 次；余 2：多一次删 2',
              '余 1（`k > 1`）：拿一个 3 配上 1 得 4，做两次删 2，次数 = `k/3 + 1`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`，并删去类型说明',
                 '易错：`k = 1` 必须先返回 -1',
                 '与 2244 题完全相同'],
    ),
)
