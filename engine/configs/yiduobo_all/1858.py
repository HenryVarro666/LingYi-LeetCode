def _layout(root):
    pos, cnt = {}, [0]

    def go(n, d):
        ks = list(n.childs.values())
        if not ks:
            pos[id(n)] = (cnt[0], d)
            cnt[0] += 1
            return pos[id(n)]
        cols = [go(c, d + 1)[0] for c in ks]
        pos[id(n)] = ((cols[0] + cols[-1]) / 2, d)
        return pos[id(n)]

    go(root, 0)
    return pos, max(cnt[0], 1), max(d for _, d in pos.values())


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    words = S.get('words', [])
    order = sorted(words, key=len)
    w = S.get('w')
    cv.text((x0 + 18, y0 + 4), '按长度排序后依次处理（黄 = 当前单词）', 22, T['muted'], bold=True)
    cw = min(150, (x1 - x0 - 40) / max(1, len(order)))
    done_i = None
    if 'res' in S and w is not None:
        done_i = order.index(w)
    ok_set = S.get('_ok', set())
    for i, s in enumerate(order):
        X = x0 + 20 + i * cw
        cur = done_i is not None and i == done_i
        past = done_i is not None and i < done_i
        fill = T['yellow'] if cur else (T['panel2'])
        cv.rect((X + 3, y0 + 44, X + cw - 3, y0 + 90), fill=fill, r=10, outline=T['border'])
        cv.text((X + cw / 2, y0 + 67), s, 22, T['bg'] if cur else (T['text'] if not past else T['muted']), anchor='mm', bold=True, mono=True)
    root = S.get('root')
    if root is None:
        return
    pos, wd, dep = _layout(root)
    cc = min(120, (x1 - x0 - 60) / wd)
    rh = min(100, (y1 - y0 - 230) / max(dep, 1))
    sx = x0 + 30 + ((x1 - x0 - 60) - cc * wd) / 2 + cc / 2
    sy = y0 + 170
    P = {k: (sx + c * cc, sy + d * rh) for k, (c, d) in pos.items()}
    now = S.get('now')
    lab = {}
    st = [root]
    while st:
        n = st.pop()
        for k, c in n.childs.items():
            a, b = P[id(n)], P[id(c)]
            cv.line([(a[0], a[1] + 24), (b[0], b[1] - 24)], T['border'], 3)
            lab[id(c)] = k
            st.append(c)
    cv.text((x0 + 18, y0 + 118), 'trie：只存「每个前缀都是单词」的字符串', 22, T['muted'], bold=True)
    st = [root]
    while st:
        n = st.pop()
        X, Y = P[id(n)]
        hot = n is now
        cv.rect((X - 26, Y - 24, X + 26, Y + 24), fill=T['panel2'], r=12, outline=T['blue'] if hot else T['border'], width=6 if hot else 2)
        cv.text((X, Y), lab.get(id(n), '根'), 26, T['yellow'] if n is not root else T['text'], anchor='mm', bold=True, mono=True)
        st.extend(n.childs.values())
    if now is not None:
        X, Y = P[id(now)]
        cv.text((X + 30, Y - 4), 'now', 20, T['blue'], anchor='lm', bold=True)


def _floop(S, B, r):
    d, n = 0, S.root
    while n is not S.now and d < len(S.w):
        n = n.childs[S.w[d]]
        d += 1
    if d > S.index:
        return f'`{S.w}` 除最后一个字母外的前缀都检查过了'
    return f'检查第 `{S.index}` 个字符 `{S.w[S.index]}`'


