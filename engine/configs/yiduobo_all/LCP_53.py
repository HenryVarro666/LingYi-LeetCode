TBL_N = 40   # f 表只画前 40 个 right_state（5 行 × 8 列）


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    line = S.get('_line') or 0
    ls = S.get('left_state', 0)
    rs = S.get('right_state')
    f = S.get('f')
    have = rs is not None
    lc = ((rs >> 5) ^ ls) if have else 0          # 左列新增（只能靠双列板盖）
    hl = S.get('hyper_left') if (have and line >= 26) else None
    hr = S.get('hyper_right') if (have and line >= 26) else None
    sst = S.get('single_state') if (have and line == 38) else 0
    cst = S.get('combo_state') if (have and line == 46) else 0

    # ---------- 左：两列 × 五行 的棋盘 ----------
    cs = 64
    bx, by = x0 + 80, y0 + 84
    cv.text((x0 + 14, y0 + 4), '棋盘：行 = 时刻，列 = 舱室', 22, T['muted'], bold=True)
    cv.text((bx + cs / 2, by - 12), '左列', 20, T['purple'], anchor='mb', bold=True)
    cv.text((bx + cs + 10 + cs / 2, by - 12), '右列', 20, T['cyan'], anchor='mb', bold=True)
    for k in range(5):
        Y = by + (4 - k) * cs
        cv.text((x0 + 22, Y + cs / 2), k, 20, T['dim'], anchor='mm', mono=True)
        for c in range(2):
            X = bx + c * (cs + 10)
            fill, ol = T['panel2'], T['border']
            if have and c == 0:
                if (ls >> k) & 1:
                    fill = T['blue']
                elif (lc >> k) & 1:
                    fill = T['purple']
            if have and c == 1 and (rs >> k) & 1:
                fill = T['cyan']
            if have and line == 38 and c == 1 and (sst >> k) & 1:
                fill = T['orange']
            if have and line == 46 and (cst >> (5 * (1 - c)) >> k) & 1:
                fill = T['yellow']
            cv.rect((X, Y + 3, X + cs, Y + cs - 3), fill=fill, outline=ol, width=2, r=10)
    # hyper_left / hyper_right 指针
    if hl is not None and hl >= 0:
        Y = by + (4 - hl) * cs + cs / 2
        cv.arrow((bx - 36, Y), (bx - 4, Y), T['purple'], 4, 12)
        cv.text((bx - 40, Y), 'hl', 20, T['purple'], anchor='rm', bold=True, mono=True)
    if hr is not None and hr >= 0:
        Y = by + (4 - hr) * cs + cs / 2
        X = bx + 2 * cs + 10
        cv.arrow((X + 36, Y), (X + 4, Y), T['pink'], 4, 12)
        cv.text((X + 40, Y), 'hr', 20, T['pink'], anchor='lm', bold=True, mono=True)
    yb = by + 5 * cs + 12
    if have:
        cv.text((x0 + 14, yb), f'left_state  = {ls:05b}', 20, T['blue'], mono=True, bold=True)
        cv.text((x0 + 14, yb + 28), f'right_state = {rs >> 5:05b}|{rs & 31:05b}', 20, T['cyan'], mono=True, bold=True)
        if line >= 11:
            cv.text((x0 + 14, yb + 56), f'left_change = {lc:05b}', 20, T['purple'], mono=True, bold=True)
    else:
        cv.text((x0 + 14, yb), '每个 f[left][right]', 20, T['muted'])
        cv.text((x0 + 14, yb + 28), '对应棋盘上的一种摆法', 20, T['muted'])
    cv.text((x0 + 14, yb + 90), 'hl = hyper_left，hr = hyper_right', 18, T['muted'], mono=True)

    # ---------- 右：f[left_state] 前 40 个值 ----------
    cw, ch = 50, 52
    rx = x1 - 8 * cw - 8
    cv.text((rx, y0 + 4), f'f[{ls}][right_state]（前 {TBL_N} 个）', 22, T['muted'], bold=True)
    cv.text((rx, y0 + 34), '· = 100：还没有可行方案', 18, T['dim'])
    row = f[ls] if f and isinstance(f, list) and ls < len(f) else None
    ty = y0 + 66
    for i in range(TBL_N):
        r_, c_ = divmod(i, 8)
        X, Y = rx + c_ * cw, ty + r_ * ch
        v = row[i] if row else 100
        hot = have and i == rs
        src = have and ((line == 38 and i == (rs ^ sst)) or (line == 46 and i == (rs ^ cst)))
        fill = T['panel2'] if v < 100 else T['panel']
        cv.rect((X + 2, Y + 2, X + cw - 2, Y + ch - 2), fill=fill, outline=T['pink'] if hot else (T['orange'] if src else T['border']),
                width=4 if (hot or src) else 1, r=8)
        cv.text((X + 7, Y + 5), i, 13, T['dim'], mono=True)
        cv.text((X + cw / 2, Y + ch / 2 + 5), v if v < 100 else '·', 24 if v < 100 else 20,
                T['text'] if v < 100 else T['dim'], anchor='mm', bold=True)
    yl = ty + 5 * ch + 12
    cv.text((rx, yl), '粉框 = 当前 right_state', 18, T['pink'], bold=True)
    cv.text((rx, yl + 26), '橙框 = 转移用到的旧值', 18, T['orange'], bold=True)
    cv.text((rx, yl + 58), '单列板盖 k 行：代价 k + 1', 18, T['muted'])
    cv.text((rx, yl + 84), '双列板盖 k 行：代价 k + 2', 18, T['muted'])
    cv.text((rx, yl + 116), '蓝 = left_state  紫 = 左列新增', 18, T['muted'])
    cv.text((rx, yl + 142), '青 = 右列  橙/黄 = 本次放的板', 18, T['muted'])


