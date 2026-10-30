def _tree_pos(n, edges, root=0):
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
    xs, ds, ch, cnt = {}, {}, {}, [0]

    def go(x, fa, d):
        ds[x] = d
        ch[x] = [y for y in g[x] if y != fa]
        for y in ch[x]:
            go(y, x, d + 1)
        if ch[x]:
            xs[x] = (xs[ch[x][0]] + xs[ch[x][-1]]) / 2
        else:
            xs[x] = cnt[0]
            cnt[0] += 1
    go(root, -1, 0)
    return xs, ds, ch, max(cnt[0], 1)


def _draw_tree(cv, box, T, n, edges, node_fn, title='', edge_fn=None, edge_label=None, bot_right=False, txt_size=28):
    """node_fn(i) -> dict(fill=颜色名或None, txt=节点里的字, top=上方小字, bot=下方小字, ring=颜色名或None)"""
    x0, y0, x1, y1 = box
    xs, ds, ch, nl = _tree_pos(n, edges)
    md = max(ds.values())
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    gx0, gx1 = x0 + 70, x1 - 70
    gy0, gy1 = y0 + 84, y1 - 52
    step = (gx1 - gx0) / max(nl - 1, 1) if nl > 1 else 0
    step = min(step, 150)
    ox = (x0 + x1) / 2 - step * (nl - 1) / 2
    ly = (gy1 - gy0) / max(md, 1)
    ly = min(ly, 140)
    P = {i: (ox + xs[i] * step, gy0 + ds[i] * ly) for i in range(n)}
    for p in range(n):
        for c in ch[p]:
            col = edge_fn(p, c) if edge_fn else None
            cv.line([P[p], P[c]], T[col] if col else T['border'], 6 if col else 3)
            lab = edge_label(p, c) if edge_label else None
            if lab is not None:
                mx, my = (P[p][0] + P[c][0]) / 2, (P[p][1] + P[c][1]) / 2
                right = P[c][0] >= P[p][0]
                cv.text((mx + (10 if right else -10), my), lab, 22, T[col] if col else T['cyan'], anchor='lm' if right else 'rm', bold=True, mono=True)
    R = 27
    for i in range(n):
        X, Y = P[i]
        d = node_fn(i)
        f = d.get('fill')
        ring = d.get('ring')
        if ring:
            cv.d.ellipse((X - R - 6, Y - R - 6, X + R + 6, Y + R + 6), outline=T[ring], width=4)
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=T[f] if f else T['panel2'],
                     outline=T[f] if f else T['muted'], width=2)
        cv.text((X, Y), d.get('txt', i), txt_size, T['dim'] if d.get('dim') else (T['bg'] if f else T['text']), anchor='mm', bold=True)
        if not edge_label:
            cv.text((X - R - 10, Y - R - 4), i, 18, T['dim'], anchor='rb', mono=True)
        if d.get('top'):
            cv.text((X, Y - R - 10), d['top'], 20, T['cyan'], anchor='mb', bold=True)
        if d.get('bot'):
            if bot_right:
                cv.text((X + R + 12, Y), d['bot'], 22, T[d.get('botc', 'green')], anchor='lm', bold=True)
            else:
                cv.text((X, Y + R + 8), d['bot'], 22, T[d.get('botc', 'green')], anchor='mt', bold=True)


N = 5
EDGES = [[0, 1], [0, 2], [1, 3], [1, 4]]
LABELS = 'abaab'


def _node(S):
    now = S.get('now')
    used = S.get('used', set())
    res = S.get('res', [0] * N)
    fin = S.get('_line') is not None

    def f(i):
        d = dict(txt=LABELS[i])
        if i == now:
            d['fill'] = 'yellow'
        elif res[i] > 0:
            d['fill'] = 'green'
        elif i in used:
            d['fill'] = 'blue'
        if res[i] > 0:
            d['bot'] = f'res={res[i]}'
        return d
    return f


def _draw(cv, S, B, box, T):
    _draw_tree(cv, box, T, N, EDGES, _node(S), title='树（字母 = 标签；黄 = 当前 now，蓝 = 已访问，绿 = res 已算出）')


