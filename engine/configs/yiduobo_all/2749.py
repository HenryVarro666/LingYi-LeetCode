def _t1(S):
    if 'k' not in S or 'num1' not in S:
        return ''
    if 'v' not in S:
        return f'k = =={S["k"]}==：假设做 k 次操作'
    return f'v = num1 − k×num2 = {S["num1"]} − {S["k"]}×{S["num2"]} = =={S["v"]}==（二进制 `{S["v"]:b}`）'


def _t2(S):
    if 't' not in S or S.get('_line', 0) < 7:
        return ''
    return f'v 的二进制有 `t = {S["t"]}` 个 1 → p 数组至少 {S["t"]} 项；最多 `{S["v"]}` 项（全是 2^0）'


def _t3(S):
    if 't' not in S or S.get('_line', 0) < 8:
        return ''
    t, k, v = S['t'], S['k'], S['v']
    ok = t <= k <= v
    return f'`{t} ≤ {k} ≤ {v}` ' + ('成立 → ==存在构造方案==' if ok else '不成立 → 换下一个 k')


CONFIG = dict(
    num=2749, title='得到整数零需要执行的最少操作数', difficulty='Medium', category='位运算',
    author='yiduobo', technique='枚举 k · 二进制 1 的个数',
    tags=['位运算', '贪心与思维', '难度分 2132'],
    code='''
class Solution(object):
    def makeTheIntegerZero(self, num1, num2):

        k = 1
        while num1 - num2 * k > 0:
            v = num1 - num2 * k
            t = sum([int(x) for x in list(bin(v)[2:])])
            if t <= k <= v:
                return k
            k += 1
        
        return -1
''',
    call='Solution().makeTheIntegerZero(9, 3)',
    expect=2,
    views=[
        dict(type='text', fn=_t1, size=28, h=70),
        dict(type='text', fn=_t2, size=28, h=70),
        dict(type='text', fn=_t3, size=28, h=70),
    ],
    watch=['num1', 'num2', 'k', 'v', ('t', 't', 'cyan')],
    captions={
        'k = 1': '从 `k = 1` 开始向上枚举：这个最小的 k 不会太大',
        'while num1': lambda S, B, r: (f'`num1 − num2×k = {S.num1 - S.num2 * S.k}` > 0，还有构造的可能' if S.num1 - S.num2 * S.k > 0
                                       else f'`num1 − num2×k = {S.num1 - S.num2 * S.k}` ≤ 0：k 再大只会更小，无解 → 跳出循环'),
        'v = num1': '`v = {num1} − {k}×{num2} = {v}`：要用恰好 k 个 2 的幂凑出 v',
        't = sum': '`bin({v}) = {bin(v)}`，1 的个数 `t = {t}`：p 数组至少 t 项',
        'if t <= k <= v': lambda S, B, r: (f'`{S.t} ≤ {S.k} ≤ {S.v}` 成立：k 项在 [t, v] 内，可由拆分 2^m 得到 → 就是最小的 k' if S.t <= S.k <= S.v
                                           else (f'`k = {S.k} < t = {S.t}`：项数不够，二进制的 1 一个都合不了 → 试下一个 k' if S.k < S.t
                                                 else f'`k = {S.k} > v = {S.v}`：就算全拆成 1 也凑不出这么多项')),
        'return k': '找到了，最少操作数 `k = {k}`',
        'k += 1': '`k` 增加到 `{k}`，再试一次',
        'return -1': '`v ≤ 0` 之后不可能再变大：返回 `-1`',
    },
    cards=dict(
        one_liner='把 k×num2 移到左边：v 要拆成恰好 k 个 2 的幂',
        complexity='时间 `O(log)`（k 很小），空间 `O(1)`',
        problem=['每次选 `p`，`num1 -= 2^p + num2`，求变成 0 的最少次数',
                 '等价于 `num1 = k×num2 + 2^p[0] + … + 2^p[k-1]`',
                 '本视频：`num1=9, num2=3` → `2`'],
        quote='若v二进制表示中1的数量有t个，那么p数组的长度就至少要等于t，也就是说这里的k必须要大于等于t。',
        quote_src='—— yiduobo 题解原文',
        idea=['记 `v = num1 − k×num2`，v 必须是 2 的若干次幂之和',
              'v 的 1 的个数 t 是最少项数，v 本身（全拆成 1）是最多项数',
              '每次把最高项拆成两个低一次的项，项数 +1，所以 t..v 之间都能构造'],
        summary=['时间 `O(log)`，空间 `O(1)`',
                 '`v ≤ 0` 时直接 -1：k 增大 v 不会再变正（num2 ≥ 0 的情形）',
                 '易错：条件是 `t ≤ k ≤ v`，两边都要判',
                 '`bin(v)[2:]` 去掉前缀 `0b` 后数 1，等价于 popcount',
                 '对比灵神：灵神 `k > x` 返回 -1 在循环内；这里把 `v > 0` 写进 while 条件'],
    ),
)
