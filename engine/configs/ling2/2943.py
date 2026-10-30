_CODE = '''
class Solution:
    # 128. 最长连续序列
    def longestConsecutive(self, nums: List[int]) -> int:
        st = set(nums)  # 把 nums 转成哈希集合
        ans = 0
        for x in st:  # 遍历哈希集合
            if x - 1 in st:  # 如果 x 不是序列的起点，直接跳过
                continue
            # x 是序列的起点
            y = x + 1
            while y in st:  # 不断查找下一个数是否在哈希集合中
                y += 1
            # 循环结束后，y-1 是最后一个在哈希集合中的数
            ans = max(ans, y - x)  # 从 x 到 y-1 一共 y-x 个数
        return ans

    def maximizeSquareHoleArea(self, n: int, m: int, hBars: List[int], vBars: List[int]) -> int:
        side = min(self.longestConsecutive(hBars), self.longestConsecutive(vBars)) + 1
        return side * side
'''
_LINES = _CODE.strip('\n').split('\n')


def _best(bars):
    """(起点编号, 连续条数) of the longest consecutive run"""
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
    if 'nums' in inner:
        cur = 'h' if inner['nums'] == S['hBars'] else 'v'
    final = 'side' in inner
    done_h = cur == 'v' or final
    done_v = final or (cur == 'v' and src.startswith('return'))
    return cur, done_h, done_v, inner


def _chain(inner):
    st, x, y = inner.get('st'), inner.get('x'), inner.get('y')
    if st is None or x is None or y is None or x - 1 in st or not x < y:
        return set()
    if all(v in st for v in range(x, y)):
        return set(range(x, y))
    return set()


