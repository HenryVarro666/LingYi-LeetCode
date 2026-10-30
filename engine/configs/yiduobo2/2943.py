_CODE = '''
class Solution(object):
    def maximizeSquareHoleArea(self, n, m, hBars, vBars):

        def calc(bars):
            bars.sort()
            p = 0
            ma = 0
            while p < len(bars):
                start = p
                p += 1
                while p < len(bars) and bars[p] == bars[p - 1] + 1:
                    p += 1

                ma = max(ma, p - start)

            return ma

        return (min(calc(hBars), calc(vBars)) + 1) ** 2
'''
_LINES = _CODE.strip('\n').split('\n')


def _best(bars):
    s = sorted(bars)
    best, i = (0, 0), 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and s[j + 1] == s[j] + 1:
            j += 1
        if j - i + 1 > best[1]:
            best = (s[i], j - i + 1)
        i = j + 1
    return best


def _phase(S):
    inner = S['_inner']
    src = _LINES[S['_line'] - 1].strip() if 0 < S['_line'] <= len(_LINES) else ''
    cur = None
    if 'bars' in inner:
        cur = 'h' if sorted(inner['bars']) == sorted(S['hBars']) else 'v'
    done_h = cur == 'v'
    done_v = cur == 'v' and src.startswith('return')
    return cur, done_h, done_v, inner


def _chain(inner):
    if 'start' not in inner or 'p' not in inner:
        return set()
    return set(inner['bars'][inner['start']:inner['p']])


