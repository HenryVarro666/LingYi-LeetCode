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


_draw = make_trie_draw(
    root_of=lambda S: S.get('root'),
    kids=lambda nd: list(nd.childs.items()),
    elabel=lambda k: f'{k[0]}{k[1]}',
    ntext=lambda S, nd: str(nd.weight) if nd.weight else '',
    nfill=lambda S, nd, T: T['green'] if nd.weight >= 2 else (T['blue'] if nd.weight else None),
    hot=lambda S: S.get('now'),
    head='字符对字典树：边 = (首字母, 尾字母) 字符对；节点里的数字 = 权重 weight',
    legend='绿色 = weight ≥ 2，说明有别的单词也走到这里',
)


def _key_txt(S):
    w = S.get('w')
    if not isinstance(w, str):
        return '把每个单词看成字符对序列 (w[0],w[-1]), (w[1],w[-2]), …'
    pairs = ' '.join(f'({w[k]},{w[-k - 1]})' for k in range(len(w)))
    return f'`{w!r}` 的字符对序列：==`{pairs}`=='


CONFIG = dict(
    num=3045, title='统计前后缀下标对 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='(首字符, 尾字符) 对合并前后缀的 trie',
    tags=['难度分 2328'],
    code='''
class Node():
    def __init__(self):
        self.childs = {}
        self.weight = 0

class Solution(object):
    def countPrefixSuffixPairs(self, words):

        root = Node()
        res = 0
        for w in words[::-1]:
            now = root
            for index in range(len(w)):
                key = (w[index], w[-index - 1])
                if key not in now.childs:
                    now.childs[key] = Node()
                now = now.childs[key]
                now.weight += 1
            
            res += now.weight - 1
        
        return res
''',
    call='Solution().countPrefixSuffixPairs(["ma", "mama", "pa"])',
    expect=1,
    skip=['self.childs = {}', 'self.weight = 0', 'for index in range(len(w))', 'now = now.childs[key]'],
    views=[
        dict(type='array', var='words', label='words（从后往前扫，蓝 = 当前 w）', h=150, cell=110,
             color=lambda S, i, v: 'blue' if S.get('w') == v else None),
        dict(type='text', fn=_key_txt, h=70),
        dict(type='custom', draw=_draw, h=380),
    ],
    watch=['w', 'index', 'key', ('weight', lambda S: S['now'].weight if 'now' in S else None, 'cyan'), ('res', 'res', 'green')],
    captions={
        'root = Node()': '一棵只有根的 trie；边不是单个字母，而是==字符对==',
        'res = 0': '`res` 累计答案',
        'for w in words[::-1]': lambda S, B, r: ('所有单词都处理完了' if 'w' in B and B['w'] == S['w'] else f"从后往前取单词 `w = {S['w']!r}`：它前面的单词（下标更小）还没插入树"),
        'now = root': '`now` 回到根，准备沿 `w` 的字符对往下走',
        'key = (w[index]': '字符对 `(w[{index}], w[-{index+1}])` = `{key}`：同时看==前缀第 {index+1} 个字母==和==后缀倒数第 {index+1} 个字母==',
        'if key not in now.childs': lambda S, B, r: (f"字符对 `{S.key}` 在 `now.childs` 里：前面处理过的单词（下标更大）有同样的开头对" if S.key in S.now.childs else f"字符对 `{S.key}` 不在 `now.childs` 里：这条路还没人走过，要新建"),
        'now.childs[key] = Node()': '新建节点，边是字符对 `{key}`',
        'now.weight += 1': '沿 `{key}` 往下一层；经过该节点的单词又多一个：`weight = {now.weight}`（包含 `w` 自己）',
        'res += now.weight - 1': '走完整个 `w`：终点 `weight = {now.weight}`，==减 1 去掉 `w` 自己==，其余都是以它为前后缀的更长单词 → `res = {res}`',
        'return res': '一共 `{res}` 对',
    },
    max_steps=70,
    cards=dict(
        one_liner='前缀和后缀合成「字符对」，一棵 trie 同时匹配两头',
        complexity='时间 `O(L)`，空间 `O(L)`，`L` 为所有单词长度之和',
        problem=['数出下标对 `i < j`，使 `words[i]` 既是 `words[j]` 的前缀又是后缀',
                 '单词总长可达 `5·10^5`，必须线性时间',
                 '本视频：`["ma","mama","pa"]` → `1`（只有 `ma`-`mama` 一对）'],
        quote='既然words[i]在前缀trie树和后缀trie树中匹配的长度相同，那么不妨将二者合并，即构造trie树以及进行匹配时，使用(words[0], words[-1])，(words[1], words[-2])，...这样的字符对来作为树中的节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['前缀 trie 与后缀 trie 各自匹配，再取交集会退化成 `O(n^2)`',
              '把第 `k` 个字符和倒数第 `k` 个字符并成一对：匹配成功就==前后缀同时匹配==，不用求交集',
              '从后往前插入：节点的 `weight` 数的是「以此为前缀对序列的更长单词」，终点 `weight - 1` 就是答案增量'],
        summary=['`words[::-1]`：只会遇到下标比当前大的单词，所以数到的 `j` 都满足 `i < j`',
                 '`weight` 包含单词自己，所以 `res += weight - 1`',
                 '字符对序列相同 ⟺ 前缀与后缀都匹配：`w` 的字符对序列是 `W` 的字符对序列的前缀时，`w` 就是 `W` 的前后缀',
                 '原文为 Python 2 风格的 `class Node()`，在 Python 3 下无需改动；对比灵神方法一：这里不用 Z 函数'],
    ),
)
