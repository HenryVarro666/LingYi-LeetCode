from math import comb as _comb

_N, _K = 6, 2


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    line = S.get('_line', 0)
    length = S.get('length')
    if length is None:
        return
    cv.text((x0 + 18, y0 + 4), f'先定长度：长度 L 的合法数共 C(L−1, L−k) 个（最高位必为 1）；要第 {_N} 小', 22, T['muted'], bold=True)
    chips = []
    cum = 0
    for L in range(_K, length + 1):
        cnt = _comb(L - 1, L - _K)
        chips.append((L, cnt, cum + 1, cum + cnt))
        cum += cnt
    cw, ch = 170, 80
    for j, (L, cnt, a, b) in enumerate(chips):
        X = x0 + 20 + j * (cw + 14)
        Y = y0 + 44
        found = line >= 16 and L == length
        cur = line < 16 and L == length
        hit = a <= _N <= b and line >= 12 and L == length and (S.get('tot', 0) + cnt >= _N)
        fill = T['green'] if found else T['panel2']
        cv.rect((X, Y, X + cw, Y + ch), fill=fill, r=10, outline=T['yellow'] if cur else T['border'], width=4 if cur else 1)
        cv.text((X + cw / 2, Y + 22), f'长度 {L}：{cnt} 个', 24, T['bg'] if found else T['text'], anchor='mm', bold=True)
        cv.text((X + cw / 2, Y + 56), f'第 {a}–{b} 小', 22, T['bg'] if found else T['muted'], anchor='mm')
    if 'res' in S:
        res = S['res']
        cell = min(70, (x1 - x0 - 60) / length)
        sx = x0 + 30
        ys = y0 + 175
        cv.text((x0 + 18, ys - 38), f'逐位填：res 的二进制（{length} 位，最高位必为 1）', 22, T['muted'], bold=True)
        idx = S.get('index')
        for t in range(length):
            pos = length - 1 - t
            X = sx + t * cell
            bit = (res >> pos) & 1
            passed = idx is not None and pos > idx and line >= 27
            cur = idx is not None and pos == idx and line in (27, 28, 29, 30, 32)
            fill = T['green'] if bit else ((52, 60, 72) if pos > (idx if idx is not None else -1) else T['panel2'])
            cv.rect((X + 3, ys, X + cell - 3, ys + cell * 0.8), fill=fill, r=8, outline=T['yellow'] if cur else T['border'], width=4 if cur else 1)
            cv.text((X + cell / 2, ys + cell * 0.4), bit, 30, T['bg'] if bit else T['muted'], anchor='mm', bold=True, mono=True)
            cv.text((X + cell / 2, ys + cell * 0.8 + 6), pos, 18, T['yellow'] if cur else T['dim'], anchor='mt', mono=True)
        cv.text((sx + length * cell + 24, ys + cell * 0.4), f'res = {res}', 30, T['text'], anchor='lm', bold=True)


def _txt(S):
    line = S.get('_line', 0)
    if 'res' in S and line >= 25:
        idx, z, n = S.get('index'), S.get('zero'), S.get('n')
        if idx is None:
            return f'最高位定为 1；剩 `{S["zero"]}` 个 0 要放，还要找这个长度里的第 `{n}` 小'
        return f'`index = {idx}`：还剩 `zero = {z}` 个 0，第 `{n}` 小'
    if line >= 16:
        return '用递推填杨辉三角 `c[m][t]` = C(m, t)（`-1` 表示还没填）'
    if 'comb' in S:
        return f'长度 `{S["length"]}`：`zero = {S["zero"]}`，合法数 `C({S["length"] - 1}, {S["zero"]})` = =={S["comb"]}==；已累计 `tot` = {S.get("tot", 0)}'
    return ''


