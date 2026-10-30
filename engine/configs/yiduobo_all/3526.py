NUMS = [5, 2, 7]
QUERIES = [[2, 0, 1], [3, 0, 1], [1, 2, 4], [2, 1, 2]]

CODE = '''
class Solution(object):
    def getResults(self, nums, queries):
        
        n = len(nums)
        fa = [n + 2] * (n + 3)
        childs = [[n + 2] * 2 for _ in range(n + 3)]
        val = [0] * (n + 3)
        xor = [0] * (n + 3)
        size = [0] * (n + 3)
        reverse = [0] * (n + 3)

        def build(left, right):
            mid = (left + right) >> 1
            if 1 <= mid <= n:
                val[mid] = nums[mid - 1]
                xor[mid] = val[mid]
            size[mid] = 1
            
            if left < mid:
                childs[mid][0] = build(left, mid - 1)
                fa[childs[mid][0]] = mid
                size[mid] += size[childs[mid][0]]
                xor[mid] ^= xor[childs[mid][0]]
            
            if mid < right:
                childs[mid][1] = build(mid + 1, right)
                fa[childs[mid][1]] = mid
                size[mid] += size[childs[mid][1]]
                xor[mid] ^= xor[childs[mid][1]]
            
            return mid
            
        def find(k):
            now = childs[n + 2][0]
            while True:
                if reverse[now]:
                    childs[now].reverse()
                    reverse[childs[now][0]] ^= 1
                    reverse[childs[now][1]] ^= 1
                    reverse[now] = 0
            
                left_size = size[childs[now][0]] + 1
                if left_size == k:
                    return now
                if left_size > k:
                    now = childs[now][0]
                else:
                    k -= left_size
                    now = childs[now][1]
            
            return now

        def update_value(now):
            xor[now] = val[now]
            size[now] = 1
            for index in range(2):
                xor[now] ^= xor[childs[now][index]]
                size[now] += size[childs[now][index]]

        def splay(now, target):
            while fa[now] != target:
                f = fa[now]
                gf = fa[f]
                if now == childs[f][0]:
                    side = 0
                else:
                    side = 1

                if gf == target:
                    if f == childs[gf][0]:
                        childs[gf][0] = now
                    else:
                        childs[gf][1] = now
                    fa[now] = gf

                    b = childs[now][side ^ 1]
                    c = childs[f][side ^ 1]

                    fa[b] = f
                    childs[f][side] = b

                    fa[f] = now
                    childs[now][side ^ 1] = f

                    size[f] = 1 + size[b] + size[c]
                    xor[f] = val[f] ^ xor[b] ^ xor[c]

                    break

                if (childs[gf][0] == f and childs[f][0] == now) or (childs[gf][1] == f and childs[f][1] == now):
                    ggf = fa[gf]
                    if gf == childs[ggf][0]:
                        childs[ggf][0] = now
                    else:
                        childs[ggf][1] = now
                    fa[now] = ggf

                    a = childs[now][side]
                    b = childs[now][side ^ 1]
                    c = childs[f][side ^ 1]
                    d = childs[gf][side ^ 1]

                    fa[c] = gf
                    childs[gf][side] = c
                    size[gf] = 1 + size[c] + size[d]
                    xor[gf] = val[gf] ^ xor[c] ^ xor[d]

                    fa[b] = f
                    fa[gf] = f
                    childs[f][side] = b
                    childs[f][side ^ 1] = gf
                    size[f] = 1 + size[b] + size[gf]
                    xor[f] = val[f] ^ xor[b] ^ xor[gf]

                    fa[f] = now
                    childs[now][side ^ 1] = f
                
                else:
                    ggf = fa[gf]
                    if gf == childs[ggf][0]:
                        childs[ggf][0] = now
                    else:
                        childs[ggf][1] = now
                    fa[now] = ggf

                    a = childs[now][side]
                    b = childs[now][side ^ 1]
                    c = childs[f][side ^ 1]
                    d = childs[gf][side]

                    fa[a] = gf
                    childs[gf][side ^ 1] = a
                    size[gf] = 1 + size[a] + size[d]
                    xor[gf] = val[gf] ^ xor[a] ^ xor[d]

                    fa[b] = f
                    childs[f][side] = b
                    size[f] = 1 + size[b] + size[c]
                    xor[f] = val[f] ^ xor[b] ^ xor[c]

                    fa[f] = now
                    fa[gf] = now
                    childs[now][side] = gf
                    childs[now][side ^ 1] = f

            update_value(now)
                
        childs[-1][0] = build(0, n + 1)
        fa[childs[-1][0]] = n + 2

        res = []
        for q in queries:
            if q[0] == 1:
                now = find(q[1] + 2)
                val[now] = q[2]
                splay(now, n + 2)
            else:
                x = find(q[1] + 1)
                y = find(q[2] + 3)
                splay(x, n + 2)
                splay(y, x)
                
                if q[0] == 2:
                    if childs[y][0]:
                        res.append(xor[childs[y][0]])
                    else:
                        res.append(0)
                else:
                    if childs[y][0]:
                        reverse[childs[y][0]] ^= 1

        return res
'''
_L = CODE.split('\n')


