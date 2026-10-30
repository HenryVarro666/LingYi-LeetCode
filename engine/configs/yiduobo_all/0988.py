def _v(n):
    return 'None' if n is None else str(n.val)


def _cap_leaf(S, B, ret):
    n = S.now
    if not n.left and not n.right:
        return f'`{n.val}` 没有左右孩子 → ==叶子==，`suffix` 就是从它出发的完整字符串'
    return f'`{n.val}` 不是叶子 → 还要往下走'


CONFIG = dict(
    num=988, title='从叶节点开始的最小字符串', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='DFS · 字符串拼在头部',
    tags=['灵神核心路线', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def smallestFromLeaf(self, root):
        return self.dfs(root, "")

    def dfs(self, now, suffix):
        now_suffix = chr(now.val + 97) + suffix
        if not now.left:
            if not now.right:
                return now_suffix
            else:
                return self.dfs(now.right, now_suffix)
        elif not now.right:
            return self.dfs(now.left, now_suffix)
        else:
            return min(self.dfs(now.left, now_suffix), self.dfs(now.right, now_suffix))
''',
    call='Solution().smallestFromLeaf(Tr([0,1,2,3,4,3,4]))',
    expect='dba',
    views=[
        dict(type='text', fn=lambda S: f"当前 `now_suffix = \"{S['_inner'].get('now_suffix', S['_inner'].get('suffix', ''))}\"`（从当前节点到根的字符串）" if 'now' in S else '节点值 0..25 对应 a..z', size=26, h=56),
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=330),
        dict(type='calls', h=240),
    ],
    watch=[('now', lambda S: S['_inner'].get('now') and S['_inner']['now'].val, 'blue'),
           ('suffix', lambda S: S['_inner'].get('suffix'), 'yellow'),
           ('now_suffix', lambda S: S['_inner'].get('now_suffix'), 'green')],
    captions={
        'self.dfs(root, "")': '从根出发，`suffix` 初始为空串',
        'now_suffix = chr': '`now.val = {now.val}` → 字符 `{chr(now.val + 97)}`，==拼在 suffix 头部==：`{now_suffix}`',
        'if not now.left': _cap_leaf,
        8: '没有左孩子，再看右孩子：{"也没有 → 叶子，返回" if not now.right else "有 → 只递归右边"}',
        'return now_suffix': '到达叶子，返回整条字符串 `{now_suffix}`',
        'return self.dfs(now.right': '只有右孩子 → 直接递归右边，不用比较',
        'return self.dfs(now.left': '只有左孩子 → 直接递归左边，不用比较',
        'return min': '左右都有 → 先递归左边，再递归右边，最后取两个返回串中较小的（字典序）',
        12: '有左孩子；右孩子{"为空 → 只递归左边" if not now.right else "也有 → 两边都要递归"}',
    },
    cards=dict(
        one_liner='字符串拼在头部，叶子处得到完整串，左右取 min',
        complexity='时间 `O(n·h)`（字符串拼接），空间 `O(h)`',
        problem=['二叉树节点值为 `0..25`，分别对应 `a..z`',
                 '求从==叶子出发、到根结束==的所有字符串中字典序最小的一个',
                 '示例：`[0,1,2,3,4,3,4]` → `"dba"`'],
        quote='dfs的结果则定义为以当前节点为根节点的子树中，从叶节点开始，到原始的root结束的最小字符串是什么。',
        quote_src='—— yiduobo 题解',
        idea=['`suffix` 记录根到当前节点的字符串；新字符拼在==头部==，正好是叶到根的顺序',
              '叶子：直接返回 `suffix`；只有一个孩子：递归那一边',
              '两个孩子都有：各自递归，返回较小的字符串'],
        summary=['时间 `O(n·h)`，每次拼接要复制字符串；空间 `O(h)`',
                 '易错：字符串要==从叶子往根读==，所以新字符放在前面',
                 '易错：不能只比较叶子字符，前缀相同时较短的字符串更小，`min` 已处理',
                 '原文为 Python 2 写法，仅删去了空行，代码无需其他改动'],
    ),
)
