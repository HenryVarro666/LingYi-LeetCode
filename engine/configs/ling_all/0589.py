SETUP = '''
class Node:
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
    cv.text((x0 + 18, y0 + 4), 'N 叉树（绿 = 已访问，数字 = 访问顺序；黄圈 = 当前 node）', 22, T['muted'], bold=True)
    W_, top, gap = x1 - x0 - 80, y0 + 92, (y1 - y0 - 140) / 2
    P = {v: (x0 + 40 + fx * W_, top + lv * gap) for v, (fx, lv) in POS.items()}
    order = list(S.get('ans') or [])
    node = S.get('node')
    cur = getattr(node, 'val', None)
    for a, b in EDGES:
        cv.line([P[a], P[b]], T['border'], 3)
    R = 34
    for v, (X, Y) in P.items():
        seen = v in order
        fill = T['green'] if seen else T['panel2']
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=fill, outline=T['border'], width=2)
        cv.text((X, Y), v, 30, T['bg'] if seen else T['text'], anchor='mm', bold=True)
        if v == cur:
            cv.d.ellipse((X - R - 8, Y - R - 8, X + R + 8, Y + R + 8), outline=T['yellow'], width=5)
        if seen:
            k = order.index(v) + 1
            cv.d.ellipse((X + R - 14, Y - R - 10, X + R + 14, Y - R + 18), fill=T['orange'])
            cv.text((X + R, Y - R + 4), k, 18, T['bg'], anchor='mm', bold=True)


def _cap_for(S, B, ret):
    c = S['_inner'].get('c')
    nd = S['_inner'].get('node')
    if c is None:
        return f'`{nd.val}` ==没有儿子==（children 为空），循环直接结束'
    if c.val in S['ans']:
        return f'`{nd.val}` 的儿子都递归完了，这一层结束'
    kids = [ch.val for ch in nd.children]
    return f'按顺序递归 `{nd.val}` 的儿子 `{kids}`：下一个是 `{c.val}`'


CONFIG = dict(
    num=589, title='N 叉树的前序遍历', difficulty='Easy', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='递归 · 根 → 依次递归每个儿子',
    tags=['labuladong', '灵神题单·链表树与回溯'],
    code='''
class Solution:
    def preorder(self, root: 'Node') -> List[int]:
        ans = []
        def dfs(node: 'Node') -> None:
            if node is None:
                return
            ans.append(node.val)
            for c in node.children:
                dfs(c)
        dfs(root)
        return ans
''',
    setup=SETUP,
    call='Solution().preorder(root)',
    expect=[1, 3, 5, 6, 2, 4],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='array', var='ans', cell=80, h=150, label='ans（前序遍历结果）', min_slots=6),
        dict(type='calls', h=180, hide=('self',)),
    ],
    watch=[('node', lambda S: getattr(S.get('node'), 'val', None), 'yellow'), ('ans', 'ans', 'green')],
    skip=['def dfs'],
    captions={
        'ans = []': '`ans` 收集前序遍历的结果',
        'dfs(root)': '从根节点开始递归',
        'if node is None': lambda S, B, r: ('空节点' if S.node is None else f'进入节点 `{S.node.val}`，不是空节点'),
        'ans.append(node.val)': '前序：==先访问根==，`ans` 加入 `{node.val}` → `{ans}`',
        'for c in node.children': _cap_for,
        'dfs(c)': '递归儿子 `{c.val}`：进入新的一层',
        'return ans': '所有节点访问完毕：=={ret}==',
    },
    cards=dict(
        one_liner='二叉树前序遍历的推广：先访问根，再依次递归 children 里的每棵子树',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给 N 叉树的根节点 `root`，返回节点值的==前序遍历==',
                 '输入按层序序列化，每组子节点用 `null` 分隔',
                 '示例：`root = [1,null,3,2,4,null,5,6]` → `[1,3,5,6,2,4]`'],
        quote='对于二叉树来说，前序遍历的顺序为：根节点 - 递归左儿子 - 递归右儿子。推广到 N 叉树，顺序是==先访问根节点，再依次递归其 children 数组中的节点==（子树）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(node)`：空节点直接返回',
              '否则先把 `node.val` 加入答案，再按顺序对每个儿子调用 `dfs`',
              '`ans` 定义在外层，所有递归共用一个列表'],
        summary=['时间 `O(n)`；空间 `O(n)`（递归栈最坏是一条链）',
                 '易错：先 `append` 再递归儿子；顺序反过来就成了后序遍历',
                 '叶子的 `children` 是空列表，`for` 循环直接结束',
                 '进阶的迭代写法：用栈，儿子==倒序==入栈（见 yiduobo 的写法）'],
    ),
)
