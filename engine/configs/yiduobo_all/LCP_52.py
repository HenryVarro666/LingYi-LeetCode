OPS = [[1, 2, 6], [0, 4, 8], [1, 0, 3]]


def _get(f, n, pos):
    now, l, r = 0, 0, n - 1
    while not (f[now] != 0 or l == r):
        mid = (l + r) >> 1
        if pos <= mid:
            now, r = now + now + 1, mid
        else:
            now, l = now + now + 2, mid + 1
    return f[now]


def _nodes(n):
    out = []

    def go(now, l, r, d):
        out.append((now, l, r, d))
        if l < r:
            m = (l + r) >> 1
            go(now + now + 1, l, m, d + 1)
            go(now + now + 2, m + 1, r, d + 1)
    go(0, 0, n - 1, 0)
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ln = S.get('_line', 0)
    nl = S.get('num_list') or []
    N = len(nl)
    W = x1 - x0 - 40
    # ---- 1. num_list 条（中序 = 升序），染色后红 / 蓝
    cv.text((x0 + 18, y0 + 2), 'num_list：树的中序遍历 = 升序数组（下标 0 … n−1 就是线段树的叶子）', 21, T['muted'], bold=True)
    if N:
        cw = min(100, W / N)
        sx = x0 + 20 + (W - cw * N) / 2
        f = S.get('f')
        colored = f is not None and ln >= 43
        for i, v in enumerate(nl):
            X = sx + i * cw
            fill = T['panel2']
            tc = T['muted']
            if colored:
                c = _get(f, N, i)
                if c == 1:
                    fill, tc = T['red'], T['bg']
                elif c == 2:
                    fill, tc = T['blue'], T['bg']
            if ln >= 95 and S.get('index') == i:
                cv.rect((X + 1, y0 + 26, X + cw - 1, y0 + 80), outline=T['yellow'], width=4, r=10)
            cv.rect((X + 5, y0 + 30, X + cw - 5, y0 + 78), fill=fill, r=8, outline=T['border'])
            cv.text((X + cw / 2, y0 + 54), v, 28, tc, anchor='mm', bold=True)
            cv.text((X + cw / 2, y0 + 80), i, 16, T['dim'], anchor='mt', mono=True)
    # ---- 2. 映射表：每个值映射到哪个下标
    sm = S.get('sorted_mixed_num_list')
    lm, rm = S.get('left_mapping', {}), S.get('right_mapping', {})
    ty = y0 + 108
    if sm:
        cv.text((x0 + 18, ty), '映射表：树中的值映射到自己的下标，别的值映射到最近的树中值的下标', 21, T['muted'], bold=True)
        m = len(sm)
        cw = min(86, (W - 150) / m)
        sx = x0 + 20 + 150
        cur = S.get('now') if ln in (28, 29, 30, 31, 32, 33, 36, 37, 38, 39, 40, 41) else None
        for r_i, (name, mp, colr) in enumerate((('值', None, None), ('left_mapping', lm, 'cyan'), ('right_mapping', rm, 'orange'))):
            Y = ty + 30 + r_i * 35
            cv.text((sx - 10, Y + 16), name, 17 if r_i else 20, T['muted'] if r_i == 0 else T[colr], anchor='rm', bold=True)
            for k, v in enumerate(sm):
                X = sx + k * cw
                if r_i == 0:
                    cv.rect((X + 2, Y, X + cw - 2, Y + 32), fill=T['panel2'], r=6)
                    cv.text((X + cw / 2, Y + 16), v, 22, T['text'] if v in nl else T['muted'], anchor='mm', bold=True)
                else:
                    val = mp.get(v)
                    hot = cur == v and val is not None
                    base = v in nl
                    fill = T['yellow'] if hot else (T[colr] if base and val is not None else None)
                    cv.rect((X + 2, Y, X + cw - 2, Y + 32), fill=fill, outline=T['border'], r=6, alpha=255 if hot else (90 if base else 255))
                    cv.text((X + cw / 2, Y + 16), '·' if val is None else val, 22, T['bg'] if hot else (T['text'] if val is not None else T['dim']), anchor='mm', bold=True)
    # ---- 3. 线段树
    if ln >= 43 and N:
        f = S.get('f')
        fl = S.get('flag')
        if f is not None and fl is not None:
            top = ty + 30 + 3 * 35 + 62
            cv.text((x0 + 18, top - 44), '线段树：颜色 红 / 蓝；灰 = 混合；橙点 = 整段待下放标记', 21, T['muted'], bold=True)
            nd = _nodes(N)
            lvl = max(d for *_, d in nd)
            gap = min(70, (y1 - top - 50) / max(lvl, 1))
            pos = {}
            for now, l, r, d in nd:
                pos[now] = (x0 + 20 + (l + r + 1) / 2 / N * W, top + 18 + d * gap)
            for now, l, r, d in nd:
                if l < r:
                    for ch in (now + now + 1, now + now + 2):
                        cv.line([pos[now], pos[ch]], T['border'], 2)
            hot = S.get('now') if 47 <= ln <= 73 else None
            for now, l, r, d in nd:
                X, Y = pos[now]
                c = f[now]
                fill = T['red'] if c == 1 else T['blue'] if c == 2 else T['panel2']
                tc = T['bg'] if c else T['muted']
                cv.rect((X - 44, Y - 16, X + 44, Y + 16), fill=fill, outline=T['border'], r=8)
                cv.text((X, Y), f'[{l},{r}]', 22, tc, anchor='mm', bold=True)
                if fl[now]:
                    cv.d.ellipse((X + 36, Y - 24, X + 50, Y - 10), fill=T['orange'])
                if hot == now:
                    cv.rect((X - 50, Y - 22, X + 50, Y + 22), outline=T['yellow'], width=4, r=10)


