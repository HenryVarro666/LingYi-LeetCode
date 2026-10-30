# ---- 自定义 Trie 视图：节点是 [孩子 dict, 结尾标记] 的嵌套 list；绿 = 单词结尾，黄框 = now，黄边 = 根到 now 的路径
ADD_LINES = range(7, 14)


def _kids(nd):
    return list(nd[0].items())


def _path(root, target):
    """根到 target 的节点列表（含两端）"""
    stack = [(root, [root])]
    while stack:
        nd, p = stack.pop()
        if nd is target:
            return p
        stack += [(ch, p + [ch]) for _, ch in _kids(nd)]
    return None


def _word_row(cv, S, x0, y0, T, depth):
    ln = S.get('_line')
    w = S.get('word')
    if not isinstance(w, str):
        return
    adding = ln in ADD_LINES
    title = 'addWord 的 word' if adding else 'dfs 里剩下的 word'
    cv.text((x0 + 20, y0 + 30), title, 22, T['muted'], anchor='lm')
    bx = x0 + 230
    if not w:
        cv.text((bx, y0 + 30), "''（空串：匹配完了）", 22, T['dim'], anchor='lm', mono=True)
        return
    for k, ch in enumerate(w):
        X = bx + k * 50
        if adding:
            c = T['green'] if depth is not None and k < depth else (T['yellow'] if k == depth else T['panel2'])
        else:
            c = T['yellow'] if k == 0 else T['panel2']
        cv.rect((X, y0 + 10, X + 44, y0 + 50), fill=c, r=8)
        cv.text((X + 22, y0 + 30), ch, 26, T['bg'] if c != T['panel2'] else T['text'], anchor='mm', bold=True, mono=True)
    note = '绿 = 已插入，黄 = 当前字符' if adding else "黄 = word[0]，'.' 可以匹配任意孩子"
    cv.text((bx + len(w) * 50 + 20, y0 + 30), note, 19, T['dim'], anchor='lm')


def draw_trie(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    root = S.get('self.trie')
    cur = S.get('now')
    path = _path(root, cur) if (root is not None and cur is not None) else None
    depth = len(path) - 1 if path else None
    _word_row(cv, S, x0, y0, T, depth)
    if root is None:
        cv.text((x0 + 20, y0 + 90), '（Trie 尚未创建）', 24, T['dim'])
        return
    on_path = {id(n) for n in (path or [])}
    pos, cnt = {}, [0]

    def lay(nd, dep):
        ch = _kids(nd)
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
    top, R = y0 + 105, 24
    sp = min(200, (x1 - x0 - 80) / n)
    dy = min(120, (y1 - top - 36) / max(1, D))

    def P(nd):
        x, dep = pos[id(nd)]
        return x0 + (x1 - x0) / 2 + (x - (n - 1) / 2) * sp, top + dep * dy

    def edges(nd):
        X, Y = P(nd)
        for c, ch in _kids(nd):
            X2, Y2 = P(ch)
            hot = id(nd) in on_path and id(ch) in on_path
            cv.line([(X, Y), (X2, Y2)], T['yellow'] if hot else T['border'], 5 if hot else 3)
            mx, my = (X + X2) / 2, (Y + Y2) / 2
            cv.rect((mx - 16, my - 16, mx + 16, my + 16), fill=T['panel'], outline=T['yellow'] if hot else T['border'], r=6)
            cv.text((mx, my), c, 22, T['code'], anchor='mm', mono=True, bold=True)
            edges(ch)

    def nodes(nd):
        X, Y = P(nd)
        end = nd[1]
        hot = nd is cur
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=T['green'] if end else T['panel2'],
                     outline=T['yellow'] if hot else T['border'], width=5 if hot else 2)
        cv.text((X, Y), 'T' if end else 'F', 18, T['bg'] if end else T['dim'], anchor='mm', bold=True, mono=True)
        if hot:
            cv.text((X + R + 6, Y), 'now', 20, T['yellow'], anchor='lm', bold=True)
        for _, ch in _kids(nd):
            nodes(ch)
    edges(root)
    nodes(root)
    rx, ry = P(root)
    cv.text((rx - R - 8, ry), 'self.trie', 20, T['muted'], anchor='rm', mono=True)
    cv.text((x1 - 20, y0 + 72), '节点 = [孩子 dict, 结尾标记]', 19, T['dim'], anchor='ra')
    cv.text((x1 - 20, y0 + 98), '绿 = 结尾标记为 True', 19, T['dim'], anchor='ra')


def _if_not_word(S, B, ret):
    if not B.word:
        return '`word` 已经匹配完 → 答案取决于这个节点的==结尾标记=='
    return f'还剩 `{B.word!r}` 要匹配'


def _dot(S, B, ret):
    if B.word[0] == '.':
        return "`word[0]` 是 `'.'` → 需要==尝试当前节点的所有孩子=="
    return f'`word[0] = {B.word[0]!r}` 是普通字符 → 找对应的孩子'


def _for_next(S, B, ret):
    if 'next_char' in S and ('next_char' not in B or B.next_char != S.next_char):
        return f"让 `'.'` 去匹配孩子 `{S.next_char!r}`"
    return '所有孩子都试过了'


def _not_in(S, B, ret):
    w0 = B.word[0]
    if w0 not in B.now[0]:
        return f'`{w0!r}` 不在孩子里 → 这条路走不通'
    return f'`{w0!r}` 在孩子里 → 走下去'


