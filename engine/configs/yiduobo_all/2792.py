def _cmp(S, B, ret):
    ml = S.mi_list
    mx = -ml[0]
    if S.now.val > mx:
        return f'`now.val = {S.now.val}` > 堆顶（最小 k 个里最大的）`{mx}` → ==比子树里至少 k 个值都大==，答案加 1'
    return f'`now.val = {S.now.val}` ≤ 堆顶 `{mx}` → 不够大，不计数'


CONFIG = dict(
    num=2792, title='计算满足条件的节点数', difficulty='Hard', category='二叉树与回溯',
    author='yiduobo', technique='递归 · 子树最小 k 个值（大顶堆）',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def countGreatEnoughNodes(self, root, k):

        global res
        res = 0

        def dfs(now):
            global res

            mi_list = [-now.val]
            if now.left:
                left_mi = dfs(now.left)
                for v in left_mi:
                    heapq.heappush(mi_list, v)
                    if len(mi_list) > k:
                        heapq.heappop(mi_list)
            
            if now.right:
                right_mi = dfs(now.right)
                for v in right_mi:
                    heapq.heappush(mi_list, v)
                    if len(mi_list) > k:
                        heapq.heappop(mi_list)
            
            if now.val > -mi_list[0]:
                res += 1

            return mi_list
        

        dfs(root)
        return res
''',
    call='Solution().countGreatEnoughNodes(Tr([7,6,5,4,3,2,1]), 2)',
    expect=3,
    views=[
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=300),
        dict(type='heap', var='mi_list', label='mi_list（存相反数的大顶堆，堆顶 = 最大的那个）', fmt=lambda x: str(x), h=130),
        dict(type='text', fn=lambda S: f"本子树最小的 k 个值：`{sorted(-x for x in S['mi_list'])}`" if 'mi_list' in S else '', size=26, h=56),
        dict(type='calls', h=170, hide=('res',)),
    ],
    watch=[('now', 'now.val', 'blue'), ('k', 'k', 'yellow'), ('res', "res", 'green')],
    captions={
        'res = 0': '`res` 是全局计数：记录满足条件的节点数',
        'mi_list = [-now.val]': '先把 `now.val = {now.val}` 放进自己的堆（存相反数 `{-now.val}`，Python 的堆是小顶堆，取负变大顶）',
        'if now.left': lambda S, B, r: (f'有左孩子 `{S.now.left.val}` → 先递归求左子树最小的 k 个值' if S.now.left else '没有左孩子，跳过'),
        'if now.right': lambda S, B, r: (f'有右孩子 `{S.now.right.val}` → 再递归求右子树最小的 k 个值' if S.now.right else '没有右孩子，跳过'),
        'left_mi = dfs': '左子树返回的堆 `left_mi = {left_mi}`（相反数）',
        'right_mi = dfs': '右子树返回的堆 `right_mi = {right_mi}`（相反数）',
        'for v in left_mi': '把左子树的候选值逐个并入当前堆',
        'for v in right_mi': '把右子树的候选值逐个并入当前堆',
        'heapq.heappush': '`{-v}` 入堆 → 堆内（取负前）`{sorted(-x for x in mi_list)}`',
        'if len(mi_list) > k': lambda S, B, r: (f'堆大小 `{len(S.mi_list)}` > k = `{S.k}` → 超了，弹出最大的' if len(S.mi_list) > S.k else f'堆大小 `{len(S.mi_list)}` ≤ k = `{S.k}` → 不用弹'),
        'heapq.heappop': '弹出堆顶 `{-B.mi_list[0]}`：它==不可能==属于最小的 k 个 → 堆内 `{sorted(-x for x in mi_list)}`',
        'if now.val > -mi_list[0]': _cmp,
        'res += 1': '满足条件 → `res` 变成 =={res}==',
        'return mi_list': '把本子树最小 k 个值 `{sorted(-x for x in mi_list)}` 返回给父节点用',
        'dfs(root)': '从根开始后序递归，`k = {k}`',
        'return res': '一共有 `{res}` 个节点满足条件',
    },
    skip=['global res', 'for v in'],
    max_steps=130,
    cards=dict(
        one_liner='每棵子树只留最小的 k 个值：根比它们都大就计数',
        complexity='时间 `O(n·k·log k)`，空间 `O(n·k)`（递归栈与堆）',
        problem=['节点值为整数的二叉树 `root` 和正整数 `k`',
                 '节点 `x` 满足条件：子树中==至少有 k 个节点==值严格小于它',
                 '求满足条件的节点个数',
                 '本视频：`root = [7,6,5,4,3,2,1]`，`k = 2` → `3`'],
        quote='题目给出的n比较大，但是k很小，于是可以对于每颗子树都维护树中最小的k个节点值，接下来就只需检测子树的根节点的值是否大于这k个最小的节点值中最大的那一个就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['k 很小 → 每个子树只维护==最小的 k 个值==，用大顶堆',
              '先放入自己，再把左右子树返回的堆逐个并入；超过 k 个就弹堆顶',
              '堆顶是 k 个最小值里最大的：`now.val` 比它大，就说明比至少 k 个都大'],
        summary=['时间约 `O(n·k·log k)`，空间 `O(n·k)`',
                 '堆里存的是相反数，所以比较用 `-mi_list[0]`',
                 '只有堆满 k 个且 `now.val` 大于堆顶才计数：堆里不足 k 个时，自己一定在堆里（堆顶 ≥ 自己），不会误判',
                 '原文为 Python 2 风格，代码无需改动（只删去了类型说明）；`global res` 在 Python 3 同样可用'],
    ),
)
