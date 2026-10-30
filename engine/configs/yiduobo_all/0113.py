def _v(n):
    return 'None' if n is None else str(n.val)


def _info(S):
    if 'now_choose' not in S:
        return '回溯：边走边记路径，叶子处看值是否等于剩余的 s'
    return f"路径 `now_choose = {S['now_choose']}`，还需要凑 `s = {S['_inner'].get('s')}`"


def _cap_leaf(S, B, ret):
    n = S.now_node
    if not n.left and not n.right:
        return f'`{n.val}` 是==叶子== → 看它的值是否等于剩余的 `s = {S.s}`'
    return f'`{n.val}` 不是叶子 → 加入路径，继续往下搜'


def _cap_eq(S, B, ret):
    n = S.now_node
    if n.val == S.s:
        return f'叶子值 `{n.val}` == 剩余 `s = {S.s}` → ==找到一组解=='
    return f'叶子值 `{n.val}` ≠ 剩余 `s = {S.s}` → 这条路不行'


def _cap_child(side, word):
    def f(S, B, ret):
        ch = getattr(B.now_node, side)
        if ch is not None:
            return f'`{B.now_node.val}` 有{word}儿子 `{ch.val}` → 往{word}搜，带着 `s = {B.s}`'
        return f'`{B.now_node.val}` 没有{word}儿子 → 跳过'
    return f


CONFIG = dict(
    num=113, title='路径总和 II', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='搜索回溯',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def pathSum(self, root, sum):

        res = []
        self.dfs(root, sum, [], res)
        return res

    def dfs(self, now_node, s, now_choose, res):
        if not now_node:
            return
        if not now_node.left and not now_node.right:
            if now_node.val == s:
                res.append(now_choose[:] + [now_node.val])
        else:
            now_choose.append(now_node.val)
            s -= now_node.val
            if now_node.left:
                self.dfs(now_node.left, s, now_choose, res)
            if now_node.right:
                self.dfs(now_node.right, s, now_choose, res)
            s += now_node.val
            now_choose.pop()
''',
    call='Solution().pathSum(Tr([5,4,8,11,None,13,4,7,2,None,None,5]), 22)',
    expect=[[5, 4, 11, 2], [5, 8, 4, 5]],
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='tree', label='二叉树（蓝 = now_node）', pointers={'now_node': 'blue'}, h=300),
        dict(type='array', var='now_choose', label='now_choose（当前路径）', cell=72, h=150),
        dict(type='text', fn=lambda S: f"找到的路径 `res = {S['res']}`" if 'res' in S else '', size=26, h=56),
        dict(type='calls', h=200, hide=('res', 'now_choose')),
    ],
    watch=[('now_node', 'now_node.val', 'blue'), ('s', lambda S: S['_inner'].get('s'), 'yellow')],
    captions={
        'res = []': '`res` 收集所有满足条件的路径',
        'self.dfs(root, sum': '从根出发：`s = {sum}` 是还需要凑的和，`now_choose` 记录走过的节点',
        'if not now_node.left and not now_node.right': _cap_leaf,
        'if now_node.val == s': _cap_eq,
        'res.append': '路径 + 叶子 = `{res[-1]}`，==复制一份==记进 `res`',
        'now_choose.append': '`{now_node.val}` 加入路径 → `{now_choose}`',
        's -= now_node.val': '`s = {B.s} - {now_node.val} = {s}`：下面的节点还需要凑 =={s}==',
        'if now_node.left:': _cap_child('left', '左'),
        'if now_node.right:': _cap_child('right', '右'),
        'self.dfs(now_node.left': lambda S, B, r: f'进入左儿子 `{_v(S.now_node)}`',
        'self.dfs(now_node.right': lambda S, B, r: f'进入右儿子 `{_v(S.now_node)}`',
        's += now_node.val': '左右都搜完 → ==回溯==：`s` 加回 `{now_node.val}` = `{s}`',
        'now_choose.pop()': '`{B.now_choose[-1]}` 移出路径 → `{now_choose}`，回到上一层',
        'return res': '全部搜完，共 `{len(res)}` 条路径：`{res}`',
    },
    skip=['if not now_node:'],
    max_steps=120,
    cards=dict(
        one_liner='搜索回溯：边走边减 s，叶子的值恰好等于剩余的 s 就是一条解',
        complexity='时间 `O(n^2)`（复制路径），空间 `O(n)`',
        problem=['给你二叉树的根 `root` 和整数 `targetSum`',
                 '找出所有==根到叶子==、节点值之和等于 `targetSum` 的路径',
                 '本视频：`[5,4,8,11,null,13,4,7,2,null,null,5]`，`targetSum = 22`',
                 '答案：`[[5,4,11,2],[5,8,4,5]]`'],
        quote='每次尝试往左子树或者右子树走，同时修改此时的sum。==如果当前节点是叶子结点，那么判断该节点的值是否等于现在的sum==，如果是，说明找到了一组解，将其记录下来即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['非叶子：入路径、`s` 减去自己，再搜左右儿子',
              '搜完把 `s` 加回、节点出路径，这就是回溯',
              '叶子：不入栈，直接比较 `now_node.val == s`，相等就把路径加上叶子存进 `res`'],
        summary=['时间 `O(n^2)` 最坏（每条解要复制路径），空间 `O(n)`',
                 '`now_choose` 是共享列表：==搜完必须 pop==；存答案要 `[:]` 复制，否则被后续修改',
                 '`s` 是参数、每层一份，`s += now_node.val` 其实可省略',
                 '原文代码可直接在 Python 3 运行，一字未改'],
    ),
)