CONFIG = dict(
    num=211, title='添加与搜索单词 - 数据结构设计', difficulty='Medium', category='设计',
    author='yiduobo', technique='嵌套 list 字典树 + DFS 处理通配符',
    tags=['面试经典150'],
    code='''
class WordDictionary(object):

    def __init__(self):
        self.trie = [{}, False]

    def addWord(self, word):
        now = self.trie
        for char in word:
            if char not in now[0]:
                now[0][char] = [{}, False]
            now = now[0][char]

        now[1] = True

    def dfs(self, now, word):
        if not word:
            return now[1]

        if word[0] == '.':
            for next_char in now[0].keys():
                if self.dfs(now[0][next_char], word[1:]):
                    return True
            return False
        else:
            if word[0] not in now[0]:
                return False
            return self.dfs(now[0][word[0]], word[1:])

    def search(self, word):
        return self.dfs(self.trie, word)
''',
    call='''wd = WordDictionary()
wd.addWord("bat"); wd.addWord("cad")
[wd.search("ba"), wd.search(".ad")]''',
    expect=[False, True],
    views=[
        dict(type='custom', draw=draw_trie, h=420),
        dict(type='calls', h=215, hide=('now',), label='调用栈（now 参数省略）'),
    ],
    watch=['word', 'char', 'next_char'],
    captions={
        'self.trie = [{}, False]': '每个节点 = `[孩子 dict, 结尾标记]`：根是 `[{{}}, False]`',
        'now = self.trie': 'addWord(`{word!r}`)：`now` 从根出发',
        'for char in word': lambda S, B, r: (f'下一个字符 `{S.char!r}`' if 'char' in S and ('char' not in B or B.char != S.char)
                                             else f'`{S.word!r}` 的字符都走完了'),
        'if char not in now[0]': lambda S, B, r: (f'`{S.char!r}` 不在孩子里 → 新建节点' if S.char not in S.now[0]
                                                  else f'`{S.char!r}` 已经有了 → 直接走过去'),
        'now[0][char] = [{}, False]': '新建孩子 `{char!r}`：`[{{}}, False]`',
        'now = now[0][char]': '`now` 走到 `{char!r}` 对应的孩子',
        'now[1] = True': '最后一个字符：标记 `now[1] = True`，根到这里是一个单词（变绿）',
        'if not word': _if_not_word,
        'return now[1]': lambda S, B, r: (f'返回结尾标记 `{r}`：' + ('==找到了这个单词==' if r else '路径存在，但==不是某个单词的结尾==')),
        "if word[0] == '.'": _dot,
        'for next_char in': _for_next,
        'if self.dfs(now[0][next_char]': lambda S, B, r: f"递归：在孩子 `{B.next_char!r}` 下面匹配剩下的 `{B.word[1:]!r}`",
        'return True': '这个孩子匹配成功 → 直接返回 `True`，不用再试别的孩子',
        23: lambda S, B, r: "所有孩子都失败 → 返回 `False`",
        'if word[0] not in now[0]': _not_in,
        26: '没有这条路 → 返回 `False`',
        'return self.dfs(now[0][word[0]]': lambda S, B, r: f'走到孩子 `{B.word[0]!r}`，递归匹配剩下的 `{B.word[1:]!r}`',
        'return self.dfs(self.trie, word)': lambda S, B, r: f'search(`{B.word!r}`)：从根开始 dfs',
    },
    max_steps=70,
    cards=dict(
        one_liner='普通字符走对应孩子；遇到 . 就把所有孩子都试一遍',
        complexity='addWord `O(L)`；search 无 `.` 时 `O(L)`，最坏 `O(26^L)`',
        problem=['设计 `WordDictionary`：`addWord(word)` 添加单词',
                 '`search(word)`：是否有已添加的单词与 `word` 匹配，`word` 里的 `.` 可以匹配==任意一个字母==',
                 '示例：加入 `bad, dad, mad`；查 `pad` → F，`.ad` → T，`b..` → T',
                 '本视频：加入 `bat, cad`，查 `ba` → `False`，`.ad` → `True`'],
        quote="依然是trie树的运用。按常规的方法建好树之后，在trie树中进行dfs。==若当前字符为'.'，则需要尝试当前节点的所有孩子节点==，否则找到当前字符对应的孩子节点进行下一步搜索即可。",
        quote_src='—— yiduobo 题解',
        idea=['用==嵌套的 list== 实现：节点 = `[孩子 dict, 结尾标记]`，不用定义节点类',
              '`dfs(now, word)`：每层吃掉 `word[0]`，剩下的 `word[1:]` 交给孩子',
              '`word` 吃完时，看结尾标记 `now[1]` 决定是否匹配'],
        result='`search("ba") = False`（只是前缀），`search(".ad") = True`（`.` 匹配了 `c`）✓',
        summary=['addWord `O(L)`；search 遇到 `.` 要分叉，最坏会遍历整棵树',
                 '易错：`word` 匹配完要看==结尾标记==，不能直接返回 `True`（`ba` 只是 `bat` 的前缀）',
                 '易错：`.` 分支里某个孩子成功就立刻返回 `True`，全失败才返回 `False`',
                 '`word[1:]` 每层复制字符串，也可以改成传下标',
                 '原文为 Python 2 风格，只删去了文档字符串和 LeetCode 模板注释'],
    ),
)
