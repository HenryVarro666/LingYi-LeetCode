CONFIG = dict(
    num=366, title='寻找二叉树的叶子节点', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='递归 · 按「被删除的轮次」分组',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def findLeaves(self, root):

        node_dict = {}

        def dfs(now):
            if not now.left:
                if not now.right:
                    level = 0
                else:
                    level = dfs(now.right) + 1
            elif not now.right:
                level = dfs(now.left) + 1
            else:
                level = max(dfs(now.left), dfs(now.right)) + 1
            
            if level not in node_dict:
                node_dict[level] = []
            node_dict[level].append(now.val)
            return level

        dfs(root)

        return [x[1] for x in sorted(node_dict.items(), key=lambda d:d[0])]
''',
    call='Solution().findLeaves(Tr([1,2,3,4,5]))',
    expect=[[4, 5, 3], [2], [1]],
    views=[
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=280),
        dict(type='map', var='node_dict', label='node_dict：轮次 → 该轮删除的节点', fmt=lambda k, v: f'{k}: {v}', h=150),
        dict(type='text', fn=lambda S: f"当前节点 `{S['now'].val}` 被删除的轮次 `level = {S['level']}`" if 'now' in S and 'level' in S else '', size=26, h=56),
        dict(type='calls', h=170),
    ],
    watch=[('now', 'now.val', 'blue'), ('level', lambda S: S['_inner'].get('level'), 'yellow')],
    captions={
        'node_dict = {}': '`node_dict`：key 是删除轮次，value 是这一轮删掉的节点值（从左到右）',
        7: lambda S, B, r: (f'`{S.now.val}` 没有左孩子 → 看右孩子' if not S.now.left else f'`{S.now.val}` 有左孩子 → 继续判断右孩子'),
        8: lambda S, B, r: (f'`{S.now.val}` 没有任何孩子 → 是叶子，第 ==0== 轮就被删' if not S.now.right else f'只有右孩子 → 等右孩子被删后的下一轮'),
        12: lambda S, B, r: (f'只有左孩子 → 等左孩子被删后的下一轮' if not S.now.right else '左右孩子都有 → 要等两个孩子都被删完'),
        'level = 0': '叶子：`level = 0`',
        'level = dfs(now.right) + 1': '右孩子的轮次 + 1：`level = =={level}==`',
        'level = dfs(now.left) + 1': '左孩子的轮次 + 1：`level = =={level}==`',
        'level = max': '取左右孩子较大的轮次再 + 1（要等较晚被删的那个）：`level = =={level}==`',
        'if level not in node_dict': lambda S, B, r: (f'第 `{S.level}` 轮还没有记录 → 新建空列表' if S.level not in S.node_dict else f'第 `{S.level}` 轮已有记录'),
        'node_dict[level] = []': '新建 `node_dict[{level}] = []`',
        'node_dict[level].append': '把 `{now.val}` 放进第 `{level}` 轮：`node_dict[{level}] = {node_dict[level]}`',
        'return level': '把 `{now.val}` 的轮次 `{level}` 返回给父节点',
        'dfs(root)': '先递归左再递归右，保证同一轮里==从左到右==',
        'return [x[1]': '按轮次 key 从小到大取出各轮的节点：`{ret}`',
    },
    skip=['else:'],
    cards=dict(
        one_liner='节点的删除轮次 = 左右孩子较大的轮次 + 1，叶子是第 0 轮',
        complexity='时间 `O(n log n)`（最后按 key 排序），空间 `O(n)`',
        problem=['给你一棵二叉树，像摘叶子一样：==收集所有叶子并删除==，重复直到树空',
                 '返回每一轮收集到的叶子，同一轮从左到右',
                 '本视频：`root = [1,2,3,4,5]` → `[[4,5,3],[2],[1]]`'],
        quote='每个节点会在其所有孩子节点全部被删除之后的下一轮遭到删除，那么在这里就可以从根节点向下递归求解。对于当前节点now，先递归求解now.left和now.right遭到删除的轮次，那么now被删除的轮次就是二者中较大值加上1。',
        quote_src='—— yiduobo 题解原文',
        idea=['不真的删节点：算出每个节点在==第几轮==被删（高度）',
              '叶子 0 轮；其他节点 = 孩子里最大轮次 + 1',
              '用哈希表按轮次分组，最后按 key 排序输出'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`；轮次是连续整数，也可直接用列表避免排序',
                 '必须先递归左子树再右子树，同一轮才是从左到右',
                 '只有一个孩子时不能用 `max`，原文分三种情况写',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行'],
    ),
)