def _grid(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n, m = S['n'], S['m']
    cur, done_h, done_v, inner = _phase(S)
    chain = _chain(inner)
    cv.text((x0 + 18, y0 + 4), '网格：实线固定，虚线可删（蓝 = hBars，粉 = vBars），绿 = 当前连续横杠组', 22, T['muted'], bold=True)
    rows, cols = n + 1, m + 1
    cell = min((x1 - x0 - 260) / cols, (y1 - y0 - 90) / rows)
    gx0 = x0 + 90 + ((x1 - x0 - 260) - cell * cols) / 2
    gy0 = y0 + 64
    gx1, gy1 = gx0 + cell * cols, gy0 + cell * rows
    hb, vb = _best(S['hBars']), _best(S['vBars'])
    if done_h and done_v:
        side = min(hb[1], vb[1]) + 1
        r0, c0 = hb[0] - 2, vb[0] - 2
        cv.rect((gx0 + c0 * cell, gy0 + r0 * cell, gx0 + (c0 + side) * cell, gy0 + (r0 + side) * cell),
                fill=T['green'], alpha=70)
        cv.text((gx0 + (c0 + side / 2) * cell, gy0 + (r0 + side / 2) * cell), f'({side - 1}+1)²={side * side}', 32,
                T['text'], anchor='mm', bold=True)
    for i in range(1, n + 3):
        y = gy0 + (i - 1) * cell
        removable = i in S['hBars']
        c, wdt, dashed = T['muted'], 3, False
        if removable:
            c, dashed = T['blue'], True
            if cur == 'h' and i in chain:
                c, wdt, dashed = T['green'], 6, False
            if done_h and hb[0] <= i < hb[0] + hb[1]:
                c, wdt = T['dim'], 2
        if dashed:
            cv.dashed((gx0, y), (gx1, y), c, wdt, dash=14, gap=10)
        else:
            cv.line([(gx0, y), (gx1, y)], c, wdt)
        cv.text((gx0 - 14, y), i, 22, T['blue'] if removable else T['dim'], anchor='rm', bold=removable, mono=True)
    for j in range(1, m + 3):
        x = gx0 + (j - 1) * cell
        removable = j in S['vBars']
        c, wdt, dashed = T['muted'], 3, False
        if removable:
            c, dashed = T['pink'], True
            if cur == 'v' and j in chain:
                c, wdt, dashed = T['green'], 6, False
            if done_v and vb[0] <= j < vb[0] + vb[1]:
                c, wdt = T['dim'], 2
        if dashed:
            cv.dashed((x, gy0), (x, gy1), c, wdt, dash=14, gap=10)
        else:
            cv.line([(x, gy0), (x, gy1)], c, wdt)
        cv.text((x, gy0 - 10), j, 22, T['pink'] if removable else T['dim'], anchor='mb', bold=removable, mono=True)
    tx = gx1 + 30
    cv.text((tx, gy0 + 10), 'calc(hBars)', 24, T['blue'], bold=True)
    cv.text((tx, gy0 + 44), f'最长组 {hb[1]} 根' if done_h else '……', 24, T['text'] if done_h else T['dim'])
    cv.text((tx, gy0 + 76), f'→ 空格 {hb[1] + 1}' if done_h else '', 24, T['green'], bold=True)
    cv.text((tx, gy0 + 140), 'calc(vBars)', 24, T['pink'], bold=True)
    cv.text((tx, gy0 + 174), f'最长组 {vb[1]} 根' if done_v else '……', 24, T['text'] if done_v else T['dim'])
    cv.text((tx, gy0 + 206), f'→ 空格 {vb[1] + 1}' if done_v else '', 24, T['green'], bold=True)


def _bars(S):
    return S['_inner'].get('bars')


def _ptr(name):
    def f(S):
        return S['_inner'].get(name)
    return f


_START, _P = _ptr('start'), _ptr('p')


def _win_end(S):
    inner = S['_inner']
    if 'start' in inner and inner['p'] > inner['start']:
        return inner['p'] - 1
    return None


def _label(S):
    cur = _phase(S)[0]
    return {'h': '当前：`calc(hBars)`', 'v': '当前：`calc(vBars)`'}.get(cur, '')


def _inner_while(S, B, ret):
    p, bars = S.p, S.bars
    if p >= len(bars):
        return f'`p = {p}` 已到末尾 → 这一组结束'
    if bars[p] == bars[p - 1] + 1:
        return f'`bars[{p}] = {bars[p]}` 紧挨着 `{bars[p - 1]}` → 同一组，继续延伸'
    return f'`bars[{p}] = {bars[p]}` ≠ `{bars[p - 1]} + 1` → 中间有原生横杠隔断，这一组结束'


CONFIG = dict(
    num=2943, title='最大化网格图中正方形空洞的面积', difficulty='Medium', category='哈希',
    author='yiduobo', technique='横竖分开 · 排序后找最长连续组',
    tags=['字节3个月', '字节6个月'],
    code=_CODE,
    call='Solution().maximizeSquareHoleArea(4, 4, [3, 5, 2], [5, 2, 4, 3])',
    expect=9,
    views=[
        dict(type='custom', draw=_grid, h=470),
        dict(type='array', var=_bars, pointers={_START: 'blue', _P: 'pink'}, pointer_labels={_START: 'start', _P: 'p'},
             window=(_START, _win_end), h=200, cell=80, label='bars（框 = 当前连续组 bars[start..p-1]）'),
        dict(type='text', fn=_label, size=26, h=50),
    ],
    watch=[('start', 'start', 'blue'), ('p', 'p', 'pink'), ('ma', 'ma', 'green')],
    captions={
        'return (min(': '水平、竖直的消除==互不相关==：分别 `calc` 出最长连续组，取较小值',
        'bars.sort()': lambda S, B, r: f'先排序：`{list(B.bars)}` → `{list(S.bars)}`，编号相邻的横杠排到一起',
        'p = 0': '`p` 扫描指针',
        'ma = 0': '`ma`：最长的==连续可消除横杠组==有几根',
        'while p < len(bars):': lambda S, B, r: (f'`p = {S.p} < {len(S.bars)}`：开始新的一组' if S.p < len(S.bars)
                                                 else '扫描完毕'),
        'start = p': '这一组从 `start = {start}`（横杠 `{bars[start]}`）开始',
        'p += 1': lambda S, B, r: f'`p` → {S.p}',
        'while p < len(bars) and': _inner_while,
        'ma = max': '这一组 `p − start = {p - start}` 根：`ma = max({B.ma}, {p - start}) = {ma}`',
        'return ma': lambda S, B, r: f'最长连续组 `{r}` 根 → 消除后连续空白 `{r} + 1 = {r + 1}` 格',
    },
    cards=dict(
        one_liner='排序后找最长的连续横杠组，k 根连续横杠空出 k+1 格',
        complexity='时间 `O(h log h + v log v)`，空间 `O(1)`（忽略排序）',
        problem=['网格有 `n+2` 条水平线、`m+2` 条竖直线，`hBars` / `vBars` 中的线可以删除',
                 '求删除一些线后==正方形空洞==的最大面积',
                 '示例：`n=2, m=1, hBars=[2,3], vBars=[2]` → `4`',
                 '本视频：`n=4, m=4, hBars=[3,5,2], vBars=[5,2,4,3]` → `9`'],
        quote='一旦消除的横杠之间不连续，那么就会被原生的横杠隔断……只需将横杠进行排序，然后==一趟遍历找出最长的连续值==就行了。',
        quote_src='—— yiduobo 题解原文',
        result='`(min(2, 4) + 1) ** 2 = 3² = 9`：最大正方形空洞面积为 9',
        idea=['水平和竖直方向的消除==互不相关==，答案是两方向连续空白较小值的平方',
              '可消除的横杠不连续 → 被原生横杠隔断 → 只能用==最长连续组==',
              '连续 `k` 根横杠形成长度 `k + 1` 的空格：==别忘了 +1=='],
        summary=['时间 `O(h log h + v log v)`，空间 `O(1)`（忽略排序）',
                 '易错：`k` 根连续横杠空出 `k + 1` 格，平方前要先 +1',
                 '内层 `while` 先判 `p < len(bars)` 再访问 `bars[p]`，防止越界',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神用 128 题的哈希集合技巧做到线性时间，不用排序'],
    ),
)
