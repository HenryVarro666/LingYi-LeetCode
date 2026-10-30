def _kids(nd):
    return list(nd.next_dict.items())


def _prod(S):
    return S.get('products') or []


def _names(S, nd):
    P = _prod(S)
    return [P[i] for i in nd.candidate if i is not None]


def _depth(S):
    root, cur = S.get('root'), S.get('now')
    if root is None or cur is None:
        return None
    st = [(root, 0)]
    while st:
        nd, d = st.pop()
        if nd is cur:
            return d
        st += [(c, d + 1) for _, c in _kids(nd)]
    return None


def draw_trie(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    root, cur = S.get('root'), S.get('now')
    searching = 'res' in S
    word = S.get('searchWord') if searching else S.get('word')
    d = _depth(S)
    if isinstance(word, str):
        cv.text((x0 + 20, y0 + 30), 'searchWord' if searching else 'word', 22, T['muted'], anchor='lm')
        for k, ch in enumerate(word):
            X = x0 + 150 + k * 50
            c = T['green'] if d is not None and k < d else (T['yellow'] if k == d else T['panel2'])
            cv.rect((X, y0 + 10, X + 44, y0 + 50), fill=c, r=8)
            cv.text((X + 22, y0 + 30), ch, 26, T['bg'] if c != T['panel2'] else T['text'], anchor='mm', bold=True, mono=True)
    if root is None:
        cv.text((x0 + 20, y0 + 90), '（Trie 尚未创建）', 24, T['dim'])
        return
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
    top = y0 + 110
    sp = min(200, (x1 - x0 - 60) / n)
    dy = min(130, (y1 - top - 60) / max(1, D + 1))

    def P(nd):
        x, dep = pos[id(nd)]
        return x0 + (x1 - x0) / 2 + (x - (n - 1) / 2) * sp, top + dep * dy

    def edges(nd):
        X, Y = P(nd)
        for c, ch in _kids(nd):
            X2, Y2 = P(ch)
            cv.line([(X, Y), (X2, Y2)], T['border'], 3)
            mx, my = (X + X2) / 2, (Y + Y2) / 2
            cv.rect((mx - 14, my - 14, mx + 14, my + 14), fill=T['panel'], outline=T['border'], r=6)
            cv.text((mx, my), c, 22, T['code'], anchor='mm', mono=True, bold=True)
            edges(ch)

    def nodes(nd):
        X, Y = P(nd)
        hot = nd is cur
        nm = _names(S, nd)
        txt = ' '.join(nm) if nm else ('root' if nd is root else '')
        w = max(46, cv.tlen(txt, 22, mono=True) + 24) if txt else 46
        h = 40
        cv.rect((X - w / 2, Y - h / 2, X + w / 2, Y + h / 2), fill=T['yellow'] if hot else T['panel2'],
                outline=T['yellow'] if hot else T['border'], width=4 if hot else 2, r=12)
        if txt:
            cv.text((X, Y), txt, 22, T['bg'] if hot else (T['muted'] if nd is root else T['text']), anchor='mm', mono=True, bold=True)
        for _, ch in _kids(nd):
            nodes(ch)
    edges(root)
    nodes(root)
    cv.text((x1 - 20, y1 - 14), '节点里的词 = 该前缀下字典序最小的至多 3 个', 19, T['dim'], anchor='rb')


def _info(S):
    if 'res' in S:
        return '已得到的答案 `res` = ' + str(S['res'])
    P = _prod(S)
    return 'products = ' + str(P) if P else ''


def _cand_slot(S, B):
    nm = _names(S, S['now'])
    return '、'.join(nm)


CONFIG = dict(
    num=1268, title='搜索推荐系统', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='字典树 + 节点存最小 3 个词',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Trie(object):
    def __init__(self):
        self.end_flag = False
        self.next_dict = {}
        self.candidate = [None] * 3

class Solution(object):
    def suggestedProducts(self, products, searchWord):

        root = Trie()
        for index, word in enumerate(products):
            now = root
            for char in word:
                if char not in now.next_dict:
                    tmp = Trie()
                    now.next_dict[char] = tmp
                
                now = now.next_dict[char]
                if now.candidate[0] is None or word < products[now.candidate[0]]:
                    now.candidate[2] = now.candidate[1]
                    now.candidate[1] = now.candidate[0]
                    now.candidate[0] = index
                elif now.candidate[1] is None or word < products[now.candidate[1]]:
                    now.candidate[2] = now.candidate[1]
                    now.candidate[1] = index
                elif now.candidate[2] is None or word < products[now.candidate[2]]:
                    now.candidate[2] = index
            
            now.end_flag = True
        
        res = []
        now = root
        for char in searchWord:
            if char not in now.next_dict:
                while len(res) < len(searchWord):
                    res.append([])
                return res
            now = now.next_dict[char]
            res.append([])
            for index in range(3):
                if now.candidate[index] is not None:
                    res[-1].append(products[now.candidate[index]])
        
        return res
''',
    call='Solution().suggestedProducts(["bb", "bd", "ba", "bc"], "bbx")',
    expect=[['ba', 'bb', 'bc'], ['bb'], []],
    views=[
        dict(type='custom', draw=draw_trie, h=470),
        dict(type='text', h=70, size=28, fn=_info),
    ],
    watch=[('word', lambda S: S.get('word') if 'res' not in S else '—'), ('char', 'char'), ('index', 'index', 'orange'),
           ('候选', lambda S: _names(S, S['now']) if S.get('now') is not None else None, 'green')],
    captions={
        'root = Trie()': '建根节点：每个节点有子节点字典和 3 个槽（存字典序最小的三个词的下标）。然后把商品依次插进去',
        'for index, word in enumerate(products)': lambda S, B, ret: (
            '所有商品都插入完毕，开始搜索' if ('index' in B and B.index == S.index)
            else f'插入第 {S.index} 个商品 `{S.word}`'),
        'now = root': lambda S, B, ret: ('搜索：`now` 回到根节点，沿 `searchWord` 往下走' if 'res' in S
                                         else '`now` 从根出发'),
        'for char in word': lambda S, B, ret: (f'`{S.word}` 的字符都插完了' if _depth(S) == len(S.word)
                                               else f'下一个字符 `{S.char!r}`'),
        'if char not in now.next_dict': lambda S, B, ret: (
            (f'`{S.char!r}` 不是当前节点的子节点 → ' + ('==走不通，没有词以此开头==' if 'res' in S else '==要新建==')) if S.char not in S.now.next_dict
            else f'`{S.char!r}` 已有子节点，沿着走'),
        'now.next_dict[char] = tmp': '新建子节点，挂到 `{char!r}` 这条边上',
        'now = now.next_dict[char]': lambda S, B, ret: (f'走到 `{S.char!r}` 对应的节点（前缀 `{S.word[:_depth(S)] if "res" not in S else S.searchWord[:_depth(S)]}`）'),
        'if now.candidate[0] is None or word <': lambda S, B, ret: (
            (lambda c: f'`{S.word}` 比第 1 名{"（空位）" if c is None else " `" + S.products[c] + "`"}更小？'
             + ('==是==：坐上第 1 名（旧的往后挪）' if (c is None or S.word < S.products[c]) else '否，继续看第 2 名'))(S.now.candidate[0])),
        'now.candidate[0] = index': lambda S, B, ret: f'旧的名次依次后挪，`{S.word}` 坐上第 1 名：候选 = `{_names(S, S.now)}`',
        'elif now.candidate[1] is None': lambda S, B, ret: (
            (lambda c: f'`{S.word}` 比第 2 名{"（空位）" if c is None else " `" + S.products[c] + "`"}更小？'
             + ('==是==：坐上第 2 名，原第 2 名降为第 3 名' if (c is None or S.word < S.products[c]) else '否，继续看第 3 名'))(S.now.candidate[1])),
        'now.candidate[1] = index': lambda S, B, ret: f'原第 2 名后挪到第 3，`{S.word}` 成为第 2 名：候选 = `{_names(S, S.now)}`',
        'elif now.candidate[2] is None': lambda S, B, ret: (
            (lambda c: f'`{S.word}` 比第 3 名{"（空位）" if c is None else " `" + S.products[c] + "`"}更小？'
             + ('==是==：替换第 3 名（原来的第 3 名被挤出前三）' if (c is None or S.word < S.products[c]) else '否，不进前三，丢掉'))(S.now.candidate[2])),
        'now.candidate[2] = index': lambda S, B, ret: f'`{S.word}` 成为第 3 名（旧的第 3 名出局）：候选 = `{_names(S, S.now)}`',
        'res = []': '开始搜索：`res` 存每个前缀对应的推荐列表',
        'for char in searchWord': lambda S, B, ret: (f'`searchWord` 的字符走完了' if _depth(S) == len(S.searchWord)
                                                     else f'搜索前缀的下一个字符 `{S.char!r}`'),
        'while len(res) < len(searchWord)': lambda S, B, ret: (
            f'后面的前缀都不可能匹配：补空列表，`res` 长度 `{len(S.res)}`' + ('' if len(S.res) < len(S.searchWord) else '，补齐了')),
        'res.append([])': '`res` 末尾添一个空列表，装这个前缀的推荐',
                'if now.candidate[index] is not None': lambda S, B, ret: (
            f'第 {S.index + 1} 个槽有词 → 取出' if S.now.candidate[S.index] is not None else f'第 {S.index + 1} 个槽是空的，没有更多推荐'),
        'res[-1].append': '推荐 `{products[now.candidate[index]]}`，当前 `res[-1]` = `{res[-1]}`',
        'return res': '返回每个前缀的推荐：`{ret}`',
    },
    skip=['now.candidate[2] = now.candidate[1]', 'now.candidate[1] = now.candidate[0]', 'self.end_flag', 'self.next_dict = {}', 'self.candidate = [None] * 3', 'tmp = Trie()', 'now.end_flag = True', 'for index in range(3)'],
    max_steps=110,
    cards=dict(
        one_liner='节点里直接存好“字典序最小的三个词”，走到哪读到哪',
        complexity='建树 `O(总长度)`，查询 `O(|searchWord|)`',
        problem=['给 `products` 和 `searchWord`：每输入一个字符，推荐字典序最小、以当前前缀开头的至多 3 个商品',
                 '本视频：`["bb","bd","ba","bc"]`，搜索 `bbx`',
                 '结果：`[["ba","bb","bc"],["bb"],[]]`'],
        quote='按正常做法构造trie树，不过在构造时需要对每个节点额外储存一个信息，即到当前节点的所有单词中字典序最小的三个。……每走到一个节点，该节点所储存的三个单词就是当前前缀对应的答案。若无法继续行走，那么就直接使用空list填充答案。',
        quote_src='—— yiduobo 题解',
        idea=['插入每个词时，沿路每个节点都维护三个槽（存下标）',
              '新词比第 1/2/3 名小就插队，后面的名次依次往后挪',
              '搜索只是沿路读槽；走不通就把剩下的前缀全补 `[]`'],
        summary=['时间：建树 `O(L)`（L 为总长度，每节点常数次比较），查询 `O(m)`',
                 '空间：Trie 节点数，每个节点只存 3 个下标',
                 '==槽位挪动顺序==：先 `[2]=[1]`，再 `[1]=[0]`，最后写 `[0]`，否则会覆盖',
                 '走不通后要补足 `len(searchWord)` 个空列表，别漏']),
)
