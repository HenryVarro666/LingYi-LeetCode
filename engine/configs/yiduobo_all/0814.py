def nv(x):
    return '空' if x is None else str(x.val)


def cap_left(S, B, ret):
    return f'递归处理 `now={S.now.val}` 的左子树 `{nv(S.now.left)}`：返回它里面==是否含有 1=='


def cap_right(S, B, ret):
    return f'左边结果 `left = {B.left}` 已记下；再递归右子树 `{nv(S.now.right)}`，结果存进 `right`'


def cap_final(S, B, ret):
    n = S.now
    left, right = S.left, S.right
    if left or right or n.val == 1:
        why = '左子树有 1' if left else '右子树有 1' if right else '自己的值是 1'
        return f'节点 `{n.val}`：{why} → 这棵子树要保留，返回 `True`'
    return f'节点 `{n.val}`：左 `{left}`、右 `{right}`、自己 `{n.val}` 都没有 1 → 整棵子树可以剪掉，返回 `False`'


CONFIG = dict(
    num=814, title='二叉树剪枝', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='后序递归 · 子树是否含 1',
    tags=['灵神核心路线', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def pruneTree(self, root):

        if(self.remove(root)):
            return root
        return None
    
    def remove(self, now):
        if not now:
            return False
        
        left = self.remove(now.left)
        if not left:
            now.left = None
        
        right = self.remove(now.right)
        if not right:
            now.right = None
        
        if left or right or (now.val == 1):
            return True

        return False
''',
    call='''s = Solution()
s.tree = Tr([1,0,1,0,None,None,1])
s.pruneTree(s.tree)''',
    expect=[1, None, 1, None, 1],
    result_fn=tree_list,
    views=[
        dict(type='tree', label='二叉树（绿 = 值为 1，剪掉的子树会从图中消失）', pointers={'now': 'blue'}, h=400,
             color=lambda S, n: 'green' if n.val == 1 else None),
        dict(type='calls', h=210),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'blue'),
           ('left', lambda S: S['_inner'].get('left')),
           ('right', lambda S: S['_inner'].get('right'))],
    captions={
        'if(self.remove(root))': '从根开始判断：整棵树里有没有 1？没有就整棵返回空',
        'if not now': lambda S, B, r: ('空节点 → 没有 1，==递归边界==，返回 `False`' if S.now is None
                                       else f'节点 `{S.now.val}` 非空 → 继续看它的左右子树'),
        'return False': lambda S, B, r: ('空节点：返回 `False`，告诉上一层这边没有 1' if S.now is None
                                         else f'节点 `{S.now.val}` 的整棵子树都没有 1 → 返回 `False`，让父节点断开它'),
        'left = self.remove': cap_left,
        'if not left': lambda S, B, r: (f'左子树里没有 1 → 下一行把 `now.left` 置空，剪掉它'
                                        if not S.left else '左子树里有 1 → 保留，不动'),
        'now.left = None': '`now.left = None`：断开左子树，整棵子树被剪掉',
        'right = self.remove': cap_right,
        'if not right': lambda S, B, r: (f'右子树里没有 1 → 下一行把 `now.right` 置空，剪掉它'
                                         if not S.right else '右子树里有 1 → 保留，不动'),
        'now.right = None': '`now.right = None`：断开右子树，整棵子树被剪掉',
        'if left or right': cap_final,
        'return True': lambda S, B, r: f'节点 `{S.now.val}` 子树里有 1 → 返回 `True`，父节点要保留这条边',
        'return root': '整棵树里有 1，返回剪好的 `root`',
        'return None': '整棵树都没有 1 → 返回空树',
    },
    cards=dict(
        one_liner='递归返回「这棵子树里有没有 1」，没有就剪掉',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['二叉树每个节点值是 `0` 或 `1`，把不含 `1` 的子树全部剪掉',
                 '剪完后每棵子树都至少含一个 `1`',
                 '示例：`[1,0,1,0,null,null,1]` → `[1,null,1,null,1]`'],
        quote='若left_flag为false，那么置now.left为空。若right_flag为false，那么置now.right为空。最后若left_flag为true，或者right_flag为true，或者当前节点值为1，那么返回true，否则返回false。',
        quote_src='—— yiduobo 题解原文',
        idea=['`remove(now)` 返回：以 `now` 为根的子树里有没有 `1`',
              '先递归左右子树，没有 1 的一侧直接 `= None` 断开',
              '左有、右有、或自己是 1，就返回 `True`，否则让父节点剪掉自己'],
        summary=['时间 `O(n)`：每个节点访问一次；空间 `O(h)`',
                 '易错：必须先递归子树、再判断自己，也就是==后序==；先看自己会剪错',
                 '根节点没有 1 时要返回 `None`，所以 `pruneTree` 里要看 `remove(root)` 的结果',
                 '原文代码未改动（本来就是 Python 3 可运行）'],
    ),
)
