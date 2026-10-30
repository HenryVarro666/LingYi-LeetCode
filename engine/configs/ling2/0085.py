M = [["1", "0", "1", "1"],
     ["1", "1", "1", "1"],
     ["0", "1", "1", "1"]]
ROWMAX = [2, 4, 6]   # 每一行做一次 84 题的结果（用来在 84 题内部显示全局 ans）


def _row(S):
    """当前底边是第几行"""
    row = S.get('row')
    if row is None:
        return None
    for k, r in enumerate(M):
        if r is row or (S.get('matrix') is not None and S['matrix'][k] is row):
            return k
    return None


def _inside(S):
    return 'st' in S


def _active(S):
    return _inside(S) and S['_line'] in (9, 10) and isinstance(S.get('left'), int) and isinstance(S.get('i'), int)


def _expected(r):
    h = [0] * len(M[0])
    for k in range(r + 1):
        for j in range(len(h)):
            h[j] = 0 if M[k][j] == '0' else h[j] + 1
    return h


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 2), 'matrix（蓝 = 以当前行为底的柱子，黄框 = 正在结算的矩形）', 22, T['muted'], bold=True)
    R, C = len(M), len(M[0])
    cell = min(78, (y1 - y0 - 130) / R)
    gx = x0 + 150
    gy = y0 + 42
    r = _row(S)
    hs = S.get('heights')
    cur = _expected(r) if r is not None else None
    prev = _expected(r - 1) if r is not None and r > 0 else [0] * C
    for i in range(R):
        cv.text((gx - 18, gy + i * cell + cell / 2), f'行 {i}' + ('（底）' if i == r else ''), 20, T['cyan'] if i == r else T['dim'], anchor='rm', bold=i == r)
        for j in range(C):
            X, Y = gx + j * cell, gy + i * cell
            fill = T['panel2']
            if hs is not None and r is not None and j < C:
                h = hs[j]
                base = r if h == cur[j] else r - 1
                if h > 0 and base - h + 1 <= i <= base:
                    fill = (40, 84, 140)
            cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), fill=fill, r=6,
                    outline=T['cyan'] if i == r else None, width=2)
            cv.text((X + cell / 2, Y + cell / 2), M[i][j], 30, T['text'] if M[i][j] == '1' else T['dim'], anchor='mm', mono=True, bold=True)
    # sentinel column
    Xs = gx + C * cell
    cv.dashed((Xs + 8, gy + 4), (Xs + 8, gy + R * cell - 4), T['border'], 2)
    # heights row
    hy = gy + R * cell + 14
    cv.text((gx - 18, hy + 20), 'heights', 20, T['muted'], anchor='rm', bold=True)
    if hs is not None:
        for j, h in enumerate(hs):
            X = gx + j * cell
            col = T['red'] if j == C else (T['text'] if (r is None or h == cur[j]) else T['muted'])
            cv.text((X + cell / 2, hy + 20), h, 28, col, anchor='mm', mono=True, bold=True)
            cv.text((X + cell / 2, hy + 48), '哨兵' if j == C else j, 16, T['dim'], anchor='mm')
        # pointers inside the 84 call
        if _inside(S):
            for name, c, dy in (('right', T['pink'], 0), ('left', T['blue'], 22)):
                v = S.get(name)
                if isinstance(v, int) and (name == 'right' or _active(S)):
                    X = gx + v * cell + cell / 2 if v >= 0 else gx - cell / 2
                    cv.tri_up(X, hy + 64, 8, c)
                    cv.text((X, hy + 74 + dy), name if v >= 0 else 'left=-1', 18, c, anchor='mt', bold=True)
    if _active(S):
        i, left, right = S['i'], S['left'], S['right']
        h = hs[i]
        if h > 0:
            cv.rect((gx + (left + 1) * cell + 1, gy + (r - h + 1) * cell + 1, gx + right * cell - 1, gy + (r + 1) * cell - 1),
                    outline=T['yellow'], width=5, r=8)


def _stack_fmt(i):
    return '-1' if i == -1 else f'{i}'


def _formula(S):
    if _active(S):
        i, l, rr, hs = S['i'], S['left'], S['right'], S['heights']
        ls = l if l >= 0 else f'({l})'
        return f'高 `heights[{i}] = {hs[i]}`，宽 `{rr} − {ls} − 1 = {rr - l - 1}` → 面积 =={hs[i] * (rr - l - 1)}=='
    r = _row(S)
    if r is None:
        return '枚举矩形的==底边==，每行做一次 84 题'
    if _inside(S):
        return f'第 {r} 行为底：对 `heights = {S["heights"][:-1]}` 做 84 题'
    return f'第 {r} 行为底：`1` 就在柱子下面==垫一块石头==，`0` 柱子高度归零'


def _best(S):
    r = _row(S)
    if _inside(S):
        return max(ROWMAX[:r], default=0)
    return S.get('ans')


def _for_row(S, B, ret):
    r = _row(S)
    if r is None or _row(B) == r:
        return f'所有底边枚举完，答案 `ans = {S.ans}`'
    if r == 0:
        return '枚举底边：先以第 0 行为底'
    return f'第 {r - 1} 行为底的最大矩形是 `{ROWMAX[r - 1]}`，`ans = {S.ans}`；底边下移到第 {r} 行'


