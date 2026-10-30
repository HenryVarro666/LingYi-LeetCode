def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cp = S.get('checkpoints')
    inner = S['_inner']
    lv = inner.get('level')
    cv.text((x0 + 18, y0 + 4), '4×4 网格（绿 = 路径格，粉框 = 当前填的数位）', 21, T['muted'], bold=True)
    cell = 60
    gx, gy = x0 + 24, y0 + 52
    order = {}
    if cp:
        k = 0
        for p in range(16):
            if cp[p]:
                k += 1
                order[p] = k
    for p in range(16):
        r, c = divmod(p, 4)
        X, Y = gx + c * cell, gy + r * cell
        on = p in order
        cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), fill=T['green'] if on else T['panel2'], r=8, outline=T['border'])
        cv.text((X + cell / 2, Y + cell / 2), p, 24, T['bg'] if on else T['dim'], anchor='mm', bold=True, mono=True)
        if on:
            cv.text((X + cell - 8, Y + 6), order[p], 14, T['bg'], anchor='rt', bold=True)
        if lv is not None and p == lv:
            cv.rect((X, Y, X + cell, Y + cell), outline=T['pink'], width=6, r=10)
    hs, ls = S.get('r'), S.get('l')
    if not (isinstance(hs, list) and isinstance(ls, list) and cp):
        return
    cw = min(38, (x1 - (gx + 4 * cell + 100) - 20) / 16)
    sx = gx + 4 * cell + 90
    rows = [('r', hs, T['orange']), ('l', ls, T['blue']), ('路径', cp, T['green'])]
    for k, (name, arr, col) in enumerate(rows):
        Y = gy + 20 + k * 80
        cv.text((sx - 12, Y + 22), name, 22, col, anchor='rm', bold=True)
        for j, v in enumerate(arr):
            X = sx + j * cw
            hit = lv is not None and j == lv
            txt = ('√' if v else '·') if name == '路径' else str(v)
            cv.rect((X + 2, Y, X + cw - 2, Y + 44), fill=T['panel2'], r=6, outline=T['pink'] if hit else T['border'])
            cv.text((X + cw / 2, Y + 22), txt, 22, (T['green'] if v else T['dim']) if name == '路径' else T['text'], anchor='mm', bold=True, mono=True)
    if lv is not None:
        cv.text((sx, gy + 20 + 3 * 80 + 4), f'当前 level = {lv}（网格第 {lv} 格）', 24, T['pink'], bold=True)
        cv.text((sx, gy + 20 + 3 * 80 + 40), f"pre = {inner.get('pre')}（路径上上一个填的数）", 24, T['cyan'], bold=True)
        st = inner.get('state')
        if st is not None:
            cv.text((sx, gy + 20 + 3 * 80 + 76), f"state = {st:02b}（{'贴 r' if st & 2 else '不贴 r'}，{'贴 l' if st & 1 else '不贴 l'}）", 24, T['yellow'], bold=True)


def _g(S, k):
    return S['_inner'].get(k)


