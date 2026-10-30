PARENT = [-1, 0, 0, 1, 1]
NUMS = [1, 2, 3, 4, 5]
K = 3


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(PARENT)
    kids = [[] for _ in range(n)]
    for i in range(1, n):
        kids[PARENT[i]].append(i)
    depth = [0] * n
    for i in range(1, n):
        depth[i] = depth[PARENT[i]] + 1
    pos, cnt = {}, [0]

    def lay(u):
        if not kids[u]:
            pos[u] = cnt[0]
            cnt[0] += 1
        else:
            for c in kids[u]:
                lay(c)
            pos[u] = sum(pos[c] for c in kids[u]) / len(kids[u])
    lay(0)
    leaves = cnt[0]
    md = max(depth)
    W = (x1 - x0 - 80) / max(leaves, 1)
    H = (y1 - y0 - 160) / max(md, 1)
    H = min(H, 100)
    cur = S.get('_inner', {}).get('now') if S.get('_inner') else S.get('now')
    ch = S.get('_inner', {}).get('nxt') if S.get('_inner') else S.get('nxt')
    cv.text((x0 + 18, y0 + 4), '树（括号里是 nums；蓝 = 正在算的 now，粉 = 当前儿子 nxt）', 22, T['muted'], bold=True)
    P = {u: (x0 + 40 + W * (pos[u] + 0.5), y0 + 80 + H * depth[u]) for u in range(n)}
    for u in range(1, n):
        cv.line([P[PARENT[u]], P[u]], T['border'], 3)
    for u in range(n):
        px, py = P[u]
        fill = T['blue'] if u == cur else T['pink'] if u == ch else T['panel2']
        cv.rect((px - 34, py - 26, px + 34, py + 26), fill=fill, r=26, outline=T['border'])
        cv.text((px, py - 4), u, 26, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)
        cv.text((px, py + 38), f'({NUMS[u]})', 18, T['muted'], anchor='mm', mono=True)


def _fmt(d):
    return '{' + ', '.join(f'{a}:{b}' for a, b in sorted(d.items())) + '}'


def _for(S, B, ret):
    inn, now = S['_inner'], S.now
    kids = S.t[now]
    st = f'`f[{now}]` = {_fmt(S.f[now])}，`g[{now}]` = {_fmt(S.g[now])}'
    if not kids:
        return f'`{now}` 是叶子，没有儿子可合并：{st}，直接返回'
    if 'f_now' not in inn:
        return f'{st}：开始逐个合并儿子 {kids}'
    nxt = inn['nxt']
    if 'f_now' in B and B.get('nxt') == nxt and nxt == kids[-1]:
        return f'合并完最后一个儿子 `{nxt}`：{st}。儿子都合并完了，`calc({now})` 结束'
    if 'f_now' in B:
        return f'合并完儿子 `{B.nxt}`：{st}。接着合并下一个儿子 `{nxt}`'
    return f'{st}：开始逐个合并儿子 {kids}，先看 `{nxt}`'


