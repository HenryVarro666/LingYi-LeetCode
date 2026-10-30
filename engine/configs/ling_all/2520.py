def _txt(S):
    if 'x' not in S:
        return ''
    n, x = S['num'], S['x']
    if x == 0:
        return f'`x = 0`，每一位都取完了：答案 =={S["ans"]}=='
    d = x % 10
    return f'`x = {x}`，个位 `d = {d}`；`{n} % {d}` = =={n % d}== → {"整除，ans 加一" if n % d == 0 else "不整除"}'


CONFIG = dict(
    num=2520, title='统计能整除数字的位数', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='模 10 取位、除 10 去位', tags=[],
    code='''
class Solution:
    def countDigits(self, num: int) -> int:
        ans = 0
        x = num
        while x:
            ans += num % (x % 10) == 0
            x //= 10
        return ans
''',
    call='Solution().countDigits(1245)',
    expect=2,
    views=[
        dict(type='text', fn=_txt, size=34, h=140),
        dict(type='string', var=lambda S: str(S['x']) if 'x' in S and S['x'] else '', label='x 还剩的数位', cell=110, h=200),
        dict(type='text', fn=lambda S: f"原数 `num = {S['num']}`" if 'num' in S else '', size=30, h=100),
    ],
    watch=['num', ('x', 'x', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 统计能整除 `num` 的数位个数',
        'x = num': '拷贝一份 `x`：它会被不断除 10，`num` 要留着做被除数',
        'while x': lambda S, B, r: (f'`x = {S.x}`，还有数位，继续' if S.x else '`x = 0`：数位取完了，退出循环'),
        'ans += num': '`num % {x % 10}` = {num % (x % 10)}：=={"整除，ans 加一" if num % (x % 10) == 0 else "不整除，ans 不变"}== → ans = {ans}',
        'x //= 10': '去掉最低位：`x` → {x}',
        'return ans': '所有数位都检查完，返回 `{ans}`',
    },
    cards=dict(
        one_liner='不转字符串：模 10 取最低位，除 10 去掉它',
        complexity='时间 `O(log num)`，空间 `O(1)`',
        problem=['返回 `num` 的数位中，能整除 `num` 的数位个数',
                 '`num` 的数位中不含 0；重复数位要重复计数',
                 '示例：`121` → `2`；本视频：`1245` → `2`'],
        quote='代码实现时，可以不用转成字符串处理，而是不断取最低位（模 10），去掉最低位（除以 10），直到数字为 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x % 10` 得到当前最低位 `d`，`x //= 10` 去掉它',
              '`num % d == 0` 是布尔值，直接累加到 `ans`',
              '1245：`5` 整除、`4` 不整除、`2` 不整除、`1` 整除 → 2'],
        summary=['时间 `O(log num)`，即 `num` 的十进制位数，空间 `O(1)`',
                 '被除数始终是 `num`，不是 `x`',
                 '题目保证没有 0 数位，所以 `x % 10` 不会除零',
                 '写法二用 `divmod(x, 10)` 一次拿到商和余数'],
    ),
)
