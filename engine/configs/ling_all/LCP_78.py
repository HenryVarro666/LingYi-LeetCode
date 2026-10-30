RAMP = [[2, 3], [11, 14], [16, 21], [22, 24]]
XMIN, XMAX = -3, 29


def _sim(m, upto):
    """贪心：先向左膨胀，再向右膨胀；返回前 upto+1 段城墙膨胀后的 (左扩展起点, 原l, 原r, 右扩展终点, 是否失败)"""
    out = []
    pre_r = None
    for i, (l, r) in enumerate(RAMP):
        if i > upto:
            break
        gap = m if pre_r is None else l - pre_r
        left_part = min(m, gap)
        space = m - gap
        nr = r + space if space > 0 else r
        if i == len(RAMP) - 1:
            nr = r + max(0, m - left_part)
        bad = i + 1 < len(RAMP) and nr > RAMP[i + 1][0]
        out.append((l - left_part, l, r, nr, bad))
        pre_r = nr
    return out


def _cur(S):
    inn = S['_inner']
    if 'm' not in inn:
        return None, None
    m = inn['m']
    if S['_line'] == 12:
        return m, len(RAMP) - 1
    if 'l' not in inn:
        return m, -1
    for i, (l, r) in enumerate(RAMP):
        if l == inn['l']:
            return m, i
    return m, -1


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    a, b = x0 + 40, x1 - 40
    sc = (b - a) / (XMAX - XMIN)
    X = lambda v: a + (v - XMIN) * sc
    m, upto = _cur(S)
    title = '城墙（灰 = 原位置，青 = 向左膨胀，橙 = 向右膨胀，红 = 撞上下一段）'
    cv.text((x0 + 18, y0 + 4), title, 21, T['muted'], bold=True)
    yb = y0 + 74
    ya = y0 + 150
    axis = y1 - 50
    cv.line([(a, axis), (b, axis)], T['border'], 2)
    for v in range(0, XMAX + 1, 5):
        cv.line([(X(v), axis - 6), (X(v), axis + 6)], T['dim'], 2)
        cv.text((X(v), axis + 10), v, 17, T['dim'], anchor='mt', mono=True)
    for i, (l, r) in enumerate(RAMP):
        cv.rect((X(l), yb, X(r), yb + 44), fill=(110, 118, 130), r=4)
        cv.text(((X(l) + X(r)) / 2, yb - 4), f'[{l},{r}]', 18, T['text'], anchor='mb', bold=True)
        cv.dashed((X(l), yb + 46), (X(l), axis), T['dim'], 1, dash=5, gap=6)
        cv.dashed((X(r), yb + 46), (X(r), axis), T['dim'], 1, dash=5, gap=6)
    if m is None:
        cv.text(((a + b) / 2, ya + 40), '（进入 check(m) 后，这里画出每段城墙的膨胀）', 22, T['dim'], anchor='mm')
        return
    cv.text((x1 - 18, ya + 72), f'膨胀后（m = {m}）', 20, T['yellow'], anchor='ra', bold=True)
    for i, (sl, l, r, nr, bad) in enumerate(_sim(m, upto)):
        cv.rect((X(sl), ya, X(l), ya + 44), fill=T['cyan'], r=3)
        cv.rect((X(l), ya, X(r), ya + 44), fill=(110, 118, 130))
        if nr > r:
            cv.rect((X(r), ya, X(nr), ya + 44), fill=T['red'] if bad else T['orange'], r=3)
        if i + 1 < len(RAMP) and i == upto:
            nl = RAMP[i + 1][0]
            cv.line([(X(nl), ya - 10), (X(nl), ya + 54)], T['red'] if bad else T['green'], 3)


def _top(S):
    m, upto = _cur(S)
    if m is not None:
        return f'检查 `m = {m}`：每段城墙==先向左膨胀，剩下的再向右=='
    if 'right' in S:
        l, r = S['left'], S['right']
        if l + 1 < r:
            return f'开区间 `({l}, {r})`：left 一定不重叠，right 一定重叠'
        return f'`left + 1 == right`：`{l}` 可行、`{r}` 不可行 → 答案 =={l}=='
    if 's' in S:
        return f"间距之和 `s = {S['s']}`，分给中间 `n − 2 = {len(RAMP) - 2}` 段城墙"
    return '膨胀越短越不会重叠 → ==二分答案=='


def _space(S, B, ret):
    inn = S._inner
    gap = inn['l'] - inn['pre_r']
    if inn['space'] == float('-inf'):
        return '第一段：左边是无穷远，`m` 全部向左膨胀，`space = -inf`'
    if inn['space'] > 0:
        return f"左边空隙 `{inn['l']} − {inn['pre_r']} = {gap}` 不够 `m = {inn['m']}`：向左膨胀 {gap}，==还剩 {inn['space']}== 要向右"
    return f"左边空隙 `{gap}` ≥ `m = {inn['m']}`：全部向左膨胀就够了（`space = {inn['space']}`）"


