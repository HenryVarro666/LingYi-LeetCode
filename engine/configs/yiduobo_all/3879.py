def _vv(S):
    return sorted(S['_inner'].get('vis', []))


def _info(S):
    i = S['_inner']
    if 'dis' not in i:
        return '第一遍 BFS 记录每个节点的父亲 `fa`，之后==枚举起点==做 DFS'
    return f"当前起点 `start = {S['start'].val}`，路径节点值集合 `vis = {_vv(S)}`，路径和 `dis = {i['dis']}`，全局最大 `res = {i.get('best')}`"


BEST = [None]


def _cmp(S, B, r):
    d, b = S['_inner']['dis'], B['_inner'].get('best')
    if b is None or b < d:
        return f'路径和 `dis = {d}` 比当前最大 `res = {b}` 更大 → 要更新答案'
    return f'路径和 `dis = {d}` 不超过当前最大 `res = {b}` → 不更新'


def _wrap(fn):
    def cap(S, B, r):
        if S['_line'] == LINE_NONE:
            BEST[0] = None
        B['_inner']['best'] = BEST[0]
        if S['_line'] == LINE_SET and 'dis' in S['_inner']:
            BEST[0] = S['_inner']['dis']
        S['_inner']['best'] = BEST[0]
        if callable(fn):
            return fn(S, B, r)
        from make import render_caption
        return render_caption(fn, S, B, r)
    return cap


def _nv(x):
    return '空' if x is None else str(x.val)


def _step(kind):
    def f(S, B, ret):
        n = B.now
        if kind == 'fa':
            c = B.fa[n]
        else:
            c = getattr(n, kind)
        if c is None:
            return f'`{n.val}` 没有{ {"fa": "父亲", "left": "左孩子", "right": "右孩子"}[kind] } → 这个方向不能走'
        if c.val in B.vis:
            return f'`{c.val}` 已在路径里（`vis = {sorted(B.vis)}`）→ ==值重复，不能走=='
        return f'`{c.val}` 的值不在 `vis` 里 → 可以走过去：路径和 `{B.dis} + {c.val} = {B.dis + c.val}`'
    return f


