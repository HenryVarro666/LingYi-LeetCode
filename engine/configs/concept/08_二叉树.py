def _formula(S):
    nd = S.get('node')
    if nd is not None and 'l' in S and 'r' in S:
        return (f"节点 =={nd.val}==：拐弯路径 `l + r = {S['l'] + S['r']}`，"
                f"返回链长 `max(l, r) + 1 = {max(S['l'], S['r']) + 1}`")
    if nd is not None and 'l' in S:
        return f"节点 {nd.val}：左子树深度 `l = {S['l']}` 已经拿到，再问右子树"
    if 'node' in S and nd is None:
        return '空节点：递归边界，深度 0'
    if nd is not None:
        return f'节点 {nd.val}：先问左子树有多深'
    return '后序遍历：==先算左右子树，再算自己=='


def _ret_cap(S, B, ret):
    return (f'归：节点 `{S.node.val}` 返回 `max({S.l}, {S.r}) + 1 = {ret}`'
            + ('——==返回的是链长，不是直径==' if S.node.val == 2 else ''))


CONFIG = dict(
    num=None, title='二叉树 · 通用思想与模板', author='概念讲解', category='二叉树',
    technique='通用思想与模板', kind='concept', difficulty='',
    code='''
def diameter(root):                # 543. 二叉树的直径
    ans = 0
    def dfs(node):                 # 返回 node 子树的最大深度（链长）
        nonlocal ans
        if node is None:           # 递归边界：空树深度为 0
            return 0
        l = dfs(node.left)         # 相信它能算对左子树
        r = dfs(node.right)        # 相信它能算对右子树
        ans = max(ans, l + r)      # 在 node 拐弯的路径长 l + r
        return max(l, r) + 1       # 后序：左右都算完，才算自己
    dfs(root)
    return ans
''',
    call='diameter(Tr([1, 2, 3, 4, 5]))',
    expect=3,
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='tree', label='二叉树（黄圈 = 递归路径，蓝框 = 当前节点）', pointers={'node': 'blue'}, h=330),
        dict(type='calls', label='递归调用栈', h=220),
    ],
    watch=[('node', 'node.val if node else None', 'blue'), ('l', 'l'), ('r', 'r'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 记录最长路径（边数）；真正的工作交给递归函数 `dfs`',
        'if node is None': lambda S, B, ret: ('`node` 是空节点 → 到达递归边界' if S.node is None
                                              else f'节点 `{S.node.val}` 不为空，继续往下'),
        'return 0': '空树深度为 0，直接返回',
        'l = dfs(node.left)': lambda S, B, ret: (f'递：问节点 `{B.node.val}` 的左子树有多深——==假设它返回的一定是对的=='
                                                 if B.node.val == 1 else f'递：问节点 `{B.node.val}` 的左子树有多深'),
        'r = dfs(node.right)': lambda S, B, ret: f'左子树深度 `l = {B.l}`；递：再问节点 `{B.node.val}` 的右子树',
        'ans = max(ans, l + r)': '在节点 `{node.val}` 拐弯：`l + r = {l + r}`，`ans = max({B.ans}, {l + r}) = {ans}`',
        'return max(l, r) + 1': _ret_cap,
        'dfs(root)': '从根节点开始递归',
        'return ans': '答案 `{ret}`：每个节点只访问一次，时间 `O(n)`',
    },
    cards=dict(
        one_liner='把问题交给左右子树，相信递归能算对，再在当前节点合并',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈，h 为树高）',
        problem_heading='什么时候用？',
        problem=['答案能由「左子树结果 + 右子树结果」拼出来 → 后序递归',
                 '要从上往下传信息（深度、上下界、路径和）→ 递归参数',
                 '二叉搜索树 → 中序遍历就是有序数组',
                 '按层处理（层序遍历、右视图）→ BFS 队列'],
        before=[dict(heading='核心概念：递归 = 数学归纳法', lines=[
            '先定义 `dfs(node)` ==返回什么==：深度、链长、是否合法……',
            '写好边界（空节点），然后相信 `dfs(node.left)` 已经算对',
            '后序：拿到左右结果再算自己——深度、直径、最大路径和',
            '前序传参：带着上下界 / 当前深度 / 路径和往下走']),
        ],
        idea_heading='两位作者怎么说',
        quote='我在网上看到一种理解递归的说法：「在写递归函数时，==可以假设递归返回的结果一定是正确的==」。其实这种说法本质上就是数学归纳法。',
        quote_src='—— 灵茶山艾府 · 104. 二叉树的最大深度',
        idea=['yiduobo 543：直径 = 某子树根 + 左边最长路径 + 右边最长路径',
              '灵神 543：`dfs` 返回 ==链== 的长度而不是直径；124 同理（树形 DP）',
              '灵神 98 比较前中后序：==后序（自底向上）最通用==，学 DP 必须掌握'],
        after=[dict(heading='本类 Hot100 题目 & 学习顺序（1/2）', chapter='④ 小结', lines=[
            '`94` 中序遍历：左 → 根 → 右',
            '`104` 最大深度：`max(l, r) + 1`',
            '`226` 翻转二叉树：交换左右，递归',
            '`101` 对称二叉树：两棵子树同步递归',
            '`543` 直径：返回链长，`l + r` 更新答案',
            '`102` 层序遍历：BFS 队列',
            '`108` 有序数组转 BST：中点当根',
            '`98` 验证 BST：传上下界 / 中序递增'])],
        summary_heading='本类 Hot100 题目 & 学习顺序（2/2）',
        summary=['`230` BST 第 K 小：中序第 k 个',
                 '`199` 右视图：每层最后一个',
                 '`114` 展开为链表：后序 / 头插',
                 '`105` 构造二叉树：前序定根，中序分左右',
                 '`437` 路径总和 III：树上的前缀和',
                 '`236` 最近公共祖先：左右都找到即答案',
                 '`124` 最大路径和：同 543，负链取 0',
                 '易错：返回「链」不是「直径」；BST 严格递增'],
    ),
)
