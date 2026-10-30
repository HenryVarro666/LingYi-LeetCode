CONFIG = dict(
    num=1009, title='十进制整数的反码', difficulty='Easy', category='位运算',
    author='yiduobo', technique='2 的幂减 1 减 N',
    tags=['位运算', '基础题'],
    code='''
class Solution(object):
    def bitwiseComplement(self, N):

        pow2 = 2
        while pow2 <= N:
            pow2 <<= 1
        
        return pow2 - N - 1
''',
    call='Solution().bitwiseComplement(10)',
    expect=5,
    views=[
        dict(type='array', var=lambda S: [2, 4, 8, 16, 32, 64], label='pow2 依次翻倍',
             color=lambda S, i, v: 'blue' if v == S.get('pow2') else None, h=200),
        dict(type='text', fn=lambda S: f"`pow2 = {S['pow2']}`，`N = {S['N']}`：" + ("`pow2 <= N` → 还要左移" if S['pow2'] <= S['N'] else "`pow2 > N` → 停下，pow2 = 100…0"), size=30),
    ],
    watch=['N', ('pow2', 'pow2', 'blue')],
    captions={
        'pow2 = 2': '`pow2` 从 2 开始（N = 0 时也能得到 1），找第一个大于 N 的 2 的幂',
        'while pow2 <= N': lambda S, B, r: (f'`{S.pow2} <= {S.N}` → 还不够大，继续' if S.pow2 <= S.N else f'`{S.pow2} > {S.N}` → 够了，`pow2 = 100…0`，0 的个数 = N 的位数'),
        'pow2 <<= 1': '左移一位：`pow2` = {pow2}',
        'return': '全 1 = `pow2 - 1` = {pow2 - 1}，反码 = 全 1 减 N = `{pow2} - {N} - 1` = =={ret}==',
    },
    cards=dict(
        one_liner='反码 = 11…1 减去 N，而 11…1 = 100…0 - 1',
        complexity='时间 `O(log N)`，空间 `O(1)`',
        problem=['把 `N` 的二进制每位取反，求十进制结果',
                 '示例：`10 = 1010` → `0101` = `5`'],
        quote='设N的二进制表示有K位，那么答案应该是11...1 - N(2)，其中一共有K个1，而11...1又等于100...0 - 1。',
        quote_src='—— yiduobo 题解原文',
        idea=['K 位全 1 减去 N，每位都不会借位，恰好等于逐位取反',
              '全 1 = `2^K - 1`，先求 `pow2 = 2^K`',
              '答案就是 `pow2 - N - 1`'],
        summary=['时间 `O(log N)`，空间 `O(1)`',
                 '`pow2` 从 2 开始：`N = 0` 时得到 `2 - 0 - 1 = 1`，正好符合题意',
                 '同类题：476 数字的补数（那里 pow2 从 1 开始）',
                 '原文本身可在 Python 3 运行，没有改动'],
    ),
)
