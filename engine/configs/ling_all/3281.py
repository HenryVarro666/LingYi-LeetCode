START = [6, 0, 1]
D = 2


def _xs(S, score):
    st = sorted(S['start'])
    xs, prev = [], None
    for s in st:
        prev = s if prev is None else max(prev + score, s)
        xs.append(prev)
    return st, xs


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    st = sorted(START)
    n = len(st)
    lo, hi = st[0], st[-1] + D
    cv.text((x0 + 18, y0 + 4), '每个区间 [start, start+d]（黄 = 当前区间，绿点 = 已选的数）', 24, T['muted'], bold=True)
    left, right = x0 + 100, x1 - 40
    unit = (right - left) / max(1, hi - lo)
    rowh = min(70, (y1 - y0 - 120) / n)
    top = y0 + 56
    score = S.get('score')
    s_cur = S.get('s') if 'score' in S else None
    xs = _xs(S, score)[1] if score is not None else None
    for k, s in enumerate(st):
        y = top + k * rowh
        cur = s_cur == s
        cv.rect((left + (s - lo) * unit, y + 8, left + (s + D - lo) * unit, y + rowh - 14),
                fill=T['yellow'] if cur else (70, 76, 86), r=6, alpha=200 if cur else 255)
        cv.text((left - 12, y + rowh / 2 - 3), f'[{s},{s + D}]', 20, T['muted'], anchor='rm', mono=True)
        if xs is not None and (s_cur is None or s < s_cur or (cur and S.get('x') == xs[k])):
            px = left + (xs[k] - lo) * unit
            ok = s <= xs[k] <= s + D
            cv.rect((px - 9, y + rowh / 2 - 16, px + 9, y + rowh / 2 + 2), fill=T['green'] if ok else T['red'], r=9)
            cv.text((px, y + rowh / 2 + 6), xs[k], 20, T['text'], anchor='mt', bold=True)
    base = top + n * rowh + 6
    cv.line([(left, base), (right, base)], T['border'], 2)
    for v in range(lo, hi + 1):
        px = left + (v - lo) * unit
        cv.line([(px, base), (px, base + 8)], T['border'], 2)
        cv.text((px, base + 12), v, 18, T['dim'], anchor='mt', mono=True)


def _color(S, i, v):
    if 'left' not in S:
        return None
    if i <= S['left']:
        return 'green'
    if i >= S['right']:
        return 'red'
    return None


def _top(S):
    if 'score' in S:
        sc = S['score']
        return f'试 `score = {sc}`：相邻两数至少差 `{sc}`，==每个数尽量靠左=='
    if 'left' not in S:
        return '最大化「最小差」→ ==二分猜 score==，再贪心验证'
    l, r = S['left'], S['right']
    if l + 1 < r:
        return f'开区间 `({l}, {r})`：`{l}` 可以，`{r}` 不行，中间还不确定'
    return f'`left + 1 == right`：`{l}` 可以，`{r}` 不行 → 答案 =={l}=='


def _cond(S, B, ret):
    return (f'`x = {S.x}`，区间右端点 `s + d = {S.s + D}`：'
            + ('超出了 → ==这个 score 太大==，返回 False' if S.x > S.s + D else '没超出，选得下 → 继续'))


CONFIG = dict(
    num=3281, title='范围内整数的最大得分', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分答案 · 最大化最小值',
    tags=['灵神题单·二分算法', '难度分 1768'],
    code='''
class Solution:
    def maxPossibleScore(self, start: List[int], d: int) -> int:
        start.sort()

        def check(score: int) -> bool:
            x = -inf
            for s in start:
                x = max(x + score, s)  # x 必须 >= 区间左端点 s
                if x > s + d:
                    return False
            return True

        left, right = 0, (start[-1] + d - start[0]) // (len(start) - 1) + 1
        while left + 1 < right:
            mid = (left + right) // 2
            if check(mid):
                left = mid
            else:
                right = mid
        return left
''',
    call=f'Solution().maxPossibleScore({START}, {D})',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var=lambda S: list(range(6)), label='候选 score（绿 = 可以，红 = 不行，灰 = 未知）',
             cell=70, color=_color, pointers={'left': 'green', 'mid': 'yellow', 'right': 'red'}, h=220),
    ],
    watch=[('left', 'left', 'green'), ('right', 'right', 'red'), ('mid', 'mid', 'yellow'), ('score', 'score', 'cyan'),
           ('x', 'x', 'orange')],
    captions={
        'start.sort()': '按左端点排序：只需看==相邻==区间所选的数之差',
        'x = -inf': '假想第一个区间左边选了 `-inf`，这样第一个数自然落在 `start[0]`',
        'x = max(x': '`x = max({B.x} + {score}, {s}) = {x}`：离上一个数至少 `{score}`，且不能小于左端点 `{s}`，==越靠左越好==',
        'if x > s': _cond,
        'return False': '有区间选不下 → `score = {score}` ==太大==',
        'return True': '每个区间都选得下 → `score = {score}` ==可行==',
        'left, right =': '`left = 0` 一定可行；`right = {right}` 超过平均间隔，==一定不行==',
        'while left + 1': lambda S, B, r: (f'开区间 `({S.left}, {S.right})` 不为空 → 继续' if S.left + 1 < S.right
                                          else f'`left + 1 == right`：区间为空，==left 就是最大可行 score=='),
        'mid = (left': '猜 `mid = ({left} + {right}) // 2 = {mid}`',
        'if check(mid)': '调用 `check({mid})`：能否让相邻差都 ≥ {mid}？',
        'left = mid': '`{mid}` 可行，答案 ==≥ mid==：`left = {left}`',
        'right = mid': '`{mid}` 不行，答案 ==< mid==：`right = {right}`',
        'return left': '`left` 是==最大的可行 score== → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='最大化最小值 → 二分 score，再贪心地「每个数选最靠左」',
        complexity='时间 `O(n log n + n log A)`，空间 `O(1)`',
        problem=['`start[i]` 对应区间 `[start[i], start[i] + d]`，每个区间选一个整数',
                 '得分 = 所选整数两两之差的==最小值==，求最大得分',
                 '示例：`start = [6,0,3], d = 2` → `4`（选 8、0、4）',
                 '本视频：`start = [6,0,1], d = 2` → `3`'],
        quote='贪心地想，第一个数越小，第二个数就越能在区间内，所以第一个数要选 start[0]。依此类推，第 i 个区间所选的数为 x_i = max(x_{i-1}+score, start[i])。',
        quote_src='—— 灵茶山艾府题解',
        idea=['score 越大越难满足，有单调性 → ==二分答案==',
              '给定 score：排序后逐个区间选「离上个数至少 score 的最小数」',
              '选出的数超过区间右端点 `s + d` 就失败'],
        summary=['时间 `O(n log n + n log A)`，空间 `O(1)`',
                 '`check` 判的是「至少 score」，不是「恰好」；二分会自己收敛到恰好',
                 '开区间右端点用平均间隔 `+1`，比 `10^9` 更紧',
                 '同类题：二分题单「最大化最小值」；另有 `bisect_left` 库函数写法'],
    ),
)
