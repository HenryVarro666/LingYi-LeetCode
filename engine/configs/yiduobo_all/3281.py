START = [6, 0, 1]
D = 2


def _replay(mid):
    st = sorted(START)
    xs = [st[0]]
    for v in st[1:]:
        x = xs[-1]
        xs.append(v if x + mid <= v else x + mid)
    return st, xs


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    st = sorted(START)
    n = len(st)
    lo, hi = st[0], st[-1] + D
    cv.text((x0 + 18, y0 + 4), '每个区间 [start, start+d]（黄 = 当前区间，圆点 = 已取的数）', 24, T['muted'], bold=True)
    left, right = x0 + 100, x1 - 40
    unit = (right - left) / max(1, hi - lo)
    rowh = min(70, (y1 - y0 - 120) / n)
    top = y0 + 56
    line = S.get('_line', 0)
    active = 'mid' in S and 11 <= line <= 20
    xs = _replay(S['mid'])[1] if active else None
    v_cur = S.get('v') if active and line >= 13 else None
    k_cur = st.index(v_cur) if v_cur is not None else None
    for k, s in enumerate(st):
        y = top + k * rowh
        cur = k_cur == k
        cv.rect((left + (s - lo) * unit, y + 8, left + (s + D - lo) * unit, y + rowh - 14),
                fill=T['yellow'] if cur else (70, 76, 86), r=6, alpha=200 if cur else 255)
        cv.text((left - 12, y + rowh / 2 - 3), f'[{s},{s + D}]', 20, T['muted'], anchor='rm', mono=True)
        if xs is None:
            continue
        show = (k == 0) or (k_cur is not None and (k < k_cur or (k == k_cur and line in (15, 17))))
        if show:
            px = left + (xs[k] - lo) * unit
            cv.rect((px - 9, y + rowh / 2 - 16, px + 9, y + rowh / 2 + 2), fill=T['green'], r=9)
            cv.text((px, y + rowh / 2 + 6), xs[k], 20, T['text'], anchor='mt', bold=True)
        elif cur and line == 19:
            px = left + (S['now'] + S['mid'] - lo) * unit
            cv.rect((px - 9, y + rowh / 2 - 16, px + 9, y + rowh / 2 + 2), fill=T['red'], r=9)
            cv.text((px, y + rowh / 2 + 6), S['now'] + S['mid'], 20, T['text'], anchor='mt', bold=True)
    base = top + n * rowh + 6
    cv.line([(left, base), (right, base)], T['border'], 2)
    for v in range(lo, hi + 1):
        px = left + (v - lo) * unit
        cv.line([(px, base), (px, base + 8)], T['border'], 2)
        cv.text((px, base + 12), v, 18, T['dim'], anchor='mt', mono=True)


def _color(S, i, v):
    if 'left' not in S:
        return None
    if i < S['left']:
        return 'red'
    if i > S['right']:
        return 'red'
    return None


def _top(S):
    line = S.get('_line', 0)
    if 'mid' in S and 11 <= line <= 20:
        return f"试 `mid = {S['mid']}`：相邻两数至少差 `{S['mid']}`，==每个数尽量靠前=="
    if 'left' not in S:
        return '最大化「最小差」→ ==二分这个差值 mid=='
    l, r = S['left'], S['right']
    if l < r:
        return f'答案在闭区间 `[{l}, {r}]` 内'
    return f'`left == right = {l}` → 答案 =={l}=='


def _branch(S, B, ret):
    now, mid, v = S.now, S.mid, S.v
    if now + mid <= v:
        return f'上一个数 `now = {now}`：`{now} + {mid} = {now + mid} <= v = {v}` → 直接取 `v`'
    if now + mid <= v + D:
        return f'`{now} + {mid} = {now + mid}` 没到 `v = {v}`，但 `<= v + d = {v + D}` → 取 `now + mid`'
    return f'`{now} + {mid} = {now + mid} > v + d = {v + D}` → ==这个区间取不到数=='


