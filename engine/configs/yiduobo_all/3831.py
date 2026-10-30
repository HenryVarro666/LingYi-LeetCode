def _cur(S):
    q = S.get('q')
    if q is None or 'head' not in S:
        return set()
    return {id(n) for n in q[S['head']:S['tail']]}


def _info(S):
    if 'curr' not in S:
        return '层序遍历，走到第 `level` 层，取这层正中间的节点'
    return f"已走到第 `{S['curr']}` 层（目标第 `{S['level']}` 层），当前层有 `{S['tail'] - S['head']}` 个节点"


CONFIG = dict(
    num=3831, title='二叉搜索树某一层的中位数', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='层序遍历 · 取中间节点',
    tags=['链表树与回溯'],
    code='''
class Solution(object):
    def levelMedian(self, root, level):
        
        q = [root]
        curr = 0
        head, tail = 0, 1

        while head < tail and curr < level:
            for x in q[head : tail]:
                if x.left:
                    q.append(x.left)
                if x.right:
                    q.append(x.right)
            
            head, tail = tail, len(q)
            curr += 1
        
        if curr < level or head == tail:
            return -1
        return q[head + (tail - head) // 2].val
''',
    call='Solution().levelMedian(Tr([4, 2, 6, 1, 3, 5, 7]), 2)',
    expect=5,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='tree', label='二叉搜索树（蓝 = 当前层，黄 = 正在展开的节点）', pointers={'x': 'yellow'}, path=False, h=330,
             color=lambda S, n: 'blue' if id(n) in _cur(S) else None),
        dict(type='array', var=lambda S: [n.val for n in S['q']] if 'q' in S else [], label='队列 q（存节点值，天然从左到右有序）',
             pointers={'head': 'blue', 'tail': 'pink'}, cell=72, h=170),
    ],
    watch=[('level', 'level', 'yellow'), ('curr', 'curr', 'blue'), ('head', 'head', 'blue'), ('tail', 'tail', 'pink')],
    captions={
        'q = [root]': '队列从根开始：根在第 0 层',
        'curr = 0': '`curr` 记录 `q[head:tail]` 当前是第几层：现在是第 `{curr}` 层',
        'head, tail = 0, 1': '`q[head:tail]` 圈出当前层：第 0 层只有根',
        'while head < tail': lambda S, B, r: (f'`head = {S.head} < tail = {S.tail}` 且 `curr = {S.curr} < level = {S.level}` → 还没到目标层，继续往下走'
                                              if S.head < S.tail and S.curr < S.level
                                              else (f'`curr = {S.curr}` 已到第 `level = {S.level}` 层 → 停下' if S.curr >= S.level
                                                    else '这一层已经没有节点 → 停下')),
        'for x in q[head : tail]': lambda S, B, r: ('这一层的孩子都入队了' if getattr(B.get('x'), '_uid', 0) == getattr(S.get('x'), '_uid', 1)
                                                    else f'取当前层节点 `x = {S.x.val}`，把它的孩子放进下一层'),
        'if x.left': lambda S, B, r: (f'`{S.x.val}` 有左孩子 `{S.x.left.val}`' if S.x.left else f'`{S.x.val}` 没有左孩子'),
        'if x.right': lambda S, B, r: (f'`{S.x.val}` 有右孩子 `{S.x.right.val}`' if S.x.right else f'`{S.x.val}` 没有右孩子'),
        'q.append(x.left)': '==先左后右==入队：保证同一层按树中从左到右排列，即值从小到大',
        'q.append(x.right)': '右孩子紧跟在左孩子后面入队',
        'head, tail = tail, len(q)': '下一层是 `q[{head}:{tail}]`，共 `{tail - head}` 个节点',
        'curr += 1': '层数加一：`curr = {curr}`',
        'if curr < level or head == tail': lambda S, B, r: ('层数不够或这一层是空的 → 返回 -1' if S.curr < S.level or S.head == S.tail
                                                            else f'正好走到第 `{S.level}` 层且非空 → 取这层中间的节点'),
        'return -1': '该层不存在 → `-1`',
        'return q[head': lambda S, B, r: (f'这层 `{S.tail - S.head}` 个节点，中间靠右的下标 `head + {(S.tail - S.head) // 2} = {S.head + (S.tail - S.head) // 2}` → 值 ==`{r}`==（偶数个取靠右的）'),
    },
    cards=dict(
        one_liner='BFS 先左后右，每层天然有序，直接取正中间',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给你一棵二叉搜索树的根 `root` 和整数 `level`，根在第 0 层',
                 '返回第 `level` 层所有节点值的==中位数==',
                 '该层不存在或没有节点返回 `-1`；个数为偶数时取==中间靠右==的值',
                 '本视频：`[4,2,6,1,3,5,7]`，`level = 2` → 该层 `1 3 5 7`，答案 `5`'],
        quote='如果在层序遍历的bfs时，严格按照先左后右的顺序将孩子节点加入到bfs队列，那么队列中每一层对应的节点就必然是按照树中从左到右的顺序排好的，也就是说这些节点是天然有序的。',
        quote_src='—— yiduobo 题解原文',
        idea=['二叉搜索树中序有序：同一层从左到右，值也是从小到大',
              '先左后右的 BFS 正好按这个顺序排队，不用再排序',
              '走到第 `level` 层后，`q[head:tail]` 就是有序数组，取下标 `head + (tail-head)//2`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '个数偶数时 `(tail-head)//2` 正好是中间靠右；奇数时就是正中间',
                 '循环提前结束有两种情形：层数不够（某层已空），或到达目标层；最后统一判断',
                 '原文中的 `//` 已是整数除法，代码无需修改'],
    ),
)
