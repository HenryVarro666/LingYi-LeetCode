# ---------- 一般树自绘（custom 视图）：按孩子列表布局，状态由当前步变量推出 ----------
def _tree_pos(CH, root, box, top=46, bottom=34):
    x0, y0, x1, y1 = box
    depth, pos, cnt = {}, {}, [0]

    def go(u, d):
        depth[u] = d
        ks = CH.get(u, [])
        if not ks:
            pos[u] = cnt[0]
            cnt[0] += 1
        else:
            for k in ks:
                go(k, d + 1)
            pos[u] = sum(pos[k] for k in ks) / len(ks)
    go(root, 0)
    nl, md = max(1, cnt[0]), max(depth.values()) + 1
    sp = min(110, (x1 - x0 - 60) / nl)
    dy = min(100, (y1 - y0 - top - bottom) / max(1, md))
    rad = max(16, min(26, sp * 0.36, dy * 0.3))
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * (nl - 1)) / 2
    return {u: (sx + pos[u] * sp, y0 + top + depth[u] * dy + rad) for u in depth}, rad


def _gtree(cv, T, box, CH, root, cur, hl=(), done=(), badge=None, sub=None, title=None, anc=()):
    P, rad = _tree_pos(CH, root, box)
    if title:
        cv.text((box[0] + 18, box[1] + 4), title, 22, T['muted'], bold=True)
    for u, ks in CH.items():
        for k in ks:
            on = k in anc or k == cur
            cv.line([P[u], P[k]], T['yellow'] if on and u in anc or (on and u == cur) else T['border'], 5 if on else 3)
    for u, (X, Y) in P.items():
        fill, outl, w, tc = T['panel2'], T['border'], 2, T['text']
        if u in done:
            fill, tc = T['green'], T['bg']
        if u in hl:
            fill, tc = T['cyan'], T['bg']
        if u in anc:
            outl, w = T['yellow'], 4
        if u == cur:
            outl, w = T['blue'], 5
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=outl, width=w)
        cv.text((X, Y), u, int(rad * 0.95), tc, anchor='mm', bold=True)
        if sub and u in sub:
            cv.text((X + rad + 6, Y - 4), sub[u], 20, T['yellow'], anchor='lm', bold=True, mono=True)
        if badge and u in badge:
            s = badge[u]
            bw = cv.tlen(s, 19, bold=True) + 14
            cv.rect((X - bw / 2, Y + rad + 4, X + bw / 2, Y + rad + 28), fill=T['panel'], outline=T['green'], width=2, r=8)
            cv.text((X, Y + rad + 16), s, 19, T['green'], anchor='mm', bold=True)


def _anc(PAR, u):
    out = []
    while u is not None and PAR.get(u) is not None:
        u = PAR[u]
        out.append(u)
    return out


def _preorder(CH, root):
    out = []

    def go(u):
        out.append(u)
        for k in CH[u]:
            go(k)
    go(root)
    return out


def _subtree(CH, u):
    out = [u]
    for k in CH[u]:
        out += _subtree(CH, k)
    return out

MANAGER = [2, 2, -1, 2, 2, 4, 4]
INFORM = [0, 0, 3, 0, 2, 0, 0]
HEAD = 2
N = len(MANAGER)
CH = {i: [] for i in range(N)}
for _i, _m in enumerate(MANAGER):
    if _m >= 0:
        CH[_m].append(_i)
PAR = {i: (MANAGER[i] if MANAGER[i] >= 0 else None) for i in range(N)}
ORDER = _preorder(CH, HEAD)
PS = {}
for _u in ORDER:
    PS[_u] = INFORM[_u] + (PS[PAR[_u]] if PAR[_u] is not None else 0)


def _draw(cv, S, B, box, T):
    inner = S.get('_inner', {})
    x, y = inner.get('x'), inner.get('y')
    by = B.get('_inner', {}).get('y') if isinstance(B.get('_inner'), dict) else None
    line = S.get('_line', 0)
    vis = set()
    cur = None
    if x is not None:
        cur = x
        vis = set(ORDER[:ORDER.index(x) + 1])
        ks = CH[x]
        if y in ks and line == FOR_LINE and by == y:
            for k in ks:
                vis |= set(_subtree(CH, k))
        elif y in ks:
            for k in ks[:ks.index(y)]:
                vis |= set(_subtree(CH, k))
    anc = set(_anc(PAR, x)) if x is not None else set()
    _gtree(cv, T, box, CH, HEAD, cur, hl=(), done=set(), badge={u: f'{PS[u]}' for u in vis},
           sub={u: f'+{INFORM[u]}' for u in range(N)}, anc=anc,
           title='员工树（节点旁 +t = informTime，下方绿框 = 到达该点的 path_sum）')


