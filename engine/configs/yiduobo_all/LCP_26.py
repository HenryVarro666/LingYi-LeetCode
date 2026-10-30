TREE_H = 380
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
        if record and S.get('now') is not None and S.get('_inner', {}).get('now') is not None:
            DONE[S['_inner']['now']._uid] = ret
        nodes = _walk(S.get('self.tree'))
        for n in reversed(nodes):
            if n._uid not in DONE and (n.left is None) != (n.right is None):
                c = n.left or n.right
                if c._uid in DONE:
                    DONE[n._uid] = DONE[c._uid]
        for n in nodes:
            n._d = DONE.get(n._uid)
        return fn(S, B, ret) if callable(fn) else fn
    return cap


def _layout(root, box):
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
    pos, rad, order = _layout(root, (box[0], box[1] - TREE_H, box[2], box[1]))
    for n in order:
        d = getattr(n, '_d', None)
        if d is None:
            continue
        X, Y = pos[n._uid]
        s = f'返回 {d}'
        w = cv.tlen(s, 19, bold=True) + 16
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 18), s, 19, T['green'], anchor='mm', bold=True)


def _res(S):
    if 'self.res' in S:
        return S['self.res']
    return getattr(S.get('self'), 'res', '?')


def _v(x):
    return '空' if x is None else str(x.val)


def _cap_both(S, B, r):
    I = S['_inner']
    n = I['now']
    return f'节点 `{n.val}` 左右孩子都在 → 它的度为 3，要看两侧子树的导航装置'


def _cap_state(S, B, r):
    I = S['_inner']
    n, ls, rs = I['now'], I['left_state'], I['right_state']
    if ls == 0 and rs == 0:
        return f'节点 `{n.val}`：左 `{ls}`、右 `{rs}` 都没有装置 → ==必须新装一个==，`res` → {S["self.res"] if "self.res" in S else S["_inner"].get("self.res", "")}'
    if ls == 0 or rs == 0:
        return f'节点 `{n.val}`：左 `{ls}`、右 `{rs}`，有一侧没装置 → 先不装，向上返回 `1` 继续往上找位置'
    return f'节点 `{n.val}`：左 `{ls}`、右 `{rs}`，两侧都有装置 → 不用再装，返回 `2`'


def _cap_dfs_root(S, B, r):
    return '根只有一个孩子：把根当作树的一端，直接对它做 dfs'