CONFIG = dict(
    num='LCP 78', title='城墙防线', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分答案 + 贪心先左后右',
    tags=['灵神核心路线', '灵神题单·二分算法'],
    code='''
class Solution:
    def rampartDefensiveLine(self, rampart: List[List[int]]) -> int:
        def check(m: int) -> bool:
            pre_r = -inf
            for (l, r), (nxt_l, _) in pairwise(rampart):
                space = m - (l - pre_r)  # 向左膨胀后的剩余长度
                if space > 0:
                    r += space  # 向右膨胀
                    if r > nxt_l:  # 无法膨胀
                        return False
                pre_r = r
            return True

        s = sum(l2 - r1 for (_, r1), (l2, _) in pairwise(rampart))
        left, right = 0, s // (len(rampart) - 2) + 1
        while left + 1 < right:
            mid = (left + right) // 2
            if check(mid):
                left = mid
            else:
                right = mid
        return left
''',
    call=f'Solution().rampartDefensiveLine({RAMP})',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=26, h=70),
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var=lambda S: list(range(7)),
             label='候选膨胀长度（绿 = 可行，红 = 不可行）', cell=72, index=False, h=190,
             color=lambda S, i, v: (('green' if v <= S['left'] else 'red' if v >= S['right'] else None) if 'right' in S else None),
             pointers={'left': 'green', 'mid': 'yellow', 'right': 'red'}),
    ],
    watch=[('left', 'left', 'green'), ('right', 'right', 'red'), ('mid', 'mid', 'yellow'),
           ('pre_r', lambda S: S['_inner'].get('pre_r', '—'), 'cyan'), ('space', lambda S: S['_inner'].get('space', '—'), 'orange')],
    skip=['for (l, r), (nxt_l'],
    captions={
        's = sum': '相邻城墙间距之和 `s = {s}`',
        'left, right = 0': '`left = 0` 一定可行；`right = s // (n − 2) + 1 = {right}`：比平均间距还大，==一定重叠==',
        'while left + 1 < right': lambda S, B, r: (f'开区间 `({S.left}, {S.right})` 不为空 → 继续二分' if S.left + 1 < S.right
                                                    else '`left + 1 == right`：开区间为空，结束'),
        'mid = (left': '猜膨胀长度 `mid = ({left} + {right}) // 2 = {mid}`',
        'if check(mid)': '调用 `check({mid})`：每段都膨胀 {mid}，能否互不重叠？',
        'pre_r = -inf': '`pre_r`：上一段城墙膨胀后的右端点，第一段左边是无穷远',
        'space = m': _space,
        'if space > 0': lambda S, B, r: ('`space > 0`：要向右膨胀' if S._inner['space'] > 0 else '`space ≤ 0`：不用向右膨胀'),
        'r += space': lambda S, B, r: f"向右膨胀到 `r = {S._inner['r']}`",
        'if r > nxt_l': lambda S, B, r: (f"`r = {S._inner['r']} > nxt_l = {S._inner['nxt_l']}`：==撞上下一段== → m 过大"
                                          if S._inner['r'] > S._inner['nxt_l'] else f"`r = {S._inner['r']} ≤ nxt_l = {S._inner['nxt_l']}`：没撞上，下一段继续"),
        'return False': '`check` 返回 `False`',
        'pre_r = r': lambda S, B, r: f"`pre_r = {S._inner['pre_r']}`：留给下一段向左膨胀的空间从这里算",
        'return True': '中间都没撞上，最后一段向外无限膨胀 → `check` 返回 `True`',
        'left = mid': '可行 → 答案 ==≥ {left}==：`left = {left}`',
        'right = mid': '不可行 → 答案 ==< {right}==：`right = {right}`',
        'return left': '城墙最多膨胀 =={ret}==',
    },
    cards=dict(
        one_liner='二分膨胀长度；验证时每段先向左撑满，剩下的再向右',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['`rampart[i] = [x, y]` 是第 i 段城墙，已升序且互不重叠',
                 '所有城墙同时膨胀==相同长度==，可向左、向右或两边分着膨胀',
                 '求不重叠时的最大膨胀长度；示例 `[[1,2],[5,8],[11,15],[18,25]]` → `4`',
                 '本视频：`[[2,3],[11,14],[16,21],[22,24]]` → `3`'],
        quote='膨胀长度越短，越能满足要求（不重叠）……据此可以==二分答案==。我们可以贪心。每段城墙==先向左膨胀，再向右膨胀==，如果向右膨胀后，与右侧的城墙重叠，则说明 m 过大。',
        quote_src='—— 灵茶山艾府题解',
        idea=['两个方向的膨胀长度可以不相等，只要和等于 `m`',
              '左边空着的地方不用白不用：先向左占满，给右边的城墙留更多空间',
              '最左最右两段向外膨胀即可；中间 `n − 2` 段分 `s` → 右端点 `s // (n−2) + 1`'],
        summary=['时间 `O(n log U)`，`U` 为二分初始长度；空间 `O(1)`',
                 '`pre_r` 初始 `-inf`：第一段可以全部向左',
                 '`pairwise` 只遍历到倒数第二段：最后一段向右无限膨胀，不用检查',
                 '左端点也可以优化成相邻城墙的最小间距；另有 `bisect_left` 库函数写法'],
    ),
)
