def make_trie_draw(root_of, kids, elabel, ntext, nfill, hot, head=None, legend=None, R=24):
    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        root = root_of(S)
        if head:
            cv.text((x0 + 18, y0 + 4), head, 22, T['muted'], bold=True)
        if root is None:
            cv.text((x0 + 18, y0 + 60), '（还没有 trie）', 22, T['dim'])
            return
        pos, cnt = {}, [0]

        def lay(nd, dep):
            ch = kids(nd)
            if not ch:
                pos[id(nd)] = (cnt[0], dep)
                cnt[0] += 1
                return cnt[0] - 1
            xs = [lay(c, dep + 1) for _, c in ch]
            pos[id(nd)] = ((xs[0] + xs[-1]) / 2, dep)
            return pos[id(nd)][0]
        lay(root, 0)
        n = max(1, cnt[0])
        D = max(p[1] for p in pos.values())
        top = y0 + 60
        sp = min(130, (x1 - x0 - 100) / n)
        dy = min(84, (y1 - top - 50) / max(1, D + 1))

        def P(nd):
            x, dep = pos[id(nd)]
            return x0 + (x1 - x0) / 2 + (x - (n - 1) / 2) * sp, top + dep * dy

        def edges(nd):
            X, Y = P(nd)
            for k, ch in kids(nd):
                X2, Y2 = P(ch)
                cv.line([(X, Y), (X2, Y2)], T['border'], 3)
                t = elabel(k)
                mx, my = (X + X2) / 2, (Y + Y2) / 2
                hw = 12 + 6 * len(t)
                cv.rect((mx - hw, my - 15, mx + hw, my + 15), fill=T['panel'], outline=T['border'], r=6)
                cv.text((mx, my), t, 20, T['code'], anchor='mm', mono=True, bold=True)
                edges(ch)
        hots = hot(S) or []
        if not isinstance(hots, (list, tuple)):
            hots = [hots]

        def nodes(nd):
            X, Y = P(nd)
            fc = nfill(S, nd, T)
            h = any(nd is z for z in hots)
            cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=fc or T['panel2'], outline=T['yellow'] if h else T['border'], width=5 if h else 2)
            t = ntext(S, nd)
            if t:
                cv.text((X, Y), t, 20 if len(t) < 3 else 15, T['bg'] if fc else T['text'], anchor='mm', bold=True)
            for _, ch in kids(nd):
                nodes(ch)
        edges(root)
        nodes(root)
        rx, ry = P(root)
        cv.text((rx - R - 8, ry), 'root', 20, T['muted'], anchor='rm')
        if legend:
            cv.text((x1 - 16, y1 - 8), legend, 18, T['dim'], anchor='rb')
    return draw


def _zcolor(S, i, v):
    ln, k = S.get('_line', 0), S.get('i')
    if ln >= 24:
        if k == i:
            return 'blue'
        if S.get('l') is not None and S.get('r') is not None and S['l'] <= i <= S['r'] and i > 0:
            return 'orange'
        return None
    if 15 < ln < 21 and k is not None and len(S['z']) - 1 - k == i:
        return 'cyan'
    return None


_draw = make_trie_draw(
    root_of=lambda S: S.get('root'),
    kids=lambda nd: list(nd.son.items()),
    elabel=lambda k: k,
    ntext=lambda S, nd: str(nd.cnt) if nd.cnt else '',
    nfill=lambda S, nd, T: T['green'] if nd.cnt else None,
    hot=lambda S: S.get('cur'),
    head='字典树：边 = 字母；绿色节点里的数字 = 在这里结束的单词个数 cnt',
)


