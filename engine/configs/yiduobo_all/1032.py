def _trie_root(S):
    return S.get('self.trie')


def _layout(root):
    order, path, kids, depth = [root], {id(root): ''}, {id(root): []}, {id(root): 0}
    seen = {id(root)}
    qi = 0
    while qi < len(order):
        n = order[qi]
        qi += 1
        for ch, s in n.char_dict.items():
            if id(s) in seen:
                continue
            seen.add(id(s))
            path[id(s)] = path[id(n)] + ch
            depth[id(s)] = depth[id(n)] + 1
            kids[id(s)] = []
            kids[id(n)].append((ch, s))
            order.append(s)
    return order, path, kids, depth


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    root = _trie_root(S)
    cv.text((x0 + 18, y0 + 4), 'trie 图（橙色虚线 = next 指针，没画的都指向根；绿角标 = 单词结尾）', 22, T['muted'], bold=True)
    if root is None:
        cv.text((x0 + 18, y0 + 50), '（尚未创建）', 24, T['dim'])
        return
    order, path, kids, depth = _layout(root)
    X, cnt = {}, [0]

    def place(n):
        ks = kids[id(n)]
        if not ks:
            X[id(n)] = cnt[0]
            cnt[0] += 1
        else:
            for _, k in ks:
                place(k)
            X[id(n)] = (X[id(ks[0][1])] + X[id(ks[-1][1])]) / 2
    place(root)
    nl = max(cnt[0], 1)
    maxd = max(depth.values())
    gx = min(150, (x1 - x0 - 120) / max(nl, 1))
    gy = min(120, (y1 - y0 - 150) / max(maxd, 1))
    sx = x0 + 60 + ((x1 - x0 - 120) - gx * (nl - 1)) / 2
    P = {id(n): (sx + X[id(n)] * gx, y0 + 90 + depth[id(n)] * gy) for n in order}
    now, tmp, pos = S.get('now'), S.get('tmp'), S.get('self.pos')
    for n in order:
        for ch, k in kids[id(n)]:
            (ax, ay), (bx, by) = P[id(n)], P[id(k)]
            cv.line([(ax, ay + 24), (bx, by - 24)], T['border'], 3)
            cv.text(((ax + bx) / 2 + 12, (ay + by) / 2), ch, 22, T['muted'], anchor='lm', bold=True, mono=True)
    for n in order:
        f = n.next
        if f is not None and f is not root and id(f) in P and n is not root:
            (ax, ay), (bx, by) = P[id(n)], P[id(f)]
            if abs(ay - by) < 1:
                cv.arc_arrow((ax - 20, ay - 22), (bx + 20, by - 22), -50, T['orange'], 3)
            else:
                cv.dashed((ax - 16, ay), (bx + 16, by), T['orange'], 3)
    for n in order:
        x, y = P[id(n)]
        fill, tc = T['panel2'], T['text']
        for who, c in ((now, T['blue']), (tmp, T['cyan']), (pos, T['yellow'])):
            if who is n:
                fill, tc = c, T['bg']
        cv.rect((x - 34, y - 24, x + 34, y + 24), fill=fill, outline=T['border'], r=24)
        lab = path[id(n)] or 'root'
        cv.text((x, y), lab, 24 if lab != 'root' else 20, tc, anchor='mm', bold=True, mono=True)
        if n.end_flag:
            cv.rect((x + 18, y - 38, x + 52, y - 14), fill=T['green'], r=10)
            cv.text((x + 35, y - 26), '✓', 20, T['bg'], anchor='mm', bold=True)
    cv.text((x0 + 18, y1 - 30), '蓝 = now；青 = tmp；黄 = pos（查询时当前所在节点）', 20, T['dim'])


def _name(S, n):
    root = _trie_root(S)
    if root is None or n is None:
        return '?'
    order, path, _, _ = _layout(root)
    return path.get(id(n), '?') or 'root'


def _q(S):
    return f"`letter = {S['letter']}`" if 'letter' in S else ''


