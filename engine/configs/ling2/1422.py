S0 = '011101'
N = len(S0)
TOTAL1 = S0.count('1')
SCORES = [S0[:k + 1].count('0') + S0[k + 1:].count('1') for k in range(N - 1)]   # 分割线在 s[k] 右侧时的得分


def _p(S):
    """分割线左边已有几个字符（= left0 + 已移到左边的 1 的个数）"""
    if 'left0' not in S or 'right1' not in S:
        return 0
    return S['left0'] + (TOTAL1 - S['right1'])


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    p = _p(S)
    line = S.get('_line')
    moving = 'c' in S and p < N - 1 and line in (5, 6)  # for / if 行：s[p] 正要跨过分割线
    cell = min(110, (x1 - x0 - 80) / N)
    sx = x0 + 40 + ((x1 - x0 - 80) - cell * N) / 2
    ys = y0 + 130
    ch = cell * 0.85
    cv.text((x0 + 18, y0 + 4), 's（绿 = 左边的 0，蓝 = 右边的 1，粉框 = 正要跨过分割线的字符）', 22, T['muted'], bold=True)
    if p > 0:
        cv.rect((sx - 6, ys - 44, sx + p * cell + 6, ys + ch + 8), fill=T['green'], alpha=30, r=12)
    cv.rect((sx + p * cell - 6, ys - 44, sx + N * cell + 6, ys + ch + 8), fill=T['blue'], alpha=24, r=12)
    if 'left0' in S:
        cv.text((sx + p * cell - 12, ys - 40), f"左边 0 的个数 left0 = {S['left0']}", 22, T['green'], anchor='ra', bold=True)
    if 'right1' in S:
        cv.text((sx + p * cell + 12, ys - 40), f"右边 1 的个数 right1 = {S['right1']}", 22, T['blue'], anchor='la', bold=True)
    for i, ch_ in enumerate(S0):
        X = sx + i * cell
        good = (i < p and ch_ == '0') or (i >= p and ch_ == '1')
        fill = (T['green'] if i < p else T['blue']) if good and 'right1' in S else T['panel2']
        cv.rect((X + 5, ys, X + cell - 5, ys + ch), fill=fill, r=10, outline=T['border'])
        cv.text((X + cell / 2, ys + ch / 2), ch_, 38, T['bg'] if fill != T['panel2'] else T['muted'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, ys + ch + 12), i, 18, T['dim'], anchor='mt', mono=True)
        if moving and i == p:
            cv.rect((X + 1, ys - 4, X + cell - 1, ys + ch + 4), outline=T['pink'], width=5, r=12)
    # 分割线
    X = sx + p * cell
    cv.line([(X, ys - 14), (X, ys + ch + 40)], T['yellow'], 5)
    cv.text((X, ys + ch + 44), '分割线', 20, T['yellow'], anchor='mt', bold=True)
    # 每个分割位置的得分（已经算过的）
    yb = ys + ch + 130
    cv.text((x0 + 18, yb - 8), '每条分割线的得分（只到 n−2：两边都要非空）', 22, T['muted'], bold=True)
    done = p - 1 if line in (7, 9) else p   # 7/9 行：字符刚跨过分割线，这条线的得分还没算
    best = max(SCORES[:done]) if done > 0 else None
    for k in range(N - 1):
        X = sx + (k + 1) * cell
        known = k < done
        hot = known and SCORES[k] == best
        cv.rect((X - cell / 2 + 8, yb + 30, X + cell / 2 - 8, yb + 30 + cell * 0.7),
                fill=T['orange'] if hot else ((52, 60, 72) if known else T['panel2']), r=8, outline=T['border'])
        cv.text((X, yb + 30 + cell * 0.35), SCORES[k] if known else '?', 30, T['bg'] if hot else (T['text'] if known else T['dim']),
                anchor='mm', bold=True)
        cv.text((X, yb + 36 + cell * 0.7), f'{S0[:k + 1]}|{S0[k + 1:]}', 15, T['dim'], anchor='mt', mono=True)


def _cap_for(S, B, ret):
    p = _p(S)
    if p >= N - 1:
        return '只遍历 `s[:-1]`：分割线不能移到最右边（右边必须==非空==）→ 循环结束'
    return f'取 `c = s[{p}] = \'{S.c}\'`，准备把它从分割线右边==移到左边=='


def _cap_ans(S, B, ret):
    p = _p(S)
    sc = S.left0 + S.right1
    tail = '，==刷新最大值==' if S.ans > B.ans else ''
    return f'分割 `{S0[:p]} | {S0[p:]}`：得分 `left0 + right1 = {S.left0} + {S.right1} = {sc}` → `ans = {S.ans}`{tail}'


CONFIG = dict(
    num=1422, title='分割字符串的最大得分', difficulty='Easy', category='子串',
    author='灵茶山艾府', technique='枚举分割线 · 前后缀分解',
    tags=['List.md'],
    code='''
class Solution:
    def maxScore(self, s: str) -> int:
        right1 = s.count('1')
        ans = left0 = 0
        for c in s[:-1]:  # 移动分割线
            if c == '0':
                left0 += 1
            else:
                right1 -= 1
            ans = max(ans, left0 + right1)
        return ans
''',
    call=f'Solution().maxScore("{S0}")',
    expect=5,
    views=[
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=[('c', 'c', 'pink'), ('left0', 'left0', 'green'), ('right1', 'right1', 'blue'), ('ans', 'ans', 'orange')],
    captions={
        "right1 = s.count('1')": '分割线先放在最左边：右边是整个 `s`，`right1` = `s` 中 `1` 的个数 = =={right1}==',
        'ans = left0 = 0': '左边还没有字符：`left0 = 0`，`ans = 0`',
        'for c in s[:-1]': _cap_for,
        "if c == '0'": lambda S, B, r: ("`c = '0'` → 它到了左边，左边==多了一个 0==" if S.c == '0'
                                        else "`c = '1'` → 它离开了右边，右边==少了一个 1=="),
        'left0 += 1': '`left0` → {left0}',
        'right1 -= 1': '`right1` → {right1}：这个 1 之前在分割线右侧，现在属于左侧了',
        'ans = max': _cap_ans,
        'return ans': '所有分割线都试过，最大得分 =={ret}==',
    },
    cards=dict(
        one_liner='枚举分割线的位置，边移动边维护左边 0 的个数和右边 1 的个数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 01 字符串 `s` 分成==非空==的左、右两段',
                 '得分 = 左段里 `0` 的个数 + 右段里 `1` 的个数，求最大得分',
                 '示例：`s = "011101"` → `5`（`"0" | "11101"`：1 + 4）'],
        quote='核心思想：==枚举分割线的位置，维护 0 和 1 的个数==。……否则 s[i] = 1，那么把 right1 减少 1。因为 s[i] 之前在分割线右侧，现在属于分割线左侧了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先统计整个 `s` 的 1 的个数，作为分割线在最左边时的 `right1`',
              '分割线每右移一格，就有一个字符从右边跑到左边：`0` 让 `left0 + 1`，`1` 让 `right1 − 1`',
              '每次移动后算 `left0 + right1`，取最大'],
        summary=['时间 `O(n)`，空间 `O(1)`（`s[:-1]` 切片另占 `O(n)`）',
                 '易错：只能枚举到 `n−2`，所以遍历 `s[:-1]`；分割线不能在最左/最右',
                 '写法二：把两个变量合成 `score`，遇 0 加一、遇 1 减一',
                 '写法三：一次遍历，同时统计 1 的总数和 `±1` 的最大增量',
                 '同类：前后缀分解'],
    ),
)
