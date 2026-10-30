def _per(S):
    return list(range(1, S['p'] + 1)) if 'p' in S else []


def _color(S, i, v):
    x, y = S.get('x'), S.get('y')
    if x is not None and v == x:
        return 'blue'
    if y is not None and v == y:
        return 'pink'
    return None


def _dim(S, i, v):
    return v % S['a'] and v % S['b']


def _txt(S):
    if 'p' not in S:
        return f"第 `{S['n']}` 个能被 `{S['a']}` 或 `{S['b']}` 整除的数"
    if 'cnt' not in S:
        return f"一个周期 `p = {S['p']}`（最小公倍数）"
    if 'x' not in S:
        return f"每 `p = {S['p']}` 个数有 `cnt = {S['cnt']}` 个神奇数；整周期共 `res = {S['res']}`"
    return f"还要走 `n = {S['n']}` 步：`x = {S['x']}`，`y = {S['y']}`，较小的 ==`{min(S['x'], S['y'])}`=="


CONFIG = dict(
    num=878, title='第 N 个神奇数字', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='最小公倍数周期 + 双指针模拟',
    tags=['难度分 1897'],
    code='''
class Solution(object):
    def nthMagicalNumber(self, n, a, b):

        mod = 10 ** 9 + 7
        n -= 1
        p = a * b // self.gcd(a, b)
        cnt = p // a + p // b - 1
        res = n // cnt * p % mod
        n %= cnt
        x = a
        y = b
        while n:
            if x < y:
                x += a
            else:
                y += b
            n -= 1
        return (res + min(x, y)) % mod
    
    def gcd(self, x, y):
        while y:
            x, y = y, x % y
        return x
''',
    call='Solution().nthMagicalNumber(7, 2, 3)',
    expect=10,
    views=[
        dict(type='text', fn=_txt, h=80),
        dict(type='array', var=_per, label='一个周期 1..p（亮 = 神奇数字；蓝 = x 所在，粉 = y 所在）', color=_color, dim=_dim, h=240),
    ],
    watch=['n', 'p', 'cnt', ('res', 'res', 'green'), ('x', 'x', 'blue'), ('y', 'y', 'pink')],
    captions={
        6: '先求最小公倍数 `p = a × b // gcd(a, b)`：调用 `gcd` 辗转相除',
        5: '`n` 先减一，改成 0 起点的名次（跳过 n 个之后的下一个）：`n = {n}`',
        17: '少走一步，`n = {n}`',
        'p = a * b': '最小公倍数 `p = {a} × {b} // gcd = {p}`：数字的整除规律每 `p` 个重复一次',
        'cnt = p': '一个周期里：`{p}//{a} + {p}//{b} − 1 = {cnt}` 个（`p` 自己被数了两次，减 1）',
        'res = n //': '前面有 `n // cnt = {B.n // cnt}` 个完整周期，共 `{B.n // cnt} × {p}` → `res = {res}`',
        'n %= cnt': '剩下 `n = {n}`：还要在新周期里再往后走 `n` 个',
        'x = a': '`x` 是 a 的倍数里当前最小的',
        'y = b': '`y` 是 b 的倍数里当前最小的',
        'while n': lambda S, B, r: (f'还要走 `n = {S.n}` 步 → 继续' if S.n else '走完了，`min(x, y)` 就是周期内要找的数'),
        'if x < y': lambda S, B, r: (f'`x = {S.x} < y = {S.y}`：`x` 更小，先被用掉 → ==x 前进=='if S.x < S.y else f'`x = {S.x} ≥ y = {S.y}`：`y` 更小（或相等），先被用掉 → ==y 前进=='),
        'x += a': '`x` 跳到下一个 a 的倍数：`{x}`',
        'y += b': '`y` 跳到下一个 b 的倍数：`{y}`',
        'return (res': '`res + min(x, y)` = `{res} + {min(x, y)}`，取模后 = =={ret}==',
        'while y': lambda S, B, r: (f'`y = {S.y}` 不为 0 → 继续辗转相除' if S.y else '`y = 0`，`x` 就是最大公约数'),
        'x, y = y': '辗转相除：`x, y = y, x % y` → `({x}, {y})`',
        'return x': '`gcd = {x}`，最小公倍数 = `a × b // gcd`',
    },
    cards=dict(
        one_liner='数字规律每 lcm 个重复一次：先跳过整周期，再在周期里数余项',
        complexity='时间 `O(a + b)`（周期内最多 `cnt` 步），空间 `O(1)`',
        problem=['能被 `a` 或 `b` 整除的正整数是神奇数字，求第 `n` 个，结果对 `10^9 + 7` 取模',
                 '示例：`n=4, a=2, b=3` → `6`',
                 '本视频：`n=7, a=2, b=3` → `10`（2,3,4,6,8,9,10）'],
        quote='每p个数中就有p/A + p/B - 1个数可以整除A或者B，记这个数为cnt。接下来，我们就可以利用上面p和cnt的性质，来确定第n个数位于第几个p的区间内。',
        quote_src='—— yiduobo 题解原文',
        idea=['`p = lcm(a, b)`，每个周期 `p` 里有 `cnt = p/a + p/b − 1` 个神奇数字',
              '`n // cnt` 个整周期直接跳过，`n % cnt` 是周期内的名次',
              '周期内用两个指针 `x`、`y` 像归并一样：谁小谁前进，走 `n` 步取较小者'],
        summary=['时间 `O(a + b)`，空间 `O(1)`；不用二分，用周期性',
                 '`n -= 1` 先转成 0 起点，最后 `min(x, y)` 才是第 `n` 个',
                 '`cnt` 减 1 是因为 `p` 本身同时是 a、b 的倍数，被数了两次',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '对比灵神：灵神二分答案 + 容斥；yiduobo 用周期 + 归并'],
    ),
)
