def _tree(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '基因树（黄环 = 正在 dfs 的节点，蓝 = 根到它的路径，旁边 = 挂在该节点的询问 [第几个: x]）', 21, T['muted'], bold=True)
    g, root = S.get('g'), S.get('root')
    if not isinstance(g, dict) or root is None:
        return
    pos = [0]
    place = {}

    def lay(v, d):
        ks = sorted(g[v])
        if not ks:
            place[v] = (pos[0], d)
            pos[0] += 1
            return pos[0] - 1
        xs = [lay(c, d + 1) for c in ks]
        place[v] = ((xs[0] + xs[-1]) / 2, d)
        return place[v][0]

    lay(root, 0)
    cols = max(pos[0], 1)
    maxd = max(d for _, d in place.values())
    gx = min(130, (x1 - x0 - 200) / cols)
    gy = min(70, (y1 - y0 - 90) / max(maxd, 1))
    P = {v: (x0 + 100 + (x1 - x0 - 200 - gx * (cols - 1)) / 2 + a * gx, y0 + 62 + d * gy) for v, (a, d) in place.items()}
    now = S.get('now')
    par = S.get('parents') or []
    path = set()
    c = now
    while c is not None and c != -1 and isinstance(c, int) and c < len(par) + 1:
        path.add(c)
        c = par[c] if c < len(par) else None
    for v, ks in g.items():
        for c in ks:
            cv.line([(P[v][0], P[v][1] + 20), (P[c][0], P[c][1] - 20)], T['blue'] if (v in path and c in path) else T['muted'], 3 if (v in path and c in path) else 2)
    qd = S.get('query_dict') or {}
    for v, (X, Y) in P.items():
        on = v in path
        cv.rect((X - 20, Y - 20, X + 20, Y + 20), fill=T['blue'] if on else T['panel2'],
                outline=T['yellow'] if v == now else T['border'], width=5 if v == now else 2, r=20)
        cv.text((X, Y), v, 24, T['bg'] if on else T['text'], anchor='mm', bold=True)
        if v in qd:
            cv.text((X + 28, Y), ' '.join(f'q{i}:{val}' for i, val in qd[v]), 18, T['pink'], anchor='lm', bold=True, mono=True)


def _lay(node, depth, pos, out):
    ks = [(str(i), c) for i, c in enumerate(node.child) if c is not None]
    if not ks:
        pos[0] += 1
        out.append((node, depth, pos[0] - 1, []))
        return pos[0] - 1
    xs = [_lay(c, depth + 1, pos, out) for k, c in ks]
    x = (xs[0] + xs[-1]) / 2
    out.append((node, depth, x, ks))
    return x


def _trie(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '0-1 字典树（圆内 = weight，=0 表示已被删除；黄环 = 当前走到的位置 p）', 21, T['muted'], bold=True)
    trie = S.get('trie')
    if trie is None:
        return
    out = []
    pos = [0]
    _lay(trie, 0, pos, out)
    maxd = max(o[1] for o in out)
    cols = max(pos[0], 1)
    gx = min(150, (x1 - x0 - 100) / cols)
    gy = min(80, (y1 - y0 - 100) / max(maxd, 1))
    P = {id(o[0]): (x0 + 50 + (x1 - x0 - 100 - gx * (cols - 1)) / 2 + o[2] * gx, y0 + 60 + o[1] * gy) for o in out}
    cur = S.get('p')
    for node, d, x, ks in out:
        a = P[id(node)]
        for k, c in ks:
            b = P[id(c)]
            alive = c.weight > 0
            cv.line([(a[0], a[1] + 22), (b[0], b[1] - 22)], T['muted'] if alive else T['border'], 2)
            cv.text(((a[0] + b[0]) / 2 + (-14 if k == '0' else 14), (a[1] + b[1]) / 2), k, 22,
                    (T['cyan'] if k == '0' else T['pink']) if alive else T['dim'], anchor='mm', bold=True, mono=True)
    for node, d, x, ks in out:
        X, Y = P[id(node)]
        alive = node.weight > 0 or d == 0
        ring = T['yellow'] if node is cur else None
        cv.rect((X - 22, Y - 22, X + 22, Y + 22), fill=T['panel2'] if alive else T['bg'], outline=ring or T['border'], width=5 if ring else 2, r=22)
        cv.text((X, Y), 'root' if d == 0 else node.weight, 17 if d == 0 else 24, T['text'] if alive else T['dim'], anchor='mm', bold=True)


