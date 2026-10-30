NUMS = [1, 0, 2, 0, 0, 1, 2, 1]


def _pos(S, x):
    last = S.get('last')
    if not last:
        return None
    v = last[x]
    return v if isinstance(v, int) else None


L1 = lambda S: _pos(S, 0)  # noqa: E731
L2 = lambda S: _pos(S, 1)  # noqa: E731


def _color(S, i, v):
    if 'i' in S and i == S['i'] and v > 0:
        return 'yellow'
    if i == _pos(S, 0):
        return 'cyan'
    if i == _pos(S, 1):
        return 'orange'
    return None


def _dim(S, i, v):
    return 'i' in S and i > S['i']


def _txt(S):
    if 'last' not in S:
        return '遍历时记录 1 和 2 ==上一次出现的位置=='
    last = S['last']
    f = lambda v: '-inf' if v == -float('inf') else str(v)  # noqa: E731
    s = f"`last[0]`（上一个 1）= {f(last[0])}，`last[1]`（上一个 2）= {f(last[1])}"
    if 'ans' in S and S['ans'] < float('inf'):
        s += f"，`ans = {S['ans']}`"
    return s


def _upd(S, B, r):
    i, x = S.i, S.x
    want = '2' if x == 0 else '1'
    j = S.last[x ^ 1] if S._line != 13 else B.last[x ^ 1]
    if j == -float('inf'):
        return f'左边还没有出现过 {want}：`i − (−inf) = inf`，答案不变'
    return (f'`last[{x} ^ 1] = last[{x ^ 1}] = {j}` 是上一个 {want}：距离 `{i} − {j} = {i - j}`，'
            + (f'==更新== `ans = {S.ans}`' if S.ans != B.ans else f'不小于 `{S.ans}`，不变'))


CONFIG = dict(
    num=3880, title='两个值之间的最小绝对差值', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右，维护左 · 记录上次出现位置',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1257'],
    code='''
class Solution:
    def minAbsoluteDifference(self, nums: List[int]) -> int:
        ans = inf
        last = [-inf] * 2  # last[x] 表示 x+1 上一次出现的位置

        for i, x in enumerate(nums):
            if x > 0:
                # 如果 x 是 1，那么找上一个 2 的位置
                # 如果 x 是 2，那么找上一个 1 的位置
                x -= 1
                ans = min(ans, i - last[x ^ 1])
                last[x] = i

        return ans if ans < inf else -1
''',
    call=f'Solution().minAbsoluteDifference({NUMS})',
    expect=1,
    views=[
        dict(type='text', fn=_txt, h=90, size=28),
        dict(type='array', var='nums', h=330, cell=104, pointers={'i': 'yellow', L1: 'cyan', L2: 'orange'},
             pointer_labels={L1: '上个1', L2: '上个2'}, color=_color, dim=_dim,
             label='nums（黄 = 当前 i，青 = 上一个 1，橙 = 上一个 2）'),
    ],
    watch=[('i', 'i', 'yellow'), 'x', ('last', 'last'), ('ans', 'ans', 'green')],
    captions={
        'ans = inf': '`ans = inf`：最小距离，先设成无穷大',
        'last = [-inf]': '`last[0]` 记 ==1== 上次的位置，`last[1]` 记 ==2== 上次的位置；初始 `-inf`',
        'for i, x in enumerate': lambda S, B, r: (f'枚举右：`nums[{S.i}] = {S.x}`' if B.get('i') != S.i
                                                  else '遍历结束'),
        'if x > 0': lambda S, B, r: (f'`x = {S.x}` 是 {S.x}：去左边找上一个 =={3 - S.x}==' if S.x > 0
                                     else '`x = 0`，与答案无关，跳过'),
        'x -= 1': '`x` 减一变成下标：1 → 0，2 → 1，现在 `x = {x}`；`x ^ 1` 就是另一个数的下标',
        'ans = min': _upd,
        'last[x] = i': lambda S, B, r: f'记录：{S.x + 1} 最近一次出现在 `last[{S.x}] = {S.i}`',
        'return ans': lambda S, B, r: (f'`ans = {S.ans} < inf`，返回 =={r}==' if S.ans < float('inf')
                                       else '`ans` 仍是 `inf`：没有有效下标对，返回 -1'),
    },
    cards=dict(
        one_liner='遇到 1 找上一个 2，遇到 2 找上一个 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 只含 0、1、2；`nums[i] == 1` 且 `nums[j] == 2` 的 `(i, j)` 是有效对',
                 '求有效对中 `abs(i − j)` 的==最小值==，没有就返回 `-1`',
                 '示例：`[1,0,0,2,0,1]` → `2`；本视频 `[1,0,2,0,0,1,2,1]` → `1`'],
        quote='无需找 i 右边的 j，因为我们会继续遍历，==遍历到 j 那个位置时，它会去找左边的 i==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['维护 `last[x]`：元素 `x` 上一次出现的位置',
              '遇到 1，用 `i − 上一个 2 的位置` 更新答案；遇到 2 同理',
              '`x -= 1` 后，`x ^ 1` 把 0 ↔ 1 互换，一行代码同时处理两种情况'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '只看==最近==的另一个数：更早的位置距离只会更大',
                 '`last` 初始 `-inf`：`i − (−inf) = inf`，不会误更新答案',
                 '易错：没有有效对时返回 `-1`，不是 `inf`'],
    ),
)
