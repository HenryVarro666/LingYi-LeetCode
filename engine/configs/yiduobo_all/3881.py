def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n, pos, k = S['n'], S['pos'], S['k']
    cv.text((x0 + 18, y0 + 4), f'{n} 个人：pos 左边 {pos} 个空位，右边 {n - 1 - pos} 个空位', 24, T['muted'], bold=True)
    cell = min(80, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    ys = y0 + 56
    left = S.get('left')
    right = S.get('right')
    for i in range(n):
        X = sx + i * cell
        if i == pos:
            fill, txt = T['yellow'], 'pos'
        elif left is not None and right is not None:
            vis = i < left if i < pos else (i - pos) <= right
            fill, txt = (T['green'], 'L' if i < pos else 'R') if vis else (T['panel2'], 'R' if i < pos else 'L')
        else:
            fill, txt = T['panel2'], ''
        cv.rect((X + 4, ys, X + cell - 4, ys + cell - 10), fill=fill, r=10, outline=T['border'])
        cv.text((X + cell / 2, ys + (cell - 10) / 2), txt, 26 if i != pos else 22, T['bg'] if fill != T['panel2'] else T['muted'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, ys + cell), i, 18, T['dim'], anchor='mt', mono=True)
    if left is not None and right is not None:
        cv.text((x0 + 20, ys + cell + 36), f'左侧 {left} 人选 L、右侧 {right} 人选 R（绿，被看见）', 24, T['green'], bold=True)


def _arrays(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    fac, ivf = S.get('fac', []), S.get('inv_fac', [])
    m = max(len(fac), len(ivf), 1)
    cell = min(170, (x1 - x0 - 150) / m)
    sx = x0 + 130
    for r, (name, arr, col) in enumerate((('fac[i]', fac, 'blue'), ('inv_fac[i]', ivf, 'cyan'))):
        y = y0 + 14 + r * 82
        cv.text((x0 + 20, y + 26), name, 22, T[col], anchor='lm', bold=True, mono=True)
        for i, v in enumerate(arr):
            X = sx + i * cell
            new = i == len(arr) - 1 and i > 1
            cv.rect((X + 3, y, X + cell - 3, y + 52), fill=T['panel2'], outline=T[col] if new else T['border'], width=3 if new else 1, r=8)
            cv.text((X + cell / 2, y + 26), v, 24, T['text'], anchor='mm', bold=True, mono=True)
    cv.text((x0 + 20, y0 + 14 + 2 * 82 - 4), 'fac[i] = i!，inv_fac[i] = (i!) 模 10^9+7 的逆元；下标 0..ma', 19, T['dim'])


def _term(S):
    if 'left' not in S or 'right' not in S or S.get('_line') not in (20, 21, 28):
        return '枚举 `left`：左侧被看见的人数；`right = k − left`'
    ls, rs = S['left_slot'], S['right_slot']
    from math import comb
    l, r = S['left'], S['right']
    return f'`C({ls}, {l}) × C({rs}, {r})` = {comb(ls, l)} × {comb(rs, r)} = =={comb(ls, l) * comb(rs, r)}=='


CONFIG = dict(
    num=3881, title='恰好看到 K 个人的方向选择', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='枚举左侧人数 · 组合数相乘',
    tags=['组合计数', '难度分 1761'],
    code='''
class Solution(object):
    def countVisiblePeople(self, n, pos, k):
        
        left_slot = pos
        right_slot = n - pos - 1
        ma = max(left_slot, right_slot)

        fac = [1, 1]
        mod = 10 ** 9 + 7
        for v in range(2, ma + 1):
            fac.append(fac[-1] * v % mod)
        
        inv = [1, 1]
        inv_fac = [1, 1]
        for v in range(2, ma + 1):
            inv.append((mod - mod // v) * inv[mod % v] % mod)
            inv_fac.append(inv_fac[-1] * inv[-1] % mod)
        
        def C(m, k):
            v = fac[m] * inv_fac[k] % mod * inv_fac[m - k] % mod
            return v

        left_mi = max(0, k - right_slot)
        left_ma = min(left_slot, k)
        res = 0
        for left in range(left_mi, left_ma + 1):
            right = k - left
            res = (res + C(left_slot, left) * C(right_slot, right) % mod) % mod
        
        return res * 2 % mod
''',
    call='Solution().countVisiblePeople(6, 2, 3)',
    expect=20,
    views=[
        dict(type='custom', draw=_draw, h=250),
        dict(type='custom', draw=_arrays, h=210),
        dict(type='text', fn=_term, size=28, h=70),
    ],
    watch=['left_slot', 'right_slot', 'left', 'right', ('res', 'res', 'green')],
    captions={
        'left_slot = pos': '`pos` 左边一共 `{left_slot}` 个空位',
        'right_slot =': '`pos` 右边一共 `n − pos − 1` = `{right_slot}` 个空位',
        'ma = max': '阶乘只需要预处理到两边空位数的较大值 `ma = {ma}`',
        'fac.append(fac[-1]': '`fac[{v}] = fac[{v - 1}] × {v}` = {fac[-1]}（阶乘，取模）',
        'inv.append': '线性递推逆元：`inv[{v}] = (mod − mod//{v}) × inv[mod % {v}]` 取模 = {inv[-1]}',
        'inv_fac.append(inv_fac': '`inv_fac[{v}] = inv_fac[{v - 1}] × inv[{v}]` = {inv_fac[-1]}：阶乘的逆元',
        'v = fac[m]': '算 `C({m}, {k}) = {m}! / ({k}! × {m - k}!)`：用 `fac` 乘两个 `inv_fac`，不用除法',
        'return v': '`C` 返回 =={ret}==',
        'left_mi = max': '左侧至少要看到 `k − right_slot` 个：即使右侧全可见也要凑够 → 下界 `left_mi = {left_mi}`',
        'left_ma = min': '左侧最多看到 `min(k, left_slot)` 个 → 上界 `left_ma = {left_ma}`',
        'right = k - left': '左边看到 `{left}` 个，右边就必须看到 `k − left = {right}` 个',
        'res = (res': '左边从 {left_slot} 个空位选 {left} 个、右边从 {right_slot} 个选 {right} 个：两个组合数相乘，累加进 `res`（现在是 {B.res}）',
        'return res': '`pos` 自己选 L 或 R 都行 → 答案 ×2：`{res}` × 2 = =={ret}==',
    },
    cards=dict(
        one_liner='左边选 left 个、右边选 k−left 个，枚举 left 再 ×2',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 个人排一排，每人选 `L` 或 `R`',
                 '`pos` 左边的人选 `L`、右边的人选 `R` 时才被 `pos` 看见',
                 '求 `pos` 恰好看见 `k` 人的方案数；本视频：`n=6, pos=2, k=3` → `20`'],
        quote='需要从左侧选出left个空位，让这些空位上的人选择L……然后从右侧选出k - left个空位，让这些空位上的人选择R。',
        quote_src='—— yiduobo 题解原文',
        idea=['`pos` 左边有 `pos` 个空位，右边有 `n−1−pos` 个空位',
              '枚举左边被看见的人数 `left`：方案数 `C(pos, left) × C(n−1−pos, k−left)`',
              '`left` 的范围：下界 `max(0, k−右空位)`，上界 `min(k, 左空位)`',
              '组合数要取模：预处理阶乘和阶乘逆元；最后 `pos` 自己 ×2'],
        summary=['时间 `O(n)`（预处理阶乘 + 逆元，枚举 left），空间 `O(n)`',
                 '`left` 的上下界不能漏，否则 `C(m, k)` 会下标越界',
                 '别忘最后 `res * 2`：`pos` 自己的方向',
                 '这个枚举求和其实等于 `C(n−1, k)`（范德蒙德恒等式），所以灵神直接一个组合数就够',
                 '原文已是 Python 3 可直接运行的写法，未做修改'],
    ),
)
