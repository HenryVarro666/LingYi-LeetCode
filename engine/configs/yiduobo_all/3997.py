CONFIG = dict(
    num=3997, title='统计二叉树中支配节点的数量', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='递归返回 (数量, 最大值)',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1427'],
    code='''
class Solution(object):
    def countDominantNodes(self, root):
        def dfs(now):
            if now.left:
                left_res, left_v = dfs(now.left)
            else:
                left_res, left_v = 0, 0

            if now.right:
                right_res, right_v = dfs(now.right)
            else:
                right_res, right_v = 0, 0

            res = left_res + right_res
            ma = max(left_v, right_v)
            if now.val >= ma:
                return res + 1, now.val
            else:
                return res, ma

        return dfs(root)[0]
''',
    call='Solution().countDominantNodes(Tr([5,3,8,2,4,7,1]))',
    expect=5,
    views=[
        dict(type='tree', label='完全二叉树（蓝 = 当前 now）', pointers={'now': 'blue'}, h=330),
        dict(type='text', fn=lambda S: (f"本层 `res = {S['_inner']['res']}`，子树最大值 `ma = {S['_inner']['ma']}`"
                                         if 'ma' in S['_inner'] else ''), size=26, h=60),
        dict(type='calls', h=210),
    ],
    watch=[('now', lambda S: S['_inner'].get('now') and S['_inner']['now'].val, 'blue'),
           ('res', lambda S: S['_inner'].get('res'), 'green'),
           ('ma', lambda S: S['_inner'].get('ma'), 'yellow')],
    captions={
        'if now.left:': lambda S, B, r: (f'`{B.now.val}` 有左孩子 → 递归求左子树的 (数量, 最大值)' if B.now.left
                                         else f'`{B.now.val}` 没有左孩子 → 左边记为 `(0, 0)`'),
        'if now.right:': lambda S, B, r: (f'`{B.now.val}` 有右孩子 → 递归求右子树的 (数量, 最大值)' if B.now.right
                                          else f'`{B.now.val}` 没有右孩子 → 右边记为 `(0, 0)`'),
        'left_res, left_v = dfs': '左子树返回：支配节点 `{left_res}` 个，最大值 `{left_v}`',
        'right_res, right_v = dfs': '右子树返回：支配节点 `{right_res}` 个，最大值 `{right_v}`',
        'left_res, left_v = 0, 0': '没有左孩子：`left_res = 0`，`left_v = 0`',
        'right_res, right_v = 0, 0': '没有右孩子：`right_res = 0`，`right_v = 0`',
        'res = left_res': '先把两边的支配节点数加起来：`res = {left_res} + {right_res} = {res}`',
        'ma = max': '两边子树的最大值 `ma = max({left_v}, {right_v}) = {ma}`',
        'if now.val >= ma': lambda S, B, r: (f'`{S.now.val} >= {S.ma}` → 自己不比后代小，==自己也是支配节点=='
                                             if S.now.val >= S.ma else
                                             f'`{S.now.val} < {S.ma}` → 后代里有更大的，自己不是支配节点'),
        'return res + 1': '多了自己：返回 `({res} + 1, {now.val})`，子树最大值就是自己',
        'return res, ma': '自己不是：数量不变，返回 `({res}, {ma})`，最大值仍是后代的 `{ma}`',
        'return dfs(root)[0]': '从根开始递归，最后取返回二元组的第 0 项 = ==支配节点总数=='
    },
    cards=dict(
        one_liner='每棵子树返回两个值：支配节点数 + 子树最大值',
        complexity='时间 `O(n)`，空间 `O(log n)`',
        problem=['节点值等于其子树中 ==最大值== 的节点叫支配节点',
                 '给定一棵完全二叉树，求支配节点的数量',
                 '示例：`root = [5,3,8,2,4,7,1]` → `5`'],
        quote='题目中关于支配节点的定义设计到子树中所有节点的最大值，那么一个自然的想法就是自顶向下递归求解。',
        quote_src='—— yiduobo 题解',
        idea=['`dfs(now)` 返回 `(res, v)`：子树的支配节点数、子树最大值',
              '没有孩子就记 `(0, 0)`，有孩子就递归',
              '`res` 先取左右之和；`now.val >= max(左, 右)` 时再加自己并把最大值换成 `now.val`'],
        summary=['时间 `O(n)`，空间 `O(log n)`',
                 '原文用 `>=` 判断，`val` 都 >= 1，和 `==` 等价',
                 '先判断孩子是否存在再递归，所以不会递归到空节点',
                 '同类题：2265 同样需要子树返回多个信息'],
    ),
)
