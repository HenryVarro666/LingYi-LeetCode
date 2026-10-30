LET = 'abcdefghijklmnopqrstuvwxyz'


def _row(S):
    """base 里 'z' 这一行的非零列：z 经过当前次数的变换后变成什么"""
    base = S.get('base')
    if not base:
        return ''
    parts = [f'{LET[j]}×{v}' for j, v in enumerate(base[25]) if v]
    return '`base` 的 z 行：一个 `z` 经过当前这么多次变换后变成 ==' + ('、'.join(parts) if parts else '空') + '=='


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    res = S.get('res')
    cv.text((x0 + 18, y0 + 2), 'res[0]：每个字母现在有多少个（长度 = 全部相加）', 24, T['muted'], bold=True)
    if not res or not isinstance(res[0], list):
        return
    row = res[0]
    old = (B.get('res') or [[0] * 26])[0] if isinstance(B.get('res'), list) and B.get('res') else row
    cell = (x1 - x0 - 40) / 13
    for k in range(26):
        r, c = divmod(k, 13)
        X = x0 + 20 + c * cell
        Y = y0 + 50 + r * 120
        v = row[k]
        changed = k < len(old) and old[k] != v
        fill = T['yellow'] if changed else (T['blue'] if v else (60, 66, 76))
        cv.rect((X + 2, Y, X + cell - 2, Y + 64), fill=fill, r=8, alpha=230)
        cv.text((X + cell / 2, Y + 32), v, 28, T['bg'] if v else T['dim'], anchor='mm', bold=True)
        cv.text((X + cell / 2, Y + 70), LET[k], 20, T['muted'], anchor='mt', mono=True)
    tot = sum(row)
    cv.text((x0 + 20, y0 + 300), f'现在共 {tot} 个字符（还没取模）' , 26, T['green'], bold=True)


def _tbin(S):
    t = S.get('t')
    if t is None or S['_line'] < 34:
        return ''
    if not t:
        return '`t = 0`：次数用完'
    return f'`t` = `{bin(t)[2:]}`（{t}）：' + ('最低位是 1 → 乘进 res' if t & 1 else '最低位是 0 → 不乘进 res')


