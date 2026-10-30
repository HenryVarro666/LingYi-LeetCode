TARGET = 'abcab'


def _kids(node):
    return [c for c in (getattr(node, 'childs', None) or []) if c is not None and c.prefix_length == node.prefix_length + 1]


def _nodes(root):
    """(node, parent, path string) 先序"""
    out = []

    def go(n, par, path):
        out.append((n, par, path))
        for c in _kids(n):
            go(c, n, path + c.char)
    go(root, None, '')
    return out


def _path(S, node):
    root = S.get('root')
    if root is None or node is None:
        return ''
    for n, _, p in _nodes(root):
        if n is node:
            return p or '∅'
    return ''


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    root = S.get('root')
    cv.text((x0 + 18, y0 + 4), 'Trie 图（黄 = now；橙色弧线 = fail 指针）', 24, T['muted'], bold=True)
    if root is None:
        return
    ns = _nodes(root)
    # 叶子序号布局
    xs = {}
    cnt = [0]

    def lay(n):
        ks = _kids(n)
        if not ks:
            xs[id(n)] = cnt[0]
            cnt[0] += 1
        else:
            for k in ks:
                lay(k)
            xs[id(n)] = (xs[id(ks[0])] + xs[id(ks[-1])]) / 2
    lay(root)
    nl = max(1, cnt[0])
    maxd = max(n.prefix_length for n, _, _ in ns)
    gx = min(150, (x1 - x0 - 120) / max(1, nl))
    sx = x0 + (x1 - x0) / 2 - gx * (nl - 1) / 2
    top, gy = y0 + 150, min(110, (y1 - y0 - 200) / max(1, maxd))
    pos = {id(n): (sx + xs[id(n)] * gx, top + n.prefix_length * gy) for n, _, _ in ns}
    now = S.get('now')
    if S.get('_line') in (20, 21, 22):
        now = None
    R = 27
    for n, par, path in ns:
        if par is not None:
            cv.line([pos[id(par)], pos[id(n)]], T['border'], 3)
    for n, par, path in ns:
        if n is not root and getattr(n, 'fail', None) is not None and id(n.fail) in pos:
            a, b = pos[id(n)], pos[id(n.fail)]
            if n.fail is root:
                cv.arc_arrow((a[0] - 8, a[1] - R), (b[0] + 8, b[1] + R * 0.2), 70 + 12 * n.prefix_length, T['orange'], 3)
            else:
                cv.arc_arrow((a[0] - 8, a[1] - R), (b[0] + 4, b[1] - R), 55, T['orange'], 3)
    for n, par, path in ns:
        X, Y = pos[id(n)]
        hot = n is now
        cv.rect((X - R, Y - R, X + R, Y + R), fill=T['yellow'] if hot else T['panel2'], outline=T['border'], width=2, r=R)
        cv.text((X, Y), '∅' if n is root else n.char, 30, T['bg'] if hot else T['text'], anchor='mm', bold=True, mono=True)
        cv.text((X, Y + R + 6), n.prefix_length, 17, T['dim'], anchor='mt', mono=True)
    if isinstance(now, object) and hasattr(now, 'childs'):
        cv.text((x1 - 20, y0 + 6), f"now = “{_path(S, now)}”，匹配长度 {now.prefix_length}", 24, T['yellow'], anchor='ra', bold=True)


def _level(S):
    return ''


