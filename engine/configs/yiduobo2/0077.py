def _inner(S):
    return S.get('_inner') or {}


def _range(S):
    I = _inner(S)
    if 'now' not in I or 'level' not in I or I['level'] == I.get('k'):
        return None
    return I['now'][-1] + 1, I['n']


def _cand_color(S, idx, v):
    I = _inner(S)
    rg = _range(S)
    if rg is None:
        return None
    if 'index' in I and v == I['index']:
        return 'yellow'
    if rg[0] <= v <= rg[1]:
        return 'blue'
    return None


def _cand_dim(S, idx, v):
    rg = _range(S)
    return rg is not None and not (rg[0] <= v <= rg[1])


def _info(S):
    I = _inner(S)
    if 'level' not in I:
        return '`now[0] = 0` 是哨兵：第一个数可以从 `0 + 1 = 1` 开始'
    if I['level'] == I['k']:
        return f"已经选了 `level = {I['level']} = k` 个数 → `now[1:]` 就是一个组合"
    lo, hi = I['now'][-1] + 1, I['n']
    if lo > hi:
        return f"`now[-1] = {I['now'][-1]}`，后面==没有更大的数==可选 → 这条分支白跑"
    return f"已选 `level = {I['level']}` 个；下一个数要比 `now[-1] = {I['now'][-1]}` 大：只试 `{lo}..{hi}`"


def _cap_for(S, B, ret):
    lo = S.now[-1] + 1
    if lo > S.n:
        return f'`range({lo}, {S.n + 1})` 是空的：`{S.now[-1]}` 后面没有数可选，凑不满 `k` 个 → ==白跑一趟==（原文没有剪枝）'
    if 'index' in B and S.index == B.index:
        return f'`{lo}..{S.n}` 都试过了 → 返回上一层'
    if S.index == lo:
        return f'组合要求 now ==单调递增==：只试比 `now[-1] = {S.now[-1]}` 大的数 `{lo}..{S.n}`，先试 `{S.index}`'
    return f'换下一个数：`index = {S.index}`'


CONFIG = dict(
    num=77, title='组合', difficulty='Medium', category='回溯',
    author='yiduobo', technique='搜索回溯 · now 单调递增 + 哨兵 0',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def combine(self, n, k):
        now = [0]
        res = []

        self.dfs(0, n, k, now, res)
        return res

    def dfs(self, level, n, k, now, res):
        if level == k:
            res.append(now[1:])
            return

        for index in range(now[-1] + 1, n + 1):
            now.append(index)
            self.dfs(level + 1, n, k, now, res)
            now.pop()
''',
    call='Solution().combine(3, 2)',
    expect=[[1, 2], [1, 3], [2, 3]],
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='array', var=lambda S: list(range(1, S['n'] + 1)) if 'n' in S else None,
             label='1..n（蓝 = 本层能试的数，黄 = 当前 index，暗 = 不能选）', cell=90, h=150,
             color=_cand_color, dim=_cand_dim, index=False),
        dict(type='stack', var='now', label='now（now[0] = 0 是哨兵）', h=105),
        dict(type='calls', h=190, hide=('n', 'k', 'now', 'res')),
        dict(type='stack', var='res', label='res', h=105),
    ],
    watch=[('level', lambda S: _inner(S).get('level'), 'blue'), ('now[-1]', lambda S: _inner(S)['now'][-1], 'cyan'),
           ('index', lambda S: _inner(S).get('index'), 'yellow'), ('now', 'now', 'green'), ('len(res)', 'len(res)')],
    captions={
        'now = [0]': '`now = [0]`：先放一个哨兵 0，这样第一个数也能统一写成 `now[-1] + 1` 开始',
        'self.dfs(0, n, k, now, res)': '从 `level = 0`（一个数都没选）开始搜索',
        'if level == k': lambda S, B, ret: ('`level == k`：已经选够 `k` 个数' if S.level == S.k
                                            else f'`level = {S.level} < k = {S.k}`：还要继续选'),
        'res.append(now[1:])': '去掉哨兵，`now[1:] = {res[-1]}` 加入答案（切片==自带复制==）',
        '            return': '叶子：返回上一层',
        'for index in range': _cap_for,
        'now.append(index)': '选 `{index}` → now = `{now}`',
        'self.dfs(level + 1': lambda S, B, ret: (f'下一轮：`dfs(level = {B.level + 1})`，已选够 `k` 个 → 去记录答案' if B.level + 1 == B.k
                                                 else f'下一轮：`dfs(level = {B.level + 1})`，从比 `{B.index}` 大的数里继续选'),
        'now.pop()': '回溯：弹出 `{B.now[-1]}`，now 回到 `{now}`',
        'return res': '共 `{len(ret)}` 个组合',
    },
    skip=['res = []'],
    max_steps=60,
    cards=dict(
        one_liner='每轮往 now 里加一个比末尾更大的数，加满 k 个就是一个组合',
        complexity='时间 `O(k·C(n,k))` 量级，空间 `O(k)`（不计返回值）',
        problem=['给定 `n` 和 `k`，返回 `[1, n]` 中所有 `k` 个数的组合（顺序任意）',
                 '示例：`n = 4, k = 2` → `[[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]`',
                 '本视频：`n = 3, k = 2` → 3 个组合'],
        quote='因为题目中要求的是组合，因此我们可以==要求now满足单调递增==，于是在每次操作时，只需要尝试now[-1] + 1到n之间的数即可。为了方便起见，可以首先令now[0] = 0，来处理边界情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['经典搜索回溯：每轮把一个数加入 `now`，然后进行下一轮',
              '组合不讲顺序 → 规定 now ==递增==，`[2,1]` 这种就不会再出现',
              '哨兵 `now[0] = 0`：第一轮也是 `now[-1] + 1 = 1` 起步，不用特判'],
        result='得到 `[[1,2],[1,3],[2,3]]` ✓',
        summary=['复杂度：每个组合复制 `O(k)`，共 `C(n,k)` 个组合，外加一些走不通的分支',
                 '易错：答案要去掉哨兵，写 `now[1:]`（切片同时完成了复制）',
                 '没有剪枝：`now = [0,3]` 时后面已没有数，仍会进入一层空循环；灵神用 `j ≥ d` 剪掉这种分支',
                 '原文为 Python 2 写法，只删去了类型说明文档字符串，代码未改'],
    ),
)