CONFIG = dict(
    num=3821, title='二进制中恰好K个1的第N小整数', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='先定长度，再逐位填 · 组合数',
    tags=['组合计数', '位运算', '难度分 2069'],
    code='''
class Solution(object):
    def nthSmallest(self, n, k):

        tot = 0
        for length in range(k, 51):
            zero = length - k
            if zero == 0:
                comb = 1
            else:
                comb = comb * (length - 1) // zero

            if tot + comb >= n:
                break
            tot += comb

        c = [[-1] * length for _ in range(length)]
        c[0][0] = 1
        for m in range(1, length):
            c[m][0] = 1
            c[m][m] = 1
            for t in range(1, m):
                c[m][t] = c[m - 1][t] + c[m - 1][t - 1]

        n -= tot
        res = 1 << (length - 1)
        for index in range(length - 2, -1, -1):
            if zero == 0 or c[index][zero - 1] < n:
                res |= 1 << index
                if zero > 0:
                    n -= c[index][zero - 1]
            else:
                zero -= 1
        
        return res
''',
    call=f'Solution().nthSmallest({_N}, {_K})',
    expect=12,
    views=[
        dict(type='custom', draw=_draw, h=290),
        dict(type='table', var='c', label='c[m][t] = C(m, t)', h=190,
             cursors=[(lambda S: S['m'] if S['_line'] < 24 else S.get('index', 0),
                       lambda S: S['t'] if S['_line'] < 24 else max(S.get('zero', 1) - 1, 0),
                       'yellow', '')]),
        dict(type='text', fn=_txt, size=24, h=60),
    ],
    watch=['n', 'k', ('tot', 'tot', 'blue'), ('zero', 'zero', 'pink'), ('res', 'res', 'green')],
    skip=['tot = 0', 'zero = length - k', 'for length in range', 'else:', 'for m in range', 'for t in range', 'for index in range', 'c[m][0] = 1', 'c[m][m] = 1'],
    max_steps=70,
    captions={
        'if zero == 0:': lambda S, B, r: ('`zero = 0`：长度 = k，只有全 1 这一种' if S.zero == 0 else f'`zero = {S.zero}` > 0：递推组合数'),
        'comb = 1': '长度 `{length}` 恰好 `k` 位全是 1：只有 `1` 个',
        'comb = comb *': '长度 `{length}`：`C({length - 1}, {zero})` = 上一个 `{B.comb}` × `{length - 1}` // `{zero}` = =={comb}==（最高位固定为 1，其余 `{length - 1}` 位里放 `{zero}` 个 0）',
        'if tot + comb >= n': lambda S, B, r: (f'`tot + comb = {S.tot} + {S.comb} = {S.tot + S.comb}` ≥ `n = {S.n}` → 第 `{S.n}` 小就在这个长度里' if S.tot + S.comb >= S.n else f'`tot + comb = {S.tot + S.comb}` < `n = {S.n}` → 答案比这个长度更长'),
        'break': '长度确定：`length = {length}`',
        'tot += comb': '短于答案的数共 `tot` = =={tot}== 个，继续看更长的长度',
        'c = [[-1]': '建一张 `length × length` 的杨辉三角表，`-1` = 没填',
        'c[0][0] = 1': '`C(0, 0) = 1`',
        'c[m][t] = c': '`c[{m}][{t}] = c[{m - 1}][{t}] + c[{m - 1}][{t - 1}]` = =={c[m][t]}==',
        'n -= tot': '前面更短的数 `tot` 个都不是：问题变成「长度为 `{length}` 的数里第 `{n}` 小」',
        'res = 1 <<': '最高位必须是 1：`res = 1 << {length - 1}` = {res}',
        'if zero == 0 or': lambda S, B, r: (f'`zero = 0`：0 都放完了，剩下的位只能是 1' if S.zero == 0 else f'这一位填 0 的方案数 `c[{S.index}][{S.zero - 1}]` = {S.c[S.index][S.zero - 1]}；{"小于" if S.c[S.index][S.zero - 1] < S.n else "不小于"} `n = {S.n}` → ' + ('这一位填 1' if S.c[S.index][S.zero - 1] < S.n else '这一位填 0')),
        'res |= 1 << index': '第 `{index}` 位填 1：`res` = =={res}==',
        'n -= c[index]': '填 0 的那 `c[{index}][{zero - 1}]` = {c[index][zero - 1]} 个都排在前面：`n` → =={n}==',
        'zero -= 1': '第 `{index}` 位填 0：用掉一个 0，`zero` → =={zero}==；`n` 不变',
        'return res': '第 `6` 小的数是 =={ret}==，二进制 `1100`',
    },
    cards=dict(
        one_liner='先数出答案有几位，再从高位逐位填 0 / 1',
        complexity='时间 `O(L²)`（L ≤ 50，建杨辉三角），空间 `O(L²)`',
        problem=['求二进制恰好有 `k` 个 `1` 的第 `n` 小的正整数，答案 `< 2^50`',
                 '示例：`n=4, k=2` → `9`',
                 '本视频：`n=6, k=2` → `12`（`3, 5, 6, 9, 10, 12`）'],
        quote='越长的二进制数就越大，题目需要找出恰好是第n小的数，因此在这里可以先想办法确定答案的长度。',
        quote_src='—— yiduobo 题解原文',
        idea=['长度为 `length` 的合法数：最高位必为 1，其余 `length−1` 位放 `length−k` 个 0，共 `C(length−1, zero)` 个',
              '从 `k` 开始累计 `tot`，直到 `tot + comb ≥ n`，答案长度就是此时的 `length`',
              '`n -= tot` 后，在该长度里从高位逐位填：填 0 的方案数 `c[index][zero−1]`',
              '`c[...] < n` 就必须填 1 并 `n -= c[...]`，否则填 0（`zero -= 1`）'],
        summary=['时间 `O(L²)`，空间 `O(L²)`，`L ≤ 50`',
                 '最高位固定是 1，所以逐位填从 `length − 2` 开始',
                 '`zero == 0` 时剩下的位全填 1，不用再查表',
                 '`comb` 是递推出来的：`C(l−1, z) = C(l−2, z−1) × (l−1) / z`，整除不会丢精度',
                 '对比灵神：他从第 49 位试填、一个 `comb(i, k)` 搞定；yiduobo 先定长度再填，思路更「数位」',
                 '原文已是 Python 3 可直接运行的写法（整除本来就用 `//`），未做修改'],
    ),
)
