def _tv(d):
    return {k: v.val for k, v in d.items()}


def _same(B, S, name):
    try:
        a, b = B[name], S[name]
        return a is b or (getattr(a, 'val', a) == getattr(b, 'val', b) and getattr(a, '_uid', 0) == getattr(b, '_uid', 0))
    except Exception:
        return False


def _info(S):
    I = S['_inner']
    if 'root_dict' not in I:
        return '先收集根值和叶子值，找出唯一的最终根，再中序遍历边合并边验证'
    s = f"`root_dict` 键 {sorted(I['root_dict'])}"
    if 'leaf_set' in I:
        s += f"　叶子值 {sorted(I['leaf_set'])}"
    lv = S.get('self.last_v')
    if lv is not None and 'now' in I:
        s += f"　中序上一个值 `last_v = {lv}`"
    return s


def _child(side):
    def f(S, B, ret):
        n = B.now
        ch = getattr(n, side)
        word = '左' if side == 'left' else '右'
        if ch is None:
            return f'`{n.val}` 没有{word}孩子 → 跳过'
        if ch.val in B.root_dict:
            return f'{word}孩子 `{ch.val}` 在 `root_dict` 里 → 说明有一棵树要接到这里'
        return f'{word}孩子 `{ch.val}` 不在 `root_dict` → 普通叶子，只需检查大小'
    return f


def _visit(S, B, ret):
    return f'`now.val = {B.now.val}` 必须 `> last_v = {B.self.last_v}`（中序严格递增）'


