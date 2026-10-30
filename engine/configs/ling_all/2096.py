CODE = '''
class Solution:
    def getDirections(self, root: Optional[TreeNode], startValue: int, destValue: int) -> str:
        path_to_start = path_to_dest = None
        path = []

        def dfs(node: Optional[TreeNode]) -> None:
            if node is None:
                return

            nonlocal path_to_start, path_to_dest
            if node.val == startValue:
                path_to_start = path.copy()
            elif node.val == destValue:
                path_to_dest = path.copy()

            # 往左找
            path.append('L')
            dfs(node.left)

            # 往右找
            path[-1] = 'R'  # 直接覆盖，无需恢复现场
            dfs(node.right)
            path.pop()  # 恢复现场

        dfs(root)

        i = 0
        while i < min(len(path_to_start), len(path_to_dest)) and path_to_start[i] == path_to_dest[i]:
            i += 1

        return 'U' * (len(path_to_start) - i) + ''.join(path_to_dest[i:])
'''
_L = CODE.strip('\n').split('\n')
RET_NONE = next(i + 1 for i, t in enumerate(_L) if t.strip() == 'return')


def nv(x):
    return '空' if x is None else str(x.val)


def _p(x):
    return '未找到' if x is None else ('`' + ''.join(x) + '`' if x else '`（空）`')


def _info(S):
    i = S['_inner']
    if 'path_to_start' not in S:
        return ''
    return f"到起点的路径 `path_to_start` = =={_p(S['path_to_start'])}==　　到终点的路径 `path_to_dest` = =={_p(S['path_to_dest'])}=="


def _hit(S, B, ret):
    n = S.node
    if n.val == S.startValue:
        return f'`{n.val}` 就是起点 `startValue` → 把当前路径 `path` 复制下来'
    return f'`{n.val}` 不是起点 → 再看是不是终点'


def _hit2(S, B, ret):
    n = S.node
    if n.val == S.destValue:
        return f'`{n.val}` 就是终点 `destValue` → 把当前路径 `path` 复制下来'
    return f'`{n.val}` 也不是终点 → 继续往下找'


def _cap_none(S, B, ret):
    if S.node is None:
        return '空节点 → 没得找，直接返回'
    return f'节点 `{S.node.val}` 非空 → 先看它是不是起点或终点'


CONFIG = dict(
    num=2096, title='从二叉树一个节点到另一个节点每一步的方向', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='一次 DFS 记录两条根路径 · 去掉公共前缀',
    tags=['难度分 1805'],
    code=CODE,
    call='''s = Solution()
s.tree = Tr([5,1,2,3,4])
s.getDirections(s.tree, 3, 4)''',
    expect='UR',
    views=[
        dict(type='tree', label='二叉树（蓝 = node；起点 3，终点 4）', pointers={'node': 'blue'}, h=250),
        dict(type='array', var='path', label='path（当前从根走到 node 的方向）', cell=64, h=130),
        dict(type='text', fn=_info, size=22, h=62),
        dict(type='calls', h=220),
    ],
    watch=[('node', lambda S: S['_inner']['node'].val if S['_inner'].get('node') is not None else None, 'blue'),
           ('i', 'i', 'yellow')],
    captions={
        'if node is None': _cap_none,
        RET_NONE: '空节点：回到上一层（这条路径没有更多东西了）',
        'if node.val == startValue': _hit,
        'elif node.val == destValue': _hit2,
        'path_to_start = path.copy()': '`path_to_start` = `{path_to_start}`：==根 → 起点== 的方向（要 `copy`，`path` 之后还会变）',
        'path_to_dest = path.copy()': '`path_to_dest` = `{path_to_dest}`：==根 → 终点== 的方向',
        'path.append': '往左走：`path` 末尾加 `L` → `{path}`',
        'dfs(node.left)': lambda S, B, r: f'递归左儿子 `{nv(B.node.left)}`',
        "path[-1] = 'R'": '左边搜完 → 把末尾的 `L` ==直接覆盖==成 `R` → `{path}`（不用先 pop 再 append）',
        'dfs(node.right)': lambda S, B, r: f'递归右儿子 `{nv(B.node.right)}`',
        'path.pop()': '左右都搜完 → ==恢复现场==：弹出末尾 → `{path}`，回到父节点',
        'dfs(root)': '从根开始，一次 DFS 同时找起点和终点',
        'i = 0': '`i` 统计两条路径的==公共前缀==长度',
        'while i < min': lambda S, B, r: (
            f'`path_to_start[{S.i}] = {S.path_to_start[S.i]}`，`path_to_dest[{S.i}] = {S.path_to_dest[S.i]}`：相同 → 还在公共路径上' if
            S.i < min(len(S.path_to_start), len(S.path_to_dest)) and S.path_to_start[S.i] == S.path_to_dest[S.i]
            else f'`i = {S.i}`：公共前缀到此为止，从这里开始分道扬镳 → 这个分叉点就是 ==最近公共祖先=='),
        'i += 1': '公共前缀再长一格：`i` → {i}',
        'return': lambda S, B, r: (f'起点要往上走 `{len(S.path_to_start)} - {S.i}` 步 → `U` × {len(S.path_to_start) - S.i}；'
                                   f'再接 `path_to_dest[{S.i}:]` = `{"".join(S.path_to_dest[S.i:])}` → ==`{r}`=='),
    },
    skip=['nonlocal'],
    cards=dict(
        one_liner='根到起点、根到终点两条路径：去掉公共前缀，起点那段全变 U',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二叉树节点值互不相同，给起点 `startValue` 和终点 `destValue`',
                 '返回起点到终点最短路径的每一步方向：`L` 左孩子、`R` 右孩子、`U` 父节点',
                 '示例：`[5,1,2,3,null,6,4]`，`3 → 6` → `"UURL"`',
                 '本视频：`[5,1,2,3,4]`，起点 `3`，终点 `4` → `"UR"`（两条根路径有公共前缀）'],
        quote='两条路径的最长公共前缀为 RR，然后分道扬镳。根据最近公共祖先的定义，分道扬镳的位置就是最近公共祖先。',
        quote_src='—— 灵茶山艾府题解',
        idea=['DFS 时用 `path` 记录==从根走到当前节点==的 `L/R` 序列',
              '遇到起点、终点就把 `path` 复制下来，得到两条根路径',
              '最长公共前缀结束的地方就是 lca；起点到 lca 全是 `U`，lca 到终点照抄终点路径剩下的部分',
              '回溯技巧：`L` 搜完直接覆盖成 `R`，只有最后才 `pop`'],
        result='运行结束，返回 `"UR"`：先上 1 步到 lca `1`，再 `R` 到 `4`',
        summary=['时间 `O(n)`，空间 `O(n)`（路径和递归栈）',
                 '易错：`path.copy()` 必须复制，否则后面 `path` 变了结果也变',
                 '起点到 lca 是向上走，所以长度是 `len(path_to_start) - i` 个 `U`',
                 '写法一是两次 DFS，每次只找一个目标，找到就提前返回；本视频演示一次 DFS 写法'],
    ),
)
