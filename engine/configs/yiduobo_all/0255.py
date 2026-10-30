def _cmp(S, B, r):
    v, rv = S.v, S.root_val
    if rv > v:
        return f'`root_val = {rv} > v = {v}`：{v} 本该在 {rv} 的左子树里，却出现在右子树位置 → ==非法=='
    return f'`root_val = {rv} ≤ v = {v}`：没有违反「右子树都大于 root_val」→ 继续'


def _while(S, B, r):
    if S.stack and S.stack[-1] < S.v:
        return f'栈顶 `{S.stack[-1]} < v = {S.v}`：{S.v} 是它的右子树里的数 → 弹出栈顶，==root_val 记为它=='
    if not S.stack:
        return '栈空了，不再弹出'
    return f'栈顶 `{S.stack[-1]} ≥ v = {S.v}`：{S.v} 在它的左子树里 → 停止弹出'


def _show(S):
    if 'stack' not in S:
        return ''
    return f"`root_val = {S['root_val']}`：此后所有数都必须 ==大于== 它；栈 = {S['stack']}"


CONFIG = dict(
    num=255, title='验证前序遍历序列二叉搜索树', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='单调栈 · 维护 root_val 下界',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def verifyPreorder(self, preorder):

        root_val = -1
        stack = []
        for v in preorder:
            if root_val > v:
                return False
            
            while stack and stack[-1] < v:
                root_val = stack[-1]
                stack.pop()

            stack.append(v)
        
        return True
''',
    call='Solution().verifyPreorder([5,2,1,3,6])',
    expect=True,
    views=[
        dict(type='array', var='preorder', label='preorder（黄色 = 当前 v）', h=200,
             color=lambda S, i, x: ('yellow' if 'v' in S and i == S['preorder'].index(S['v']) else ('green' if 'v' in S and i < S['preorder'].index(S['v']) else None))),
        dict(type='stack', var='stack', label='stack（单调递减：栈底 → 栈顶）', h=150),
        dict(type='text', h=70, fn=_show, size=26),
    ],
    watch=[('v', 'v', 'yellow'), ('root_val', 'root_val', 'pink'), ('stack', 'stack', 'blue')],
    captions={
        'root_val = -1': '`root_val` 是当前允许的下界，开始还没有限制',
        'stack = []': '`stack` 保存「还在等右子树」的祖先，从底到顶递减',
        'for v in preorder': lambda S, B, r: (f'读下一个数 `v = {S.v}`' if S.get('v') != B.get('v') else '序列读完了，没有发现矛盾'),
        'if root_val > v': _cmp,
        'return False': '序列不是合法的 BST 前序 → 返回 `False`',
        'while stack': _while,
        'root_val = stack[-1]': '`root_val = {root_val}`：被弹出的最后一个，是比 `{v}` 小的 ==最小祖先==，`{v}` 在它右边',
        'stack.pop()': '弹出后 `stack = {stack}`',
        'stack.append(v)': '`v = {v}` 入栈，等它自己的左右子树 → `stack = {stack}`',
        'return True': '每个数都没有违反下界 → 是合法的前序序列，返回 `True`',
    },
    cards=dict(
        one_liner='单调栈弹出的最后一个数，就是此后所有数的下界',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给一个无重复元素的整数数组 `preorder`',
                 '判断它能否是某棵==二叉搜索树的前序遍历==结果',
                 '示例：`[5,2,1,3,6]` → `True`；`[5,2,6,1,3]` → `False`'],
        quote='被弹出栈的最后一个节点必然是所有值小于当前节点的节点中值最小，也是辈分最高的那一个。只要满足了这个节点，其他被弹出节点关于向左走的节点的值的检测也顺带就完成了，因此不妨将其记为root_val。',
        quote_src='—— yiduobo 题解原文',
        idea=['前序 = 根 + 左子树 + 右子树；右子树的值都要比根大',
              '栈里存还没有进右子树的祖先；来了更大的 `v` 就说明进了某些祖先的右子树',
              '弹出的最后一个祖先 `root_val` 就是 `v` 的最近 ==左祖先==',
              '从此往后任何数都得 `> root_val`，否则非法'],
        summary=['时间 `O(n)`，空间 `O(n)`；元素互不相同，所以弹栈用 `<`',
                 '`root_val` 只增不减；每次比较在弹栈之前，用的是上一轮的下界',
                 '易错点：先检查 `root_val > v`，再弹栈，顺序不能换',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