CONFIG = dict(
    num=1519, title='子树中标签相同的节点数', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='DFS 合并子树标签计数',
    tags=['灵神题单', '链表树与回溯'],
    setup='',
    code='''
class Solution(object):
    def countSubTrees(self, n, edges, labels):

        g = {x : set() for x in range(n)}
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)
        
        used = set([0])

        res = [0] * n
        final_cnt = self.dfs(0, g, used, res, labels)
        return res
    
    def dfs(self, now, g, used, res, labels):
        now_cnt = {labels[now] : 1}
        for next in g[now]:
            if next not in used:
                used.add(next)
                child_cnt = self.dfs(next, g, used, res, labels)
                for char in child_cnt:
                    now_cnt[char] = now_cnt.get(char, 0) + child_cnt[char]
        
        res[now] = now_cnt[labels[now]]
        return now_cnt
''',
    call="Solution().countSubTrees(5, [[0,1],[0,2],[1,3],[1,4]], 'abaab')",
    expect=[3, 2, 1, 1, 1],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='map', var='now_cnt', label='now_cnt：当前子树各标签个数', h=120, fmt=lambda k, v: f"'{k}': {v}"),
        dict(type='calls', h=170, hide=('g', 'used', 'res', 'labels')),
    ],
    watch=[('now', "now", 'yellow'), ('res', 'res', 'green')],
    captions={
        'g = {x': '用 `set` 建邻接表（循环 `g[x].add(y)`、`g[y].add(x)` 双向加边）：每个点的邻居集合',
        'used = set': '`used` 记录已访问的点，从根 `0` 出发，避免走回父亲',
        'res = [0]': '`res[i]` 存「以 i 为根的子树里，标签与 i 相同的节点数」',
        'self.dfs(0': '从根节点 0 开始 DFS，返回值是子树的标签计数',
        'now_cnt = {': '先算自己：`now_cnt = {{ \'{labels[now]}\': 1 }}`，节点 {now} 本身占一个标签',
        'if next not in used': lambda S, B, r: (f'`{S.next}` ==没访问过== → 它是 {S.now} 的孩子，要进去' if S.next not in B.used
                                                else f'`{S.next}` 已在 `used` 里（是父亲）→ 跳过'),
        'used.add': '先把 `{next}` 标记为已访问，再递归进去',
        'child_cnt = self.dfs': lambda S, B, r: (f'递归进入孩子 `{S.next}`，去求它子树的标签计数' if S['_inner'].get('now') != B['_inner'].get('now')
                                                 else f'孩子 `{S.next}` 返回子树标签计数：`child_cnt = {S.child_cnt}`'),
        'now_cnt[char] =': '把孩子的标签 `{char}`（{child_cnt[char]} 个）并入：`now_cnt[\'{char}\']` = =={now_cnt[char]}==',
        'res[now] =': '孩子都合并完：节点 {now} 的子树里，标签 `{labels[now]}` 共 =={res[now]}== 个，写入 `res[{now}]`',
        'return now_cnt': '把整棵子树的标签计数 `{now_cnt}` 交给上层父亲去合并',
        'return res': '全部算完，返回 `res = {res}`',
    },
    skip=['final_cnt', 'g[x].add', 'g[y].add', 'for x, y in edges', 'for next in g[now]', 'for char in child_cnt'],
    max_steps=110,
    cards=dict(
        one_liner='子树标签数 = 自己 + 各孩子子树标签数之和，边 DFS 边记答案',
        complexity='时间 `O(n·26)`，空间 `O(n)`',
        problem=['无向树，根为 `0`，每个节点有一个小写字母标签 `labels[i]`',
                 '对每个节点 `i`，求它的子树里标签和 `labels[i]` ==相同==的节点数',
                 '示例：`labels = "abaedcd"` → `[2,1,1,1,1,1,1]`','本视频：5 个点，`labels = "abaab"` → `[3,2,1,1,1]`'],
        quote='对于一颗以now为根节点的子树而言，其所有节点的各个标签数可以通过统计以now的各个孩子为根节点的子树中标签数之和，再加上root这个节点本身的标签来计算出来。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dfs(now)` 返回一个字典：这棵子树里各标签出现几次',
              '先放入自己的标签，再把每个孩子返回的字典逐项加进来',
              '合并完毕，字典里 `labels[now]` 的值就是答案，顺手写进 `res[now]`'],
        summary=['时间：每个节点合并一次字典，字典最多 26 项 → `O(26n)`；空间 `O(n)`',
                 '用 `used` 集合防止从孩子走回父亲；每个点只会被访问一次',
                 '返回值是整个计数字典，答案 `res[now]` 是在返回前顺手记录的',
                 '易错：答案要取 `now_cnt[labels[now]]`，必须在孩子全部合并之后']),
)
