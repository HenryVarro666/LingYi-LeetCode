NUMS = [18, 43, 36, 13, 7]

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


def _expr(x):
    return ' + '.join(str(x)) + f' = {_ds(x)}' if x >= 10 else str(x)


def _ds(x):
    return sum(map(int, str(x)))


def _color(S, i, v):
    k = _k(S)
    if k is None:
        return None
    if i == k:
        return 'blue'
    if i < k and S.get('_line') in (6, 7) and _ds(v) == S['s'] and S['mx'][S['s']] == v:
        return 'green'
    return None


def _dim(S, i, v):
    k = _k(S)
    return k is not None and i > k


def _mx(S):
    mx = S.get('mx')
    if mx is None:
        return None
    return {s: v for s, v in enumerate(mx) if v != -float('inf')}


def _txt(S):
    if 'mx' not in S:
        return '`mx[s]`：左边数位和为 `s` 的==最大==的数'
    k = _k(S)
    if k is None:
        return f"遍历结束，最大和 `ans = {S['ans']}`"
    if 's' not in S or S.get('_line') == 5:
        return f"枚举 `nums[j] = {S['num']}`"
    return f"`{S['num']}` 的数位和 `s = {_expr(S['num'])}`"


def _ans(S, B, r):
    s, num, m = S.s, S.num, S.mx[S.s]
    if m == -float('inf'):
        return f'左边没有数位和为 {s} 的数：`mx[{s}] = -inf`，答案不变'
    return (f'左边数位和为 {s} 的最大数是 `mx[{s}] = {m}`：`{m} + {num} = {m + num}`，'
            + (f'==更新== `ans = {S.ans}`' if S.ans != B.ans else f'不超过 `{S.ans}`，不变'))


CONFIG = dict(
    num=2342, title='数位和相等数对的最大和', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右，维护左 · 按数位和记最大值',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1309'],
    code='''
class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        ans = -1
        mx = [-inf] * 82  # 至多 9 个 9 相加
        for num in nums:  # 枚举 num = nums[j]
            s = sum(map(int, str(num)))  # 更快的写法见【Python3 写法二】
            ans = max(ans, mx[s] + num)  # 左边找一个数位和也为 s 的最大的 nums[i]
            mx[s] = max(mx[s], num)  # 维护数位和等于 s 的最大元素
        return ans
''',
    setup=TRACK,
    call=f'Solution().maximumSum(TList({NUMS}))',
    expect=54,
    views=[
        dict(type='text', fn=_txt, h=90),
        dict(type='array', var='nums', h=260, cell=120, pointers={_k: 'blue'}, pointer_labels={_k: 'num'},
             color=_color, dim=_dim, label='nums（蓝 = 当前 nums[j]，绿 = 能和它配对的最大 nums[i]）'),
        dict(type='map', var=_mx, label='mx（只画出已有值的数位和 s → 最大的数）',
             fmt=lambda k, v: f's={k}: {v}', h=170, font=32),
    ],
    watch=[('num', 'num', 'blue'), 's', ('ans', 'ans', 'green')],
    captions={
        'ans = -1': '`ans = -1`：没有数位和相同的两个数就返回 -1',
        'mx = [-inf]': '`mx[s]`：数位和为 `s` 的最大元素；数位和至多 `9 × 9 = 81`，开 82 个位置',
        'for num in nums': lambda S, B, r: (f'枚举右：`num = nums[{_k(S)}] = {S.num}`' if _k(S) is not None
                                            else '所有数都枚举完了'),
        's = sum(': lambda S, B, r: f"数位和 `s = {_expr(S.num)}`",
        'ans = max': _ans,
        'mx[s] = max': lambda S, B, r: (f'维护左：`mx[{S.s}]` → =={S.mx[S.s]}==，留给后面数位和为 {S.s} 的数配对'
                                        if S.mx[S.s] != B.mx[S.s] else
                                        f'`{S.num}` 不比 `mx[{S.s}] = {S.mx[S.s]}` 大，不变'),
        'return ans': '返回最大和 =={ans}==',
    },
    cards=dict(
        one_liner='回想两数之和：枚举 nums[j]，查左边同数位和的最大数',
        complexity='时间 `O(n log U)`，空间 `O(D log U)`',
        problem=['选 `i ≠ j`，要求 `nums[i]` 与 `nums[j]` 的==数位和相等==',
                 '求 `nums[i] + nums[j]` 的最大值，不存在返回 `-1`',
                 '示例：`[18,43,36,13,7]` → `54`（18 + 36，数位和都是 9）'],
        quote='枚举 nums[j]，设 nums[j] 的数位和为 s，我们需要知道 j 左边的数位和也等于 s 的==最大==的 nums[i]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['和 1. 两数之和一样「枚举右，维护左」',
              '`mx[s]` 记录左边数位和为 `s` 的最大值，用 `mx[s] + nums[j]` 更新答案',
              '==先更新答案，再更新 mx==，避免 nums[j] 和自己配对'],
        summary=['时间 `O(n log U)`，`U = max(nums)`；空间 `O(D log U)`，`D = 9`',
                 '`mx` 初始 `-inf`：没配对时 `-inf + num` 不会更新答案',
                 '更快的写法二：用 `% 10`、`//= 10` 手动求数位和，避免转字符串',
                 '同类：题单「§0.1 枚举右，维护左」'],
    ),
)
