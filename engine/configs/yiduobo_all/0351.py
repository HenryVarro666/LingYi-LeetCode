import math


NROWS = 6            # 表里画 state = 0 .. 5（视频只演示前面这几个状态）
SHOW_LINE_LAST = 41  # cnt_list 那一行


def _key_xy(k, x0, y0, c):
    return x0 + (k % 3) * c + c / 2, y0 + (k // 3) * c + c / 2


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    line = S.get('_line')
    live = 'state' in S
    state = S.get('state', 0)
    last = S.get('last') if live and line is not None and line >= 27 else None
    in_pre = live and line is not None and 32 <= line <= 39 and 'pre_last' in S
    pre_last = S.get('pre_last') if in_pre else None
    cn = S.get('check_num')
    mid = None
    if in_pre and last is not None and pre_last is not None and pre_last != last and cn:
        m = cn[pre_last][last]
        mid = m if m != -1 else None

    # ---------- 左：手势键盘 ----------
    kc = 104
    kx, ky = x0 + 30, y0 + 58
    cv.text((x0 + 18, y0 + 4), '手势键盘（数字 = 位下标 + 1）', 22, T['muted'], bold=True)
    if cn and not live:  # 开头：登记「会跨过别的键」的 8 对走法
        for a in range(9):
            for b in range(a + 1, 9):
                if cn[a][b] != -1:
                    pa, pb = _key_xy(a, kx, ky, kc), _key_xy(b, kx, ky, kc)
                    cv.dashed(pa, pb, T['yellow'], 3, dash=10, gap=8)
    for k in range(9):
        cx, cy = _key_xy(k, kx, ky, kc)
        r = 38
        visited = live and (state >> k) & 1
        fill, tc, ol = T['panel2'], T['dim'], T['border']
        if visited:
            fill, tc, ol = T['cyan'], T['bg'], None
        if k == last:
            fill, tc, ol = T['pink'], T['bg'], None
        if k == pre_last and k != last:
            fill, tc, ol = T['orange'], T['bg'], None
        if not live:
            tc = T['muted']
        cv.rect((cx - r, cy - r, cx + r, cy + r), fill=fill, outline=ol, width=2, r=r)
        cv.text((cx, cy), k + 1, 40, tc, anchor='mm', bold=True)
        if k == mid:
            cv.rect((cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8), outline=T['yellow'], width=5, r=r + 8)
    if pre_last is not None and last is not None and pre_last != last:
        (ax, ay), (bx, by) = _key_xy(pre_last, kx, ky, kc), _key_xy(last, kx, ky, kc)
        d = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / d, (by - ay) / d
        cv.arrow((ax + ux * 44, ay + uy * 44), (bx - ux * 46, by - uy * 46), T['orange'], 6, 18)
    # 状态说明
    ty = ky + 3 * kc + 24
    if pre_last is not None and last is not None and pre_last != last:
        cv.text((x0 + 30, ty), f'走法：{pre_last + 1} → {last + 1}', 28, T['orange'], bold=True)
        if mid is None:
            cv.text((x0 + 30, ty + 40), '中间不跨过任何键', 24, T['muted'])
        else:
            ok = ((state ^ (1 << last)) >> mid) & 1
            cv.text((x0 + 30, ty + 40), f'要跨过键 {mid + 1}', 24, T['yellow'], bold=True)
            if line >= 37:
                cv.text((x0 + 30, ty + 76), f'键 {mid + 1} 已按过 → 可以走' if ok else f'键 {mid + 1} 没按过 → 不能走',
                        24, T['green'] if ok else T['red'], bold=True)
    elif live:
        cv.text((x0 + 30, ty), '青 = state 里已按的键，粉 = last', 22, T['muted'])
    elif cn:
        cv.text((x0 + 30, ty), '黄色虚线 = 会跨过中间键的走法', 22, T['yellow'])

    # ---------- 右上：state / pre_state 的二进制 ----------
    rx = x0 + 410
    bw = 48

    def strip(y, name, val, color, hot=None):
        cv.text((rx, y), name, 22, color, bold=True, mono=True)
        for j in range(9):          # 左边是高位
            k = 8 - j
            X = rx + 140 + j * bw
            on = (val >> k) & 1
            cv.rect((X, y - 6, X + bw - 6, y + 36), fill=color if on else T['panel2'],
                    outline=T['yellow'] if k == hot else T['border'], width=4 if k == hot else 1, r=6)
            cv.text((X + (bw - 6) / 2, y + 15), on, 24, T['bg'] if on else T['dim'], anchor='mm', bold=True, mono=True)
            cv.text((X + (bw - 6) / 2, y + 40), k + 1, 16, T['dim'], anchor='mt', mono=True)

    cv.text((rx, y0 + 4), '二进制：第 k 位 = 数字 k+1 是否已按（下面小字是数字）', 22, T['muted'], bold=True)
    strip(y0 + 52, 'state', state if live else 0, T['cyan'])
    if last is not None:
        strip(y0 + 128, 'pre_state', state ^ (1 << last), T['blue'], hot=mid)
    else:
        cv.text((rx, y0 + 134), 'pre_state：去掉 last 之后的状态', 22, T['dim'])

    # ---------- 右下：f 表 ----------
    f = S.get('f')
    nl = S.get('num_list')
    fin = bool(last is not None and (line == 41 or (line == 27 and B.get('last') == last and nl and nl[-1] == last)))
    ty0 = y0 + 214
    cv.text((rx, ty0), 'f[state][last]（行 = state，列 = last 的数字）', 22, T['muted'], bold=True)
    hy = ty0 + 34
    cw, rh, lw = 52, 40, 128
    for k in range(9):
        cv.text((rx + lw + k * cw + cw / 2, hy + 12), k + 1, 22, T['pink'] if k == last else T['muted'], anchor='mm', bold=True)
    for s in range(NROWS):
        Y = hy + 30 + s * rh
        cur = live and s == state
        if cur:
            cv.rect((rx - 4, Y, rx + lw + 9 * cw + 2, Y + rh - 4), fill=T['cyan'], alpha=34, r=8)
        cv.text((rx + 4, Y + rh / 2 - 2), f'{s:>2} {s:09b}', 20, T['cyan'] if cur else T['muted'], anchor='lm', mono=True)
        row = f[s] if f and s < len(f) else None
        if not isinstance(row, list):
            if row is not None:   # f[0] = 1
                cv.text((rx + lw + 4, Y + rh / 2 - 2), f'f[0] = {row}：什么都没按，算 1 种', 20, T['green'], anchor='lm', bold=True)
            continue
        for k in range(9):
            X = rx + lw + k * cw
            if not (s >> k) & 1:
                cv.text((X + cw / 2, Y + rh / 2 - 2), '·', 22, T['dim'], anchor='mm')
                continue
            v = row[k]
            hot = cur and k == last
            if not live:
                computed = False
            elif s < state:
                computed = True
            elif cur and last is not None:
                computed = k < last or (k == last and fin)
            else:
                computed = False
            if hot:
                cv.rect((X + 2, Y, X + cw - 2, Y + rh - 4), outline=T['pink'], width=3, r=6)
            if not computed and not (hot and line >= 30):
                cv.text((X + cw / 2, Y + rh / 2 - 2), '?', 22, T['dim'], anchor='mm')
                continue
            col = T['red'] if (v == 0 and computed) else T['text']
            cv.text((X + cw / 2, Y + rh / 2 - 2), v, 24, col, anchor='mm', bold=True)
    # cnt_list
    cl = S.get('cnt_list')
    if cl:
        yy = hy + 30 + NROWS * rh + 10
        cv.text((rx, yy), 'cnt_list[k] = 恰好按 k 个键的方案数：', 22, T['muted'], bold=True)
        cv.text((rx, yy + 34), '  '.join(f'{k}:{cl[k]}' for k in range(1, 5)), 26, T['green'], bold=True, mono=True)


def _ended(S, B):
    return 'last' in B and S.last == B.last and S.last == S.num_list[-1]


def _cap_last(S, B, r):
    if _ended(S, B):
        return f'`state = {S.state}` 的每个 `last` 都算完 → 汇总进 `cnt_list[{len(S.num_list)}]`'
    return f'假设最后按的是键 `{S.last + 1}`；去掉它，前面按过的是 `pre_state = {S.state ^ (1 << S.last):09b}`'


def _cap_prelast(S, B, r):
    if 'pre_last' in B and S.pre_last == B.pre_last:
        return '倒数第二个键都试完了'
    if S.pre_last == S.last:
        return f'`pre_last` 就是 `last`（键 {S.last + 1}）：不能连按同一个键 → 跳过'
    return f'假设倒数第二个按的是键 `{S.pre_last + 1}`'


def _cap_chk(S, B, r):
    a, b = S.pre_last, S.last
    m = S.check_num[a][b]
    if m == -1:
        return f'`{a + 1} → {b + 1}` 不跨过任何键 → 直接可走'
    return f'`{a + 1} → {b + 1}` 会跨过键 `{m + 1}` → 要检查它按过没有'


def _cap_ok(S, B, r):
    m = S.check_num[S.pre_last][S.last]
    if (S.pre_state & S.check_state) != S.check_state:
        return f'`pre_state` 里没有键 `{m + 1}` → ==这一步非法==，跳过'
    return f'键 `{m + 1}` 已按过 → 可以跨过去'


def _cap_cnt(S, B, r):
    k = len(S.num_list)
    return f'把 `f[{S.state}][{S.last}]` 累加进 `cnt_list[{k}]`（按了 {k} 个键的方案数）'


CONFIG = dict(
    num=351, title='安卓系统手势解锁', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='状压 DP · f[state][last]',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def numberOfPatterns(self, m, n):

        max_state = 512
        f = [[0] * 9 for _ in range(max_state)]

        f[0] = 1
        cnt_list = [0] * 10

        check_num = [[-1] * 9 for _ in range(9)]

        check_num[0][2] = check_num[2][0] = 1
        check_num[0][6] = check_num[6][0] = 3
        check_num[0][8] = check_num[8][0] = 4
        check_num[1][7] = check_num[7][1] = 4
        check_num[2][6] = check_num[6][2] = 4
        check_num[2][8] = check_num[8][2] = 5
        check_num[3][5] = check_num[5][3] = 4
        check_num[6][8] = check_num[8][6] = 7

        for state in range(1, 512):
            num_list = []
            for num in range(9):
                if (state & (1 << num)) == (1 << num):
                    num_list.append(num)

            for last in num_list:
                pre_state = state ^ (1 << last)
                if pre_state == 0:
                    f[state][last] += f[0]
                else:
                    for pre_last in num_list:
                        if pre_last == last:
                            continue
                        if check_num[pre_last][last] != -1:
                            check_state = (1 << check_num[pre_last][last])
                            if (pre_state & check_state) != check_state:
                                continue
                        f[state][last] += f[pre_state][pre_last]

                cnt_list[len(num_list)] += f[state][last]

        return sum(cnt_list[m : n + 1])
''',
    call='Solution().numberOfPatterns(1, 2)',
    expect=65,
    trace_limit=718, snap_maxlen=16, max_steps=90,
    truncated_caption='…… 一共 511 个 `state`，后面的同理，快进到结束 ……',
    skip=[12, 13, 14, 15, 16, 17, 18, 22, 23, 24, 25, 28, 29, 33, 34, 36, 41],
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('state', 'state', 'cyan'), ('last', 'last', 'pink'), ('pre_state', 'pre_state', 'blue'),
           ('pre_last', 'pre_last', 'orange')],
    captions={
        'max_state = 512': '9 个键，每个键「按过 / 没按过」→ 共 `2^9 = 512` 种状态，用一个二进制数 `state` 表示',
        'f = [[0]': '`f[state][last]` = 按过 `state` 里这些键、且==最后一个==按 `last` 的合法手势数',
        'f[0] = 1': '空状态记 1 种：只有「第一个键」会用到 `f[0]`',
        'cnt_list = [0] * 10': '`cnt_list[k]` = 恰好按 `k` 个键的合法手势总数（最后按 `m ~ n` 汇总）',
        'check_num = [[': '`check_num[a][b]` = 从 `a` 走到 `b` 会==跨过==的键；`-1` 表示不跨过',
        'check_num[6][8]': '登记 8 对「隔着一个键」的走法：如 `1→3` 跨过 `2`，`1→9` 跨过 `5`（数字 = 下标 + 1）',
        'for state in range': lambda S, B, r: (f'枚举状态 `state = {S.state}`（二进制 `{S.state:09b}`）= 按过键 '
                                               f'{[k + 1 for k in range(9) if (S.state >> k) & 1]}'),
        'for last in num_list': _cap_last,
        'f[state][last] += f[0]': '去掉 `last` 后为空：只按这一个键，1 种 → `f[{state}][{last}]` = =={f[state][last]}==',
        'for pre_last in num_list': _cap_prelast,
        'if check_num[pre_last][last] != -1': _cap_chk,
        'if (pre_state & check_state)': _cap_ok,
        38: '`continue`：不能从 `f[{pre_state}][{pre_last}]` 转移',
        'f[state][last] += f[pre_state][pre_last]': '合法：并入 `f[{pre_state}][{pre_last}] = {f[pre_state][pre_last]}` → `f[{state}][{last}]` = =={f[state][last]}==',
    },
    cards=dict(
        one_liner='用二进制记「按过哪些键」，再记最后一个键，枚举上一个键转移',
        complexity='时间 `O(2^9 × 9 × 9)`，空间 `O(2^9 × 9)`',
        problem=['3×3 键盘，按 `m ~ n` 个互不相同的键连成手势',
                 '从 `a` 走到 `b` 若==跨过==别的键，那个键必须已按过',
                 '示例：`m = 1, n = 2` → `65`（1 键 9 种 + 2 键 56 种）'],
        quote='令f[state][last]表示当前访问过state这些数字，且最后一个数字为last时的合法手势数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['`state` 每一位表示一个键按没按，`last` 记最后按的键',
              '去掉 `last` 得到 `pre_state`，枚举上一个键 `pre_last` 转移',
              '若 `pre_last → last` 跨过中间键，中间键必须在 `pre_state` 里'],
        summary=['时间 `O(2^9 × 9 × 9)`，空间 `O(2^9 × 9)`；最后对 `cnt_list[m..n]` 求和',
                 '`state` 要从 1 枚举到 511，写死的大循环；视频只演示 1 ~ 5，其余快进',
                 '`state = 5`（键 1、3）跨过键 2 且没按 → 0 种；`state = 7` 就合法了',
                 '易错：跨过的键要在 `pre_state` 里查；`f[0] = 1` 把整行换成了整数',
                 '原文本身是 Python 3 可运行的写法，没有改动'],
    ),
)
