def _layout(g, n):
    """以 0 为根的树：返回 (children, depth, x 坐标(叶子序号))"""
    ch = {i: [] for i in range(n)}
    depth = {0: 0}
    st = [(0, -1)]
    order = []
    while st:
        x, fa = st.pop()
        order.append(x)
        for y in g[x]:
            if y != fa:
                ch[x].append(y)
                depth[y] = depth[x] + 1
                st.append((y, x))
    xs, cnt = {}, [0]

    def go(x):
        if not ch[x]:
            xs[x] = cnt[0]
            cnt[0] += 1
        else:
            for y in ch[x]:
                go(y)
            xs[x] = (xs[ch[x][0]] + xs[ch[x][-1]]) / 2
    go(0)
    return ch, depth, xs, max(cnt[0], 1)



def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g, nums = S['g'], S['nums']
    n = len(nums)
    ch, depth, xs, w = _layout(g, n)
    cv.text((x0 + 18, y0 + 4), '树（圈内 = 节点值；灰 = 未访问，黄 = 已求出答案，蓝 = 正在处理，绿 = 它的答案节点）', 22, T['muted'], bold=True)
    res = S.get('res') or [None] * n
    cur = S.get('next_node')
    if cur is None and '_inner' in S:
        cur = S['_inner'].get('next_node')
    ansn = res[cur] if cur is not None and res[cur] is not None and res[cur] >= 0 else None
    sp = min(150, (x1 - x0 - 120) / w)
    sx = x0 + 60 + ((x1 - x0 - 120) - sp * (w - 1)) / 2
    md = max(depth.values())
    rad = 28
    top = y0 + 88
    dy = min(110, (y1 - y0 - 88 - rad - 24) / max(md, 1))
    pos = {i: (sx + xs[i] * sp, top + depth[i] * dy) for i in range(n)}
    for p in range(n):
        for c in ch[p]:
            cv.line([pos[p], pos[c]], T['border'], 3)
    for i in range(n):
        X, Y = pos[i]
        fill = T['panel2'] if res[i] is None else T['yellow']
        if i == ansn:
            fill = T['green']
        if i == cur:
            fill = T['blue']
        cv.rect((X - rad, Y - rad, X + rad, Y + rad), fill=fill, r=rad, outline=T['border'])
        cv.text((X, Y), nums[i], 30, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
        cv.text((X + rad + 4, Y - rad - 2), f'#{i}', 20, T['dim'], anchor='lb', mono=True)
        if res[i] is not None:
            cv.text((X - rad - 4, Y + rad), f'答案 {res[i]}', 20, T['green'], anchor='rt', bold=True)


def _cand(S):
    if 'next_node' not in S or 'candidate' not in S:
        return ''
    nn = S['next_node']
    st = S['state'][S['nums'][nn]]
    fs = S['candidate'][st]
    show = lambda v: '无' if v is None else f'节点 {v}'
    return f"节点 {nn}（值 {S['nums'][nn]}，因子状态 `{st:04b}`）查 `candidate[{st}]` = [first: ==`{show(fs[0])}`==，second: `{show(fs[1])}`]"


CONFIG = dict(
    num=1766, title='互质树', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='BFS + 因子状态压缩（2/3/5/7）+ first/second 候选',
    tags=['灵神题单', '难度分 2232'],
    code='''
class Solution(object):
    def getCoprimes(self, nums, edges):

        n = len(nums)
        g = [set() for _ in range(n)]
        root_candidate = set(range(n))
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)

        state = [0] * 51
        p = list(range(51))
        for index in range(1, 51):
            # state[index]表示index是否具有因子2、3、5、7
            if index % 2 == 0:
                state[index] += 1
            if index % 3 == 0:
                state[index] += 2
            if index % 5 == 0:
                state[index] += 4
            if index % 7 == 0:
                state[index] += 8
            tmp = index
            while tmp % 2 == 0:
                tmp //= 2
            while tmp % 3 == 0:
                tmp //= 3
            while tmp % 5 == 0:
                tmp //= 5
            while tmp % 7 == 0:
                tmp //= 7
            p[index] = tmp #计算p值

        # f[i][j]表示i和j的p值是否大于1且相同
        f = [[True] * 51 for _ in range(51)]
        for i in range(1, 50):
            if p[i] > 1:
                for j in range(i, 51):
                    if p[i] == p[j]:
                        f[i][j] = f[j][i] = False

        candidate = {}
        for index in range(16):
            if index & state[nums[0]] == 0:
                candidate[index] = [0, None]
            else:
                candidate[index] = [None, None]

        res = [None] * n
        l = 0
        r = 1
        q = [[0, candidate]]
        res[0] = -1
        while l < r:
            for now_node, candidate in q[l : r]:
                for next_node in g[now_node]:
                    if res[next_node] is not None:
                        continue
                    res[next_node] = -1
                    next_candidate = candidate.copy()
                    first, second = candidate[state[nums[next_node]]]
                    if first is not None:
                        if not f[nums[first]][nums[next_node]]:
                            # first的p值与当前节点的p值相同，因此考虑使用second作为答案
                            if second is not None:
                                res[next_node] = second
                        else:
                            res[next_node] = first

                    for index in range(16):
                        if state[nums[next_node]] & index == 0:
                            first, second = next_candidate[index]
                            if first is not None and not f[nums[first]][nums[next_node]]:
                                # 老first的p值与当前节点的p值相同，那么沿用老的second
                                next_candidate[index] = [next_node, second]
                            else:
                                next_candidate[index] = [next_node, first]
                    
                    q.append([next_node, next_candidate])
            
            l, r = r, len(q)

        return res
''',
    call='Solution().getCoprimes([2, 3, 3, 2], [[0, 1], [1, 2], [1, 3]])',
    expect=[-1, 0, 0, 1],
    skip=['n = len(nums)', 'g = [set()', 'root_candidate', 'for x, y in edges', 'g[x].add', 'g[y].add', 'state = [0]', 'p = list(range', 'for index in range(1, 51)',
          'if index % ', 'state[index] +=', 'tmp = index', 'while tmp', 'tmp //=', 'p[index] = tmp', 'f = [[True]', 'for i in range(1, 50)',
          'if p[i] > 1', 'for j in range(i, 51)', 'if p[i] == p[j]', 'f[i][j] = ',
          'for index in range(16)', 'if index & state[nums[0]] == 0', 'candidate[index] = [0, None]', 'candidate[index] = [None, None]',
          'if state[nums[next_node]] & index == 0', 'first, second = next_candidate[index]', 'if first is not None and not f', 'next_candidate[index] = ['],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='text', fn=_cand, size=24, h=110),
        dict(type='array', var='res', label='res（None = 还没访问，-1 = 没有互质祖先）', cell=60, h=120),
    ],
    watch=['l', 'r', ('now_node', 'now_node', 'blue'), ('next_node', 'next_node', 'pink'), ('first', 'first', 'green'), ('second', 'second', 'purple')],
    captions={
        'candidate = {}': '`candidate[s]`（s = 0..15）：与因子状态 s ==按位与为 0==（没有公共的 2/3/5/7）的最深祖先 [first, second]。根节点 0 先填进所有与它状态无公共因子的项',
        'if index & state[nums[0]] == 0': '根节点 0 的值 `{nums[0]}`，状态 `{state[nums[0]]}`：和 `index` 没有公共因子才能进候选',
        'candidate[index] = [0, None]': '根节点 0 成为 `candidate[{index}]` 的 first',
        'candidate[index] = [None, None]': '`candidate[{index}]` 暂无候选',
        'res = [None]': '`res` 存答案，None 表示还没访问（顺便当 visited）',
        'q = [[0, candidate]]': '队列存 [节点, 它路径上的 candidate]：BFS 一层层往下',
        'res[0] = -1': '根节点没有祖先：`res[0] = -1`',
        'while l < r': '`[l, r)` 是当前这一层的节点',
        'if res[next_node] is not None': lambda S, B, r: ('邻居已访问过（是父节点）→ 跳过' if S.res[S.next_node] is not None else '没访问过，是孩子'),
        'continue': '跳过父节点',
        'res[next_node] = -1': '孩子 `{next_node}` 先记 -1，同时标记已访问',
        'next_candidate = candidate.copy()': '孩子的 candidate 要在父亲的基础上改，所以先 ==copy==（别的分支不受影响）',
        'first, second = candidate[state': '取 `candidate[状态]`：first = `{first}`，second = `{second}`——都是与节点 `{next_node}` 因子互不相交的最深祖先',
        'if first is not None': lambda S, B, r: ('没有候选 first → 答案保持 -1' if S.first is None else f'有候选 first = 节点 {S.first}，还要检查 p 值'),
        'if not f[nums[first]]': lambda S, B, r: (f'`f[{S.nums[S.first]}][{S.nums[S.next_node]}]` = False：p 值相同且 > 1，其实不互质' if not S.f[S.nums[S.first]][S.nums[S.next_node]] else 'p 值不冲突 → first 就是答案'),
        'if second is not None': '改用 second（它的 p 值必然与 first 不同）',
        'res[next_node] = second': '`res[{next_node}] = {second}`',
        'res[next_node] = first': '`res[{next_node}] = {first}`：最近的互质祖先',
        'for index in range(16)': lambda S, B, r: ('更新 candidate：枚举 16 种状态' if S.index == 0 or 'index' not in S else f'检查状态 `{S.index}`'),
        'if state[nums[next_node]] & index == 0': lambda S, B, r: (f'节点 {S.next_node} 状态 `{S.state[S.nums[S.next_node]]}` & `{S.index}` = 0 → 它可以作为 `candidate[{S.index}]` 的新 first' if S.state[S.nums[S.next_node]] & S.index == 0 else f'`{S.state[S.nums[S.next_node]]}` & `{S.index}` ≠ 0：有公共因子，不能做候选'),
        'next_candidate[index] = [next_node, second]': '老 first 的 p 值和当前相同：沿用老 second 做新 second',
        'next_candidate[index] = [next_node, first]': '节点 `{next_node}` 最深，成为新 first；老 first 降为 second',
        'q.append': '16 种状态里无公共因子的项：节点 `{next_node}` 当新 first，老 first 降为 second（p 值相同则沿用老 second），入队',
        'l, r = r, len(q)': '这一层处理完，下一层是 `[{l}, {r})`',
        'return res': '全部节点的答案：`{res}`',
    },
    cards=dict(
        one_liner='BFS 往下走，用 2/3/5/7 的位状态压缩互质检测，每个状态只留两个候选',
        complexity='时间约 `O(16n)`，空间 `O(16n)`（每个节点拷贝一份 candidate）',
        problem=['树根为 0，节点值 ≤ 50',
                 '求每个节点最近的、值与它互质的祖先，没有则 -1',
                 '示例：`nums=[2,3,3,2]`，边 `0-1, 1-2, 1-3` → `[-1,0,0,1]`'],
        quote='对于 50 这个范围而言，其中的所有数字都可以写成 2^a * 3^b * 5^c * 7^d * p，其中 p 等于 1 或者 p 是质数。',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素：bfs 时维护 1~50 每个数最后一次出现的位置，再枚举互质数',
              '优化：用 4 位二进制表示有没有因子 2、3、5、7，共 16 种状态',
              '`candidate[state]`：与 state 按位与为 0 的最深祖先',
              '剩下的质因子 p 若相同也不互质（22 和 33）→ 每个状态存 first、second 两个 p 不同的候选'],
        summary=['时间 `O(16n)`，空间 `O(16n)`：每个节点复制一份 16 项的 candidate',
                 'first 与当前节点 p 值相同时，答案改用 second',
                 '更新 candidate 时，老 first 的 p 值相同就沿用老 second',
                 '原文为 Python 2 写法，`p = range(51)` 已改为 `list(range(51))`，`tmp /= 2` 等整数除法已改为 `//=`',
                 '对比灵神：灵神 DFS + 恢复现场，每个节点枚举至多 50 个值；本解 BFS，把 50 压到 16'],
    ),
)
