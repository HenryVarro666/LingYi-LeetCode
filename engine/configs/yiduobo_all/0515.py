CONFIG = dict(
    num=515, title='在每个树行中找最大值', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='BFS · l/r 划分每一层',
    tags=[],
    code='''
class Solution(object):
    def largestValues(self, root):

        if not root:
            return []

        q = [root]
        l = 0
        r = 1
        new_r = r
        res = []
        while l < r:
            level_max = None
            for index in range(l, r):
                now = q[index]
                if level_max is None or level_max < now.val:
                    level_max = now.val
                if now.left:
                    q.append(now.left)
                    new_r += 1
                if now.right:
                    q.append(now.right)
                    new_r += 1
            res.append(level_max)

            l = r
            r = new_r

        return res
''',
    call='Solution().largestValues(Tr([1,3,2,5,3,None,9]))',
    expect=[1, 3, 9],
    views=[
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, path=False, h=280),
        dict(type='text', fn=lambda S: ('队列 `q = ' + str([x.val for x in S['q']]) + '`') if 'q' in S else '', size=26, h=56),
        dict(type='text', fn=lambda S: (f"当前层下标 `[{S['l']}, {S['r']})`，`level_max = {S.get('level_max')}`，`res = {S['res']}`") if 'res' in S else '', size=26, h=56),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('new_r', 'new_r', 'purple'), ('level_max', 'level_max', 'yellow'), ('res', 'res', 'green')],
    captions={
        'if not root': '空树没有任何层 → 返回 `[]`',
        'q = [root]': '`q` 是只增不减的数组，按层顺序放节点',
        'l = 0': '`l`：当前层在 `q` 里的起点',
        'r = 1': '`r`：当前层的终点（不含），第 1 层 = `q[0:1]`',
        'new_r = r': '`new_r`：下一层的终点，每追加一个孩子就 +1',
        'res = []': '`res` 按层记录最大值',
        'while l < r': lambda S, B, r_: (f'`l = {S.l} < r = {S.r}`：还有一层要处理' if S.l < S.r else f'`l = {S.l} ≥ r = {S.r}`：没有下一层 → 结束'),
        'level_max = None': '这一层的最大值先置为 `None`（节点值可能是负数，不能用 0）',
        'for index in range': '取本层下一个下标（范围 `q[{l}:{r}]`）；取完就退出 for',
        'now = q[index]': '取出节点 `{now.val}`',
        'if level_max is None or': lambda S, B, r_: (f'`level_max` 还是 None → 第一个节点直接当作最大值' if S.level_max is None and B.get('level_max') is None
                                                    else f'`{B.level_max} < {S.now.val}` → 更新' if B.get('level_max') is not None and B.level_max < S.now.val
                                                    else f'`{B.level_max} ≥ {S.now.val}` → 不更新'),
        'level_max = now.val': '`level_max = {level_max}`',
        'if now.left': lambda S, B, r_: (f'`{S.now.val}` 有左儿子 `{S.now.left.val}` → 追加到 `q` 末尾，`new_r` +1' if S.now.left else f'`{S.now.val}` 没有左儿子'),
        'q.append(now.left)': '`q` 追加左儿子',
        'if now.right': lambda S, B, r_: (f'`{S.now.val}` 有右儿子 `{S.now.right.val}` → 追加到 `q` 末尾，`new_r` +1' if S.now.right else f'`{S.now.val}` 没有右儿子'),
        'q.append(now.right)': '`q` 追加右儿子',
        'new_r += 1': '`new_r = {new_r}`：下一层的终点后移一位',
        'res.append(level_max)': '这一层看完 → 最大值 `{level_max}` 放进 `res` = `{res}`',
        'l = r': '下一层的起点 = 本层终点：`l = {l}`',
        'r = new_r': '下一层的终点 = `new_r`：`r = {r}`',
        'return res': '每层最大值依次是 `{ret}`',
    },
    cards=dict(
        one_liner='BFS 里用一对 l/r 圈出当前层，逐个比较取最大',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给定二叉树根节点 `root`，返回每一层节点值中的==最大值==',
                 '结果按层从上到下排列',
                 '示例：`[1,3,2,5,3,null,9]` → `[1,3,9]`'],
        quote='具体来说，就是在bfs过程中使用一组l和r来表示当前准备处理的这一层，在bfs队列中的头尾位置，然后从l遍历到r。',
        quote_src='—— yiduobo 题解原文',
        idea=['`q` 只增不减；`[l, r)` 是当前层，`new_r` 随着孩子追加而增长',
              '遍历当前层时：更新 `level_max`，同时把左右孩子追加到 `q`',
              '这一层结束：`res.append(level_max)`，再令 `l = r`、`r = new_r` 进入下一层'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`level_max` 初值用 `None` 而不是 0，节点值可以为负',
                 '易错：`r` 要在这一层遍历完才能改成 `new_r`，否则会把下一层的节点混进来',
                 '题面库里没有，题意按 LeetCode 515 与 yiduobo 原文整理；原文已是 Python 3 可运行写法，无需修改'],
    ),
)
