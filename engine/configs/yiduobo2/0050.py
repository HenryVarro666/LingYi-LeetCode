X0, N0 = -2.0, 11
CHAIN = []
_t = N0
while _t >= 1:
    CHAIN.append(_t)
    _t //= 2                                   # 11 → 5 → 2 → 1

CODE = '''
class Solution(object):
    def myPow(self, x, n):
        if x == 0:
            return 0

        if n == 0:
            return 1

        if x < 0:
            if n % 2 == 1:
                symbol_flag = -1
            else:
                symbol_flag = 1
            x = -x
        else:
            symbol_flag = 1

        if n < 0:
            x = 1 / x
            n = -n

        return symbol_flag * self.calc(x, n)

    def calc(self, x, n):
        if n == 1:
            return x

        tmp = self.calc(x, n // 2)
        if n % 2 == 1:
            return tmp * tmp * x
        else:
            return tmp * tmp
'''
_LINES = CODE.strip('\n').split('\n')


def _ln(sub, nth=0):
    hits = [i + 1 for i, s in enumerate(_LINES) if sub in s]
    return hits[nth]


CALC_DEF = _ln('def calc')
RET_LINES = {_ln('return x'), _ln('return tmp * tmp * x'), _ln('return tmp * tmp', 1)}


def _done_levels(S):
    """哪些层（用 n 表示）已经算出结果"""
    line = S.get('_line', 0)
    inner = S.get('_inner') or {}
    if line < CALC_DEF or 'n' not in inner:
        return set()
    cur = inner['n']
    done = {v for v in CHAIN if v < cur and ('tmp' in inner or cur == 1)}
    if line in RET_LINES:
        done.add(cur)
    return done


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '递归链：x^n 依赖 x^(n//2)（绿 = 已算出，黄框 = 当前层）', 24, T['muted'], bold=True)
    line = S.get('_line', 0)
    inner = S.get('_inner') or {}
    cur = inner.get('n') if line > CALC_DEF else None
    done = _done_levels(S)
    k = len(CHAIN)
    w = min(176, (x1 - x0 - 80) / k - 40)
    gap = ((x1 - x0 - 80) - w * k) / max(1, k - 1)
    y = y0 + 64
    base = abs(X0)
    for i, v in enumerate(CHAIN):
        X = x0 + 40 + i * (w + gap)
        ok = v in done
        fill = T['green'] if ok else T['panel2']
        cv.rect((X, y, X + w, y + 110), fill=fill, r=14, outline=T['yellow'] if v == cur else T['border'],
                width=4 if v == cur else 1)
        tc = T['bg'] if ok else T['text']
        cv.text((X + w / 2, y + 32), f'x^{v}', 32, tc, anchor='mm', bold=True, mono=True)
        cv.text((X + w / 2, y + 80), f'= {base ** v:g}' if ok else '= ?', 28, tc, anchor='mm', bold=True)
        rule = '边界 x^1 = x' if v == 1 else ('奇：tmp·tmp·x' if v % 2 else '偶：tmp·tmp')
        cv.text((X + w / 2, y + 130), rule, 22, T['cyan'] if v % 2 or v == 1 else T['purple'], anchor='mt', bold=True)
        if i + 1 < k:
            cv.arrow((X + w + 6, y + 55), (X + w + gap - 6, y + 55), T['muted'], 3, 12)
            cv.text((X + w + gap / 2, y + 48), f'{v}//2', 20, T['muted'], anchor='mb', mono=True)
    yy = y + 190
    sf = S.get('symbol_flag')
    s1 = f'符号：`symbol_flag = {sf}`' if sf is not None else '符号：还没确定'
    cv.rich(x0 + 40, yy, s1 + f'（底数 `{X0:g}` 为负，`n = {N0}` 为奇数 → 结果为负）', x1 - x0 - 80, size=26)
    cv.rich(x0 + 40, yy + 52, f'最终答案 = `symbol_flag × calc({base:g}, {N0})`', x1 - x0 - 80, size=26, color=T['muted'])


def _calc_head(S, B, ret):
    n = S.n
    if n == 1:
        return '`n == 1`：==递归边界==，`x^1 = x`，直接返回'
    return f'`n = {n}` ≠ 1 → 先递归算出 `x^({n}//2) = x^{n // 2}`'