CONFIG = dict(
    num=1932, title='合并多棵二叉搜索树', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='哈希表找根 · 中序遍历边合并边验证',
    tags=['灵神题单', '链表树与回溯', '难度分 2484'],
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
    call='Solution().canMerge([Tr([2,1]), Tr([3,2,5]), Tr([5,4])])',
    expect=[3, 2, 5, 1, None, 4],
    result_fn=lambda r: tree_list(r) if r is not None else None,
    views=[
        dict(type='text', fn=_info, size=22, h=60),
        dict(type='tree', label='待合并的树（蓝 = now）', pointers={'now': 'blue', 'final_root': 'green'}, h=250),
        dict(type='map', var='root_dict', label='root_dict（根值 → 根节点）', fmt=lambda k, v: f'{k}', h=100),
        dict(type='set', var='leaf_set', label='leaf_set（出现过的叶子值）', h=100),
        dict(type='calls', h=130, hide=('root_dict',)),
    ],
    watch=[('final_root', lambda S: getattr(S['_inner'].get('final_root'), 'val', None), 'green'),
           ('now', lambda S: getattr(S['_inner'].get('now'), 'val', None), 'blue'),
           ('last_v', lambda S: S.get('self.last_v'), 'yellow')],
    captions={
        'root_dict = {}': '`root_dict`：值 → 那棵树的根。题目保证根值互不相同，所以能唯一定位',
        'leaf_set = set()': '`leaf_set` 收集所有叶子值，BST 里值不能重复，重复就合并不了',
        'for root in trees': lambda S, B, r: ('所有树都登记完了' if _same(B, S, 'root') else f'逐棵处理：这棵树的根是 `{S.root.val}`'),
        'root_dict[root.val] = root': '登记：`root_dict[{root.val}]` = 这棵树',
        'if root.left:': lambda S, B, r: (f'`{B.root.val}` 有左叶子 `{B.root.left.val}`' if B.root.left else f'`{B.root.val}` 没有左孩子'),
        'if root.left.val not in leaf_set': '左叶子 `{root.left.val}` 没出现过 → 可以收集；出现过说明有两处要接它，无解',
        'leaf_set.add(root.left.val)': '收进 `leaf_set`：`{leaf_set}`',
        'if root.right:': lambda S, B, r: (f'`{B.root.val}` 有右叶子 `{B.root.right.val}`' if B.root.right else f'`{B.root.val}` 没有右孩子'),
        'if root.right.val not in leaf_set': '右叶子 `{root.right.val}` 没出现过 → 可以收集',
        'leaf_set.add(root.right.val)': '收进 `leaf_set`：`{leaf_set}`',
        'final_root = None': '最终的根：==不在任何树的叶子里==的那个根值',
        'for key in root_dict': lambda S, B, r: ('根值都检查完了' if _same(B, S, 'key') else f'检查根值 `{S.key}`'),
        'if key not in leaf_set': lambda S, B, r: (f'`{S.key}` 不是任何树的叶子 → 它没法接到别处，是最终根的候选'
                                                     if S.key not in S.leaf_set else f'`{S.key}` 出现在 `leaf_set` → 它会被接到别的树上，不是根'),
        'if final_root is None': '还没有候选 → 记下；已经有了第二个就==无解==（两棵树都接不上去）',
        'final_root = root_dict[key]': '最终根 = `{final_root.val}`',
        'if final_root is None:': '一个候选都没有说明成环，无解',
        'self.last_v = 0': '`last_v` 记录中序遍历上一个值，初值 0（节点值 ≥ 1）',
        'if not self.dfs(final_root': '从最终根开始中序遍历，边遍历边把子树接上',
        'if now.left:': _child('left'),
        'if now.left.val in root_dict': lambda S, B, r: (f'左孩子 `{B.now.left.val}` 在 `root_dict` 里' if B.now.left.val in B.root_dict else f'左孩子 `{B.now.left.val}` 是普通叶子'),
        'now.left = root_dict': '把根为 `{now.left.val}` 的整棵树接到 `now` 的左边',
        'root_dict.pop(now.left.val)': '从 `root_dict` 弹出 `{B.now.left.val}`：这棵树已被用掉',
        'self.dfs(now.left': '递归进入刚接上的左子树',
        'elif now.left.val <= self.last_v': '普通叶子要比 `last_v = {self.last_v}` 大才保持递增',
        'self.last_v = now.left.val': '访问左叶子，`last_v = {self.last_v}`',
        'if now.val <= self.last_v': _visit,
        'self.last_v = now.val': '访问 `now`，`last_v = {self.last_v}`',
        'if now.right:': _child('right'),
        'if now.right.val in root_dict': lambda S, B, r: (f'右孩子 `{B.now.right.val}` 在 `root_dict` 里' if B.now.right.val in B.root_dict else f'右孩子 `{B.now.right.val}` 是普通叶子'),
        'now.right = root_dict': '把根为 `{now.right.val}` 的整棵树接到 `now` 的右边',
        'root_dict.pop(now.right.val)': '从 `root_dict` 弹出 `{B.now.right.val}`：这棵树已被用掉',
        'self.dfs(now.right': '递归进入刚接上的右子树',
        'elif now.right.val <= self.last_v': '普通叶子要比 `last_v = {self.last_v}` 大才保持递增',
        'self.last_v = now.right.val': '访问右叶子，`last_v = {self.last_v}`',
        'return True': '这棵子树中序严格递增，返回 True',
        'if len(root_dict) != 1': lambda S, B, r: f'`root_dict` 只剩 {len(S.root_dict)} 个 → ' + ('其它树都已合并进来' if len(S.root_dict) == 1 else '有树没合并进来，无解'),
        'return final_root': '合并成功，返回最终根 `{final_root.val}`',
    },
    skip=['if not self.dfs(now.left', 'if not self.dfs(now.right', 'if now.left.val in root_dict', 'if now.right.val in root_dict'],
    max_steps=110,
    cards=dict(
        one_liner='唯一不是叶子的根就是最终根，中序遍历时边接边验证',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`trees` 里有 n 棵 BST（每棵最多 3 个节点），根值互不相同',
                 '每步：选一棵树的叶子，值等于另一棵树的根值，就用后者替换这个叶子',
                 '做完 n - 1 次操作后若得到一棵合法 BST，返回根，否则返回 `null`',
                 '本视频：`[[2,1],[3,2,5],[5,4]]` → `[3,2,5,1,null,4]`'],
        quote='可以使用哈希表root_dict建立值到节点的唯一映射，方便后续的合并操作。……遍历所有根节点的值，如果其没有出现在叶子节点值的集合中，说明其对应的根节点就是最终的根节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['`root_dict`：根值 → 树；`leaf_set`：所有叶子值，重复出现就==无解==',
              '不在 `leaf_set` 里的根只能当最终根，多于一个也无解',
              '从最终根中序遍历：遇到值在 `root_dict` 的叶子就把整棵树接上并弹出；只用 `last_v` 检查严格递增'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '三处判无解：叶子值重复；候选根不唯一；中序不递增或 `root_dict` 没被用完（`len != 1`）',
                 '`dfs` 里 `pop` 之后 `now.left` 已指向新树，所以 `now.left.val` 仍是同一个值',
                 '中序遍历只保存 `last_v`，不需要存整个序列；原文为 Python 2 风格，本代码无需改动'],
    ),
)