CONFIG = dict(
    num=3045, title='统计前后缀下标对 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='Z 函数判前后缀 + 字典树数前缀',
    tags=['难度分 2328'],
    code='''
class Node:
    __slots__ = 'son', 'cnt'

    def __init__(self):
        self.son = dict()
        self.cnt = 0

class Solution:
    def countPrefixSuffixPairs(self, words: List[str]) -> int:
        ans = 0
        root = Node()
        for t in words:
            z = self.calc_z(t)
            cur = root
            for i, c in enumerate(t):
                if c not in cur.son:
                    cur.son[c] = Node()
                cur = cur.son[c]
                if z[-1 - i] == i + 1:  # t[-1-i:] == t[:i+1]
                    ans += cur.cnt
            cur.cnt += 1
        return ans

    def calc_z(self, s: str) -> List[int]:
        n = len(s)
        z = [0] * n
        l, r = 0, 0
        for i in range(1, n):
            if i <= r:
                z[i] = min(z[i - l], r - i + 1)
            while i + z[i] < n and s[z[i]] == s[i + z[i]]:
                l, r = i, i + z[i]
                z[i] += 1
        z[0] = n
        return z
''',
    call='Solution().countPrefixSuffixPairs(["a", "aba", "aa"])',
    expect=2,
    skip=['self.son = dict()', 'self.cnt = 0', 'n = len(s)', 'z = [0] * n', 'l, r = 0, 0', 'l, r = i, i + z[i]'],
    views=[
        dict(type='string', var='t', label='当前单词 t（蓝 = i）', pointers={'i': 'blue'}, h=170),
        dict(type='array', var='z', label='Z 数组（calc_z：蓝 = i，橙 = Z 盒子 [l, r]；判前后缀：青 = z[-1-i]）', color=_zcolor, h=190),
        dict(type='custom', draw=_draw, h=290),
    ],
    watch=['t', 'i', 'c', ('z[-1-i]', lambda S: S['z'][-1 - S['i']] if 'c' in S and 'z' in S and 'cur' in S and S.get('_line', 0) >= 13 else None, 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'z = self.calc_z(t)': '先算 `{t!r}` 的 Z 数组：==`z[k] = len(t) - k`== 说明长 `len(t)-k` 的后缀等于同长的前缀',
        'cur = root': '字典树里已经存着前面的单词；`cur` 从根出发，沿 `t` 的前缀往下走',
        'for i, c in enumerate(t)': lambda S, B, r: ('`t` 走完了，终点就是整个 `t` 对应的节点' if S['i'] == len(S['t']) - 1 and B.get('i') == S['i'] and B.get('c') == S['c'] else f"`t[:{S['i']+1}]` 的最后一个字母 `c = {S['c']!r}`"),
        'if c not in cur.son': lambda S, B, r: (f"`{S.c!r}` 不在 `cur.son` 里：没有前面的单词以 `t[:{S.i+1}]` 开头，要新建节点" if S.c not in S.cur.son else f"`{S.c!r}` 已在 `cur.son` 里：有单词走过同样的前缀"),
        'cur.son[c] = Node()': '新建节点，挂到 `cur` 的儿子 `{c!r}` 上',
        'cur = cur.son[c]': '往下走一步：`cur` 现在对应前缀 `t[:{i+1}]`',
        'if z[-1 - i] == i + 1': lambda S, B, r: (f"后缀 `t[-{S.i+1}:]` 的 z 值 `z[{-1-S.i}] = {S.z[-1-S.i]}` " + (f"等于 `{S.i+1}` → ==长 {S.i+1} 的前后缀相同==：只要 `t[:{S.i+1}]` 是前面某个单词，就是一对" if S.z[-1 - S.i] == S.i + 1 else f"不等于 `{S.i+1}` → 前后缀不同，这个长度不可能成对")),
        'ans += cur.cnt': '`cur.cnt = {cur.cnt}`：前面恰有 `{cur.cnt}` 个单词等于 `t[:{i+1}]`，各成一对 → `ans = {ans}`',
        'cur.cnt += 1': '`t = {t!r}` 插入完毕：终点 `cnt += 1`，后面的单词就能数到它（保证 i < j）',
        'if i <= r': lambda S, B, r: (f"`i = {S.i} <= r = {S.r}`：`i` 落在 Z 盒子 `[{S.l}, {S.r}]` 里，可以抄 `z[{S.i - S.l}]`" if S.i <= S.r else f"`i = {S.i} > r = {S.r}`：在盒子外，只能从 0 开始暴力匹配"),
        'z[i] = min(z[i - l]': '盒子里的 `z[i]` 先取 `min(z[{i-l}], {r-i+1})` = `{z[i]}`，不会越过盒子右端 `r`',
        'while i + z[i] < n': lambda S, B, r: (f"`s[{S.z[S.i]}] == s[{S.i + S.z[S.i]}]`（`{S.s[S.z[S.i]]}` = `{S.s[S.i + S.z[S.i]]}`）→ 还能再匹配一位" if S.i + S.z[S.i] < S.n and S.s[S.z[S.i]] == S.s[S.i + S.z[S.i]] else '再也匹配不下去了 → `z[i]` 定下来'),
        'z[i] += 1': '多匹配一位：`z[{i}] = {z[i]}`，Z 盒子推到 `[{l}, {r}]`',
        'z[0] = n': '`z[0]` 约定为整个长度 `{n}`',
        'return z': '`z = {z}`',
        'return ans': '一共 `{ans}` 对',
    },
    max_steps=60,
    cards=dict(
        one_liner='Z 函数判断前后缀相等，字典树统计有几个前缀单词',
        complexity='时间 `O(L)`，空间 `O(L)`，`L` 为所有字符串长度之和',
        problem=['找满足 `i < j` 且 `words[i]` 既是 `words[j]` 的==前缀==又是==后缀==的下标对 `(i, j)` 的个数',
                 '示例：`["a","aba","ababa","aa"]` → `4`',
                 '本视频：`["a","aba","aa"]` → `2`'],
        quote='如果 $z[i] = n-i$ 成立，我们只需要判断 $s$ 是否为 $t$ 的前缀。枚举 $t=words[j]$，……这可以用字典树解决，在遍历 words 的同时，维护每个字符串的出现次数。',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['对 `t`，长为 `m` 的前后缀相等 ⟺ `z[n-m] == m`（Z 函数的定义）',
              '只剩一个条件：`s = t[:m]` 是不是前面出现过的单词 → 用字典树 `cnt` 数出来',
              '边走字典树边查 `z`：走到第 `i+1` 层，若 `z[-1-i] == i+1`，就 `ans += cur.cnt`'],
        summary=['时间 `O(L)`；先数后插：`cur.cnt += 1` 放在循环之后，保证只数到前面的单词（`i < j`）',
                 '`z[-1 - i]` 对应后缀 `t[-1-i:]`；它等于 `i+1` 才表示这个后缀等于长度 `i+1` 的前缀',
                 '易错：`calc_z` 的 `z[0]` 要设为 `n`，否则整串（`i = n-1`）的前后缀检查会漏',
                 '题解方法二：用 `(s[k], s[-1-k])` 的字符对建字典树，只用一棵树，不需要 Z 函数'],
    ),
)
