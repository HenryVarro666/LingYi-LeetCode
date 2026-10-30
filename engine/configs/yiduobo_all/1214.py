V1 = [0, -10, 10]
V2 = [5, 1, 7, 0, 2]
TARGET = 6


def _top(S, key):
    """这棵树当前最上面的节点（树被一路改写，root 变量已经不在顶上了）"""
    nodes = S[key]
    kids = set()
    for n in nodes:
        for c in (n.left, n.right):
            if c is not None:
                kids.add(c._uid)
    for n in nodes:
        if n._uid not in kids:
            return n
    return nodes[0]   # 改写的中途出现临时的环：随便取一个


def _info(S):
    ln = S.get('_line', 0)
    p1, p2 = S.get('p1'), S.get('p2')
    if p1 is not None and p2 is not None and ln >= 31:
        return f"`p1.val + p2.val = {p1.val} + {p2.val} = ` ==`{p1.val + p2.val}`==，目标 `{S['target']}`"
    return '左树正序（小→大）、右树倒序（大→小）：和偏小就让 p1 变大，偏大就让 p2 变小'


def _col1(S, n):
    return 'blue' if n is S.get('p1') else None


def _col2(S, n):
    return 'pink' if n is S.get('p2') else None


CONFIG = dict(
    num=1214, title='查找两棵二叉搜索树之和', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='Morris 式改树 + 一棵正序一棵倒序的双指针',
    tags=['常用数据结构', '链表树与回溯'],
    code='''
class Solution(object):
    def twoSumBSTs(self, root1, root2, target):

        def maintainLeft():
            nonlocal p1

            while p1.left:
                rightest = p1.left
                while rightest.right:
                    rightest = rightest.right
            
                rightest.right = p1
                p1 = p1.left
                rightest.right.left = None
        
        def maintainRight():
            nonlocal p2

            while p2.right:
                leftest = p2.right
                while leftest.left:
                    leftest = leftest.left
            
                leftest.left = p2
                p2 = p2.right
                leftest.left.right = None
        

        p1 = root1
        p2 = root2
        maintainLeft()
        maintainRight()

        while p1 and p2:
            s = p1.val + p2.val
            if s == target:
                return True
            
            if s < target:
                p1 = p1.right
                if not p1:
                    break
                maintainLeft()
            else:
                p2 = p2.left
                if not p2:
                    break
                maintainRight()
        
        return False
''',
    call=f'''s = Solution()
t1 = Tr({V1!r})
t2 = Tr({V2!r})
def _all(r):
    return [] if r is None else [r] + _all(r.left) + _all(r.right)
s.nodes1 = _all(t1)
s.nodes2 = _all(t2)
s.twoSumBSTs(t1, t2, {TARGET})''',
    expect=False,
    views=[
        dict(type='tree', var=lambda S: _top(S, 'self.nodes1'), label='root1（蓝 = p1，从最小的开始正序）', path=False,
             pointers={'p1': 'blue', 'rightest': 'yellow'}, color=_col1, h=230),
        dict(type='tree', var=lambda S: _top(S, 'self.nodes2'), label='root2（粉 = p2，从最大的开始倒序）', path=False,
             pointers={'p2': 'pink', 'leftest': 'yellow'}, color=_col2, h=300),
        dict(type='text', fn=_info, size=26, h=80),
    ],
    watch=[('target', 'target', 'yellow'), ('s', 's', 'green')],
    captions={
        'nonlocal p1': '`p1` 是外层函数的变量，这个函数要改它',
        'nonlocal p2': '`p2` 同理',
        'while p1.left': lambda S, B, r: (f'`p1 = {S.p1.val}` 还有左子树 → 继续把它改成 ==链==' if S.p1.left else f'`p1 = {S.p1.val}` 没有左子树了：它就是当前最小的节点'),
        'rightest = p1.left': '找 `p1` 左子树里最右（最大）的节点，从 `{rightest.val}` 开始',
        'while rightest.right': lambda S, B, r: (f'`{S.rightest.val}` 还有右儿子 → 继续往右' if S.rightest.right else f'`{S.rightest.val}` 已是最右 → 它是 `p1` 的中序前驱'),
        'rightest = rightest.right': '往右走：`rightest = {rightest.val}`',
        'rightest.right = p1': '把 `p1` 挂到前驱的右边：==左子树整个提到 p1 上面==，`{rightest.val}.right = {p1.val}`',
        'p1 = p1.left': '`p1` 下移到原来的左儿子 `{p1.val}`',
        'rightest.right.left = None': '断开 `{rightest.right.val}` 原来的左边：不然会形成环',
        'while p2.right': lambda S, B, r: (f'`p2 = {S.p2.val}` 还有右子树 → 继续改' if S.p2.right else f'`p2 = {S.p2.val}` 没有右子树了：它就是当前最大的节点'),
        'leftest = p2.right': '找 `p2` 右子树里最左（最小）的节点，从 `{leftest.val}` 开始',
        'while leftest.left': lambda S, B, r: (f'`{S.leftest.val}` 还有左儿子 → 继续往左' if S.leftest.left else f'`{S.leftest.val}` 已是最左 → 它是 `p2` 的中序后继'),
        'leftest = leftest.left': '往左走：`leftest = {leftest.val}`',
        'leftest.left = p2': '把 `p2` 挂到后继的左边：==右子树整个提到 p2 上面==',
        'p2 = p2.right': '`p2` 下移到原来的右儿子 `{p2.val}`',
        'leftest.left.right = None': '断开 `{leftest.left.val}` 原来的右边',
        'p1 = root1': '`p1` 从 `root1` 出发',
        'p2 = root2': '`p2` 从 `root2` 出发',
        'maintainLeft()': lambda S, B, r: ('`p1` 一路向左改树，直到停在最小节点' if S.p1 is B.p1 or True else ''),
        'maintainRight()': '`p2` 一路向右改树，直到停在最大节点',
        'while p1 and p2': lambda S, B, r: ('两个指针都还在树里 → 继续' if S.p1 and S.p2 else '有一棵树走完了'),
        's = p1.val + p2.val': '`p1` 最小 + `p2` 最大：`{p1.val} + {p2.val}` = =={s}==',
        'if s == target': lambda S, B, r: (f'`{S.s} == {S.target}` → 找到了' if S.s == S.target else f'`{S.s} != {S.target}`，看大小关系'),
        'if s < target': lambda S, B, r: (f'`{S.s} < {S.target}`：和偏小 → 让 `p1` 取更大的值' if S.s < S.target
                                          else f'`{S.s} > {S.target}`：和偏大 → 让 `p2` 取更小的值'),
        'p1 = p1.right': '`p1` 走到中序的下一个（因为已改成链，直接 `.right`）：`{p1.val}`' ,
        'p2 = p2.left': '`p2` 走到中序的上一个：`{p2.val}`',
        'if not p1': lambda S, B, r: ('`p1` 走出了树 → 没有更大的数可选了，退出' if not S.p1 else '`p1` 还在树里'),
        'if not p2': lambda S, B, r: ('`p2` 走出了树 → 没有更小的数可选了，退出' if not S.p2 else '`p2` 还在树里'),
        'break': '退出循环',
        'return False': '指针耗尽也没凑出 `target` → ==返回 False==',
        'return True': '找到了 → 返回 True',
    },
    cards=dict(
        one_liner='把两棵 BST 改成"可顺着走"的链：一棵从小到大，一棵从大到小',
        complexity='时间 `O(n + m)`，空间 `O(1)`',
        problem=['给两棵二叉搜索树和整数 `target`',
                 '是否各取一个节点，使两个节点的值之和等于 `target`',
                 '示例：`[2,1,4]`、`[1,0,3]`、`5` → `true`',
                 '本视频：`[0,-10,10]`、`[5,1,7,0,2]`、`6` → `false`'],
        quote='最直观的做法是对其中一棵树进行遍历，使用哈希表储存其中出现的所有节点值……不过上面的做法没有利用到二叉搜索树的性质，需要想办法将中序遍历运用起来。',
        quote_src='—— yiduobo 题解原文',
        idea=['哈希表法要 `O(n)` 额外空间；BST 的中序是有序的，可以用双指针',
              '用 94 题的改树技巧（左子树最右节点挂回去），不用栈就能迭代中序',
              '一棵树正序遍历，另一棵==倒序==遍历（对右子树最左节点做同样处理）',
              '和偏小：`p1` 往大走；和偏大：`p2` 往小走'],
        summary=['时间 `O(n + m)`，空间 `O(1)`（但会破坏原树）',
                 '原文用 `global p1, p2`，Python 3 里已改为 `nonlocal p1` / `nonlocal p2`，外层去掉 `global`',
                 '易错：倒序那棵树要处理的是==右子树的最左节点==',
                 '每一步有一个指针单向移动，两个指针各最多走 n、m 步',
                 '原文先提到哈希表法，这题的重点是 `O(1)` 空间的双指针'],
    ),
)
