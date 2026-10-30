M = [["1", "0", "1", "1"],
     ["1", "1", "1", "1"],
     ["0", "1", "1", "1"]]

L_UPD = (15, 17)          # 计算柱子高度的两行
L_MAIN = (20, 21, 22, 24, 25, 27)
L_TAIL = (29, 30, 31, 32, 34)


def _expected(r):
    h = [0] * len(M[0])
    for k in range(r + 1):
        for j in range(len(h)):
            h[j] = 0 if M[k][j] == '0' else h[j] + 1
    return h


def _rect(S):
    """(左, 右, 高) of the rectangle whose area is being computed on this step"""
    ln, st, hs, j = S['_line'], S.get('stack'), S.get('height'), S.get('j')
    if not st or j is None:
        return None
    if ln == 22:
        return st[-2] + 1, j - 1, hs[st[-1]]
    if ln == 24:
        return 0, j - 1, hs[st[-1]]
    if ln == 32:
        return 0, st[-1], hs[st[0]]
    if ln == 34:
        return st[j - 1] + 1, st[-1], hs[st[j]]
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 2), 'matrix（青 = 以第 i 行为基底的柱子，黄框 = 正在计算的矩形）', 22, T['muted'], bold=True)
    R, C = len(M), len(M[0])
    cell = min(78, (y1 - y0 - 130) / R)
    gx, gy = x0 + 150, y0 + 42
    r = S.get('i')
    hs = S.get('height')
    cur = _expected(r) if r is not None else None
    for i in range(R):
        cv.text((gx - 18, gy + i * cell + cell / 2), f'i={i}' + ('（基底）' if i == r else ''), 20,
                T['cyan'] if i == r else T['dim'], anchor='rm', bold=i == r)
        for j in range(C):
            X, Y = gx + j * cell, gy + i * cell
            fill = T['panel2']
            if hs is not None and r is not None:
                h = hs[j]
                base = r if h == cur[j] else r - 1
                if h > 0 and base - h + 1 <= i <= base:
                    fill = (24, 110, 104)
            cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), fill=fill, r=6,
                    outline=T['cyan'] if i == r else None, width=2)
            cv.text((X + cell / 2, Y + cell / 2), M[i][j], 30, T['text'] if M[i][j] == '1' else T['dim'], anchor='mm', mono=True, bold=True)
    hy = gy + R * cell + 14
    cv.text((gx - 18, hy + 20), 'height', 20, T['muted'], anchor='rm', bold=True)
    if hs is None:
        return
    st = S.get('stack') or []
    ln = S['_line']
    for j, h in enumerate(hs):
        X = gx + j * cell
        instack = ln not in L_UPD and j in st
        col = T['purple'] if instack else (T['text'] if (r is None or h == cur[j]) else T['muted'])
        cv.text((X + cell / 2, hy + 20), h, 28, col, anchor='mm', mono=True, bold=True)
        cv.text((X + cell / 2, hy + 48), j, 16, T['dim'], anchor='mm')
    jj = S.get('j')
    if isinstance(jj, int) and ln in L_MAIN:
        X = gx + jj * cell + cell / 2
        cv.tri_up(X, hy + 64, 8, T['pink'])
        cv.text((X, hy + 74), 'j', 20, T['pink'], anchor='mt', bold=True)
    if isinstance(jj, int) and ln in (31, 32, 34) and jj < len(st):
        X = gx + st[jj] * cell + cell / 2
        cv.tri_up(X, hy + 64, 8, T['yellow'])
        cv.text((X, hy + 74), f'stack[{jj}]', 18, T['yellow'], anchor='mt', bold=True)
    rc = _rect(S)
    if rc and rc[2] > 0 and r is not None:
        l, rr, h = rc
        cv.rect((gx + l * cell + 1, gy + (r - h + 1) * cell + 1, gx + (rr + 1) * cell - 1, gy + (r + 1) * cell - 1),
                outline=T['yellow'], width=5, r=8)


def _formula(S):
    rc = _rect(S)
    if rc:
        l, rr, h = rc
        return f'矩形：列 `{l}..{rr}`，高 `{h}` → 面积 `{h} × {rr - l + 1}` = =={h * (rr - l + 1)}=='
    if S['_line'] in L_TAIL:
        return '收尾：栈里剩下的柱子，==右边界都是最后一列== `stack[-1]`'
    if S['_line'] in L_MAIN:
        return '栈中柱子高度递增：当前柱子更矮时，栈顶的==右边界找到了=='
    return '把竖着连续的 1 看作柱子，==转化成 84 题=='


def _upd1(S, B, ret):
    return f'`matrix[{S.i}][{S.j}] = 1` → 柱子接着往下长：`height[{S.j}]` → {S.height[S.j]}'


def _upd0(S, B, ret):
    return f'`matrix[{S.i}][{S.j}] = 0` → ==悬空的柱子不能要==，`height[{S.j}] = 0`'


def _while(S, B, ret):
    st, hs, j = B.stack, B.height, B.j
    if not st:
        return f'`j = {j}`：栈空，直接入栈'
    t = st[-1]
    if hs[t] > hs[j]:
        return f'`j = {j}`：栈顶 `height[{t}] = {hs[t]}` > `{hs[j]}` → 栈顶的==右边界是 j−1==，计算它'
    return f'`j = {j}`：栈顶 `height[{t}] = {hs[t]}` ≤ `{hs[j]}` → 停止，`j` 入栈'


