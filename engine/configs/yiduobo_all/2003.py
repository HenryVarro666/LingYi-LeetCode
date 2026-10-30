# ---- 通用的一般树画法：按 parents 数组布局，节点带颜色/外圈/下标注
def _gt_layout(parents):
    n = len(parents)
    ch = [[] for _ in range(n)]
    for i in range(1, n):
        ch[parents[i]].append(i)
    depth, xs, cnt = [0] * n, [0.0] * n, [0]

    def go(u, d):
        depth[u] = d
        if not ch[u]:
            xs[u] = cnt[0]
            cnt[0] += 1
        else:
            for v in ch[u]:
                go(v, d + 1)
            xs[u] = (xs[ch[u][0]] + xs[ch[u][-1]]) / 2
    go(0, 0)
    return ch, depth, xs, max(cnt[0], 1), max(depth) + 1


def gtree_draw(cv, box, T, parents, label, fill=None, ring=None, under=None, edge=None, edge_label=None, title=''):
    x0, y0, x1, y1 = box
    n = len(parents)
    ch, depth, xs, nleaf, nd = _gt_layout(parents)
    if title:
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    sp = min(130, (x1 - x0 - 80) / max(1, nleaf))
    dy = min(120, (y1 - y0 - 125) / max(1, nd - 1))
    rad = max(18, min(30, sp * 0.36, dy * 0.3))
    sx = x0 + (x1 - x0 - sp * (nleaf - 1)) / 2
    P = {u: (sx + xs[u] * sp, y0 + 80 + depth[u] * dy) for u in range(n)}
    for u in range(1, n):
        a, b = P[parents[u]], P[u]
        ec = edge(u) if edge else None
        cv.line([a, b], T[ec] if ec else T['border'], 6 if ec else 3)
        if edge_label:
            s = edge_label(u)
            if s is not None:
                mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
                w = cv.tlen(str(s), 18, bold=True) + 10
                cv.rect((mx - w / 2, my - 12, mx + w / 2, my + 12), fill=T['bg'], r=6)
                cv.text((mx, my), str(s), 18, T['muted'], anchor='mm', bold=True)
    for u in range(n):
        X, Y = P[u]
        f = fill(u) if fill else None
        rc = ring(u) if ring else None
        if rc:
            cv.rect((X - rad - 6, Y - rad - 6, X + rad + 6, Y + rad + 6), outline=T[rc], width=5, r=rad + 6)
        cv.rect((X - rad, Y - rad, X + rad, Y + rad), fill=T[f] if f else T['panel2'], outline=T['border'], r=rad)
        cv.text((X, Y), str(label(u)), 26, T['bg'] if f else T['text'], anchor='mm', bold=True)
        cv.text((X + rad + 6, Y - rad * 0.4), f'#{u}', 15, T['dim'], anchor='lm', mono=True)
        if under:
            s = under(u)
            if s:
                cv.text((X, Y + rad + 8), s, 19, T['green'], anchor='mt', bold=True)
    return P
PARENTS = [-1, 0, 1, 0, 3, 3]
NUMS = [5, 4, 6, 2, 1, 3]


def _draw(cv, S, B, box, T):
    ns = S.get('num_set') or set()
    p, now, nx = S.get('p'), S.get('now'), S['_inner'].get('next')
    res = S.get('res') or [1] * len(PARENTS)
    done = {i for i in range(len(PARENTS)) if res[i] != 1}

    def ring(i):
        if i == nx:
            return 'pink'
        if i == now:
            return 'yellow'
        if i == p:
            return 'blue'
        return None
    gtree_draw(cv, box, T, PARENTS, lambda i: NUMS[i], lambda i: 'green' if NUMS[i] in ns else None, ring,
               lambda i: f'res {res[i]}' if i in done else None,
               title='家族树（圈内 = 基因值，绿 = 已进 num_set，蓝环 = p，黄环 = now，粉环 = next）')


