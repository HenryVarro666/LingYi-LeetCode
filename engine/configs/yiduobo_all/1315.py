DONE = {}


def _walk(root):
    out, st, seen = [], [root], set()
    while st:
        n = st.pop()
        if n is None or n._uid in seen:
            continue
        seen.add(n._uid)
        out.append(n)
        st += [n.left, n.right]
    return out


def track(fn, add=None):
    def cap(S, B, ret):
        if add:
            c = getattr(S.now, add)
            if c is not None:
                DONE[c._uid] = True
        for n in _walk(S.get('self.tree')):
            n._g = DONE.get(n._uid)
        return fn(S, B, ret) if callable(fn) else fn
    return cap


def _txt(S):
    I = S.get('_inner', {})
    now = I.get('now')
    if now is None:
        return '`flag`：当前节点的父亲值是不是偶数；`flag` 为真，孩子就是「祖父为偶数」的节点'
    return f'节点 `{now.val}`，`flag = {I.get("flag")}`（它的父亲' + ('是偶数 → 孩子要加' if I.get('flag') else '不是偶数/没有父亲 → 孩子不加') + '）'


def _call(side):
    def f(S, B, r):
        return (f'进入{"左" if side == "left" else "右"}孩子 `{S.now.val}`：传下来的 `flag = {S.flag}`，即它的父亲是'
                + ('==偶数==，所以它的孩子会被加' if S.flag else '奇数，它的孩子不加'))
    return f


CONFIG = dict(
    num=1315, title='祖父节点值为偶数的节点和', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='DFS · 传递父亲奇偶性',
    tags=['灵神核心路线', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def sumEvenGrandparent(self, root):

        return self.dfs(root, False)

    def dfs(self, now, flag):
        res = 0
        if now.left:
            if flag:
                res += now.left.val
            res += self.dfs(now.left, now.val % 2 == 0)
        
        if now.right:
            if flag:
                res += now.right.val
            res += self.dfs(now.right, now.val % 2 == 0)
        
        return res
''',
    call='''s = Solution()
s.tree = Tr([6,7,8,2,7,1,3,9])
s.sumEvenGrandparent(s.tree)''',
    expect=13,
    skip=['res = 0'],
    max_steps=110,
    views=[
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='tree', label='二叉树（绿 = 已加入答案的孙子，蓝 = now）', pointers={'now': 'blue'}, h=330,
             color=lambda S, n: 'green' if getattr(n, '_g', None) else None),
        dict(type='calls', h=230),
    ],
    watch=[('now', lambda S: S['_inner']['now'].val if S['_inner'].get('now') is not None else None, 'blue'),
           ('flag', lambda S: S['_inner'].get('flag'), 'orange'), ('res', lambda S: S['_inner'].get('res'), 'green')],
    captions={
        'return self.dfs(root, False)': '从根出发：根没有父亲，`flag = False`',
        'if now.left': lambda S, B, r: (f'`{S.now.val}` 有左孩子 `{S.now.left.val}`' if S.now.left else f'`{S.now.val}` 没有左孩子'),
        'if now.right': lambda S, B, r: (f'`{S.now.val}` 有右孩子 `{S.now.right.val}`' if S.now.right else f'`{S.now.val}` 没有右孩子'),
        'if flag': lambda S, B, r: ('`flag` 为真：`{}` 的父亲是偶数 → 孩子的祖父是偶数，要加'.format(S.now.val) if S.flag else '`flag` 为假：父亲不是偶数 → 孩子不加'),
        'res += now.left.val': track(lambda S, B, r: f'孩子 `{S.now.left.val}` 的祖父是偶数 → 加进答案：`res = {S.res}`', add='left'),
        'res += now.right.val': track(lambda S, B, r: f'孩子 `{S.now.right.val}` 的祖父是偶数 → 加进答案：`res = {S.res}`', add='right'),
        'res += self.dfs(now.left': track(_call('left')),
        'res += self.dfs(now.right': track(_call('right')),
        'return res': track(lambda S, B, r: f'`{S.now.val}` 这棵子树里「祖父为偶数」的节点和 = `{S.res}`，返回给上一层'),
        'return self.dfs': '从根开始的 DFS 全部结束',
    },
    cards=dict(
        one_liner='DFS 往下传「我的值是不是偶数」，孩子的孩子才会被加',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['二叉树里，把所有==祖父节点值为偶数==的节点值加起来',
                 '祖父 = 父亲的父亲；没有祖父就不算',
                 '本视频：`root = [6,7,8,2,7,1,3,9]`'],
        quote='对于当前节点，根据其父亲节点的奇偶性，来决定是否将当前节点左右孩子值加入到答案中。……每一轮的参数为当前节点now以及now的父亲的奇偶性flag。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dfs(now, flag)`：`flag` 表示 `now` 的父亲是不是偶数',
              '`flag` 为真时，`now` 的孩子的祖父就是偶数 → 孩子值直接加进 `res`',
              '递归时把 `now.val % 2 == 0` 当作孩子的 `flag` 传下去'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '不是给「当前节点」判断，而是==站在爷爷的孙辈前一层==：用 `flag` 决定加不加孩子',
                 '孩子的值在进入递归之前就加了，所以递归的返回值只统计更深层的',
                 '根的 `flag = False`；根的孩子没有祖父，不会被加',
                 '原文已是 Python 3 可运行写法，未改动'],
    ),
)
