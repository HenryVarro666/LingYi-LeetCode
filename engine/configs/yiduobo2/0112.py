def _v(n):
    return 'None' if n is None else str(n.val)


def _info(S):
    if 'now_choose' not in S:
        return '113 题的回溯：走到叶子时，==叶子的值 == 剩余的 s== 就是一条解'
    return f"路径 `now_choose = {S['now_choose']}`，还需要凑 `s = {S['_inner'].get('s')}`"


def _cap_leaf(S, B, ret):
    n = S.now_node
    if not n.left and not n.right:
        return f'`{n.val}` 是==叶子== → 看它的值是否等于剩余的 `s = {S.s}`'
    return f'`{n.val}` 不是叶子 → 把它加入路径，继续往下搜'


def _cap_eq(S, B, ret):
    n = S.now_node
    if n.val == S.s:
        return f'叶子值 `{n.val}` == 剩余 `s = {S.s}` → ==找到一组解=='
    return f'叶子值 `{n.val}` ≠ 剩余 `s = {S.s}` → 这条路不行'


def _cap_if_child(side, word):
    def f(S, B, ret):
        ch = getattr(B.now_node, side)
        if ch is not None:
            return f'`{B.now_node.val}` 有{word}儿子 `{ch.val}` → 往{word}搜，带着 `s = {B.s}`'
        return f'`{B.now_node.val}` 没有{word}儿子 → 跳过'
    return f


CONFIG = dict(
    num=112, title='路径总和', difficulty='Easy', category='二叉树',
    author='yiduobo', technique='搜索回溯（原文给的是 113 题代码）',
    tags=['字节30天', '热题173', '面试经典150'],
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
    call='len(Solution().pathSum(Tr([5,4,8,11,None,13,4]), 26)) > 0',
    expect=True,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='tree', label='二叉树（蓝 = now_node）', pointers={'now_node': 'blue'}, h=300),
        dict(type='array', var='now_choose', label='now_choose（当前路径）', cell=72, h=120),
        dict(type='text', fn=lambda S: f"找到的路径 `res = {S['res']}`" if 'res' in S else '', size=26, h=56),
        dict(type='calls', h=200, hide=('res', 'now_choose')),
    ],
    watch=[('now_node', 'now_node.val', 'blue'), ('s', lambda S: S['_inner'].get('s'), 'yellow')],
    captions={
        'res = []': '`res` 收集所有满足条件的路径；==112 只需判断它是否非空==',
        'self.dfs(root, sum': '从根出发：`s = {sum}` 是还需要凑的和，`now_choose` 记录走过的节点',
        'if not now_node.left and not now_node.right': _cap_leaf,
        'if now_node.val == s': _cap_eq,
        'res.append': '路径 + 叶子 = `{res[-1]}`，复制一份记进 `res`',
        'now_choose.append': '`{now_node.val}` 加入路径 → `{now_choose}`',
        's -= now_node.val': '`s = {B.s} - {now_node.val} = =={s}==`：下面的节点还需要凑 `{s}`',
        'if now_node.left:': _cap_if_child('left', '左'),
        'if now_node.right:': _cap_if_child('right', '右'),
        'self.dfs(now_node.left': lambda S, B, r: f'进入左儿子 `{_v(S.now_node)}`',
        'self.dfs(now_node.right': lambda S, B, r: f'进入右儿子 `{_v(S.now_node)}`',
        's += now_node.val': '`{now_node.val}` 的左右都搜完了 → ==回溯==：`s` 加回来 = `{s}`',
        'now_choose.pop()': '`{B.now_choose[-1]}` 移出路径 → `{now_choose}`，回到上一层',
        'return res': lambda S, B, r: f'`res = {r}` 非空 → 112 的答案是 ==True==',
    },
    skip=['if not now_node:'],
    cards=dict(
        one_liner='搜索回溯：边走边减 s，叶子的值恰好等于剩余的 s 就是一条解',
        complexity='时间 `O(n)`（不算复制路径），空间 `O(n)`',
        problem=['给你二叉树的根 `root` 和整数 `targetSum`',
                 '判断是否存在==根节点到叶子节点==的路径，路径上节点值之和等于 `targetSum`',
                 '本视频：`root = [5,4,8,11,null,13,4]`，`targetSum = 26`',
                 '`5 + 8 + 13 = 26` → `true`'],
        quote='两个问题都是用搜索回溯来解决，每次尝试往左子树或者右子树走，同时修改此时的sum。==如果当前节点是叶子结点，那么判断该节点的值是否等于现在的sum==。',
        quote_src='—— yiduobo 知乎题解（112 & 113 合写）',
        idea=['原文只给了 ==113 题（找出所有路径）== 的代码：112 的答案就是 `res` 是否非空',
              '非叶子：入路径、`s` 减去自己，再搜左右儿子；搜完把 `s` 加回、出路径（回溯）',
              '叶子：不减，直接比较 `now_node.val == s`'],
        result='`res = [[5, 8, 13]]` 非空 → 返回 `True` ✓',
        summary=['时间 `O(n)`（113 还要算上复制路径的开销），空间 `O(n)`',
                 '对比灵神：灵神先减再判 `== 0`；yiduobo 在叶子处判 `val == s`，两者等价',
                 '`s` 是参数（每层一份），`s += now_node.val` 其实可以省略；`now_choose` 是共享列表，==必须 pop==',
                 '112 只要一个答案，可以找到就返回提前结束；113 要全部搜完',
                 '原文为 Python 2 风格：删去了文档字符串和模板注释；用 `len(res) > 0` 得到 112 的答案'],
    ),
)
