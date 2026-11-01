def _leafs(S):
    return S.get('leaf_set')


def _rd(S):
    d = S.get('root_dict')
    return None if d is None else {k: f'树根 {k}' for k in d}


def _col(S, n):
    lv = S.get('self.last_v')
    if lv is not None and lv > 0 and n.val <= lv:
        return 'green'
    ts = S.get('trees') or []
    if any(n is t for t in ts):
        return 'blue'
    return None


def _cap_chk(side):
    def f(S, B, ret):
        root = S['root']
        ch = getattr(root, side)
        w = '左' if side == 'left' else '右'
        if ch.val in S['leaf_set']:
            return f'`{root.val}` 的{w}儿子 `{ch.val}` 已经在 `leaf_set` 里 → BST 里不能有两个相同的值，返回 `None`'
        return f'`{root.val}` 的{w}儿子 `{ch.val}` 第一次出现，可以收进 `leaf_set`'
    return f


def _cap_dfs_side(side):
    def f(S, B, ret):
        i = S['_inner']
        now = i['now']
        ch = getattr(now, side)
        w = '左' if side == 'left' else '右'
        if ch is None:
            return f'`{now.val}` 没有{w}儿子，跳过'
        if ch.val in i['root_dict']:
            return f'{w}儿子 `{ch.val}` 在 `root_dict` 里 → 有一棵树要接到这里'
        return f'{w}儿子 `{ch.val}` 不在 `root_dict` 里 → 它就是普通叶子，直接参与中序比较'
    return f


