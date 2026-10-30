def _ph(S):
    ln = S.get('_line', 0)
    return 1 if ln <= 8 else (2 if ln <= 21 else 3)


def _show(S):
    ph = _ph(S)
    if 'rank' not in S:
        return '先把插入顺序转成 ==rank==：值 `v` 是第几个插入的'
    if ph == 1:
        return '`rank[v-1] = 插入时刻`；`rank[x]` 越小，值 `x+1` 越早插入'
    if ph == 2:
        return '在 rank 上找「左侧第一个更大」得到 ma，同时得到 mi（下标 = 插入时刻）'
    return '时刻 `i` 的节点深度 = `max(depth[ma[i]], depth[mi[i]]) + 1`（ma/mi 为 n 表示没有，深度记 0）'


CONFIG = dict(
    num=1902, title='给定二叉搜索树的插入顺序求深度', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='rank 数组 + 单调栈 · 找插入时的前驱后继',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def maxDepthBST(self, order):

        n = len(order)
        rank = [0] * n
        for index, v in enumerate(order):
            rank[v - 1] = index
        
        ma = [n] * n
        mi = [n] * n
        stack = []

        for index, v in enumerate(rank):
            while stack and rank[stack[-1]] > v:
                ma[rank[stack[-1]]] = v
                stack.pop()

            if stack:
                mi[v] = rank[stack[-1]]

            stack.append(index)
        
        depth = [0] * (n + 1)
        for index in range(1, n):
            depth[index] = max(depth[ma[index]], depth[mi[index]]) + 1
            
        return max(depth) + 1
''',
    call='Solution().maxDepthBST([2,6,1,4,3,5])',
    expect=4,
    max_steps=80,
    views=[
        dict(type='array', var='order', label='order（插入顺序）', h=100, cell=46),
        dict(type='array', var='rank', label='rank[值-1] = 插入时刻', h=150, cell=46, pointers={'index': 'blue'}),
        dict(type='array', var='ma', label='ma[t]：后继（更大且更早）的时刻，n=无', h=100, cell=46),
        dict(type='array', var='mi', label='mi[t]：前驱（更小且更早）的时刻，n=无', h=100, cell=46),
        dict(type='stack', var='stack', label='stack（值-1）', h=100),
        dict(type='array', var='depth', label='depth[t]：时刻 t 的节点深度（根记 0）', h=100, cell=46),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'yellow'), ('stack', 'stack', 'cyan')],
    captions={
        'n = len(order)': '`n = {n}`：节点个数',
        'rank = [0]': '`rank[v-1]` 将记录「值 v 是第几个插入的」',
        'rank[v - 1] = index': '值 `{v}` 在时刻 `{index}` 插入 → `rank[{v-1}] = {index}`',
        'ma = [n]': '`ma`、`mi` 先全填 `n`，表示「没有这样的邻居」',
        'mi = [n]': '`mi` 同样先填 `n`',
        'stack = []': '`stack` 保存值（下标）；对 `rank` 做单调栈',
        'for index, v in enumerate(rank)': '按值从小到大扫 `rank`：值 `{index+1}` 的插入时刻 `v = {v}`',
        'while stack and': lambda S, B, r: (f'栈顶值 `{S.stack[-1]+1}` 的时刻 `{S.rank[S.stack[-1]]}` > 当前时刻 `{S.v}`：栈顶更晚插入 → 当前这个比它更早，它的 ma 就是 `{S.v}`' if S.stack and S.rank[S.stack[-1]] > S.v else '栈空或栈顶时刻更早 → 不再弹'),
        'ma[rank[stack[-1]]] = v': '`ma[{B.rank[B.stack[-1]]}] = {v}`：值 `{B.stack[-1]+1}`（时刻 `{B.rank[B.stack[-1]]}`）遇到时刻更早的更大值 `{index+1}` → 它的后继时刻是 `{v}`',
        'stack.pop()': '弹出 → `stack = {stack}`',
        'if stack': lambda S, B, r: (f'栈非空：栈顶值 `{S.stack[-1]+1}` 比当前更小且更早插入 → 记为 mi' if S.stack else '栈空：左边没有更早插入的更小值'),
        'mi[v] = rank[stack[-1]]': '`mi[{v}] = {mi[v]}`：值 `{index+1}`（时刻 `{v}`）的前驱，是栈顶那个更小且更早的值，时刻 `{mi[v]}`',
        'stack.append(index)': '值 `{index+1}` 入栈 → `stack = {stack}`',
        'depth = [0]': '`depth[t]` 记录时刻 `t` 的节点深度，根（时刻 0）深度 0',
        'for index in range(1, n)': lambda S, B, r: (f'按插入时刻 `{S.index}` 依次算深度' if S.index != B.get('index') else '所有时刻都算完了'),
        'depth[index] = max': '时刻 `{index}` 的父亲是前驱 `mi={mi[index]}` 和后继 `ma={ma[index]}`（`{n}` = 无）中较深的一个：`max({B.depth[ma[index]]}, {B.depth[mi[index]]}) + 1` = =={depth[index]}==',
        'return max(depth) + 1': '`depth` 里根记 0，最大值 `{max(depth)}`，题目根深度为 1 → +1，返回 =={ret}==',
    },
    cards=dict(
        one_liner='新节点挂在「前驱、后继」中较深的那个下面',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给一个 `1 ~ n` 的排列 `order`，按顺序依次插入一棵空二叉搜索树',
                 '求最终这棵树的==最大深度==（根深度为 1）',
                 '示例：`[2,6,1,4,3,5]` → `4`'],
        quote='对于一个值v，其插入树的位置取决于已有树中所有小于v的节点中最大的那一个以及所有大于v的节点中最小的那一个中深度较深的那一个。',
        quote_src='—— yiduobo 题解原文',
        idea=['暴力建树 `O(n^2)`；换思路：新值 `v` 的位置由已有节点里它的前驱、后继决定',
              '前驱、后继一定是父子 / 祖孙，`v` 挂在较深者下面',
              '用 `rank` 把「找更早插入的最近邻居」变成经典的单调栈',
              '一遍扫描得到每个节点的 `ma`、`mi`，再按时刻递推深度'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`ma/mi` 的下标都是插入时刻，默认值 `n` 指向 `depth[n] = 0`，所以 `depth` 要开 `n+1`',
                 '最后 `+1`：`depth` 里根的深度记 0',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
