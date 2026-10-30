WORDS = ['ab', 'bc']
TARGET = 'abbc'


def _is_node(x):
    return hasattr(x, 'prefix_length') and hasattr(x, 'childs')


def _tree(root):
    """沿真正的 trie 边（深度 +1）收集节点，返回 [(node, depth, 前缀串, 父节点)]，按 DFS 顺序"""
    out = []

    def go(nd, depth, pre, par):
        out.append((nd, depth, pre, par))
        for i, c in enumerate(nd.childs):
            if _is_node(c) and c.prefix_length == depth + 1 and c is not nd:
                go(c, depth + 1, pre + chr(97 + i), nd)
    go(root, 0, '', None)
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'trie 图：实线 = trie 边，橙色箭头 = fail 指针，蓝 = now，粉 = 子节点 c', 22, T['muted'], bold=True)
    root = S.get('root')
    if root is None:
        return
    info = _tree(root)
    # 布局：深度 = 横向列，叶子 = 纵向槽位
    kids = {}
    for nd, d, pre, par in info:
        kids.setdefault(id(par), []).append(nd)
    slot = {}
    cnt = [0]

    def lay(nd):
        ch = [c for c in kids.get(id(nd), [])]
        if not ch:
            slot[id(nd)] = cnt[0]
            cnt[0] += 1
        else:
            for c in ch:
                lay(c)
            slot[id(nd)] = sum(slot[id(c)] for c in ch) / len(ch)
    lay(root)
    nleaf = max(1, cnt[0])
    maxd = max(d for _, d, _, _ in info)
    ty0, ty1 = y0 + 60, y0 + 280
    dx = min(240, (x1 - x0 - 200) / max(1, maxd))
    pos = {}
    for nd, d, pre, par in info:
        sy = slot[id(nd)]
        Y = (ty0 + ty1) / 2 if nleaf == 1 else ty0 + 30 + (ty1 - ty0 - 60) * sy / (nleaf - 1)
        pos[id(nd)] = (x0 + 100 + d * dx, Y)
    now, c = S.get('now'), S.get('c')
    R = 32
    # trie 边
    for nd, d, pre, par in info:
        if par is not None:
            (ax, ay), (bx, by) = pos[id(par)], pos[id(nd)]
            cv.arrow((ax + R, ay), (bx - R - 2, by), T['border'], 3, 10)
            cv.text(((ax + bx) / 2, (ay + by) / 2 - 22), nd.char, 26, T['muted'], anchor='mm', bold=True, mono=True)
    # fail 指针
    for nd, d, pre, par in info:
        f = nd.fail
        if f is not None and id(f) in pos:
            (ax, ay), (bx, by) = pos[id(nd)], pos[id(f)]
            if abs(ax - bx) < 1 and abs(ay - by) < 1:
                continue
            cv.arc_arrow((ax - 8, ay - R), (bx + 8, by - R), 36 + 14 * abs(d - f.prefix_length), T['orange'], 3)
    # 节点
    for nd, d, pre, par in info:
        X, Y = pos[id(nd)]
        hot_now = nd is now
        hot_c = nd is c
        fill = T['blue'] if hot_now else (T['pink'] if hot_c else T['panel2'])
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=fill, outline=T['border'], width=3)
        lab = 'root' if nd is root else pre
        cv.text((X, Y), lab, 22 if nd is root else 26, T['bg'] if (hot_now or hot_c) else T['text'], anchor='mm', bold=True, mono=True)
        cv.text((X, Y + R + 6), f'长度 {nd.prefix_length}', 17, T['dim'], anchor='mt')
    # 队列（BFS 阶段）
    q = S.get('q')
    if q is not None and 'f' not in S:
        qs = '  '.join('root' if n is root else _label(info, n) for n in q)
        cv.text((x0 + 18, y0 + 330), f'队列 q：{qs}', 24, T['cyan'], bold=True)
    # 匹配阶段：target 与 f 数组
    if 'f' in S:
        tg = S['target']
        n = len(tg)
        cell = 76
        sx = x0 + 20
        ys = y0 + 385
        cv.text((x0 + 18, ys - 34), 'target（蓝 = 当前字符）与 f：f[i] = 拼出前 i 个字符的最少个数', 22, T['muted'], bold=True)
        idx = S.get('index')
        busy = S['_line'] >= 29
        for i, ch in enumerate(tg):
            X = sx + i * cell
            cur = idx == i
            fill = T['blue'] if cur else (T['panel2'])
            cv.rect((X + 3, ys, X + cell - 3, ys + 56), fill=fill, r=8, outline=T['border'])
            cv.text((X + cell / 2, ys + 28), ch, 32, T['bg'] if cur else T['text'], anchor='mm', bold=True, mono=True)
            cv.text((X + cell / 2, ys + 62), i, 16, T['dim'], anchor='mt', mono=True)
        fy = ys + 115
        fl = S['f']
        for i in range(n + 1):
            X = sx + i * cell
            have = i < len(fl)
            cv.rect((X + 3, fy, X + cell - 3, fy + 56), fill=T['green'] if have and i == len(fl) - 1 else T['panel2'], r=8, outline=T['border'])
            cv.text((X + cell / 2, fy + 28), fl[i] if have else '?', 32, T['bg'] if (have and i == len(fl) - 1) else (T['text'] if have else T['dim']), anchor='mm', bold=True)
            cv.text((X + cell / 2, fy + 62), f'f[{i}]', 16, T['dim'], anchor='mt', mono=True)


