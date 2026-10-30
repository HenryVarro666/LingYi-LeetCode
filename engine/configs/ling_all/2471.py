CONFIG = dict(
    num=2471, title='逐层排序二叉树所需的最少操作数目', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='BFS 分层 + 置换环',
    tags=['链表树与回溯', '难度分 1635'],
    code='''
class Solution:
    def minimumOperations(self, root: Optional[TreeNode]) -> int:
        ans, q = 0, [root]
        while q:
            a = []
            tmp = q
            q = []
            for node in tmp:
                a.append(node.val)
                if node.left: q.append(node.left)
                if node.right: q.append(node.right)

            n = len(a)
            a = sorted(range(n), key=lambda i: a[i])  # 离散化

            ans += n
            vis = [False] * n
            for v in a:
                if vis[v]: continue
                while not vis[v]:
                    vis[v] = True
                    v = a[v]
                ans -= 1
        return ans
''',
    call='''root = Tr([1,4,3,7,6,8,5])
Solution().minimumOperations(root)''',
    expect=3,
    views=[
        dict(type='tree', var='root', label='二叉树', path=False, h=230,
             color=lambda S, nd: 'yellow' if any(x is nd for x in (S.get('tmp') or [])) else None),
        dict(type='array', var='a', label='a：本层节点值 → 离散化后变成「排好序时的下标」', h=150,),
        dict(type='array', var='vis', label='vis：置换环里走过的下标（蓝箭头 = v）', pointers={'v': 'blue'}, h=170,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='text', fn=lambda S: f"==环的大小 − 1== 就是这个环要的交换次数；本层 n = {S['n']}，ans = n − 环数" if 'n' in S and 'vis' in S else '', size=24, h=50),
    ],
    watch=[('ans', 'ans', 'green'), ('n', 'n', 'pink'), ('v', 'v', 'blue')],
    captions={
        'ans, q = 0': '`ans` 累计交换次数；`q` 是当前层的节点，从根开始',
        'tmp = q': '`tmp` 拿走当前层的节点：`{[x.val for x in tmp]}`',
        'q = []': '`q` 清空，准备装下一层的节点',
        'a = []': '开始处理新的一层，`a` 收集这一层的节点值',
        'a.append(node.val)': '取出节点值 `{node.val}`：交换的是==值==，不会影响下一层的节点顺序，所以层与层互不相干',
        'q.append(node.left)': '左儿子 `{node.left.val}` 进入下一层',
        'q.append(node.right)': '右儿子 `{node.right.val}` 进入下一层',
        'n = len(a)': '这一层共 `{n}` 个节点：`a = {a}`',
        'a = sorted': '离散化：`a[k]` 变成「第 k 小的值原来在哪个位置」→ `a = {a}`。位置 `v` 的数应该去 `a[v]`，连成置换环',
        'ans += n': '先假设每个点自成一个环，需要 `n = {n}` 次（后面每找到一个环就减 1）：`ans = {ans}`',
        'vis = [False]': '`vis` 记录哪些下标已经在某个环里',
        'for v in a': '枚举下一个 `v`：从它出发找环',
        'if vis[v]': lambda S, B, r: (f'`vis[{S.v}]` 已走过 → 它在之前的环里，跳过' if S.vis[S.v] else f'`vis[{S.v}]` 没走过 → 发现一个新环，沿着 `a` 走一圈'),
        'vis[v] = True': '标记 `{v}` 已访问',
        'v = a[v]': '跳到 `a[{B.v}] = {v}`，沿环走，回到起点就结束',
        'ans -= 1': '环走完：大小为 k 的环要 k−1 次交换 = k 次 − 1 → `ans = {ans}`',
        'return ans': '所有层都处理完，最少交换 `{ans}` 次',
    },
    cards=dict(
        one_liner='每层离散化成排列，数置换环：交换次数 = 大小 − 1',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每次操作可以交换==同一层==任意两个节点的值，节点值互不相同',
                 '求让每一层都严格递增的最少操作次数',
                 '示例：`[1,3,2,7,6,5,4]` → `3`；本视频用 `[1,4,3,7,6,8,5]` → `3`'],
        quote='这是一个经典问题，做法是置换环。……对于每个环，交换次数为环的大小减一。代码实现时需要离散化。',
        quote_src='—— 灵茶山艾府题解',
        idea=['BFS 一层层取出节点值；交换值不影响下层，层之间独立',
              '把本层值排名（离散化），得到一个排列，排列由若干环组成',
              '环内交换即可，大小 k 的环需要 `k - 1` 次；`ans = n - 环数`'],
        summary=['时间 `O(n log n)`：瓶颈在每层排序；空间 `O(n)`',
                 '写法技巧：先 `ans += n`，每个环再 `-= 1`，省去统计环大小',
                 '易错：`a` 被重新赋值成排序后的下标，之后 `v` 访问的是下标而不是原值',
                 '相似题：765 情侣牵手（同样是置换环 / 并查集）'],
    ),
)