def _while(S, B, ret):
    st, hs, h, rr = B.st, B.heights, B.h, B.right
    tag = '（末尾哨兵）' if rr == len(hs) - 1 else ''
    if len(st) <= 1:
        return f'`right = {rr}`{tag}：栈里只剩 `-1`，不弹'
    j = st[-1]
    if hs[j] >= h:
        return f'`right = {rr}`{tag}：栈顶 `{hs[j]}` ≥ `h = {h}`，扩展不过 right → 弹出结算'
    return f'`right = {rr}`：栈顶 `{hs[j]}` < `h = {h}`，不弹'


def _set0(S, B, ret):
    return f'`matrix[{_row(S)}][{S.j}] = 0` → 悬空的柱子不要，高度归零'


def _add1(S, B, ret):
    return f'`matrix[{_row(S)}][{S.j}] = 1` → ==垫一块石头==，高度 {S.heights[S.j]}'


def _call(S, B, ret):
    return f'以第 {_row(S)} 行为底，`heights = {S.heights[:-1]}`：==调用 84 题=='


CONFIG = dict(
    num=85, title='最大矩形', difficulty='Hard', category='栈',
    author='灵茶山艾府', technique='枚举底边 + 84 题单调栈',
    tags=['热题173'],
    code='''
class Solution:
    # 84. 柱状图中最大的矩形
    def largestRectangleArea(self, heights: List[int]) -> int:
        st = [-1]  # 在栈中只有一个数的时候，栈顶的「下面那个数」是 -1，对应 left[i] = -1 的情况
        ans = 0
        for right, h in enumerate(heights):
            while len(st) > 1 and heights[st[-1]] >= h:
                i = st.pop()  # 矩形的高（的下标）
                left = st[-1]  # 栈顶下面那个数就是 left
                ans = max(ans, heights[i] * (right - left - 1))
            st.append(right)
        return ans

    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        n = len(matrix[0])
        heights = [0] * (n + 1)  # 末尾多一个 0，理由见我 84 题题解
        ans = 0
        for row in matrix:
            # 计算底边为 row 的柱子高度
            for j, c in enumerate(row):
                if c == '0':
                    heights[j] = 0  # 柱子高度为 0
                else:
                    heights[j] += 1  # 柱子高度加一
            ans = max(ans, self.largestRectangleArea(heights))  # 调用 84 题代码
        return ans
''',
    call=f'Solution().maximalRectangle({M})',
    expect=6,
    skip=['for j, c in', "if c == '0'", 'ans = 0', 'for right, h in', 'i = st.pop()', 12],
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='stack', var='st', label='st（84 题的单调栈，存下标）', fmt=_stack_fmt, h=95),
        dict(type='text', fn=_formula, size=26),
    ],
    watch=[('right', 'right', 'pink'), ('i', 'i', 'yellow'), ('left', 'left', 'blue'),
           ('本行最大', lambda S: S['ans'] if 'st' in S else None, 'orange'), ('ans', _best, 'green')],
    captions={
        'n = len(matrix[0])': '`n = {n}` 列',
        'heights = [0] * (n + 1)': '`heights` 多开一格放 `0`：84 题末尾的哨兵，最后把栈清空',
        'for row in matrix': _for_row,
        'heights[j] = 0': _set0,
        'heights[j] += 1': _add1,
        'ans = max(ans, self': _call,
        'st = [-1]': '84 题：栈底放 `-1`，对应 `left = -1`',
        'while len(st) > 1': _while,
        'i = st.pop()': '弹出 `i = {i}`：以 `heights[{i}] = {heights[i]}` 为高，右边界是 `right`',
        'left = st[-1]': '弹出 `i = {i}` 当矩形的高；新栈顶 `left = {left}` 是左边==第一个更矮==的',
        'ans = max(ans, heights[i]': lambda S, B, ret: f'面积 `{S.heights[S.i]} × {S.right - S.left - 1} = {S.heights[S.i] * (S.right - S.left - 1)}`，本行最大 `{S.ans}`',
        'st.append(right)': '`{right}` 入栈',
        26: '最大矩形面积 =={ret}==',
    },
    max_steps=76,
    cards=dict(
        one_liner='枚举矩形的底边，每一行都做一次 84 题',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['`rows × cols` 的 `0/1` 矩阵，找==只包含 1==的最大矩形，返回面积',
                 '示例 1：4×5 矩阵 → `6`',
                 '本视频：`[[1,0,1,1],[1,1,1,1],[0,1,1,1]]` → `6`'],
        quote='我们可以==枚举矩形的底边，做 m 次 84 题==。……如果 matrix[i][j]=0，那么没有柱子，高度等于 0。否则，在上一行柱子的基础上，把柱子高度增加 1。',
        quote_src='—— 灵茶山艾府题解（直接调用 84 题代码）',
        idea=['以第 `i` 行为底：每列向上连续的 1 就是一根柱子',
              '`1` → 柱子下面==垫一块石头==（高度 +1）；`0` → 高度归零',
              '对每行的 `heights` 调用 84 题，取最大值'],
        result='三行的结果 `2, 4, 6`，答案 `6` ✓',
        summary=['时间 `O(mn)`：做 m 次 84 题，每次 `O(n)`；空间 `O(n)`',
                 '`heights` 末尾多一个 `0`：哨兵把栈里的柱子全部弹出结算',
                 '易错：`0` 必须把高度清零，不能只是不加（悬空的柱子不能要）',
                 '84 题是本题的子程序：先把 84 题的单调栈写熟'],
    ),
)