def _cap_rs(S, B, r):
    if 'right_state' not in S:
        return '枚举两列最终的覆盖状态 `right_state`（10 位）'
    rs = S.right_state
    base = f'`right_state = {rs}`：左列 `{rs >> 5:05b}` | 右列 `{rs & 31:05b}`'
    if rs == 0:
        return base + '（左列要盖住 `left_state`，这里成立）'
    return base


def _cap_lc(S, B, r):
    lc = (S.right_state >> 5) ^ S.left_state
    if S.right_state == 0:
        return f'`left_change = {lc:05b}`：左列==新增==的行，只能靠双列板盖'
    return f'左列新增行 `left_change = {lc:05b}`'


def _cap_hyper(S, B, r):
    hl, hr = S.hyper_left, S.hyper_right
    if S.right_state <= 1:
        head = f'`hyper_left = {hl}`（左列新增最高行），`hyper_right = {hr}`（右列最高行）：'
    else:
        head = f'`hyper_left = {hl}`，`hyper_right = {hr}`：'
    return head + (f'`{hl} > {hr}` ==成立==→ 不可达' if hl > hr else f'`{hl} > {hr}` 不成立')


def _cap_which(S, B, r):
    if S.hyper_right > S.hyper_left:
        return '最高行只在右列 → 先放==单列板=='
    return '最高行左右列都有 → 放==双列板=='


def _cap_single(S, B, r):
    k = S.length + 1
    return (f'单列板盖右列 `{k}` 行：`f[{S.left_state}][{S.right_state ^ S.single_state}] + 2 + {S.length}`'
            f' → `f[{S.left_state}][{S.right_state}]` = =={S.f[S.left_state][S.right_state]}==')


def _cap_combo(S, B, r):
    k = S.length + 1
    return (f'双列板盖两列各 `{k}` 行：`f[{S.left_state}][{S.right_state ^ S.combo_state}] + 3 + {S.length}`'
            f' → `f[{S.left_state}][{S.right_state}]` = =={S.f[S.left_state][S.right_state]}==')


