def _idx(S):
    """答案是 x 从高到低第几位（0 开始）；仅在第 14 行之后有意义"""
    line, k = S.get('_line'), S['res_len']
    if line in (14, 15):
        return S['n']
    stripped = k - len(str(S['res']))
    return k - (S['n'] + stripped) - 1


def _orig(S):
    if 'res' not in S:
        return S.get('n')
    line = S.get('_line')
    base = S['prev_cnt'] + 1
    if line in (11, 12, 13):
        return S['n'] + base
    return base + S['offset'] * S['res_len'] + _idx(S)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'prev_cnt' not in S:
        return
    line = S.get('_line')
    n0 = _orig(S)
    cv.text((x0 + 18, y0 + 4), f'f[k]：1 位数到 k 位数一共有多少个数字（求第 {n0} 个数字）', 23, T['muted'], bold=True)
    k = S.get('res_len', 1)
    y = y0 + 46
    tot = 0
    for kk in range(1, 5):
        c = 9 * 10 ** (kk - 1) * kk
        tot += c
        Y = y + (kk - 1) * 62
        known = kk <= k and 'cnt' in S
        cur = kk == k and 'cnt' in S
        fill = (70, 60, 25) if cur else ((30, 70, 45) if known else T['panel2'])
        cv.rect((x0 + 30, Y, x1 - 30, Y + 52), fill=fill, r=10, outline=T['yellow'] if cur else T['border'],
                width=3 if cur else 1)
        cv.text((x0 + 48, Y + 26), f'{kk} 位数', 24, T['yellow'] if cur else (T['green'] if known else T['dim']),
                anchor='lm', bold=True)
        cv.text((x0 + 150, Y + 26), f'{kk} × 9 × 10^{kk - 1} = {c} 个数字', 22,
                T['text'] if known else T['dim'], anchor='lm', mono=True)
        cv.text((x1 - 50, Y + 26), f'f[{kk}] = {tot}', 22, T['text'] if known else T['dim'], anchor='rm', mono=True, bold=True)
    y += 4 * 62 + 8
    if 'res' not in S:
        cv.rich(x0 + 30, y, f'`prev_cnt = f[{k - 1}] = {S["prev_cnt"]}`，`cnt = f[{k}] = {S.get("cnt", "?")}`，目标 `n = {S["n"]}`',
                x1 - x0 - 60, size=26)
        return
    res, n = S['res'], S['n']
    if line in (11, 12, 13):
        cv.rich(x0 + 30, y, f'`n = {n}`：在所有 {k} 位数的数字里==排第 {n} 个==（从 0 数）', x1 - x0 - 60, size=26)
        y += 52
        if 'offset' in S:
            cv.rich(x0 + 30, y, f'`offset = {n} // {k} = {S["offset"]}`：落在第 {S["offset"]} 个 {k} 位数里', x1 - x0 - 60, size=26)
        return
    idx = _idx(S)
    full = S['res'] if line in (14, 15) else None
    x_full = 10 ** (k - 1) + S['offset']
    cv.rich(x0 + 30, y, f'所在的数 `{10 ** (k - 1)} + offset = {x_full}`，要它从高到低第 `{idx}` 位', x1 - x0 - 60, size=26)
    y += 56
    s = str(x_full)
    cw = 70
    sx = x0 + 60
    shown = str(res) if line not in (14, 15) else s
    if line == 14:
        shown = str(res)  # res 还没加 offset
    for i, ch in enumerate(s):
        X = sx + i * cw
        alive = line in (14, 15) or i < len(str(res))
        hit = i == idx
        fill = T['yellow'] if hit else (T['panel2'] if alive else T['bg'])
        cv.rect((X, y, X + cw - 8, y + 66), fill=fill, r=10, outline=T['border'])
        cv.text((X + (cw - 8) / 2, y + 33), ch, 34, T['bg'] if hit else (T['text'] if alive else T['dim']),
                anchor='mm', bold=True, mono=True)
    if line in (16, 18, 19, 20, 22):
        cv.text((sx + len(s) * cw + 16, y + 33), f'res = {res}，还要去掉末尾 {n} 位', 24, T['cyan'], anchor='lm')


