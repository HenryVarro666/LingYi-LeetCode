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


def track(fn, record=False):
    def cap(S, B, ret):
        if record and S.now is not None:
            DONE[S.now._uid] = S.now_sum
        for n in _walk(S.get('self.tree')):
            n._d = DONE.get(n._uid)
        return fn(S, B, ret) if callable(fn) else fn
    return cap


def _layout(root, box):  # 与 views.v_tree 相同的布局
    x0, y0, x1, y1 = box
    order, depth = [], {}

    def ino(n, d):
        if n is None or n._uid in depth:
            return
        depth[n._uid] = d
        ino(n.left, d + 1)
        order.append(n)
        ino(n.right, d + 1)
    ino(root, 0)
    maxd = max(depth.values()) + 1
    sp = min(78, (x1 - x0 - 60) / max(1, len(order)))
    dy = min(95, (y1 - y0 - 80) / max(1, maxd))
    rad = max(14, min(26, sp * 0.4, dy * 0.32))
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * len(order)) / 2 + sp / 2
    pos = {n._uid: (sx + i * sp, y0 + 60 + depth[n._uid] * dy + rad) for i, n in enumerate(order)}
    return pos, rad, order


def badges(cv, S, B, box, T):
    root = S.get('self.tree')
    if root is None:
        return
    pos, rad, order = _layout(root, (box[0], box[1] - 300, box[2], box[1]))
    for n in order:
        d = getattr(n, '_d', None)
        if d is None:
            continue
        X, Y = pos[n._uid]
        s = f'和 {d}'
        w = cv.tlen(s, 19, bold=True) + 16
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 18), s, 19, T['green'], anchor='mm', bold=True)


CONFIG = dict(
    num=508, title='出现次数最多的子树元素和', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='后序求子树和 · dict 计数',
    tags=['二叉树', '自底向上 DFS'],
    code='''
class Solution(object):
    def findFrequentTreeSum(self, root):

        if not root:
            return []

        sum_dict = {}
        self.dfs(root, sum_dict)

        res = []
        max_freq = 0
        for s, cnt in sum_dict.items():
            if cnt > max_freq:
                max_freq = cnt
                res = [s]
            elif cnt == max_freq:
                res.append(s)
        return res

    def dfs(self, now, sum_dict):
        left_sum = right_sum = 0
        if now.left:
            left_sum = self.dfs(now.left, sum_dict)
        if now.right:
            right_sum = self.dfs(now.right, sum_dict)
        now_sum = left_sum + right_sum + now.val
        sum_dict[now_sum] = sum_dict.get(now_sum, 0) + 1
        return now_sum
''',
    call='''s = Solution()
s.tree = Tr([5,2,-5])
s.findFrequentTreeSum(s.tree)''',
    expect=[2],
    views=[
        dict(type='tree', var='self.tree', label='二叉树（蓝 = now，绿标签 = 已算出的子树和）', pointers={'now': 'blue'}, h=300),
        dict(type='custom', draw=badges, h=0),
        dict(type='map', var='sum_dict', label='sum_dict（子树和 → 出现次数）', h=130),
        dict(type='calls', h=200, hide=('sum_dict', 'self')),
    ],
    watch=[('now', lambda S: S['_inner']['now'].val if S['_inner'].get('now') is not None else None, 'blue'),
           ('left_sum', lambda S: S['_inner'].get('left_sum'), 'cyan'), ('right_sum', lambda S: S['_inner'].get('right_sum'), 'pink'),
           ('max_freq', 'max_freq', 'yellow')],
    captions={
        'if not root': '空树直接返回 `[]`；本题树非空',
        'sum_dict = {}': '`sum_dict`：记录每个「子树元素和」出现了几次',
        'self.dfs(root, sum_dict)': track('从根出发后序遍历：先算左右子树的和，再算当前子树的和，每算出一个就计数'),
        'left_sum = right_sum = 0': track('没有孩子时左右和都是 `0`'),
        'if now.left': track(lambda S, B, r: (f'`{S.now.val}` 有左孩子 `{S.now.left.val}` → 先递归求左子树的和' if S.now.left
                                              else f'`{S.now.val}` 没有左孩子，`left_sum` 保持 `0`')),
        'if now.right': track(lambda S, B, r: (f'`{S.now.val}` 有右孩子 `{S.now.right.val}` → 再递归求右子树的和' if S.now.right
                                               else f'`{S.now.val}` 没有右孩子，`right_sum` 保持 `0`')),
        'now_sum = left_sum': track(lambda S, B, r: f'子树和 = 左 `{S.left_sum}` + 右 `{S.right_sum}` + 自己 `{S.now.val}` = ==`{S.now_sum}`==', record=True),
        'sum_dict[now_sum]': track(lambda S, B, r: f'子树和 `{S.now_sum}` 的出现次数 +1 → `{S.sum_dict[S.now_sum]}`'),
        'return now_sum': track(lambda S, B, r: f'把 `{S.now_sum}` 返回给父节点，作为它的 `left_sum` 或 `right_sum`'),
        'res = []': '`res` 存答案，`max_freq` 记最高次数',
        'max_freq = 0': '最高次数从 `0` 开始',
        'for s, cnt': '一趟扫描 `sum_dict`：逐个看「和 `s` 出现了 `cnt` 次」',
        'if cnt > max_freq': lambda S, B, r: (f'和 `{S.s}` 出现 `{S.cnt}` 次 > 目前最高 `{S.max_freq}` → 重新开始记录' if S.cnt > S.max_freq else f'和 `{S.s}` 出现 `{S.cnt}` 次，不超过最高 `{S.max_freq}`'),
        'max_freq = cnt': '新的最高次数 `{max_freq}`',
        'res = [s]': '`res` 重置为只含 `{s}`',
        'elif cnt == max_freq': lambda S, B, r: (f'`{S.cnt} == max_freq({S.max_freq})` → 并列，也要收进答案' if S.cnt == S.max_freq else f'`{S.cnt} < max_freq({S.max_freq})` → 出现次数更少，不要'),
        'res.append': '并列：`res` 追加 `{s}` → `{res}`',
        'return res': '出现次数最多的子树和：`{res}`',
    },
    cards=dict(
        one_liner='后序算出每棵子树的和，dict 计数，最后找出现最多的',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['子树元素和 = 以某节点为根的整棵子树所有节点值之和',
                 '返回==出现次数最多==的子树元素和；并列时全部返回，顺序不限',
                 '本视频：`[5,2,-5]`：子树和分别是 `2`、`-5`、`2` → 返回 `[2]`'],
        quote='对于某棵子树，其树中元素之和应该等于这棵树根节点的val加上其左子树元素之和以及右子树元素之和，于是可以优先递归求解其左右子树的元素和，然后再求当前子树的元素和。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dfs(now)` 返回以 `now` 为根的子树和：左和 + 右和 + 自己',
              '每算出一个子树和，就在 `sum_dict` 里计数 +1',
              '最后扫描字典：次数更高就重置 `res`，次数相同就追加'],
        summary=['时间 `O(n)`，空间 `O(n)`（字典 + 递归栈）',
                 '子树和可以为负或为 0，用 dict 计数不受影响',
                 '易错：`res` 要处理并列；遇到更大的 `cnt` 才重置为 `[s]`',
                 '原文为 Python 2 风格（`class Solution(object)`），`items()` 本就兼容，代码没有改动'],
    ),
)
