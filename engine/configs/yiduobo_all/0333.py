def _ret(S, B, r):
    if not r:
        return None
    return r


def _cap_ret(S, B, r):
    if r[0]:
        return f'`{S.now.val}` 为根是 ==BST==：返回 `(True, 最小 {r[1]}, 最大 {r[2]}, 节点数 {r[3]})`'
    return f'`{S.now.val}` 为根不是 BST → 返回 `(False, 0, 0, 0)`，父节点也不可能是 BST'


CONFIG = dict(
    num=333, title='最大BST子树', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='递归 · 返回 (是否BST, 最小, 最大, 节点数)',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def largestBSTSubtree(self, root):

        global res
        res = 0

        def dfs(now):
            global res

            if not now.left:
                if not now.right:
                    res = max(res, 1)
                    return True, now.val, now.val, 1
                else:
                    right_flag, right_mi, right_ma, right_size = dfs(now.right)
                    if right_flag and right_mi > now.val:
                        res = max(res, right_size + 1)
                        return True, now.val, right_ma, right_size + 1
                    else:
                        return False, 0, 0, 0

            elif not now.right:
                left_flag, left_mi, left_ma, left_size = dfs(now.left)
                if left_flag and left_ma < now.val:
                    res = max(res, left_size + 1)
                    return True, left_mi, now.val, left_size + 1
                else:
                    return False, 0, 0, 0
            
            else:
                left_flag, left_mi, left_ma, left_size = dfs(now.left)
                right_flag, right_mi, right_ma, right_size = dfs(now.right)
                if left_flag and right_flag and left_ma < now.val < right_mi:
                    res = max(res, left_size + right_size + 1)
                    return True, left_mi, right_ma, left_size + right_size + 1
                else:
                    return False, 0, 0, 0

        if root:
            dfs(root)
        return res
''',
    call='Solution().largestBSTSubtree(Tr([10,5,15,1,8,None,7]))',
    expect=3,
    views=[
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=300),
        dict(type='text', fn=lambda S: (f"左子树：`{S['_inner']['left_flag']}`，最大 `{S['_inner']['left_ma']}`，{S['_inner']['left_size']} 个节点"
                                        if 'left_flag' in S['_inner'] else ''), size=24, h=50),
        dict(type='text', fn=lambda S: (f"右子树：`{S['_inner']['right_flag']}`，最小 `{S['_inner']['right_mi']}`，{S['_inner']['right_size']} 个节点"
                                        if 'right_flag' in S['_inner'] else ''), size=24, h=50),
        dict(type='calls', h=170, hide=('res',)),
    ],
    watch=[('now', 'now.val', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 是全局答案：目前见过的最大 BST 的节点数',
        10: lambda S, B, r: ('没有左孩子 → 分「有无右孩子」两种情况' if not S.now.left else '有左孩子 → 看右孩子是否也有'),
        11: lambda S, B, r: (f'`{S.now.val}` 是==叶子==' if not S.now.right else f'只有右孩子 `{S.now.right.val}` → 先递归右子树'),
        22: lambda S, B, r: (f'只有左孩子 `{S.now.left.val}` → 先递归左子树' if not S.now.right else '左右孩子都有 → 两边都要递归'),
        'res = max(res, 1)': '叶子本身就是 BST（1 个节点）：`res = {res}`',
        'return True, now.val, now.val, 1': '叶子：`(True, 最小 {now.val}, 最大 {now.val}, 1)`',
        'right_flag, right_mi, right_ma, right_size = dfs': '右子树返回：`(是BST={right_flag}, 最小={right_mi}, 最大={right_ma}, 数量={right_size})`',
        'left_flag, left_mi, left_ma, left_size = dfs': '左子树返回：`(是BST={left_flag}, 最小={left_mi}, 最大={left_ma}, 数量={left_size})`',
        'if right_flag and right_mi > now.val': '右子树是 BST 且 `最小 {right_mi}` > `{now.val}`？ → ==以 {now.val} 为根也是 BST==，否则不是',
        'if left_flag and left_ma < now.val:': '左子树是 BST 且 `最大 {left_ma}` < `{now.val}`？ → ==以 {now.val} 为根也是 BST==，否则不是',
        'if left_flag and right_flag and': lambda S, B, r: (f'左右都是 BST，检查 `{S.left_ma} < {S.now.val} < {S.right_mi}`？' if S.left_flag and S.right_flag else f'左边是 BST：`{S.left_flag}`，右边是 BST：`{S.right_flag}` → 有一边不是，当前肯定不是 BST'),
        'res = max(res, right_size + 1)': '节点数 `{right_size} + 1`，更新 `res = max({B.res}, {right_size + 1}) = {res}`',
        'res = max(res, left_size + 1)': '节点数 `{left_size} + 1`，更新 `res = max({B.res}, {left_size + 1}) = {res}`',
        'res = max(res, left_size + right_size + 1)': '节点数 `{left_size} + {right_size} + 1`，更新 `res = max({B.res}, {left_size + right_size + 1}) = {res}`',
        'return True, now.val, right_ma': _cap_ret,
        'return True, left_mi, now.val': _cap_ret,
        'return True, left_mi, right_ma': _cap_ret,
        'return False': _cap_ret,
        'if root:': '从根开始递归',
        'return res': '最大 BST 子树有 `{res}` 个节点',
    },
    skip=['global res', 'else:'],
    max_steps=110,
    cards=dict(
        one_liner='后序递归：子树信息凑齐，再判断当前节点能否成为 BST 的根',
        complexity='时间 `O(n)`，空间 `O(h)`',
        problem=['给定二叉树，找出其中==节点数最多的 BST 子树==，返回它的节点数',
                 'BST：左子树所有值 < 根 < 右子树所有值',
                 '本视频：`root = [10,5,15,1,8,null,7]` → `3`',
                 '`5` 为根的子树 `[5,1,8]` 是 BST'],
        quote='若以now.left为根节点的子树或这以now.right为根节点的子树不是bst，那么以now为根节点的子树也不是bst。此时另外三个值就无关紧要了，直接返回False, 0, 0, 0',
        quote_src='—— yiduobo 题解原文',
        idea=['每棵子树返回四个信息：==是否 BST、最小值、最大值、节点数==',
              '左右都是 BST，且 `左最大 < now.val < 右最小`，当前子树才是 BST',
              '是 BST 就用节点数更新 `res`；不是就返回 `False, 0, 0, 0`'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '不是 BST 时后三个值不会被用到，因为父节点先判 flag',
                 '缺孩子时最小/最大值取 `now.val` 自己，容易漏掉',
                 '比较用严格不等号，等于也不是 BST',
                 '原文为 Python 2 风格，代码可直接在 Python 3 运行，未做修改'],
    ),
)
