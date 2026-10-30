def _rng(S):
    q = S.get('q')
    if q is None or 'end' not in S or q not in S['end'] or '_inner' not in S or 'prefix_max' not in S:
        return None
    return S['start'][q], S['end'][q]


def _order(S):
    o = S.get('dfs_order')
    return list(o) if o is not None else None


def _depths(S):
    o, d = S.get('dfs_order'), S.get('depth')
    if o is None or d is None:
        return None
    return [d.get(v) for v in o]


def _info(S):
    r = _rng(S)
    if r is None:
        return ''
    q = S['q']
    return f'删掉 `{q}`：它在 dfs 序里占区间 `[{r[0]}, {r[1]}]`，剩下的是前缀 `[0, {r[0] - 1}]` 和后缀 `[{r[1] + 1}, {len(S["dfs_order"]) - 1}]`'


def _cap_in(S, B, ret):
    return f'进入节点 `{S.now.val}`：深度 `{S.level}`，在 dfs 序里的位置是 `{S.start[S.now.val]}`'


def _cap_end(S, B, ret):
    return f'节点 `{S.now.val}` 的整棵子树已走完：它占的区间是 `[{S.start[S.now.val]}, {S.end[S.now.val]}]`'


def _cap_pre(S, B, ret):
    return f'`prefix_max = {S.prefix_max}`：前缀里的最大深度'


def _cap_pre_in(S, B, ret):
    return f'`prefix_max[{len(S.prefix_max) - 1}] = max(前一项, 深度) = {S.prefix_max[-1]}`'


def _cap_suf_in(S, B, ret):
    return f'从后往前扫：`suffix_max` 末尾加入 `{S.suffix_max[-1]}`（记录的是从当前位置到末尾的最大深度）'


def _cap_pr(S, B, ret):
    return f'`{S.q}` 的区间 `[{S.start[S.q]}, {S.end[S.q]}]` 被删掉；先给这次的答案放一个 `0`'


def _cap_lo(S, B, ret):
    s = S.start[S.q]
    if s > 0:
        return f'左边有前缀 `[0, {s - 1}]` → 候选 `prefix_max[{s - 1}] = {S.prefix_max[s - 1]}`，答案 → =={S.res[-1]}=='
    return f'`start = 0`：左边没有前缀，不用考虑'


def _cap_hi(S, B, ret):
    e = S.end[S.q]
    if e < len(S.dfs_order) - 1:
        return f'右边有后缀 `[{e + 1}, {len(S.dfs_order) - 1}]` → 候选 `suffix_max[{e + 1}] = {S.suffix_max[e + 1]}`，答案 → =={S.res[-1]}=='
    return f'`end` 已是最后一位：右边没有后缀，不用考虑'


