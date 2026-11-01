def _subs(S):
    a = S.get('is_sub')
    return None if a is None else {i for i, b in enumerate(a) if b}


def _roots(S):
    a = S.get('roots')
    return None if a is None else {i: f'树根 {i}' for i, r in enumerate(a) if r is not None}


def _col(S, n):
    a = S.get('roots')
    if a is not None and n.val < len(a) and a[n.val] is n:
        return 'blue'
    return None


def _cap_sub(side):
    def f(S, B, ret):
        rt = S['rt']
        ch = getattr(rt, side)
        w = '左' if side == 'left' else '右'
        if S['is_sub'][ch.val]:
            return f'`{rt.val}` 的{w}儿子 `{ch.val}` 之前已经当过别人的儿子 → 同一个值出现两次，BST 不可能，返回 `None`'
        return f'`{rt.val}` 有{w}儿子 `{ch.val}`，之前没当过别人的儿子 → 继续'
    return f


def _cap_bound(side):
    def f(S, B, ret):
        i = S['_inner']
        node = i['node']
        ch = getattr(node, side)
        w = '左' if side == 'left' else '右'
        if side == 'left':
            bad, rel = ch.val <= i['l'], f'`{ch.val} <= {i["l"]}`'
        else:
            bad, rel = ch.val >= i['r'], f'`{ch.val} >= {i["r"]}`'
        s = f'{w}儿子 `{ch.val}` 必须在开区间 `({i["l"]}, {i["r"]})` 内：{rel} '
        return s + ('成立 → ==越界，不是 BST==，返回 `None`' if bad else '不成立 → 没越界')
    return f


def _cap_graft(side):
    def f(S, B, ret):
        i = S['_inner']
        node = i['node']
        ch = getattr(node, side)
        w = '左' if side == 'left' else '右'
        sub = i['lo'] if side == 'left' else i['ro']
        if sub is None:
            return f'`roots[{ch.val}]` 是空 → `{ch.val}` 只是普通叶子，不用拼'
        return f'`roots[{ch.val}]` 有树 → 把它接到 `{node.val}` 的{w}边，递归 `build` 并带上收紧后的值域'
    return f