CONFIG = dict(
    num=3939, title='统计有根树中不相邻子集的数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='树形 DP · 哈希表存模 k 状态',
    tags=['灵神题单', '动态规划', '难度分 2354'],
    code='''
class Solution(object):
    def countValidSubsets(self, parent, nums, k):
        
        n = len(parent)
        f = [{} for _ in range(n)]
        g = [{} for _ in range(n)]
        mod = 10 ** 9 + 7

        t = [[] for _ in range(n)]
        for index, p in enumerate(parent):
            if p != -1:
                t[p].append(index)

        def calc(now):
            f[now][nums[now] % k] = 1
            g[now][0] = 1

            for nxt in t[now]:
                calc(nxt)
                f_now = f[now].items()
                f[now] = {}
                g_now = g[now].items()
                g[now] = {}

                for now_v, now_cnt in f_now:
                    for nxt_v, nxt_cnt in g[nxt].items():
                        v = (now_v + nxt_v) % k
                        f[now][v] = (f[now].get(v, 0) + now_cnt * nxt_cnt) % mod
                
                for now_v, now_cnt in g_now:
                    for nxt_v, nxt_cnt in f[nxt].items():
                        v = (now_v + nxt_v) % k
                        g[now][v] = (g[now].get(v, 0) + now_cnt * nxt_cnt) % mod
                    for nxt_v, nxt_cnt in g[nxt].items():
                        v = (now_v + nxt_v) % k
                        g[now][v] = (g[now].get(v, 0) + now_cnt * nxt_cnt) % mod
            
        calc(0)
        return (f[0].get(0, 0) + g[0][0] - 1) % mod
''',
    call=f'Solution().countValidSubsets({PARENT!r}, {NUMS!r}, {K})',
    expect=4,
    skip=['for now_v, now_cnt in', 'for nxt_v, nxt_cnt in', 'v = (now_v', 'f[now][v] =', 'g[now][v] =', 'for index, p in enumerate', 'if p != -1', 't[p].append', 'n = len(parent)', 'f = [{}', 'g = [{}', 't = [[]'],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='map', var=lambda S: S['f'][S['now']] if 'now' in S else {}, label='f[now]：含 now，模 k = v 的子集数', h=110, fmt=lambda k, v: f'{k}:{v}'),
        dict(type='map', var=lambda S: S['g'][S['now']] if 'now' in S else {}, label='g[now]：不含 now，模 k = v 的子集数', h=110, fmt=lambda k, v: f'{k}:{v}'),
        dict(type='calls', h=110),
    ],
    watch=['now', 'nxt', ('f_now', lambda S: _fmt(dict(S['f_now'])) if 'f_now' in S else '', 'blue'), ('g_now', lambda S: _fmt(dict(S['g_now'])) if 'g_now' in S else '', 'pink')],
    captions={
        'f[now][nums[now]': '`f[{now}]`：==含== now，一开始只选它自己，和模 k = `{nums[now] % k}` → `f[{now}][{nums[now] % k}] = 1`',
        'g[now][0] = 1': '`g[{now}]`：==不含== now，一开始是空集，和为 0 → `g[{now}][0] = 1`',
        'for nxt in t[now]': _for,
        'calc(nxt)': '先递归把儿子 `{nxt}` 算完，得到 `f[{nxt}]`、`g[{nxt}]`',
        'f_now = f[now].items()': '先把 `f[{now}]` 的旧状态取出来（取模后不能原地改）',
        'f[now] = {}': '`f[{now}]` 清空，下面用 `g[{nxt}]` 重新合并：==含 now 就不能含儿子== → `now_cnt × nxt_cnt` 落到 `(now_v+nxt_v)%k`',
        'g_now = g[now].items()': '同理取出 `g[{now}]` 旧状态',
        'g[now] = {}': '`g[{now}]` 清空，下面合并：不含 now 时儿子 ==含不含都行== → 同时用 `f[{nxt}]` 与 `g[{nxt}]`（内部三重循环略过，结果见下一步）',
        'return (f[0]': '`f[0][0] + g[0][0] - 1` = `{f[0].get(0, 0)} + {g[0][0]} - 1` = ==`{ret}`==（减 1 去掉空集）',
    },
    cards=dict(
        one_liner='f 含 now、g 不含 now，各存一张「模 k → 方案数」的哈希表',
        complexity='时间 `O(nk^2)`，空间 `O(nk)`',
        problem=['有根树，选非空点集：任意两点不相邻（不同时选父子），权值和是 `k` 的倍数', '求方案数，对 `10^9+7` 取模',
                 '视频用 `parent=[-1,0,0,1,1], nums=[1,2,3,4,5], k=3` → `4`'],
        quote='因为不能存在相邻的节点，因此f[now]只能通过g[nxt]更新，而g[now]则不受限制。……最终答案就是f[0][0] + g[0][0] - 1。这里的减一是因为g[0][0]中必然包含了空集。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[now][v]`：含 now、子树和模 k 为 v 的子集数；`g[now]`：不含 now', '用哈希表只存「取得到」的 v，避免遍历不存在的状态',
              '合并儿子时：按乘法原理，把 `now_cnt × nxt_cnt` 加到 `(now_v+nxt_v)%k`；取模所以要清空重建'],
        summary=['时间 `O(nk^2)`，空间 `O(nk)`',
                 '易错：`f[now]` 只能并 `g[nxt]`，`g[now]` 并 `f[nxt]` 和 `g[nxt]` 两份',
                 '`f_now` / `g_now` 要先保存旧状态再清空，否则边遍历边改',
                 '原文就是 Python 3 可运行的写法，未做修改（`.items()` 视图在 `f[now] = {}` 后仍指向旧字典）',
                 '视频跳过了合并内部的三重循环逐行高亮，只在下一步展示合并后的哈希表；灵神用定长数组，这里用哈希表'],
    ),
)
