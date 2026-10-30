DESC = [[20, 15, 1], [20, 17, 0], [50, 20, 1], [50, 80, 0], [80, 19, 1]]


def _lr(n):
    return f"L={n.left.val if n.left else '-'} R={n.right.val if n.right else '-'}"


def _cur(S, i, v):
    I = S['_inner']
    if 'x' in I and 'y' in I and v[0] == I['x'] and v[1] == I['y']:
        return 'yellow'
    return None


def _size(n):
    return 1 + (_size(n.left) if n.left else 0) + (_size(n.right) if n.right else 0)


def _big(S):
    nd = S.get('nodes') or {}
    ks = list(nd.values())
    kids = {id(c) for n in ks for c in (n.left, n.right) if c}
    roots = [n for n in ks if id(n) not in kids]
    return max(roots, key=_size) if roots else None


def _edges(S):
    I = S['_inner']
    out = []
    for d in DESC:
        t = f'[{d[0]},{d[1]},{d[2]}]'
        out.append(f'=={t}==' if I.get('x') == d[0] and I.get('y') == d[1] else f'`{t}`')
    return 'descriptions：' + ' '.join(out)


def _xor(S):
    I = S['_inner']
    return f"异或和 `root = {I['root']}`" + ('，恰好是根节点的值' if S.get('_line') == 21 else '：每个值进入 nodes 时异或一次，作为儿子时再异或一次')


CONFIG = dict(
    num=2196, title='根据描述创建二叉树', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='哈希表 + 异或找根',
    tags=['链表树与回溯', '二叉树', '难度分 1644'],
    code='''
class Solution:
    def createBinaryTree(self, descriptions: List[List[int]]) -> Optional[TreeNode]:
        nodes = {}  # val -> TreeNode
        root = 0

        for x, y, is_left in descriptions:
            if x not in nodes:
                nodes[x] = TreeNode(x)
                root ^= x
            if y not in nodes:
                nodes[y] = TreeNode(y)
                root ^= y
            if is_left:
                nodes[x].left = nodes[y]
            else:
                nodes[x].right = nodes[y]
            root ^= y

        return nodes[root]
''',
    call='''s = Solution()
s.descs = ''' + repr(DESC) + '''
tree_list(s.createBinaryTree(s.descs))''',
    expect=[50, 20, 80, 15, 17, 19],
    views=[
        dict(type='text', fn=_edges, size=26, h=70),
        dict(type='map', var='nodes', label='nodes：值 → 节点（黄 = 刚创建 / 刚改动）', fmt=lambda k, v: f'{k} → {_lr(v)}', h=210),
        dict(type='text', fn=_xor, size=24, h=50),
        dict(type='tree', var=_big, label='已连好的最大子树', h=230),
    ],
    watch=[('x', lambda S: S['_inner'].get('x'), 'blue'), ('y', lambda S: S['_inner'].get('y'), 'pink'), ('is_left', lambda S: S['_inner'].get('is_left')), ('root', 'root', 'green')],
    captions={
        'nodes = {}': '`nodes` 记录「节点值 → TreeNode」：题目给的是整数，==要自己建节点==，并能按值找回来',
        'root = 0': '`root` 用来异或：每个值进入 `nodes` 异或一次，作为儿子再异或一次',
        'for x, y, is_left': '{"取一条边：父 `x = " + str(x) + "`，子 `y = " + str(y) + "`，`is_left = " + str(is_left) + "`" if not (B.get("y") == y and B.get("x") == x) else "所有边处理完，循环结束"}',
        'if x not in nodes': '父节点 `{x}` {"之前没建过" if x not in nodes else "已经建过"} → {"现在创建" if x not in nodes else "直接复用"}',
        'nodes[x] = TreeNode(x)': '创建父节点 `{x}`',
        'if y not in nodes': '子节点 `{y}` {"之前没建过 → 创建" if y not in nodes else "已经建过 → 复用"}',
        'nodes[y] = TreeNode(y)': '创建子节点 `{y}`',
        'if is_left:': '`is_left = {is_left}` → 连到 {"左" if is_left else "右"}边',
        'nodes[x].left = nodes[y]': '把 `{y}` 接到 `{x}` 的==左==儿子',
        'nodes[x].right = nodes[y]': '把 `{y}` 接到 `{x}` 的==右==儿子',
        9: '`{x}` 第一次出现：`root ^= {x}` → `root = {root}`',
        12: '`{y}` 第一次出现：`root ^= {y}` → `root = {B.root} ^ {y} = {root}`',
        17: '`{y}` 当了儿子，再异或一次：`root = {B.root} ^ {y} = {root}`，==出现两次的值抵消==',
        'return nodes[root]': lambda S, B, r: f'只有根没当过儿子，只异或了一次，其余值都抵消 → `root = {S.root}` 就是根，返回 `nodes[{S.root}]`',
    },
    cards=dict(
        one_liner='哈希表按值找节点，异或抵消掉所有当过儿子的值，剩下的就是根',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`descriptions[i] = [parent, child, isLeft]`：`parent` 是 `child` 的父节点，`isLeft = 1` 为左儿子',
                 '节点值互不相同，构造二叉树并返回==根节点==',
                 '本视频：`[[20,15,1],[20,17,0],[50,20,1],[50,80,0],[80,19,1]]` → `[50,20,80,15,17,19]`'],
        quote='用一个哈希集合 children 记录哪些节点值有父节点。……优化：把树上每个值异或一遍，再把所有儿子异或一遍。由于同一个值异或两次等于 0，所以最终异或和恰好等于根节点的值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['题目给整数不给节点：用 `nodes: val → TreeNode`，第一次见到才创建',
              '根 = 从未当过儿子的值。优化前用集合 `children`，遍历 `nodes` 找',
              '优化：每个值先在创建时异或一次，每次当儿子再异或一次；除了根，其余值都被异或偶数次 → 0'],
        summary=['时间 `O(n)`，空间 `O(n)`（`n` 是 `descriptions` 的长度）',
                 '本视频演示的是优化写法（异或）；优化前写法：用集合 `children` 记录有父节点的值，再遍历 `nodes` 找不在其中的',
                 '易错：创建节点和 `root ^= 值` 要放在 `not in nodes` 里面，==每个值只异或一次==；`root ^= y` 在每条边都做',
                 '异或技巧同 136 题「只出现一次的数字」'],
    ),
)