CONFIG = dict(
    num=1932, title='合并多棵二叉搜索树', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='找唯一根 · 递归拼接并校验上下界（Go 原文转写）',
    tags=['灵神题单·链表树与回溯', '难度分 2484'],
    code='''
class Solution:
    def canMerge(self, trees: List[TreeNode]) -> Optional[TreeNode]:
        mx = 5 * 10 ** 4 + 1
        is_sub = [False] * mx  # 对于根节点，需要知道其是否为另一颗二叉搜索树的子节点
        roots = [None] * mx  # 对于子节点，我们需要知道其数值所对应的二叉搜索树的根节点是哪个
        for rt in trees:
            if rt.left is not None:
                if is_sub[rt.left.val]:  # 由于二叉搜索树上不能有两个值相同的节点，所以 trees 中也不能有两个值相同的子节点
                    return None
                is_sub[rt.left.val] = True
            if rt.right is not None:
                if is_sub[rt.right.val]:
                    return None
                is_sub[rt.right.val] = True
            roots[rt.val] = rt

        root = None
        for rt in trees:
            if not is_sub[rt.val]:  # 根节点不应是另一颗二叉搜索树的子节点，否则二叉搜索树上会出现两个值相同的节点
                if root is not None:  # 根节点应只有一个，否则会构成森林
                    return None
                root = rt
        if root is None:  # 未找到根节点
            return None

        cnt = 0
        # 在构建二叉搜索树的同时判断是否合法
        def build(node: TreeNode, l: int, r: int) -> Optional[TreeNode]:
            nonlocal cnt
            cnt += 1
            if node.left is not None:
                if node.left.val <= l:
                    return None
                lo = roots[node.left.val]
                if lo is not None:
                    node.left = build(lo, l, node.val)
                    if node.left is None:
                        return None
            if node.right is not None:
                if node.right.val >= r:
                    return None
                ro = roots[node.right.val]
                if ro is not None:
                    node.right = build(ro, node.val, r)
                    if node.right is None:
                        return None
            return node
        root = build(root, 0, mx)
        if cnt == len(trees):  # 所有 trees[i] 均参与构建二叉搜索树
            return root
        return None
''',
    call='Solution().canMerge([Tr([2, 1]), Tr([3, 2, 5]), Tr([5, 4])])',
    expect=[3, 2, 5, 1, None, 4],
    result_fn=tree_list,
    snap_maxlen=16,
    views=[
        dict(type='tree', label='森林（黄圈 = 当前 build，蓝 = 原树根）', h=300, color=_col),
        dict(type='set', var=_subs, label='is_sub（这些值当过别人的子节点）', h=95),
        dict(type='map', var=_roots, label='roots（值 → 以它为根的那棵树）', h=95, font=22),
        dict(type='calls', h=140),
    ],
    watch=[('rt', lambda S: S.get('rt').val if S.get('rt') is not None else None, 'blue'),
           ('root', lambda S: S.get('root').val if S.get('root') is not None else None, 'green'),
           ('cnt', 'cnt', 'yellow'), ('l', lambda S: S['_inner'].get('l')), ('r', lambda S: S['_inner'].get('r'))],
    skip=['mx = 5', 'is_sub = [False]', 'roots = [None]', 'cnt = 0', 'nonlocal', 'cnt += 1', 'if rt.left is not None', 'if rt.right is not None', 'if lo is not None', 'if ro is not None', 'if node.left is None', 'if node.right is None', 'root = None'],
    captions={
        'is_sub[rt.left.val] = True': '记下：值 `{rt.left.val}` 是别人的儿子，`is_sub` 里加上它',
        'is_sub[rt.right.val] = True': '记下：值 `{rt.right.val}` 是别人的儿子，`is_sub` 里加上它',
        'if is_sub[rt.left.val]': _cap_sub('left'),
        'if is_sub[rt.right.val]': _cap_sub('right'),
        'roots[rt.val] = rt': '`roots[{rt.val}]` 记住这棵树：以后某个叶子的值是 `{rt.val}`，就拿它来替换',
        'if not is_sub[rt.val]': lambda S, B, ret: (f'树根 `{S.rt.val}` ' + ('当过别人的叶子 → 它会被接到别的树上，不是最终的根' if S.is_sub[S.rt.val] else '没当过任何人的叶子 → 它有资格当最终的根')),
        'if root is not None': lambda S, B, ret: ('已经有一个候选根了，这里又来一个 → 会剩下森林，返回 `None`' if S.root is not None else '这是第一个候选根'),
        'root = rt': '记下候选根：`root = {rt.val}`',
        'if root is None': lambda S, B, ret: ('一个候选根都没有 → 返回 `None`' if S.root is None else f'有唯一的根 `{S.root.val}` → 往下拼'),
        'root = build(root, 0, mx)': '从根开始拼：值域是开区间 `(0, mx)`，一边递归一边校验 BST',
        'if node.left is not None': lambda S, B, ret: (f'`{S["_inner"]["node"].val}` 有左儿子 `{S["_inner"]["node"].left.val}`' if S['_inner']['node'].left is not None else f'`{S["_inner"]["node"].val}` 没有左儿子，跳过'),
        'if node.right is not None': lambda S, B, ret: (f'`{S["_inner"]["node"].val}` 有右儿子 `{S["_inner"]["node"].right.val}`' if S['_inner']['node'].right is not None else f'`{S["_inner"]["node"].val}` 没有右儿子，跳过'),
        'node.left.val <= l': _cap_bound('left'),
        'node.right.val >= r': _cap_bound('right'),
        'lo = roots': _cap_graft('left'),
        'ro = roots': _cap_graft('right'),
        'node.left = build': '把根为 `{B.lo.val}` 的那棵树接到 `{B.node.val}` 左边：左边的值要夹在 `({B.l}, {B.node.val})` 之间',
        'node.right = build': '把根为 `{B.ro.val}` 的那棵树接到 `{B.node.val}` 右边：右边的值要夹在 `({B.node.val}, {B.r})` 之间',
        'return node': '`{node.val}` 这一层没问题，返回自己作为合并后的子树',
        'if cnt == len(trees)': lambda S, B, ret: f'`cnt = {S.cnt}`：被拼进来的树有 {S.cnt} 棵，一共 {len(S.trees)} 棵 → ' + ('全部用上了' if S.cnt == len(S.trees) else '有树没用上'),
    },
    cards=dict(
        one_liner='先找出唯一的根，再一路拼接一路检查值域',
        complexity='时间 `O(n)`，空间 `O(n)`（`n` 是 `trees` 的长度，值域为 5×10⁴）',
        problem=['给若干棵最多 3 个节点的 BST，操作：把某棵树的根换到另一棵的叶子上',
                 '做 `n-1` 次操作后若能得到一棵有效 BST，返回它的根，否则返回 `null`',
                 '示例：`[[2,1],[3,2,5],[5,4]]` → `[3,2,5,1,null,4]`'],
        quote='根节点不应是另一颗二叉搜索树的子节点，否则二叉搜索树上会出现两个值相同的节点。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['`is_sub` 记录哪些值当过叶子，`roots` 记录每个值对应的树根',
              '没有当过叶子的根只能有一个，它就是最终的根；多了或没有都不行',
              '从根开始 `build`，沿途把叶子换成对应的树，并用开区间 `(l, r)` 检查 BST 性质；最后看 `cnt` 是否等于树的个数'],
        result='运行结束，返回合并后的树 `[3,2,5,1,null,4]`',
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`[mx]bool{}` → `[False] * mx`，`var build func` → 嵌套函数 + `nonlocal cnt`）',
                 '时间 `O(n)`，空间 `O(mx)`（两个大小为 5×10⁴+1 的数组）',
                 '易错：叶子值重复出现、没有唯一根、拼出来越界、有的树没被用上，都要返回 `None`',
                 '`cnt == len(trees)` 用来发现「有树根本接不上」的情况'],
    ),
)
