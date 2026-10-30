def _root(S):
    if S.get('self.root') is not None:
        return S['self.root']
    for k in ('ac',):
        o = S.get(k)
        if o is not None and hasattr(o, 'root'):
            return o.root
    return None


def _trie(root):
    """BFS 取出真正的字典树边（虚拟 son 指向的节点一定已经被发现过）"""
    order, path, par, depth = [root], {id(root): ''}, {}, {id(root): 0}
    kids = {id(root): []}
    seen = {id(root)}
    qi = 0
    while qi < len(order):
        n = order[qi]
        qi += 1
        for i, s in enumerate(n.son):
            if s is None or id(s) in seen:
                continue
            seen.add(id(s))
            path[id(s)] = path[id(n)] + chr(97 + i)
            depth[id(s)] = depth[id(n)] + 1
            kids[id(s)] = []
            kids[id(n)].append(s)
            par[id(s)] = n
            order.append(s)
    return order, path, kids, depth


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    root = _root(S)
    cv.text((x0 + 18, y0 + 4), 'AC 自动机（字典树 + fail 指针；橙色虚线 = fail，没画的 fail 都指向 root）', 22, T['muted'], bold=True)
    if root is None:
        cv.text((x0 + 18, y0 + 50), '（尚未创建）', 24, T['dim'])
        return
    order, path, kids, depth = _trie(root)
    # 叶子均分横坐标，父节点在子节点中间
    X = {}
    cnt = [0]

    def place(n):
        ks = kids[id(n)]
        if not ks:
            X[id(n)] = cnt[0]
            cnt[0] += 1
        else:
            for k in ks:
                place(k)
            X[id(n)] = (X[id(ks[0])] + X[id(ks[-1])]) / 2
    place(root)
    nl = max(cnt[0], 1)
    maxd = max(depth.values())
    gx = min(150, (x1 - x0 - 120) / max(nl, 1))
    gy = min(120, (y1 - y0 - 140) / max(maxd, 1))
    sx = x0 + 60 + ((x1 - x0 - 120) - gx * (nl - 1)) / 2
    P = {id(n): (sx + X[id(n)] * gx, y0 + 90 + depth[id(n)] * gy) for n in order}
    cur, mn = S.get('cur'), S.get('match_node')
    for n in order:
        for k in kids[id(n)]:
            (ax, ay), (bx, by) = P[id(n)], P[id(k)]
            cv.line([(ax, ay + 24), (bx, by - 24)], T['border'], 3)
            cv.text(((ax + bx) / 2 + 12, (ay + by) / 2), path[id(k)][-1], 22, T['muted'], anchor='lm', bold=True, mono=True)
    for n in order:
        f = n.fail
        if f is not None and f is not root and id(f) in P and n is not root:
            (ax, ay), (bx, by) = P[id(n)], P[id(f)]
            if abs(ay - by) < 1:
                cv.arc_arrow((ax - 20, ay - 22), (bx + 20, by - 22), -50, T['orange'], 3)
            else:
                cv.dashed((ax - 16, ay), (bx + 16, by), T['orange'], 3)
    for n in order:
        x, y = P[id(n)]
        fill = T['panel2']
        if n is cur:
            fill = T['blue']
        if n is mn and mn is not None:
            fill = T['yellow']
        cv.rect((x - 34, y - 24, x + 34, y + 24), fill=fill, outline=T['border'], r=24)
        lab = path[id(n)] or 'root'
        cv.text((x, y), lab, 24 if lab != 'root' else 20, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True, mono=True)
        if n.cnt > 0:
            cv.rect((x + 18, y - 38, x + 52, y - 14), fill=T['green'], r=10)
            cv.text((x + 35, y - 26), n.cnt, 20, T['bg'], anchor='mm', bold=True)
        elif n.cnt < 0:
            cv.text((x + 35, y - 26), '✓', 22, T['dim'], anchor='mm', bold=True)
    cv.text((x0 + 18, y1 - 30), '绿角标 = 以此结尾的模式串个数；蓝 = cur；黄 = match_node；灰 ✓ = 已统计', 20, T['dim'])


def _fl(S, B, r):
    return ''


