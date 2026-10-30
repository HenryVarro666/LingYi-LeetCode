PID = [1, 3, 10, 5, 7, 8, 2]
PPID = [3, 0, 5, 3, 5, 10, 1]
KILL = 5


def _layout():
    ch = {}
    for x, y in zip(PID, PPID):
        ch.setdefault(y, []).append(x)
    pos, cnt = {}, [0]

    def go(u, d):
        kids = ch.get(u, [])
        if not kids:
            pos[u] = (cnt[0], d)
            cnt[0] += 1
            return
        for v in kids:
            go(v, d + 1)
        pos[u] = ((pos[kids[0]][0] + pos[kids[-1]][0]) / 2, d)

    for r in ch.get(0, []):
        go(r, 0)
    return pos, cnt[0], ch


POS, NLEAF, CH = _layout()


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '进程树（红 = 已出队，橙 = 在队列中，黄 = now）', 22, T['muted'], bold=True)
    depth = max(d for _, d in POS.values()) + 1
    gx0, gx1, gy0, gy1 = x0 + 90, x1 - 90, y0 + 85, y1 - 40

    def P(u):
        c, d = POS[u]
        return (gx0 + (c + 0.5) / NLEAF * (gx1 - gx0), gy0 + d / max(1, depth - 1) * (gy1 - gy0))

    q = S.get('q') or []
    head = S.get('head', 0) if 'head' in S else 0
    done, waiting = set(q[:head]), set(q[head:])
    now = S.get('now') if S.get('_line', 0) >= 14 else None
    for y, kids in CH.items():
        if y == 0:
            continue
        for v in kids:
            cv.line([P(y), P(v)], T['red'] if v in done | waiting and y in done else T['border'], 3)
    for u in POS:
        if u == now and 'now' in S:
            f = T['yellow']
        elif u in done:
            f = T['red']
        elif u in waiting:
            f = T['orange']
        else:
            f = T['panel2']
        X, Y = P(u)
        r = 34
        cv.d.ellipse((X - r, Y - r, X + r, Y + r), fill=f, outline=T['muted'] if f == T['panel2'] else f, width=2)
        cv.text((X, Y), str(u), 28, T['bg'] if f != T['panel2'] else T['text'], anchor='mm', bold=True)
    cv.text((x1 - 20, y0 + 4), f'kill = {KILL}', 24, T['pink'], anchor='ra', bold=True)


CONFIG = dict(
    num=582, title='杀掉进程', difficulty='Medium', category='图论',
    author='yiduobo', technique='建有向图 + BFS，队列即答案',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def killProcess(self, pid, ppid, kill):

        childs = {}
        for x, y in zip(pid, ppid):
            if y not in childs:
                childs[y] = []
            childs[y].append(x)

        q = [kill]
        head, tail = 0, 1
        while head < tail:
            now = q[head]
            head += 1
            for next in childs.get(now, []):
                q.append(next)
                tail += 1

        return q
''',
    call=f'Solution().killProcess({PID}, {PPID}, {KILL})',
    expect=[5, 10, 7, 8],
    views=[
        dict(type='custom', draw=_draw, h=440),
        dict(type='map', var='childs', label='childs：父进程 → 子进程列表（有向图）', h=110,
             fmt=lambda k, v: f'{k}→{v}'),
        dict(type='array', var='q', label='q（灰 = 已出队；head 之后是待处理）', h=150, cell=80, min_slots=5,
             pointers={'head': 'cyan', 'tail': 'pink'},
             dim=lambda S, i, v: i < S.get('head', 0)),
    ],
    watch=[('now', 'now', 'yellow'), ('head', 'head', 'cyan'), ('tail', 'tail', 'pink')],
    skip=['childs[y] = []', 'if y not in childs'],
    captions={
        'childs = {}': '根据父子关系建立==有向图==：`childs[父] = [子…]`',
        'for x, y in zip': lambda S, B, r: ('父子关系都建好了' if B.get('x') == S.x and B.get('y') == S.y
                                             else f'进程 `{S.x}` 的父进程是 `{S.y}`'),
        'if y not in childs': lambda S, B, r: (f'`{S.y}` 还没有子进程列表 → 新建' if B.y not in B.childs else f'`{S.y}` 已有子进程列表'),
        'childs[y].append(x)': lambda S, B, r: (f'`{S.y}` 第一次出现 → 新建列表，`childs[{S.y}]` = {S.childs[S.y]}' if len(S.childs[S.y]) == 1
                                                 else f'`{S.x}` 加入 `{S.y}` 的子进程：`childs[{S.y}]` = {S.childs[S.y]}'),
        'q = [kill]': '从要杀的进程 `{kill}` 开始 ==向下 BFS==',
        'head, tail = 0, 1': '用数组模拟队列：`q[head:tail]` 是待处理部分，==出队的元素不删除==',
        'while head < tail': lambda S, B, r: ('`head < tail` → 队列非空' if S.head < S.tail else '`head == tail`：队列空了 → BFS 结束'),
        'now = q[head]': '取出队首进程 `now = {now}`：它会被杀掉',
        'head += 1': '`head` 后移到 {head}（`{now}` 仍留在 q 里）',
        'for next in childs.get': lambda S, B, r: (f'`{S.now}` 的子进程 `{S.next}` 也要被连带杀掉'
                                                   if S.get('next') in S.childs.get(S.now, []) and S.get('next') != B.get('next') or (S.get('next') in S.childs.get(S.now, []) and B.get('now') != S.now and B.get('_line') != 17)
                                                   else f'`{S.now}` 的子进程处理完了' if S.now in S.childs else f'`{S.now}` 没有子进程'),
        'q.append(next)': '`{next}` 入队：`q = {q}`',
        'tail += 1': '`tail` → {tail}',
        'return q': '遍历到的所有进程都会被杀掉，==队列 q 本身就是答案==：`{q}`',
    },
    cards=dict(
        one_liner='建父→子有向图，从 kill 向下 BFS，队列 q 就是答案',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 个进程构成一棵树：`pid[i]` 的父进程是 `ppid[i]`（`ppid = 0` 表示根）',
                 '杀掉进程 `kill` 时，它的==所有子孙进程==也会被杀掉',
                 '返回被杀掉的所有进程 id（顺序任意）',
                 '示例：`pid=[1,3,10,5]`，`ppid=[3,0,5,3]`，`kill=5` → `[5,10]`'],
        quote='根据题目给出的父子关系建立有向图，然后从 kill 节点开始向下进行 bfs，遍历到的所有进程都是会连带被杀掉的进程，而 ==bfs 的队列 q 就是最终答案==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`ppid` 只给出“子 → 父”，要先反过来建 `childs[父] = [子…]`',
              '从 `kill` 出发 BFS，能到达的都是它的子孙',
              '用 `head/tail` 下标模拟队列，==出队不删元素==，最后 q 直接返回'],
        summary=['时间 `O(n)`：建图一遍 + 每个进程最多入队一次；空间 `O(n)`',
                 '易错：用 `childs.get(now, [])`，叶子进程没有子进程列表',
                 '也可以 DFS；树没有环，不需要 visited',
                 '原文为 Python 2 写法，仅删去了类型注释的文档字符串'],
    ),
)
