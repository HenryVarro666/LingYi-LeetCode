import math as _math


def _gdraw(cv, T, box, title, pos, edges, color_of, sub_of=None, ecolor_of=None, R=26):
    """有向图：pos = [(fx, fy)]（0~1 的相对位置），edges = [(a, b)]"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    Wd, Hd = x1 - x0 - 100, y1 - y0 - 110
    P = [(x0 + 50 + fx * Wd, y0 + 60 + fy * Hd) for fx, fy in pos]
    es = set(edges)
    for a, b in edges:
        ec = (ecolor_of(a, b) if ecolor_of else None) or 'dim'
        col = T[ec] if isinstance(ec, str) else ec
        (xa, ya), (xb, yb) = P[a], P[b]
        if a == b:
            cv.arc_arrow((xa - 12, ya - R + 2), (xa + 12, ya - R + 2), 46, col, 3, 11)
            continue
        dx, dy = xb - xa, yb - ya
        L = _math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        off = 9 if (b, a) in es else 0
        nx, ny = -uy * off, ux * off
        cv.arrow((xa + ux * (R + 3) + nx, ya + uy * (R + 3) + ny), (xb - ux * (R + 6) + nx, yb - uy * (R + 6) + ny), col, 3, 12)
    for i, (x, y) in enumerate(P):
        c = color_of(i)
        fill = T[c] if isinstance(c, str) else (c or T['panel2'])
        cv.rect((x - R, y - R, x + R, y + R), fill=fill, outline=T['border'], r=R)
        cv.text((x, y), i, 26, T['bg'] if c else T['muted'], anchor='mm', bold=True)
        if sub_of:
            s = sub_of(i)
            if s:
                cv.text((x, y + R + 6), s, 19, T['text'], anchor='mt', mono=True)
    return P


FAV = [1, 0, 0, 2, 5, 6, 4]
_N = len(FAV)

CODE = '''
class Solution(object):
    def maximumInvitations(self, favorite):

        g = {}
        used = set()
        n = len(favorite)
        res = 0
        pair = []
        for index in range(n):
            if favorite[index] not in g:
                g[favorite[index]] = set()
            g[favorite[index]].add(index)

            if index not in used:
                used.add(index)
                next = favorite[index]
                stack = [index]
                circle = set([index])
                while next not in circle and next not in used:
                    used.add(next)
                    circle.add(next)
                    stack.append(next)
                    next = favorite[next]
                
                if next not in circle:
                    continue

                step = 0
                while stack:
                    now = stack.pop()
                    step += 1
                    if now == next:
                        break

                if step == 2:
                    pair.append([now, favorite[now]])
                else:
                    res = max(res, step)

        def bfs(start):
            q = [start]
            l = 0
            r = 1
            step = 0
            while l < r:
                step += 1
                for now in q[l : r]:
                    for next in g.get(now, set()):
                        q.append(next)
                
                l, r = r, len(q)

            return step

        cnt = 0
        for x, y in pair:
            g[x].remove(y)
            g[y].remove(x)
            cnt += bfs(x) + bfs(y)

        return max(res, cnt)
'''
_L = CODE.strip('\n').split('\n')
L_DECIDE = [k + 1 for k, s in enumerate(_L) if 'if next not in circle' in s][0]


def _ring_set(f):
    r = set()
    for s in range(len(f)):
        x = s
        for _ in range(len(f)):
            x = f[x]
        y = x
        while True:
            r.add(y)
            y = f[y]
            if y == x:
                break
    return r


RING = _ring_set(FAV)
POS = [(0.34, 0.45), (0.52, 0.45), (0.17, 0.45), (0.0, 0.45), (0.87, 0.1), (0.76, 0.85), (0.98, 0.85)]


def _col(S, i):
    if 'used' not in S:
        return None
    bfs_ = 'start' in S
    if 'cnt' in S:
        pr = set(v for p in S['pair'] for v in p)
        if bfs_:
            if i == S.get('now'):
                return 'pink'
            if i in S['q']:
                return 'yellow'
        if i in pr:
            return 'green'
        return 'orange' if i not in RING else 'cyan'
    line = S.get('_line', 0)
    walking = line < L_DECIDE
    if 'index' in S and i == S['index'] and 'stack' in S and walking:
        return 'blue'
    if walking and 'stack' in S and i in S['stack'] and S.get('next') != i:
        return 'yellow'
    if walking and i == S.get('next') and i in S.get('used', ()):
        return 'pink'
    if i in S['used'] and not (walking and i in S.get('circle', ())):
        if 'next' in S and i == S['next'] and line >= L_DECIDE and i in S.get('circle', ()):
            return 'pink'
        return 'orange' if i not in RING else 'cyan'
    return None


def _draw(cv, S, B, box, T):
    f = S['favorite']
    pr = set(v for p in S['pair'] for v in p) if 'pair' in S else set()
    _gdraw(cv, T, box, '从 i 向 favorite[i] 连边（黄 = 当前路径，粉 = next，青 = 环，橙 = 树枝，绿 = 互相喜欢的 2 环）', POS,
           [(i, f[i]) for i in range(_N)], lambda i: _col(S, i),
           ecolor_of=lambda a, b: 'green' if (a in pr and b in pr) else 'dim')


def _cap_while1(S, B, ret):
    if S.next in S.circle:
        return f'`next = {S.next}` 已在本次路径里 → ==绕回来了，找到环==，退出'
    if S.next in S.used:
        return f'`next = {S.next}` 之前的路径已经走过 → 接到别的路径上，停下'
    return f'`next = {S.next}` 没走过也不在路径里 → 继续往前走'


def _cap_notcircle(S, B, ret):
    if S.next not in S.circle:
        return f'`next = {S.next}` 不在本次路径里：这条路径接到了旧路径上，没有新环 → `continue`'
    return f'环的入口是 `next = {S.next}`：路径上从 `{S.next}` 起往后的点都在环里'


def _cap_step(S, B, ret):
    if 'start' in S:
        return f'这是第 `{S.step}` 层：当前层所有点都扩展一遍'
    return f'弹出 `{S.now}`，已数 `step = {S.step}` 个点'


def _cap_step0(S, B, ret):
    if 'start' in S:
        return '`step` 记层数 = 链上的人数，从 0 开始'
    return '`step` 记环长：从栈顶往回弹，数到入口为止'


def _cap_if2(S, B, ret):
    if S.step == 2:
        return '`step == 2`：两人互相喜欢 → 记进 `pair`，后面各自向外找最长链'
    return f'环长 `{S.step}` ≥ 3：只能围一圈，不能再塞人 → 只和 `res` 比较'


def _cap_index(S, B, ret):
    if S.index in B.used:
        return f'`{S.index}` 已经被前面的路径走过 → 跳过'
    return f'`{S.index}` 还没走过 → 从它出发沿 favorite 一直走，找环'


CONFIG = dict(
    num=2127, title='参加会议的最多员工数', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='内向基环树 · 栈找环 + 反向 BFS 找链',
    tags=['灵神题单·图论算法', '难度分 2449'],
    code=CODE,
    call=f'Solution().maximumInvitations({FAV})',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=250),
        dict(type='map', var='g', h=120, fmt=lambda k, v: f'{k} ← {sorted(v)}', label='g[x] = 喜欢 x 的人（反图）'),
        dict(type='array', var='stack', h=100, label='stack（当前路径）'),
        dict(type='array', var='q', h=110, label='q（反向 BFS，当前层 = q[l:r]）'),
    ],
    watch=[('res', 'res', 'cyan'), 'step', 'l', 'r', ('pair', 'pair', 'green'), ('cnt', 'cnt', 'orange')],
    skip=['n = len(favorite)', 'g = {}', 'used = set()', 'used.add(', 'circle.add(', 'if favorite[index] not in g', 'g[favorite[index]] = set()',
          'circle = set', 'while stack:', 'stack.append(next)', 'stack = [index]', 'if now == next', 'break', 'step += 1', 'step = 0', 'for next in g.get', 'continue', 'l = 0', 'r = 1', 'res = 0', 'pair = []', 'q = [start]'],
    max_steps=72,
    captions={
        'g[favorite[index]].add(index)': '建反图：`g[{favorite[index]}]` 里记下喜欢 `{favorite[index]}` 的人 `{index}`，后面找链要用',
        'if index not in used': _cap_index,
        'next = favorite[index]': '`next` = `{index}` 喜欢的人 = {next}',
        'stack = [index]': '栈保存本次走过的路径：`{stack}`',
        'circle = set': '`circle` 记录本次路径上的点，用来判断有没有绕回来',
        'while next not in circle': _cap_while1,
        'used.add(next)': '`{next}` 标记为已走过',
        'circle.add(next)': '`{next}` 加入本次路径集合',
        'stack.append(next)': '`{next}` 入栈：`{stack}`',
        'next = favorite[next]': '`{next}` 入栈，路径 `{stack}`；再往前走一步：`next` = {next}',
        'if next not in circle': _cap_notcircle,
        'step = 0': _cap_step0,
        'now = stack.pop()': lambda S, B, r: (f'栈顶弹出 `now = {S.now}`，已弹 `{S.step + 1}` 个' + ('：就是入口 `' + str(S.next) + '` → 环数完，环长 ==' + str(S.step + 1) + '==' if S.now == S.next else f'：不是入口 `{S.next}`，它在环里，继续弹')),
        'while l < r': lambda S, B, r: (f'`l < r`：还有一层没扩展，层数 +1，`step` = {S.step + 1}' if S.l < S.r else f'`l = r`：没有新的人了，链长就是层数 `{S.step}`'),
        'step += 1': _cap_step,
        'if now == next': lambda S, B, r: (f'`now = {S.now}` 就是入口 `{S.next}` → 环数完了，`step = {S.step}`' if S.now == S.next
                                           else f'`now = {S.now}` ≠ 入口 `{S.next}` → 它在环里，继续弹'),
        'if step == 2': _cap_if2,
        'pair.append': '`pair` = {pair}：这个 2 环两侧各自找最长链',
        'res = max(res, step)': '`res = max({B.res}, {step}) = {res}`',
        'q = [start]': '从 `{start}` 出发沿反图 BFS：谁喜欢它、谁又喜欢那个人……每一层多一个人',
        'for now in q[l : r]': '处理这一层：`q[{l}:{r}]` = {q[l:r]}',
        'q.append(next)': '`{next}` 喜欢 `{now}` → 链上又多一人，入队 `{q}`',
        'l, r = r, len(q)': '换到下一层：`l = {l}, r = {r}`',
        'return step': '最长链共 `{ret}` 人（含终点 `{start}`）',
        'cnt = 0': '所有环长 2 的链能拼到同一桌上，所以累加到 `cnt`',
        'g[x].remove(y)': '先删掉环内的边 `{y} → {x}`：找链只能往环外走',
        'g[y].remove(x)': '再删 `{x} → {y}`，反向 BFS 不会走回环里',
        'cnt += bfs(x)': '`cnt` += `bfs({x}) + bfs({y})`：分别向环外找 `{x}` 和 `{y}` 两侧的最长链',
        'return max(res, cnt)': '答案 = `max(最长环 {res}, 2 环的链之和 {cnt})` = =={ret}==',
    },
    cards=dict(
        one_liner='每人只有一条出边：栈走一遍找出所有环，环长 2 再反向 BFS 找链',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`favorite[i]` 是第 `i` 位员工喜欢的人，圆桌上每人必须坐在他喜欢的人旁边',
                 '求圆桌最多能坐多少人',
                 '本视频：`[1,0,0,2,5,6,4]` → `4`'],
        quote='两个员工互相喜欢，也就是环的长度等于2的情况……可以在图中找到两条长度最长的链，那么将这两条链上的人员按顺序分别安排在这两个员工空闲的那一侧同样也是合法的安排。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个点只有一条出边，所以==从任意点一路走下去==，要么撞上自己这条路径（新环），要么接到旧路径',
              '环长 `≥ 3`：整桌只能是这个环，取最长；环长 `= 2`：两人各有一侧空位，可接链',
              '环长 2 的几组链互不冲突，==全部拼一桌==，和最长环比大小'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '两种情形不能混着加：答案是 `max(最长环, 所有 2 环的链之和)`',
                 '反向 BFS 前要先把 2 环内部的边从 `g` 里删掉，否则会在环里来回走',
                 '原文已是 Python 3 可运行的写法，未做任何修改',
                 '对比灵神：灵神用拓扑排序剪枝，yiduobo 用栈 + 集合直接找环'],
    ),
)