def _grid(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n, m = S['n'], S['m']
    cur, done_h, done_v, inner = _phase(S)
    chain = _chain(inner)
    skipx = inner.get('x') if inner.get('st') is not None and inner.get('x') is not None and inner['x'] - 1 in inner['st'] else None
    cv.text((x0 + 18, y0 + 4), '网格：实线固定，虚线可删（蓝 = hBars，粉 = vBars），绿 = 正在数的连续段', 22, T['muted'], bold=True)
    rows, cols = n + 1, m + 1
    cell = min((x1 - x0 - 260) / cols, (y1 - y0 - 90) / rows)
    gx0 = x0 + 90 + ((x1 - x0 - 260) - cell * cols) / 2
    gy0 = y0 + 64
    gx1, gy1 = gx0 + cell * cols, gy0 + cell * rows
    hb, vb = _best(S['hBars']), _best(S['vBars'])
    # final square
    if done_h and done_v:
        side = min(hb[1], vb[1]) + 1
        r0, c0 = hb[0] - 2, vb[0] - 2
        cv.rect((gx0 + c0 * cell, gy0 + r0 * cell, gx0 + (c0 + side) * cell, gy0 + (r0 + side) * cell),
                fill=T['green'], alpha=70)
        cv.text((gx0 + (c0 + side / 2) * cell, gy0 + (r0 + side / 2) * cell), f'{side}×{side}={side * side}', 34,
                T['text'], anchor='mm', bold=True)
    # horizontal lines
    for i in range(1, n + 3):
        y = gy0 + (i - 1) * cell
        removable = i in S['hBars']
        c, wdt, dashed = T['muted'], 3, False
        if removable:
            c, dashed = T['blue'], True
            if cur == 'h' and i in chain:
                c, wdt, dashed = T['green'], 6, False
            elif cur == 'h' and i == skipx:
                c = T['purple']
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
            elif cur == 'v' and j == skipx:
                c = T['purple']
            if done_v and vb[0] <= j < vb[0] + vb[1]:
                c, wdt = T['dim'], 2
        if dashed:
            cv.dashed((x, gy0), (x, gy1), c, wdt, dash=14, gap=10)
        else:
            cv.line([(x, gy0), (x, gy1)], c, wdt)
        cv.text((x, gy0 - 10), j, 22, T['pink'] if removable else T['dim'], anchor='mb', bold=removable, mono=True)
    # results on the right
    tx = gx1 + 30
    cv.text((tx, gy0 + 10), '水平方向', 24, T['blue'], bold=True)
    cv.text((tx, gy0 + 44), f'最长连续 {hb[1]} 条' if done_h else '……', 24, T['text'] if done_h else T['dim'])
    cv.text((tx, gy0 + 76), f'→ 高 {hb[1] + 1}' if done_h else '', 24, T['green'], bold=True)
    cv.text((tx, gy0 + 140), '竖直方向', 24, T['pink'], bold=True)
    cv.text((tx, gy0 + 174), f'最长连续 {vb[1]} 条' if done_v else '……', 24, T['text'] if done_v else T['dim'])
    cv.text((tx, gy0 + 206), f'→ 宽 {vb[1] + 1}' if done_v else '', 24, T['green'], bold=True)


def _order(S):
    st = S['_inner'].get('st')
    return list(st) if st is not None else None


def _xi(S):
    st, x = S['_inner'].get('st'), S['_inner'].get('x')
    return list(st).index(x) if st is not None and x in st else None


def _color(S, i, v):
    inner = S['_inner']
    if inner.get('x') is None:
        return None
    if v in _chain(inner):
        return 'green'
    if v == inner['x']:
        return 'purple' if v - 1 in inner['st'] else 'blue'
    return None


def _label(S):
    cur = _phase(S)[0]
    return {'h': '当前：longestConsecutive(hBars)', 'v': '当前：longestConsecutive(vBars)'}.get(cur, '')


def _skip_q(S, B, ret):
    x = S.x
    if x - 1 in S.st:
        return f'`{x - 1}` 也能删：从 `{x - 1}` 数会更长 → `{x}` ==不是起点==，跳过'
    return f'`{x - 1}` 不在集合里 → 线 `{x}` 是一段连续可删线的==起点=='


def _side(S, B, ret):
    return '先对 `hBars` 求最长连续段（==128 题==），再对 `vBars` 求，取较小值 + 1'


CONFIG = dict(
    num=2943, title='最大化网格图中正方形空洞的面积', difficulty='Medium', category='哈希',
    author='灵茶山艾府', technique='横竖分开 · 128 题哈希集合求最长连续',
    tags=['字节3个月', '字节6个月'],
    code=_CODE,
    call='Solution().maximizeSquareHoleArea(4, 4, [3, 5, 2], [5, 2, 4, 3])',
    expect=9,
    views=[
        dict(type='custom', draw=_grid, h=470),
        dict(type='array', var=_order, pointers={_xi: 'blue'}, pointer_labels={_xi: 'x'}, color=_color, h=180, cell=80,
             label='st（哈希集合，遍历顺序；紫 = 非起点，绿 = 当前连续段）'),
        dict(type='text', fn=_label, size=26, h=50),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'green'), ('ans', 'ans', 'orange'), ('side', 'side', 'pink')],
    captions={
        'side = min': _side,
        'st = set(nums)': lambda S, B, r: f"把可删的线 `{list(S.nums)}` 转成==哈希集合==，`O(1)` 判断某条线能不能删",
        'ans = 0': '`ans`：最多能删多少条==编号连续==的线',
        'for x in st': lambda S, B, r: ('集合遍历完' if 'x' in B and B.x == S.x else f'遍历哈希集合：`x = {S.x}`'),
        'if x - 1 in st': _skip_q,
        'continue': '跳过：避免从连续段中间重复往后数',
        'y = x + 1': '从起点 `{x}` 往后找：`y = {y}`',
        'while y in st': lambda S, B, r: (f'线 `{S.y}` 也能删 → 连续段继续延长' if S.y in S.st
                                          else f'线 `{S.y}` 不能删（固定线）→ 连续段到 `{S.y - 1}` 为止'),
        'y += 1': '`y` → {y}',
        'ans = max': '删掉 `{x}..{y - 1}` 共 `{y - x}` 条：`ans = max({B.ans}, {y - x}) = {ans}`',
        'return ans': lambda S, B, r: f'这个方向最多连续删 `{r}` 条 → 空出 `{r} + 1 = {r + 1}` 格',
        'return side * side': '`side = {side}`：正方形边长取==长宽较小值==，面积 `{side}² = {side * side}`',
    },
    cards=dict(
        one_liner='删 k 条编号连续的线，空出 k+1 格：横竖各求最长连续段',
        complexity='时间 `O(h + v)`，空间 `O(h + v)`',
        problem=['网格有 `n+2` 条水平线、`m+2` 条竖直线（编号从 1 开始），相邻线围成 1×1 格子',
                 '`hBars` / `vBars` 中的线可以删除，其余线固定。求删除后==正方形空洞==的最大面积',
                 '示例：`n=2, m=1, hBars=[2,3], vBars=[2]` → `4`',
                 '本视频：`n=4, m=4, hBars=[3,5,2], vBars=[5,2,4,3]` → `9`'],
        quote='贪心地，删的线段越多，面积越大……删除三条编号连续的线段（例如 2,3,4），最长长度是 4。所以本题要做的是，求==最长连续递增子数组的长度加一==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['横竖互不影响：先把能删的全删掉，算出最大矩形的长和宽',
              '删 `k` 条==编号连续==的线 → 空出 `k + 1` 格；不连续就被固定线隔断',
              '用 ==128. 最长连续序列== 的哈希集合技巧，不用排序，线性时间'],
        summary=['时间 `O(h + v)`，空间 `O(h + v)`；排序写法为 `O(h log h + v log v)`',
                 '易错：答案是最长连续段长度 ==+1== 再平方，别忘了 +1',
                 '正方形边长取长宽==较小值==（多删的线撤销即可）',
                 '128 题技巧：`x − 1` 在集合里就跳过，每条线至多被访问两次',
                 '另一种写法：排序后分组循环数最长连续递增段'],
    ),
)
