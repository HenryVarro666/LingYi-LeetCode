CONFIG = dict(
    num=270, title='最接近的二叉搜索树值', difficulty='Easy', category='二叉树与回溯',
    author='yiduobo', technique='沿 BST 向下查找 · 途中更新答案',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def closestValue(self, root, target):

        now = root
        res = None

        while now:
            if res is None or abs(res - target) > abs(now.val - target):
                res = now.val
            
            if now.val > target:
                now = now.left
            else:
                now = now.right
        
        return res
''',
    call='Solution().closestValue(Tr([8,4,12,2,6,10,14,1,3,5,7]), 5.3)',
    expect=5,
    views=[
        dict(type='tree', var='root', pointers={'now': 'blue'}, path=False, h=420,
             color=lambda S, n: 'green' if S.get('res') is not None and n.val == S['res'] else None),
        dict(type='text', h=70, fn=lambda S: (f"`target = {S['target']}`，当前最接近 `res = {S['res']}`，差 `{abs(S['res'] - S['target']):.1f}`" if S.get('res') is not None else f"`target = {S['target']}`，还没有候选答案")),
    ],
    watch=[('target', 'target', 'orange'), ('now', 'now.val if now else None', 'blue'), ('res', 'res', 'green')],
    captions={
        'now = root': '从根节点出发，像普通 BST 查找一样往下走',
        'res = None': '`res` 记录目前见过的最接近 target 的节点值，先置空',
        'while now': lambda S, B, r: (f'`now = {S.now.val}`，还有节点 → 继续' if S.now else '走到空节点（越过叶子）→ 查找结束'),
        'abs(res - target)': lambda S, B, r: (f'`res` 还是空 → 第一个节点直接成为候选，进入赋值' if S.res is None else
            (f'`|{S.res} − {S.target}| = {abs(S.res - S.target):.1f}` > `|{S.now.val} − {S.target}| = {abs(S.now.val - S.target):.1f}` → 当前节点更近，==要更新 res==' if abs(S.res - S.target) > abs(S.now.val - S.target) else
             f'`|{S.res} − {S.target}| = {abs(S.res - S.target):.1f}` ≤ `|{S.now.val} − {S.target}| = {abs(S.now.val - S.target):.1f}` → 旧答案更近，不更新')),
        'res = now.val': '`res = {res}`：沿途每个节点都当一次候选',
        'if now.val > target': lambda S, B, r: (f'`{S.now.val} > {S.target}`：节点偏大，更近的值只可能在==左子树==' if S.now.val > S.target
                                              else f'`{S.now.val} ≤ {S.target}`：节点偏小，更近的值只可能在==右子树=='),
        'now = now.left': lambda S, B, r: '往左走' + (f'，到 `{S.now.val}`' if S.now else '，左边是空 → 到头了'),
        'now = now.right': lambda S, B, r: '往右走' + (f'，到 `{S.now.val}`' if S.now else '，右边是空 → 到头了'),
        'return res': '返回 `res = {res}`：路径上离 `{target}` 最近的节点值',
    },
    cards=dict(
        one_liner='像查找一样往下走，路过的每个节点都试着当答案',
        complexity='时间 `O(h)`（树高），空间 `O(1)`',
        problem=['给一棵二叉搜索树和一个目标值 `target`（浮点数）',
                 '返回 BST 中==最接近 target==的节点值（题目保证唯一）',
                 '示例：BST `[8,4,12,2,6,10,14,1,3,5,7]`，`target = 5.3` → `5`'],
        quote='对于本题，则可以直接套用这种查找方法，从根节点开始向下走到某个叶子节点，在向下行走的过程中使用经过的每一个节点值来更新最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['BST 查找：节点比 target 大就去左边，否则去右边',
              '最接近的值一定在这条查找路径上，无需遍历整棵树',
              '路过一个节点就比一次 `abs` 差值，更近就更新 `res`'],
        summary=['时间 `O(h)`，空间 `O(1)`，不需要递归',
                 '比较的是 `abs(差值)`，不是节点值本身；`res` 初值为 None 要单独判断',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '同类题：272 题（找最近的 k 个值）'],
    ),
)
