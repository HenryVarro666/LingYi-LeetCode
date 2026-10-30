
PARENT = [-1, 0, 0, 1, 1, 2]
STR = 'acaabc'
N = len(PARENT)
KIDS = {i: [j for j in range(N) if PARENT[j] == i] for i in range(N)}
PRE = []
XORS = [0] * N


def _walk(v):
    PRE.append(v)
    for w in KIDS[v]:
        XORS[w] = XORS[v] ^ (1 << (ord(STR[w]) - 97))
        _walk(w)


_walk(0)
POS = {}
_leaf = [0]


def _lay(v):
    if not KIDS[v]:
        POS[v] = (_leaf[0], 0)
        _leaf[0] += 1
        return
    for w in KIDS[v]:
        _lay(w)
    xs = [POS[w][0] for w in KIDS[v]]
    POS[v] = ((min(xs) + max(xs)) / 2, 0)


_lay(0)
DEPTH = {0: 0}
for _v in PRE[1:]:
    DEPTH[_v] = DEPTH[PARENT[_v]] + 1


def _oddset(x):
    return '{' + ','.join(chr(97 + i) for i in range(26) if x >> i & 1) + '}' if x else '∅'


def _counted(S, curv, thr):
    cnt = S.get('cnt')
    if cnt is None:
        return {0}
    k = max(0, sum(cnt.values()) - 1)
    return set(PRE[:k + 1])


def _make_draw(curv, parv, thr):
    def _draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), '树（边上是字符；节点下方 = 根到它路径上奇数次的字母）', 22, T['muted'], bold=True)
        W = x1 - x0 - 100
        gx = W / max(1, max(p[0] for p in POS.values()))
        gx = min(gx, 150)
        total = gx * max(p[0] for p in POS.values())
        sx = x0 + 50 + (W - total) / 2
        gy = min(130, (y1 - y0 - 130) / max(DEPTH.values()))
        top = y0 + 70
        pt = lambda v: (sx + POS[v][0] * gx, top + DEPTH[v] * gy)
        counted = _counted(S, curv, thr)
        cur, par = S.get(curv), S.get(parv)
        for v in range(1, N):
            a, b = pt(PARENT[v]), pt(v)
            on = v == cur
            cv.line([a, b], T['blue'] if on else T['border'], 5 if on else 3)
            m = (a[0] + 0.62 * (b[0] - a[0]), a[1] + 0.62 * (b[1] - a[1]))
            left = b[0] < a[0] - 1
            cv.text((m[0] + (-16 if left else 16), m[1]), STR[v], 28, T['yellow'] if on else T['text'], anchor='rm' if left else 'lm', bold=True, mono=True)
        for v in range(N):
            X, Y = pt(v)
            fill = T['blue'] if v == cur else T['pink'] if v == par else T['green'] if v in counted else T['panel2']
            cv.rect((X - 28, Y - 28, X + 28, Y + 28), fill=fill, outline=T['border'], r=28)
            cv.text((X, Y), v, 28, T['bg'] if fill != T['panel2'] else T['muted'], anchor='mm', bold=True, mono=True)
            if v in counted:
                cv.text((X, Y + 34), _oddset(XORS[v]), 22, T['cyan'], anchor='mt', bold=True)
    return _draw


def _cnt_map(var):
    def f(S):
        d = S.get(var)
        if d is None:
            return {}
        return {_oddset(k): v for k, v in d.items() if v}
    return f


def _ok(x):
    return x == 0 or x & (x - 1) == 0


