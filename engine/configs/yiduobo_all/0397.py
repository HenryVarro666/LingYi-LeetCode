CONFIG = dict(
    num=397, title='整数替换', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='看二进制末尾 · 11 结尾就加 1',
    tags=['灵神题单·动态规划', '灵神题单·贪心与思维'],
    code='''
class Solution(object):
    def integerReplacement(self, n):

        res = 0

        while n != 1:
            while n % 2 == 0:
                res += 1
                n //= 2
            if n == 1:
                break
                
            if n % 4 == 3 and n != 3:
                n += 1
            else:
                n -= 1
            res += 1

        return res
''',
    call='Solution().integerReplacement(11)',
    expect=5,
    views=[
        dict(type='text', h=80, fn=lambda S: (f"`n = {S['n']}`，二进制 ==`{bin(S['n'])[2:]}`==，已用 `{S['res']}` 步" if 'res' in S else '')),
        dict(type='string', var='bin(n)[2:]', label='n 的二进制（从高位到低位）', h=200),
        dict(type='text', h=110, fn=lambda S: (
            '偶数：末位是 0，只能除以 2（右移一位）' if 'res' in S and S['n'] % 2 == 0 and S['n'] != 0 else
            ('`n = 3`（`11`）：特例，减 1 更短' if 'res' in S and S['n'] == 3 else
             ('奇数且以 `11` 结尾：加 1 让进位吃掉一串 1' if 'res' in S and S['n'] % 4 == 3 else
              ('奇数且以 `01` 结尾：减 1 后只剩一个 0 可除' if 'res' in S else ''))))),
    ],
    watch=[('n', 'n', 'blue'), ('res', 'res', 'green'), ('n % 4', 'n % 4', 'orange')],
    captions={
        'res = 0': '`res` 记操作次数',
        'while n != 1': lambda S, B, r: (f'`n = {S.n}`，不是 1 → 继续' if S.n != 1 else '`n = 1`，到了 → 结束'),
        'while n % 2 == 0': lambda S, B, r: (f'`{S.n}` 是偶数（二进制末位 0）→ 只能除以 2' if S.n % 2 == 0
                                             else '`n = 1`，不用再除了' if S.n == 1 else f'`{S.n}` 是奇数（二进制末位 1）→ 要决定加 1 还是减 1'),
        'res += 1': lambda S, B, r: (f'除以 2 也算一次操作：`res` → =={S.res}==' if S['_line'] == 8 else f'加 / 减 1 算一次操作：`res` → =={S.res}=='),
        'n //= 2': '除以 2：`n` 变成 `{n}`（二进制去掉末位 0）',
        'if n == 1': lambda S, B, r: ('`n == 1` → 已经变成 1，提前结束' if S.n == 1 else f'`n = {S.n}` 还不是 1，是奇数，继续判断'),
        'if n % 4 == 3': lambda S, B, r: (
            f'`{S.n} % 4 = {S.n % 4}`，且 `n != 3` → 末尾是 ==11==，加 1 能让一串 1 连锁进位，省步数' if S.n % 4 == 3 and S.n != 3 else
            ('`n = 3` 是特例：加 1 要 3 步（4,2,1），减 1 只要 2 步（2,1）→ 走减 1' if S.n == 3 else
             f'`{S.n} % 4 = {S.n % 4}`，末尾是 ==01== → 减 1 最划算')),
        'n += 1': '加 1：`n` → `{n}`（二进制末尾的连续 1 变成 0，进位）',
        'n -= 1': '减 1：`n` → `{n}`（末位 1 变 0）',
        'return res': '最少操作 =={ret}== 次',
    },
    cards=dict(
        one_liner='看二进制末尾：01 就减 1，11 就加 1（3 除外）',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['正整数 `n`：偶数除以 2；奇数可以 `+1` 或 `-1`',
                 '求把 `n` 变成 `1` 的最少操作次数',
                 '示例：`n = 11` → `5`（11→12→6→3→2→1）'],
        quote='若其为奇数，那么一定可以写成XXXX11...111这种形式。设n的末尾有k个1……',
        quote_src='—— yiduobo 题解原文',
        idea=['三种操作都是位操作：除以 2 去掉末位 0，加减 1 改变末尾',
              '`k = 1`（以 01 结尾）：减 1 最优；`k > 1`（以 11 结尾）：加 1，进位后整串 1 变成 0',
              '特例 `3`：减 1 更短（2 步）。其余按「`n % 4 == 3` 且 `n != 3` → 加 1」'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错点：`n = 3` 要减 1；`n = 2^31 - 1` 加 1 在别的语言会溢出，Python 没有此问题',
                 '原文为 Python 2 写法，`n /= 2` 已改为 `n //= 2`',
                 '同类题：位运算找规律、BFS / 记忆化搜索也可做'],
    ),
)
