ARR = ['A', '1', 'B', 'C', 'D', '2', '3']
N = len(ARR)
REL = [0]
for _v in ARR:
    REL.append(REL[-1] + (-1 if _v[0].isdigit() else 1))
ANS = ['1', 'B', 'C', 'D', '2', '3']

CODE = '''
class Solution:
    def findLongestSubarray(self, array: List[str]) -> List[str]:
        begin = end = 0
        s = n = len(array)
        first = [-1] * (n * 2 + 1)
        first[s] = 0  # s[0] = 0
        for i, v in enumerate(array, 1):
            s += -1 if v[0].isdigit() else 1
            j = first[s]
            if j < 0:
                first[s] = i
            elif i - j > end - begin:
                begin, end = j, i
        return array[begin:end]
'''
_LINES = CODE.strip('\n').split('\n')


def _ln(sub):
    return next(i + 1 for i, l in enumerate(_LINES) if sub in l)


L_FOR, L_S, L_J, L_IF, L_SET, L_ELIF, L_UPD, L_RET = (
    _ln('for i, v in'), _ln('s += -1'), _ln('j = first[s]'), _ln('if j < 0'), _ln('first[s] = i'),
    _ln('elif i - j'), _ln('begin, end = j, i'), _ln('return array'))


def _done(S, B):
    """已经算出前缀和的最后一个前缀下标"""
    if 'i' not in S:
        return 0
    if S.get('_line') == L_FOR and B.get('i') != S['i']:
        return S['i'] - 1
    return S['i']


def _cur(S, B):
    """正在处理的元素下标（i - 1）；循环外 / 遍历结束为 None"""
    i = S.get('i')
    if i is None or S.get('_line') == L_RET or (S.get('_line') == L_FOR and B.get('i') == i):
        return None
    return i - 1


def _pair(S, B):
    """(j, i)：当前前缀和与首次出现位置配成的一对；没有则 None"""
    if S.get('_line') in (L_J, L_IF, L_ELIF, L_UPD) and 'j' in S and S['j'] >= 0 and S.get('i') == _done(S, B):
        return S['j'], S['i']
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ncol = N + 1
    W = x1 - x0 - 150
    cw = min(120, W / ncol)
    sx = x0 + 120 + (W - cw * ncol) / 2
    X = lambda j: sx + j * cw + cw / 2
    D = _done(S, B)
    L = S.get('_line')
    i = S.get('i')
    first = S.get('first') or []
    fset = {v for v in first if v >= 0}
    begin, end = S.get('begin', 0), S.get('end', 0)
    pr = _pair(S, B)
    cv.text((x0 + 18, y0 + 4), '字母 +1、数字 −1：前缀和折线（紫 = 首次出现，黄 = 当前，绿线 = 两个相同前缀和之间）', 21, T['muted'], bold=True)
    ya, ch = y0 + 66, 66
    cv.text((sx - 14, ya + ch / 2), 'array', 22, T['muted'], anchor='rm', bold=True)
    if end > begin:
        a, b = X(begin + 1) - cw / 2 + 2, X(end) + cw / 2 - 2
        cv.rect((a, ya - 8, b, ya + ch + 8), fill=T['green'], alpha=50, r=12)
        cv.rect((a, ya - 8, b, ya + ch + 8), outline=T['green'], width=3, r=12)
    cur = _cur(S, B)
    for j in range(1, ncol):
        xc = X(j)
        v = ARR[j - 1]
        dig = v[0].isdigit()
        done = j <= D
        is_cur = cur == j - 1
        c = T['orange'] if dig else T['cyan']
        bw = cw - 12
        cv.rect((xc - bw / 2, ya, xc + bw / 2, ya + ch), fill=c if done else T['panel2'],
                outline=T['pink'] if is_cur else T['border'], width=4 if is_cur else 1, r=10)
        cv.text((xc, ya + 26), v, 28, T['bg'] if done else T['muted'], anchor='mm', bold=True)
        cv.text((xc, ya + 52), '−1' if dig else '+1', 20, T['bg'] if done else T['dim'], anchor='mm', bold=True)
        cv.text((xc, ya - 14), j - 1, 16, T['dim'], anchor='mb', mono=True)
    # 折线图
    top, bot = ya + ch + 56, y1 - 40
    lo, hi = min(REL), max(REL)
    Y = lambda v: bot - (bot - top) * (v - lo) / max(1, hi - lo)
    for v in range(lo, hi + 1):
        cv.line([(sx, Y(v)), (sx + cw * ncol, Y(v))], T['border'], 1)
        cv.text((sx - 10, Y(v)), f'{v:+d}' if v else '0', 20, T['dim'], anchor='rm', mono=True)
    cv.text((x0 + 18, top - 34), '纵轴：字母数 − 数字数', 18, T['muted'], anchor='la')
    pts = [(X(j), Y(REL[j])) for j in range(0, D + 1)]
    if len(pts) > 1:
        cv.line(pts, T['muted'], 3)
    if pr:
        j, ii = pr
        yy = Y(REL[ii])
        cv.line([(X(j), yy), (X(ii), yy)], T['green'], 6)
        lab = f'长度 {ii} − {j} = {ii - j}'
        lw = cv.tlen(lab, 22, bold=True)
        mx = (X(j) + X(ii)) / 2
        cv.rect((mx - lw / 2 - 8, yy - 40, mx + lw / 2 + 8, yy - 8), fill=T['panel'], r=6, alpha=235)
        cv.text((mx, yy - 10), lab, 22, T['green'], anchor='mb', bold=True)
    for j in range(0, D + 1):
        cx, cy = X(j), Y(REL[j])
        is_new = j == D and L in (L_S, L_J, L_IF, L_SET, L_ELIF, L_UPD)
        r, c = (13, T['yellow']) if is_new else ((10, T['purple']) if j in fset else (8, (120, 128, 140)))
        if pr and j == pr[0]:
            r, c = 13, T['green']
        cv.rect((cx - r, cy - r, cx + r, cy + r), fill=c, r=r)
        cv.text((cx, bot + 10), f's[{j}]', 17, T['yellow'] if is_new else T['dim'], anchor='mt', mono=True)


