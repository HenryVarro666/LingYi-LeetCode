def _fn(S):
    if 'res' not in S:
        return ''
    return f"当前检查 `res` = =={S['res']}==（`{format(S['res'], 'b')}`）　{'在集合里 → 还能拼出，继续翻倍' if S['res'] in S['num_set'] else '不在集合里 → 它就是答案'}"


CONFIG = dict(
    num=2568, title='最小无法得到的或值', difficulty='Medium', category='位运算',
    author='yiduobo', technique='集合 + 逐个检查 2 的幂次',
    tags=['灵神题单·位运算', '灵神题单·贪心与思维', '难度分 1754'],
    code='''
class Solution(object):
    def minImpossibleOR(self, nums):

        num_set = set(nums)
        res = 1
        while res in num_set:
            res <<= 1
        
        return res
''',
    call='Solution().minImpossibleOR([2,1,7,4,3])',
    expect=8,
    views=[
        dict(type='text', fn=_fn, size=30, h=90),
        dict(type='set', var='num_set', fmt=lambda x: str(x), h=300),
    ],
    watch=[('res', "S.get('res')", 'green')],
    captions={
        'num_set = set(nums)': '数组放进集合，方便 `O(1)` 判断某个数在不在',
        'res = 1': '从最小的 2 的幂次 `1` 开始检查',
        'while res in num_set': lambda S, B, r: (f'`{S.res}` 在数组里：它能被表示，而且 ==2 的幂次齐了== 就能或出更小的所有数 → 继续看 `{S.res * 2}`' if S.res in S.num_set
                                                  else f'`{S.res}` 不在数组里：或运算不会产生新的最高位，==永远拼不出== → 停下'),
        'res <<= 1': '翻倍，检查下一个 2 的幂次：`res` = {res}',
        'return res': '最小不可表达的值是 =={res}==',
    },
    cards=dict(
        one_liner='或运算不进位：缺的第一个 2 的幂次就是答案',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组 `nums` 的任意子序列做 OR，能得到的数叫可表达的',
                 '求最小的不可表达的 ==正整数==',
                 '示例：`[2,1]` → `4`'],
        quote='或运算是无法产生进位的，因此可以从2的幂次出发来考虑问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['假设 `1..k` 都能表示，看 `k+1`',
              '若 `k+1` 是 2 的幂：它不能由更小的数 OR 出来，必须在数组里',
              '若不是：设 `2^p` 为最高位，它在数组里，剩下的部分更小，也能表示 → 两者 OR 得到'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '只需检查 2 的幂次，`res` 每次翻倍，最多约 31 次',
                 '对比灵神：灵神用 `mask` 记录加 lowbit，空间 `O(1)`；这里用集合更直观',
                 '`res` 初值是 1，不是 0（题目要最小的非零数）'],
    ),
)
