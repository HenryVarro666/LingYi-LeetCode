def _sys(S):
    if S.get('self.root') is not None and S.get('self.p') is not None:
        return S
    return None


def _lay(node, depth, pos, out):
    kids = list(node.childs.items())
    if not kids:
        x = pos[0]
        pos[0] += 1
        out.append((node, depth, x, []))
        return x
    xs = [_lay(c, depth + 1, pos, out) for k, c in kids]
    x = (xs[0] + xs[-1]) / 2
    out.append((node, depth, x, [(c, k) for k, c in kids]))
    return x


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '字典树（圆 = 节点；绿数字 = 被搜索次数 weight；下方 = 该前缀的 top3）', 22, T['muted'], bold=True)
    so = _sys(S)
    if so is None:
        return
    out = []
    pos = [0]
    _lay(so['self.root'], 0, pos, out)
    maxd = max(o[1] for o in out)
    cols = max(pos[0], 1)
    gx = min(180, (x1 - x0 - 100) / cols)
    gy = min(120, (y1 - y0 - 140) / max(maxd, 1))
    P = {}
    for node, d, x, kids in out:
        P[id(node)] = (x0 + 50 + (x1 - x0 - 100 - gx * (cols - 1)) / 2 + x * gx, y0 + 70 + d * gy)
    inner = S.get('_inner', {})
    cur_p = so['self.p']
    for node, d, x, kids in out:
        a = P[id(node)]
        for c, k in kids:
            b = P[id(c)]
            cv.line([(a[0], a[1] + 22), (b[0], b[1] - 22)], T['muted'], 2)
    for node, d, x, kids in out:
        X, Y = P[id(node)]
        ring = None
        if node is inner.get('now'):
            ring = T['yellow']
        elif node is cur_p:
            ring = T['blue']
        cv.rect((X - 22, Y - 22, X + 22, Y + 22), fill=T['panel2'], outline=ring or T['border'], width=5 if ring else 2, r=22)
        lab = 'root' if d == 0 else node.s[-1]
        cv.text((X, Y), lab, 18 if d == 0 else 26, T['text'], anchor='mm', bold=True, mono=True)
        if node.weight:
            cv.text((X + 28, Y - 22), node.weight, 22, T['green'], anchor='lm', bold=True)
        tp = [t.s for t in node.top if t is not None]
        if tp:
            if kids:
                cv.text((X + 28, Y + 6), ','.join(tp), 15, T['cyan'], anchor='lm', mono=True)
            else:
                cv.text((X, Y + 28), ','.join(tp), 15, T['cyan'], anchor='mt', mono=True)
    cv.text((x0 + 18, y1 - 28), '黄环 = update 正在处理的节点 now，蓝环 = 当前输入走到的节点 self.p', 18, T['dim'])


def _top(S):
    so = _sys(S)
    return '' if so is None else so['self.p'].s


