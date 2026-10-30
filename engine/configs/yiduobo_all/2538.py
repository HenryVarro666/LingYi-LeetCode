import math as _m


def _layout(edges, n):
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
    pos, depth, nxt = {}, {}, [0]

    def go(x, fa, d):
        kids = [y for y in g[x] if y != fa]
        if not kids:
            pos[x] = nxt[0]
            nxt[0] += 1
        else:
            for y in kids:
                go(y, x, d + 1)
            pos[x] = sum(pos[y] for y in kids) / len(kids)
        depth[x] = d

    go(0, -1, 0)
    return pos, depth, max(depth.values()), max(nxt[0] - 1, 1)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    edges, price = S['edges'], S['price']
    n = len(price)
    pos, depth, md, mw = _layout(edges, n)
    cv.text((x0 + 18, y0 + 4), '树（以 0 为根 DFS）：黄 = 当前 now，绿 = 当前孩子 child，蓝 = 父节点 fa', 22, T['muted'], bold=True)
    R = 34
    w, h = x1 - x0 - 2 * R - 80, y1 - y0 - 2 * R - 90
    P = {i: (x0 + 40 + R + pos[i] / mw * w, y0 + 56 + R + depth[i] / max(md, 1) * h) for i in range(n)}
    for a, b in edges:
        cv.line([P[a], P[b]], T['dim'], 4)
    cur, fa, ch = S.get('now'), S.get('fa'), S.get('child')
    if 'ma_s1' not in S or cur is None:
        cur = fa = ch = None
    for i in range(n):
        cx, cy = P[i]
        c = None
        if i == cur:
            c = 'yellow'
        elif i == ch:
            c = 'green'
        elif i == fa:
            c = 'blue'
        fill = T[c] if c else T['panel2']
        cv.d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=fill, outline=T['border'], width=3)
        cv.text((cx, cy - 10), i, 26, T['bg'] if c else T['text'], anchor='mm', bold=True)
        cv.text((cx, cy + 14), f'价{price[i]}', 20, T['bg'] if c else T['muted'], anchor='mm', bold=True)


def _info(S):
    if 'ma_s1' not in S or 'now' not in S:
        return ''
    return (f"节点 `{S['now']}`：到叶子最大 `ma_s1 = {S['ma_s1']}`，不含叶子最大 `ma_s2 = {S['ma_s2']}`")


CONFIG = dict(
    num=2538, title='最大价值和与最小价值和的差值', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='dfs 返回两条树链 · 叶子值要扣掉',
    tags=['动态规划', '链表树与回溯', '难度分 2398'],
    code='''
class Solution(object):
    def maxOutput(self, n, edges, price):

        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        def dfs(now, fa):
            s1 = price[now]
            s2 = 0

            ma_s1 = price[now]
            ma_s2 = 0

            for child in g[now]:
                if child == fa:
                    continue
                
                child_s1, child_s2 = dfs(child, now)
                global res
                res = max(res, child_s1 + ma_s2, child_s2 + ma_s1)
                
                ma_s1 = max(ma_s1, child_s1 + price[now])
                ma_s2 = max(ma_s2, child_s2 + price[now])

            return ma_s1, ma_s2

        global res
        res = 0
        dfs(0, None)
        return res
''',
    call='Solution().maxOutput(6, [[0,1],[1,2],[1,3],[3,4],[3,5]], [9,8,7,6,10,5])',
    expect=24,
    skip=['g = [[]', 'for x, y in edges', 'g[x].append', 'g[y].append', 'global res', 'continue', 10, 11, 'def dfs'],
    max_steps=80,
    views=[
        dict(type='custom', draw=_draw, h=380),
        dict(type='text', fn=_info, h=60, size=24),
        dict(type='calls', h=200),
    ],
    watch=[('now', 'now', 'yellow'), ('ma_s1', 'ma_s1', 'blue'), ('ma_s2', 'ma_s2', 'pink')],
    captions={
        'ma_s1 = price[now]': '`ma_s1`：从 `now` 出发、==到叶子结束==的最大树链和，先只有自己 `{ma_s1}`',
        'ma_s2 = 0': '`ma_s2`：到叶子、但==不含这个叶子==的最大和，先是空链 `0`',
        'for child in g[now]': lambda S, B, r: ((f'遍历 `now={S.now}` 的下一个邻居 `child = {S.child}`' if S.child != B._inner.get('child') else f'`now={S.now}` 的孩子都遍历完了')
                                                if 'child' in S else '遍历 `now` 的所有孩子'),
        'if child == fa': lambda S, B, r: (f'`child = {S.child}` 是父节点 → 跳过' if S.child == S.fa else f'`child = {S.child}` 是孩子 → 递归求它的两个值'),
        'child_s1, child_s2 = dfs': '孩子 `{child}` 返回：`child_s1 = {child_s1}`（含叶子），`child_s2 = {child_s2}`（不含叶子）',
        'res = max': '两种拼法：`child_s1 + ma_s2 = {child_s1 + ma_s2}`，`child_s2 + ma_s1 = {child_s2 + ma_s1}` → 取大者和 `res` 比较，更大就更新',
        'ma_s1 = max(ma_s1, child': '孩子的链头部再接上 `now`：`ma_s1 = {ma_s1}`',
        'ma_s2 = max(ma_s2, child': '不含叶子的链同样接上 `now`：`ma_s2 = {ma_s2}`',
        'return ma_s1, ma_s2': '返回 `({ma_s1}, {ma_s2})` 给上层节点',
        'dfs(0, None)': '从节点 0 开始，没有父节点',
        'res = 0': '全局答案 `res = 0`',
        'return res': '最大开销 `{res}`',
    },
    cards=dict(
        one_liner='最大链必到叶子；答案 = 两条叶子链拼起来，再扣一个叶子',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无根树，节点有正的价值 `price`，选一个根',
                 '开销 = 以根为起点的最大路径和 − 最小路径和，求最大开销',
                 '示例：`price=[9,8,7,6,10,5]` → `24`'],
        quote='以某个节点开始的最小价值路径必然只包含该节点自身，而从该节点开始的最大价值路径必然会延伸到==某个叶子节点==。',
        quote_src='—— yiduobo 题解原文',
        idea=['答案必是「叶子到叶子的树链和」减去其中一个叶子的值',
              '`dfs(now)` 返回两个值：到叶子且含叶子 `ma_s1`，到叶子但不含叶子 `ma_s2`',
              '每遇到一个孩子，先用「孩子 s1 + 已有 ma_s2」「孩子 s2 + 已有 ma_s1」更新答案，再合并进 `now`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '先更新答案，再合并孩子，否则同一棵子树会和自己拼接',
                 '`ma_s2` 接上 `price[now]`：`now` 一定不是叶子',
                 '原文是 Python 2 风格的类写法，代码无需改动即可运行',
                 '对比灵神：灵神用 `nonlocal ans`、yiduobo 用 `global res`，思路同为树形 DP'],
    ),
)