def _ln(sub):
    return next(i for i, s in enumerate(_L) if sub in s)


SKIP = list(range(_ln('def build') + 1, _ln('childs[-1][0] = build'))) + ['reverse = [0]', 'size = [0]', 'xor = [0]', 'val = [0]']


def _seq(S):
    if 'childs' not in S or 'fa' not in S or 'size' not in S:
        return None
    n = S['n']
    ch, rv, va = S['childs'], S['reverse'], S['val']
    root = ch[n + 2][0]
    out = []

    def go(p, flip):
        if p == n + 2 or p is None:
            return
        flip ^= rv[p]
        a, b = (ch[p][1], ch[p][0]) if flip else (ch[p][0], ch[p][1])
        go(a, flip)
        if 1 <= p <= n:
            out.append(va[p])
        go(b, flip)
    try:
        go(root, 0)
    except RecursionError:
        return None
    return out if len(out) == n else None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'Splay 树（圈 = val，下方 ^ = 子树异或，R = 待翻转标记，0 / n+1 是哨兵）', 20, T['muted'], bold=True)
    if 'childs' not in S or 'size' not in S or 'n' not in S:
        return
    n = S['n']
    ch, va, xr, rv = S['childs'], S['val'], S['xor'], S['reverse']
    root = ch[n + 2][0]
    if root == n + 2 or (xr[root] == 0 and size_zero(S, root)):
        cv.text((x0 + 18, y0 + 50), '（还没建树）', 24, T['dim'])
        return
    order, depth = [], {}

    def ino(p, d):
        if p == n + 2 or p in depth or len(depth) > 12:
            return
        depth[p] = d
        ino(ch[p][0], d + 1)
        order.append(p)
        ino(ch[p][1], d + 1)
    ino(root, 0)
    pos = {p: i for i, p in enumerate(order)}
    maxd = max(depth.values()) + 1
    sp = min(120, (x1 - x0 - 60) / max(1, len(order)))
    dy = min(110, (y1 - y0 - 150) / max(1, maxd - 1 if maxd > 1 else 1))
    rad = min(30, sp * 0.36)
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * len(order)) / 2 + sp / 2

    def P(p):
        return sx + pos[p] * sp, y0 + 110 + depth[p] * dy

    inn = S.get('_inner') or {}
    xi, yi = S.get('x'), S.get('y')
    nowi = S.get('now')
    sub = set()
    if xi is not None and yi is not None and 'q' in S and S['q'][0] != 1 and yi in depth and ch[yi][0] != n + 2:
        st = [ch[yi][0]]
        while st:
            p = st.pop()
            if p == n + 2 or p in sub:
                continue
            sub.add(p)
            st += ch[p]
    for p in order:
        for c in ch[p]:
            if c != n + 2 and c in pos:
                cv.line([P(p), P(c)], T['border'], 3)
    for p in order:
        X, Y = P(p)
        fill = T['green'] if p in sub else T['panel2']
        outline = T['border']
        tag = None
        if p == xi and 'q' in S and S['q'][0] != 1:
            outline, tag = T['blue'], 'x'
        elif p == yi and 'q' in S and S['q'][0] != 1:
            outline, tag = T['pink'], 'y'
        elif p == nowi and 'q' in S and S['q'][0] == 1:
            outline, tag = T['yellow'], 'now'
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=outline, width=5 if tag else 2)
        label = '–' if p in (0, n + 1) else va[p]
        cv.text((X, Y), label, int(rad * 0.9), T['bg'] if p in sub else T['text'], anchor='mm', bold=True)
        cv.text((X, Y + rad + 4), f'^{xr[p]}', 18, T['cyan'], anchor='mt', mono=True)
        cv.text((X - rad - 2, Y - rad), f'#{p}', 16, T['dim'], anchor='rb', mono=True)
        if rv[p]:
            cv.text((X + rad + 2, Y - rad), 'R', 22, T['red'], anchor='lb', bold=True)
        if tag:
            cv.text((X, Y - rad - 6), tag, 20, outline, anchor='mb', bold=True)


