import math


def _txt(S):
    if 'state' not in S:
        return '`f[state]`：state 的第 k 位为 1，表示数字 `k+1` 已被放进前 `p` 个位置'
    st, n = S['state'], S['n']
    bits = f'{st:0{n}b}'
    p = S.get('p')
    s = f'`state = {bits}`（已放数字 {[k + 1 for k in range(n) if st >> k & 1]}）'
    if p is not None:
        s += f'，共 `p = {p}` 个 → 填第 ==p== 个位置'
    return s


CONFIG = dict(
    num=2992, title='自整除排列的数量', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='状态压缩 DP · 数字填位置',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def selfDivisiblePermutationCount(self, n):

        max_state = 1 << n
        f = [0] * max_state
        f[0] = 1

        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        for state in range(1, max_state):
            p = 0
            for index in range(n):
                if state & (1 << index) == (1 << index):
                    p += 1
            
            for index in range(n):
                if state & (1 << index) == (1 << index) and gcd(index + 1, p) == 1:
                    f[state] += f[state ^ (1 << index)]
        
        return f[-1]
''',
    call='Solution().selfDivisiblePermutationCount(3)',
    expect=3,
    views=[
        dict(type='text', fn=_txt, h=90),
        dict(type='array', var='f', label='f[state]：已用数字集合为 state 时的方案数', cell=70, h=260,
             pointers={'state': 'blue'},
             color=lambda S, i, v: 'green' if v > 0 else None),
        dict(type='array', var='[(k + 1) for k in range(n)]', label='数字 1..n（位 k 对应数字 k+1）', cell=70, h=170,
             pointers={'index': 'pink'}),
    ],
    watch=['state', 'p', 'index', ('f[state]', "f[state] if 'state' in dir() else 0", 'green')],
    skip=['while y:', 'x, y = y, x % y', 'return x', 'def gcd', 'max_state = 1 << n', 14, 15, 16, 17, 19],
    captions={
        'f = [0]': '`f` 有 `2^n = {len(f)}` 个状态，初值 0',
        'f[0] = 1': '什么数都没放（空排列）算 ==1 种==方案：`f[0] = 1`',
        'for state in range': '枚举状态 `state = {state}`（二进制 `{state:0{n}b}`）：里面有 `p = {bin(state).count("1")}` 个数字，填进前 `p` 个位置',
        'and gcd(': lambda S, B, r: (
            f"数字 `{S.index + 1}` 不在 `state` 里 → 跳过" if not S.state >> S.index & 1 else
            f"数字 `{S.index + 1}` 放第 `{S.p}` 位：`gcd({S.index + 1}, {S.p}) = {math.gcd(S.index + 1, S.p)}` → "
            + ('==互质，合法==' if math.gcd(S.index + 1, S.p) == 1 else '==不互质，不能放==')),
        'f[state] += f[state ^': '数字 `{index + 1}` 放第 `{p}` 位合法：`state` 来自去掉它的 `{state ^ (1 << index)}`，方案数相加 → `f[{state}]` = =={f[state]}==',
        'return f[-1]': '全部数字都用上的状态 `f[-1]` = =={ret}== 种自整除排列',
    },
    max_steps=80,
    cards=dict(
        one_liner='f[state] 数一数：state 里的数字填满前 p 个位置有多少种',
        complexity='时间 `O(n · 2^n)`，空间 `O(2^n)`',
        problem=['给你正整数 `n`，把 `1..n` 排成排列 `a`（下标从 1 开始）',
                 '要求每个位置满足 `gcd(a[i], i) == 1`，称为自整除排列',
                 '求这样的排列有多少个；本视频示例 `n = 3`'],
        quote='本题的数据规模很小，可以直接使用状态压缩动态规划来处理。令f[state]表示用state中的字符填充数组前p个位置的方案数，其中p是state中包含的1的数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['`state` 里 1 的个数 `p` 就是已经填了多少位，不用额外记',
              '枚举最后填的数字 `v`：它放第 `p` 位必须 `gcd(v, p) == 1`',
              '合法就从 `state ^ (1 << v)` 转移过来，方案数相加'],
        summary=['时间 `O(n · 2^n)`（统计 1 的个数再加 gcd），空间 `O(2^n)`',
                 '位与数字对应：下标 `index` 对应数字 `index + 1`，gcd 也用 `index + 1`',
                 '`f[0] = 1`：空排列是一种方案，否则全为 0',
                 '原文为 Python 2 风格写法，Python 3 下可直接运行，未改动'],
    ),
)