CONFIG = dict(
    num=3906, title='统计网格路径中好整数的数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='数位 DP（checkpoints 标记路径数位）',
    tags=['灵神题单', '动态规划', '数学算法', '难度分 2160'],
    code='''
class Solution(object):
    def countGoodIntegersOnPath(self, l, r, directions):
        
        checkpoints = [False] * 16
        checkpoints[0] = True
        p = 0
        for c in directions:
            if c == 'D':
                p += 4
            else:
                p += 1
            checkpoints[p] = True
        
        f = [[[None] * 4 for _ in range(10)] for _ in range(16)]
        l = [int(d) for d in list(str(l))]
        r = [int(d) for d in list(str(r))]
        l = [0] * (16 - len(l)) + l
        r = [0] * (16 - len(r)) + r

        def calc(level, pre, state):
            if level == 16:
                return 1

            if f[level][pre][state] is None:
                f[level][pre][state] = 0
                start, end = 0, 9
                if state & 1:
                    start = max(start, l[level])
                if checkpoints[level]:
                    start = max(start, pre)
                
                if state & 2:
                    end = min(end, r[level])
                
                for d in range(start, end + 1):
                    if checkpoints[level]:
                        nxt_pre = d
                    else:
                        nxt_pre = pre
                    
                    nxt_state = 0
                    if (state & 1) and d == l[level]:
                        nxt_state |= 1
                    if (state & 2) and d == r[level]:
                        nxt_state |= 2
                    
                    f[level][pre][state] += calc(level + 1, nxt_pre, nxt_state)
            
            return f[level][pre][state]
    
        return calc(0, 0, 3)
''',
    call='Solution().countGoodIntegersOnPath(8, 12, "DDRRDR")',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=440),
        dict(type='calls', h=200),
    ],
    watch=[('level', lambda S: _g(S, 'level'), 'pink'), ('pre', lambda S: _g(S, 'pre'), 'cyan'),
           ('start', lambda S: _g(S, 'start'), 'blue'), ('end', lambda S: _g(S, 'end'), 'orange'),
           ('d', lambda S: _g(S, 'd'), 'yellow')],
    skip=['checkpoints[0] = True', 'p = 0', 'if c == ', 'p += 4', 'p += 1', 'else:', 'f[level][pre][state] = 0',
          'start, end = 0, 9', 'start = max', 'end = min', 'if state & 1', 'if state & 2', 'if checkpoints[level]',
          'nxt_pre = ', 'nxt_state = 0', 'nxt_state |= ', 'if (state & 1) and', 'if (state & 2) and', 'f[level][pre][state] is None',
          'f = [[[None]', 'for c in directions', 'for d in range', 'if level == 16', 'list(str(', 'r = [0] * (16', 'return f[level][pre][state]'],
    captions={
        'checkpoints = [False]': '`checkpoints[p]` = 第 p 个数位是否在路径上（最终是 16 位数字对应的 16 格）',
        'checkpoints[p] = True': '`directions` 固定，路径走过的格子也固定：`checkpoints[{p}] = True`',
        'l = [0] * ': '`l`、`r` 补成 16 位：`l = {l}`，`r = {r}`',
        'return calc(0, 0, 3)': lambda S, B, ret: ('入口 `calc(0, 0, 3)`：`pre = 0` 让路径第一个数不受限，`state = 11` 上下界都贴着' if ret is None else f'答案 `{ret}`'),
        'return 1': '16 位都填完，路径上每个数都 ≥ 上一个 → 找到一个好整数，返回 `1`',
        'f[level][pre][state] += calc': lambda S, B, ret: (
            (lambda lv: f'第 {lv} 位' + ('（==路径格==）' if S.checkpoints[lv] else '（非路径）')
             + f'：可填 `d ∈ [{S.start}, {S.end}]`' + ('，路径格下界还要 ≥ pre' if S.checkpoints[lv] else '，非路径格不看 pre')
             + f'；填 `d = {S.d}` → ' + (f'`pre = {S.nxt_pre}`' if S.checkpoints[lv] else 'pre 不变')
             + f'，下一位 `state = {S.nxt_state:02b}`（' + ('贴 r' if S.nxt_state & 2 else '不贴 r') + '，' + ('贴 l' if S.nxt_state & 1 else '不贴 l') + '）')(S.level - 1)),
    },
    max_steps=70,
    cards=dict(
        one_liner='路径固定 → 路径上的数位要 ≥ 上一个路径数位',
        complexity='时间 `O(D²·16)`，空间 `O(D·16)`，`D = 10`',
        problem=['16 位数字（前补 0）按行填进 4×4 网格，从左上角按 `directions` 走 6 步',
                 '路径上的 7 个数非递减，这个整数就是好整数；求 `[l, r]` 内好整数个数',
                 '本视频：`l=8, r=12`，`DDRRDR` → `4`（8、9、11、12）'],
        quote='directions在一开始就给定了，那么从左上角(0, 0)出发，走过的单元格也随之固定了下来，换言之，出现在数字序列中的数位下标也固定了下来。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用 `checkpoints[0..15]` 标出哪些数位在路径上',
              '`f[level][pre][state]`：`pre` 是上一个路径数位填的值，`state` 两位记贴 l / 贴 r',
              '路径格的下界再和 `pre` 取大，非路径格不管 `pre`，`nxt_pre` 只在路径格更新'],
        summary=['时间 `O(16·D²)`：状态 `16·10·4`，转移枚举 `D` 个数字',
                 '`pre` 初始 0：路径第一个数前面当作 0，不受限制',
                 '`l`、`r` 都要补前导 0 到 16 位，`level` 才和网格格子一一对应',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神只处理 `r` 的位数（倒着标记路径），yiduobo 固定 16 位、正着走一遍路径'],
    ),
)
