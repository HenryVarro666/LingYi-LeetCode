
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
    return _pairs(S['cnt']) + (S['cnt'].get(S['next_v'], 0) if S.get('_line') == 18 else 0)


def _c18(S, B, r):
    return f'先数「编码完全相同」的根路径（它们之间的路径每个字母都成对）：`cnt[{_oddset(S.next_v)}]` = {S.cnt.get(S.next_v, 0)}'


def _c21(S, B, r):
    c = _contrib(S.cnt, S.next_v) - 1  # cnt 已含自己
    return (f'枚举 26 个落单字母，查「恰好差一位」的编码；`{_oddset(S.next_v)}` 一共配出 =={c}== 对，'
            f'已找到 `{_pairs(S.cnt)}` 对。把它记入 `cnt`：{S.cnt[S.next_v]} 次')


def _c17(S, B, r):
    return f'字符 `{S.s[S.child]}` 翻转对应位：根到 `{S.child}` 的编码里奇数次的字母 ==' + _oddset(S.next_v) + '=='


CONFIG = dict(
    num=2791, title='树中可以形成回文的路径数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='根节点中转 + 奇偶编码哈希表',
    tags=['前缀和', '状态压缩前缀和', '难度分 2677'],
    code='''
class Solution(object):
    def countPalindromePaths(self, parent, s):

        n = len(parent)
        g = {index : set() for index in range(n)}
        for index in range(1, n):
            g[parent[index]].add(index)

        global res
        res = 0

        cnt = {0 : 1}

        def dfs(now, v):
            global res
            for child in g[now]:
                next_v = v ^ (1 << (ord(s[child]) - 97))
                res += cnt.get(next_v, 0)
                for single in range(26):
                    res += cnt.get(next_v ^ (1 << single), 0)
                cnt[next_v] = cnt.get(next_v, 0) + 1
                dfs(child, next_v)
        
        dfs(0, 0)
        return res
''',
    call=f'Solution().countPalindromePaths({PARENT!r}, {STR!r})',
    expect=8,
    skip=['for single in', 'res += cnt.get(next_v ^'],
    views=[
        dict(type='custom', draw=_make_draw('child', 'now', 21), h=330),
        dict(type='map', var=_cnt_map('cnt'), label='cnt（根到节点的奇偶编码 → 个数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=30),
        dict(type='calls', h=170),
    ],
    watch=['now', 'child', ('next_v', 'next_v', 'blue'), ('已找到', _total, 'green')],
    captions={
        'index in range(1, n)': '建树：为每个节点登记父节点的孩子集合',
        'g[parent[index]].add': '`{index}` 是 `{parent[index]}` 的孩子',
        'global res': '`res` 用全局变量，递归里直接累加',
        'cnt = {0': '哈希表 `cnt`：根到各节点的编码出现次数；空路径编码 0 先记 1 次',
        'next_v = v ^': _c17,
        'res += cnt.get(next_v, 0)': _c18,
        'cnt[next_v] =': _c21,
        'dfs(child, next_v)': '递归 `{child}`，传入它的编码 `next_v`',
        'return res': lambda S, B, r: f'全部累加完，共 `{r}` 对',
    },
    cards=dict(
        one_liner='把路径改成「点 → 根 → 点」，多出的公共段成对抵消',
        complexity='时间 `O(26n)`，空间 `O(n)`',
        problem=['给一棵树，每个节点连向父节点的边上有字母',
                 '数有多少对 `(u, v)`，`u < v`，路径字母能重排成回文',
                 '示例：`[-1,0,0,1,1,2]`，`"acaabc"` → `8`'],
        quote='常规的两点间路径是 x - lca(x, y) - y，而对于本题，则可以变为 x - lca(x, y) - root - lca(x, y) - y，其中多出了一正一反两段……字母都是成对出现，因此不会影响最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['异构回文：奇数次的字符不超过 1 个 → 26 位奇偶编码',
              '路径换成点到根再到点，答案变成找编码相同或差一位的两条根路径',
              '从根 dfs，哈希表存已遍历的编码；对每个孩子先查再记'],
        summary=['时间 `O(26n)`，空间 `O(n)`',
                 '原文为 Python 2 风格，只删去了类型说明，`global res` 保留',
                 '编码为 2 的幂 = 路径恰好一个字母奇数次',
                 '对比灵神：灵神 dfs 返回值累加，这里用全局 `res`；都是边走边查哈希表'],
    ),
)
