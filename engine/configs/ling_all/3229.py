def _find(S, n, t):
    for i, (x, y) in enumerate(zip(S['nums'], S['target'])):
        if x == n and y == t:
            return i
    return 0


def _cur(S):
    """已经处理到差分数组 d 的哪一个下标"""
    return _find(S, S['n2'], S['t2']) if 'n2' in S else 0


def _a(S):
    return [t - n for n, t in zip(S['nums'], S['target'])]


def _d(S):
    a = _a(S)
    return [a[0]] + [a[i] - a[i - 1] for i in range(1, len(a))]


def _dcolor(S, i, v):
    if i > _cur(S) or 'pos_sum' not in S:
        return None
    return 'green' if v > 0 else ('pink' if v < 0 else None)


def _text(S):
    if 'pos_sum' not in S:
        return ''
    return f"`pos_sum = {S['pos_sum']}`（d 中正数之和），`neg_sum = {S['neg_sum']}`（负数绝对值之和）"


CONFIG = dict(
    num=3229, title='使数组等于目标数组所需的最少操作次数', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='差分数组 · max(正数和, 负数和)',
    tags=['灵神题单', '常用数据结构', '难度分 2067'],
    code='''
class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        pos_sum = neg_sum = 0
        d = target[0] - nums[0]
        if d > 0:
            pos_sum = d
        else:
            neg_sum = -d
        for (n1, t1), (n2, t2) in pairwise(zip(nums, target)):
            d = (t2 - n2) - (t1 - n1)
            if d > 0:
                pos_sum += d
            else:
                neg_sum -= d
        return max(pos_sum, neg_sum)
''',
    call='Solution().minimumOperations([3,5,1,2,2], [4,3,2,4,1])',
    expect=6,
    views=[
        dict(type='array', var='nums', label='nums', h=120, index=False),
        dict(type='array', var='target', label='target', h=120, index=False),
        dict(type='array', var=_a, label='a = target - nums（要把 a 变成全 0）', h=130, index=False),
        dict(type='array', var=_d, label='d = a 的差分（绿 = 正，粉 = 负；暗 = 还没算到）', h=150, color=_dcolor,
             dim=lambda S, i, v: i > _cur(S) or 'pos_sum' not in S),
        dict(type='text', fn=_text, h=50),
    ],
    watch=['d', ('pos_sum', 'pos_sum', 'green'), ('neg_sum', 'neg_sum', 'pink')],
    captions={
        'pos_sum = neg_sum = 0': '`pos_sum`：差分里正数之和；`neg_sum`：负数绝对值之和',
        'd = target[0] - nums[0]': '`a[0] = target[0] - nums[0] = {d}`，它就是差分数组的第一个数 `d[0]`',
        'pos_sum = d': '`pos_sum = {pos_sum}`',
        'neg_sum = -d': '`neg_sum = -({d}) = {neg_sum}`',
        'for (n1, t1)': lambda S, B, r: ('所有相邻位置都处理完' if 'n2' in B and B.n2 == S.n2 and B.t2 == S.t2 else f'取相邻两个位置：`a` 从 `{S.t1 - S.n1}` 变到 `{S.t2 - S.n2}`'),
        'd = (t2 - n2)': '差分 `d = a[i] - a[i-1] = ({t2} - {n2}) - ({t1} - {n1})`，得 =={d}==',
        'if d > 0:': lambda S, B, r: (f'`d = {S.d} > 0` → 正数，计入 `pos_sum`' if S.d > 0 else f'`d = {S.d} <= 0` → 计入 `neg_sum`（取绝对值）'),
        'pos_sum += d': '正的差分要靠「一次 -1」的操作消掉：`pos_sum` → {pos_sum}',
        'neg_sum -= d': '负的差分要靠「一次 +1」的操作消掉：`neg_sum` 加上 `{-d}` → {neg_sum}',
        'return max': '一次操作能同时抵消一个正数和一个负数，剩下的单独处理 → `max({pos_sum}, {neg_sum})`，等于 =={ret}==',
    },
    cards=dict(
        one_liner='子数组 ±1 就是差分数组两处一加一减，答案是 max(正数和, 负数和)',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次选 `nums` 的一个子数组，整体加 1 或减 1',
                 '求把 `nums` 变成 `target` 的最少操作次数',
                 '示例：`nums=[3,5,1,2,2], target=[4,3,2,4,1]` → `6`'],
        quote='「子数组内的每个元素的值增加或减少 1」这个操作等价于修改差分数组两个位置上的数，一个加一，另一个减一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['令 `a = target - nums`，目标是把 `a` 变成全 0，也就是把差分 `d` 变成全 0',
              '一次操作改 `d` 两处：一处 +1、另一处 -1；改后缀时只改一处',
              '正负配对最划算：先抵消 `min` 次，剩下的单独处理，共 `max(pos_sum, neg_sum)`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`d[0]` 要单独处理，它前面相当于有一个 0',
                 '`d == 0` 归到 else 里也没问题：`neg_sum -= 0`',
                 '写法二：给两个数组前面补 0，省去单独处理首项',
                 '`pairwise` 需要 Python 3.10+'],
    ),
)