CONFIG = dict(
    num=2458, title='移除子树后的二叉树高度', difficulty='Hard', category='二叉树与回溯',
    author='yiduobo', technique='dfs 序 + 前后缀最大值',
    tags=['灵神题单', '链表树与回溯', '难度分 2299'],
    code='''
class Solution(object):
    def treeQueries(self, root, queries):

        depth = {}
        dfs_order = []
        start = {}
        end = {}

        def dfs(now, level):
            depth[now.val] = level
            dfs_order.append(now.val)
            start[now.val] = len(dfs_order) - 1

            if now.left:
                dfs(now.left, level + 1)
            if now.right:
                dfs(now.right, level + 1)
            end[now.val] = len(dfs_order) - 1

        dfs(root, 0)
        
        prefix_max = [depth[dfs_order[0]]]
        for index in range(1, len(dfs_order)):
            prefix_max.append(max(prefix_max[-1], depth[dfs_order[index]]))
        
        suffix_max = [depth[dfs_order[-1]]]
        for index in range(len(dfs_order) - 2, -1, -1):
            suffix_max.append(max(suffix_max[-1], depth[dfs_order[index]]))
        suffix_max.reverse()

        res = []
        for q in queries:
            res.append(0)
            print(start[q], end[q])
            if start[q] > 0:
                res[-1] = max(res[-1], prefix_max[start[q] - 1])
            if end[q] < len(dfs_order) - 1:
                res[-1] = max(res[-1], suffix_max[end[q] + 1])
        
        return res
''',
    call='''s = Solution()
s.tree = Tr([1,2,3,4,5,None,None,6])
s.treeQueries(s.tree, [3,4,2])''',
    expect=[3, 2, 1],
    views=[
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=250),
        dict(type='text', fn=_info, size=22, h=60),
        dict(type='array', var=_order, label='dfs_order：节点值（按访问顺序）', cell=64, h=120,
             window=(lambda S: (_rng(S) or (None, None))[0], lambda S: (_rng(S) or (None, None))[1])),
        dict(type='array', var=_depths, label='对应的深度', cell=64, h=110),
        dict(type='array', var=lambda S: S.get('prefix_max'), label='prefix_max（前缀最大深度）', cell=64, h=110, min_slots=6),
        dict(type='array', var=lambda S: S.get('suffix_max'), label='suffix_max（后缀最大深度）', cell=64, h=110, min_slots=6),
        dict(type='text', fn=lambda S: f"`res = {S['res']}`" if S.get('res') is not None else '', size=26, h=50),
    ],
    watch=[('now', lambda S: S['_inner'].get('now') and S['_inner']['now'].val, 'blue'),
           ('q', lambda S: S.get('q') if 'res' in S else None, 'yellow')],
    captions={
        'depth = {}': '`depth`：节点 → 深度；`dfs_order`：dfs 访问顺序；`start/end`：子树在 dfs 序里的区间',
        'start[now.val] =': lambda S, B, r: f'到节点 `{S.now.val}`：深度 `{S.level}`，是第 `{S.start[S.now.val]}` 个被访问的 → `start[{S.now.val}] = {S.start[S.now.val]}`',
        'end[now.val] =': _cap_end,
        'dfs(root, 0)': '根深度 0，开始 dfs：整棵子树在 dfs 序里是==连续的一段==',
        'prefix_max = [': '`prefix_max[i]`：dfs 序前 `i+1` 个节点的最大深度，先放第一个',
        'prefix_max.append': _cap_pre_in,
        'suffix_max = [': '`suffix_max` 从后往前建，先放最后一个节点的深度',
        'suffix_max.append': _cap_suf_in,
        'suffix_max.reverse()': '翻转后 `suffix_max[i]` = 位置 `i` 到末尾的最大深度 = `{suffix_max}`',
        'res = []': '开始处理查询：删掉一棵子树 = 删掉 dfs 序里的一个区间，其余节点深度不变',
        'res.append(0)': _cap_pr,
        'print(start[q], end[q])': '',
        'if start[q] > 0': lambda S, B, r: (f'`start = {S.start[S.q]} > 0` → 左边有前缀' if S.start[S.q] > 0 else '`start = 0` → 左边没有前缀'),
        'res[-1] = max(res[-1], prefix_max': _cap_lo,
        'if end[q] <': lambda S, B, r: (f'`end = {S.end[S.q]} < {len(S.dfs_order) - 1}` → 右边有后缀' if S.end[S.q] < len(S.dfs_order) - 1 else f'`end = {S.end[S.q]}` 已是最后一位 → 右边没有后缀'),
        'res[-1] = max(res[-1], suffix_max': _cap_hi,
        'return res': lambda S, B, r: f'三个查询的答案：`{r}`',
    },
    skip=['print(', 'dfs_order = []', 'start = {}', 'end = {}', 'if now.', 'for index in range', 'dfs_order.append', 'depth[now.val]', 'res.append(0)'],
    max_steps=60,
    cards=dict(
        one_liner='子树 = dfs 序里的一段区间；删掉它，剩下前缀和后缀取最大深度',
        complexity='时间 `O(n + m)`，空间 `O(n)`',
        problem=['二叉树，值是互不相同的 `1..n`；每次查询删掉以 `queries[i]` 为根的子树，返回此时树的高度（根到最远节点的==边数==）',
                 '查询彼此独立，每次删完树会恢复',
                 '示例：`[5,8,9,2,1,3,7,4,6]`，`queries=[3,2,4,8]` → `[3,2,3,2]`',
                 '本视频用小一点的树 `[1,2,3,4,5,null,null,6]`，`queries=[3,4,2]`'],
        quote='移除子树并不会对其他节点的深度造成影响，也就是说这里要求的其实是剩余节点深度的最大值。',
        quote_src='—— yiduobo 题解原文',
        idea=['树的高度 = 所有节点深度的最大值；删子树不改变别人的深度',
              '用 dfs 序把子树变成区间：记每个节点的 `start`、`end`',
              '剩下的必然是一段前缀和一段后缀 → 预处理 `prefix_max`、`suffix_max`',
              '每个查询：`max(prefix_max[start-1], suffix_max[end+1])`，`O(1)`'],
        result='运行结束，每个查询都是 `O(1)` 拼出答案：`[3, 2, 1]`',
        summary=['时间 `O(n + m)`，空间 `O(n)`',
                 '易错：`start == 0` 时没有前缀，`end` 是最后一位时没有后缀，下标要先判断',
                 '深度从 0 起算，所以最大深度就是边数，不用再减 1',
                 '对比灵神：灵神用“子树高度 + 剩余高度”两遍 dfs；yiduobo 把子树拍成区间',
                 '原文为 Python 2 写法，`print start[q], end[q]` 已改为 `print(start[q], end[q])`'],
    ),
)