CODE = '''
class Solution:
    def numOfMinutes(self, n: int, headID: int, manager: List[int], informTime: List[int]) -> int:
        g = [[] for _ in range(n)]
        for i, m in enumerate(manager):
            if m >= 0:
                g[m].append(i)  # 建树
        ans = 0
        def dfs(x: int, path_sum: int) -> None:
            path_sum += informTime[x]  # 累加递归路径上的 informTime[x]
            nonlocal ans
            ans = max(ans, path_sum)  # 更新答案的最大值
            for y in g[x]:  # 遍历 x 的儿子 y（如果没有儿子就不会进入循环）
                dfs(y, path_sum)  # 继续递归
        dfs(headID, 0)  # 从根节点 headID 开始递归
        return ans
'''
_CL = CODE.strip('\n').split('\n')
FOR_LINE = [i + 1 for i, t in enumerate(_CL) if 'for y in g[x]' in t][0]


def _g(S, k):
    return S['_inner'].get(k)


CONFIG = dict(
    num=1376, title='通知所有员工所需的时间', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='自顶向下 DFS · 路径和取最大',
    tags=['链表树与回溯', '难度分 1561'],
    code=CODE,
    call='Solution().numOfMinutes(7, 2, [2,2,-1,2,2,4,4], [0,0,3,0,2,0,0])',
    expect=5,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='informTime', label='informTime[i]（通知直属下属要花的分钟数）', cell=70, h=120),
        dict(type='calls', h=200),
    ],
    watch=[('x', lambda S: _g(S, 'x'), 'blue'), ('path_sum', lambda S: _g(S, 'path_sum'), 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'g = [[]': '`g[m]` 存 m 的所有直属下属，先把树建出来',
        'g[m].append(i)': '`{m}` 是 `{i}` 的负责人 → 把 `{i}` 挂到 `g[{m}]` 下面：`g[{m}] = {g[m]}`',
        'ans = 0': '`ans` 记录「所有人都收到通知」的最晚时刻',
        'path_sum += informTime[x]': lambda S, B, r: f"员工 `{_g(S, 'x')}` 收到消息时已过 `{_g(S, 'path_sum') - S['informTime'][_g(S, 'x')]}` 分钟，通知下属还要 `{S['informTime'][_g(S, 'x')]}` 分钟 → ==path_sum = {_g(S, 'path_sum')}==（下属开始传播的时刻）",
        'ans = max': lambda S, B, r: f"`ans = max({B.ans}, {_g(S, 'path_sum')}) = {S.ans}`：路径上的 informTime 之和，取最大值就是最晚通知到的时间",
        'for y in g[x]': lambda S, B, r: (f"枚举 `{_g(S, 'x')}` 的下属 `{_g(S, 'y')}`" if _g(S, 'y') != B['_inner'].get('y') else f"`{_g(S, 'x')}` 的下属都处理完了，递归返回上一层"),
        'dfs(y, path_sum)': lambda S, B, r: f"带着 `path_sum = {B['_inner'].get('path_sum')}` 往下走到下属 `{B['_inner'].get('y')}`：他从这一刻开始工作",
        'return ans': '所有员工都走完了，最大路径和 `{ans}` 就是答案',
    },
    skip=['nonlocal ans', 'dfs(headID, 0)', 'for i, m in enumerate'],
    max_steps=90,
    cards=dict(
        one_liner='本质是 104 题求最大深度：把递归里的 `1` 换成 `informTime[x]`',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['公司有 `n` 名员工，`manager[i]` 是 `i` 的直属负责人，总负责人是 `headID`',
                 '员工 `i` 通知所有直属下属要花 `informTime[i]` 分钟',
                 '求通知到所有员工的最少分钟数',
                 '本视频：`headID = 2`，答案 `3 + 2 = 5`'],
        quote='本质是 104. 二叉树的最大深度，把递归中的 1 替换成 informTime[x]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先用 `manager` 把每个人的下属预处理成 `g`：一般树不是二叉树',
              '自顶向下：每往下一层，`path_sum` 加上当前员工的 `informTime`',
              '每个点都更新 `ans = max(ans, path_sum)`，最大的路径和就是最晚被通知到的时刻'],
        result='所有节点遍历完，最大 `path_sum = 5` → 返回 `5`',
        summary=['时间 `O(n)`：每个节点恰好访问一次；空间 `O(n)`：链状时递归栈深 n',
                 '易错：叶子的 `informTime` 是 0，所以不用特判叶子',
                 '易错：`manager[headID] = -1` 要跳过，否则会把 `-1` 当下标建树',
                 '另有自底向上写法（返回 `max(dfs(y)) + informTime[x]`）、记忆化搜索和 `O(1)` 空间的原地写法，思想相同'],
    ),
)
