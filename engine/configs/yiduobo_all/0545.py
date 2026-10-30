def _lists(S):
    return S.get('left') or [], S.get('right') or [], S.get('leaf') or []


def color(S, n):
    L_, R_, F_ = _lists(S)
    if n.val in L_:
        return 'blue'
    if n.val in R_:
        return 'pink'
    if n.val in F_:
        return 'green'
    return None


def lines_fn(S):
    L_, R_, F_ = _lists(S)
    return f'左边界 `left = {L_}`    右边界 `right = {R_}`    叶子 `leaf = {F_}`'


def cap_while(side):
    def f(S, B, ret):
        n = S.now
        if n.left or n.right:
            return f'`{n.val}` 不是叶子（还有孩子）→ 属于{side}边界，继续向下'
        return f'`{n.val}` 是叶子 → 叶子留给先序遍历收集，{side}边界到此结束'
    return f


def cap_leaf(S, B, ret):
    n = B.now
    if not n.left and not n.right:
        return f'`{n.val}` 没有左右孩子 → 是叶子节点'
    return f'`{n.val}` 有孩子 → 不是叶子，继续递归左右子树'


CONFIG = dict(
    num=545, title='二叉树的边界', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='迭代左右边界 + 先序收集叶子',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def boundaryOfBinaryTree(self, root):

        left = []
        right = []
        leaf = []

        if root.left:
            now = root.left
            while now.left or now.right:
                left.append(now.val)
                if now.left:
                    now = now.left
                else:
                    now = now.right
        
        if root.right:
            now = root.right
            while now.left or now.right:
                right.append(now.val)
                if now.right:
                    now = now.right
                else:
                    now = now.left
            right.reverse()

        def dfs(now):
            if not now.left and not now.right:
                if now != root:
                    leaf.append(now.val)
            else:
                if now.left:
                    dfs(now.left)
                if now.right:
                    dfs(now.right)
        
        dfs(root)
        return [root.val] + left + leaf + right
''',
    call='''s = Solution()
s.tree = Tr([1,2,3,4,5,6,7,8])
s.boundaryOfBinaryTree(s.tree)''',
    expect=[1, 2, 4, 8, 5, 6, 7, 3],
    views=[
        dict(type='tree', label='二叉树（蓝 = 左边界，粉 = 右边界，绿 = 叶子；黄圈 = 递归路径）', pointers={'now': 'blue'}, h=250, color=color),
        dict(type='text', fn=lines_fn, size=24, h=50),
        dict(type='calls', h=210),
    ],
    watch=[('now', lambda S: S.get('now').val if S.get('now') else None, 'yellow'),
           ('left', lambda S: S.get('left'), 'blue'),
           ('right', lambda S: S.get('right'), 'pink'),
           ('leaf', lambda S: S.get('leaf'), 'green')],
    captions={
        4: '三个数组：`left` 左边界、`right` 右边界、`leaf` 叶子，最后和根拼起来',
        8: lambda S, B, r: ('根有左孩子 → 左边界从 `root.left` 开始向下迭代' if B.root.left else '根没有左孩子 → 左边界为空'),
        9: '`now` 从 `root.left = {now.val}` 出发',
        10: cap_while('左'),
        11: '`{now.val}` 加入左边界 → `left = {left}`',
        12: lambda S, B, r: ('有左孩子 → ==优先往左==走' if B.now.left else '没有左孩子，只能往右走'),
        13: '往左：`now = {now.val}`',
        15: '没有左孩子，改走右孩子：`now = {now.val}`',
        17: lambda S, B, r: ('根有右孩子 → 右边界与左边界对称，从 `root.right` 开始' if B.root.right else '根没有右孩子 → 右边界为空'),
        18: '`now` 从 `root.right = {now.val}` 出发',
        19: cap_while('右'),
        20: '`{now.val}` 加入右边界 → `right = {right}`',
        21: lambda S, B, r: ('有右孩子 → ==优先往右==走' if B.now.right else '没有右孩子，只能往左走'),
        22: '往右：`now = {now.val}`',
        24: '没有右孩子，改走左孩子：`now = {now.val}`',
        25: '右边界要求==自下而上==，翻转：`right = {right}`',
        28: cap_leaf,
        29: lambda S, B, r: (f'`{B.now.val}` 不是根 → 可以收集' if B.now != B.root else '它是根，根单独处理，不算叶子'),
        30: '叶子 `{now.val}` 加入 `leaf` → `{leaf}`（先序遍历，天然==从左到右==）',
        32: lambda S, B, r: ('有左孩子 → 递归左子树' if B.now.left else '没有左孩子'),
        34: lambda S, B, r: ('有右孩子 → 递归右子树' if B.now.right else '没有右孩子'),
        33: lambda S, B, r: f'进入左孩子 `{B.now.left.val}`',
        35: lambda S, B, r: f'进入右孩子 `{B.now.right.val}`',
        37: '从根开始先序遍历，收集叶子',
        38: '拼接：根 `{root.val}` + 左边界 `{left}` + 叶子 `{leaf}` + 逆序右边界 `{right}` = =={ret}==',
    },
    skip=[5, 6],
    cards=dict(
        one_liner='边界 = 根 + 左边界 + 叶子 + 逆序右边界，分开求再拼起来',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈，不含结果）',
        problem=['给你二叉树的根 `root`，按逆时针顺序返回边界节点',
                 '边界 = 根 + 左边界 + 叶子（从左到右）+ 右边界（自下而上）',
                 '本视频：`root = [1,2,3,4,5,6,7,8]` → `[1,2,4,8,5,6,7,3]`'],
        quote='由于右边界的定义方式与左边界完全对称，在这里只需要考虑左边界的求解方法，然后反过来就可以得到右边界的求解方法了。',
        quote_src='—— yiduobo 题解',
        idea=['左边界：从 `root.left` 向下，非叶子就记录，优先走左孩子，没有再走右孩子',
              '右边界对称：优先走右孩子；记录完再 `reverse()`，得到自下而上',
              '叶子：先序遍历，叶子天然从左到右；根不算叶子'],
        result='返回 `[1, 2, 4, 8, 5, 6, 7, 3]`：根 1，左边界 2、4，叶子 8、5、6、7，右边界 3',
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '易错：边界上的叶子不放进 `left`/`right`（`while` 条件排除），只由 `dfs` 收集一次，避免重复',
                 '易错：根只有一个孩子或为叶子时，不能把根重复算进叶子（`now != root`）',
                 '右边界要 `reverse()`，叶子顺序靠先序遍历保证'],
    ),
)
