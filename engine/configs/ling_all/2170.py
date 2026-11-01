def _top2(a):
    return '、'.join(f'{p.num}×{p.cnt}' for p in a[:2])


def _cnt(S, par):
    # 外层 cnt 在 getMaxCnt2 里被同名形参遮住，这里按 nums 前 i+1 个数重算同样的计数
    if 'i' not in S or 'nums' not in S:
        return {}
    d = {}
    for k, v in enumerate(S['nums'][:S['i'] + 1]):
        if k % 2 == par:
            d[v] = d.get(v, 0) + 1
    return d


def _info(S):
    if 'a1' in S:
        return f"偶数下标最多的两个：`{_top2(S['a0'])}`；奇数下标：`{_top2(S['a1'])}`"
    if 'a0' in S:
        return f"偶数下标最多的两个：`{_top2(S['a0'])}`"
    return '先把偶数下标、奇数下标上的数分开统计，每组内要全部相等'


CONFIG = dict(
    num=2170, title='使数组变成交替数组的最少操作数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='正难则反：最多保留几个数不变（Go 原文转写）',
    tags=['灵神题单', '贪心算法', '难度分 1663'],
    code='''
class pair:
    def __init__(self, num: int, cnt: int):
        self.num = num
        self.cnt = cnt

class Solution:
    # 计算出现次数最多的两个元素及其出现次数
    def getMaxCnt2(self, cnt: dict) -> List[pair]:
        a = []
        for num, c in cnt.items():
            a.append(pair(num, c))
        a.sort(key=lambda p: -p.cnt)
        while len(a) < 2:  # 不足两个时，用 pair(0, 0) 填充
            a.append(pair(0, 0))
        return a[:2]

    def minimumOperations(self, nums: List[int]) -> int:
        cnt = [defaultdict(int), defaultdict(int)]
        for i, num in enumerate(nums):
            cnt[i & 1][num] += 1
        a0 = self.getMaxCnt2(cnt[0])
        a1 = self.getMaxCnt2(cnt[1])
        if a0[0].num != a1[0].num:
            return len(nums) - a0[0].cnt - a1[0].cnt  # 不相等时，保留出现次数最多的两个
        return len(nums) - max(a0[0].cnt + a1[1].cnt, a0[1].cnt + a1[0].cnt)  # 相等时，保留出现次数最多的和另一个出现次数次多的
''',
    call='Solution().minimumOperations([1,2,2,2,2])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 偶数下标，粉 = 奇数下标）',
             color=lambda S, i, v: 'blue' if i % 2 == 0 else 'pink', h=200),
        dict(type='map', var=lambda S: _cnt(S, 0), label='cnt[0]：偶数下标上各数的次数', fmt=lambda k, v: f'{k} → {v}', h=170),
        dict(type='map', var=lambda S: _cnt(S, 1), label='cnt[1]：奇数下标上各数的次数', fmt=lambda k, v: f'{k} → {v}', h=170),
        dict(type='text', fn=_info, size=28),
    ],
    skip=['for i, num', 'self.num = num', 'self.cnt = cnt'],
    watch=[('len(nums)', 'len(nums)', 'blue')],
    captions={
        'a = []': '`a` 收集 `(数, 次数)` 对',
        'a.append(pair(num, c))': '记下 `{num}` 出现了 `{c}` 次',
        'a.sort': '按次数从大到小排序：`{[(p.num, p.cnt) for p in a]}`',
        'while len(a) < 2': lambda S, B, ret: ('不足两个 → 用 `(0, 0)` 填充：0 不在 nums 里，相当于「保留 0 个」' if len(S.a) < 2 else '已经有两个了，不用填充'),
        'a.append(pair(0, 0))': '补上 `(0, 0)`：当前共 `{len(a)}` 项',
        'return a[:2]': '返回出现次数最多的两个：`{[(p.num, p.cnt) for p in ret]}`',
        'cnt = [defaultdict': '`cnt[0]` 统计偶数下标、`cnt[1]` 统计奇数下标',
                'cnt[i & 1][num] += 1': '`nums[{i}] = {num}`，下标是{"偶" if i % 2 == 0 else "奇"}数 → 记入 `cnt[{i & 1}]`：`{num}` 共 {cnt[i & 1][num]} 次',
        'a0 = ': '偶数组：最多的两个 `{[(p.num, p.cnt) for p in a0]}`',
        'a1 = ': '奇数组：最多的两个 `{[(p.num, p.cnt) for p in a1]}`',
        'if a0[0].num != a1[0].num': lambda S, B, ret: (f'两组最多的数：`{S.a0[0].num}` 和 `{S.a1[0].num}` → ' + ('==不同==，各保留自己最多的' if S.a0[0].num != S.a1[0].num else '==相同==，不能都保留，要让其中一组退而求其次')),
        'return len(nums) - a0[0].cnt - a1[0].cnt': '不相等：保留 `{a0[0].cnt} + {a1[0].cnt}` 个，改 `{ret}` 个',
        'return len(nums) - max': '相等：方案一 `{a0[0].cnt} + {a1[1].cnt}`，方案二 `{a0[1].cnt} + {a1[0].cnt}`，取大者 → 保留 `{len(nums) - ret}` 个，改 =={ret}== 个',
    },
    cards=dict(
        one_liner='正难则反：最多能保留几个数不动',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['交替数组：`nums[i-2] == nums[i]` 且 `nums[i-1] != nums[i]`；每次操作可改任一个数',
                 '示例：`[1,2,2,2,2]` → `2`（改成 `[1,2,1,2,1]`）'],
        quote='正难则反，考虑最多保留多少个数不变。',
        quote_src='—— 灵茶山艾府题解',
        idea=['按奇偶下标分成两组，每组内部要全相等',
              '两组最多的数不同：各保留自己的众数',
              '相同：一组保留众数，另一组退到次多的数（不足两个就用 0 补），两种取较大'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n)`，空间 `O(n)`',
                 '易错：两组众数相同时不能都保留，必须一组退而求其次',
                 '用 `(0, 0)` 填充，避免组内只有一种数时越界；Go 的 `sort.Slice` 改为 Python 的 `sort(key=…)`'],
    ),
)
