CONFIG = dict(
    num=3790, title='最小全 1 倍数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='先排除 2、5 的倍数，再累加 10^i 的余数',
    tags=['数学算法', '链表、二叉树与回溯', '难度分 1015'],
    code='''
class Solution(object):
    def minAllOneMultiple(self, k):
        
        if k % 2 == 0 or k % 5 == 0:
            return -1
        
        r = 1
        s = 1
        res = 1
        while s != 0:
            r = r * 10 % k
            s = (s + r) % k
            res += 1
        
        return res
''',
    call='Solution().minAllOneMultiple(7)',
    expect=6,
    views=[
        dict(type='text', fn=lambda S: (f"全 1 数共 =={S['res']}== 位：`{'1' * S['res']}`，模 {S['k']} 的余数 `s` = =={S['s']}==；`r` = 10^{S['res'] - 1} % {S['k']} = {S['r']}" if 's' in S else ''), h=100),
        dict(type='text', fn=lambda S: ('' if 's' not in S else ('`s = 0` → 整除，退出循环' if S['s'] == 0 else '`s != 0` → 还没整除，继续加一位')), h=70),
    ],
    watch=['k', ('r', 'r', 'cyan'), ('s', 's', 'yellow'), ('res', 'res', 'blue')],
    captions={
        'k % 2 == 0': lambda S, B, r: (f'`k = {S.k}` 是 2 或 5 的倍数 → 全 1 数个位是 1，不可能整除 → 返回 -1' if S.k % 2 == 0 or S.k % 5 == 0
                                       else f'`{S.k}` 不是 2 或 5 的倍数 → ==必有解==，且余数重复前一定先碰到 0，不需要判重'),
        'r = 1': '`r` 记录 `10^i % k`，现在 `i = 0`：`r = 1`',
        'res = 1': '`res` 是当前位数：1 位',
        's = 1': '`s` 记录全 1 数 `N` 模 k 的余数，一位的 `1` 余数是 `1`',
        'while s != 0': lambda S, B, r: ('`s = 0` → 找到了' if S.s == 0 else f'`s = {S.s} != 0` → 继续加一位'),
        'r = r * 10': '`10^i % k` 乘 10：`{B.r} * 10 % {k}` = =={r}==',
        's = (s + r)': '加一位：`N = N + 10^i`，余数 `({B.s} + {r}) % {k}` = =={s}==',
        'res += 1': '位数加一：`res = {res}`',
        'return res': '`s = 0`：返回位数 =={res}==',
    },
    cards=dict(
        one_liner='余数最多 k 种；不是 2、5 的倍数时，重复前必先碰到 0',
        complexity='时间 `O(k)`，空间 `O(1)`',
        problem=['给定正整数 `k`，找最小的、十进制表示全是 `1` 的整数 `n`，使 `n` 能被 `k` 整除',
                 '返回 `n` 的位数；不存在则返回 `-1`',
                 '示例：`k=3` → `3`；`k=7` → `6`；`k=2` → `-1`'],
        quote='若k不是2或者5的倍数，就可以直接暴力计算，在余数出现重复时必然先找出合法的答案，即暴力计算的次数不超过k次。',
        quote_src='—— yiduobo 题解原文',
        idea=['`k` 是 2 的倍数要偶数，是 5 的倍数要以 0 或 5 结尾，全 1 数都不行 → 直接 -1',
              '若两个全 1 数余数相同，作差得 `11..100..0`；`k` 与 10 互质时可约去 0 → 更短的全 1 数已整除',
              '所以直接暴力累加，最多 k 步就会碰到 0，不用 set 记余数'],
        summary=['时间 `O(k)`，空间 `O(1)`',
                 '`r` 是 `10^i % k`，`s` 是全 1 数 % k：每轮先更新 `r` 再加到 `s`',
                 '易错点：`k` 是 2 或 5 的倍数必须先返回 -1，否则 `while` 会死循环',
                 '本题与 1015 完全相同'],
    ),
)