def _info(S):
    ln = S.get('_line', 0)
    if ln >= 94 and 'res' in S:
        return f'已数到的红色节点 `res` = =={S["res"]}=='
    if ln >= 43 and 'type' in S and 'x' in S and 'right_mapping' in S:
        x, y = S['x'], S['y']
        w = '红' if S['type'] == 1 else '蓝'
        s = f'操作 `[{S["type"]}, {x}, {y}]`：值在 `[{x}, {y}]` 的节点染==={w}==='
        if 'mapped_x' in S and ln >= 47:
            s += f'；映射成下标 `[{S["mapped_x"]}, {S["mapped_y"]}]`'
        return s
    return ''


CONFIG = dict(
    num='LCP 52', title='二叉搜索树染色', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='离散化 · 区间染色线段树',
    tags=['线段树'],
    code='''
class Solution(object):
    def getNumber(self, root, ops):

        num_list = []

        def dfs(now):
            if now.left:
                dfs(now.left)
            num_list.append(now.val)
            if now.right:
                dfs(now.right)

        dfs(root)

        left_mapping = {}
        right_mapping = {}
        p = 0
        for index, num in enumerate(num_list):
            left_mapping[num] = right_mapping[num] = index

        mixed_num_set = set(num_list)
        for _, x, y in ops:
            mixed_num_set.add(x)
            mixed_num_set.add(y)

        sorted_mixed_num_list = sorted(list(mixed_num_set))
        for index in range(len(sorted_mixed_num_list)):
            now = sorted_mixed_num_list[index]
            if now not in left_mapping:
                if index == 0:
                    left_mapping[now] = -1
                else:
                    left_mapping[now] = left_mapping[sorted_mixed_num_list[index - 1]]

        for index in range(len(sorted_mixed_num_list) - 1, -1, -1):
            now = sorted_mixed_num_list[index]
            if now not in right_mapping:
                if index == len(sorted_mixed_num_list) - 1:
                    right_mapping[now] = n
                else:
                    right_mapping[now] = right_mapping[sorted_mixed_num_list[index + 1]]

        n = len(num_list)
        f = [0] * (n * 4)
        flag = [False] * (n * 4)

        def insert(now, left, right, i, j, f, color):
            if left == i and right == j:
                f[now] = color
                flag[now] = True
                return

            if f[now] == color:
                return

            if flag[now]:
                f[now + now + 1] = f[now + now + 2] = f[now]
                flag[now + now + 1] = flag[now + now + 2] = True
                flag[now] = False

            mid = (left + right) >> 1
            if j <= mid:
                insert(now + now + 1, left, mid, i, j, f, color)
            elif i > mid:
                insert(now + now + 2, mid + 1, right, i, j, f, color)
            else:
                insert(now + now + 1, left, mid, i, mid, f, color)
                insert(now + now + 2, mid + 1, right, mid + 1, j, f, color)

            if f[now + now + 1] == f[now + now + 2]:
                f[now] = f[now + now + 1]
            else:
                f[now] = 0

        def get(now, left, right, f, pos):
            if f[now] != 0 or left == right:
                return f[now]

            mid = (left + right) >> 1
            if pos <= mid:
                return get(now + now + 1, left, mid, f, pos)
            else:
                return get(now + now + 2, mid + 1, right, f, pos)

        for type, x, y in ops:
            if right_mapping[x] == n or left_mapping[y] == -1:
                continue

            mapped_x = right_mapping[x]
            mapped_y = left_mapping[y]

            insert(0, 0, n - 1, mapped_x, mapped_y, f, 2 - type)

        res = 0
        for index in range(n):
            if get(0, 0, n - 1, f, index) == 1:
                res += 1

        return res
''',
    call=f'Solution().getNumber(Tr([5,3,7,1,None,None,9]), {OPS})',
    expect=2,
    views=[
        dict(type='tree', h=130),
        dict(type='custom', draw=_draw, h=500),
        dict(type='text', fn=_info, size=26, h=50),
    ],
    watch=[('mapped_x', 'mapped_x', 'blue'), ('mapped_y', 'mapped_y', 'pink'), ('res', 'res', 'green')],
    skip=['left_mapping = {}', 'right_mapping = {}', 'p = 0', 'if now.left', 'dfs(now.left)', 'if now.right', 'dfs(now.right)',
          'for index, num in enumerate', 'left_mapping[num] =', 'mixed_num_set.add', 'for _, x, y in ops',
          'for index in range(len(sorted', 'now = sorted_mixed', 'if now not in', 'if index == ', 'else:',
          'flag[now] = True', 51, 54, 77, 81, 83, 76, 79, 80, 'mid = (left', 'if f[now] == color', 'flag[now] = False', 'flag[now + now + 1]',
          'insert(now + now', 'mapped_x =', 'mapped_y =', 'if right_mapping[x]',
          48, 56, 64, 70, 'num_list = []', 'mixed_num_set = set(', 'for type, x, y in ops', 'def ', 'f = [0]', 'flag = [False]', 'for index in range(n)', 'res += 1'],
    captions={
        'dfs(root)': '先中序遍历：二叉搜索树的中序 ==就是升序数组==',
        'num_list.append(now.val)': '中序遍历访问 `{now.val}`：`num_list` 末尾加入它',
                'sorted_mixed_num_list = sorted': '树中的值已映射到自己的下标；再把操作端点一起去重排序，给不在树里的端点找最近的树中值',
        'left_mapping[now] = -1': '`{now}` 左边没有树中值 → `left_mapping = -1`，作右端点时区间落空',
        'left_mapping[now] = left_mapping[sorted': '`{now}` 不在树里 → 向左找最近的树中值：`left_mapping[{now}] = {left_mapping[now]}`（给右端点 y 用）',
        'right_mapping[now] = n': '右边没有树中值 → `right_mapping = n`（作左端点时区间落空）',
        'right_mapping[now] = right_mapping[sorted': '`{now}` 不在树里 → 向右找最近的树中值：`right_mapping[{now}] = {right_mapping[now]}`（给左端点 x 用）',
        'n = len(num_list)': '树有 `{n}` 个值，下标 `0 … {n-1}`；开线段树：`f` 存颜色（0 = 混合 / 未染），`flag` 存整段标记',
        'for type, x, y in ops': lambda S, B, r: (f'取操作 `[{S.type}, {S.x}, {S.y}]`：`type = 1` 染红，`type = 0` 染蓝' if 'type' in S and ('x' not in B or (B.x, B.y, B.type) != (S.x, S.y, S.type) or S._line != B._line) else '操作处理完，开始数红色'),
        'insert(0, 0, n - 1': lambda S, B, r: f'`x` 向右、`y` 向左映射成区间 `[{B.right_mapping[B.x]}, {B.left_mapping[B.y]}]`，颜色 `2 - type` = `{2 - B.type}`（1 红 2 蓝），开始染色',
        'f[now] = color': '区间恰好等于待染区间 → 整段染成 `{color}`，打上 `flag` 懒标记，不再往下',
        'if flag[now]': lambda S, B, r: ('这段之前被整体染过色（`flag`），要往下走就得先把颜色下放给两个孩子' if B.flag[B.now] else '没有整段标记，直接往下走'),
        'f[now + now + 1] = f[now + now + 2] = f[now]': '把 `{f[now]}` 下放给左右孩子，孩子也打上整段标记',
        'if j <= mid': lambda S, B, r: f'区间 `[{B.i}, {B.j}]` 和中点比：全在一侧只进那侧，跨过中点两边都进',
        'f[now] = f[now + now + 1]': '回溯：两个孩子颜色相同 → 当前节点沿用，`f = {f[now]}`',
        'f[now] = 0': '回溯：两个孩子颜色不同 → 当前节点是混合，`f = 0`',
        'if get(': lambda S, B, r: (lambda c: f'下标 `{B.index}`（值 {S.num_list[B.index]}）自顶向下查，遇到非 0 就停 → ' + ('==红色==，`res` 加 1' if c == 1 else '蓝色'))(_get(B.f, len(B.num_list), B.index)),
        'res = 0': '数红色：每个下标自顶向下查一次',
        'return res': '一共 `{res}` 个红色节点',
    },
    max_steps=110,
    cards=dict(
        one_liner='树当成升序数组：离散化后用线段树做区间染色',
        complexity='时间 `O(n log n + m log n)`，空间 `O(n)`',
        problem=['给一棵二叉搜索树，初始所有节点都是蓝色',
                 '`ops[i] = [type, x, y]`：把值在 `[x, y]` 内的节点染红（`type=1`）或染蓝（`type=0`），后面的操作覆盖前面的',
                 '求最后红色节点的数量',
                 '本视频：树 `[5,3,7,1,null,null,9]`，`ops = [[1,2,6],[0,4,8],[1,0,3]]` → `2`'],
        quote='虽然给出的是二叉搜索树，实际上可以认为是给出了一个数组以及若干区间染色操作，问最终数组中红色下标的数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['中序遍历得到升序数组 `num_list`，区间值域很大，要先==离散化==到 `0 … n−1`',
              '左端点向右找最近的树中值（`right_mapping`），右端点向左找（`left_mapping`），区间可能落空',
              '映射后就是「区间染色、单点查询」：线段树，整段染色时打标记，要往下走时再下放'],
        summary=['时间 `O(n log n + m log n)`，空间 `O(n)`',
                 '易错：左端点映射要向右找、右端点向左找；落空的区间（`n` 或 `-1`）要跳过',
                 '懒标记 `flag`：整段染色就停；往下走之前先下放，回溯时左右同色才合并成一种颜色',
                 '原文已是 Python 3 写法，未做修改；`right_mapping[now] = n` 在 `n` 赋值前，本例未走到该分支'],
    ),
)
