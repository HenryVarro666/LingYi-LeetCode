def _v(n):
    return 'None' if n is None else str(n.val)


CONFIG = dict(
    num=671, title='二叉树中第二小的节点', difficulty='Easy', category='二叉树与回溯',
    author='yiduobo', technique='递归 · 分情况讨论',
    tags=['灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def findSecondMinimumValue(self, root):

        return self.find(root)

    def find(self, now):
        if not now.left:
            return -1

        if now.left.val == now.val:
            if now.right.val == now.val:
                second_l = self.find(now.left)
                second_r = self.find(now.right)
            else:
                second_l = self.find(now.left)
                second_r = now.right.val
        else:
            second_l = now.left.val
            second_r = self.find(now.right)
        
        if second_l == -1:
            return second_r
        elif second_r == -1:
            return second_l
        else:
            return min(second_l, second_r)
''',
    call='Solution().findSecondMinimumValue(Tr([2,2,2,2,3,2,4]))',
    expect=3,
    views=[
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=330),
        dict(type='text', fn=lambda S: (f"`now = {_v(S['now'])}`，`second_l = {S['_inner'].get('second_l', '?')}`，`second_r = {S['_inner'].get('second_r', '?')}`" if 'now' in S else ''), size=26, h=60),
        dict(type='calls', h=230, hide=()),
    ],
    watch=[('now', lambda S: S['now'].val if 'now' in S and S['now'] else None, 'blue'),
           ('second_l', lambda S: S['_inner'].get('second_l'), 'cyan'),
           ('second_r', lambda S: S['_inner'].get('second_r'), 'pink')],
    captions={
        'return self.find(root)': '从根开始求整棵树的第二小值',
        'if not now.left': lambda S, B, r: (f'`{S.now.val}` 没有孩子 → 这棵子树只有一个值，不存在第二小' if not S.now.left
                                           else f'`{S.now.val}` 有孩子（要么 0 个要么 2 个）→ 继续分情况'),
        'return -1': '叶子：没有第二小，返回 `-1`',
        'if now.left.val == now.val': lambda S, B, r: (f'左孩子 `{S.now.left.val}` == 根 `{S.now.val}`：左子树里还可能藏着更大的值' if S.now.left.val == S.now.val
                                                      else f'左孩子 `{S.now.left.val}` ≠ 根 `{S.now.val}`：左孩子就是左子树最小的 ==更大值=='),
        'if now.right.val == now.val': lambda S, B, r: (f'右孩子也等于根 `{S.now.val}`：==两边都要递归==，各自找第二小' if S.now.right.val == S.now.val
                                                       else f'右孩子 `{S.now.right.val}` ≠ 根：它就是右子树的候选第二小'),
        'second_l = self.find(now.left)': '递归求左子树的第二小：`second_l = {second_l}`',
        'second_r = self.find(now.right)': '递归求右子树的第二小：`second_r = {second_r}`',
        'second_r = now.right.val': '右孩子值直接当候选：`second_r = {second_r}`（不用再往下找，子树最小就是它）',
        'second_l = now.left.val': '左孩子值直接当候选：`second_l = {second_l}`',
        'if second_l == -1': lambda S, B, r: ('左边没有候选 → 答案只能来自右边' if S.second_l == -1 else '左边有候选，再看右边'),
        'return second_r': '只有右边有候选，返回 `{second_r}`',
        'elif second_r == -1': lambda S, B, r: ('右边没有候选 → 返回左边' if S.second_r == -1 else '两边都有候选 → 取较小的'),
        'return second_l': '只有左边有候选，返回 `{second_l}`',
        'return min': '两边都有：`min({second_l}, {second_r})` = =={ret}==',
    },
    skip=[],
    cards=dict(
        one_liner='根最小，所以第二小只可能藏在「值等于根」的那一侧',
        complexity='时间 `O(n)`，空间 `O(h)`',
        problem=['特殊二叉树：每个节点有 `0` 或 `2` 个孩子，且==根的值 ≤ 子树里所有值==',
                 '求整棵树中==第二小的值==，不存在则返回 `-1`',
                 '本视频：`root = [2,2,2,2,3,2,4]` → `3`'],
        quote='任意节点的孩子个数只会是0或者2，另一个则是任意子树最小的节点必然是根节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['原文分四种情况：叶子返回 `-1`；左右都等于根就两边递归；只有一边等于根，另一边的孩子值就是候选',
              '`second_l` / `second_r` 是左右两侧各自的第二小候选，`-1` 表示没有',
              '最后取两个候选里存在的较小者'],
        summary=['时间 `O(n)`，空间 `O(h)`（递归栈）',
                 '易错点：==孩子值大于根时不用再递归==，它就是该侧的最小值',
                 '两个候选都是 `-1` 时返回 `-1`（所有值都相同的树）',
                 '原文本来就是 Python 3 可跑的写法，仅示例树用 Tr([...]) 构造'],
    ),
)