CONFIG = dict(
    num=400, title='第 N 位数字', difficulty='Medium', category='数学',
    author='yiduobo', technique='找规律 · 累计数字个数 f[k]',
    tags=['字节30天'],
    code='''
class Solution(object):
    def findNthDigit(self, n):
        prev_cnt = 0
        cnt = 9
        res_len = 1
        while cnt < n:
            res_len += 1
            prev_cnt = cnt
            cnt += 9 * (10 ** (res_len - 1)) * res_len

        n -= prev_cnt + 1
        res = 10 ** (res_len - 1)
        offset = n // res_len
        n %= res_len
        res += offset
        n = res_len - n - 1

        while n:
            n -= 1
            res //= 10

        return res % 10
''',
    call='[Solution().findNthDigit(11), Solution().findNthDigit(193)]',
    expect=[0, 1],
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('n', 'n', 'yellow'), ('prev_cnt', 'prev_cnt'), ('cnt', 'cnt'), ('res_len', 'res_len', 'cyan'),
           ('offset', 'offset'), ('res', 'res', 'green')],
    captions={
        'prev_cnt = 0': '`prev_cnt`、`cnt`：1 位数到 `res_len−1`、`res_len` 位数一共有多少个数字（即 f）',
        'cnt = 9': '1 位数只有 1~9，共 `9` 个数字',
        'while cnt < n': lambda S, B, ret: (
            f'`f[{B.res_len}] = {B.cnt} < n = {B.n}`：{B.res_len} 位数的数字不够数到第 {B.n} 个 → 再加一组'
            if B.cnt < B.n else f'`f[{B.res_len}] = {B.cnt} ≥ n = {B.n}`：==第 {B.n} 个数字落在 {B.res_len} 位数里=='),
        'res_len += 1': '看 `{res_len}` 位数',
        'prev_cnt = cnt': '`prev_cnt = f[{res_len - 1}] = {prev_cnt}`',
        'cnt += 9': '{res_len} 位数共 `{res_len} × 9 × 10^{res_len - 1} = {cnt - prev_cnt}` 个数字 → `cnt = f[{res_len}] = {cnt}`',
        'n -= prev_cnt + 1': '`n − f[k−1] − 1 = {n}`：在所有 {res_len} 位数的数字里==排第 {n} 位==（从 0 数）',
        'res = 10 **': '{res_len} 位数从 `{res}` 开始',
        'offset = n // res_len': '每个数 {res_len} 位：`offset = {n} // {res_len} = {offset}`，是从 `{res}` 开始数的第 {offset} 个数',
        'n %= res_len': '`n %= {res_len}` → `{n}`：答案是这个数==从高到低==第 {n} 位',
        'res += offset': '这个数是 `{res}`',
        'n = res_len - n - 1': '要用「除 10」从低位取，所以换成==从低到高==：还要去掉末尾 `{res_len} − {B.n} − 1 = {n}` 位',
        'while n:': lambda S, B, ret: (f'`n = {B.n}`：还要去掉 {B.n} 位' if B.n else '`n = 0`：要的那一位已经在个位了'),
        'res //= 10': '去掉末位：`res = {res}`',
        'return res % 10': '个位就是答案：`{res} % 10` = =={ret}==',
    },
    skip=['n -= 1', 'res_len = 1'],
    cards=dict(
        one_liner='算出 1 位数到 k 位数的数字总数，定位到第几个 k 位数的第几位',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['在无限序列 `1 2 3 4 5 6 7 8 9 10 11 …` 中，找第 `n` 位上的数字',
                 '示例：`n = 3` → `3`；`n = 11` → `0`（是 10 的 `0`）',
                 '本视频：`n = 11` 和 `n = 193`'],
        quote='设1位数到k位数的数字总和为f[k]，那么==通过f[k]就能知道第N个数字的位数==，通过N-f[k]-1则可以知道N在所有k位数中的排位p，即从10^(k-1)开始数的第p个数字。',
        quote_src='—— yiduobo 题解原文',
        idea=['一位数 9 个数字，两位数 `2×90 = 180` 个，k 位数 `k·9·10^(k−1)` 个',
              '累加到 `f[k] ≥ N` 就知道位数 k；`p = N − f[k−1] − 1` 是在 k 位数里的排位',
              '`p // k` 定位是哪个数，`p % k` 是从高往低第几位；转成从低往高后不断除 10'],
        result='`n = 11` → `0`，`n = 193` → `1` ✓',
        summary=['时间 `O(log n)`：位数最多十来组',
                 '易错：p 是从高位数的，用「除 10、模 10」取数字时要先换成从低位数的位置',
                 '原文为 Python 2 写法，`n / res_len`、`res /= 10` 的整除已改为 `//`、`//=`；删去了文档字符串',
                 '对比灵神：灵神 `n -= 1` 后整组减掉，再用 `10 ** (…)` 一步取出那一位'],
    ),
)