CONFIG = dict(
    num='LCP 53', title='守护太空城', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状压 DP · 先预处理 f 再按列 DP',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def defendSpaceCity(self, time, position):

        f = [[100] * 1024 for _ in range(32)]

        for left_state in range(32):
            for right_state in range(1024):
                if ((right_state >> 5) & left_state) != left_state:
                    continue

                left_change = (right_state >> 5) ^ left_state
                if left_change == 0:
                    hyper_left = -1
                else:
                    hyper_left = 4
                    while (left_change & (1 << hyper_left)) == 0:
                        hyper_left -= 1

                if (right_state & 31) == 0:
                    hyper_right = -1
                else:
                    hyper_right = 4
                    while (right_state & (1 << hyper_right)) == 0:
                        hyper_right -= 1

                if hyper_left > hyper_right:
                    continue

                if hyper_left == -1 and hyper_right == -1:
                    f[left_state][right_state] = 0
                    continue

                if hyper_right > hyper_left:
                    single_state = 0
                    length = 0
                    while hyper_right > hyper_left and (right_state & (1 << hyper_right)) == (1 << hyper_right):
                        single_state |= (1 << hyper_right)
                        f[left_state][right_state] = min(f[left_state][right_state], f[left_state][right_state ^ single_state] + 2 + length)
                        hyper_right -= 1
                        length += 1
                else:
                    combo_state = 0
                    length = 0
                    while hyper_left >= 0 and (left_change & (1 << hyper_left)) == (1 << hyper_left) and (right_state & (1 << hyper_right)) == (1 << hyper_right):
                        combo_state |= (1 << (hyper_right + 5)) | (1 << hyper_right)
                        f[left_state][right_state] = min(f[left_state][right_state], f[left_state][right_state ^ combo_state] + 3 + length)
                        hyper_left -= 1
                        hyper_right -= 1
                        length += 1

        n = max(position)
        state_list = [0] * n
        for index in range(len(time)):
            state_list[position[index] - 1] |= (1 << (time[index] - 1))

        g = [[1000] * 32 for _ in range(n)]
        for state in range(32):
            g[0][state] = f[0][state]

        for index in range(1, n):
            for left_state in range(32):
                if g[index - 1][left_state] == 1000:
                    continue
                for right_state in range(1024):
                    if f[left_state][right_state] < 100 and ((right_state >> 5) & state_list[index - 1]) == state_list[index - 1]:
                        g[index][right_state & 31] = min(g[index][right_state & 31], g[index - 1][left_state] + f[left_state][right_state])

        res = 1000
        for state in range(32):
            if (state & state_list[-1]) == state_list[-1]:
                res = min(res, g[-1][state])

        return res
''',
    call='Solution().defendSpaceCity([1,2,1], [6,3,3])',
    expect=5,
    trace_limit=871, snap_maxlen=3, max_steps=44,
    truncated_caption='…… f 的预处理共 32×1024 个状态，后面同理；接着按列做 DP，快进到结束 ……',
    skip=[8, 9, 29, 31, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24, 34, 35, 36, 37, 39, 40, 42, 43, 44, 45, 47, 48, 49],
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('right_state', 'right_state', 'cyan'),
           ('hyper_left', 'hyper_left', 'purple'), ('hyper_right', 'hyper_right', 'pink')],
    captions={
        'f = [[100]': '`f[left][right]` = 左列已盖 `left`、两列最终盖成 `right` 的最小代价；`100` = 还不可达',
        'for left_state in range': '`left_state`（5 位）= 左列已被板子盖住的行',
        'for right_state in range': _cap_rs,
        'left_change = ': _cap_lc,
        'if hyper_left > hyper_right': _cap_hyper,
        27: '左列新增行比右列最高行还高 → 盖不到，跳过',
        'f[left_state][right_state] = 0': '两列都无新增 → 什么都不用放：`f[{left_state}][{right_state}] = 0`',
        'if hyper_right > hyper_left': _cap_which,
        'f[left_state][right_state] = min(f[left_state][right_state], f[left_state][right_state ^ single_state]': _cap_single,
        'f[left_state][right_state] = min(f[left_state][right_state], f[left_state][right_state ^ combo_state]': _cap_combo,
    },
    cards=dict(
        one_liner='把 5 个时刻当成 5 行，用 k×1、k×2 的板子盖住陨石，状压 DP',
        complexity='预处理 `O(32 × 1024)`，DP `O(n × 32 × 1024)`',
        problem=['陨石在 `time[i]` 时刻砸向舱室 `position[i]`，要用屏障守住',
                 '单舱屏障 2、双舱联合屏障 3，每多维持一个时刻 +1',
                 '示例：`time=[1,2,1]`，`position=[6,3,3]` → `5`'],
        quote='可以发现，这里的f在确定了left_state和right_state之后就是一个定值，那么在这里可以先使用动态规划，将f的值都预处理出来。',
        quote_src='—— yiduobo 题解原文',
        idea=['时刻 ≤ 5 → 每列是 5 位状态；板子 `k×1`、`k×2` 不能旋转、不能重叠',
              '先预处理 `f[left][right]`：从左列状态 `left` 补板，盖成两列状态 `right` 的最小代价',
              '再按舱室编号一列列做 DP：`g[i][state]` = 前 `i` 列、最后一列盖成 `state` 的最小代价'],
        after=[dict(heading='f 预处理之后的 DP（视频快进了）', lines=[
            '`g[i][right & 31] = min(g[i−1][left] + f[left][right])`',
            '条件：`right` 的高 5 位要盖住第 `i − 1` 列的所有陨石',
            '最后只保留能盖住最后一列陨石的 `state`，取 `g[-1][state]` 最小 → `5`',
        ])],
        summary=['预处理 `O(32 × 1024)`，DP `O(n × 32 × 1024)`；`n` 是最大舱室编号',
                 '外层 32 × 1024 次循环写死：视频先看开头，再跳到 `right_state = 33`（第一个双列板）',
                 '`hyper_left > hyper_right` 双列板盖不到 → 不可达；两者都是 −1 → 代价 0',
                 '易错：`f` 只在最后一列放单列板，倒数第二列的单列板在上一轮已放过'],
    ),
)
