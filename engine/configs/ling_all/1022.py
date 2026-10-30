def _cap_leaf(S, B, ret):
    n = B.node
    if n is None:
        return '空节点 → 没有路径，直接返回'
    if n.left is None and n.right is None:
        return f'`{n.val}` 左右都空 → ==叶子==，路径值 `num = {B.num}` 就是一个二进制数'
    return f'`{n.val}` 不是叶子 → 继续往下递'


def _cap_num(S, B, ret):
    return f'`num = {B.num} << 1 | {B.node.val}` = =={S._inner.get("num")}==（左移一位腾出末位，再填上 `{B.node.val}`）'


CONFIG = dict(
    num=1022, title='从根到叶的二进制数之和', difficulty='Easy', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='自顶向下 DFS · 移位累加',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1462'],
    code='''
class Solution:
    def sumRootToLeaf(self, root: Optional[TreeNode]) -> int:
        # 从根到 node（不含）的路径值为 num
        def dfs(node: Optional[TreeNode], num: int) -> None:
            nonlocal ans
            if node is None:
                return
            num = num << 1 | node.val
            if node.left is None and node.right is None:
                ans += num
                return
            dfs(node.left, num)
            dfs(node.right, num)

        ans = 0
        dfs(root, 0)
        return ans
''',
    call='''s = Solution()
s.tree = Tr([1,0,1,0,1,0,1])
s.sumRootToLeaf(s.tree)''',
    expect=22,
    views=[
        dict(type='text', fn=lambda S: f"路径值 `num = {S['_inner'].get('num')}` = 二进制 `{bin(S['_inner'].get('num'))[2:]}`　累计 `ans = {S.get('ans')}`" if isinstance(S['_inner'].get('num'), int) and 'node' in S['_inner'] else '', size=26, h=56),
        dict(type='tree', label='二叉树（蓝 = node）', pointers={'node': 'blue'}, h=300),
        dict(type='calls', h=250),
    ],
    watch=[('node', lambda S: S['_inner'].get('node') and S['_inner']['node'].val, 'blue'),
           ('num', lambda S: S['_inner'].get('num'), 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '答案累加器 `ans` 先置 0',
        'dfs(root, 0)': '从根出发，路径值 `num` 从 0 开始',
        'if node is None': '进入 `dfs`：路径值 `num = {num}`',
        'return\n': '空节点，没有路径，返回',
        'num = num << 1': _cap_num,
        'if node.left is None and': _cap_leaf,
        'ans += num': '叶子：把整条路径的数加进答案 `ans = {B.ans} + {num}` = =={ans}==',
        'dfs(node.left': '带着当前 `num = {B.num}` 递归左子树',
        'dfs(node.right': '带着当前 `num = {B.num}` 递归右子树',
        'return ans': '所有叶子都累加完：`ans` = ==22==（4+5+6+7）',
    },
    skip=['nonlocal ans'],
    cards=dict(
        one_liner='和十进制拼数字一样：每下一层，num 左移一位再补当前位',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['二叉树每个节点值为 `0` 或 `1`，根到叶的路径是一个二进制数（根是最高位）',
                 '把所有叶子对应的数相加，返回总和',
                 '示例：`[1,0,1,0,1,0,1]` → `4+5+6+7 = 22`'],
        quote='每访问到一个新的节点 node，就把 num 更新成 num << 1 | node.val。如果 node 是叶子节点，把 num 加到答案中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['类比十进制：`0 → 1 → 12 → 123` 每步 `×10 + 位`；二进制就是 `×2 + 位`',
              '`×2` 等价于左移一位，`+` 可以写成或运算：`num << 1 | node.val`',
              '`num` 作为参数往下传：自顶向下 DFS，叶子处累加到 `ans`'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '先更新 `num` 再判断叶子：叶子本身的位也要算进去',
                 '写法二让 `dfs` 返回左右之和，不用 `nonlocal`；本视频演示写法一',
                 '`node is None` 要先判：单孩子节点会递归到空节点上'],
    ),
)