def _pairs(cnt):
    it = [(k, v) for k, v in cnt.items() if v]
    t = sum(v * (v - 1) // 2 for k, v in it)
    for i in range(len(it)):
        for j in range(i + 1, len(it)):
            if _ok(it[i][0] ^ it[j][0]):
                t += it[i][1] * it[j][1]
    return t


def _contrib(cnt, x):
    return cnt.get(x, 0) + sum(cnt.get(x ^ (1 << i), 0) for i in range(26))


def _total(S):
    if 'cnt' not in S:
        return 0
    return _pairs(S['cnt']) + (_contrib(S['cnt'], S['x']) if S.get('_line') == 14 else 0)


def _xcap(S, B, ret):
    return f'根到 `{S.w}` 的异或和 `x`：奇数次的字母 ==' + _oddset(S.x) + '=='


def _retcap(S, B, ret):
    return f'子树 `{S.w}` 里新增 `{S.res - B.res}` 对（含它自己这条根路径）→ 本层 `res` = =={S.res}=='


def _res_cap(S, B, ret):
    same = S.cnt[S.x]
    one = sum(S.cnt[S.x ^ (1 << i)] for i in range(26))
    return (f'路径 `{_oddset(S.x)}`：已有 {same} 条路径奇偶相同（全偶数次）+ {one} 条只差一个字母（恰好一个奇数次）'
            f' → 本层 `res` 增加 =={same + one}==')


CONFIG = dict(
    num=2791, title='树中可以形成回文的路径数', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='根到节点异或前缀 + 哈希表',
    tags=['前缀和', '状态压缩前缀和', '难度分 2677'],
    code='''
class Solution:
    def countPalindromePaths(self, parent: List[int], s: str) -> int:
        n = len(s)
        g = [[] for _ in range(n)]
        for i in range(1, n):
            g[parent[i]].append(i)

        cnt = Counter([0])  # 一条「空路径」
        def dfs(v: int, xor: int) -> int:
            res = 0
            for w in g[v]:
                bit = 1 << (ord(s[w]) - ord('a'))
                x = xor ^ bit
                res += cnt[x] + sum(cnt[x ^ (1 << i)] for i in range(26))
                cnt[x] += 1
                res += dfs(w, x)
            return res
        return dfs(0, 0)
''',
    call=f'Solution().countPalindromePaths({PARENT!r}, {STR!r})',
    expect=8,
    views=[
        dict(type='custom', draw=_make_draw('w', 'v', 15), h=330),
        dict(type='map', var=_cnt_map('cnt'), label='cnt（根到节点的奇偶集合 → 个数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=30),
        dict(type='calls', h=170),
    ],
    watch=['v', 'w', ('x', 'x', 'blue'), ('已找到', _total, 'green')],
    captions={
        'g[parent[i]].append': '建树：`{i}` 是 `{parent[i]}` 的孩子',
        'cnt = Counter': '`cnt` 记录「根到各节点」的异或值个数；先放一条空路径（异或值 0）',
        'bit = 1': '边 `{s[w]}` 对应一个二进制位：`bit = {bit}`',
        'x = xor ^ bit': _xcap,
        'res += cnt[x]': _res_cap,
        'cnt[x] += 1': lambda S, B, r: f'把根到 `{S.w}` 的状态记入 `cnt`：`cnt[{_oddset(S.x)}]` = {S.cnt[S.x]}',
        'res += dfs': _retcap,
        'res = 0': '进入节点 `{v}`：本层答案从 0 开始',
        'return res': '节点 `{v}` 下面共 `{res}` 条合法路径',
        'return dfs': lambda S, B, r: '全树共 `' + str(_pairs(Counter(XORS))) + '` 对',
    },
    cards=dict(
        one_liner='两点路径的异或 = 根到两点异或再异或，公共段抵消',
        complexity='时间 `O(26n)`，空间 `O(n)`',
        problem=['树上每条边有一个字母，找满足 `u < v` 的点对',
                 '路径上的字母能重排成回文就算一对',
                 '示例：`parent=[-1,0,0,1,1,2]`，`s="acaabc"` → `8`'],
        quote='设从根到 i 的路径异或和为 XOR_i……所以 v-lca-w 的异或和为 XOR_v ⊕ XOR_w。',
        quote_src='—— 灵茶山艾府题解',
        idea=['回文 = 至多一个字母奇数次 → 26 位二进制压缩奇偶',
              '根到各点的异或和算出来，LCA 到根那段异或两次抵消',
              '于是只要找「异或和为 0 或 2 的幂」的两个根路径：像两数之和一样用哈希表',
              '空路径（0）先放进 `cnt`，根到某点本身合法时才能配对'],
        summary=['时间 `O(26n)`，空间 `O(n)`',
                 '先查 `cnt` 再把当前 `x` 放进去：不会数到自己',
                 '`cnt` 初始放 `0`（空路径），否则漏掉从根出发的路径',
                 '同类题：1915、1371；树上用 dfs 传递异或和'],
    ),
)
