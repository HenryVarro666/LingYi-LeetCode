M = 1_000_000_007
OPS = ('`append(2)` `addAll(3)` `append(7)` `multAll(2)` `getIndex(0)` `addAll(3)` `append(10)` `multAll(2)` '
       '`getIndex(0)` `getIndex(1)` `getIndex(2)` `getIndex(3)`')


def _frac(v):
    """把模意义下的数写成小分数（如 500000004 ≡ 1/2），找不到就返回 None"""
    for d in range(1, 300):
        n = v * d % M
        if n < 100000:
            return n, d
    return None


def _show(v):
    f = _frac(v)
    if f and f[1] > 1:
        return f'{v} ≡ {f[0]}/{f[1]}'
    return str(v)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    vals, mul, add = S.get('self.vals'), S.get('self.mul'), S.get('self.add')
    if vals is None or mul is None or add is None:
        cv.text((x0 + 18, y0 + 10), '（尚未创建）', 24, T['dim'])
        return
    cv.rich(x0 + 22, y0 + 6, f'真实值 = `vals[i]` × ==mul== + ==add==（对 `10^9+7` 取模）', x1 - x0 - 44, size=28,
            accent=T['orange'])
    bm, ba = B.get('self.mul'), B.get('self.add')
    for k, (name, v, bv) in enumerate((('mul', mul, bm), ('add', add, ba))):
        X = x0 + 30 + k * 260
        ch = bv is not None and bv != v
        cv.rect((X, y0 + 64, X + 230, y0 + 124), fill=T['panel2'], r=10,
                outline=T['yellow'] if ch else T['border'], width=3 if ch else 1)
        cv.text((X + 16, y0 + 94), f'{name} = {v}', 30, T['yellow'] if ch else T['orange'], anchor='lm', mono=True, bold=True)
    n = len(vals)
    slots = max(3, n)
    w = (x1 - x0 - 40) / slots
    top = y0 + 170
    hot = S.get('idx') if S.get('_line') in (20, 22) else None
    bvals = B.get('self.vals') or []
    cv.text((x0 + 22, top - 8), '序列（上：vals 里存的值；下：真实值）', 22, T['muted'], anchor='lb', bold=True)
    for i in range(n):
        X = x0 + 20 + i * w
        v = vals[i]
        real = (v * mul + add) % M
        new = i >= len(bvals)
        oc = T['yellow'] if (i == hot or new) else T['border']
        cv.rect((X + 8, top, X + w - 8, top + 250), fill=T['panel2'], r=12, outline=oc, width=4 if oc != T['border'] else 1)
        cv.text((X + w / 2, top + 22), f'vals[{i}]', 20, T['muted'], anchor='mm', mono=True)
        cv.text((X + w / 2, top + 62), _show(v), 24 if len(_show(v)) < 14 else 19, T['code'], anchor='mm', mono=True, bold=True)
        cv.line([(X + 24, top + 100), (X + w - 24, top + 100)], T['border'], 2)
        cv.text((X + w / 2, top + 126), f'×{mul} + {add}', 20, T['muted'], anchor='mm', mono=True)
        cv.text((X + w / 2, top + 190), real, 52, T['green'], anchor='mm', bold=True)
    if hot is not None and hot >= n:
        X = x0 + 20 + min(hot, slots - 1) * w if hot < slots else x1 - w
        cv.text((x1 - 30, top + 290), f'idx = {hot} ≥ len(vals) = {n} → -1', 24, T['red'], anchor='ra', bold=True)


def _append(S, B, ret):
    val, add, mul = S.val, S.self.add, S.self.mul
    v = S.self.vals[-1]
    if mul == 1:
        return f'`append({val})`：存 `{val} − add = {val} − {add} = {v}`，保证 `{v} × 1 + {add} = {val}`，==式子对所有元素一致=='
    return (f'`append({val})`：要存 `({val} − {add}) / {mul}`，除法用==逆元== `pow({mul}, -1, MOD)` → `{_show(v)}`')


