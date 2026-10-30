def _vals(S):
    I = S['_inner']
    if 'node_list' in I:
        return [n.val for n in I['node_list']]
    if 'l_list' in I:
        return [n.val for n in I['l_list']] + [I['now'].val] + [n.val for n in I['r_list']]
    return []


_LONE = {}


def _tree_var(S):
    I = S['_inner']
    if 'node_list' in I and 'now' in I:
        if S.get('_line') == 27 or len(I['node_list']) == 4:
            return I['now']
        v = I['now'].val
        if v not in _LONE:
            _LONE[v] = TreeNode(v)  # 只画当前根这一个点，子树返回后再整棵显示
        return _LONE[v]
    return S.get('self.tree')


CONFIG = dict(
    num=1382, title='将二叉搜索树变平衡', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='中序遍历 + 取中点递归建树',
    tags=['链表树与回溯', '二叉树'],
    code='''
class Solution(object):
    def balanceBST(self, root):
        node_list = self.dfs(root)
        return self.build(node_list)

    def dfs(self, now):
        l_list = []
        r_list = []
        if now.left:
            l_list = self.dfs(now.left)
        if now.right:
            r_list = self.dfs(now.right)
        return l_list + [now] + r_list

    def build(self, node_list):
        mid = len(node_list) // 2
        now = node_list[mid]
        if mid > 0:
            now.left = self.build(node_list[:mid])
        else:
            now.left = None
        if mid < len(node_list) - 1:
            now.right = self.build(node_list[mid + 1:])
        else:
            now.right = None

        return now
''',
    call='''s = Solution()
s.tree = Tr([1, None, 2, None, 3, None, 4])
tree_list(s.balanceBST(s.tree))''',
    expect=[3, 2, 4, 1],
    views=[
        dict(type='text', fn=lambda S: ('`node_list` = 中序遍历得到的节点（按值从小到大），取中间那个当根' if 'node_list' in S['_inner'] else '中序遍历：左子树列表 + 自己 + 右子树列表'), size=24, h=56),
        dict(type='tree', var=_tree_var, label='二叉树（先是原 BST；建树阶段只画 now，子树返回后显示完整子树）', pointers={'now': 'blue'}, path=False, h=230),
        dict(type='array', var=_vals, label='当前列表的节点值（node_list / 中序合并结果）', pointers={'mid': 'orange'}, cell=72, h=165),
        dict(type='calls', h=170, hide=('node_list',)),
    ],
    watch=[('now', lambda S: getattr(S['_inner'].get('now'), 'val', None), 'blue'), ('mid', lambda S: S['_inner'].get('mid'), 'orange'), ('l_list', lambda S: [n.val for n in S['_inner']['l_list']] if 'l_list' in S['_inner'] else None), ('r_list', lambda S: [n.val for n in S['_inner']['r_list']] if 'r_list' in S['_inner'] else None)],
    captions={
        'node_list = self.dfs(root)': '先中序遍历：BST 的中序结果==按节点值从小到大排好==',
        'l_list = []': '`l_list`、`r_list` 分别装左、右子树的中序结果，先都置空',
        'if now.left:': '节点 `{now.val}`：{"有左儿子，先去收集左子树" if now.left else "没有左儿子，l_list 保持为空"}',
        'l_list = self.dfs': '递归收集左子树 `dfs({B.now.left.val})`，结果存进 `l_list`',
        'if now.right:': '节点 `{now.val}`：{"有右儿子，再去收集右子树" if now.right else "没有右儿子，r_list 保持为空"}',
        'r_list = self.dfs': '递归收集右子树 `dfs({B.now.right.val})`，结果存进 `r_list`',
        'return l_list + [now] + r_list': lambda S, B, r: f'左 + 根 + 右 = 中序：节点值 `{[n.val for n in r]}`，递增',
        'return self.build(node_list)': '拿到有序节点列表，开始取中点建树',
        'mid = len(node_list) // 2': '列表长 `{len(node_list)}`，`mid = {len(node_list)} // 2` = =={mid}==：取中间当根，==左右两边数量最多差 1==',
        'now = node_list[mid]': '`node_list[{mid}]` 节点 `{now.val}` 作为这棵子树的==根==（复用原节点，重新连边）',
        'if mid > 0:': '`mid = {mid}`：{"左边还有节点 → 用前半部分递归建左子树" if mid > 0 else "左边没有节点 → 左子树为空"}',
        'now.left = self.build': '左子树：用前半 `node_list[:{B.mid}]`（{B.mid} 个节点）递归构造，==返回值接到 now.left 上==',
        'now.left = None': '左边没有节点 → `now.left = None`（==要显式清空==，否则还连着旧的儿子）',
        'if mid < len(node_list) - 1:': '`mid = {mid}`，列表长 `{len(node_list)}`：{"右边还有节点 → 用后半部分递归建右子树" if mid < len(node_list) - 1 else "右边没有节点 → 右子树为空"}',
        'now.right = self.build': '右子树：用后半 `node_list[{B.mid + 1}:]`（{len(B.node_list) - B.mid - 1} 个节点）递归构造，==返回值接到 now.right 上==',
        'now.right = None': '右边没有节点 → `now.right = None`（同样要清空旧指针）',
        'return now': lambda S, B, r: f'以 `{r.val}` 为根的平衡子树建好，返回上一层',
    },
    skip=['r_list = []'],
    cards=dict(
        one_liner='不旋转，直接「粗暴」重建：中序遍历后取中点当根',
        complexity='时间 `O(n log n)`（切片复制），空间 `O(n)`',
        problem=['给你一棵二叉搜索树，返回一棵节点值相同的==平衡== BST',
                 '平衡：每个节点两棵子树的高度差不超过 `1`',
                 '本视频：`[1,null,2,null,3,null,4]`（一条链）→ `[3,2,4,1]`'],
        quote='比较高级的做法应该是根据当前树的形态执行各种旋转操作，我在这里采用的是比较粗暴的做法。先执行一趟中序遍历，那么此时遍历结果就是按照节点值从小到大排列的。',
        quote_src='—— yiduobo 知乎题解',
        idea=['放弃旋转：先 `dfs` 中序遍历，把==节点本身==（不是值）按顺序收进列表',
              '`build`：选正中间的节点作根，前半部分建左子树，后半部分建右子树',
              '每层左右数量最多差 1 → 必然平衡'],
        summary=['时间：切片每层复制 `O(n)`，共 `O(log n)` 层 → `O(n log n)`；空间 `O(n)`',
                 '直接复用原节点，所以 `left` / `right` ==必须都重新赋值==（含置 None）',
                 '边界：`mid > 0` 才有左子树，`mid < len - 1` 才有右子树',
                 '原文为 Python 2 写法，`len(node_list) / 2` 的整数除法已改为 `//`；删去了函数开头的空白行'],
    ),
)