CONFIG = dict(
    num=1938, title='查询最大基因差', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='离线 dfs + 可回退 0-1 字典树',
    tags=['字典树', '离线算法', '难度分 2503'],
    code='''
class Trie(object):
    def __init__(self):
        self.child = [None, None]
        self.weight = 0

class Solution(object):
    def maxGeneticDifference(self, parents, queries):

        n = len(parents)
        root = None

        g = {x : set() for x in range(n)}
        for index, fa in enumerate(parents):
            if fa == -1:
                root = index
            else:
                g[fa].add(index)

        max_num = n
        query_dict = {}
        for index, [node, val] in enumerate(queries):
            if node not in query_dict:
                query_dict[node] = []
            query_dict[node].append([index, val])
            max_num = max(max_num, val)

        pow2 = [1]
        while pow2[-1] <= max_num:
            pow2.append(pow2[-1] + pow2[-1])
        pow2.reverse()
        
        res = [0] * len(queries)
        trie = Trie()
        self.dfs(root, g, trie, query_dict, res, pow2)
        return res
    
    def dfs(self, now, g, trie, query_dict, res, pow2):
        tmp = now
        p = trie
        for pow_val in pow2:
            if tmp >= pow_val:
                v = 1
                tmp -= pow_val
            else:
                v = 0
        
            if p.child[v] is None:
                p.child[v] = Trie()
            
            p = p.child[v]
            p.weight += 1
        
        if now in query_dict:
            for index, val in query_dict[now]:
                p = trie
                s = 0
                for pow_val in pow2:
                    if val >= pow_val:
                        v = 1
                        val -= pow_val
                    else:
                        v = 0
                    
                    if p.child[1 - v] is not None and p.child[1 - v].weight > 0:
                        s += pow_val
                        p = p.child[1 - v]
                    else:
                        p = p.child[v]
                
                res[index] = s
            
        for next in g[now]:
            self.dfs(next, g, trie, query_dict, res, pow2)
        
        tmp = now
        p = trie
        for pow_val in pow2:
            if tmp >= pow_val:
                v = 1
                tmp -= pow_val
            else:
                v = 0
            
            p = p.child[v]
            p.weight -= 1
''',
    call='Solution().maxGeneticDifference([-1, 0, 0], [[1, 2], [2, 2]])',
    expect=[3, 2],
    views=[
        dict(type='custom', draw=_tree, h=230),
        dict(type='custom', draw=_trie, h=340),
        dict(type='array', var='res', label='res（每个询问的答案）', cell=90, h=140),
    ],
    watch=['now', 'pow_val', 'v', 'val', 's', ('p.weight', lambda S: S['p'].weight if getattr(S.get('p'), 'weight', None) is not None else '', 'yellow')],
    skip=[54, 72, 3, 4, 9, 10, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 25, 27, 28, 29, 30, 32, 33, 38, 39, 40, 41, 42, 43, 44,
          45, 47, 48, 50, 55, 56, 57, 58, 59, 60, 61, 62, 66, 67, 68, 75, 76, 77, 78, 79, 80, 81, 82, 84, 86],
    max_steps=120,
    captions={
        24: '询问 `#{index}` = `[节点 {node}, 数 {val}]`：按节点分组存起来（==离线==：先收集，再一起回答）',
        31: '位权 `pow2 = {pow2}`：从高到低，用来拆二进制位',
        34: lambda S, B, r: '从根开始 dfs：沿途把节点编号插进字典树，回答询问，回溯时再删掉',
        51: '节点 `{now}` 的第 `{pow_val}` 位是 `{v}`：走 `{v}` 这条边，`weight += 1` → ==`{p.weight}`==（路径上的数都在树里）',
        53: lambda S, B, r: (f'节点 `{S.now}` 有询问 → 此时字典树里恰好是根到 `{S.now}` 路径上的数' if S.now in S.query_dict else f'节点 `{S.now}` 没有询问'),
        # 54: '回答询问 `#{index}`：`val = {val}`，在字典树里找和它异或最大的数',
        64: lambda S, B, r: (lambda c: f'`val` 这一位是 `{S.v}`，想走相反的 `{1 - S.v}`：' + ('对面存在且 weight > 0 → ==能走，这位异或得 1==' if c is not None and c.weight > 0
                                                              else '对面没有（或已被删除）→ 只能走同侧，这位异或得 0'))(S.p.child[1 - S.v]),
        65: '这一位异或得 1：`s += {pow_val}` → ==`{s}`==，走到对面',
        70: '这个询问答案 `res[{index}] = {s}`',
        72: lambda S, B, r: (f'递归处理 `{S.now}` 的孩子：字典树保持着根到 `{S.now}` 的路径' if len(S.g[S.now]) else f'`{S.now}` 是叶子，没有孩子'),
        73: '进入孩子 `{next}`：在父亲的字典树基础上再插入它自己',
        83: '',
        85: '回溯：节点 `{now}` 的第 `{pow_val}` 位路径 `weight -= 1` → `{p.weight}`；==变成 0 就等于删除，不影响其他子树==',
        35: '全部询问回答完：`{res}`',
    },
    cards=dict(
        one_liner='离线 dfs：进入节点就插入字典树，离开就删掉，树里永远是根到当前节点的路径',
        complexity='时间 `O((n + q) · log V)`，空间 `O(n · log V)`',
        problem=['有根树，节点编号就是基因值；询问 `[node, val]`：求 `val` 与「根到 node 路径上任一节点编号」异或的最大值',
                 '返回每个询问的答案',
                 '本视频：`parents = [-1,0,0]`，询问 `[1,2] [2,2]` → `[3,2]`'],
        quote='对于node而言，设其父亲节点为fa，那么就可以在根节点到fa构造的trie树的基础上，再加入node自身二进制表示的结果，从而得到想要的从根节点到node的trie树。',
        quote_src='—— yiduobo 题解原文',
        idea=['求异或最值 → 0-1 字典树，高位到低位尽量走相反的边（同第 1707 题）',
              '难点：每个询问要的字典树不同（只含根到 node 的路径）',
              '==离线==：先按节点收集询问；dfs 进入时插入、离开时 `weight -= 1` 删除，复用父亲的字典树'],
        summary=['时间 `O((n+q)·log V)`，空间 `O(n·log V)`，`V` 取节点数与询问值的最大值',
                 '删除只做 `weight -= 1`，不真删节点；走边前必须检查 `weight > 0`',
                 '先插入、再回答、再递归孩子、最后删除：顺序不能错',
                 '本题代码在 Python 3 下无需改动即可运行'],
    ),
)