def size_zero(S, p):
    return S['size'][p] == 0


CONFIG = dict(
    num=3526, title='范围异或查询与子数组反转', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='Splay 树 + 懒翻转 + 子树异或',
    tags=['灵神题单·常用数据结构'],
    code=CODE,
    call=f'Solution().getResults({NUMS}, {QUERIES})',
    expect=[7, 1],
    max_steps=64,
    skip=SKIP,
    views=[
        dict(type='array', var=_seq, label='当前数组（把待翻转标记都算上后的真实顺序）', cell=76, h=170),
        dict(type='custom', draw=_draw, h=420),
    ],
    watch=[('q', "S.get('q')", 'blue'), ('x', "S.get('x')", 'blue'), ('y', "S.get('y')", 'pink'), ('res', "S.get('res')", 'green')],
    captions={
        'n = len(nums)': '用 Splay 树维护数组：树的中序遍历 = 数组顺序；每个节点记子树异或 `xor`、子树大小 `size`、翻转标记 `reverse`',
        'fa = [n + 2]': '节点 `0` 和 `n+1` 是两个哨兵，`n+2` 是“空”和固定的根的父亲；`fa`、`childs` 全部先指向 `n+2`',
        'childs[-1][0] = build': '把 `0 .. n+1` 建成一棵尽量平衡的树：中点当根，左右递归；每个节点 `xor` = 自己 ^ 左子树 ^ 右子树',
        'fa[childs[-1][0]] = n + 2': '树根挂在 `n+2` 的左孩子上：以后“旋转到根”就是“旋转到 `n+2` 的孩子”，不用判断祖先是否为空',
        'res = []': '`res` 收集所有异或查询的答案',
        'for q in queries': lambda S, B, r: (f'第 `{S.queries.index(S.q) + 1}` 个操作 `{S.q}`' if not ('q' in B and B.q is S.q) else '所有操作处理完了'),
        'childs = [[n + 2]': '`childs[p] = [左孩子, 右孩子]`，初始全指向 `n+2`（= 空）',
        'if q[0] == 1': lambda S, B, r: ('`q[0] = 1`：把 `nums[{}]` 改成 `{}`'.format(S.q[1], S.q[2]) if S.q[0] == 1 else '`q[0] = {}`：区间操作，要把区间 `[{}, {}]` 单独“切”出来'.format(S.q[0], S.q[1], S.q[2])),
        'now = find(q[1] + 2)': '找中序第 `q[1] + 2` 个节点（前面还有哨兵 0），也就是 `nums[{q[1]}]` 对应的节点；`find` 一路下探时会顺手下放翻转标记',
        'val[now] = q[2]': '改成新值 `{q[2]}`',
        'splay(now, n + 2)': '把 `now` 旋转到根：旋转过程中会重新计算各节点的 `xor`、`size`，所以改过的值被正确汇总',
        'x = find(q[1] + 1)': '找区间左边界的前驱节点 `x`（中序第 `q[1] + 1` 个）：区间 `[{q[1]}, {q[2]}]` 就夹在 `x` 和 `y` 之间',
        'y = find(q[2] + 3)': '找区间右边界的后继节点 `y`（中序第 `q[2] + 3` 个）',
        'splay(x, n + 2)': '先把 `x` 旋转到根',
        'splay(y, x)': '再把 `y` 旋转到 `x` 的右孩子：这时 ==`y` 的左子树正好就是区间 `[{q[1]}, {q[2]}]` 的全部节点==（绿色）',
        'if q[0] == 2': lambda S, B, r: ('`q[0] = 2`：异或查询，直接读 `y` 左子树的 `xor`' if S.q[0] == 2 else '`q[0] = 3`：翻转，只给 `y` 的左子树根打个懒标记，不真的翻'),
        'if childs[y][0]': '区间不为空吗？`y` 的左孩子 = `{childs[y][0]}`',
        'res.append(xor[childs[y][0]])': '区间异或 = 子树异或 `xor = {xor[childs[y][0]]}`，答案加入 `res`',
        'reverse[childs[y][0]] ^= 1': '`reverse` 标记取反（红色 R）：整棵子树的左右孩子交换“欠着”，等以后 `find` 经过时再下放，复杂度不会爆',
        'return res': '全部处理完，异或查询的结果 =={ret}==',
    },
    cards=dict(
        one_liner='区间夹在两个节点之间 → 整段是一棵子树，异或查询和翻转都在子树上做',
        complexity='时间 `O((n + q) log n)` 均摊，空间 `O(n)`',
        problem=['数组 `nums` 和一串操作：`[1,i,v]` 把 `nums[i]` 改成 `v`',
                 '`[2,l,r]` 求 `nums[l..r]` 的异或，`[3,l,r]` 原地翻转 `nums[l..r]`',
                 '按顺序执行，返回所有异或查询的结果',
                 '本视频：`[5,2,7]`，操作 `[[2,0,1],[3,0,1],[1,2,4],[2,1,2]]` → `[7,1]`'],
        quote='在splay中处理区间问题，则只需将区间两侧的节点向上旋转……区间中所有元素的异或值就是q的左子树中所有节点的异或值，因此在这里对于每个节点，需要额外维护子树中所有节点的异或值。',
        quote_src='—— yiduobo 题解原文',
        idea=['Splay 树的中序遍历就是数组；多加两个哨兵 `0` 和 `n+1`，区间两边一定有节点可夹',
              '查区间 `[l, r]`：把前驱 `x` 转到根、后继 `y` 转到 `x` 的右孩子，`y` 的左子树就是整个区间',
              '每个节点额外维护子树异或 `xor`，旋转时一并更新',
              '翻转区间不真的翻：给子树根打 `reverse` 标记，之后 `find` 经过时再交换左右孩子并下放'],
        after=[dict(heading='另一份写法', lines=['原文先给了一份用类 `Node` 的写法，会超时',
                                                  '这里用的是第二份：数组实现，建树尽量平衡，两步旋转直接设置旋转后的形态'])],
        summary=['时间 `O((n + q) log n)` 均摊，空间 `O(n)`',
                 '易错：`find` 经过节点前必须先下放 `reverse`，否则按排名找错',
                 '易错：哨兵让下标整体右移 —— 改值找 `index + 2`，区间前驱 `l + 1`、后继 `r + 3`',
                 '易错：改完值要 `splay` 回根，让沿路各节点的 `xor` 重新汇总',
                 '原文可直接在 Python 3 运行，代码未改'],
    ),
)