def _fx(S, B):
    L = S.get('_line')
    if 'i' not in S or L in (None,) or L <= _ln('first[s] = 0'):
        return '「字母数 = 数字数」⇔ 字母 +1、数字 −1 后 ==子数组和为 0== ⇔ 两个前缀和相同'
    i, n = S['i'], S['n']
    if L == L_RET:
        return f"答案 `array[{S['begin']}:{S['end']}]`，长度 ==`{S['end'] - S['begin']}`=="
    if L == L_FOR and B.get('i') == i:
        return '遍历结束，最长的那一段就是答案'
    if L in (L_FOR, L_S):
        d = _done(S, B)
        return f"字母数 − 数字数 = `{S['s'] - n}`" if L == L_S else f"处理 `array[{i - 1}] = {S['v']!r}`"
    j = S['j']
    if L in (L_J, L_IF):
        return (f"`s[{i}]` 与 `s[{j}]` 相同 → 中间字母数 = 数字数" if j >= 0 else f"这个前缀和 `{S['s'] - n}` 第一次出现")
    if L == L_SET:
        return f"首次出现：`first[{S['s']}] = {i}`（差值 `{S['s'] - n}` 记在位置 {i}）"
    if L == L_ELIF:
        return f"`{i} − {j} = {i - j}` 对比当前最长 `{S['end'] - S['begin']}`"
    return f"更新为 `[{S['begin']}, {S['end']})`，长度 {S['end'] - S['begin']}"


