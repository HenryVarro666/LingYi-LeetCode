CONFIG = dict(
    num=3848, title='阶数数字排列', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='数位阶乘和 · 计数比较',
    code='''
# 预处理阶乘
fac = [1] * 10
for i in range(1, 10):
    fac[i] = fac[i - 1] * i

class Solution:
    def isDigitorialPermutation(self, n: int) -> bool:
        sum_fac = 0
        cnt = [0] * 10
        while n > 0:
            n, d = divmod(n, 10)
            sum_fac += fac[d]
            cnt[d] += 1

        while sum_fac > 0:
            sum_fac, d = divmod(sum_fac, 10)
            cnt[d] -= 1

        return cnt == [0] * 10
''',
    call='Solution().isDigitorialPermutation(541)',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: f"阶乘和 `sum_fac` = =={S['sum_fac']}==" if 'sum_fac' in S else '', size=34),
        dict(type='text', fn=lambda S: '预处理 `fac[d] = d!`：1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880', size=26),
        dict(type='array', var='cnt', label='cnt[d]：n 的数位 +1，sum_fac 的数位 −1', h=200, cell=70,
             color=lambda S, i, v: ('green' if v > 0 else 'pink' if v < 0 else None) if 'd' in S and i == S['d'] else None,
             pointers={'d': 'yellow'}),
    ],
    watch=['n', 'd', 'sum_fac', 'cnt'],
    captions={
        'n, d = divmod(n, 10)': '取出最低位 `d = {d}`，`n` 变成 {n}',
        'sum_fac += fac[d]': '数位 {d} 的阶乘 `{d}! = {fac[d]}`，累加：`sum_fac` = =={sum_fac}==',
        'cnt[d] += 1': '`n` 里数字 {d} 出现次数 +1：`cnt[{d}] = {cnt[d]}`',
        'sum_fac, d = divmod': '取出 `sum_fac` 的最低位 `d = {d}`，剩下 {sum_fac}',
        'cnt[d] -= 1': '`sum_fac` 里数字 {d} 抵消一个：`cnt[{d}] = {cnt[d]}`',
        'return cnt': lambda S, B, r: ('每种数字个数都抵消为 0 → ==n 能重排成 sum_fac== → 返回 True' if r else '个数对不上 → 返回 False'),
    },
    cards=dict(
        one_liner='数位阶乘和与排列无关，只需比较 n 和 s 的数字个数',
        complexity='时间 `O(log n + D)`，空间 `O(D)`，`D = 10`',
        problem=['阶数数字：各位数字的阶乘之和等于它本身，如 `145 = 1! + 4! + 5!`',
                 '问 `n` 的某个排列（不能前导零）能否是阶数数字',
                 '本视频：`n = 541` → `true`'],
        quote='无论如何排列 n 中的数位，这些数位的阶乘之和是不变的。问题变成：能否把 n 重新排列，变成 s？',
        quote_src='—— 灵茶山艾府题解',
        idea=['先算出 `n` 各数位阶乘之和 `s`，它对任何排列都一样',
              '`n` 能重排成 `s` ⟺ 两者 0~9 的个数都相等',
              '用一个 `cnt`：`n` 的数位加一，`s` 的数位减一，最后全 0 即可'],
        summary=['时间 `O(log n + D)`，空间 `O(D)`',
                 '前导零不用特判：能重排成 `s`，长度相等，而 `s` 本身没有前导零',
                 '注里的另一种写法：只有 1、2、145、40558 四个本质不同的解，直接查表'],
    ),
)