def _label(info, nd):
    for n, d, pre, par in info:
        if n is nd:
            return pre or 'root'
    return '?'


def _nodename(S, nd):
    root = S['root']
    if nd is root:
        return 'root'
    for n, d, pre, par in _tree(root):
        if n is nd:
            return f"'{pre}'"
    return '?'


def _cap_ifroot(S, B, r):
    if 'f' in S:
        if S.now is S.root:
            return '`now` 回到了 ==root==：说明以这个字符结尾的任何后缀都不是单词前缀 → 无法拼出，返回 -1'
        return f'`now` 在节点 {_nodename(S, S.now)}，不是 root：以 `{S.char}` 结尾能匹配到长度 ==`{S.now.prefix_length}`== 的单词前缀'
    return None


def _cap_fail(S, B, r):
    if S.now is S.root:
        return f'第一层节点 {_nodename(S, S.c)} 的 `fail` 指向 root：失配后只能从头再来'
    return (f'`fail` = 沿父节点 {_nodename(S, S.now)} 的 `fail` 找到的 `{S.index_char}` 孩子：'
            f'{_nodename(S, S.c)} 的 `fail` → {_nodename(S, S.c.fail)}（保留尽量长的后缀）')


CONFIG = dict(
    num=3291, title='形成目标字符串需要的最少字符串数 I', difficulty='Medium', category='字符串',
    author='yiduobo', technique='trie 图（AC 自动机）+ 动态规划',
    tags=[],
    code='''
class Node(object):
    def __init__(self, prefix_length, char):
        self.prefix_length = prefix_length
        self.childs = [None] * 26
        self.fail = None
        self.char = char

class Solution(object):
    def minValidStrings(self, words, target):

        root = Node(0, None)
        for w in words:
            now = root
            for index, char in enumerate(w):
                asc = ord(char) - 97
                if now.childs[asc] is None:
                    now.childs[asc] = Node(index + 1, char)
                now = now.childs[asc]
        
        q = [root]
        head, tail = 0, 1
        while head < tail:
            for now in q[head : tail]:
                for index, c in enumerate(now.childs):
                    if c is None:
                        if now == root:
                            now.childs[index] = now
                        else:
                            now.childs[index] = now.fail.childs[index]
                    else:
                        if now == root:
                            c.fail = now
                        else:
                            c.fail = now.fail.childs[index]
                        q.append(c)

            head, tail = tail, len(q)
        
        
        n = len(target)
        f = [0]
        now = root
        for index, char in enumerate(target):
            asc = ord(char) - 97
            now = now.childs[asc]
            if now == root:
                return -1
            f.append(f[index + 1 - now.prefix_length] + 1)
        
        return f[-1]
''',
    call=f'Solution().minValidStrings({WORDS!r}, {TARGET!r})',
    expect=2,
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=['head', 'tail', ('index', 'index', 'yellow'), ('f', 'f', 'green')],
    skip=[3, 4, 5, 6, 13, 22, 35, 15, 18, 21, 24, 25, 26, 27, 29, 40, 42, 44],
    max_steps=95,
    captions={
        11: '先建根节点 `root`：空串，前缀长度 0；trie 的每个节点都记着「从根走到这里的前缀长度」',
        12: lambda S, B, r: ('所有单词都插完了' if S.w == B.get('w') else f'插入单词 `{S.w}`：每个单词都从 `root` 出发，`now` 指向走到的节点'),
        14: lambda S, B, r: ('这个单词的字母走完了' if S.index == B.get('index') else f'取单词的下一个字母 `{S.char}`'),
        16: lambda S, B, r: (f'`now` 还没有 `{S.char}` 这条边 → 需要新建节点' if S.now.childs[ord(S.char) - 97] is None else f'`now` 已经有 `{S.char}` 这条边 → 直接走过去'),
        17: '新建节点：前缀长度 `index + 1`，字符 `{char}`，挂在 `now` 下面；`now` 随后走到它',
        20: 'BFS 建 fail 指针：队列 `q` 从 `root` 开始，一层一层处理',
        22: lambda S, B, r: ('当前层非空，处理这一层' if S.head < S.tail else '队列处理完了，trie 图建好'),
        23: lambda S, B, r: ('这一层的节点处理完了' if 'root' in B and _nodename(S, S.now) == _nodename(B, B.get('now')) else
                             ('取出 ==root==，看它的 26 个孩子位：有孩子的设 `fail` 并入队；没孩子的补边指向 `fail` 的孩子'
                              if S.now is S.root else f'取出节点 {_nodename(S, S.now)}，同样处理它的孩子位')),
        31: lambda S, B, r: ('`now` 是 root：它的孩子失配了只能回到 root' if S.now is S.root else '`now` 不是 root：孩子的 `fail` 要沿 `now.fail` 去找'),
        32: lambda S, B, r: f'第一层节点 {_nodename(S, S.c)} 的 `fail` 指向 root：一旦失配就从头再来；随后入队',
        34: lambda S, B, r: (f'{_nodename(S, S.c)} 的 `fail` = `now.fail` 的 `{chr(97 + S.index)}` 孩子 = {_nodename(S, S.c.fail)}：'
                             f'保留以 {_nodename(S, S.now)} 结尾的最长后缀，并且能接上 `{chr(97 + S.index)}`；随后入队'),
        37: lambda S, B, r: f'这一层处理完：下一层是 `q[{S.head}:{S.tail}]`' + ('' if S.head < S.tail else '（空）'),
        41: '`f[i]`：拼出 `target` 前 `i` 个字符的最少个数，`f[0] = 0`；然后让 `target` 在 trie 图里从 `root` 走一圈',
        43: lambda S, B, r: (f'取 `target[{S.index}] = {S.char}`' if 'char' in S and S.index is not None and S.index < len(S.target) and S.f is not None and len(S.f) == S.index + 1 else '`target` 走完了'),
        45: lambda S, B, r: f'沿 `{S.char}` 这条边走到 {_nodename(S, S.now)}（失配的边已被补成指向 fail，不会越界）',
        46: _cap_ifroot,
        47: '走回 root：以这个字符结尾的任何后缀都不是单词前缀，拼不出来 → `-1`',
        48: lambda S, B, r: (f'最长匹配 `{S.now.prefix_length}`：`f[{S.index + 1}] = f[{S.index + 1} - {S.now.prefix_length}] + 1` = ==`{S.f[-1]}`==，'
                             f'即最后一块用 `{S.target[S.index + 1 - S.now.prefix_length:S.index + 1]}`'),
        50: '`f[-1]` 就是拼出整个 `target` 的最少个数：`{f[-1]}`',
    },
    cards=dict(
        one_liner='先建 trie 图，再让 target 走一圈：f[i+1] = f[i+1-当前匹配长度] + 1',
        complexity='时间 `O(26·L + n)`，空间 `O(26·L)`（`L` 是单词总长）',
        problem=['用 `words` 中字符串的==前缀==拼接 `target`，求最少用几个前缀，不能拼出返回 `-1`',
                 '示例：`words = ["abc","aaaaa","bcdef"]`，`target = "aabcdabc"` → `3`',
                 '本视频：`words = ["ab","bc"]`，`target = "abbc"` → `2`（`ab` + `bc`）'],
        quote='trie图……就是以当前节点形成的子串无法继续匹配目标串的子串时，可以尝试通过之前的匹配结果将目标串的匹配起始位置向后移动，同时将当前节点移动到可以匹配新的子串的位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]` = 拼出 `target` 前 `i` 个字符的最少个数，`f[0] = 0`',
              '对 `i < j` 有 `f[i] <= f[j]`，所以转移时 `pre` 越靠前越好 → 要找最长的单词前缀',
              '把 `words` 建成 trie 图，`fail` 指针像 KMP 的 next，失配时回退到最长可用后缀',
              '`target` 走一圈，当前节点的深度就是以该字符结尾的最长前缀长度'],
        summary=['时间 `O(26·L + n)`，`L` 是单词总长度；空间 `O(26·L)`',
                 '补全不存在的孩子边（指向 `fail` 的孩子），匹配时就不用循环回退',
                 '易错点：`f` 比下标多一位，所以是 `f[index + 1 - now.prefix_length] + 1`',
                 '`now` 走回 root 说明这个字符无法被任何前缀覆盖 → `-1`',
                 '代码本身是 Python 3 可直接运行的写法，无需修改'],
    ),
)
