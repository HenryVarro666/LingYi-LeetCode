NUMS = [7, 1, 5, 4, 9, 2]

TRACK = '''
class KList(list):  # 快照用的普通 list（带上下标 k）
    pass

class TList(list):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k in range(len(self)):
            self.k = k
            yield list.__getitem__(self, k)
        self.k = None

    def __deepcopy__(self, memo):
        c = KList(list.copy(self))
        c.k = getattr(self, 'k', -1)
        return c
'''


def _k(S):
    k = getattr(S.get('nums'), 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _left_end(S):
    """pre_min 覆盖的范围：执行完 pre_min 行后包含 x 自己"""
    k = _k(S)
    if k is None:
        return len(NUMS) - 1 if S.get('_line') == 8 else None
    return k if S.get('_line') == 7 else k - 1


def _color(S, i, v):
    k = _k(S)
    e = _left_end(S)
    if k is not None and i == k:
        return 'blue'
    if e is not None and e >= 0 and i <= e and v == S.get('pre_min'):
        return 'green'
    return None


def _dim(S, i, v):
    e = _left_end(S)
    k = _k(S)
    return k is not None and i > k


def _txt(S):
    if 'pre_min' not in S:
        return '把 `nums[j]` 当作卖出价，左边的==最小值==当作买入价'
    k = _k(S)
    if k is None:
        return f"遍历结束：最大差值 `ans = {S['ans']}`"
    x, pm = S['x'], S['pre_min']
    if S.get('_line') == 7:
        return f"`x = {x}` 当作 nums[i]：左边最小值更新为 =={pm}=="
    if pm == float('inf'):
        return f"`x = {x}` 左边没有数，`x − inf` 不会更新答案"
    return f"以 `x = {x}` 为 nums[j]：`{x} − pre_min({pm}) = {x - pm}`"


CONFIG = dict(
    num=2016, title='增量元素之间的最大差值', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右，维护左 · 前缀最小值',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1246'],
    code='''
class Solution:
    def maximumDifference(self, nums: List[int]) -> int:
        ans = 0
        pre_min = inf
        for x in nums:
            ans = max(ans, x - pre_min)  # 把 x 当作 nums[j]
            pre_min = min(pre_min, x)    # 把 x 当作 nums[i]
        return ans or -1
''',
    setup=TRACK,
    call=f'Solution().maximumDifference(TList({NUMS}))',
    expect=8,
    views=[
        dict(type='text', fn=_txt, h=90),
        dict(type='array', var='nums', h=300, cell=110, pointers={_k: 'blue'}, pointer_labels={_k: 'x'},
             color=_color, dim=_dim, label='nums（蓝 = 当前 x，绿 = 左边的最小值 pre_min）'),
    ],
    watch=[('x', 'x', 'blue'), ('pre_min', 'pre_min', 'green'), ('ans', 'ans', 'orange')],
    captions={
        'ans = 0': '`ans = 0`：==不能初始化成 -1==，`[1,1]` 的最大差值是 0，但要返回 -1',
        'pre_min = inf': '`pre_min` 维护==左边==的最小值；一开始左边没有数 → `inf`',
        'for x in nums': lambda S, B, r: (f'枚举右：`x = nums[{_k(S)}] = {S.x}`' if _k(S) is not None
                                          else '每个数都当过一次 nums[j]，循环结束'),
        'ans = max': lambda S, B, r: (f'`{S.x} − inf` 是负无穷，答案不变' if S.pre_min == float('inf') else
                                      f'`{S.x}` 当卖出价：差值 `{S.x} − {S.pre_min} = {S.x - S.pre_min}`，'
                                      + (f'==更新== `ans = {S.ans}`' if S.ans != B.ans else f'不超过 `{S.ans}`，答案不变')),
        'pre_min = min': lambda S, B, r: (f'再把 `{S.x}` 当成以后的 nums[i]：==更小==，`pre_min` → {S.pre_min}'
                                          if S.pre_min != B.pre_min else
                                          f'再把 `{S.x}` 当成以后的 nums[i]：不比 `{S.pre_min}` 小，`pre_min` 不变'),
        'return ans or -1': lambda S, B, r: (f'`ans = {S.ans}` 不为 0 → 返回 =={r}==' if S.ans
                                             else '`ans` 仍为 0：不存在 `nums[i] < nums[j]` → 返回 -1'),
    },
    cards=dict(
        one_liner='和 121 买卖股票一样：枚举卖出价，维护左边最低买入价',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['求 `nums[j] − nums[i]` 的最大值，要求 `i < j` 且 ==`nums[i] < nums[j]`==',
                 '不存在这样的 `i, j` 就返回 `-1`',
                 '示例：`[7,1,5,4]` → `4`；本视频：`[7,1,5,4,9,2]` → `8`'],
        quote='从左到右枚举卖出价格 nums[j]，要想获得最大利润，我们需要知道从 prices[0] 到 prices[j−1] 的==最小值（前缀最小值）==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举右：`x` 当 nums[j]，用 `x − pre_min` 更新答案',
              '维护左：再把 `x` 当成以后的 nums[i]，更新 `pre_min`',
              '==先算答案再更新 pre_min==，保证 `i < j`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`ans` 要初始化为 0，`ans or -1` 把 0 转成 -1（相等的数差值为 0 不合法）',
                 '两行顺序不能反：先更新 pre_min 会让 `i = j`',
                 '同类：121 买卖股票、题单「§0.1 枚举右，维护左」'],
    ),
)