CONFIG = dict(
    num=3879, title='二叉树中的最大不同路径和', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='记父亲 + 枚举起点 DFS 回溯',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def maxSum(self, root):
        
        fa = {}
        fa[root] = None
        q = [root]
        head, tail = 0, 1
        while head < tail:
            now = q[head]
            head += 1
            if now.left:
                fa[now.left] = now
                q.append(now.left)
                tail += 1
            if now.right:
                fa[now.right] = now
                q.append(now.right)
                tail += 1
        
        global res
        res = None

        def dfs(now, vis, dis):
            global res
            if res is None or res < dis:
                res = dis
            if fa[now] is not None and fa[now].val not in vis:
                vis.add(fa[now].val)
                dfs(fa[now], vis, dis + fa[now].val)
                vis.remove(fa[now].val)
            
            if now.left and now.left.val not in vis:
                vis.add(now.left.val)
                dfs(now.left, vis, dis + now.left.val)
                vis.remove(now.left.val)
            
            if now.right and now.right.val not in vis:
                vis.add(now.right.val)
                dfs(now.right, vis, dis + now.right.val)
                vis.remove(now.right.val)

        for start in fa:
            vis = set()
            vis.add(start.val)
            dfs(start, vis, start.val)
        
        return res
''',
    call='Solution().maxSum(Tr([3,1,3,None,2]))',
    expect=6,
    views=[
        dict(type='tree', label='二叉树（蓝 = now，黄圈 = 递归路径）', pointers={'now': 'blue'}, h=250),
        dict(type='text', fn=_info, size=22, h=64),
        dict(type='calls', h=220, hide=('fa',)),
    ],
    watch=[('now', lambda S: S['_inner']['now'].val if 'now' in S['_inner'] and S['_inner']['now'] is not None else None, 'blue'),
           ('dis', lambda S: S['_inner'].get('dis'), 'yellow'), ('res', lambda S: S['_inner'].get('best'), 'green')],
    captions={
        'fa = {}': '题目只给了孩子指针，先用 BFS 建 ==父亲表 `fa`==，这样路径才能往上走',
        'fa[root] = None': '根没有父亲：`fa[root] = None`',
        'q = [root]': '队列 `q` 做 BFS，`head`/`tail` 当队头队尾',
        'while head < tail': '`head < tail`：队里还有节点没处理',
        'now = q[head]': '取出队头 `{now.val}`',
        'fa[now.left] = now': '记下：`{now.left.val}` 的父亲是 `{now.val}`',
        'fa[now.right] = now': '记下：`{now.right.val}` 的父亲是 `{now.val}`',
        'global res': '`res` 是全局答案，==所有起点共用==',
        'res = None': '`res` 先设为 `None`：路径和可能很小，不用 0 当下限',
        'def dfs': 'DFS 三个参数：当前节点 `now`、路径上的节点值集合 `vis`、路径和 `dis`',
        'for start in fa': '==枚举起点 `start`==：路径可以从任意节点出发（`fa` 的键正好是全部节点）',
        'vis = set()': '每个起点用新的空集合',
        'vis.add(start.val)': '起点自己的值 `{start.val}` 先放进集合',
        'dfs(start, vis': lambda S, B, r: f'从 `start = {S.start.val}` 出发 DFS：能往父亲、左孩子、右孩子走',
        'if res is None or res < dis': _cmp,
        'res = dis': lambda S, B, r: f'==每走到一个节点就更新答案==：`res` → `{S["_inner"]["dis"]}`',
        'if fa[now] is not None': _step('fa'),
        'if now.left and': _step('left'),
        'if now.right and': _step('right'),
        'vis.add(fa[now].val)': lambda S, B, r: f'把父亲的值 `{B.fa[B.now].val}` 加入 `vis` → `{sorted(S.vis)}`',
        'vis.add(now.left.val)': '把左孩子的值 `{now.left.val}` 加入 `vis` → `{sorted(vis)}`',
        'vis.add(now.right.val)': '把右孩子的值 `{now.right.val}` 加入 `vis` → `{sorted(vis)}`',
        'dfs(fa[now], vis': '往上走到父亲 `{B.fa[B.now].val}`，路径和 `{B.dis} + {B.fa[B.now].val}`',
        'dfs(now.left, vis': '往下走到左孩子 `{B.now.left.val}`，路径和 `{B.dis} + {B.now.left.val}`',
        'dfs(now.right, vis': '往下走到右孩子 `{B.now.right.val}`，路径和 `{B.dis} + {B.now.right.val}`',
        'vis.remove(fa[now].val)': lambda S, B, r: f'==回溯==：把父亲的值 `{B.fa[B.now].val}` 从 `vis` 删掉 → `{sorted(S.vis)}`',
        'vis.remove(now.left.val)': '==回溯==：把左孩子的值 `{now.left.val}` 从 `vis` 删掉 → `{sorted(vis)}`',
        'vis.remove(now.right.val)': '==回溯==：把右孩子的值 `{now.right.val}` 从 `vis` 删掉 → `{sorted(vis)}`',
        'return res': '所有起点都试过，最大不同路径和 `{res}`',
    },
    skip=['head += 1', 'tail += 1', 'q.append', 'global res', 'fa[root] = None', 'fa = {}', 'q = [root]', 'if now.left:', 'if now.right:'],
    max_steps=72,
    cards=dict(
        one_liner='枚举起点 + DFS 回溯：用集合保证路径上节点值互不相同',
        complexity='时间 `O(n^2)`（n 个起点，每次 DFS `O(n)`），空间 `O(n)`',
        problem=['给一棵二叉树，节点带整数值 `val`',
                 '路径是相连节点的序列，起点终点任意、不必过根，==路径上节点值互不相同==',
                 '求所有有效路径中节点值之和的最大值',
                 '本视频：`[3,1,3,null,2]` → `6`（`2 → 1 → 3`，右边那个 3 与根重复不能接）'],
        quote='可以考虑O(n^2)的算法。……完全可以枚举路径的起点start，然后从start开始做dfs，找出所有以start为起点的合法路径，并使用这个路径值更新答案。',
        quote_src='—— yiduobo 题解',
        idea=['树上路径能往上走，所以先 BFS 建 ==父亲表 `fa`==',
              '枚举每个起点，DFS 往父亲、左、右三个方向扩展',
              '不能走重复值：用 `vis` 记录路径上的值，==递归前加入、返回后删除==（回溯）',
              '每到一个节点就用路径和更新全局 `res`'],
        summary=['时间 `O(n^2)`，空间 `O(n)`：题目规模小，暴力枚举可行',
                 '用 DFS 而不是 BFS：`vis` 要随递归/回溯增删',
                 '易错：判重比较的是==节点值==不是节点；路径上的 `vis.remove` 必须配对',
                 '`fa` 的键遍历正好是全部节点，作为起点集合',
                 '原文用 `global res` 保存答案（Python 3 同样可用），代码未改动；题面由原文整理'],
    ),
)

_L = CONFIG['code'].strip('\n').split('\n')
LINE_NONE = next(i + 1 for i, t in enumerate(_L) if t.strip() == 'res = None')
LINE_SET = next(i + 1 for i, t in enumerate(_L) if t.strip() == 'res = dis')
CONFIG['captions'] = {k: _wrap(v) for k, v in CONFIG['captions'].items()}
CONFIG['captions'][''] = _wrap(lambda S, B, r: 1 / 0)  # 兜底：只更新 best，随后退回默认字幕
