def _digs(S):
    d = S.get('d')
    return ''.join(str(t) for t in d) if d else ''


def _split(S):
    d, w = S.get('d'), S.get('w')
    if not d or w is None:
        return ''
    s = ''.join(str(t) for t in d)
    x, y = S.get('x'), S.get('y')
    tail = ''
    if S.get('_line', 0) >= 28:
        tail = f'，x = `{x}`'
    return f'数位 ==`{s}`==：前 `w = {w}` 位 `{s[:w]}` 组成 x，剩下 `{s[w:]}` 组成 y' + (f'；当前 x = `{x}`' if x else '')


def _dcolor(S, k, v):
    w = S.get('w')
    if w is None:
        return None
    return 'blue' if k < w else 'pink'


CONFIG = dict(
    num=4039, title='解码值之和', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='数位拆分 + 递归快速幂',
    tags=[],
    code='''
class Solution(object):
    def sumDecoded(self, nums):
        
        def quick_power(base, p, mod):
            if p == 0:
                return 1
            if p == 1:
                return base % mod
            
            x = quick_power(base, p // 2, mod)
            x = x * x % mod
            if p & 1:
                x = x * base % mod
            return x

        res = 0
        mod = 10 ** 9 + 7
        for v in nums:
            w = v % 10
            v //= 10

            d = []
            while v:
                d.append(v % 10)
                v //= 10

            d.reverse()
            x = 0
            for index in range(w):
                x = x * 10 + d[index]
            
            y = 0
            for index in range(w, len(d)):
                y = y * 10 + d[index]
            
            res += quick_power(x, y, mod)
            if res >= mod:
                res -= mod
        
        return res
''',
    call='Solution().sumDecoded([2522, 2101])',
    expect=1649,
    skip=['res = 0', 'mod = 10 ** 9', 'd = []', 'v //= 10', 'x = 0', 'y = 0', 'd.reverse'],
    max_steps=110,
    views=[
        dict(type='array', var='nums', label='nums（编码值）', h=140, cell=120,
             color=lambda S, k, v: None),
        dict(type='array', var=lambda S: S['d'] if S.get('d') else [], label='d（蓝 = x，粉 = y）', h=200, cell=70, color=_dcolor),
        dict(type='text', fn=lambda S: _split(S), size=24, h=60),
        dict(type='calls', h=240),
    ],
    watch=['w', 'x', 'y', ('res', 'res', 'green')],
    captions={
        'for v in nums': lambda S, B, r: ('nums 处理完了，退出循环' if S.v == 0 else f'取下一个编码值 `{S.v}`'),
        'w = v % 10': '最后一位是宽度：`w = {w}`；去掉它（`v //= 10`），剩下 `{v // 10}`',
        'while v': lambda S, B, r: (f'`v = {S.v}` 还没取完，继续逐位拆' if S.v else '`v = 0`：数位拆完了（此时 d 是倒序）'),
        'd.append': '取最低位 `{v % 10}` 放进 `d`：`d = {d}`',
        'for index in range(w)': lambda S, B, r: (f'前 `w = {S.w}` 位拼完了，x = =={S.x}==' if B.get('index') == S.index and S.y == 0 and S.x else f'前 `w = {S.w}` 位组成 x：`index = {S.index}`'),
        'x = x * 10 + d[index]': '`x = x * 10 + d[{index}]`：拼数字，`x = {x}`',
        'for index in range(w, len': lambda S, B, r: ('剩下的位拼完了，y = ==' + str(S.y) + '==' if S.y else '剩下的数位组成 y'),
        'y = y * 10': '`y = y * 10 + d[{index}]`：`y = {y}`',
        'res += quick_power': '调用 `quick_power({x}, {y}, mod)` 算 `{x}^{y}`，结果累加进 `res`',
        'if res >= mod': '`res = {res}`，没超过 `mod` 就不用减' ,
        'res -= mod': '超过了 `mod`，减一次即可',
        'if p == 0': lambda S, B, r: ('`p = 0`：指数 0 → 结果是 1' if S.p == 0 else f'`p = {S.p}` ≠ 0，继续'),
        'return 1': '任何数的 0 次方是 1',
        'if p == 1': lambda S, B, r: (f'`p = 1`：指数 1 → 就是 `base % mod`' if S.p == 1 else f'`p = {S.p}` ≠ 1，要折半递归'),
        'return base % mod': '递归到底，返回 `{ret}`',
        'x = quick_power': '折半：先递归求 `base^(p // 2)` = `{base}^{p // 2}`',
        'x = x * x % mod': '平方得到 `base^{p - p % 2}`：`x = {x}`',
        'if p & 1': lambda S, B, r: (f'`p = {S.p}` 是奇数，还要再乘一个 base' if S.p & 1 else f'`p = {S.p}` 是偶数，不用再乘'),
        'x = x * base % mod': '补乘一个 `base`：`x = {x}`',
        'return x': '返回 `{ret}`',
        'return res': '全部解码值之和 `{res}`',
    },
    cards=dict(
        one_liner='把数字拆成数位，前 w 位是底数，剩下是指数',
        complexity='时间 `O(n·(log U + log y))`，空间 `O(log y)`',
        problem=['`nums[i]` 编码了 `x`、`y`：`w = nums[i] % 10`，`d = nums[i] // 10`',
                 '`x` 是 `d` 的前 `w` 位，`y` 是剩下的位，解码值是 `x^y`，求总和模 `10^9+7`',
                 '示例：`[2522,2101]` → `25² + 2¹⁰ = 625 + 1024 = 1649`'],
        quote='通过模10除以10的方法分离出数位数组d，然后将d反转，通过前w位构造出x，剩余的数位构造出y，最后利用快速幂计算x^y并累加到答案中。',
        quote_src='—— yiduobo 题解原文',
        idea=['先 `v % 10` 取出 `w`，再反复 `% 10`、`// 10` 把数位收进 `d`',
              '收进来是倒序，所以要 `d.reverse()`，再顺着拼出 `x` 和 `y`',
              '`quick_power` 递归折半：先算 `p // 2`，平方，奇数再补乘一次 `base`'],
        summary=['时间 `O(n·(log U + log y))`，空间 `O(log y)`（递归深度）',
                 '`d` 是倒序收集的，不 reverse 会把 x 和 y 拼反',
                 '累加后只减一次 `mod`：两个小于 mod 的数相加不会超过 `2*mod`',
                 '对比灵神：灵神数位数后用 `10^(len-w)` 一刀切开，yiduobo 先拆成数位数组再拼接'],
    ),
)
