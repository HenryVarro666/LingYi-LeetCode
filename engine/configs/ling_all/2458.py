def _hmap(S):
    h = S.get('height')
    if not isinstance(h, dict):
        return None
    return {k.val: v for k, v in h.items() if k is not None}


def _nv(n):
    return '空' if n is None else str(n.val)


def _info(S):
    I = S.get('_inner', {})
    if 'rest_h' in I and 'depth' in I and I.get('node') is not None:
        return f"走到节点 `{I['node'].val}`：深度 `depth = {I['depth']}`，删掉它后其余部分的高度 `rest_h = {I['rest_h']}`"
    return ''


def _cap_gh(S, B, ret):
    n = S.node
    if n is None:
        return '空节点高度是 `0`，递归边界'
    return f'节点 `{n.val}` 非空 → 高度取决于左右子树'


def _cap_set(S, B, ret):
    return f'节点 `{S.node.val}`：`height = 1 + max({_h(S.node.left, S)}, {_h(S.node.right, S)}) = =={S.height[S.node]}==`'


def _h(n, S):
    return 0 if n is None else S.height[n]


def _cap_res(S, B, ret):
    return f'删掉 `{S.node.val}` 整棵子树后，树的高度 = 目前的 `rest_h = =={S.rest_h}==`，记到 `res[{S.node.val}]`'


def _cap_l(S, B, ret):
    n = B.node
    return (f'往左走：删掉左子树里的点时，右子树还在 → 候选高度 `depth + height[右] = {B.depth} + {_h(n.right, S)}`，'
            f'和 `rest_h = {B.rest_h}` 取大 → 传下去 =={max(B.rest_h, B.depth + _h(n.right, S))}==')


def _cap_r(S, B, ret):
    n = B.node
    return (f'往右走：此时左子树还在 → `depth + height[左] = {B.depth} + {_h(n.left, S)}`，'
            f'和 `rest_h = {B.rest_h}` 取大 → 传下去 =={max(B.rest_h, B.depth + _h(n.left, S))}==')


