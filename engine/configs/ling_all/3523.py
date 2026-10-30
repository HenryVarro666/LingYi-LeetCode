NUMS = [4, 2, 6, 3, 5, 7, 1]


def _kept(a, i):
    return i == 0 or a[i] >= max(a[:i])


def _cur(S):
    if 'x' not in S:
        return None
    return S['nums'].index(S['x'])


def _color(S, i, v):
    c = _cur(S)
    if c is None or i > c:
        return None
    if i == c and S['_line'] in (4, 5):
        return 'blue'
    return 'green' if _kept(S['nums'], i) else 'red'


def _dim(S, i, v):
    c = _cur(S)
    return c is not None and i < c and not _kept(S['nums'], i)


def _txt(S):
    if 'x' not in S:
        return '规则：左边有更大的数，这个数就必须去掉'
    return f"当前 `x = {S['x']}`，已保留的最大值 `mx = {S['mx']}`，已保留 ==`{S['ans']}`== 个"


CONFIG = dict(
    num=3523, title='非递减数组的最大长度', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='贪心 · 左边有更大数就必须删',
    tags=['灵神题单', '贪心与思维', '难度分 1435'],
    code='''
class Solution:
    def maximumPossibleSize(self, nums: List[int]) -> int:
        ans = mx = 0
        for x in nums:
            if x >= mx:
                mx = x
                ans += 1
        return ans
''',
    call=f'Solution().maximumPossibleSize({NUMS})',
    expect=3,
    views=[
        dict(type='text', fn=_txt),
        dict(type='array', var='nums', color=_color, dim=_dim, h=300),
    ],
    watch=[('mx', 'mx', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = mx = 0': '`ans` 统计保留的个数，`mx` 是已保留元素的最大值，都从 0 开始',
        'for x in nums': lambda S, B, r: ('`nums` 遍历完了，退出循环' if B.get('x') == S.x and S.nums.index(S.x) == len(S.nums) - 1 and 'x' in B else f'看下一个数 `x = {S.x}`'),
        'if x >= mx': lambda S, B, r: (
            f'`x = {S.x}` ≥ `mx = {S.mx}`：左边没有比它大的数 → ==保留==' if S.x >= S.mx
            else f'`x = {S.x}` < `mx = {S.mx}`：左边有更大的数 → ==必须删除=='),
        'mx = x': '保留 `x`，`mx` 更新为 `{mx}`',
        'ans += 1': '保留个数 `ans` → {ans}',
        'return ans': '保留的个数就是最大长度 `{ans}`',
    },
    cards=dict(
        one_liner='左边有更大的数，这个数就必须去掉；其余全保留',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一次操作：把一个子数组替换成它的最大值',
                 '操作若干次后数组要非递减，求最大可能长度',
                 '示例：`[4,2,5,3,5]` → `3`；本视频用 `[4,2,6,3,5,7,1]`'],
        quote='如果在元素 x=nums[i] 的左边，有比 x 大的数 y，那么 x 必须去掉。',
        quote_src='—— 灵茶山艾府题解（定理）',
        idea=['操作等价于：选一段，只留下最大值，其余都去掉',
              '反证：想保留 x，就得去掉它左边所有更大的数，但最大的那个永远去不掉',
              '第一个数左边没人，必保留；之后维护 `mx`，`x >= mx` 就保留'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '判断用 `>=`：和 `mx` 相等的数也能保留（非递减允许相等）',
                 '`mx` 只在保留时更新，被删的数不参与',
                 '本质是数「前缀最大值（含相等）」的个数'],
    ),
)