CONFIG = dict(
    num=1932, title='合并多棵二叉搜索树', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='哈希表找根 · 中序遍历合并并检查递增',
    tags=['灵神题单·链表树与回溯', '难度分 2484'],
    code='''
class Solution(object):
    def canMerge(self, trees):
        root_dict = {}
        leaf_set = set()

        for root in trees:
            root_dict[root.val] = root
            if root.left:
                if root.left.val not in leaf_set:
                    leaf_set.add(root.left.val)
                else:
                    return None
            if root.right:
                if root.right.val not in leaf_set:
                    leaf_set.add(root.right.val)
                else:
                    return None
        
        final_root = None
        for key in root_dict:
            if key not in leaf_set:
                if final_root is None:
                    final_root = root_dict[key]
                else:
                    return None
        
        if final_root is None:
            return None

        self.last_v = 0
        if not self.dfs(final_root, root_dict):
            return None
        if len(root_dict) != 1:
            return None
        return final_root
    
    def dfs(self, now, root_dict):
        if now.left:
            if now.left.val in root_dict:
                now.left = root_dict[now.left.val]
                root_dict.pop(now.left.val)
                if not self.dfs(now.left, root_dict):
                    return False
            elif now.left.val <= self.last_v:
                return False
            else:
                self.last_v = now.left.val

        if now.val <= self.last_v:
            return False
        self.last_v = now.val

        if now.right:
            if now.right.val in root_dict:
                now.right = root_dict[now.right.val]
                root_dict.pop(now.right.val)
                if not self.dfs(now.right, root_dict):
                    return False
            elif now.right.val <= self.last_v:
                return False
            else:
                self.last_v = now.right.val
        
        return True
''',
    call='Solution().canMerge([Tr([2, 1]), Tr([3, 2, 5]), Tr([5, 4])])',
    expect=[3, 2, 5, 1, None, 4],
    result_fn=tree_list,
    views=[
        dict(type='tree', label='森林（蓝 = 原树根，绿 = 中序已访问，黄圈 = 当前 dfs）', h=290, color=_col),
        dict(type='set', var=_leafs, label='leaf_set（出现过的叶子值，不许重复）', h=95),
        dict(type='map', var=_rd, label='root_dict（值 → 还没被合并的树）', h=95, font=22),
        dict(type='calls', h=130),
    ],
    watch=[('final_root', lambda S: S['final_root'].val if S.get('final_root') is not None else None, 'green'),
           ('now', lambda S: S['_inner']['now'].val if S['_inner'].get('now') is not None else None, 'blue'),
           ('last_v', 'self.last_v', 'orange')],
    skip=['root_dict = {}', 'leaf_set = set()', 'final_root = None', 'self.last_v = 0', 'if root.left:', 'if root.right:', 'if now.left:', 'if now.right:', 'else:'],
    captions={
        'root_dict[root.val] = root': '值 `{root.val}` ↔ 这棵树：根的值互不相同，所以能当 `root_dict` 的键',
        'if root.left.val not in leaf_set': _cap_chk('left'),
        'if root.right.val not in leaf_set': _cap_chk('right'),
        'leaf_set.add(root.left.val)': '`leaf_set` 加入 `{root.left.val}`',
        'leaf_set.add(root.right.val)': '`leaf_set` 加入 `{root.right.val}`',
        'if key not in leaf_set': lambda S, B, ret: (f'根 `{S.key}` ' + ('不是任何树的叶子 → 它有资格当最终的根' if S.key not in S.leaf_set else '是别人的叶子 → 会被接到别的树上')),
        'if final_root is None': lambda S, B, ret: (('这是第一个候选根（`final_root` 还是 `None`）' if S.final_root is None else '已经有候选根了，又来一个 → 会剩下森林，返回 `None`') if S['_line'] == 22 else ('没找到根 → 返回 `None`' if S.final_root is None else f'有唯一的根 `{S.final_root.val}` → 往下拼')),
        'final_root = root_dict[key]': '最终的根：`{final_root.val}`',
        'if not self.dfs(final_root': '从最终的根出发做「中序遍历」，边走边把树接上',
        'if len(root_dict) != 1': lambda S, B, ret: f'`root_dict` 里还剩 `{len(S.root_dict)}` 棵树：' + ('只剩最终的根 → 全部合进来了' if len(S.root_dict) == 1 else '还有树没合进去 → 返回 `None`'),
        'if now.left.val in root_dict': _cap_dfs_side('left'),
        'if now.right.val in root_dict': _cap_dfs_side('right'),
        'now.left = root_dict': '把 `root_dict[{now.left.val}]` 这棵树换到 `{now.val}` 的左边',
        'now.right = root_dict': '把 `root_dict[{now.right.val}]` 这棵树换到 `{now.val}` 的右边',
        'root_dict.pop(now.left.val)': '用掉了就弹出：`root_dict` 剩 `{list(root_dict)}`',
        'root_dict.pop(now.right.val)': '用掉了就弹出：`root_dict` 剩 `{list(root_dict)}`',
        'if not self.dfs(now.left': '递归处理左边这棵新接上的树',
        'if not self.dfs(now.right': '递归处理右边这棵新接上的树',
        'elif now.left.val <= self.last_v': lambda S, B, ret: (f'叶子 `{S["_inner"]["now"].left.val}` ≤ 上一个值 `{S["self.last_v"]}` → 中序不递增，不是 BST，返回 `False`' if S['_inner']['now'].left.val <= S['self.last_v'] else f'叶子 `{S["_inner"]["now"].left.val}` > 上一个值 `{S["self.last_v"]}` → 仍然递增'),
        'elif now.right.val <= self.last_v': lambda S, B, ret: (f'叶子 `{S["_inner"]["now"].right.val}` ≤ 上一个值 `{S["self.last_v"]}` → 中序不递增，不是 BST，返回 `False`' if S['_inner']['now'].right.val <= S['self.last_v'] else f'叶子 `{S["_inner"]["now"].right.val}` > 上一个值 `{S["self.last_v"]}` → 仍然递增'),
        'self.last_v = now.left.val': '普通叶子：`last_v` 更新为 `{now.left.val}`',
        'self.last_v = now.right.val': '普通叶子：`last_v` 更新为 `{now.right.val}`',
        'if now.val <= self.last_v': lambda S, B, ret: (f'`{S["_inner"]["now"].val}` 比上一个值 `{S["self.last_v"]}` 大吗？' + ('不大 → 中序不递增，返回 `False`' if S['_inner']['now'].val <= S['self.last_v'] else '大 → 仍然递增')),
        'self.last_v = now.val': '访问到 `{now.val}`：`last_v` → `{now.val}`（只存上一个值，不用存整个中序序列）',
        'return True': '`{now.val}` 这棵子树的中序一路递增，返回 `True`',
    },
    cards=dict(
        one_liner='用中序遍历是否严格递增来验证合并后的 BST',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给若干棵最多 3 个节点的 BST，可把某棵树的根换到另一棵的叶子上',
                 '做完 `n-1` 次操作后若得到一棵有效 BST，返回根，否则返回 `null`',
                 '示例：`[[2,1],[3,2,5],[5,4]]` → `[3,2,5,1,null,4]`'],
        quote='中序遍历完成后，若中序遍历的结果不是单调递增的，那么说明最终并不是二叉搜索树，直接返回空。',
        quote_src='—— yiduobo 题解',
        idea=['`root_dict` 记根值到树的映射，`leaf_set` 收集所有叶子值，叶子值重复就失败',
              '不在 `leaf_set` 里的根只能有一个，它是最终的根',
              '从最终的根做中序遍历，遇到能接的叶子就把整棵树接上并弹出；只记上一个值 `last_v` 检查递增'],
        result='运行结束，返回合并后的树 `[3,2,5,1,null,4]`',
        summary=['时间 `O(n)`，空间 `O(n)`；中序遍历只保存 `last_v`，不用存整个序列',
                 '易错：中序比较要把左叶子、根、右叶子都算进去，而且是严格递增（相等也不行）',
                 '易错：遍历完要检查 `len(root_dict) == 1`，否则有树没合进去',
                 '对照灵神：他用 `(l, r)` 值域边递归边检查，这里改用「中序是否递增」来验证'],
    ),
)