CONFIG = dict(
    num=3281, title='范围内整数的最大得分', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分最小差 · 贪心取数',
    tags=['灵神题单·二分算法', '难度分 1768'],
    code='''
class Solution:
    def maxPossibleScore(self, start, d):

        start.sort()

        left = 0
        right = start[-1] + d - start[0]

        while left < right:
            mid = (left + right + 1) // 2
            now = start[0]
            flag = True
            for v in start[1:]:
                if now + mid <= v:
                    now = v
                elif now + mid <= v + d:
                    now += mid
                else:
                    flag = False
                    break

            if flag:
                left = mid
            else:
                right = mid - 1

        return left
''',
    call=f'Solution().maxPossibleScore({START}, {D})',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var=lambda S: list(range(9)), label='候选最小差（红 = 已排除，其余 = 还可能）',
             cell=64, color=_color, pointers={'left': 'green', 'mid': 'yellow', 'right': 'red'}, h=220),
    ],
    watch=[('left', 'left', 'green'), ('right', 'right', 'red'), ('mid', 'mid', 'yellow'), ('now', 'now', 'orange'),
           ('flag', 'flag', 'cyan')],
    captions={
        'start.sort()': '先按起点排序：最小差只会出现在==大小相邻==的数之间',
        'left = 0': '`left = 0`：差至少是 0',
        'right = start': '`right = {right}`：最大跨度，差不会比它大',
        'while left < right': lambda S, B, r: (f'`{S.left} < {S.right}`，答案还没夹住 → 继续' if S.left < S.right
                                              else f'`left == right = {S.left}` → 结束'),
        'mid = (left': '二分最小差：`mid = ({left} + {right} + 1) // 2 = {mid}`（==上取整==，因为 `left = mid` 不会前进）',
        'now = start[0]': '第一个数取 `start[0] = {now}`：越小，给后面留的空间越大',
        'flag = True': '`flag` 记录能否取完所有区间',
        'for v in start[1:]': lambda S, B, r: ('所有区间都取到了数 → 循环结束' if B.get('v') == S.v and S.v == max(START)
                                               else f'看下一个区间，左端点 `v = {S.v}`'),
        14: lambda S, B, r: (f'`now + mid = {S.now + S.mid} <= v = {S.v}` → 成立：直接取 `v`' if S.now + S.mid <= S.v
                             else f'`now + mid = {S.now + S.mid} > v = {S.v}` → 不成立：取不到 `v`，再看右端点'),
        16: lambda S, B, r: (f'`{S.now} + {S.mid} = {S.now + S.mid} <= v + d = {S.v + D}` → 取 `now + mid`'
                             if S.now + S.mid <= S.v + D else f'`{S.now} + {S.mid} = {S.now + S.mid} > v + d = {S.v + D}` → 取不到'),
        'now = v': '`now = {now}`：左端点已经够远，取最靠左的 `v`',
        'now += mid': '`now = {now}`：与上一个数恰好差 `{mid}`',
        'flag = False': '`now + mid` 超出区间右端点 → `mid = {mid}` ==太大，取不到==',
        'break': '已经失败，不用看后面的区间了',
        'if flag': lambda S, B, r: (f'`flag = True`：差 `{S.mid}` 可行 → 答案 `>= {S.mid}`' if S.flag
                                    else f'`flag = False`：差 `{S.mid}` 不行 → 答案 `< {S.mid}`'),
        'left = mid': '可行，`left = {left}`（`mid` 本身还可能是答案，所以不 +1）',
        'right = mid - 1': '不行，`right = {mid} - 1 = {right}`（`mid` 已被排除）',
        'return left': '`left == right` → 最大的最小差 =={ret}==',
    },
    cards=dict(
        one_liner='二分「最小差」mid，再贪心：每个数取最靠前的',
        complexity='时间 `O(n log n + n log A)`，空间 `O(1)`',
        problem=['`start[i]` 对应区间 `[start[i], start[i] + d]`，每个区间选一个整数',
                 '所选整数两两差的绝对值的==最小值==要尽量大',
                 '示例：`start = [6,0,3], d = 2` → `4`；本视频：`[6,0,1], d = 2` → `3`'],
        quote='在确定了mid之后，贪心的标准就确定下来了，即在满足相邻数对差大于等于mid的前提下，让当前区间的取数尽量靠前。',
        quote_src='—— yiduobo 题解原文',
        idea=['最小差一定出在==相邻==的数之间 → 先按起点排序',
              '纯贪心标准不好定：取小了差不够，取大了挤占后面',
              '二分定下 mid 后：`now + mid <= v` 取 `v`，否则取 `now + mid`，超出右端点就失败'],
        summary=['时间 `O(n log n + n log A)`，空间 `O(1)`',
                 '`mid = (left + right + 1) // 2` 上取整，配 `left = mid`，否则死循环',
                 '`right = mid - 1`：不可行的 mid 直接排除',
                 '对比灵神：灵神用开区间 + `x = max(x + score, s)`，这里分两种情况写',
                 '原文已是 Python 3 可运行，没有改动'],
    ),
)
