def _path_cells(directions):
    r = c = 0
    cells = [0]
    for ch in directions:
        if ch == 'D':
            r += 1
        else:
            c += 1
        cells.append(r * 4 + c)
    return cells


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    directions = S.get('directions')
    if not directions:
        return
    cells = _path_cells(directions)
    order = {p: k + 1 for k, p in enumerate(cells)}
    n = S.get('n')
    inner = S['_inner']
    i = inner.get('i')
    cv.text((x0 + 18, y0 + 4), f'4×4 网格（绿 = 路径格 1~7，粉框 = 当前填的数位，虚线框 = 只有最后 {n or "n"} 位有数字）', 21, T['muted'], bold=True)
    cell = 78
    gx, gy = x0 + 40, y0 + 52
    for p in range(16):
        r, c = divmod(p, 4)
        X, Y = gx + c * cell, gy + r * cell
        on = p in order
        cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), fill=T['green'] if on else T['panel2'], alpha=255 if on else 255, r=8, outline=T['border'])
        cv.text((X + cell / 2, Y + cell / 2 - 4), p, 28, T['bg'] if on else T['dim'], anchor='mm', bold=True, mono=True)
        if on:
            cv.text((X + cell - 10, Y + 8), order[p], 17, T['bg'], anchor='rt', bold=True)
        if n and p >= 16 - n:
            cv.rect((X + 1, Y + 1, X + cell - 1, Y + cell - 1), outline=T['yellow'], width=2, r=9)
        if n and i is not None and p == 16 - n + i:
            cv.rect((X, Y, X + cell, Y + cell), outline=T['pink'], width=6, r=10)
    # 右侧：low / high / in_path 对齐
    hs, ls, ip = S.get('high_s'), S.get('low_s'), S.get('in_path')
    if not (n and hs and ls):
        return
    cw = min(64, (x1 - (gx + 4 * cell + 90) - 90) / n)
    sx = gx + 4 * cell + 130
    rows = [('high', hs, T['orange']), ('low', ls, T['blue']), ('在路径', ip, T['green'])]
    for k, (name, arr, col) in enumerate(rows):
        Y = gy + 20 + k * 96
        cv.text((sx - 12, Y + 28), name, 22, col, anchor='rm', bold=True)
        if arr is None:
            continue
        for j, v in enumerate(arr):
            X = sx + j * cw
            hit = i is not None and j == i
            txt = ('是' if v else '否') if name == '在路径' else str(v)
            cv.rect((X + 3, Y, X + cw - 3, Y + 56), fill=T['panel2'], r=8, outline=T['pink'] if hit else T['border'])
            cv.text((X + cw / 2, Y + 28), txt, 28 if name != '在路径' else 24, (T['green'] if v else T['dim']) if name == '在路径' else T['text'], anchor='mm', bold=True, mono=True)
    if i is not None:
        cv.text((sx, gy + 20 + 3 * 96 + 8), f'当前 i = {i}（对应网格第 {16 - n + i} 格）', 24, T['pink'], bold=True)
    if 'pre' in inner:
        cv.text((sx, gy + 20 + 3 * 96 + 44), f"pre = {inner['pre']}（路径上上一个填的数）", 24, T['cyan'], bold=True)


def _range(S, B, ret):
    bi = S['_inner']
    tag = ('受 low 约束' if bi['limit_low'] else '') + ('、' if bi['limit_low'] and bi['limit_high'] else '') + ('受 high 约束' if bi['limit_high'] else '')
    return f"`lo = {bi['lo']}`，`hi = {bi['hi']}`" + (f"（{tag}）" if tag else '（都不受约束，0~9 随便填）')


def _start(S, B, ret):
    if S.in_path[S.i]:
        return (f"第 {S.i} 位==在路径中==：必须 `≥ pre = {S.pre}`，所以从 `max(lo, pre) = max({S.lo}, {S.pre}) = {S.start}` 开始填")
    return f"第 {S.i} 位不在路径中：没有大小限制，从 `lo = {S.lo}` 开始填"


def _call(S, B, ret):
    bi = B['_inner']
    d, i = bi['d'], bi['i']
    onp = B.in_path[i]
    if S.i != i:
        return f"递归进入第 {i + 1} 位：`pre = {d if onp else bi['pre']}`，limit_low = {bi['limit_low'] and d == bi['lo']}，limit_high = {bi['limit_high'] and d == bi['hi']}"
    return (f"第 {i} 位填 `d = {d}`：" + (f"在路径中 → 下一位的 `pre` 更新为 {d}" if onp else f"不在路径中 → `pre` 仍是 {bi['pre']}")
            + f"；limit_low = {bi['limit_low'] and d == bi['lo']}，limit_high = {bi['limit_high'] and d == bi['hi']}")


def _for(S, B, ret):
    bi = B['_inner']
    if 'd' not in bi:
        if bi['start'] > bi['hi']:
            return f"`range({bi['start']}, {bi['hi'] + 1})` 是空的：下限 {bi['start']} 已经超过上限 {bi['hi']} → 一个数也填不了，返回 0"
        return f"枚举第 `{bi['i']}` 位填的数字 `d`：从 `{bi['start']}` 到 `{bi['hi']}`"
    if bi['d'] == bi['hi']:
        return f"子问题返回，累计 `res = {bi['res']}`；`d` 已枚举到 `hi = {bi['hi']}`"
    return f"子问题返回，累计 `res = {bi['res']}`；换下一个 `d = {bi['d'] + 1}`"


_I = lambda S: S['_inner'].get('i')