CONFIG = dict(
    num='面试题 17.05', title='字母与数字', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 首次出现位置（数组代替哈希表）',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code=CODE,
    call=f'Solution().findLongestSubarray({ARR})',
    expect=ANS,
    views=[
        dict(type='text', fn=_fx, h=80, size=26),
        dict(type='custom', draw=_draw, h=400),
        dict(type='array', var='first', label='first（下标 = s；值 = 首次出现的位置，−1 = 没出现；下标 n ⇔ 差 0）',
             cell=64, h=170, pointers={'s': 'blue'},
             color=lambda S, i, v: 'purple' if v >= 0 else None, dim=lambda S, i, v: v < 0),
    ],
    watch=[('i', 'i', 'blue'), ('v', 'v', 'pink'), ('s', 's', 'blue'), ('j', 'j', 'purple'),
           ('begin', 'begin', 'green'), ('end', 'end', 'green')],
    captions={
        'begin = end = 0': '最长子数组记作左闭右开 `[begin, end)`，一开始是空的',
        's = n = len(array)': lambda S, B, ret: (f'`s` 是「字母数 − 数字数」的前缀和，范围 `[−n, n]`；'
                                                 f'为避免负下标让它从 `n = {S.n}` 起步：下标 `n` ⇔ 差 0'),
        'first = [-1]': lambda S, B, ret: (f'`first[v]`：前缀和 `v` ==第一次==出现的位置；长 `2n + 1 = {len(S.first)}`，'
                                           f'`-1` = 没出现过'),
        'first[s] = 0': '空前缀 `s[0]` 的差是 0，下标 `s = n`，先记在位置 0',
        'for i, v in enumerate': lambda S, B, ret: (f'取 `array[{S.i - 1}] = {S.v!r}`，处理完得到前缀和 `s[{S.i}]`'
                                                    if B.get('i') != S.i or 'i' not in B else '遍历结束'),
        's += -1 if': lambda S, B, ret: (f'`{S.v!r}` 是{"数字 → −1" if S.v[0].isdigit() else "字母 → +1"}：'
                                         f'`s = {B.s} → {S.s}`，字母数 − 数字数 = `{S.s - S.n}`'),
        'j = first[s]': lambda S, B, ret: (f'查 `first[{S.s}]`：这个前缀和首次出现在位置 `{S.j}`' if S.j >= 0
                                           else f'查 `first[{S.s}]`：`-1`，还没出现过'),
        'if j < 0': lambda S, B, ret: ('`j < 0`：首次遇到这个前缀和' if S.j < 0
                                       else f'`j = {S.j} ≥ 0`：出现过 → `array[{S.j}:{S.i}]` 字母数 = 数字数'),
        'first[s] = i': '==只记第一次==出现的位置 `first[{s}] = {i}`：越早出现，以后配出的子数组越长',
        'elif i - j': lambda S, B, ret: (f'长 `{S.i} − {S.j} = {S.i - S.j}`，当前最长 `{S.end - S.begin}`：'
                                         + ('==更长==，更新' if S.i - S.j > S.end - S.begin else '不更长，保持（严格 `>`，等长留左端点小的）')),
        'begin, end = j, i': '更新答案：`[begin, end) = [{begin}, {end})`，即 `{array[begin:end]}`',
        'return array': '返回 `array[{begin}:{end}]` = `{ret}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='字母记 +1、数字记 −1，求和为 0 的最长子数组：前缀和相同的最远一对',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组里是字母和数字，找最长的子数组，使其中==字母个数 = 数字个数==',
                 '有多个最长的，返回左端点最小的；不存在就返回空数组',
                 '示例：`["A","A"]` → `[]`',
                 '本视频：`[A,1,B,C,D,2,3]` → `[1,B,C,D,2,3]`'],
        quote='如果 array[i][0] 是字母，则把 array[i] 视作 1；如果是数字，则视作 −1。……问题变成「找到一个最长子数组，其元素和等于 0」。',
        quote_src='—— 灵茶山艾府题解',
        idea=['「字母个数 = 数字个数」⇔ 字母 +1、数字 −1 后，子数组和 ==等于 0==',
              '和为 0 ⇔ 两个前缀和相同：要找 `s[right] == s[left]` 且 `right − left` 最大',
              '`first` 记每个前缀和==首次==出现的位置；`s` 在 `[−n, n]` 内，用长 `2n + 1` 的数组代替哈希表，`s` 从 `n` 起步避免负下标'],
        result='返回 `[1, B, C, D, 2, 3]`：3 个字母、3 个数字，长度 6',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '==只记首次位置==：同一个前缀和出现得越早，配出的子数组越长；更新用严格 `>`，等长时保留左端点更小的',
                 '`s` 初值取 `n` 而不是 0：数组下标不能为负；`first[s] = 0` 对应空前缀',
                 '不能用双指针：前缀和不单调，没有单调性',
                 '另一种写法：`accumulate` 先算前缀和数组 + 字典；相似题：560、974、525'],
    ),
)
