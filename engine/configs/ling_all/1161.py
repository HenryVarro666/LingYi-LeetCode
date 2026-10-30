CONFIG = dict(
    num=1161, title='最大层内元素和', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='BFS 逐层求和',
    tags=['难度分 1250'],
    code='''
class Solution:
    def maxLevelSum(self, root: Optional[TreeNode]) -> int:
        max_sum = -inf
        ans = 0

        q = [root]
        level = 1
        while q:
            tmp = q
            q = []
            s = 0
            for node in tmp:
                s += node.val
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)

            if s > max_sum:
                max_sum = s
                ans = level

            level += 1

        return ans
''',
    call='Solution().maxLevelSum(Tr([1,7,0,7,-8,None,None]))',
    expect=2,
    views=[
        dict(type='tree', label='二叉树（蓝 = 当前累加的节点）', pointers={'node': 'blue'}, path=False, h=290),
        dict(type='text', fn=lambda S: ('当前层 `' + str([x.val for x in S['tmp']]) + '`  层和 `s = ' + str(S.get('s')) + '`') if 'tmp' in S else '', size=26, h=60),
        dict(type='text', fn=lambda S: f"最大层和 `max_sum = {S['max_sum']}`，层号 `ans = {S['ans']}`" if 'max_sum' in S else '', size=26, h=60),
    ],
    watch=[('level', 'level', 'yellow'), ('s', 's'), ('max_sum', 'max_sum', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'max_sum = -inf': '`max_sum` 记最大层和，初始 `-inf`：层和可能是负数，不能设成 0',
        'ans = 0': '`ans` 记最大层和所在的层号',
        'q = [root]': '`q` 装着当前层的节点，根在第 `1` 层',
        'while q': lambda S, B, r: (f'`q` 里有 `{len(S.q)}` 个节点 → 处理第 `{S.level}` 层' if S.q else '`q` 空了 → 所有层都处理完'),
        'tmp = q': '`tmp` 取走本层节点',
        'q = []': '`q` 清空，用来装==下一层==',
        's = 0': '本层和从 `0` 开始累加',
        's += node.val': '`s += {node.val}` → 层和 `{s}`',
        'if node.left': lambda S, B, r: (f'`{S.node.val}` 有左儿子 `{S.node.left.val}` → 放进下一层' if S.node.left else f'`{S.node.val}` 没有左儿子'),
        'if node.right': lambda S, B, r: (f'`{S.node.val}` 有右儿子 `{S.node.right.val}` → 放进下一层' if S.node.right else f'`{S.node.val}` 没有右儿子'),
        'if s > max_sum': lambda S, B, r: (f'第 `{S.level}` 层和 `{S.s}` > `max_sum = {S.max_sum}` → ==严格大于==才更新' if S.s > S.max_sum else f'第 `{S.level}` 层和 `{S.s}` ≤ `max_sum = {S.max_sum}` → 不更新（相等时保留更小的层号）'),
        'max_sum = s': '更新最大层和 `max_sum = {max_sum}`',
        'ans = level': '最大层和在第 `{level}` 层 → `ans = {ans}`',
        'level += 1': '进入下一层：`level = {level}`',
        'return ans': '最大层和 `{max_sum}` 出现在第 `{ans}` 层 → 返回 `{ret}`',
    },
    cards=dict(
        one_liner='BFS 一层一层求和，严格更大才更新答案',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['根节点在第 `1` 层，返回==层内元素和最大==的那一层的层号',
                 '和相同时返回==最小==的层号',
                 '示例：`[1,7,0,7,-8,null,null]` → 各层和 `1, 7, -1` → `2`'],
        quote='本题需要计算每一层的节点值之和，适合用 BFS。维护两个信息：最大层和 maxSum，以及对应的层号 ans。如果当前层的和大于 maxSum，那么更新 maxSum 和 ans。',
        quote_src='—— 灵茶山艾府题解',
        idea=['用列表 `q` 表示当前层，`tmp = q` 后重建 `q = []` 装下一层',
              '遍历 `tmp` 累加层和，同时把左右儿子放进新的 `q`',
              '`s > max_sum` 才更新，==严格大于==保证同分时留下最小层号'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`max_sum` 初值用 `-inf`，层和可以为负；用 `>` 而不是 `>=`',
                 '易错：`level` 从 1 开始，每层处理完再 `+= 1`',
                 '方法二 DFS：`row_sum[level]` 按层累加，最后 `row_sum.index(max(row_sum)) + 1`'],
    ),
)