CONFIG = dict(
    num=3906, title='统计网格路径中好整数的数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='上下界数位 DP · pre 只记路径上的数',
    tags=['灵神题单', '难度分 2160'],
    code='''
class Solution:
    def countGoodIntegersOnPath(self, l: int, r: int, directions: str) -> int:
        high_s = list(map(int, str(r)))  # 避免在 dfs 中频繁调用 int()
        n = len(high_s)
        low_s = list(map(int, str(l).zfill(n)))  # 补前导零，让 len(low_s) == n

        in_path = [False] * n
        in_path[-1] = True  # 终点一定在路径中
        pos = n - 1
        for d in reversed(directions):
            pos -= 1 if d == 'R' else 4  # 倒着往上相当于往左数 4 个位置
            if pos < 0:  # 只需要对网格图的后 n 个格子做标记
                break
            in_path[pos] = True  # 标记在路径中的格子

        @cache
        def dfs(i: int, pre: int, limit_low: bool, limit_high: bool) -> int:
            if i == n:  # 成功到达终点
                return 1  # 找到了一个好整数

            lo = low_s[i] if limit_low else 0
            hi = high_s[i] if limit_high else 9

            res = 0
            # 如果当前位置在路径中，那么当前位置填的数必须 >= pre
            start = max(lo, pre) if in_path[i] else lo
            for d in range(start, hi + 1):
                res += dfs(i + 1,
                           d if in_path[i] else pre,
                           limit_low and d == lo,
                           limit_high and d == hi)
            return res

        return dfs(0, 0, True, True)
''',
    call='Solution().countGoodIntegersOnPath(108, 121, "DDRRDR")',
    expect=11,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='calls', h=220),
    ],
    watch=[('i', _I, 'pink'), ('pre', lambda S: S['_inner'].get('pre'), 'cyan'), ('start', lambda S: S['_inner'].get('start'), 'blue'),
           ('hi', lambda S: S['_inner'].get('hi'), 'orange'), ('res', lambda S: S['_inner'].get('res'), 'green')],
    skip=['n = len(high_s)', 'res = 0', 'in_path = [False]', 'd if in_path[i] else pre,', 'limit_low and d == lo,', 'limit_high and d == hi)',
          'pos = n - 1', 'high_s = list'],
    max_steps=54,
    captions={
        'low_s = list': '`high_s = {high_s}`；`low` 补前导零成 `{low_s}`：两个数一样长，才能逐位比较',
        'break': '`break`：再往前的数位都是前导零，不用标记',
        'in_path[-1] = True': '最后一格（右下角）一定在路径里：`in_path = {in_path}`',
        'for d in reversed': '倒着走路径：从终点往回退，`R` 退一格，`D` 退 4 格（网格一行 4 个数位）',
        'pos -= 1 if': '`{d}`：`pos` 退到 `{pos}`',
        'if pos < 0': lambda S, B, r: (f"`pos = {S.pos} < 0`：已经退到只有前导零的区域，不用再标记 → break" if S.pos < 0 else f"`pos = {S.pos}` ≥ 0，这一格还在 {S.n} 位数字内"),
        'in_path[pos] = True': '标记：数位 `{pos}` 在路径中 → `in_path = {in_path}`',
        'return dfs(0, 0': '入口：`dfs(0, 0, True, True)`，`pre = 0` 保证路径上第一个数不受限，同时受 low、high 约束',
        'if i == n': lambda S, B, r: ('`i == n`：每一位都填完，路径上的数非递减 → ==找到一个好整数== 返回 1' if B['_inner'].get('i') == S.n
                                      else f"`i = {B['_inner']['i']}`，还没填完"),
        'lo = low_s': '`lo`：受 low 约束时，这一位不能比 `low_s[{i}]` 小',
        'hi = high_s': _range,
        'start = max': _start,
        'for d in range': _for,
        'res += dfs': _call,
        'return 1': '返回 1：这个数满足条件',
        'return res': lambda S, B, ret: f'`dfs({S.i}, {S.pre}, {S.limit_low}, {S.limit_high})` = ==`{ret}`==，记忆化保存',
    },
    cards=dict(
        one_liner='网格路径 = 数位里固定的几个位置：只要这些位非递减',
        complexity='时间 `O(D²log r)`，空间 `O(D log r)`',
        problem=['16 位数字（前补 0）按行填进 4×4 网格，从左上角按 `directions` 走 6 步',
                 '路径上 7 个数若非递减，该整数是好整数；求 `[l, r]` 内好整数个数',
                 '本视频：`[108, 121]`，`DDRRDR` → `11`（只看末 3 位，路径占其中 2 位）'],
        quote='如果 i 在路径中，那么 d 从 max(lo, pre) 开始枚举，从而保证路径上的数字是非递减的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`directions` 固定，路径经过哪些数位也固定：先标出 `in_path`',
              '`pre` 只记路径上上一个数，不在路径上的数位随便填',
              '`lo` / `hi` 来自 low、high 的约束，和 3791 同一套上下界数位 DP 模板',
              '只对网格后 `n` 个格子标记：更靠前的数位都是前导零'],
        summary=['时间 `O(D²log r)`：状态 `O(D log r)`，每个状态枚举 `D` 个数',
                 '倒着标记路径：`R` 退 1 格，`D` 退 4 格，退出数字范围就停',
                 '终点一定在路径中，所以 `in_path[-1] = True`',
                 '本视频用方法一（数位 DP）；方法二用组合数，`O(log r)`，思路同 3519',
                 '同类题：3519. 统计逐位非递减的整数'],
    ),
)
