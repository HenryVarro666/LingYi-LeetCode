N = 9


def _cat(S):
    if 'r' not in S or 'w' not in S:
        return ''
    done = S['r'] if S.get('_line', 0) in (6, 14, 15, 16) else S['l'] - 1
    return ''.join(bin(i)[2:] for i in range(1, done + 1))


def _top(S):
    if 'w' not in S:
        return ''
    if 'm' not in S:
        return f"枚举二进制长度 `w = {S['w']}`"
    line = S.get('_line', 0)
    base = f"第 {S['w']} 组：`[{S['l']}, {S['r']}]`，长度都是 {S['w']} 位，共 `m = {S['m']}` 个"
    if line in (13, 14):
        return base + f"；整组拼起来的值 `S` = =={S['s'] % 1_000_000_007}=="
    return base


def _col(S, i, v):
    if 'l' not in S or 'r' not in S:
        return None
    if S['l'] <= v <= S['r']:
        return ['blue', 'pink', 'green', 'purple'][(S['w'] - 1) % 4]
    return None


CONFIG = dict(
    num=1680, title='连接连续二进制数字', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='按二进制长度分组 + 等比数列求和',
    tags=['灵神题单·位运算', '灵神题单·数学算法', '难度分 1630'],
    code='''
class Solution:
    def concatenatedBinary(self, n: int) -> int:
        MOD = 1_000_000_007
        ans = 0
        w = 1
        while (1 << (w - 1)) <= n:
            l = 1 << (w - 1)
            r = min((1 << w) - 1, n)
            m = r - l + 1
            q = 1 << w
            pow_q = pow(q, m, MOD)
            inv_q1 = pow(q - 1, -1, MOD)
            s = r * (pow_q - 1) * inv_q1 - (q - m * pow_q + (m - 1) * pow_q * q) * inv_q1 * inv_q1
            ans = ans * pow_q + s
            w += 1
        return ans % MOD
''',
    call='Solution().concatenatedBinary(9)',
    expect=int(''.join(bin(i)[2:] for i in range(1, 10)), 2) % 1_000_000_007,
    views=[
        dict(type='text', fn=_top, size=26, h=60),
        dict(type='array', var=lambda S: list(range(1, S['n'] + 1)), label='1..n（同色 = 二进制长度相同的一组）',
             cell=84, h=190, color=_col, window=(lambda S: S['l'] - 1 if 'l' in S else None,
                                                 lambda S: S['r'] - 1 if 'r' in S else None)),
        dict(type='string', var=_cat, label='已经拼好的二进制（前面各组）', cell=40, h=150),
        dict(type='text', fn=lambda S: (f"拼到 ans 右边 = ans 左移 `w·m = {S['w'] * S['m']}` 位 = `ans × q^m`，所以乘 `pow_q`"
                                        if 'pow_q' in S and S.get('_line', 0) in (11, 12, 13, 14) else ''), size=24, h=50),
    ],
    watch=[('w', 'w', 'blue'), ('l', 'l'), ('r', 'r'), ('m', 'm', 'pink'), ('q', 'q'), ('ans', 'ans', 'green')],
    captions={
        'MOD =': '答案要对 `10^9+7` 取模',
        'ans = 0': '`ans` 存放已经连接好的结果',
        'w = 1': '`w` = 当前这一组数的二进制长度，从 1 位开始',
        'while (1 << (w - 1)) <= n': lambda S, B, ret: (
            f'`2^{S.w - 1} = {1 << (S.w - 1)} <= n = {S.n}`：还有 {S.w} 位的数 → 处理这一组' if (1 << (S.w - 1)) <= S.n
            else f'`2^{S.w - 1} = {1 << (S.w - 1)} > n = {S.n}`：没有更长的数了，结束'),
        'l = 1 <<': '这一组最小的数 `l = 2^(w-1) = {l}`，是 1 后面全 0',
        'r = min': '最大的数是全 1，即 `2^w - 1`，但不能超过 `n`：`r = {r}`',
        'm = r - l': '这一组共 `m = r - l + 1 = {m}` 个数',
        'q = 1 << w': '`q = 2^w = {q}`：把一个数接到后面，相当于前面的数乘 q',
        'pow_q = pow': '`pow_q = q^m = {pow_q}`（取模）：整组拼在 ans 后面，ans 要左移 `w·m` 位',
        'inv_q1 = pow': '公式里要除以 `q-1`：模运算下用逆元 `inv_q1 = {inv_q1}`',
        's = r *': lambda S, B, ret: (
            f'一组 `[{S.l},{S.r}]` 拼起来：`S = Σ (L+j)·q^(m-1-j)`，用等比数列 + 错位相减得闭式 → ==S = {S.s % 1_000_000_007}==（模意义下）'),
        'ans = ans *': '`ans = ans × q^m + S`：旧 ans 腾出位置，再接上这一组',
        'w += 1': '位数 +1，进入下一组：`w` → {w}',
        'return ans': lambda S, B, ret: f'最后统一取模：`ans % MOD` = =={ret}==',
    },
    cards=dict(
        one_liner='把 1..n 按二进制长度分组，每组一个公式算出',
        complexity='时间 `O(log² n)`，空间 `O(1)`',
        problem=['把 `1` 到 `n` 的二进制依次连接，求对应十进制数对 `10^9+7` 取余',
                 '示例：`n = 3` → `"1" "10" "11"` → `11011` → `27`',
                 '本视频：`n = 9`，分成 `[1] [2,3] [4,7] [8,9]` 四组'],
        quote='我们可以分别计算每一组连接后的值，最后再把这些值连接起来。',
        quote_src='—— 灵茶山艾府题解',
        idea=['同一组数二进制长度 `w` 相同，所以 `L..R` 连接 = `Σ (L+j)·q^(m-1-j)`，`q = 2^w`',
              '等比数列求和 + 错位相减，把一整组压成一个公式',
              '把这一组拼到 ans 右边：ans 乘 `q^m`，再加上这一组的值'],
        summary=['时间 `O(log² n)`，比逐个枚举的 `O(n)` 更快',
                 '除法在模下要用逆元：`pow(q-1, -1, MOD)`（Python 3.8+）',
                 '最后一组 `r = min(2^w - 1, n)`，不要超过 `n`',
                 '另一种写法：暴力 `for i in range(1, n+1): ans = (ans << i.bit_length() | i) % MOD`，`O(n)`'],
    ),
)
