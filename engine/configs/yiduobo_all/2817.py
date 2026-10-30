def _inorder(S):
    tp = S.get('treap')
    if tp is None:
        return None
    if 38 <= S.get('_line', 0) <= 58 and 'index' in S:  # 旋转中途指针暂时不连通，显示逻辑上的有序集合
        return sorted(set(S['nums'][:S['index'] + 1]))
    out = []

    def go(n):
        if n is None:
            return
        go(n.left)
        out.append(n.v)
        go(n.right)
    go(tp.root.right)
    return out


CONFIG = dict(
    num=2817, title='限制条件下元素之间的最小绝对差', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='自写 Treap 平衡树 · 前缀有序查找',
    tags=[],
    setup='import random\nrandom.seed(0)',
    code='''
import random

class Node(object):

    def __init__(self, v):
        self.v = v
        self.left = self.right = None
        self.fa = None
        self.key = random.randint(0, 2147483647)

class Treap(object):

    def __init__(self):
        self.root = Node(0)
        self.root.key = -1
    
    def insert(self, v):
        fa = None
        now = self.root
        while now:
            fa = now
            if now.v == v:
                return
            elif now.v > v:
                now = now.left
            else:
                now = now.right
        
        node = Node(v)
        if fa.v > v:
            fa.left = node
            node.fa = fa
        else:
            fa.right = node
            node.fa = fa
        
        now = node
        while now.key < now.fa.key:
            fa = now.fa
            grand_fa = fa.fa
            if grand_fa.left == fa:
                grand_fa.left = now
            else:
                grand_fa.right = now
            now.fa = grand_fa

            if now == fa.left:
                fa.left = now.right
                if now.right:
                    now.right.fa = fa
                now.right = fa
                fa.fa = now
            else:
                fa.right = now.left
                if now.left:
                    now.left.fa = fa
                now.left = fa
                fa.fa = now

    def find(self, v):
        now = self.root.right
        mi = abs(now.v - v)
        while now:
            mi = min(mi, abs(now.v - v))
            if mi == 0:
                return 0
            if now.v > v:
                now = now.left
            else:
                now = now.right
        
        return mi
    
    def printTree(self):
        print('----------------')
        q = [self.root]
        head, tail = 0, 1
        while head < tail:
            now = q[head]
            head += 1
            print(now.v)
            if now.left:
                print(now.v, now.left.v)
                q.append(now.left)
                tail += 1
            if now.right:
                print(now.v, now.right.v)
                q.append(now.right)
                tail += 1
        print('-------------END-------------')

class Solution(object):
    def minAbsoluteDifference(self, nums, x):

        treap = Treap()
        res = None
        for index, v in enumerate(nums[x:]):
            treap.insert(nums[index])
            t = treap.find(v)
            if res is None or res > t:
                res = t
        
        return res
''',
    call='Solution().minAbsoluteDifference([8, 2, 13, 5], 2)',
    expect=3,
    skip=['self.v = v', 'self.left = self.right', 'self.fa = None', 'self.key = random', 'while now:', 'fa = now.fa', 'grand_fa = fa.fa', 'now.fa = grand_fa', 'node.fa = fa', 'fa = now', 'now.right.fa = fa', 'now.left.fa = fa', 'fa.fa = now'],
    max_steps=90,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 刚插入树里的 nums[index]，粉 = 当前要查询的 v）', cell=84, h=210,
             color=lambda S, i, v: ('blue' if i == S.get('index') else 'pink' if 'index' in S and 'x' in S and i == S['index'] + S['x'] else None)),
        dict(type='array', var=_inorder, label='Treap 中序（= 已插入元素从小到大排序）', cell=84, h=210, index=False),
        dict(type='text', size=28, fn=lambda S: (f"可配对的前缀是 `nums[0..{S['index']}]`，要在树里找离 `nums[{S['index'] + S['x']}]` 最近的数" if 'index' in S and 'x' in S and 'res' in S else '')),
    ],
    watch=['x', 'index', ('res', 'res', 'green')],
    captions={
        95: '建一棵 Treap（平衡二叉搜索树）；根是值为 0 的哨兵，真正的数都挂在 `root.right` 下',
        96: '`res` 记录目前最小的差，先设为空',
        97: '`v = nums[index + x]`，它能配对的是前缀 `nums[0..index]`，下标差正好 `>= x`',
        98: '把 `nums[index]` 插入有序结构：新进入前缀的数',
        18: '从根往下找插入位置：`fa` 记录父节点，`now` 是当前节点',
        22: '`now.v = {now.v}` 和 `v = {v}` 相比 → {"相等，已存在，不用重复插入" if now.v == v else "不相等，继续往下"}',
        24: '`{now.v} > {v}` → {"成立，插入位置在左子树，往左走" if now.v > v else "不成立，往右子树走"}',
        25: '往左走：`now = {now.v if now else None}`',
        27: '往右走：`now = {now.v if now else None}`',
        29: '找到空位，新建节点 `{v}`，随机给它一个优先级 `key`',
        30: '和父节点 `{fa.v}` 比：`{fa.v} > {v}` → {"成立，挂左边" if fa.v > v else "不成立，挂右边"}',
        31: '挂到 `{fa.v}` 的左边',
        34: '挂到 `{fa.v}` 的右边',
        37: '从新节点开始检查是否要旋转',
        38: '堆性质：子节点 `key` 不能比父节点小；比父小就旋转上去，保持树平衡',
        41: '把新节点换到祖父节点下面：先看父节点原来是祖父的哪一边',
        47: '新节点是父节点的{"左" if now == fa.left else "右"}孩子 → 做{"右" if now == fa.left else "左"}旋转，新节点升到父节点上方',
        61: '`find`：从树根（`root.right`）开始，二叉搜索找最接近 `v = {v}` 的数',
        62: '先用起点 `{now.v}` 初始化最小差：`mi = |{now.v} - {v}| = {mi}`',
        64: '路上每个节点都可能是最近邻：`mi = min(.., |{now.v} - {v}|)` = =={mi}==',
        65: '差为 {mi}，{"已经是 0，不可能更小，直接返回" if mi == 0 else "还不是 0，继续往下找"}',
        67: '`{now.v} > {v}` → {"当前数偏大，答案可能在左边，往左走" if now.v > v else "当前数偏小，往右走"}',
        68: '往左走：`now = {now.v if now else None}`',
        70: '往右走：`now = {now.v if now else None}`',
        72: '搜索路径走完，和 `v = {v}` 最近的距离 =={mi}==',
        99: '调用 `find(v)`：在树里找离 `v` 最近的数，返回它们的差 `t`',
        100: '`res = {B.res}`，`t = {t}` → {"更新答案" if (B.res is None or B.res > t) else "不更新"}',
        101: '最小差更新：`res = {res}`',
        103: '所有 `v` 都查完，最小差 =={ret}==',
    },
    cards=dict(
        one_liner='枚举 v，前缀装进 Treap，查树里最接近 v 的数',
        complexity='时间 `O((n-x) log n)`（期望），空间 `O(n)`',
        problem=['找下标距离至少为 `x` 的两个数，使差的绝对值最小',
                 '示例：`nums = [4,3,2,4], x = 2` → `0`',
                 '视频用 `[8,2,13,5], x = 2` → `3`'],
        quote='python没有原生的平衡二叉树，但是可以使用sorted_list来处理。由于本题只需要处理插入和查找这两种操作，所以我还是选择自己写treap来实现。',
        quote_src='—— yiduobo 题解',
        idea=['`nums[i]` 只能和前缀 `nums[0..i-x]` 配对，前缀每步只多一个数',
              '数据和数值范围都很大，没法离散化，必须动态维护有序性',
              '手写 Treap：二叉搜索树 + 随机优先级旋转，只需要插入和查找最接近值'],
        summary=['期望时间 `O((n-x) log n)`，空间 `O(n)`；Treap 靠随机优先级保持平衡',
                 '原文为 Python 2 写法，`printTree` 里的 `print x` 已改为 `print(x)`（调试用，主流程不调用）',
                 '易错点：根是值为 0 的哨兵，`find` 要从 `root.right` 开始',
                 '视频里 `random.seed(0)` 固定随机优先级，结果与种子无关'],
    ),
)