CONFIG = dict(
    num=3335, title='字符串转换后的长度 I', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='字母计数向量 · 矩阵快速幂',
    tags=[],
    code='''
class Solution(object):
    def lengthAfterTransformations(self, s, t, nums):
        
        def generate(nums):
            n = len(nums)
            base = [[0] * n for _ in range(n)]
            for i, x in enumerate(nums):
                for j in range(i + 1, i + x + 1):
                    base[i][j % n] = 1
            
            return base
            
        base = generate(nums)

        res = [[0] * 26]
        for char in s:
            res[0][ord(char) - 97] += 1
        
        mod = 10 ** 9 + 7

        def mul(a, b):
            m = len(a)
            n = len(a[0])
            o = len(b[0])

            c = [[0] * o for _ in range(m)]
            for i in range(m):
                for j in range(n):
                    for k in range(o):
                        c[i][k] = (c[i][k] + a[i][j] * b[j][k]) % mod
            
            return c

        while t:
            if t & 1:
                res = mul(res, base)
            
            base = mul(base, base)
            t >>= 1

        return sum(res[0]) % mod
''',
    call='Solution().lengthAfterTransformations("abcyy", 2, [1] * 25 + [2])',
    expect=7,
    views=[
        dict(type='text', fn=_tbin, size=26, h=60),
        dict(type='custom', draw=_draw, h=400),
        dict(type='text', fn=_row, size=24, h=70),
    ],
    watch=[('t', 't', 'orange'), ('sum(res[0])', 'sum(res[0]) if "res" in S and S["res"] and isinstance(S["res"][0], list) else 0', 'green')],
    max_steps=90,
    max_events=400000,
    skip=['def generate', 'def mul', 'n = len(nums)', 'm = len(a)', 'n = len(a[0])', 'o = len(b[0])', 'c = [[0] * o for _ in range(m)]',
          'for i in range(m)', 'for j in range(n)', 'for k in range(o)', 'c[i][k] = ', 'mod = 10 ** 9 + 7',
          'for i, x in enumerate(nums)', 'for j in range(i + 1', 'base[i][j % n] = 1', 'base = [[0] * n for _ in range(n)]'],
    captions={
        'base = generate(nums)': lambda S, B, r: '构造 26×26 转移矩阵 `base`：第 i 个字母变成第 `i+1` 到 `i+nums[i]` 个字母（超出 z 回绕到 a）',
        'return base': '`base[25]`（z 行）有两个 1：`z` → `a`、`b`；其余字母各变成下一个字母',
        'res = [[0] * 26]': '`res` 是 1×26 的行向量：每个字母各有多少个',
        'for char in s': lambda S, B, r: ('统计完毕：`res[0]` 里是每个字母的个数' if sum(S.res[0]) == len(S.s) else f'统计 `s` 里每个字母出现次数：`char = {S.char}`'),
        'res[0][ord(char) - 97] += 1': '`{char}` 的计数 +1 → `res[0][{ord(char) - 97}] = {res[0][ord(char) - 97]}`',
        'while t': lambda S, B, r: (f'`t = {S.t}`（二进制 `{bin(S.t)[2:]}`）还没用完 → 按二进制位拆成 `base` 的幂' if S.t else '`t = 0`：每一位都处理完了'),
        'if t & 1': lambda S, B, r: (f'`t = {bin(S.t)[2:]}` 最低位是 1 → 这一位的 `base` 要乘进 `res`' if S.t & 1 else f'`t = {bin(S.t)[2:]}` 最低位是 0 → 这一位不乘进 `res`'),
        'res = mul(res, base)': '`res = res × base`：一次矩阵乘法 = ==所有字母同时变换若干次==（当前 base 代表 2^k 次变换）',
        'base = mul(base, base)': '`base` 自乘：变换次数翻倍（B → B² → B⁴ …），不用一次次模拟'.replace('B⁴', 'B^4'),
        't >>= 1': '`t` 右移一位，处理下一个二进制位：`t = {t}`',
        'return c': '矩阵乘完了（三重循环已快进），结果取模',
        'return sum(res[0]) % mod': '长度 = `res[0]` 所有计数相加 = `{sum(res[0])}`，再 `% (10^9+7)`',
    },
    cards=dict(
        one_liner='不模拟字符串，只数每个字母有多少个，转移用矩阵快速幂',
        complexity='时间 `O(n + 26^3 log t)`，空间 `O(26^2)`',
        problem=['`z` 变成 `"ab"`，其他字母变成下一个字母，做 `t` 次转换后字符串多长（对 10^9+7 取模）',
                 '示例：`s = "abcyy", t = 2` → `7`',
                 '本题是 3337 的特例：`nums = [1,1,...,1,2]`（z 变 2 个字符）'],
        quote='令f[index][c]表示执行index次操作后，字符串中第c种字符的数量……不妨将f[index]想象成一个1 * 26的矩阵A，那么在这里就需要构造一个26 * 26的乘数矩阵B。',
        quote_src='—— yiduobo 题解原文',
        idea=['只关心每个字母的个数：长度 `10^5`、`t` 到 `10^5` 直接模拟会爆',
              '一次变换 = 行向量 × 26×26 矩阵 `B`；`t` 次变换 = `A × B^t`',
              '`B^t` 用快速幂：按 `t` 的二进制位，`base` 不断自乘，该位为 1 就乘进 `res`'],
        summary=['时间 `O(n + 26^3 log t)`，空间 `O(26^2)`',
                 '3335 的 `nums` 取 `[1]*25 + [2]`：只有 z 会变成两个字符',
                 '易错：乘法里每次都要 `% mod`；`j % n` 让 z 之后回绕到 a',
                 '原文是 3337 的通用代码（带 `nums` 参数），本题只是传入固定的 `nums`',
                 '视频中三重循环的矩阵乘法被快进，只展示每次 `mul` 的调用与结果'],
    ),
)
