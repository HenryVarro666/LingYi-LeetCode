def _tree_pos(ch, root=0):
    """一般树自动布局：叶子按顺序排开，父亲在孩子中间。返回 {节点: (x 0~1, 深度)}"""
    pos, cnt = {}, [0]
    leaves = sum(1 for _ in _leaves(ch, root))
    def go(u, d):
        kids = ch.get(u, [])
        if not kids:
            pos[u] = ((cnt[0] + 0.5) / leaves, d); cnt[0] += 1
        else:
            for k in kids:
                go(k, d + 1)
            pos[u] = ((pos[kids[0]][0] + pos[kids[-1]][0]) / 2, d)
    go(root, 0)
    return pos


def _leaves(ch, u):
    kids = ch.get(u, [])
    if not kids:
        yield u
    for k in kids:
        yield from _leaves(ch, k)


def _gt_draw(cv, S, B, box, T, ch, pos, edges, node_fn, extra=None, title=''):
    """edges: [(父,子,颜色名或None,虚线)]；node_fn(S,u)->(填充色, 主文字, 副文字)"""
    x0, y0, x1, y1 = box
    maxd = max(d for _, d in pos.values())
    W, H = x1 - x0 - 300, y1 - y0 - 110
    P = {u: (x0 + 110 + px * W, y0 + 70 + (d / max(maxd, 1)) * H) for u, (px, d) in pos.items()}
    if title:
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    for a, b, col, dash in edges:
        pa, pb = P[a], P[b]
        if dash == 'arc':  # 从孩子 b 绕一道弧线指向 a（向左侧鼓出）
            cx, cy = min(pa[0], pb[0]) - 110, (pa[1] + pb[1]) / 2
            pts = [((1 - t) ** 2 * pb[0] + 2 * (1 - t) * t * cx + t * t * pa[0],
                    (1 - t) ** 2 * pb[1] + 2 * (1 - t) * t * cy + t * t * pa[1]) for t in [0.12 + 0.76 * i / 30 for i in range(31)]]
            cv.line(pts, T[col], 5)
            cv.arrow(pts[-3], pts[-1], T[col], 5, 16)
        elif dash:
            cv.dashed(pb, pa, T[col], 4)
        else:
            cv.line([pa, pb], T[col] if col else T['border'], 4 if col else 3)
    R = 24
    for u, (X, Y) in P.items():
        fill, main, sub = node_fn(S, u)
        cv.rect((X - R, Y - R, X + R, Y + R), fill=T[fill] if isinstance(fill, str) else fill, outline=T['border'], r=R, width=2)
        cv.text((X, Y), main, 24, T['text'] if fill == 'panel2' else T['bg'], anchor='mm', bold=True, mono=True)
        if sub:
            cv.text((X + R + 8, Y), sub, 20, T['text'], anchor='lm', bold=True)
    if extra:
        extra(cv, P, T)
    return P
PAR = [-1, 0, 4, 0, 1]
STR = 'abbba'
CH = {}
for _i in range(1, len(PAR)):
    CH.setdefault(PAR[_i], []).append(_i)
POS = _tree_pos(CH)
_NOW = lambda S: S['_inner'].get('now')


def _node(S, u):
    ans = S.get('answer')
    sub = f'{STR[u]} · 子树 {ans[u]}' if ans and ans[u] else STR[u]
    if S['_inner'].get('now') == u:
        return 'yellow', str(u), sub
    last = S.get('last') or {}
    if any(u in st for st in last.values()):
        return 'cyan', str(u), sub
    return 'panel2', str(u), sub


def _draw(cv, S, B, box, T):
    nc = S.get('new_childs') or []
    newpar = {c: a for a, ks in enumerate(nc) for c in ks}
    edges = []
    for a, ks in CH.items():
        for b in ks:
            edges.append((a, b, 'red' if newpar.get(b, a) != a else None, newpar.get(b, a) != a))
    for b, a in newpar.items():
        if a != PAR[b]:
            edges.append((a, b, 'orange', 'arc'))
        else:
            edges.append((a, b, 'green', False))
    _gt_draw(cv, S, B, box, T, CH, POS, edges, _node,
             title='原树（黄 = 当前 now，青 = last 栈里的节点；红虚线 = 删掉的旧边，橙弧线 = 新边，绿 = 保留）')


def _c_if(S, B, ret):
    now = S.now
    st = S.last.get(S.s[now]) if now == now else None
    if st:
        return f"`s[{now}] = '{S.s[now]}'`：`last['{S.s[now]}']` 栈顶是 `{st[-1]}` → 它就是最近的同字母祖先"
    return f"`s[{now}] = '{S.s[now]}'`：`last` 里没有这个字母（或栈是空的）→ 没有同字母祖先，==保留老边=="


def _c_for(S, B, ret):
    I, J = S['_inner'], B['_inner']
    if 'c' not in I:
        return f'`{S.now}` 在原树里没有孩子 → 不用往下递归'
    if 'c' in J and J['c'] == I['c']:
        return f'`{S.now}` 的孩子都递归完了 → 回溯'
    return f"原树里取下一个孩子 `c = {I['c']}`（改边只写进 `new_childs`，不改 `childs`）"


