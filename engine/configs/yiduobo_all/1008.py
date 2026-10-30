PRE = [8, 5, 1, 7, 10, 12]


CONFIG = dict(
    num=1008, title='前序遍历构造二叉搜索树', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='单调栈求 next + 区间递归',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def bstFromPreorder(self, preorder):
        n = len(preorder)
        stack = [n - 1]
        next = [-1]
        for index in range(n - 2, -1, -1):
            while stack and preorder[stack[-1]] < preorder[index]:
                stack.pop()

            if stack:
                next.append(stack[-1])
            else:
                next.append(-1)

            stack.append(index)

        next.reverse()

        return self.build(preorder, 0, n - 1, next)

    def build(self, preorder, l, r, next):
        now = TreeNode(preorder[l])
        if l < r:
            if next[l] > 0 and next[l] <= r:
                if next[l] - 1 > l:
                    now.left = self.build(preorder, l + 1, next[l] - 1, next)

                now.right = self.build(preorder, next[l], r, next)
            else:
                now.left = self.build(preorder, l + 1, r, next)

        return now
''',
    call='tree_list(Solution().bstFromPreorder([8, 5, 1, 7, 10, 12]))',
    expect=[8, 5, 10, 1, 7, None, 12],
    views=[
        dict(type='array', var='preorder', label='前序遍历 preorder（高亮框 = 当前子树区间 [l, r]）', window=('l', 'r'), h=130, cell=72),
        dict(type='array', var=lambda S: S['next'] if isinstance(S.get('next'), list) else [], label='next[i]：第一个比 preorder[i] 大的位置（-1 = 没有）', h=120, cell=72),
        dict(type='stack', var='stack', label='单调栈（存下标，从右往左扫）', fmt=lambda i: f'{i}:{PRE[i]}', h=110),
        dict(type='tree', label='正在构造的 BST（蓝 = now）', pointers={'now': 'blue'}, h=170),
        dict(type='calls', h=130, hide=('preorder', 'next')),
    ],
    watch=[('index', 'index', 'orange'), ('l', lambda S: S['_inner'].get('l'), 'blue'), ('r', lambda S: S['_inner'].get('r'), 'pink'), ('now', lambda S: getattr(S['_inner'].get('now'), 'val', None), 'green')],
    captions={
        'stack = [n - 1]': '从右往左扫：栈里先放最后一个下标 `{n - 1}`；`next[n-1] = -1`（右边没有更大的数）',
        'while stack and': '栈顶 `preorder[{stack[-1]}] = {preorder[stack[-1]]}` 与 `preorder[{index}] = {preorder[index]}` 比：{"栈顶更小 → 它不可能是 index 右边第一个更大的数" if preorder[stack[-1]] < preorder[index] else "栈顶更大 → 它就是 next"}',
        'stack.pop()': '弹掉比 `{preorder[index]}` 小的栈顶 `{B.stack[-1]}`，栈 = `{stack}`',
        'if stack:': '弹完后{"栈非空" if stack else "栈空"} → {"栈顶就是 `next[index]`" if stack else "右边没有更大的数，`next[index] = -1`"}',
        'next.append(stack[-1])': '`next[{index}] = {stack[-1]}`：第一个更大的数是 `preorder[{stack[-1]}] = {preorder[stack[-1]]}`（此时 next 是反着存的）',
        'next.append(-1)': '栈空 → `next[{index}] = -1`',
        'stack.append(index)': '`index = {index}` 入栈，栈 = `{stack}`',
        'next.reverse()': '`next` 是从后往前追加的 → 翻转，变成 `next[i]` 对应 `preorder[i]`：=={next}==',
        'return self.build': '`next` 就绪，递归构造区间 `[0, {n - 1}]`',
        'now = TreeNode': '区间 `[{l}, {r}]`：前序的第一个 `preorder[{l}] = {preorder[l]}` 就是==根==',
        'if l < r:': '区间 `[{l}, {r}]` {"还有别的节点 → 要分左右子树" if l < r else "只剩根自己 → 叶子，直接返回"}',
        'if next[l] > 0 and next[l] <= r:': '`next[{l}] = {next[l]}`：{"在区间内 → 它把 [l+1, r] 分成左段和右段（右段从 next[l] 起）" if 0 < next[l] <= r else "不存在或超出区间 → 没有右子树，[l+1, r] 全是左子树"}',
        'if next[l] - 1 > l:': '左段 `[{l + 1}, {next[l] - 1}]` {"非空 → 递归建左子树" if next[l] - 1 > l else "为空 → 没有左子树"}',
        'now.left = self.build(preorder, l + 1, next[l] - 1': '左子树：区间 `[{B.l + 1}, {B.next[B.l] - 1}]`，值都比 `{preorder[B.l]}` 小',
        'now.right = self.build(preorder, next[l], r': '右子树：区间 `[{B.next[B.l]}, {B.r}]`，值都比 `{preorder[B.l]}` 大',
        'now.left = self.build(preorder, l + 1, r': '没有更大的数 → 整段 `[{B.l + 1}, {B.r}]` 都是左子树',
        'return now': lambda S, B, r: f'`{r.val}` 的左右子树都建好，返回上一层',
    },
    skip=['for index in range', 'if stack:'],
    cards=dict(
        one_liner='用单调栈找「第一个更大的数」，它把区间分成左右子树',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给定二叉搜索树的==前序遍历== `preorder`，还原这棵树',
                 'BST：左子树 < 根 < 右子树',
                 '本视频：`preorder = [8,5,1,7,10,12]` → `[8,5,10,1,7,null,12]`'],
        quote='设其中第一个大于val[l]的位置为next[l]，那么[l + 1, next[l] - 1]就属于左子树，而[next[l], r]则属于右子树。对于next的求解，可以使用经典的单调栈进行求解。',
        quote_src='—— yiduobo 知乎题解',
        idea=['先想到：排序得到中序 + 前序建树，`O(n log n)`；但 BST 的前序本身就带有分割信息',
              '区间 `[l, r]` 的根是 `preorder[l]`，后面先是一段更小的（左），再是更大的（右）',
              '==第一个更大的位置== `next[l]` 就是分界点，用单调栈 `O(n)` 求出，再递归'],
        summary=['时间 `O(n)`：单调栈一趟 + 每个节点建一次；空间 `O(n)`',
                 '边界：左子树为空（`next[l] == l + 1`）、右子树为空（`next[l]` 不存在或 `> r`）要分别判断',
                 '`next` 是从后往前追加的，==别忘了 reverse==',
                 '原文为 Python 2 风格：删去了函数开头的空白行（代码本身未改）'],
    ),
)
