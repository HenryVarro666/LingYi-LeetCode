CONFIG = dict(
    num=1302, title='层数最深的叶子节点的和', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='层序遍历 · 只保留最后一层',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def deepestLeavesSum(self, root):

        res = 0
        q = [root]
        l = 0
        r = 1
        while l < r:
            res = 0
            for now in q[l : r]:
                res += now.val
                if now.left:
                    q.append(now.left)
                if now.right:
                    q.append(now.right)
            
            l, r = r, len(q)
        
        return res
''',
    call='Solution().deepestLeavesSum(Tr([1,2,3,4,5,None,6,7,None,None,None,None,8]))',
    expect=15,
    views=[
        dict(type='tree', label='二叉树（蓝 = 当前 now）', pointers={'now': 'blue'}, path=False, h=290),
        dict(type='array', var=lambda S: [n.val for n in S['q']], label='q（l..r-1 是当前层）',
             pointers={'l': 'blue'}, window=('l', 'r - 1'), cell=56, h=190),
        dict(type='text', fn=lambda S: f"本层累计 `res = {S.get('res')}`", size=28, h=56),
    ],
    watch=['l', 'r', ('now', lambda S: S['now'].val if S.get('now') else None, 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 保存「当前这一层」的节点值之和',
        'q = [root]': '`q` 当队列用，`q[l:r]` 是当前层；先放入根',
        'l = 0': '`l`、`r` 划出当前层的范围：初始只有根，`l = 0`',
        'r = 1': '`r = 1`：`q[0:1]` 就是第一层',
        'while l < r': lambda S, B, r: (f'当前层 `q[{S.l}:{S.r}]` 非空 → 继续处理' if S.l < S.r else '没有下一层了 → 循环结束，此时 `res` 就是最后一层的和'),
        'res = 0': '==每进入新的一层都把 `res` 清零==：只有最后一层的和会留下来',
        'for now in q': '取出当前层节点 `{now.val}`',
        'res += now.val': '`res = {B.res} + {now.val} = {res}`',
        'if now.left': lambda S, B, r: (f'`{S.now.val}` 有左儿子 `{S.now.left.val}` → 入队，属于下一层' if S.now.left else f'`{S.now.val}` 没有左儿子 → 跳过'),
        'if now.right': lambda S, B, r: (f'`{S.now.val}` 有右儿子 `{S.now.right.val}` → 入队，属于下一层' if S.now.right else f'`{S.now.val}` 没有右儿子 → 跳过'),
        'l, r = r, len(q)': lambda S, B, r: (f'这一层结束，下一层是 `q[{S.l}:{S.r}]`' + ('；为空 → 刚才那层就是最深层' if S.l >= S.r else '；还有下一层，`res` 会被覆盖')),
        'return res': '返回 `res = {ret}`：最后一层（最深的叶子们）的节点值之和',
    },
    cards=dict(
        one_liner='层序遍历，每层重置层和，遍历结束留下的就是最深层之和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给你一棵二叉树的根节点 `root`',
                 '返回==层数最深==的叶子节点的值之和',
                 '示例：最深一层是 `7` 和 `8` → `15`'],
        quote='直接执行一次层序遍历，并使用一个变量记录当前层所有节点之和。在层序遍历结束后，这个变量中记录的自然就是最深那一层叶子节点之和了。',
        quote_src='—— yiduobo 题解',
        idea=['最深一层的节点必然都是叶子，所以「最深叶子之和」就是「最后一层的节点和」',
              '层序遍历，每进入新的一层就把 `res` 清零再累加',
              '遍历结束时 `res` 里就是最后一层的和'],
        result='运行结束，返回 `15`',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`res = 0` 要放在 while 里（每层一次），不能放循环外',
                 '易错：最深层的节点一定是叶子，所以不用单独判断叶子',
                 '原文无题面，题意为：返回最深层叶子节点的值之和（LeetCode 1302）'],
    ),
)