CONFIG = dict(
    num='LCP 26', title='导航装置', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='DFS 返回子树内装置数（0 / 1 / 2）',
    tags=['链表树与回溯'],
    code='''
class Solution(object):
    def navigation(self, root):

        self.res = 0

        def dfs(now):
            if not now.left:
                if not now.right:
                    return 0
                else:
                    return dfs(now.right)
            elif not now.right:
                return dfs(now.left)
            else:
                left_state = dfs(now.left)
                right_state = dfs(now.right)
                if left_state == 0:
                    if right_state == 0:
                        self.res += 1
                        return 1
                    else:
                        return 1
                elif right_state == 0:
                    return 1
                else:
                    return 2

        if root.left is None or root.right is None:
            if dfs(root) < 2:
                self.res += 1
        elif dfs(root.left) + dfs(root.right) < 2:
            self.res += 1
        
        return self.res
''',
    call='''s = Solution()
s.tree = Tr([1,2,3,4,5,None,6])
s.navigation(s.tree)''',
    expect=2,
    views=[
        dict(type='tree', label='二叉树（绿标 = 这棵子树已返回的装置数）', pointers={'now': 'blue'}, h=TREE_H,
             color=lambda S, n: 'green' if getattr(n, '_d', None) is not None else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=240, hide=('navigation',)),
    ],
    watch=[('now', lambda S: S['_inner'].get('now') and S['_inner']['now'].val, 'blue'),
           ('left_state', lambda S: S['_inner'].get('left_state')), ('right_state', lambda S: S['_inner'].get('right_state')),
           ('res', _res, 'green')],
    captions={k: track(v, record=(k in (9, 20, 22, 24, 26))) for k, v in {
        4: '`res` 统计需要额外安装的装置个数',
        7: lambda S, B, r: f'节点 `{S["_inner"]["now"].val}` {"没有" if S["_inner"]["now"].left is None else "有"}左孩子' + ('，再看右孩子' if S["_inner"]["now"].left is None else '，不是叶子也不是单链的左端'),
        8: lambda S, B, r: f'节点 `{S["_inner"]["now"].val}` {"没有" if S["_inner"]["now"].right is None else "有"}右孩子：' + ('左右都没有 → 叶子' if S["_inner"]["now"].right is None else '只有右孩子 → 单侧，不分叉'),
        9: '==叶子节点==：本身没有分叉，子树里不需要装置 → 返回 `0`',
        11: '只有右孩子：不分叉，直接把右子树 `dfs(now.right)` 的结果当作自己的结果',
        12: lambda S, B, r: f'节点 `{S["_inner"]["now"].val}` {"没有" if S["_inner"]["now"].right is None else "有"}右孩子' + ('：只有左孩子 → 单侧' if S["_inner"]["now"].right is None else '：左右都有 → 进入度为 3 的分支'),
        13: '只有左孩子：不分叉，直接把左子树 `dfs(now.left)` 的结果当作自己的结果',
        15: '左右都有孩子 → ==度为 3 的节点==。先递归左子树，拿到装置数',
        16: lambda S, B, r: f'左子树返回 `{S["_inner"]["left_state"]}`，再递归右子树',
        17: lambda S, B, r: f'左子树返回 `{S["_inner"]["left_state"]}`：{"没有装置" if S["_inner"]["left_state"] == 0 else "已有装置"}',
        18: '左边没装置，右边呢？两边都没有，当前节点这里就必须装一个',
        19: lambda S, B, r: f'左右两侧都没装置 → ==在此处新装一个==，`res` → {_res(S)}',
        20: '左右都为 `0` 但刚装了一个 → 返回 `1`',
        22: '左边没装置、右边有：先不装，==返回 `1`== 让上层继续找位置',
        23: '左边有装置，右边呢？',
        24: '右边没装置、左边有：同样返回 `1`',
        26: '左右两侧都有装置 → 这棵子树已经安全 → 返回 `2`',
        28: '根没有“上面”可放：要在主函数里单独收尾。根只有一个孩子时，对根做 dfs',
        29: '整棵树里的装置数小于 2 → 再补 1 个',
        30: lambda S, B, r: f'补上 1 个装置：`res` → {_res(S)}',
        31: '根有两个孩子：左、右子树的装置数相加，不足 2 个就再补 1 个',
        32: lambda S, B, r: f'左右子树加起来不足 2 个装置，==补上 1 个==：`res` → {_res(S)}',
        34: lambda S, B, r: f'一共需要 `{_res(S)}` 个导航装置',
    }.items()},
    cards=dict(
        one_liner='只有度为 3 的节点才会让定位出问题，dfs 数装置个数',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['给一棵树（节点即房间），在若干房间放导航装置，使每个房间到装置的距离向量唯一',
                 '求最少需要放几个装置',
                 '示例：`[1,2,null,3,4]` → `2`；本视频 `[1,2,3,4,5,null,6]` → `2`'],
        quote='只有当出现了度为3的节点时，需要额外的导航装置，因为如果导航装置位于该节点的某一相邻节点这一侧时，另外两个相邻节点与导航装置的距离必然相同。',
        quote_src='—— yiduobo 题解原文',
        idea=['dfs 返回值：`0` 子树里没装置，`1` 有一个，`2` 有两个',
              '叶子返回 `0`；单侧孩子原样返回；度为 3 的节点看左右返回值',
              '左右都 `0` → 新装一个并返回 `1`；有一侧 `0` → 返回 `1`；都非 `0` → 返回 `2`'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '作者说明：这种构造没有严格证明，但节点度数的情况有限',
                 '易错点：根节点没有“上面”可放，要在主函数里额外判断，不足 2 个就补 1 个',
                 '一条单链（度 ≤ 2）不需要额外装置，只要在端点放 1 个',
                 '原文为 Python 2 风格，在 Python 3 下无需修改'],
    ),
)