CONFIG = dict(
    num=1858, title='包含所有前缀的最长单词', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='按长度排序 + trie',
    tags=['灵神题单'],
    code='''
class TreeNode(object):

    def __init__(self):
        self.childs = {}

class Solution(object):
    def longestWord(self, words):

        res = ''
        root = TreeNode()
        for w in sorted(words, key=lambda d:len(d)):
            now = root
            n = len(w)
            flag = True
            for index in range(n - 1):
                if w[index] not in now.childs:
                    flag = False
                    break
                
                now = now.childs[w[index]]
            
            if flag:
                tmp = TreeNode()
                now.childs[w[-1]] = tmp
                if len(w) > len(res) or (len(w) == len(res) and w < res):
                    res = w
        
        return res
''',
    call='Solution().longestWord(["a","banana","app","appl","ap","apply","apple"])',
    expect='apple',
    views=[
        dict(type='text', fn=lambda S: (f"当前单词 `{S['w']}`，要检查的前缀：`{S['w'][:-1] or '（空）'}`" + (f"，已走到第 `{S['index']}` 位" if 'index' in S and 'flag' in S else '')) if 'w' in S else '', size=26, h=60),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=['w', 'flag', ('res', 'res', 'green')],
    skip=['self.childs = {}', 'n = len(w)', 'now = root'],
    captions={
        'root = TreeNode()': '建一棵空 trie：只存「所有前缀都合法」的单词',
        "res = ''": '`res` 保存当前最优答案，初始为空串',
        'for w in sorted': lambda S, B, r: ('所有单词都处理完了' if B.get('w') == S.w else f'短的先处理，这样 `{S.w}` 的前缀一定已经判断过了'),
        'flag = True': '先假设 `{w}` 的前缀都合法',
        'for index in range': _floop,
        'if w[index] not in now.childs': lambda S, B, r: (f'`{S.w[S.index]}` 不在 trie 里 → 前缀 `{S.w[:S.index + 1]}` 不是单词，`{S.w}` ==不合法==' if S.w[S.index] not in S.now.childs else f'`{S.w[S.index]}` 在 trie 里，前缀 `{S.w[:S.index + 1]}` 合法'),
        'flag = False': '标记不合法，不再往下查',
        'break': '跳出，这个单词丢弃',
        'now = now.childs[w[index]]': '`now` 沿 `{w[index]}` 往下走一格',
        'if flag': lambda S, B, r: (f'`{S.w}` 的所有前缀都在 → 可以加入' if S.flag else f'`{S.w}` 被拒绝，不加入 trie'),
        'tmp = TreeNode()': '新建节点，代表 `{w}` 本身',
        'now.childs[w[-1]] = tmp': '把最后一个字母 `{w[-1]}` 挂上去：`{w}` 现在也成了合法前缀',
        'if len(w) > len(res)': lambda S, B, r: (f'`{S.w}` 比 `{B.res or "（空）"}` 更长，或同长且字典序更小 → 更新答案' if len(S.w) > len(B.res) or (len(S.w) == len(B.res) and S.w < B.res) else f'`{S.w}` 不比当前答案 `{S.res}` 更优，保持不变'),
        'res = w': '答案更新为 `{res}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='短的先来：前缀一定先于它自己被判断过',
        complexity='时间 `O(L + n log n)`，空间 `O(L)`（L = 总字符数）',
        problem=['找最长的单词，使它的==每个前缀==也都在 `words` 里；长度相同取字典序最小，没有则返回空串',
                 '示例：`["a","banana","app","appl","ap","apply","apple"]` → `"apple"`'],
        quote='将所有单词按长度从小到大排序，然后一趟遍历。对于当前遍历到的单词w，首先检测w除了最后一个字母外的前缀是否在之前的遍历过程中出现过。',
        quote_src='—— yiduobo 题解原文',
        idea=['trie 里只放「所有前缀都合法」的单词',
              '检查 `w[:-1]` 能否在 trie 里走通；能走通就把 `w` 的最后一个字母也挂上去',
              '每个合法的 `w` 都拿来更新答案：更长，或同长且字典序更小'],
        summary=['时间 `O(L + n log n)`，空间 `O(L)`',
                 '易错：同长度要取字典序最小，所以用 `w < res`',
                 '易错：必须先排序，否则前缀可能还没被加入 trie',
                 '对比灵神：先建完整字典树再 DFS；yiduobo 排序后边查边建',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行'],
    ),
)
