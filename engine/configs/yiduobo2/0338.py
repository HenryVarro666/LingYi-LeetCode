NUM = 5
SLOTS = 8
BITS = 3


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'f[i] = i 的二进制里 1 的个数（橙 = 这一轮新补上的最高位 1）', 24, T['muted'], bold=True)
    f = S.get('f')
    if f is None:
        return
    bf = B.get('f') or []
    grew = len(f) > len(bf) and len(bf) > 0
    h = len(bf) if grew else None
    at_ret = S.get('_line') == 7
    w = (x1 - x0 - 40) / SLOTS
    cw = w - 14
    top = y0 + 60
    ch = 200
    for i in range(SLOTS):
        X = x0 + 20 + i * w + 7
        known = i < len(f)
        new = grew and i >= h
        cut = at_ret and i > NUM
        fill = T['panel2'] if known else T['bg']
        cv.rect((X, top, X + cw, top + ch), fill=fill, r=12,
                outline=T['yellow'] if new else T['border'], width=3 if new else 1)
        c_txt = T['dim'] if (cut or not known) else T['text']
        cv.text((X + cw / 2, top + 14), f'i = {i}', 22, T['muted'] if not cut else T['dim'], anchor='mt', bold=True)
        bits = format(i, f'0{BITS}b')
        fs = 34
        bw = cv.tlen('0', fs, mono=True)
        bx = X + cw / 2 - bw * BITS / 2
        for k, b in enumerate(bits):
            pos = BITS - 1 - k  # 第几位（从右往左，0 起）
            col = T['dim'] if not known else (T['text'] if b == '1' else T['muted'])
            if new and (1 << pos) == h:
                col = T['orange']
            if cut:
                col = T['dim']
            cv.text((bx + k * bw, top + 62), b, fs, col, anchor='la', bold=True, mono=True)
        v = str(f[i]) if known else '?'
        cv.text((X + cw / 2, top + ch - 20), f'f = {v}', 28, T['green'] if new else c_txt, anchor='mb', bold=True)
        if cut:
            cv.line([(X + 8, top + ch - 8), (X + cw - 8, top + 8)], T['red'], 3)
    # 倍增箭头：f[i + h] = f[i] + 1
    if grew:
        base = top + ch + 8
        for i in range(h, len(f)):
            j = i - h
            xa = x0 + 20 + j * w + 7 + cw / 2
            xb = x0 + 20 + i * w + 7 + cw / 2
            cv.arc_arrow((xa, base), (xb, base), -(30 + (xb - xa) * 0.12), T['green'], 3, 11)
        cv.text((x0 + 30, base + 90), f'f[i + {h}] = f[i] + 1（i = 0 ~ {h - 1}）', 26, T['green'], bold=True)


def _info(S):
    f = S.get('f')
    if f is None:
        return ''
    n = len(f)
    if S.get('_line') == 7:
        return f'`f` 已有 {n} 个，只要前 `num + 1 = {NUM + 1}` 个'
    return f'目前 `len(f) = {n}`：已知 `0 ~ {n - 1}` 的答案'


def _while_cap(S, B, ret):
    n = len(S.f)
    if n < NUM + 1:
        return f'`len(f) = {n} < num + 1 = {NUM + 1}` → 还不够，继续倍增'
    return f'`len(f) = {n} ≥ num + 1 = {NUM + 1}` → 够长了，停止'


def _extend_cap(S, B, ret):
    h = len(B.f)
    k = h.bit_length()
    return (f'`{h} ~ {2 * h - 1}` 就是 `0 ~ {h - 1}` 在第 {k} 位补一个 1 → '
            f'`{B.f}` 各加 1 接在后面：`f = {S.f}`')


CONFIG = dict(
    num=338, title='比特位计数', difficulty='Easy', category='技巧',
    author='yiduobo', technique='按 2 的幂倍增',
    tags=['热题173'],
    code='''
class Solution(object):
    def countBits(self, num):
        f = [0]
        while len(f) < num + 1:
            f.extend([x + 1 for x in f])

        return f[:num + 1]
''',
    call=f'Solution().countBits({NUM})',
    expect=[0, 1, 1, 2, 1, 2],
    views=[
        dict(type='text', h=56, fn=_info, size=26),
        dict(type='custom', draw=_draw, h=420),
    ],
    watch=[('num', 'num'), ('len(f)', 'len(f)', 'yellow'), ('f', 'f', 'green')],
    captions={
        'f = [0]': '`f[i]` 表示 i 的二进制中 1 的个数：先设 `f = [0]`（0 里没有 1）',
        'while len(f)': _while_cap,
        'f.extend': _extend_cap,
        'return': '只要 `0 ~ num` 的答案：返回 `f[:{num + 1}] = {ret}`',
    },
    cards=dict(
        one_liner='后一半就是前一半在最高位补了个 1：f 每轮翻倍，新的一半 = 旧的各加 1',
        complexity='时间 `O(n)`，空间 `O(n)`（不计答案为 `O(1)`）',
        problem=['给你整数 `n`，对 `0 ≤ i ≤ n` 的每个 `i`，计算它二进制里 ==1 的个数==',
                 '返回长度为 `n + 1` 的数组',
                 '示例：`n = 2` → `[0,1,1]`；`n = 5` → `[0,1,1,2,1,2]`（本视频）'],
        before=[dict(heading='先看几个小数字', lines=[
            '`0 → 000`，`1 → 001`，`2 → 010`，`3 → 011`',
            '`4 → 100`，`5 → 101`，`6 → 110`，`7 → 111`',
            '`2、3` 是 `0、1` 把第 2 位变成 1；`4~7` 是 `0~3` 把第 3 位变成 1'])],
        quote='对于0、1、2、...、2^k - 1与2^k、2^k +1、2^k + 2、...、2^(k + 1) - 1，如果用后面的数减去前面的数，都刚好是2^k，对应到二进制上就是==从右往左数第(k + 1)位从0变成了1==。',
        quote_src='—— yiduobo 题解原文',
        idea=['所以 `f[2^k + i] = f[i] + 1`（`0 ≤ i < 2^k`）',
              '从 `f = [0]` 开始，每轮把整个 `f` 各加 1 接到末尾，长度 `1 → 2 → 4 → 8`',
              '长度够 `num + 1` 就停，最后截取 `f[:num + 1]`'],
        result='运行结束，返回 `[0,1,1,2,1,2]`：多算的 `6、7` 被截掉',
        summary=['时间 `O(n)`：每轮遍历 `1, 2, 4, …, 2^k` 个，`2^(k+1) ≥ n`，总和不超过 `2n`',
                 '易错：最后要截取 `f[:num + 1]`，倍增可能多算到 `2n` 附近',
                 '另一种常见写法：`f[i] = f[i >> 1] + (i & 1)` 或 `f[i] = f[i & (i - 1)] + 1`',
                 '原文为 Python 2 风格，只删去了 docstring，代码未改'],
    ),
)
