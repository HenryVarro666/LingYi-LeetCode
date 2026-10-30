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


def _cur(S):
    inner = S.get('_inner') or {}
    return inner.get('node')


_draw = make_trie_draw(
    root_of=lambda S: S.get('root'),
    kids=lambda nd: list(nd.son.items()),
    elabel=lambda k: '',
    ntext=lambda S, nd: nd.name,
    nfill=lambda S, nd, T: T['red'] if nd.deleted else None,
    hot=lambda S: _cur(S),
    head='文件系统字典树：节点 = 文件夹（黄圈 = 正在处理，红色 = 已标记删除）',
    legend='红色 = 待删除',
    R=22,
)


def _expr_txt(S):
    inner = S.get('_inner') or {}
    nd, e = inner.get('node'), inner.get('sub_tree_expr')
    if nd is not None and e is not None:
        return f'`{nd.name}` 的子树表达式（不含自己名字）：=={e}=='
    if nd is not None and not nd.son:
        return f'`{nd.name}` 是叶子：表达式就是名字，不参与比较'
    return '括号表达式 = 儿子表达式外套括号，排序后拼接'


CONFIG = dict(
    num=1948, title='删除系统中的重复文件夹', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='字典树 + 子树括号表达式去重',
    tags=['难度分 2534'],
    code='''
class TrieNode:
    __slots__ = 'son', 'name', 'deleted'

    def __init__(self):
        self.son = {}
        self.name = ''  # 文件夹名称
        self.deleted = False  # 删除标记

class Solution:
    def deleteDuplicateFolder(self, paths: List[List[str]]) -> List[List[str]]:
        root = TrieNode()
        for path in paths:
            # 把 path 插到字典树中，见 208. 实现 Trie
            cur = root
            for s in path:
                if s not in cur.son:
                    cur.son[s] = TrieNode()
                cur = cur.son[s]
                cur.name = s

        expr_to_node = {}  # 子树括号表达式 -> 子树根节点

        def gen_expr(node: TrieNode) -> str:
            if not node.son:  # 叶子
                return node.name  # 表达式就是文件夹名

            # 每个子树的表达式外面套一层括号
            expr = sorted('(' + gen_expr(son) + ')' for son in node.son.values())
            sub_tree_expr = ''.join(expr)  # 按字典序拼接所有子树的表达式
            if sub_tree_expr in expr_to_node:  # 哈希表中有 sub_tree_expr，说明有重复的文件夹
                expr_to_node[sub_tree_expr].deleted = True  # 哈希表中记录的节点标记为删除
                node.deleted = True  # 当前节点标记为删除
            else:
                expr_to_node[sub_tree_expr] = node

            return node.name + sub_tree_expr

        for son in root.son.values():
            gen_expr(son)

        ans = []
        path = []

        # 在字典树上回溯，仅访问未被删除的节点，并将路径记录到答案中
        # 类似 257. 二叉树的所有路径
        def dfs(node: TrieNode) -> None:
            if node.deleted:
                return
            path.append(node.name)
            ans.append(path.copy())  # path[:]
            for child in node.son.values():
                dfs(child)
            path.pop()  # 恢复现场

        for son in root.son.values():
            dfs(son)

        return ans
''',
    call='Solution().deleteDuplicateFolder([["a"], ["a", "x"], ["a", "z"], ["b"], ["b", "z"], ["b", "x"], ["c"], ["c", "x"]])',
    expect=[['c'], ['c', 'x']],
    skip=['self.son = {}', 'self.name =', 'self.deleted =', 'cur = root', 'if s not in cur.son', 'cur.son[s] = TrieNode()',
          'cur = cur.son[s]', 'cur.name = s', 'for s in path', 'expr_to_node = {}', 'ans = []', 'path = []'],
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='text', fn=_expr_txt, h=70),
        dict(type='map', var='expr_to_node', label='expr_to_node：子树表达式 → 第一个遇到的子树根', fmt=lambda k, v: f'{k} → {v.name}', font=24, h=110),
        dict(type='calls', h=170),
    ],
    watch=[('node', lambda S: (S.get('_inner') or {}).get('node').name if (S.get('_inner') or {}).get('node') is not None else None, 'yellow'),
           ('sub_tree_expr', lambda S: (S.get('_inner') or {}).get('sub_tree_expr'), 'cyan'),
           ('path', lambda S: S.get('path') if S.get('_line', 0) >= 47 else None), ('ans', lambda S: S.get('ans') if 'ans' in S else None, 'green')],
    captions={
        'root = TrieNode()': '用字典树存文件系统：每个节点是一个文件夹，==节点里存文件夹名==，儿子最多可以有 2 万个',
        'for path in paths': lambda S, B, r: (f"字典树建好了：`a`、`b` 各有 `x`、`z`；`c` 只有 `x`" if 'path' in B and B['path'] == S['path'] else f"把 `{S['path']}` 插进字典树（路径上缺的节点自动创建）"),
        'if not node.son': lambda S, B, r: (f"`{S.node.name}` 没有儿子：是叶子" if not S.node.son else f"`{S.node.name}` 有儿子 `{list(S.node.son)}`：先递归算每个儿子的表达式"),
        'return node.name  # 表达式': '叶子的表达式就是文件夹名 `{node.name}`，空文件夹不会被当成重复',
        'expr = sorted': '每个儿子的表达式外套括号，再==按字典序排序==（儿子顺序不同也得同一个串）：先递归算儿子',
        'sub_tree_expr = ': "排序后 `{expr}`，拼起来：`{node.name}` 的子树表达式（不含自己名字）= ==`{sub_tree_expr}`==",
        38: lambda S, B, r: ('顶层文件夹都生成过表达式了' if 'son' in B and B['son'].name == S['son'].name else f"处理顶层文件夹 `{S['son'].name}`"),
        55: lambda S, B, r: ('顶层文件夹都访问过了' if 'son' in B and B['son'].name == S['son'].name else f"顶层文件夹 `{S['son'].name}`：沿未删除的节点往下收集路径"),
        'for child in node.son.values()': lambda S, B, r: ('儿子都访问完了' if 'child' in B and B['child'].name == S['child'].name else f"继续访问儿子 `{S['child'].name}`"),
        'if sub_tree_expr in expr_to_node': lambda S, B, r: (f"`{S.sub_tree_expr}` 在哈希表里：==之前见过一模一样的子树== → 重复" if S.sub_tree_expr in S.expr_to_node else f"`{S.sub_tree_expr}` 第一次出现，记下来"),
        'expr_to_node[sub_tree_expr].deleted = True': '哈希表里记的那个节点 `{expr_to_node[sub_tree_expr].name}` 标记删除',
        'node.deleted = True': '当前节点 `{node.name}` 也标记删除',
        'expr_to_node[sub_tree_expr] = node': '哈希表记下：`{sub_tree_expr}` → `{node.name}`',
        'return node.name + sub_tree_expr': '返回给父节点：`{node.name + sub_tree_expr}`（这回带上了自己的名字）',
        'if node.deleted': lambda S, B, r: (f"`{S.node.name}` 已标记删除 → ==整棵子树直接丢掉==，不再往下" if S.node.deleted else f"`{S.node.name}` 没被删除，记录路径"),
        'path.append(node.name)': '路径入栈：`path = {path}`',
        'ans.append(path.copy())': '把当前路径的拷贝放进答案：`{path}`',
        'path.pop()': '回溯：恢复现场，`path = {path}`',
        'return ans': '剩下 `{ans}`',
    },
    max_steps=75,
    cards=dict(
        one_liner='把子树序列化成括号字符串，相同的串就是相同的文件夹',
        complexity='时间 `O(l·m·log m)`，空间 `O(l·m)`（`m` 为字符串总数，`l ≤ 10`）',
        problem=['`paths[i]` 是一个文件夹的绝对路径；两个文件夹包含==非空且相同的子文件夹结构==就算相同',
                 '把所有相同的文件夹连同子文件夹一起删除（只删一次），返回剩余路径',
                 '本视频：`a`、`b` 各含 `x`、`z`（相同）；`c` 只含 `x` → `[["c"],["c","x"]]`'],
        quote='把相同的子树映射为相同的字符串，就能用哈希表去重了。……用左括号表示递，用右括号表示归，……先把子树的表达式按照字典序排序，再把表达式依次拼接。',
        quote_src='—— 灵茶山艾府题解',
        idea=['字典树表示文件系统；DFS 给每个子树生成括号表达式：`名字(儿子1)(儿子2)…`',
              '题目不看根的名字 → 比较时去掉自己的名字，只比较 `(x)(z)` 这一段',
              '儿子要先==排序==再拼接，否则 `(x)(z)` 和 `(z)(x)` 会被当成不同',
              '重复就双方都标记删除；最后再 DFS 一遍，跳过被标记的节点收集路径'],
        summary=['叶子（空文件夹）直接返回名字、不进哈希表：题目要求子文件夹集合==非空==才算相同',
                 '删除只做一次：先全部标记，再统一收集；删后新出现的相同文件夹不管',
                 '拼接字符串看似 `O(n^2)`，但树高只有 `O(√m)`，总体仍是 `O(l·m)`',
                 '收集答案用回溯（`path.append / pop`），类似 257 二叉树的所有路径'],
    ),
)