CONFIG = dict(
    num=642, title='设计搜索自动补全系统', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='字典树 + 节点缓存 top3',
    tags=['字典树', '设计'],
    code='''
class TreeNode(object):

    def __init__(self, s, fa):
        self.s = s
        self.childs = {}
        self.top = [None, None, None]
        self.fa = fa
        self.weight = 0

class AutocompleteSystem(object):

    def __init__(self, sentences, times):
        self.root = TreeNode('', None)
        self.p = self.root
        for s, t in zip(sentences, times):
            now = self.root
            for char in s:
                if char not in now.childs:
                    tmp = TreeNode(now.s + char, now)
                    now.childs[char] = tmp
                now = now.childs[char]
            
            now.weight += t
            self.update(now)

    def update(self, now):
        p = now
        while now != None:
            if now.top[0] == p:
                pass
            elif now.top[1] == p:
                if now.top[0].weight < p.weight or (now.top[0].weight == p.weight and now.top[0].s > p.s):
                    now.top[0], now.top[1] = now.top[1], now.top[0]
            elif now.top[2] == p:
                if now.top[0].weight < p.weight or (now.top[0].weight == p.weight and now.top[0].s > p.s):
                    now.top[0], now.top[1], now.top[2] = now.top[2], now.top[0], now.top[1]
                elif now.top[1].weight < p.weight or (now.top[1].weight == p.weight and now.top[1].s > p.s):
                    now.top[1], now.top[2] = now.top[2], now.top[1]
            elif now.top[0] is None or now.top[0].weight < p.weight or (now.top[0].weight == p.weight and now.top[0].s > p.s):
                now.top[0], now.top[1], now.top[2] = p, now.top[0], now.top[1]
            elif now.top[1] is None or now.top[1].weight < p.weight or (now.top[1].weight == p.weight and now.top[1].s > p.s):
                now.top[1], now.top[2] = p, now.top[1]
            elif now.top[2] is None or now.top[2].weight < p.weight or (now.top[2].weight == p.weight and now.top[2].s > p.s):
                now.top[2] = p
            else:
                break
            
            now = now.fa
            
    def input(self, c):
        if c == '#':
            self.p.weight += 1
            self.update(self.p)
            self.p = self.root
            return []
        else:
            if c not in self.p.childs:
                tmp = TreeNode(self.p.s + c, self.p)
                self.p.childs[c] = tmp
            self.p = self.p.childs[c]

            res = []
            for node in self.p.top:
                if node is not None:
                    res.append(node.s)
            
            return res
''',
    call="""sys_ = AutocompleteSystem(['ab', 'ac', 'ad', 'ae'], [4, 3, 2, 2])
outs = []
outs.append(sys_.input('a'))
outs.append(sys_.input('e'))
outs.append(sys_.input('#'))
outs.append(sys_.input('a'))
outs""",
    expect=[['ab', 'ac', 'ad'], ['ae'], [], ['ab', 'ac', 'ae']],
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', fn=lambda S: f"当前输入前缀：`{_top(S)}`" if _sys(S) is not None else '', h=40),
    ],
    watch=[('c', 'c', 'blue'), ('p.s', lambda S: S['p'].s if hasattr(S.get('p'), 's') else '', 'pink'), ('now.s', lambda S: S['now'].s if hasattr(S.get('now'), 's') else '', 'yellow')],
    skip=['self.s = s', 'self.childs = {}', 'self.fa = fa', 'self.weight = 0', 'self.top = [', 'pass', 'res = []',
          'now = self.root', 'p = now', 'for char in s', 'if char not in now.childs', 'if now.top[0] == p',
          'elif now.top[1] == p', 'elif now.top[2] == p', 'elif now.top[0] is None', 'elif now.top[1] is None',
          'elif now.top[2] is None', 'now = now.fa', 'if c not in self.p.childs', 'if node is not None', 'for node in self.p.top', 'else:', 'if c == '],
    max_steps=110,
    captions={
        13: '建根节点：前缀 `""`，没有父亲（`fa = None`）',
        14: '`self.p` 记录输入时走到哪个节点，初始在根',
        'for s, t in zip': '逐句建树：句子 `{s}`，次数 `{t}`',
        'tmp = TreeNode(now.s + char, now)': '`{char}` 这条边还没有 → 新建节点，前缀 `{now.s + char}`，记下父亲 `fa`',
        20: '把新节点挂到 `{now.s!r}` 的孩子 `{char}` 上',
        'now = now.childs[char]': '走到前缀 `{now.s}` 的节点',
        'now.weight += t': '句子末尾节点：次数 `+= {t}` → ==`{now.weight}`==',
        'self.update(now)': '自底向上更新：这个句子要不要进祖先们的 top3？',
        'while now != None': lambda S, B, r: ('沿 `fa` 往上，当前节点前缀 `' + repr(S.now.s) + '`') if S.now is not None else '到根的上面了 → 更新结束',
        33: '句子在 `top[1]` 且比 `top[0]` 更优（次数大，或次数同且字典序小）→ ==两者交换==',
        36: '句子在 `top[2]` 且比 `top[0]` 更优 → ==升到第一，其余后移==',
        38: '句子在 `top[2]` 且比 `top[1]` 更优 → 两者交换',
        40: '句子不在 top3，但比 `top[0]` 更优（或 top[0] 空）→ ==插到最前，其余后移==',
        42: '不如 `top[0]`，但比 `top[1]` 更优（或空）→ 插到第二位',
        44: '只比 `top[2]` 更优（或空）→ 顶掉第三位：`top[2] = {p.s}`',
        46: '连 `top[2]` 都排不进 → ==更靠上的祖先也排不进，直接 break，不用再往上==',
        'now = now.fa': '去父亲节点，继续更新它的 top',
        'self.p.weight += 1': '`#`：当前句子 `{self.p.s}` 被搜索一次 → weight = ==`{self.p.weight}`==',
        'self.update(self.p)': '用新次数更新它所有祖先的 top3',
        'self.p = self.root': lambda S, B, r: '回到根，等待下一个句子' if S._line > 20 else '`self.p` 记录输入时走到哪个节点，初始在根',
        'return []': '`#` 不返回补全 → `[]`',
        'if c not in self.p.childs': '输入 `{c}`：`{self.p.s!r}` 下有没有这个孩子？没有就新建（次数为 0，进不了 top）',
        'self.p = self.p.childs[c]': '`self.p` 前进到前缀 `{self.p.s}`',
        'res.append(node.s)': '`top` 里存的是节点：取出 `{node.s}`（次数 {node.weight}）',
        'return res': '补全结果 ==`{res}`==，==直接读 top，不用遍历子树==',
    },
    cards=dict(
        one_liner='字典树的每个节点缓存「以它为前缀」的 top3 句子',
        complexity='输入一个字符 `O(1)`（读 top），更新 `O(句长)`',
        problem=['设计搜索补全系统：`input(c)` 输入一个字符，返回以当前前缀开头、搜索次数最高的至多 3 个句子',
                 '次数相同时==字典序小的在前==；输入 `#` 表示句子结束，计入历史并返回 `[]`',
                 '本视频：`[ab, ac, ad, ae]`，次数 `[4,3,2,2]`，依次输入 `a e # a`'],
        quote='对于trie树中的节点，除了最常规的哈希表childs用来记录孩子节点外，还需要weight、s、fa、top：top用来记录当前节点为前缀的被搜索次数最多的三个字符串对应的节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['`weight` 次数，`s` 前缀串，`fa` 父亲，`top` 前三名节点',
              '`#` 时 weight +1，再用 `fa` ==自底向上== 更新每个祖先的 top3',
              '好处：当前句子排不进某祖先的前三，==更往上的祖先也排不进==，直接 break'],
        summary=['输入字符：走一步字典树 + 读 `top`，`O(1)`；`#`：自底向上更新，`O(句长)`',
                 '更新要分情况：已在 top 内（只需换位）/ 不在 top 内（插入并挤掉末位）',
                 '次数相同比较 `s` 的字典序：==字典序小的更靠前==',
                 '`self.p` 走过程中新建的节点 weight 为 0，不会进 top',
                 '原文为 Python 2 风格，本题代码无需改动，可直接用 Python 3 运行'],
    ),
)
