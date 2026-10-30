N, LEFT, RIGHT = 6, [1, 3, -1, -1, -1, -1], [2, 4, 5, -1, -1, -1]


def _col(S, i, v):
    if 'used' in S and S['used'][i]:
        return 'green'
    return None


CONFIG = dict(
    num=1361, title='验证二叉树', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='找唯一入度 0 的根 + BFS 判连通',
    tags=['灵神题单', '拓扑排序'],
    code='''
class Solution(object):
    def validateBinaryTreeNodes(self, n, leftChild, rightChild):

        child_set = set()
        for child in leftChild:
            child_set.add(child)
        for child in rightChild:
            child_set.add(child)
        
        root = None
        for index in range(n):
            if index not in child_set:
                if root is None:
                    root = index
                else:
                    return False
        
        if root is None:
            return False

        q = [root]
        l = 0
        r = 1
        used = [False] * n
        used[root] = True
        while l < r:
            now = q[l]
            l += 1
            if leftChild[now] != -1:
                if used[leftChild[now]]:
                    return False
                used[leftChild[now]] = True
                q.append(leftChild[now])
                r += 1
            if rightChild[now] != -1:
                if used[rightChild[now]]:
                    return False
                used[rightChild[now]] = True
                q.append(rightChild[now])
                r += 1

        return len(q) == n
''',
    call=f'Solution().validateBinaryTreeNodes({N}, {LEFT}, {RIGHT})',
    expect=True,
    views=[
        dict(type='array', var='leftChild', label='leftChild[i]（-1 = 没有）', cell=70, h=150),
        dict(type='set', var='child_set', label='child_set（出现过的孩子 = 有父亲的节点）', fmt=lambda x: str(x), h=130),
        dict(type='array', var='rightChild', label='rightChild[i]', cell=70, h=150),
        dict(type='array', var='used', label='used[i]（绿 = 已被访问）', cell=70, h=165, pointers={'now': 'blue'},
             color=lambda S, i, v: 'green' if v else None),
        dict(type='array', var='q', label='q（BFS 队列，蓝箭头 = l）', cell=70, h=165, pointers={'l': 'pink'}),
    ],
    watch=[('root', 'root', 'yellow'), ('l', 'l', 'pink'), ('r', 'r', 'orange'), ('now', 'now', 'blue')],
    skip=['child_set.add', 'for child in', 'child_set = set()', 'l = 0', 'r = 1', 'r += 1', 'q.append', 'used = ['],
    captions={
        'root = None': '先在所有节点里找「没当过任何孩子」的节点 = 入度 0 = 根',
        'for index in range(n)': lambda S, B, r: (f'检查节点 `{S.index}`' + ('：它是别人的孩子' if S.index in S.child_set else '：没人指向它，是根候选')),
        'if index not in child_set': lambda S, B, r: (f'`{S.index}` 不在 `child_set` → ==入度 0==' if S.index not in S.child_set else f'`{S.index}` 是某个节点的孩子 → 入度 1，跳过'),
        13: lambda S, B, r: ('第一个入度 0 的节点 → 记为根' if S.root is None else f'已经有根 `{S.root}`，又出现入度 0 的 `{S.index}` → 森林，不是树'),
        'root = index': '`root` = {root}',
        'return False': '不满足树的条件，返回 `False`',
        18: lambda S, B, r: ('没有入度 0 的节点 → 一定有环，返回 False' if S.root is None else f'找到唯一的根 `{S.root}`，下面 BFS 验证连通且无重复'),
        'q = [root]': '从根 `{root}` 开始 BFS',
        'used[root] = True': '根标记为已访问',
        'while l < r': lambda S, B, r: (f'队列里还有 {S.r - S.l} 个节点待处理' if S.l < S.r else '队列处理完毕'),
        'now = q[l]': '取出节点 `{now}`，看它的左右孩子',
        'if leftChild[now] != -1': lambda S, B, r: (f'`{S.now}` 有左孩子 `{S.leftChild[S.now]}`' if S.leftChild[S.now] != -1 else f'`{S.now}` 没有左孩子'),
        'if rightChild[now] != -1': lambda S, B, r: (f'`{S.now}` 有右孩子 `{S.rightChild[S.now]}`' if S.rightChild[S.now] != -1 else f'`{S.now}` 没有右孩子'),
        'if used[leftChild[now]]': lambda S, B, r: ('左孩子已被访问过 → 有两个父亲或有环，返回 False' if S.used[S.leftChild[S.now]] else '左孩子第一次见到，没问题'),
        'if used[rightChild[now]]': lambda S, B, r: ('右孩子已被访问过 → 有两个父亲或有环，返回 False' if S.used[S.rightChild[S.now]] else '右孩子第一次见到，没问题'),
        'used[leftChild[now]] = True': '标记左孩子 `{leftChild[now]}` 已访问，并入队',
        'used[rightChild[now]] = True': '标记右孩子 `{rightChild[now]}` 已访问，并入队',
        'l += 1': '`l` → {l}',
        'return len(q) == n': '`len(q) = {len(q)}`，`n = {n}`：BFS 访问到的节点数 == 总数 → 连通 → =={len(q) == n}==',
    },
    cards=dict(
        one_liner='唯一的根 + 每个点只被访问一次 + 全部连通',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 个节点编号 `0..n-1`，`leftChild[i]`、`rightChild[i]` 是 `i` 的左右孩子（-1 表示没有）',
                 '判断这些节点是否恰好构成一棵二叉树',
                 '示例：`n=6, left=[1,3,-1,-1,-1,-1], right=[2,4,5,-1,-1,-1]` → `True`'],
        quote='一颗n个节点的树中，这n个节点必须互相连通，且其中有一个节点的入度为0，其他n - 1个节点的入度都为1。',
        quote_src='—— yiduobo 题解原文',
        idea=['入度：谁出现在 `leftChild/rightChild` 里谁就有父亲，没出现的是根；根必须恰好一个',
              '只看入度不够：可能是「合法二叉树 + 一个环」',
              '所以还要从根 BFS：遇到已访问节点 → False；最后访问数 ≠ n → 不连通'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '没有入度 0 的点 → 有环；入度 0 的点多于 1 个 → 森林',
                 '只数入度会漏掉「树 + 环」，必须再做连通检查',
                 '原文已是 Python 3 可运行写法，无需修改',
                 '本题在拓扑排序题单中：入度为 0 的点才是起点'],
    ),
)