CONFIG = dict(
    num=1032, title='字符流', difficulty='Hard', category='字符串',
    author='yiduobo', technique='trie 图（trie 树 + next 指针）',
    tags=['灵神题单', '字符串'],
    code='''
class Node(object):

    def __init__(self):
        self.char_dict = {}
        self.next = None
        self.end_flag = False

class StreamChecker(object):

    def __init__(self, words):

        self.trie = Node()
        
        for word in words:
            self.add(word)
        
        q = [[self.trie, None, None]]
        l = 0 
        r = 1
        while l < r:
            now, fa, edge = q[l]
            l += 1
            if now == self.trie or fa == self.trie:
                now.next = self.trie
            else:
                tmp = fa.next
                while tmp != self.trie and edge not in tmp.char_dict:
                    tmp = tmp.next
                if edge in tmp.char_dict:
                    now.next = tmp.char_dict[edge]
                    if now.next.end_flag:
                        now.end_flag = True
                else:
                    now.next = self.trie

            for char in now.char_dict:
                q.append([now.char_dict[char], now, char])
                r += 1
        
        self.pos = self.trie

    def add(self, word):
        now = self.trie
        for char in word:
            if char not in now.char_dict:
                now.char_dict[char] = Node()
            now = now.char_dict[char]
        now.end_flag = True

    def query(self, letter):
        while self.pos != self.trie and letter not in self.pos.char_dict:
            self.pos = self.pos.next
        
        if letter in self.pos.char_dict:
            self.pos = self.pos.char_dict[letter]
        else:
            self.pos = self.trie
        
        return self.pos.end_flag
''',
    call='''obj = StreamChecker(["ab", "bc"])
res = []
for c in "abc":
    res.append(obj.query(c))
res''',
    expect=[False, True, True],
    skip=['self.char_dict = {}', 'self.next = None', 'self.end_flag = False', 'l += 1', 'r += 1', 'l = 0', 'r = 1', 'q.append(', 'self.trie = Node()',
          'for word in words', 'now = self.trie', 'now, fa, edge = q[l]'],
    max_steps=110,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', fn=lambda S: ('查询 ' + _q(S) + f"：从 pos（`{_name(S, S.get('self.pos'))}`）出发" if 'letter' in S else ''), size=24),
    ],
    watch=[('l', 'l'), ('r', 'r'), ('edge', 'edge'), ('letter', 'letter', 'blue')],
    captions={
        'self.trie = Node()': '字典树的根节点',
        'for word in words': '把单词 `{word}` 插入 trie',
        'self.add(word)': '插入 `{word}`',
        'q = [[self.trie': '建 trie 图要按层（BFS）：队列里放 `[节点, 父节点, 父到它的边字符]`，先放根',
        'while l < r': lambda S, B, r_: (f'队列里还有 `{S.r - S.l}` 个节点没处理' if S.l < S.r else '全部节点的 next 都算好了 → trie 图建好'),
        'if now == self.trie or fa == self.trie': lambda S, B, r_: (
            '==根节点或第一层节点==没有更短的后缀可用 → `next` 指向根' if S.now is S.self.trie or S.fa is S.self.trie
            else f'`{_name(S, S.now)}` 在第二层及以下，要靠父节点的 next 来找后缀'),
        'now.next = self.trie': '`next` 指向 root（没有可用的后缀）',
        'tmp = fa.next': '从父节点的 next 开始找：`tmp = fa.next`，看它有没有字符 `{edge}` 的边',
        'while tmp != self.trie and edge not in tmp.char_dict': lambda S, B, r_: (
            f'`tmp` 没有 `{S.edge}` 这条边 → 继续沿 next 往上退' if S.tmp is not S.self.trie and S.edge not in S.tmp.char_dict
            else '到根了，或者 `tmp` 有这条边 → 停止回退'),
        'tmp = tmp.next': '沿 next 向上回退，类似 KMP 的 `pos = f[pos-1]`',
        'if edge in tmp.char_dict': lambda S, B, r_: (
            f'`tmp` 有 `{S.edge}` 的边 → 这条边的终点就是 `now` 的 next' if S.edge in S.tmp.char_dict
            else f'连根都没有 `{S.edge}` 的边 → 没有可用后缀'),
        'now.next = tmp.char_dict[edge]': '`now.next` = `tmp` 沿 `{edge}` 走到的节点：它的路径是 now 路径的最长后缀',
        'if now.next.end_flag': lambda S, B, r_: ('next 是某个单词的结尾 → ==now 也要看作单词结尾==（后缀被匹配上了）' if S.now.next.end_flag
                                                 else 'next 不是单词结尾，`now` 保持原样'),
        'now.end_flag = True': '`now` 的后缀是单词 → 标记为结尾（绿角标）',
        
        40: '`pos` 是查询时在 trie 图里的当前位置，从根开始',
        'now = self.trie': '从根开始插入',
        'for char in word': '插入字符 `{char}`',
        'if char not in now.char_dict': lambda S, B, r_: ('没有 `%s` 这条边 → 新建节点' % S.char if S.char not in S.now.char_dict
                                                        else '已经有 `%s` 这条边，直接走过去' % S.char),
        'now.char_dict[char] = Node()': '新建儿子节点',
        'now = now.char_dict[char]': '走到 `{char}` 的儿子',
        'now.end_flag = True': '单词 `{word}` 结束，标记为结尾（绿角标）',
        'while self.pos != self.trie and letter not in self.pos.char_dict': lambda S, B, r_: (
            '`pos` 没有 `%s` 的边 → 沿 next 回退到更短的后缀' % S.letter if S.self.pos is not S.self.trie and S.letter not in S.self.pos.char_dict
            else '`pos` 在根，或者已经有 `%s` 的边 → 不用回退' % S.letter),
        'self.pos = self.pos.next': '回退：`pos = pos.next`（黄色节点移动）',
        'if letter in self.pos.char_dict': lambda S, B, r_: (
            '`%s` 有边 → 往前走一步' % S.letter if S.letter in S.self.pos.char_dict else '连根也没有 `%s` 的边 → 重新开始' % S.letter),
        'self.pos = self.pos.char_dict[letter]': '`pos` 沿 `{letter}` 前进一步',
        56: '没有可匹配的 → `pos` 回到根',
        'return self.pos.end_flag': lambda S, B, r_: ('`pos` 是单词结尾 → 某个单词是当前字符流的后缀，返回 ==True==' if S.self.pos.end_flag
                                                    else '`pos` 不是单词结尾 → 返回 False'),
    },
    cards=dict(
        one_liner='trie 树 + KMP 的 next：失配时沿 next 退到最长后缀',
        complexity='建图 `O(L)`，每次查询均摊 `O(1)`（`L` 为单词总长）',
        problem=['设计 `StreamChecker(words)`：不断收到字符，`query(letter)` 判断==当前字符流的某个后缀==是否是 `words` 里的单词',
                 '示例：`words = ["ab","bc"]`，依次 query `a b c`',
                 '返回 `[False, True, True]`'],
        quote='kmp算法也可以认为是trie图在单个字符串形成的trie树上的特例。对于树中的节点p，其next的定义就是层数最深的q，其满足S[root -> q]是S[root -> p]的后缀。',
        quote_src='—— yiduobo 题解原文',
        idea=['多个单词做 KMP 太慢 → 把单词建成 ==trie 树==，再给每个节点加 `next`（最长后缀节点）',
              '求 next 和 KMP 一样：看父节点的 next 有没有同字符的边，没有就继续往上退',
              '若 `next` 是单词结尾，当前节点也要算作单词结尾（后缀被匹配）',
              '查询：`pos` 在 trie 图里走，失配就沿 next 回退，走到结尾节点就返回 True'],
        result='依次得到 `False, True, True`：读到 `ab` 命中，读到 `abc` 时靠 next 从 `ab` 跳到 `b` 再走 `c` 命中 `bc` ✓',
        summary=['建图用 BFS，保证算某节点 next 时它父节点的 next 已经算好',
                 '易错：next 是结尾要把当前节点也标成结尾，否则 `abc` 查不出 `bc`',
                 '第一层节点的 next 一定是根',
                 '本题题面在库里缺失，按 LeetCode 1032 题意（字符流 StreamChecker）写',
                 '原文是 Python 2 风格（`class Node(object)`），在 Python 3 下无需改动'],
    ),
)