CONFIG = dict(
    num=2458, title='移除子树后的二叉树高度', difficulty='Hard', category='二叉树与回溯',
    author='灵茶山艾府', technique='两次 DFS · 子树高度 + 剩余高度',
    tags=['灵神题单', '链表树与回溯', '难度分 2299'],
    code='''
class Solution:
    def treeQueries(self, root: Optional[TreeNode], queries: List[int]) -> List[int]:
        height = defaultdict(int)  # 每棵子树的高度
        def get_height(node: Optional[TreeNode]) -> int:
            if node is None: return 0
            height[node] = 1 + max(get_height(node.left), get_height(node.right))
            return height[node]
        get_height(root)

        res = [0] * (len(height) + 1)  # 每个节点的答案
        def dfs(node: Optional[TreeNode], depth: int, rest_h: int) -> None:
            if node is None: return
            depth += 1
            res[node.val] = rest_h
            dfs(node.left, depth, max(rest_h, depth + height[node.right]))
            dfs(node.right, depth, max(rest_h, depth + height[node.left]))
        dfs(root, -1, 0)

        for i, q in enumerate(queries):
            queries[i] = res[q]
        return queries
''',
    call='''s = Solution()
s.tree = Tr([1,2,3,4,5,None,None,6])
s.treeQueries(s.tree, [3,4,2])''',
    expect=[3, 2, 1],
    views=[
        dict(type='tree', label='二叉树（蓝 = node）', pointers={'node': 'blue'}, h=300),
        dict(type='text', fn=_info, size=24, h=50),
        dict(type='map', var=_hmap, label='height：节点值 → 子树高度（按节点数）', font=22, h=110),
        dict(type='array', var=lambda S: S.get('res'), label='res[v]：删掉 v 的子树后的高度', cell=64, h=130),
        dict(type='calls', h=180, hide=('queries',)),
    ],
    watch=[('node', lambda S: S['_inner'].get('node') and S['_inner']['node'].val, 'blue'),
           ('depth', lambda S: S['_inner'].get('depth'), 'yellow'),
           ('rest_h', lambda S: S['_inner'].get('rest_h'), 'orange')],
    captions={
        'height = defaultdict(int)': '`height[node]`：每棵子树的高度（这里数==节点数==）；`defaultdict` 让空孩子自动是 0',
        'get_height(root)': '第一遍 DFS：自底向上算出每棵子树的高度',
        'if node is None: return 0': lambda S, B, r: ('空节点高度是 `0`，递归边界' if S.node is None else f'节点 `{S.node.val}` 非空 → 高度取决于左右子树'),
        'height[node] = 1': '先递归算出左右子树的高度，再 `1 + max(左, 右)` 算上自己',
        'return height[node]': lambda S, B, r: f'节点 `{S.node.val}` 的子树高度 `1 + max(左, 右) = =={r}==`，交给父亲',
        'res = [0]': '`res[v]` 存“删掉 `v` 的子树后树的高度”；下标就是节点值，所以长度 `n + 1`',
        'dfs(root, -1, 0)': '第二遍 DFS：自顶向下，带着 `depth`（根处为 0）和 `rest_h`（删掉当前子树后其余部分的高度）',
        12: lambda S, B, r: ('到了空节点：没有子树可删，直接返回' if S.node is None else f'节点 `{S.node.val}` 非空，继续'),
        'res[node.val] = rest_h': lambda S, B, r: f'`depth` 来到 `{S.depth}`；节点 `{S.node.val}` 整棵子树删掉后，==剩下部分的高度就是 `rest_h = {S.rest_h}`== → 记入 `res[{S.node.val}]`',
        'dfs(node.left': lambda S, B, r: (f'往左走：此时右子树还留着，它能到的最深处是 `depth + height[右] = {B.depth} + {B.height[B.node.right]} = {B.depth + B.height[B.node.right]}`，和 `rest_h = {B.rest_h}` 取大 → 传给左儿子' if B.node.left is not None else '没有左儿子，传 `None` 下去会直接返回'),
        'dfs(node.right': lambda S, B, r: (f'往右走：此时左子树还留着，最深处 `depth + height[左] = {B.depth} + {B.height[B.node.left]} = {B.depth + B.height[B.node.left]}`，和 `rest_h = {B.rest_h}` 取大 → 传给右儿子' if B.node.right is not None else '没有右儿子，传 `None` 下去会直接返回'),
        'for i, q in enumerate': '现在每个查询 `q` 只需要查表 `res[q]`',
        'queries[i] = res[q]': '`queries[{i}] = res[{q}] = {queries[i]}`：删掉 `{q}` 的子树后，树高 =={queries[i]}==',
        'return queries': lambda S, B, r: f'答案直接覆盖在 `queries` 里：`{r}`',
    },
    skip=['depth += 1'],
    max_steps=56,
    cards=dict(
        one_liner='先量每棵子树多高，再往下走时带着“删掉兄弟那侧之外的最高路径”',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二叉树，值是互不相同的 `1..n`；每次查询删掉以 `queries[i]` 为根的子树，返回此时树的高度（根到最远节点的==边数==）',
                 '查询彼此独立，每次删完树会恢复',
                 '示例：`[5,8,9,2,1,3,7,4,6]`，`queries=[3,2,4,8]` → `[3,2,3,2]`',
                 '本视频用小一点的树 `[1,2,3,4,5,null,null,6]`，`queries=[3,4,2]`'],
        quote='先跑一遍 DFS，求出每棵子树的高度 height；然后再 DFS 一遍这棵树，同时维护当前节点深度 depth，以及删除当前子树后剩余部分的树的高度 rest_h。',
        quote_src='—— 灵茶山艾府题解',
        idea=['第一遍 DFS：算出每个节点的子树高度 `height`（这里数节点数）',
              '第二遍 DFS：往左走，删掉左边的点后，右子树还在，所以候选是 `depth + height[右]`',
              '往右走同理用 `height[左]`；沿路和 `rest_h` 取最大',
              '每个节点处的 `rest_h` 就是删掉它的子树后的答案，==预先全存到 res==，查询 `O(1)`'],
        result='运行结束：`res` 已存好每个点的答案，查询直接查表，返回 `[3, 2, 1]`',
        summary=['时间 `O(n)`，空间 `O(n)`；查询只需查表',
                 '易错：`height` 数的是节点数，`depth` 从 `-1` 起、进入节点先 `+1`，两者相加才等于边数',
                 '`rest_h` 沿路取 max：不仅要看兄弟子树，也要继承祖先那一层的候选',
                 '`height` 是 `defaultdict`，所以空孩子 `height[None]` 自动为 `0`',
                 '代码把答案直接覆盖写回 `queries`，省一个数组'],
    ),
)