CONFIG = dict(
    num=3292, title='形成目标字符串需要的最少字符串数 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='Trie 图（AC 自动机）+ 单调的 f 数组',
    tags=['字符串', '难度分 2662'],
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
    call="Solution().minValidStrings(['ab', 'bca'], 'abcab')",
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=430),
        dict(type='string', var='target', label='target（蓝 = 当前读到的字符）', h=170,
             window=('index if f else None', 'index if f else None')),
        dict(type='array', var='f', label='f[i]：target 前 i 个字符最少用几段', h=170,
             color=lambda S, idx, v: 'green'),
    ],
    watch=[('index', 'index', 'blue'), 'asc'],
    captions={
        'root = Node': '建根节点（空串，深度 0），然后把每个单词插进 trie',
        'for w in words': lambda S, B, r: ('单词都插完了' if B.get('w') == S.w else f'插入单词 `{S.w}`'),
        'now.childs[asc] = Node': lambda S, B, r: f"“{_path(S, S.now)}” 下没有 `{S.char}` 这条边 → 新建节点 `{S.char}`，深度 {S.index + 1}",
        'q = [root]': '补 `fail`：从根开始 ==一层一层（BFS）== 处理',
        'head, tail = 0, 1': '`q[head:tail]` 是当前这一层的节点',
        'while head < tail': lambda S, B, r: (f'这一层是 `q[{S.head}:{S.tail}]`，共 {S.tail - S.head} 个节点' if S.head < S.tail else 'BFS 结束：所有节点都有 `fail`，缺失的边也补成了跳转边'),
        'for now in q': lambda S, B, r: ('这一层的节点都处理完了' if B.get('now') is not None and _path(B, B.get('now')) == _path(S, S.now) else
                                         f"处理节点 “{_path(S, S.now)}”：补它孩子的 `fail`；缺的边指向 `now.fail` 的同名孩子（失配时一步跳转）"),
        'head, tail = tail': '这一层处理完：新的 `fail`（橙色弧线）都建好了，下一层是 `q[{head}:{tail}]`',
        'f = [0]': '`f[i]`：拼出 target 前 i 个字符的最少段数；`f[0] = 0`。`f` 是不降的，所以每步只要 ==最长的匹配前缀==',
        'for index, char in enumerate(target)': lambda S, B, r: ('target 走完了' if B.get('index') == S.index and B.get('char') == S.char else f'读入第 {S.index + 1} 个字符 `{S.char}`'),
        45: lambda S, B, r: f"沿 `{S.char}` 走一步 → 节点 “{_path(S, S.now)}”：它是以当前字符结尾、==最长的单词前缀== 后缀（失配时已经自动沿 fail 跳转），长度 {S.now.prefix_length}",
        46: lambda S, B, r: ('回到根：没有任何单词前缀能接上这个字符 → 返回 `-1`' if S.now is S.root else '没回到根：匹配成功'),
        'f.append': '`f[{index + 1}] = f[{index + 1} − {now.prefix_length}] + 1` = =={f[-1]}==：最后一段取最长的 {now.prefix_length} 个字符，前面拼 `f[{index + 1 - now.prefix_length}]`',
        'return f[-1]': '`f[-1]` = =={f[-1]}==：最少需要的段数',
    },
    skip=[18, 'self.prefix_length', 'self.childs', 'self.fail', 'self.char', 'now = root', 'for index, char in enumerate(w)', 'asc = ord', 'if now.childs[asc] is None', 
          'for index, c in enumerate(now.childs)', 'if c is None', 26, 31, 'now.childs[index]', 'c.fail', 'q.append(c)', 'n = len(target)'],
    max_steps=100,
    cards=dict(
        one_liner='单词建 trie 图，target 在图上走一圈，每步取最长匹配前缀',
        complexity='时间 `O(L|Σ| + n)`，空间 `O(L|Σ| + n)`',
        problem=['用 `words` 里单词的前缀拼出 `target`，最少用几个前缀？拼不出返回 `-1`',
                 '`words` 总长最大 `10^5`，`target` 长 `5×10^4`',
                 '本视频：`words = [ab, bca]`，`target = abcab` → `3`（`a` + `bca` + `b`）'],
        quote='首先可以明确的一点是，对于i < j，必然有f[i] <= f[j]……问题到了这里就变成了找出最小的pre，满足target[pre : index]是words中某个单词的前缀。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]` 不降：拼 `i+1` 个字符不会比拼 `i` 个更省 → 最后一段取 ==最长== 的单词前缀',
              '「最长的以当前字符结尾的单词前缀」正是 trie 图（多字符串版 KMP）要回答的',
              '建 trie → BFS 补 `fail`（思路同 KMP 的 next）→ `target` 在图上走一圈，`now.prefix_length` 就是最长匹配'],
        summary=['时间 `O(L|Σ|+n)`，空间 `O(L|Σ|+n)`（`|Σ| = 26`）',
                 '`now == root` 说明这个字符完全无法匹配，直接返回 `-1`',
                 '`f[index + 1] = f[index + 1 - now.prefix_length] + 1`：`f` 以前缀个数为下标，所以要加 1',
                 '原文为 Python 2 风格，代码没有需要改动的地方',
                 '对比灵神：灵神主推 Z 函数 + 跳跃游戏，yiduobo 直接用 trie 图做 DP'],
    ),
)
