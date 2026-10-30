TREE = [5, 3, 8, 2, 4, 7]
LEVEL = [v for v in TREE if v is not None]          # Tr() 按层序给节点编号，uid 差 = 层序下标
DESC = sorted(LEVEL, reverse=True)
CUM = [sum(DESC[:k + 1]) for k in range(len(DESC))]

CODE = '''
class Solution(object):
    def convertBST(self, root):
        if not root:
            return root

        self.dfs(root, 0)
        return root

    def dfs(self, now, delta):
        if now.right:
            delta = self.dfs(now.right, delta)
        now.val += delta
        delta = now.val
        if now.left:
            delta = self.dfs(now.left, delta)
        return delta
'''
_LINES = CODE.strip('\n').split('\n')
L_PLUS = [k + 1 for k, t in enumerate(_LINES) if 'now.val += delta' in t][0]


def _orig(S, nd):
    return LEVEL[nd._uid - S['root']._uid]


def _all_nodes(root):
    out, st = [], [root]
    while st:
        x = st.pop()
        if x is not None:
            out.append(x)
            st += [x.left, x.right]
    return out


def _done_k(S):
    if 'root' not in S:
        return 0
    k = sum(1 for nd in _all_nodes(S['root']) if nd.val != _orig(S, nd))
    if k:
        return k + 1  # 最大的节点加的是 0，值不变，但它一定最先处理
    nd = S.get('now')
    if nd is not None and _orig(S, nd) == DESC[0] and S.get('_line', 0) >= L_PLUS:
        return 1
    return 0


def _color(S, nd):
    if 'root' not in S:
        return None
    return 'green' if _orig(S, nd) in DESC[:_done_k(S)] else None


CONFIG = dict(
    num=538, title='把二叉搜索树转换为累加树', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='递归返回右侧累加和 delta',
    tags=['热题173'],
    code=CODE,
    call=f'Solution().convertBST(Tr({TREE}))',
    result_fn=tree_list,
    expect=[20, 27, 8, 29, 24, 15],
    skip=['if not root'],
    views=[
        dict(type='text', fn=lambda S: (f"`delta = {S['delta']}`：当前节点==右侧==（所有更大的节点）的累加和"
                                        if 'delta' in S else ''), h=60),
        dict(type='tree', label='BST（绿 = 已加上右侧累加和）', h=330,
             pointers={'now': 'blue'}, color=_color),
        dict(type='calls', h=150, hide=('self',)),
        dict(type='array', var=lambda S: DESC, label='处理顺序：先右后左 = 原值从大到小', cell=76, h=120,
             color=lambda S, i, v: 'green' if i < _done_k(S) else None),
    ],
    watch=[('delta', 'delta', 'green')],
    captions={
        'self.dfs(root, 0)': '从根开始，根的右侧还没有任何更大的数：`delta = 0`',
        'if now.right': lambda S, B, r: (f'`{B.now.val}` 有右子树（都比它大）→ ==先递归右边==，拿回右侧累加和' if B.now.right
                                         else f'`{B.now.val}` 没有右子树 → 右侧累加和就是传进来的 `delta = {B.delta}`'),
        'delta = self.dfs(now.right, delta)': lambda S, B, r: f'递归右子树 `{B.now.right.val}`，把 `delta = {B.delta}` 带下去',
        'now.val += delta': lambda S, B, r: f'当前节点加上右侧累加和：`{B.now.val} + {B.delta}` = =={S.now.val}==',
        'delta = now.val': '更新 `delta = {delta}`：这就是左子树节点的「右侧累加和」',
        'if now.left': lambda S, B, r: (f'有左子树 → 把 `delta = {B.delta}` ==带到左子树的递归==中' if B.now.left
                                        else '没有左子树'),
        'delta = self.dfs(now.left, delta)': lambda S, B, r: f'递归左子树 `{B.now.left.val}`',
        'return delta': lambda S, B, r: f'以（原值）`{_orig(S, S.now)}` 为根的子树处理完：返回累加和 `{r}` 给上一层',
        'return root': '每个节点都加上了比它大的所有数，返回 `root`',
    },
    cards=dict(
        result='累加树：`[20,27,8,29,24,15]` ✓',
        one_liner='先递归右子树拿到右侧累加和，加到自己身上，再带进左子树',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['给二叉==搜索==树的根，节点值各不相同',
                 '每个节点的新值 = ==原值 + 所有比它大的节点值之和==',
                 '示例：`[0,null,1]` → `[1,null,1]`；`[1,0,2]` → `[3,3,2]`',
                 '本视频：`[5,3,8,2,4,7]` → `[20,27,8,29,24,15]`'],
        quote='优先递归求解右子树，==返回整个右子树的累加和==，然后将这个累加和加到当前节点上，再==将加上累加和之后的当前节点值带到左子树的递归当中==即可。',
        quote_src='—— yiduobo 题解原文（delta 表示当前节点右侧的累加和）',
        idea=['数组的做法：排序后从大到小累加；BST 本身就有序',
              '右子树的值都更大 → 先递归右边，返回值 `delta` 是右侧累加和',
              '`now.val += delta` 后，`now.val` 又是左子树的右侧累加和'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '用参数 + 返回值传递 `delta`，不需要全局变量',
                 '易错：递归右子树要用它的==返回值==更新 delta',
                 '对比灵神：灵神用 `nonlocal s` 全局累加，并且递归到空节点；这里先判断孩子再递归',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