CONFIG = dict(
    num=2003, title='每棵子树内缺失的最小基因值', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='基因值 1 向上走 · BFS 增量合并',
    tags=['链表树与回溯', '难度分 2415'],
    code='''
class Solution(object):
    def smallestMissingValueSubtree(self, parents, nums):

        n = len(parents)
        g = {x : set() for x in range(n)}
        for index, fa in enumerate(parents):
            if fa != -1:
                g[fa].add(index)
        
        res = [1] * n
        p = None
        for index, num in enumerate(nums):
            if num == 1:
                p = index
                break
        
        if p is None:
            return res

        num_set = set()
        num_set.add(1)
        q = [p]
        l = 0
        r = 1
        while l < r:
            now = q[l]
            l += 1
            for next in g[now]:
                num_set.add(nums[next])
                q.append(next)
                r += 1
        
        miss = 2
        while miss in num_set:
            miss += 1
        res[p] = miss

        while parents[p] != -1:
            q = [parents[p]]
            num_set.add(nums[parents[p]])
            l = 0
            r = 1
            while l < r:
                now = q[l]
                l += 1
                for next in g[now]:
                    if next == p:
                        continue
                    num_set.add(nums[next])
                    q.append(next)
                    r += 1
            
            while miss in num_set:
                miss += 1

            res[parents[p]] = miss
            p = parents[p]
        
        return res
''',
    call='Solution().smallestMissingValueSubtree([-1,0,1,0,3,3], [5,4,6,2,1,3])',
    expect=[7, 1, 1, 4, 2, 1],
    views=[
        dict(type='custom', draw=_draw, h=310),
        dict(type='set', var='num_set', label='num_set（当前子树的基因值）', fmt=lambda x: str(x), h=100),
        dict(type='array', var='q', label='q（BFS 队列）', cell=60, h=100),
        dict(type='array', var='res', label='res', cell=60, h=120),
    ],
    watch=[('p', 'p', 'blue'), ('miss', 'miss', 'pink'), ('now', lambda S: S.get('now'), 'yellow')],
    captions={
        'g = {x': '`g[x]` 存节点 `x` 的儿子集合',
        'res = [1] * n': '基因值 1 只出现一次 → 先默认所有节点答案是 `1`',
        'p = index': '基因值 `1` 在节点 `{p}`：==只有从它向上到根的节点，子树里才有 1==',
        'if p is None': '`p = {p}`：{"没有基因值 1，全部答案都是 1" if p is None else "树里有基因值 1，继续"}',
        'num_set.add(1)': '节点 `p` 自己的基因值 `1` 先放进集合',
        'q = [p]': '队列从 `p` 出发，先 BFS 求出 `p` 子树的所有基因值',
        'now = q[l]': '出队节点 `{now}`',
        'for next in g[now]:': lambda S, B, r: f"节点 `{S['now']}` 的儿子：`{sorted(g[S['now']])}`",
        'num_set.add(nums[next])': '儿子 `{next}` 的基因值 `{nums[next]}` 加入集合',
        'q.append(next)': '儿子 `{next}` 入队，之后再展开它的子树',
        'while l < r': lambda S, B, r: '队列还有节点 → 继续 BFS' if S.l < S.r else '这一轮 BFS 结束：集合里就是当前子树的全部基因值',
        'while miss in num_set': '`{miss}` {"在" if miss in num_set else "不在"}集合里 → ' + '{"继续往后找" if miss in num_set else "它就是缺失的最小基因值"}',
        'miss += 1': '父节点答案 >= 子节点答案，`miss` 不用从 1 重来 → `miss = {miss}`',
        'res[p] = miss': '`res[{p}] = {miss}`',
        'while parents[p] != -1': '`p = {p}` 还有父节点 `{parents[p]}` → 向上走' ,
        'q = [parents[p]]': '新一轮从父节点 `{parents[p]}` 开始，==`p` 的子树已在集合里，不用重新遍历==',
        'num_set.add(nums[parents[p]])': '父节点自己的基因值 `{nums[parents[p]]}` 加入集合',
        'if next == p': '`next = {next}`：{"就是刚处理完的 p，跳过它的子树" if next == p else "是新的兄弟子树，需要遍历"}',
        'res[parents[p]] = miss': '`res[{parents[p]}] = {miss}`',
        'p = parents[p]': '`p` 上移到 `{p}`',
        'return res': '返回 `{ret}`',
    },
    skip=['for index, fa', 'if fa != -1', 'g[fa].add', 'for index, num', 'if num == 1', 'p = None', 'l = 0', 'r = 1', 'l += 1', 'r += 1', 'continue', 'break'],
    max_steps=100,
    cards=dict(
        one_liner='基因值互不相同：1 只在一个节点，答案只在它的祖先链上变化',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['家族树，节点有互不相同的基因值',
                 '求每个节点子树中缺失的最小正整数基因值',
                 '示例：`parents=[-1,0,1,0,3,3]`，`nums=[5,4,6,2,1,3]`',
                 '输出 `[7,1,1,4,2,1]`'],
        quote='题目中各个节点的基因值都互不相同，那么有一种tricky的做法。……从基因值为1的节点开始向上一路走到树的根节点，路过的这些节点的子树中是有基因值1的。',
        quote_src='—— yiduobo 题解',
        idea=['没有 1：全是 1。有 1：不在 1 到根路径上的节点答案都是 1',
              '沿路径向上，用 BFS 把「新增兄弟子树」的基因值并进集合，走过的 `p` 子树不再重复',
              '父节点子树是子节点的超集，`miss` 接着往上找，不用重置'],
        result='返回 `[7,1,1,4,2,1]`',
        summary=['时间 `O(n)`：每个节点只入队一次；`miss` 单调增加',
                 '易错：`q` 每轮要重置成 `[parents[p]]`，并跳过 `next == p`',
                 '`l, r` 手写队列指针；对比灵神：他用数组 `vis` 代替集合、用栈代替队列',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行'],
    ),
)
