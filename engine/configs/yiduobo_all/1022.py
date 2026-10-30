CONFIG = dict(
    num=1022, title='从根到叶的二进制数之和', difficulty='Easy', category='链表、二叉树与回溯',
    author='yiduobo', technique='DFS · 带前缀往下走',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1462'],
    code='''
class Solution(object):
    def sumRootToLeaf(self, root):
        return self.dfs(root, 0)

    def dfs(self, now, prefix):
        prefix = prefix + prefix + now.val
        if not now.left and not now.right:
            return prefix

        ret = 0
        if now.left:
            ret += self.dfs(now.left, prefix)

        if now.right:
            ret += self.dfs(now.right, prefix)

        return ret
''',
    call='Solution().sumRootToLeaf(Tr([1,0,1,0,1,0,1]))',
    expect=22,
    views=[
        dict(type='text', fn=lambda S: f"前缀 `prefix = {S['_inner'].get('prefix')}` = 二进制 `{bin(S['_inner']['prefix'])[2:]}`" if 'now' in S['_inner'] and isinstance(S['_inner'].get('prefix'), int) else '', size=26, h=56),
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=300),
        dict(type='calls', h=250),
    ],
    watch=[('now', lambda S: S['_inner'].get('now') and S['_inner']['now'].val, 'blue'),
           ('prefix', lambda S: S['_inner'].get('prefix'), 'yellow'),
           ('ret', lambda S: S['_inner'].get('ret'), 'green')],
    captions={
        'return self.dfs(root, 0)': '从根出发，前缀 `prefix` 初始为 0',
        'prefix = prefix + prefix': '`prefix + prefix + now.val` = `{B.prefix} + {B.prefix} + {B.now.val}` = =={prefix}==（前缀翻倍，相当于左移一位，再加当前位）',
        'if not now.left and not now.right': '`{now.val}` {"没有左右孩子 → ==叶子==，prefix 就是整条路径的二进制值" if (not now.left and not now.right) else "还有孩子 → 不是叶子，继续往下"}',
        'return prefix': '叶子：直接返回 `{prefix}`',
        'ret = 0': '`ret` 累计左右子树返回的和，初始 0',
        'if now.left': '`{now.val}` {"有左孩子 → 递归求左边的和" if now.left else "没有左孩子，跳过"}',
        'if now.right': '`{now.val}` {"有右孩子 → 递归求右边的和" if now.right else "没有右孩子，跳过"}',
        'ret += self.dfs(now.left': '进入左孩子，把 `prefix = {B.prefix}` 传下去',
        'ret += self.dfs(now.right': '进入右孩子，把 `prefix = {B.prefix}` 传下去',
        'return ret': '左右子树返回值相加，`ret` = =={ret}== 交给上一层',
    },
    cards=dict(
        one_liner='前缀自己加自己再加当前位，叶子返回、非叶子求和',
        complexity='时间 `O(n)`，空间 `O(h)`',
        problem=['二叉树节点值只有 `0` 或 `1`，根到叶的路径是一个二进制数，根是最高位',
                 '把所有叶子的数加起来',
                 '示例：`[1,0,1,0,1,0,1]` → `4+5+6+7 = 22`'],
        quote='带着从根节点开始到当前节点结束的二进制值前缀prefix往下走。对于当前节点now而言，这个前缀prefix的值应当更新为prefix + prefix + now.val。',
        quote_src='—— yiduobo 题解',
        idea=['`prefix + prefix` 就是 `prefix × 2`：二进制数后面补一位，前面的位权翻倍',
              '叶子：`prefix` 已经是完整路径的值，直接返回',
              '非叶子：把左右孩子返回的和加起来再返回，自底向上汇总'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '易错：先更新 `prefix` 再判叶子，叶子自己的位也要算',
                 '易错：只对存在的孩子递归，否则空节点没有 `.val`',
                 '原文为 Python 2 风格，仅删去了空行，无需其他改动',
                 '对比灵神：灵神用 `num << 1 | node.val`，这里用 `prefix + prefix + now.val`，是同一个意思'],
    ),
)
