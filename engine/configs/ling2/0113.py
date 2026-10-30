TREE = [5, 4, 8, 11, None, None, 4, 7, 2, 5]
TARGET = 22


def _path_to(root, uid):
    if root is None:
        return None
    if root._uid == uid:
        return [root]
    for ch in (root.left, root.right):
        p = _path_to(ch, uid)
        if p:
            return [root] + p
    return None


def _tree_color(S, n):
    p = _path_to(S.get('root'), n._uid) or []
    vals = [x.val for x in p]
    if any(a[:len(vals)] == vals for a in S.get('ans') or []):
        return 'green'
    return None


def _text(S):
    if 'path' not in S:
        return f'`targetSum = {TARGET}`：参数 `left` 表示==还差多少=='
    path = S['path']
    s = sum(path)
    left = S.get('left')
    tail = f'，`left = {TARGET} − {s} = {left}`' if isinstance(left, int) and path and left == TARGET - s else ''
    return f'`path = {path}`，和为 `{s}`{tail}'


def _cap_leaf(S, B, ret):
    v, left = S.node.val, S.left
    if S.node.left is None and S.node.right is None:
        if left == 0:
            return f'`{v}` 是叶子且 `left = 0` → ==找到一条路径== `{S.path}`'
        return f'`{v}` 是叶子，但 `left = {left} ≠ 0` → 和不对，不是答案'
    return f'`{v}` 不是叶子 → 递归左右子树，把 `left = {left}` 传下去'


def _cap_call(word):
    def f(S, B, ret):
        par = B.node.val
        kid = S.get('node')
        if kid is None:
            return f'`{par}` 的{word}儿子为空 → 进去立刻返回'
        note = '（int 参数是复制的，不用恢复）' if B.node is S.root else ''
        return f'递归 `{par}` 的{word}子树 `{kid.val}`，`left = {S.left}`{note}'
    return f


CONFIG = dict(
    num=113, title='路径总和 II', difficulty='Medium', category='二叉树',
    author='灵茶山艾府', technique='DFS 回溯 · 恢复现场',
    tags=['字节30天', '热题173'],
    code='''
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        ans = []
        path = []

        def dfs(node: Optional[TreeNode], left: int) -> None:
            if node is None:
                return
            path.append(node.val)
            left -= node.val
            if node.left is None and node.right is None and left == 0:
                ans.append(path.copy())  # 也可以写 path[:]
            else:
                dfs(node.left, left)
                dfs(node.right, left)
            path.pop()  # 恢复现场

        dfs(root, targetSum)
        return ans
''',
    call=f'Solution().pathSum(Tr({TREE}), {TARGET})',
    expect=[[5, 4, 11, 2], [5, 8, 4, 5]],
    skip=['if node is None', '                return'],
    max_steps=70,
    views=[
        dict(type='text', fn=_text, h=56),
        dict(type='tree', label='二叉树（黄圈 = 递归路径，绿 = 已找到的答案路径）', pointers={'node': 'blue'},
             color=_tree_color, h=310),
        dict(type='stack', var='path', label='path（= 递归栈上的节点值）', h=112),
        dict(type='table', var='ans', label='ans', rows=lambda S: [f'#{k + 1}' for k in range(len(S.get('ans') or []))],
             h=150, cell=56),
    ],
    watch=[('left', 'left', 'cyan'), ('targetSum', 'targetSum'), ('答案数', 'len(ans)', 'green')],
    captions={
        'ans = []': '`ans` 收集所有满足要求的路径',
        'path = []': '`path` 放在递归函数==外部==：记录从根到当前节点的路径',
        'path.append': '把 `{node.val}` 加入路径 → `path = {path}`',
        'left -= node.val': lambda S, B, ret: (f'`left = {B.left} − {S.node.val} = {S.left}`' + (f'：还差 `{S.left}`' if S.left > 0 else '')),
        'if node.left is None and': _cap_leaf,
        'ans.append(path.copy())': '把 `path` ==复制一份==加入答案：`{ans[-1]}`（不复制的话，之后的 pop 会改掉它）',
        'dfs(node.left, left)': _cap_call('左'),
        'dfs(node.right, left)': _cap_call('右'),
        'path.pop()': lambda S, B, ret: (f'==恢复现场==：`{B.path[-1]}` 的子树走完了，弹出它 → `path = {S.path}`'),
        'dfs(root, targetSum)': '从根出发，`left = targetSum = {left}`',
        'return ans': '所有根到叶子的路径都试过了，返回 `{ret}`',
    },
    cards=dict(
        one_liner='递归时把 left 减去节点值；path 进来时加、离开时弹（恢复现场）',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['给二叉树根 `root` 和整数 `targetSum`',
                 '找出所有==从根节点到叶子节点==、节点值之和等于 `targetSum` 的路径',
                 '示例：`[5,4,8,11,null,13,4,7,2,null,null,5,1]`，`22` → `[[5,4,11,2],[5,8,4,5]]`',
                 '本视频去掉两个节点：`[5,4,8,11,null,null,4,7,2,5]`，`22`'],
        quote='当我们递归完左子树，要递归右子树之前，path 中还保留着左子树的节点。如果不及时去掉，会导致最终加到答案中的 path，==既包含左子树的节点，又包含右子树的节点==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['递归参数 `left` 从 `targetSum` 开始，每到一个节点就减去它的值',
              '到达叶子且 `left = 0` → 把 `path` 的==副本==加入答案',
              '递归返回前 `path.pop()`：去掉开头加入的节点，==恢复现场=='],
        result='返回 `[[5,4,11,2],[5,8,4,5]]`：两条路径的和都是 22',
        after=[dict(heading='原文答疑', lines=[
            '问：为什么加入答案前要复制 `path`？',
            '答：不复制的话 `ans` 存的是同一个 `path` 的==引用==，之后修改会连带改掉',
            '问：为什么参数 `left` 不需要恢复现场？',
            '答：int 参数调用时会==复制==一份往下传，只改当前这层的 `left`',
        ])],
        summary=['时间 `O(n^2)`：「扫帚型」树有 `O(n)` 个叶子，每次复制长 `O(n)` 的 path',
                 '空间 `O(n)`：递归栈 + path，返回值不计入',
                 '易错：必须是==叶子==才判断 `left == 0`，中途凑够不算',
                 '易错：`ans.append(path)` 不复制 → 最后全是空列表',
                 '同类：112 路径总和（只问有没有）、437 路径总和 III（任意向下路径）'],
    ),
)
