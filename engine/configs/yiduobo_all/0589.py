SETUP = '''
class Node(object):
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []
    def __repr__(self):
        return f'Node({self.val})'

root = Node(1, [Node(3, [Node(5), Node(6)]), Node(2), Node(4)])
'''

# 示例 1：root = [1,null,3,2,4,null,5,6] 的固定布局（值互不相同，按值定位）
POS = {1: (0.5, 0), 3: (0.22, 1), 2: (0.5, 1), 4: (0.78, 1), 5: (0.1, 2), 6: (0.34, 2)}
EDGES = [(1, 3), (1, 2), (1, 4), (3, 5), (3, 6)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'N 叉树（绿 = 已出栈访问，数字 = 访问顺序；青 = 在栈里；黄圈 = now）', 22, T['muted'], bold=True)
    W_, top, gap = x1 - x0 - 80, y0 + 92, (y1 - y0 - 140) / 2
    P = {v: (x0 + 40 + fx * W_, top + lv * gap) for v, (fx, lv) in POS.items()}
    order = list(S.get('res') or [])
    instack = {getattr(x, 'val', None) for x in (S.get('stack') or [])}
    cur = getattr(S.get('now'), 'val', None)
    for a, b in EDGES:
        cv.line([P[a], P[b]], T['border'], 3)
    R = 34
    for v, (X, Y) in P.items():
        seen = v in order
        fill = T['green'] if seen else (T['cyan'] if v in instack else T['panel2'])
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=fill, outline=T['border'], width=2)
        cv.text((X, Y), v, 30, T['bg'] if (seen or v in instack) else T['text'], anchor='mm', bold=True)
        if v == cur:
            cv.d.ellipse((X - R - 8, Y - R - 8, X + R + 8, Y + R + 8), outline=T['yellow'], width=5)
        if seen:
            k = order.index(v) + 1
            cv.d.ellipse((X + R - 14, Y - R - 10, X + R + 14, Y - R + 18), fill=T['orange'])
            cv.text((X + R, Y - R + 4), k, 18, T['bg'], anchor='mm', bold=True)


def _cap_ext(S, B, ret):
    kids = [c.val for c in S.now.children]
    if not kids:
        return f'`{S.now.val}` 没有孩子，栈不变'
    return (f'孩子 `{kids}` ==反序==压栈 `{kids[::-1]}`：栈顶是 `{kids[0]}`，'
            f'下一个就先处理它')


CONFIG = dict(
    num=589, title='N 叉树的前序遍历', difficulty='Easy', category='链表、二叉树与回溯',
    author='yiduobo', technique='迭代 · 栈 + 孩子反序入栈',
    tags=['labuladong', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def preorder(self, root):

        if not root:
            return []

        res = []
        stack = [root]
        while stack:
            now = stack.pop()
            res.append(now.val)
            stack.extend(now.children[::-1])

        return res
''',
    setup=SETUP,
    call='Solution().preorder(root)',
    expect=[1, 3, 5, 6, 2, 4],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='stack', var='stack', fmt=lambda x: str(x.val), h=150, label='stack'),
        dict(type='array', var='res', cell=80, h=150, label='res（前序遍历结果）', min_slots=6),
    ],
    watch=[('now', lambda S: getattr(S.get('now'), 'val', None), 'yellow'), ('res', 'res', 'green')],
    captions={
        'if not root': '空树直接返回 `[]`；这里根非空',
        'res = []': '`res` 收集遍历结果',
        'stack = [root]': '用栈模拟递归：先放入根节点 `1`',
        'while stack': lambda S, B, r: (f'栈非空，还有 {len(S.stack)} 个节点待处理' if S.stack else '栈空了 → 所有节点都已访问'),
        'now = stack.pop()': '弹出栈顶 `now = {now.val}`',
        'res.append(now.val)': '前序：==弹出就访问==，`res` → `{res}`',
        'stack.extend(now.children[::-1])': _cap_ext,
        'return res': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='用栈代替递归：弹出即访问，孩子反序压栈，保证最左的孩子先出来',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给 N 叉树的根节点 `root`，返回节点值的==前序遍历==（进阶：用迭代）',
                 '输入按层序序列化，每组子节点用 `null` 分隔',
                 '示例：`root = [1,null,3,2,4,null,5,6]` → `[1,3,5,6,2,4]`'],
        quote='与二叉树的前序遍历类似，迭代的做法也是用到栈。考虑到栈后进先出的特点，因此在处理到某个节点时，我们应该==将当前节点的孩子反序压入栈中==。',
        quote_src='—— yiduobo 题解原文',
        idea=['栈里放「还没访问的子树根」；每次弹出栈顶并访问它',
              '前序要求孩子从左到右处理 → 栈后进先出，所以==反序==压栈',
              '这样第一个孩子在栈顶，它的整棵子树会先于兄弟们处理完'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：孩子要 `[::-1]` 反序入栈，否则得到的是「根 → 右 → 左」的顺序',
                 '对比灵神：递归 `dfs`，先 `append` 再依次递归儿子，思路相同、写法更直接',
                 '原文为 Python 2 风格：只删去了 LeetCode 给的 `Node` 定义注释（演示在 setup 中定义了 `Node`）'],
    ),
)