def _res_mid(S, B, ret):
    st, hs, j = S.stack, S.height, S.j
    t = st[-1]
    return f'左边界是 `stack[-2] + 1 = {st[-2] + 1}`：面积 `{hs[t]} × ({j} − {st[-2]} − 1)` = `{hs[t] * (j - st[-2] - 1)}`，`res = {S.res}`'


def _res_one(S, B, ret):
    st, hs, j = S.stack, S.height, S.j
    t = st[-1]
    return f'栈里只有它 → 左边全比它高，宽就是 `j = {j}`：面积 `{hs[t] * j}`，`res = {S.res}`'


def _res_t0(S, B, ret):
    st, hs = S.stack, S.height
    return f'`stack[0]` 是最矮的，==从第 0 列延伸到最后一列==：`{hs[st[0]]} × {st[-1] + 1}` = `{hs[st[0]] * (st[-1] + 1)}`，`res = {S.res}`'


def _res_tj(S, B, ret):
    st, hs, j = S.stack, S.height, S.j
    return f'`stack[{j}]` 左边界是 `stack[{j - 1}] + 1`：`{hs[st[j]]} × ({st[-1]} − {st[j - 1]})` = `{hs[st[j]] * (st[-1] - st[j - 1])}`，`res = {S.res}`'


CONFIG = dict(
    num=85, title='最大矩形', difficulty='Hard', category='栈',
    author='yiduobo', technique='逐行转化为 84 题 · 单调栈',
    tags=['热题173'],
    code='''
class Solution(object):
    def maximalRectangle(self, matrix):

        if not matrix:
            return 0

        m = len(matrix)
        n = len(matrix[0])

        res = 0
        height = [0] * n
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == '1':
                    height[j] += 1
                else:
                    height[j] = 0
            stack = []
            for j in range(n):
                while len(stack) > 0 and height[stack[-1]] > height[j]:
                    if len(stack) > 1:
                        res = max(res, height[stack[-1]]* (j - stack[-2] - 1))
                    else:
                        res = max(res, height[stack[-1]] * j)
                    stack.pop()

                stack.append(j)

            if len(stack) > 0:
                for j in range(len(stack)):
                    if j == 0:
                        res = max(res, height[stack[j]] * (stack[-1] + 1))
                    else:
                        res = max(res, height[stack[j]] * (stack[-1] - stack[j - 1]))

        return res
''',
    call=f'Solution().maximalRectangle({M})',
    expect=6,
    skip=[13, 14, 19, 21, 25, 29, 30, 31, 'if not matrix', 'm = len', 'n = len'],
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='stack', var=lambda S: S.get('stack') if S['_line'] not in L_UPD else None,
             label='stack（存下标，对应柱子高度递增）', h=95),
        dict(type='text', fn=_formula, size=26),
    ],
    watch=[('i', 'i', 'cyan'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录最大面积；`height[j]`：第 j 列以当前行为基底的柱子高度',
        'height = [0] * n': '`height` 先全为 0',
        'for i in range(m)': lambda S, B, ret: (f'以第 `i = {S.i}` 行为基底，关注前 {S.i + 1} 行' if B.get('i') != S.i
                                                 else f'所有行处理完，`res = {S.res}`'),
        'height[j] += 1': _upd1,
        'height[j] = 0': _upd0,
        'stack = []': '`height = {height}`：现在就是 84 题，用单调栈求最大矩形',
        'while len(stack) > 0': _while,
        22: _res_mid,
        24: _res_one,
        'stack.append(j)': '`{j}` 入栈（栈中柱子高度递增）',
        32: _res_t0,
        34: _res_tj,
        'return res': '最大矩形面积 =={ret}==',
    },
    max_steps=80,
    cards=dict(
        one_liner='以每一行为基底，把竖着连续的 1 看成柱子，转化成 84 题',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['`rows × cols` 的 `0/1` 矩阵，找==只包含 1==的最大矩形，返回面积',
                 '示例 1：4×5 矩阵 → `6`',
                 '本视频：`[[1,0,1,1],[1,1,1,1],[0,1,1,1]]` → `6`'],
        quote='我们可以从上往下，每次关注前k行。具体来说就是==以第k行为基底，将竖着的连续的1看做上一题中的柱子==，将题目转化成上一题。当然，这里悬空的柱子是不能要的。',
        quote_src='—— yiduobo 题解原文',
        idea=['示例的柱子：`1 0 1 0 0` / `2 0 2 1 1` / `3 1 3 2 2` / `4 0 0 3 0`',
              '答案是 `3 1 3 2 2` 这一行后三个柱子 `3 2 2` 组成的面积 `6`',
              '每行先从左往右算柱子高度，再从左往右用单调栈算矩形面积'],
        result='第 2 行为基底时找到面积 `6` ✓',
        summary=['时间 `O(mn)`，空间 `O(n)`',
                 '弹栈条件是严格 `>`：相等的柱子留在栈里，收尾时统一计算',
                 '收尾：栈里剩下的柱子右边界都是最后一列 `stack[-1]`，左边界是栈中前一个 + 1',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神在末尾补 0 哨兵，省掉了 yiduobo 的收尾循环'],
    ),
)
