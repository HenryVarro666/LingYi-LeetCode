import math
PAIRS = [[1, 2], [1, 3], [1, 4], [1, 5], [2, 4], [2, 5]]
NODES = [1, 2, 3, 4, 5]


def _pos(box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 25
    R = min((x1 - x0) / 2 - 70, (y1 - y0) / 2 - 70)
    return {v: (cx + R * math.sin(2 * math.pi * i / len(NODES)), cy - R * math.cos(2 * math.pi * i / len(NODES)))
            for i, v in enumerate(NODES)}


def _draw(cv, S, B, box, T):
    P = _pos(box)
    cv.text((box[0] + 18, box[1] + 4), '关系图（边 = pairs 里的祖孙关系；绿 = 根，蓝 = 已放进树，黄环 = now，粉环 = p）', 22, T['muted'], bold=True)
    q = S.get('q') or []
    rest = S.get('rest') or set()
    now, p = S.get('now'), S.get('p')
    cnt = S.get('cnt_dict') or {}
    for a, b in PAIRS:
        hot = (a == now and b == p) or (b == now and a == p)
        cv.line([P[a], P[b]], T['pink'] if hot else T['border'], 7 if hot else 3)
    rad = 30
    for v in NODES:
        X, Y = P[v]
        if now == v:
            cv.rect((X - rad - 7, Y - rad - 7, X + rad + 7, Y + rad + 7), outline=T['yellow'], width=5, r=rad + 7)
        if p == v:
            cv.rect((X - rad - 7, Y - rad - 7, X + rad + 7, Y + rad + 7), outline=T['pink'], width=5, r=rad + 7)
        f = None
        if q and v == q[0]:
            f = T['green']
        elif v in q:
            f = T['blue']
        cv.rect((X - rad, Y - rad, X + rad, Y + rad), fill=f or T['panel2'], outline=T['border'], r=rad)
        cv.text((X, Y), str(v), 30, T['bg'] if f else T['text'], anchor='mm', bold=True)
        if v in cnt:
            cv.text((X, Y + rad + 10), f'cnt {cnt[v]}', 19, T['muted'], anchor='mt', bold=True)


def _order(S):
    cl = S.get('cnt_list')
    if not cl:
        return '按 `cnt` 从大到小处理：先根，再逐个确定父亲'
    return '处理顺序（节点:cnt）：' + '  '.join(f'`{k}:{v}`' for k, v in cl)


def _cap_rel(S, B, r):
    now, p = S.now, S.p
    left = [x for x in S.g[now] if x in S.rest]
    if now in S.g[p]:
        bad = [x for x in left if x not in S.g[p]]
        t = f'`now = {now}` 与 `p = {p}` 有关系：p 是祖先或二者等价。检查 now 其余未放好的邻居 `{left}`：'
        return t + (f'`{bad}` 与 p 没关系 → ==矛盾，返回 0==' if bad else '都和 p 有关系 → 没矛盾')
    bad = [x for x in left if x in S.g[p]]
    t = f'`now = {now}` 与 `p = {p}` 没关系：应在不同分支。检查未放好的邻居 `{left}`：'
    return t + (f'`{bad}` 同时关联二者 → ==成环，返回 0==' if bad else '没有同时关联二者的 → 没矛盾')


CONFIG = dict(
    num=1719, title='重构一棵树的方案数', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='按关联数排序 · 逐点找父亲',
    tags=['链表树与回溯'],
    code='''
class Solution(object):
    def checkWays(self, pairs):

        g = {}
        cnt_dict = {}
        for x, y in pairs:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)
            cnt_dict[x] = cnt_dict.get(x, 0) + 1
            cnt_dict[y] = cnt_dict.get(y, 0) + 1
        
        cnt_list = sorted(cnt_dict.items(), key=lambda d:-d[1])
        n = len(cnt_list)
        if cnt_list[0][1] != n - 1:
            return 0

        rest = set([x[0] for x in cnt_list])
        index = 0
        while index < n and cnt_list[index][1] == n - 1:
            rest.remove(cnt_list[index][0])
            index += 1
        
        if index > 1:
            res = 2
        else:
            res = 1
        
        q = [cnt_list[0][0]]

        while index < n:
            now, cnt = cnt_list[index]
            for p in q[::-1]:
                if now in g[p]:
                    for x in g[now]:
                        if x in rest and x not in g[p]:
                            return 0
                    if cnt_dict[p] == cnt:
                        res = 2
                    else:
                        q.append(now)
                    rest.remove(now)
                    break
                else:
                    for x in g[now]:
                        if x in rest and x in g[p]:
                            return 0
            
            index += 1
        
        return res
''',
    call='Solution().checkWays([[1,2],[1,3],[1,4],[1,5],[2,4],[2,5]])',
    expect=1,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=_order, size=24, h=55),
        dict(type='array', var='q', label='q（已放进树的节点，越靠后越深）', cell=64, h=125),
        dict(type='set', var='rest', label='rest（还没确定位置的节点）', fmt=lambda x: str(x), h=110),
    ],
    watch=[('now', lambda S: S.get('now'), 'yellow'), ('p', lambda S: S.get('p'), 'pink'), ('res', lambda S: S.get('res'), 'green')],
    captions={
        'cnt_list = sorted': '按 `cnt` 从大到小排：关联越多越靠近根 → `{cnt_list}`',
        'if cnt_list[0][1] != n - 1': '根必须和其余 `n-1` 个点都有关系：最大 `cnt = {cnt_list[0][1]}`，`n - 1 = {n - 1}` → ' + '{"不满足，返回 0" if cnt_list[0][1] != n - 1 else "满足，有根了"}',
        'rest = set': '`rest` = 还没确定位置的节点',
        'rest.remove(cnt_list[index][0])': '`cnt = n-1` 的节点 `{cnt_list[index][0]}` 是根的候选，从 `rest` 去掉',
        'if index > 1': '`cnt = n-1` 的点有 `{index}` 个：{"多个，它们可以互换位置 → 方案数至少 2" if index > 1 else "只有一个，根唯一"}',
        'res = 2': '多个根候选 / 等价点 → 方案数 ==2==',
        'res = 1': '先假设方案唯一 `res = 1`',
        'q = [cnt_list[0][0]]': '`q` 记录已放好的节点，从根 `{q[0]}` 开始',
        'now, cnt = cnt_list': '取下一个节点 `now = {now}`，它有 `cnt = {cnt}` 个关联点',
        'for p in q[::-1]': '从最深的已放节点开始，找 `now` 的父亲：试 `p = {p}`',
        'if now in g[p]': _cap_rel,
        'if cnt_dict[p] == cnt': '`cnt[p] = {cnt_dict[p]}`，`cnt[now] = {cnt}`：{"一样大 → 二者等价，可互换" if cnt_dict[p] == cnt else "p 的关联更多 → p 是 now 的祖先，now 挂在 p 下面"}',
        'q.append(now)': '`now = {now}` 的父亲是 `{p}`，把它放进 `q` → `{q}`',
        'rest.remove(now)': '`now = {now}` 位置确定，从 `rest` 移除',
        'return res': '没有矛盾 → 返回 `{ret}`（`1` 表示树唯一）',
    },
    skip=[38, 39, 48, 49, 'cnt_dict.get', 'for x, y in pairs', 'if x not in g', 'if y not in g', 'g[x] = set()', 'g[y] = set()', 'g[x].add(y)', 'g[y].add(x)',
          'cnt_dict[y] =', 'n = len(cnt_list)', 'index += 1', 'index = 0', 'break', 'else:', 'g = {}', 'cnt_dict = {}'],
    max_steps=110,
    cards=dict(
        one_liner='根必须和所有点相关；按关联数从大到小，逐个给点找父亲',
        complexity='时间约 `O(n^2)`（逐点扫描已放节点），空间 `O(n)`',
        problem=['`pairs[i] = [x, y]`：`x`、`y` 之间有祖先-后代关系',
                 '问能否用这些点重构出一棵有根树，使 `pairs` 恰好是所有祖孙关系',
                 '返回 `0`（不能）、`1`（唯一）、`2`（多种）',
                 '示例：`pairs=[[1,2],[1,3],[1,4],[1,5],[2,4],[2,5]]` → `1`'],
        quote='树的根节点必然与其他所有节点都有联系。如果记cnt[x]为与x有联系的节点数目，那么根节点root对应的cnt就必然是n - 1。',
        quote_src='—— yiduobo 题解',
        idea=['没有 `cnt = n-1` 的点 → `0`；有多个 → 它们可互换，答案至少 `2`',
              '其余点按 `cnt` 降序处理，相当于自顶向下造树',
              '对 `now`：有关系的 `p` 是祖先或等价点；检查矛盾（与 now 相关却不与 p 相关 → `0`），没关系的分支不能共享后代'],
        result='无矛盾、无等价点 → 返回 `1`',
        summary=['时间约 `O(n^2)`：每个点最坏扫描全部已放节点；空间 `O(n)`',
                 '易错：`cnt` 相等说明等价（方案 2），不用再入 `q`；两个分支共享后代要返回 0',
                 '`q[::-1]` 从最深的开始找父亲，找到有关系的 `p` 就 `break`',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行；题面库中缺失，题意按原文与 LeetCode 原题补写'],
    ),
)