CONFIG = dict(
    num=1967, title='作为子字符串出现在单词中的字符串数目', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='AC 自动机（方法二）',
    tags=['灵神题单', '字符串'],
    code='''
class Node:
    __slots__ = 'son', 'fail', 'last', 'cnt'

    def __init__(self):
        self.son = [None] * 26
        self.fail = None  # 当 node.son[i] 失配时，node.fail.son[i] 即为下一个待匹配节点（等于 root 则表示没有匹配）
        self.last = None  # 后缀链接（suffix link），用来快速跳到一定是某个模式串末尾的节点（等于 root 则表示匹配结束）
        self.cnt = 0  # node 是 cnt 个模式串的末尾

class AhoCorasick:
    def __init__(self):
        self.root = Node()

    # 把模式串 pattern 插入 AC 自动机（代码和字典树一样）
    def put(self, pattern: str) -> None:
        cur = self.root
        for ch in pattern:
            i = ord(ch) - ord('a')
            if cur.son[i] is None:
                cur.son[i] = Node()
            cur = cur.son[i]
        cur.cnt += 1

    # BFS，构建 AC 自动机的 fail 和 last，方便快速查询
    def build_fail(self) -> None:
        self.root.fail = self.root.last = self.root

        q = deque()
        for i, son in enumerate(self.root.son):
            if son is None:
                self.root.son[i] = self.root
                continue
            son.fail = son.last = self.root  # 第一层的 fail 都指向根节点
            q.append(son)

        # BFS
        while q:
            cur = q.popleft()
            for i, son in enumerate(cur.son):
                if son is None:
                    # 把虚拟子节点 cur.son[i] 设置为 cur.fail.son[i]
                    # 方便失配时直接跳到下一个可能匹配的位置（但不一定是某个模式串的末尾）
                    cur.son[i] = cur.fail.son[i]
                    continue
                son.fail = cur.fail.son[i]  # 计算失配位置
                # 沿着 last 往上走，可以直接跳到一定是某个模式串末尾的节点（如果跳到 root 表示匹配结束）
                son.last = son.fail if son.fail.cnt else son.fail.last
                q.append(son)

class Solution:
    def numOfStrings(self, patterns: List[str], word: str) -> int:
        ac = AhoCorasick()
        for pattern in patterns:
            ac.put(pattern)
        ac.build_fail()

        ord_a = ord('a')
        cur = ac.root
        ans = 0
        for ch in word:
            cur = cur.son[ord(ch) - ord_a]  # 如果没有匹配，相当于移动到 fail 的 son[ord(ch)-ord_a]
            match_node = cur
            while match_node.cnt >= 0:
                ans += match_node.cnt
                match_node.cnt = -1  # 避免重复统计
                match_node = match_node.last  # 可能匹配更短的模式串，要继续在 last 链上找
        return ans
''',
    call='Solution().numOfStrings(["ab", "bc"], "abc")',
    expect=2,
    skip=['self.son = [None] * 26', 'self.fail = None', 'self.last = None', 'self.cnt = 0', 'self.root = Node()',
          'for i, son in enumerate', 'if son is None', 'self.root.son[i] = self.root', 'cur.son[i] = cur.fail.son[i]',
          'continue', 'ord_a = ord', "i = ord(ch) - ord('a')", 'ac.put(pattern)', 'q.append(son)', 'match_node = cur', 'ans = 0', 'self.root.fail = self.root.last', 'ac = AhoCorasick()'],
    max_steps=100,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', fn=lambda S: (f"word = `{S['word']}`，已读到 `{S['ch']}`" if 'ch' in S and 'word' in S else ''), size=24),
    ],
    watch=[('ans', 'ans', 'green'), 'ch', 'pattern', 'i'],
    captions={
        'for pattern in patterns': '把模式串 `{pattern}` 插进 AC 自动机',
        'cur = self.root': '从根节点出发，和字典树插入一样',
        'for ch in pattern': '处理字母 `{ch}`',
        'i = ord(ch)': '`{ch}` 对应儿子下标 `i = {i}`',
        'cur = cur.son[i]': '沿着 `{ch}` 走到儿子（新建的或已有的）',
        'cur.cnt += 1': '模式串 `{pattern}` 到此结束，`cnt` 加一 → 这个节点标上绿角标',
        'ac.put(pattern)': '插入 `{pattern}`',
        'ac.build_fail()': '字典树建好了，BFS 给每个节点算 fail',
        'self.root.fail = self.root.last': 'root 的 fail、last 都指向自己',
        'q = deque()': '队列里放第一层节点，按层从浅到深算 fail',
        'son.fail = son.last = self.root': '第一层节点 `{chr(97 + i)}` 的 fail = root（只剩一个字母，没有更短的后缀）',
        'q.append(son)': '把这个节点入队，之后处理它的儿子',
        'while q': lambda S, B, r: ('队列里还有节点，继续' if S.q else '队列空了，所有 fail 都算好 → 查询时失配也能 O(1) 跳转'),
        'cur = q.popleft()': '取出节点 `{cur.__class__.__name__}`，用它的 fail 去给儿子算 fail',
        'son.fail = cur.fail.son[i]': '儿子 `{chr(97 + i)}` 的 fail = ==cur.fail 的同字母儿子==（失配后下一个可能匹配的位置）',
        'son.last = son.fail if son.fail.cnt': '`last` = 沿 fail 链最近的“某个模式串末尾”：`fail` 本身是末尾就取它，否则取 `fail.last`',
        'cur = ac.root': '匹配从根节点开始，`cur` 是当前所在的自动机状态',
        'ans = 0': '`ans` 统计有多少个模式串出现',
        'for ch in word': '读入 word 的字母 `{ch}`',
        'cur = cur.son[ord(ch)': '`cur` 走 `{ch}` 这条边（失配的边已经被改成了 fail 的边，所以不用循环回退）',
        'match_node = cur': '从 `cur` 开始，沿 `last` 链收集以它为后缀的所有模式串',
        'while match_node.cnt >= 0': lambda S, B, r: (
            f'`match_node.cnt = {S.match_node.cnt} >= 0` → 这个节点还没统计过，进去统计'
            if S.match_node.cnt >= 0 else '`cnt = -1`：已经统计过（或走到了 root）→ 这个字母处理完了'),
        'ans += match_node.cnt': '`ans += {match_node.cnt}` → {ans}（以这个节点结尾的模式串都出现了）',
        'match_node.cnt = -1': '标成 -1，避免以后再走到这里重复统计',
        'match_node = match_node.last': '沿 `last` 跳到更短的、一定是模式串末尾的后缀节点',
        'return ans': 'word 读完了，一共 `{ans}` 个模式串作为子串出现',
    },
    cards=dict(
        one_liner='字典树 + fail 指针：读一遍 word，同时匹配所有模式串',
        complexity='时间 `O(L|Σ| + n)`，空间 `O(L|Σ| + n)`',
        problem=['给 `patterns` 和 `word`，数有多少个模式串是 `word` 的==子字符串==',
                 '示例：`["a","abc","bc","d"]`，`"abc"` → `3`',
                 '本视频：`["ab","bc"]`，`"abc"` → `2`'],
        quote='本题数据范围小，AC 自动机运行时间比暴力慢。读者可以在 P3808 AC 自动机（简单版）提交数据范围更大的版本。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['先把所有模式串插进字典树，再 BFS 给每个节点算 ==fail==：失配时下一个待匹配的节点',
              '把缺失的儿子补成 `fail.son[i]`，匹配时==一步跳转==，不用 while 回退',
              '`last` 后缀链接直接跳到“一定是某个模式串末尾”的节点；`cnt` 置 -1 防重复统计'],
        result='`"ab"` 和 `"bc"` 都在 `"abc"` 里 → 2 ✓；读到 `c` 时靠 fail 从 `ab` 一步跳到 `bc`',
        after=[dict(heading='方法一：暴力', lines=[
            '`sum(pattern in word for pattern in patterns)`，一行搞定',
            '本题数据只有 100，暴力比 AC 自动机还快；AC 自动机是为多模式串大数据准备的'])],
        summary=['时间 `O(L|Σ| + n)`，`L` 为模式串总长，`|Σ| = 26`',
                 '易错：`cnt` 置 -1 要在累加之后，否则重复模式串会少算',
                 '`while match_node.cnt >= 0` 靠 root 的 cnt 被置 -1 来终止',
                 '题单位置：字符串 · 七、AC 自动机'],
    ),
)
