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
                if not t:
                    edges(ch)
                    continue
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


def _dups(S):
    td = S.get('tree_dict') or {}
    return [n for v in td.values() if len(v) > 1 for n in v]


_draw = make_trie_draw(
    root_of=lambda S: S.get('root'),
    kids=lambda nd: list(nd.childs.items()),
    elabel=lambda k: k,
    ntext=lambda S, nd: '',
    nfill=lambda S, nd, T: T['red'] if any(nd is z for z in _dups(S)) else None,
    hot=lambda S: None if 19 < S.get('_line', 0) < 30 else (S.get('_inner') or {}).get('now'),
    head='文件夹 trie：边 = 文件夹名（黄圈 = 当前节点，红色 = 与别的子树重复）',
    legend='红色 = 在 remove_set 里，会被删除',
    R=17,
)


def _tdfmt(k, v):
    return f'{k or "∅"} → ×{len(v)}' + ('（重复）' if len(v) > 1 else '')


def _qfmt(x):
    return '/'.join(x[1]) or 'root'


CONFIG = dict(
    num=1948, title='删除系统中的重复文件夹', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='trie + 子树字符串 + BFS 收集',
    tags=['难度分 2534'],
    code='''
class Trie(object):

    def __init__(self):
        self.childs = {}

class Solution(object):
    def deleteDuplicateFolder(self, paths):

        root = Trie()
        for path in paths:
            now = root
            for val in path:
                if val not in now.childs:
                    now.childs[val] = Trie()
                now = now.childs[val]

        tree_dict = {}
        self.res = []
        self.dfs(root, tree_dict)
        remove_set = set()
        for key in tree_dict:
            if len(tree_dict[key]) > 1:
                for node in tree_dict[key]:
                    remove_set.add(node)
        
        q = [[root, []]]
        l = 0
        r = 1
        res = []
        while l < r:
            now, path = q[l]
            l += 1
            for child, next in now.childs.items():
                if next not in remove_set:
                    tmp = path[:]
                    tmp.append(child)
                    q.append([next, tmp])
                    r += 1
                    res.append(tmp)
        
        return res

    def dfs(self, now, tree_dict):
        tree_key = {}
        for child in now.childs:
            tree_key[child] = self.dfs(now.childs[child], tree_dict)

        if tree_key != {}:
            key_str = '(' + ''.join([tree_key[key] + key for key in sorted(tree_key.keys())]) + ')'
            if key_str not in tree_dict:
                tree_dict[key_str] = []
            tree_dict[key_str].append(now)
            return key_str

        return ''
''',
    call='Solution().deleteDuplicateFolder([["a"], ["c"], ["d"], ["a", "b"], ["c", "b"], ["d", "a"]])',
    expect=[['d'], ['d', 'a']],
    skip=['self.childs = {}', 'now = root', 'for val in path', 'if val not in now.childs', 'now.childs[val] = Trie()',
          'now = now.childs[val]', 'tree_dict = {}', 'self.res = []', 'tree_key = {}', 'res = []', 'l = 0', 'r = 1', 'remove_set = set()',
          'for child in now.childs:', 'tree_dict[key_str] = []', "return ''", 'for node in tree_dict[key]', 'tmp = path[:]', 'tmp.append(child)', 'q.append(', 'r += 1', 'l += 1'],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='map', var='tree_dict', label='tree_dict：子树字符串 → 有这个字符串的节点', fmt=_tdfmt, font=21, h=110),
        dict(type='queue', var='q', label='BFS 队列 q（元素 = 路径）', fmt=_qfmt, h=100),
        dict(type='calls', h=130),
    ],
    watch=[('key_str', lambda S: (S.get('_inner') or {}).get('key_str'), 'cyan'),
           ('remove_set', lambda S: len(S['remove_set']) if 'remove_set' in S else None, 'red'),
           ('path', lambda S: (S.get('_inner') or {}).get('path') if S.get('_line', 0) >= 30 else None, 'yellow'), ('res', lambda S: S.get('res') if 'remove_set' in S else None, 'green')],
    captions={
        'root = Trie()': '用 trie 组织文件夹：边是文件夹名，儿子放在 `childs` 字典里',
        'for path in paths': lambda S, B, r: ('trie 建好了：`a`、`c` 下面各有 `b`，`d` 下面是 `a`' if 'path' in B and B['path'] == S['path'] else f"把路径 `{S['path']}` 插进 trie"),
        'self.dfs(root, tree_dict)': '自底向上 DFS：每个节点用==排好序的儿子字符串==拼出自己的表示 `key_str`',
        'tree_key[child] = self.dfs': '先递归算儿子 `{child}` 的表示（叶子是空串）',
        'if tree_key != {}': lambda S, B, r: ('有儿子：要生成 `key_str`，并记进 `tree_dict`' if S.tree_key else '叶子（没有儿子）：不记录，返回空串'),
        'key_str = ': '`key_str` = `(` + 各儿子（表示 + 名字，按名字排序）+ `)` = ==`{key_str}`==',
        'tree_dict[key_str].append(now)': lambda S, B, r: f"`tree_dict[{S.key_str!r}]` 里现在有 `{len(S.tree_dict[S.key_str])}` 个节点" + ('：==出现第 2 次，重复了==' if len(S.tree_dict[S.key_str]) > 1 else '：第一次出现'),
        'return key_str': '把 `{key_str!r}` 返回给父节点',
        'for key in tree_dict': lambda S, B, r: ('所有子树字符串都检查完了，`remove_set` 里是要删的节点' if 'key' in B and B['key'] == S['key'] else '检查每个子树字符串：出现 ≥ 2 次的都要删'),
        'if len(tree_dict[key]) > 1': lambda S, B, r: (f"`{S.key!r}` 对应 `{len(S.tree_dict[S.key])}` 个节点 → ==重复==，全部加入 `remove_set`" if len(S.tree_dict[S.key]) > 1 else f"`{S.key!r}` 只有 1 个节点 → 保留"),
        'remove_set.add(node)': '节点加入 `remove_set`（共 `{len(remove_set)}` 个）',
        'q = [[root, []]]': '再从根开始 BFS：队列里放 `[节点, 路径]`',
        'now, path = q[l]': '取出队头：路径 `{path}`',
        'for child, next in now.childs.items()': lambda S, B, r: ('这个节点的儿子都看完了' if 'child' in B and B['child'] == S['child'] else f"看儿子 `{S['child']}`"),
        'if next not in remove_set': lambda S, B, r: (f"`{S.child}` 不在 `remove_set` → 保留，加入答案" if S.next not in S.remove_set else f"`{S.child}` 在 `remove_set` 里 → ==整棵子树跳过==，不入队"),
        'res.append(tmp)': '路径 `{tmp}` 入答案，节点入队 → `res = {res}`',
        'return res': '剩余路径 `{res}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='把每棵子树变成字符串，字符串相同就是重复的文件夹',
        complexity='时间 `O(L·log)`（子树字符串拼接 + 排序），空间 `O(L)`',
        problem=['`paths` 给出所有文件夹的绝对路径；==子文件夹集合非空且结构相同==的文件夹互为重复',
                 '把重复文件夹及其子文件夹一次性全部删除，返回剩下的路径',
                 '本视频（示例 1）：`a`、`c` 都含空文件夹 `b` → 删除；剩 `[["d"],["d","a"]]`'],
        quote='需要注意的是，本题是一颗多叉树，而且树中节点值是字符串，因此在构造子树表示的时候需要按一定的顺序将子树的值组织起来。……最后从根节点开始进行bfs。对于当前节点，遍历其孩子节点，若其已经被标记过，那么就跳过该节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['文件夹用 trie 组织 → 问题变成「多叉树里找重复子树」（类比 652 二叉树版本）',
              'DFS 返回子树的字符串：儿子名字排序后，拼接 `儿子表示 + 儿子名`，外面再包括号',
              '`tree_dict` 把字符串相同的节点聚在一起，超过 1 个的都进 `remove_set`',
              '最后 BFS 从根收集路径，遇到 `remove_set` 里的节点整棵跳过'],
        summary=['叶子返回 `\'\'` 且不进 `tree_dict`：空文件夹不算重复（题目要求子文件夹集合非空）',
                 '儿子名要 `sorted`：保证子树结构相同、顺序不同也得到同一个字符串',
                 '字符串里儿子名放在其表示之后（`tree_key[key] + key`），结构一样的子树字符串才一样',
                 '原文已是 Python 3 可运行的写法，未做修改；对比灵神：灵神 DFS 用括号表达式 + 回溯收集，这里用 BFS'],
    ),
)