CONFIG = dict(
    num=3331, title='修改后子树的大小', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='先 DFS 改边（字母栈） · 再 DFS 数子树',
    tags=['灵神题单', '链表树与回溯', '难度分 2046'],
    code='''
class Solution(object):
    def findSubtreeSizes(self, parent, s):
        
        n = len(parent)
        childs = [[] for _ in range(n)]
        for i, fa in enumerate(parent):
            if fa != -1:
                childs[fa].append(i)
        
        new_childs = [[] for _ in range(n)]
        last = {}

        def dfs(now, last, new_childs):
            if s[now] in last and len(last[s[now]]) > 0:
                new_childs[last[s[now]][-1]].append(now)
            else:
                if parent[now] != -1:
                    new_childs[parent[now]].append(now)
                last[s[now]] = []

            last[s[now]].append(now)
            for c in childs[now]:
                dfs(c, last, new_childs)
            last[s[now]].pop()

        dfs(0, last, new_childs)
        
        answer = [0] * n
        def new_dfs(now, answer):
            answer[now] += 1
            for c in new_childs[now]:
                new_dfs(c, answer)
                answer[now] += answer[c]
        
        new_dfs(0, answer)
        return answer
''',
    call="Solution().findSubtreeSizes([-1,0,4,0,1], 'abbba')",
    expect=[5, 2, 1, 1, 1],
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='map', var='last', label='last：字母 → 当前 dfs 路径上该字母的节点栈', h=120,
             fmt=lambda k, v: f'{k}: {v}'),
        dict(type='array', var='answer', label='answer（第二趟 DFS 才开始填）', cell=60, h=140,
             pointers={_NOW: 'yellow'}, pointer_labels={_NOW: 'now'}),
        dict(type='calls', h=110, hide=('last', 'new_childs', 'answer')),
    ],
    skip=['n = len(parent)', 'childs = [[]', 'for i, fa in', 'if fa != -1', 'childs[fa].append', 'new_childs = [[]', 'last = {}', 'answer = [0]', 'if parent[now] != -1', 'for c in new_childs'],
    max_steps=90,
    watch=[('now', "now if 'now' in _inner else ''", 'yellow'), ('new_childs', 'new_childs', 'orange')],
    captions={
        'if s[now] in last': _c_if,
        'new_childs[last[s[now]][-1]].append(now)': '新边：`{last[s[now]][-1]} → {now}`（栈顶节点成为 `{now}` 的新父亲），`new_childs = {new_childs}`',
        'if parent[now] != -1': '没有同字母祖先：看它是不是根（`parent[{now}] = {parent[now]}`）',
        'new_childs[parent[now]].append(now)': '保留老边：`{parent[now]} → {now}`',
        'last[s[now]] = []': "第一次遇到字母 `{s[now]}`：给它建一个空栈",
        'last[s[now]].append(now)': "`{now}` 入栈 `last['{s[now]}']`：往下走的路上，它就是 `{s[now]}` 的最近节点",
        'for c in childs[now]': _c_for,
        'dfs(c, last, new_childs)': '递归孩子 `{c}`',
        '.pop()': "回溯：`{now}` 出栈，兄弟分支不会看到它，`last['{s[now]}'] = {last[s[now]]}`",
        'dfs(0, last, new_childs)': '第一趟：从根 `0` 出发，按字母栈把每个点的新父亲找出来',
        'new_dfs(0, answer)': '第二趟：新边已建好，在==新树==上从根 `0` 数子树大小',
        'answer[now] += 1': '先把 `{now}` 自己算进去：`answer[{now}] = {answer[now]}`',
        'new_dfs(c, answer)': '沿新边递归孩子 `{c}`',
        'answer[now] += answer[c]': '孩子 `{c}` 的子树 `{answer[c]}` 累加进来：`answer[{now}] = {answer[now]}`',
        'return answer': '`answer = {answer}`',
    },
    cards=dict(
        one_liner='用「字母 → 节点栈」找最近同字母祖先，再在新树上数大小',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['树有 `n` 个节点，`s[i]` 是节点 `i` 的字符',
                 '每个点同时改挂到==最近的同字符祖先==（没有就不动）',
                 '求改完后每个点的子树大小。示例：`[-1,0,4,0,1]`，`"abbba"` → `[5,2,1,1,1]`'],
        quote='可以使用一个哈希表last记录在当前dfs序中，s中的每种字符对应的节点。last的key为每种字符，value为栈。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目拆成两步：==先改树，再数大小==，后一步是经典题',
              '改边：dfs 时 `last[字符]` 栈顶就是最近同字符祖先，没有就保留老边',
              '进入 `x` 入栈，回溯到 `x` 出栈；新边写进 `new_childs`，最后再 dfs 一次累加'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：栈空时要==保留老边==，不是丢掉这个点',
                 '易错点：改边只写进 `new_childs`，递归仍沿原树 `childs`，不然祖先会错',
                 '原文是 Python 2 风格 `class Solution(object)`，在 Python 3 中可直接运行，未改动',
                 '对比灵神：灵神一趟 DFS 把大小直接加给祖先；yiduobo 先建新树再数'],
    ),
)