def _odd(S, B, ret):
    n, tmp = S.n, S.tmp
    head = f'子问题返回 `tmp = x^{n // 2} = {tmp:g}`；'
    if n % 2 == 1:
        return head + f'`n = {n}` 是==奇数==：`x^{n} = (x^{n // 2})² · x`'
    return head + f'`n = {n}` 是==偶数==：`x^{n} = (x^{n // 2})²`'


CONFIG = dict(
    num=50, title='Pow(x, n)', difficulty='Medium', category='数学',
    author='yiduobo', technique='快速幂 · 递归折半',
    tags=['字节30天', '热题173', '面试经典150'],
    code=CODE,
    call=f'Solution().myPow({X0}, {N0})',
    expect=-2048.0,
    views=[
        dict(type='custom', draw=_draw, h=390),
        dict(type='calls', label='调用栈（最上面是当前层）', h=220),
    ],
    watch=[('x', 'x', 'blue'), ('n', 'n'), ('symbol_flag', 'symbol_flag', 'pink'), ('tmp', 'tmp', 'green')],
    captions={
        'if x == 0': '`x = {x:g}` ≠ 0（底数为 0 时直接返回 0）',
        'if n == 0': '`n = {n}` ≠ 0（任何数的 0 次幂都是 1）',
        'if x < 0': '`x = {x:g} < 0`：先把==符号单独拿出来==，只对 `|x|` 做快速幂',
        _ln('if n % 2 == 1', 0): lambda S, B, ret: (f'`n = {S.n}` 是奇数 → 负数的奇数次幂是负数'
                                                      if S.n % 2 == 1 else f'`n = {S.n}` 是偶数 → 结果为正'),
        'symbol_flag = -1': '记下符号 `symbol_flag = -1`',
        'x = -x': '`x` 取绝对值：`{B.x:g}` → `{x:g}`',
        'if n < 0': '`n = {n}` 不是负数；若 n 为负，就令 `x = 1/x`、`n = -n`',
        'return symbol_flag * self.calc': '答案 = 符号 × `calc({x:g}, {n})`：进入递归，计算 `{x:g}^{n}`',
        'if n == 1': _calc_head,
        'return x': '返回 `x = {ret:g}`，开始逐层往回算',
        'tmp = self.calc(x, n // 2)': '`{B.n} // 2 = {B.n // 2}`：递归求 `x^{B.n // 2}`，==规模减半==',
        _ln('if n % 2 == 1', 1): _odd,
        'return tmp * tmp * x': '`x^{n} = {tmp:g} × {tmp:g} × {x:g}` = =={ret:g}==',
        'return tmp * tmp': '`x^{n} = {tmp:g} × {tmp:g}` = =={ret:g}==',
    },
    cards=dict(
        one_liner='x^n = (x^(n/2))²，奇数再乘一个 x：每层把 n 减半',
        complexity='时间 `O(log n)`，空间 `O(log n)`（递归栈）',
        problem=['实现 `pow(x, n)`：计算 `x` 的整数 `n` 次幂',
                 '`x` 可以为负，`n` 也可以为负：`2.0^-2 = 0.25`',
                 '示例：`x = 2.0, n = 10` → `1024.0`',
                 '本视频：`x = -2.0, n = 11` → `-2048.0`'],
        quote='对于x^n，若n为偶数，那么可以认为是x^(n / 2)的平方；若n为奇数，那么就是x^(n/2)的平方==再乘上一个x==。',
        quote_src='—— yiduobo 题解（思路一）',
        idea=['递归计算 `x^(n/2)`，直到幂为 1 停止，一共 `log n` 层',
              '思路二：把 n 看成二进制，第 k 位为 1 就乘上 `x^(2^k)`——两者本质一样',
              '负数先处理：`x < 0` 时把符号单独记下；`n < 0` 时令 `x = 1/x`，`n = -n`'],
        result='`symbol_flag × calc(2.0, 11)` = `-1 × 2048` = `-2048.0` ✓',
        summary=['时间 `O(log n)`，空间 `O(log n)`（递归深度）',
                 '==原文为 Python 2 写法==：`n / 2` 在 Python 3 是浮点除法，已改为整除 `n // 2`；并删去了类型说明文档字符串',
                 '`tmp` 只递归一次再平方；写成 `calc(n//2) * calc(n//2)` 会退化成 `O(n)`',
                 '其实快速幂对负底数同样成立，单独处理符号只是更直观',
                 '对比灵神：灵神用迭代枚举比特位（思路二），空间 `O(1)`'],
    ),
)
