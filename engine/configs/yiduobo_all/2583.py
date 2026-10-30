CONFIG = dict(
    num=2583, title='二叉树中的第 K 大层和', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='层序遍历 · 大小为 K 的小顶堆',
    tags=['灵神题单', '链表树与回溯', '难度分 1374'],
    code='''
class Solution(object):
    def kthLargestLevelSum(self, root, k):

        heap = []
        q = [root]
        head, tail = 0, 1
        while head < tail:
            s = 0
            for now in q[head : tail]:
                s += now.val
                if now.left:
                    q.append(now.left)
                if now.right:
                    q.append(now.right)
            
            heapq.heappush(heap, s)
            if len(heap) > k:
                heapq.heappop(heap)
            
            head, tail = tail, len(q)

        if len(heap) < k:
            return -1
            
        return heap[0]
''',
    call='Solution().kthLargestLevelSum(Tr([5,8,9,2,1,3,7,4,6]), 2)',
    expect=13,
    views=[
        dict(type='tree', label='二叉树（蓝 = 当前 now）', pointers={'now': 'blue'}, path=False, h=240),
        dict(type='array', var=lambda S: [n.val for n in S['q']], label='q（head..tail-1 是当前层）',
             pointers={'head': 'blue'}, window=('head', 'tail - 1'), cell=56, h=200),
        dict(type='heap', var='heap', label='heap（小顶堆，只留最大的 k 个层和）', h=140),
    ],
    watch=[('now', lambda S: S['now'].val if S.get('now') else None, 'blue'), 'head', 'tail', ('s', 's', 'yellow'), ('k', 'k')],
    captions={
        'heap = []': '`heap` 是小顶堆，只保留目前最大的 `k` 个层和；堆顶就是其中最小的，即第 k 大',
        'q = [root]': '`q` 当队列用，`q[head:tail]` 是当前层；先放入根',
        'head, tail = 0, 1': '当前层的范围：`head = 0`，`tail = 1`',
        'while head < tail': lambda S, B, r: (f'当前层有 `{S.tail - S.head}` 个节点 → 处理这一层' if S.head < S.tail else '没有下一层了 → 遍历结束'),
        's = 0': '新的一层，层和 `s` 清零',
        'for now in q': '取出当前层节点 `{now.val}`',
        's += now.val': '`s = {B.s} + {now.val} = {s}`',
        'if now.left': lambda S, B, r: (f'`{S.now.val}` 有左儿子 `{S.now.left.val}` → 入队，留给下一层' if S.now.left else f'`{S.now.val}` 没有左儿子 → 跳过'),
        'if now.right': lambda S, B, r: (f'`{S.now.val}` 有右儿子 `{S.now.right.val}` → 入队，留给下一层' if S.now.right else f'`{S.now.val}` 没有右儿子 → 跳过'),
        'heapq.heappush': '这一层层和 `{s}` 压入堆 → `heap = {heap}`',
        'if len(heap) > k': lambda S, B, r: (f'堆里有 `{len(S.heap)}` 个 > `k = {S.k}` → 弹掉最小的，保证只剩最大的 k 个' if len(S.heap) > S.k else f'堆里 `{len(S.heap)}` 个 ≤ `k = {S.k}` → 不用弹'),
        'heapq.heappop': '弹出堆顶最小值 → `heap = {heap}`',
        'head, tail = tail': '进入下一层：`head = {head}`，`tail = {tail}`',
        'if len(heap) < k': lambda S, B, r: (f'堆只有 `{len(S.heap)}` 个 < `k = {S.k}` → 层数不足，返回 -1' if len(S.heap) < S.k else f'堆里恰好 `{len(S.heap)}` 个 = `k` → 树至少有 k 层'),
        'return heap[0]': '堆里是最大的 k 个层和，==堆顶就是第 k 大== → `{ret}`',
    },
    skip=['return -1'],
    cards=dict(
        one_liner='维护大小为 K 的小顶堆，堆顶就是第 K 大的层和',
        complexity='时间 `O(n + L log k)`（L 为层数），空间 `O(n)`',
        problem=['给你二叉树 `root` 和正整数 `k`，层和是同一层节点值之和',
                 '返回第 `k` 大的层和，少于 `k` 层返回 `-1`',
                 '示例：`[5,8,9,2,1,3,7,4,6]`，`k = 2` → `13`'],
        quote='对于第K大层和的求解，则可以维护一个大小为K的小顶堆，每次将层和加入到堆中，若堆中元素个数超过了K个，那么就将堆顶元素弹出。',
        quote_src='—— yiduobo 题解',
        idea=['层序遍历时，用 `head、tail` 划出当前层，累加层和 `s`',
              '每层的层和压入小顶堆，超过 `k` 个就弹出最小的',
              '最后堆不满 `k` 个说明层数不足；否则堆顶就是答案'],
        result='运行结束，返回 `13`',
        summary=['时间 `O(n + L log k)`，空间 `O(n)`（队列）+ `O(k)`（堆）',
                 '易错：堆里留的是最大的 k 个，所以弹出的是堆顶（最小）',
                 '易错：最后要先判断 `len(heap) < k` 再取 `heap[0]`',
                 '对比灵神：灵神把全部层和排序取 `a[-k]`，yiduobo 用堆只留 k 个'],
    ),
)
