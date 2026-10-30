import views as V

TREE = [3, 9, 20, None, None, 15, 7]


def tree_view(**spec):
    """迭代写法没有递归路径：画树时只传一个栈帧"""
    def draw(cv, S, B, box, T):
        V.v_tree(cv, spec, {'_S': S, '_B': B, '_frames': [dict(args=[], locals=S)]}, box, 0, {})
    return dict(type='custom', draw=draw, h=spec.get('h', 300))


def _uids(S, a, b):
    q = S.get('q') or []
    return {n._uid for n in q[a:b]}


def _tcolor(S, n):
    if 'l' not in S:
        return None
    l, r = S['l'], S['r']
    if n._uid in _uids(S, l, r):
        return 'cyan'                                   # 当前层
    if n._uid in _uids(S, 0, l):
        return 'green'                                  # 已经统计过的层
    if n._uid in _uids(S, r, len(S['q'])):
        return 'purple'                                 # 下一层（已入队）
    return None


def _qcolor(S, i, v):
    if 'l' not in S:
        return None
    if i < S['l']:
        return 'green'
    if i < S['r']:
        return 'cyan'
    return 'purple'


L_LR = 21                                                # 'l = r' 所在行


def _formula(S):
    if 'tmp' not in S or 'l' not in S:
        return '一层一层地 BFS：`q[l:r]` 是==当前层==，新入队的孩子是下一层'
    l, r = S['l'], S['r']
    if S.get('_line') in (L_LR, L_LR + 1) or l == r:
        return f'切换到下一层：`l ← r`，`r ← newr`（下一层是 `q[{S["r"] if S.get("_line") == L_LR else l}:{S["newr"]}]`）'
    return f'当前层 `q[{l}:{r}]` 共 `{r - l}` 个节点，`tmp = {S["tmp"]}`，平均值 = `{S["tmp"]} / {r - l}`'


def _ifc(side, word):
    def f(S, B, ret):
        nd = B['now']
        ch = getattr(nd, side)
        if ch is not None:
            return f'`{nd.val}` 有{word}孩子 `{ch.val}` → 入队，属于==下一层=='
        return f'`{nd.val}` 没有{word}孩子'
    return f


CONFIG = dict(
    num=637, title='二叉树的层平均值', difficulty='Easy', category='二叉树',
    author='yiduobo', technique='BFS 层序遍历 · 数组 + 左右下标当队列',
    tags=['字节30天', '面试经典150'],
    code='''
class Solution(object):
    def averageOfLevels(self, root):
        res = []
        q = [root]
        l = 0
        r = 1
        while l < r:
            newr = r
            tmp = 0
            for index in range(l, r):
                now = q[index]
                tmp += now.val
                if now.left:
                    q.append(now.left)
                    newr += 1
                if now.right:
                    q.append(now.right)
                    newr += 1

            res.append(tmp * 1.0 / (r - l))
            l = r
            r = newr

        return res
''',
    call=f'Solution().averageOfLevels(Tr({TREE}))',
    expect=[3.0, 14.5, 11.0],
    skip=['newr += 1', 'q.append(now.', 'r = 1', 'l = 0', 'now = q[index]'],
    views=[
        dict(type='text', fn=_formula, h=56),
        tree_view(label='二叉树（青 = 当前层，绿 = 已统计，紫 = 下一层）', h=230, pointers={'now': 'yellow'}, color=_tcolor),
        dict(type='array', var=lambda S: [n.val for n in S['q']] if 'q' in S else None,
             label='q（数组当队列：[l, r) 是当前层，newr 是下一层的结尾）', cell=72, h=220,
             pointers={'l': 'blue', 'r': 'pink', 'newr': 'purple'}, color=_qcolor),
        dict(type='array', var='res', label='res（每层平均值）', cell=80, min_slots=4, h=120),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('newr', 'newr', 'purple'), ('now', 'now'), ('tmp', 'tmp', 'cyan')],
    captions={
        'res = []': '`res` 存每一层的平均值',
        'q = [root]': '用数组 `q` 当队列，`l = 0`、`r = 1`：区间 `[l, r)` 就是==当前这一层==（只有根）',
        'while l < r': lambda S, B, ret: (f'`l = {B.l} < r = {B.r}`：还有一层没统计' if B.l < B.r
                                          else f'`l == r == {B.r}`：下一层是空的 → 遍历结束'),
        'newr = r': lambda S, B, ret: ('`newr` 从 `r` 开始，记录下一层的结尾（孩子入队时 +1）' if S.l == 0
                                       else f'新的一层：`newr = r = {S.r}`'),
        'tmp = 0': lambda S, B, ret: ('`tmp` 累加这一层的节点值' if S.l == 0 else '`tmp` 清零'),
        'for index in range(l, r)': lambda S, B, ret: (f'处理本层节点 `q[{S.index}] = {S.q[S.index].val}`'
                                                       if S.get('index') != B.get('index') or 'index' not in B
                                                       else '本层节点处理完'),
        'tmp += now.val': '`tmp += {now.val}` → {tmp}',
        'if now.left': _ifc('left', '左'),
        'if now.right': _ifc('right', '右'),
        'res.append(tmp * 1.0 / (r - l))': '本层平均值 `{tmp} / {r - l}` = =={res[-1]:g}==（`* 1.0` 保证是浮点除法）',
        'l = r': '`l = r = {l}`：当前层统计完，左端点移到下一层开头',
        'r = newr': lambda S, B, ret: (f'`r = newr = {S.r}`：下一层变成当前层 `q[{S.l}:{S.r}]`' if S.r > S.l
                                       else f'`r = newr = {S.r}`：这一层没有孩子入队，下一层为空'),
        'return res': '返回每层平均值 `{ret}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='BFS 一层一层地遍历：[l, r) 是当前层，统计完求平均',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给一棵非空二叉树，返回==每一层节点的平均值==组成的数组',
                 '示例：`root = [3,9,20,null,null,15,7]` → `[3.0, 14.5, 11.0]`',
                 '第 0 层 `3`；第 1 层 `(9 + 20) / 2 = 14.5`；第 2 层 `(15 + 7) / 2 = 11`'],
        quote='使用bfs执行二叉树的层序遍历，==每计算一层则统计盖（该）层的节点值和==从而计算出平均值。',
        quote_src='—— yiduobo 题解',
        idea=['数组 `q` 当队列，不出队：用下标 `[l, r)` 标出当前层',
              '遍历当前层时，孩子追加到末尾，`newr` 记下一层的结尾',
              '一层结束：平均值 = `tmp / (r - l)`，然后 `l = r`，`r = newr`'],
        result='`[3.0, 14.5, 11.0]` ✓',
        summary=['时间 `O(n)`：每个节点入队、处理各一次；空间 `O(n)`：数组队列保留了所有节点',
                 '关键：先固定本层范围 `[l, r)`，再遍历；孩子只影响 `newr`，不影响本层',
                 '`tmp * 1.0 / (r - l)`：Python 2 里整数相除会取整，乘 `1.0` 变浮点（Python 3 也照样正确）',
                 '原文删去了 TreeNode 定义注释和类型说明文档字符串，代码未改'],
    ),
)