CONFIG = dict(
    num=1622, title='奇妙序列', difficulty='Hard', category='设计',
    author='灵茶山艾府', technique='懒更新 + 等价转化 · 乘法逆元',
    tags=['字节30天'],
    code='''
MOD = 1_000_000_007

class Fancy:
    def __init__(self):
        self.vals = []
        self.add = 0
        self.mul = 1

    def append(self, val: int) -> None:
        self.vals.append((val - self.add) * pow(self.mul, -1, MOD) % MOD)

    def addAll(self, inc: int) -> None:
        self.add += inc

    def multAll(self, m: int) -> None:
        self.mul = self.mul * m % MOD
        self.add = self.add * m % MOD

    def getIndex(self, idx: int) -> int:
        if idx >= len(self.vals):
            return -1
        return (self.vals[idx] * self.mul + self.add) % MOD
''',
    call='''f = Fancy()
f.append(2); f.addAll(3); f.append(7); f.multAll(2); a = f.getIndex(0)
f.addAll(3); f.append(10); f.multAll(2)
[a, f.getIndex(0), f.getIndex(1), f.getIndex(2), f.getIndex(3)]''',
    expect=[10, 26, 34, 20, -1],
    views=[
        dict(type='text', size=22, h=86, lines=2, fn=lambda S: f'操作：{OPS}'),
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=[('val', 'val', 'blue'), ('inc', 'inc', 'blue'), ('m', 'm', 'blue'), ('idx', 'idx', 'blue'),
           ('mul', 'self.mul', 'orange'), ('add', 'self.add', 'orange')],
    captions={
        'self.vals = []': '`vals` 存的不是真实值，而是满足 ==真实值 = v × mul + add== 的 v',
        'self.add = 0': '`add`：表示“每个数都要增加 add”，初始 0',
        'self.mul = 1': '`mul`：表示“每个数都要乘以 mul”，初始 1',
        'self.vals.append(': _append,
        'self.add += inc': '`addAll({inc})`：==懒更新==，不动 vals，只把 `add` 增加 {inc} → `{self.add}`',
        'self.mul = self.mul * m % MOD': '`multAll({m})`：`(v·mul + add)·m = v·(mul·m) + add·m` → `mul = {self.mul}`',
        'self.add = self.add * m % MOD': '……所以 `add` 也要乘以 {m} → `add = {self.add}`',
        'if idx >= len(self.vals)': lambda S, B, r: (f'`getIndex({S.idx})`：`{S.idx} ≥ len(vals) = {len(S.self.vals)}`，下标越界'
                                                     if S.idx >= len(S.self.vals) else
                                                     f'`getIndex({S.idx})`：下标合法，现在才真正计算'),
        'return -1': '返回 ==-1==',
        'return (self.vals[idx]': lambda S, B, r: (f'`{S.self.vals[S.idx]} × {S.self.mul} + {S.self.add}` mod M = =={r}=='
                                                   + ('（`1/2 × 4 + 18 = 20`）' if S.self.vals[S.idx] > 1000 else '')),
    },
    cards=dict(
        one_liner='不改每个数，只记 mul 和 add；append 时先“反向还原”再存',
        complexity='`append` 为 `O(log M)`，其余 `O(1)`，空间 `O(q)`',
        problem=['`append(val)` 追加；`addAll(inc)` 所有数加 inc；`multAll(m)` 所有数乘 m',
                 '`getIndex(idx)` 返回下标 idx 的值（模 `10^9+7`），越界返回 `-1`',
                 '示例：append 2、addAll 3、append 7、multAll 2 → `[10, 14]`，`getIndex(0) = 10`'],
        quote='用 add 记录操作 addAll，用 mul 记录操作 multAll。……为了让 val 兼容 vals[idx]·mul + add 这个式子，我们可以先计算 ==v = (val − add) / mul==，再把 v 添加到 vals 的末尾。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从特殊到一般：只有加法时记一个 `add`，`append` 时存 `val − add`',
              '`multAll(m)`：`(v·mul + add)·m = v·(mul·m) + add·m`，所以 `mul`、`add` 都乘 m',
              '模意义下的除法 = 乘==逆元== `mul^(M−2)`，Python 直接 `pow(mul, -1, MOD)`'],
        summary=['`append` 求逆元 `O(log M)`，其余操作 `O(1)`',
                 '易错：`multAll` 时 ==add 也要乘 m==；`append` 时要“除以” mul 而不是忽略它',
                 '因为 `m ≥ 1` 且 M 是质数，mul 永远不为 0，逆元一定存在',
                 '题解还从“只有加法”“只有乘法”两个特殊情况推导到一般情况'],
    ),
)
