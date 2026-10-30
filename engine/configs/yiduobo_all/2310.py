def _digits(S):
    k = S['k']
    return [(m * k) % 10 for m in range(11)]


def _col(S, i, v):
    if i == 0:
        return 'dim'
    return 'green' if v == S['num'] % 10 else None


def _text(S):
    num, k = S['num'], S['k']
    if 'cnt' not in S:
        return f'`num = {num}`，`k = {k}`：写成 `p*10 + (cnt+1)*k`，看有没有合法的 `p`'
    c = S['cnt']
    r = num - (c + 1) * k
    return f'`cnt = {c}`：`{num} - {c + 1}×{k} = {r}`' + ('，不是 10 的倍数' if r % 10 else '，是 10 的倍数')


CONFIG = dict(
    num=2310, title='个位数字为 K 的整数之和', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='高位集中 · 枚举 cnt 0~9',
    tags=['灵神题单', '难度分 1559'],
    code='''
class Solution(object):
    def minimumNumbers(self, num, k):

        if num == 0:
            return 0
        
        for cnt in range(10):
            if num >= (cnt + 1) * k and (num - (cnt + 1) * k) % 10 == 0:
                return cnt + 1
        
        return -1
''',
    call='Solution().minimumNumbers(37, 2)',
    expect=-1,
    views=[
        dict(type='text', fn=_text, h=90, lines=2),
        dict(type='array', var=_digits, label='m × k 的个位数（下标 m = cnt + 1；绿 = 等于 num 的个位）',
             pointers={'cnt + 1': 'blue'}, pointer_labels={'cnt + 1': 'cnt+1'}, color=_col, h=200),
    ],
    watch=[('num', 'num', 'blue'), ('k', 'k', 'pink'), ('cnt', 'cnt', 'orange')],
    captions={
        'if num == 0': '`num = 0`：0 个数的和就是 0 → 答案 0',
        'for cnt': lambda S, B, r: ('`cnt` 已经枚举到 9，循环结束' if B.get('cnt') == S.cnt else f'枚举单独的 `k` 的个数 `cnt`，只需 0 到 9 → `cnt = {S.cnt}`'),
        'if num >= (cnt + 1)': lambda S, B, r: (
            f'总共 `{S.cnt + 1}` 个数，个位部分 `{(S.cnt + 1) * S.k}`；剩下 `{S.num - (S.cnt + 1) * S.k}`'
            + (' 是 10 的倍数 → 找到合法的 `p`，答案 `cnt + 1`' if S.num >= (S.cnt + 1) * S.k and (S.num - (S.cnt + 1) * S.k) % 10 == 0
               else ('，是负数，放不下' if S.num < (S.cnt + 1) * S.k else '，不是 10 的倍数，凑不出 `p*10` → 下一个 `cnt`'))),
        'return -1': '`cnt` 0 到 9 都试过了：==个位永远对不上== → 返回 `-1`',
    },
    cards=dict(
        one_liner='高位集中到一个数里，只枚举 cnt 从 0 到 9',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['多重集每个正整数的个位都是 `k`，总和为 `num`',
                 '求最小的元素个数，没有则 `-1`',
                 '本视频：`num = 37, k = 2` → `-1`'],
        quote='可以将所有高位上的数都集中到一个数中。如果问题有解的话，就一定可以写成(p * 10 + k) + k + k + ... + k的形式。',
        quote_src='—— yiduobo 题解原文',
        idea=['先特判 `num = 0`：0 个数，答案 0',
              '有解时一定是 `(p·10 + k) + cnt 个 k = p·10 + (cnt+1)·k`',
              '`cnt ≥ 10` 时 10 个 `k` 可并入 `p·10`，所以只枚举 `cnt = 0..9`，找到第一个合法的就是答案'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '原文为 Python 2 写法，本题代码无需改动，Python 3 直接可运行',
                 '合法条件：`num ≥ (cnt+1)·k` 且差值是 10 的倍数',
                 '对比灵神：灵神从「枚举个数 n」出发再证明只需到 10；这里直接用「高位集中」得到上限 10'],
    ),
)
