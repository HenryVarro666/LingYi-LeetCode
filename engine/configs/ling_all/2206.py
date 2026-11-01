CONFIG = dict(
    num=2206, title='将数组划分成相等数对', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='奇偶标记 + 奇数个数（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def divideArray(self, nums: List[int]) -> bool:
        parity = defaultdict(int)
        odd = 0
        for v in nums:
            parity[v] ^= 1
            odd += parity[v] * 2 - 1
        return odd == 0
''',
    call='Solution().divideArray([3, 2, 3, 2, 2, 2])',
    expect=True,
    views=[
        dict(type='array', var='nums', label='nums', cell=90, h=170),
        dict(type='map', var='parity', label='parity（1 = 出现奇数次，0 = 偶数次）', fmt=lambda k, v: f'{k}: {v}', h=150, font=34),
        dict(type='text', fn=lambda S: f"`odd = {S['odd']}`：当前出现奇数次的数有 =={S['odd']}== 种" if 'odd' in S else '', size=30),
    ],
    watch=[('v', 'v', 'blue'), ('odd', 'odd', 'orange')],
    captions={
        'parity = defaultdict': '`parity[x]` 记录 x 出现次数的奇偶性（默认 0 = 偶数次）',
        'odd = 0': '`odd` 统计当前出现奇数次的数的种数；最后为 0 才能全部配对',
        'for v in nums': '看下一个数 `v = {v}`',
        'parity[v] ^= 1': lambda S, B, ret: (f'`parity[{S.v}]` 异或 1：{S.parity[S.v] ^ 1} → {S.parity[S.v]}，'
                                             + ('变成奇数次' if S.parity[S.v] else '变成偶数次，凑成了一对')),
        'odd += ': lambda S, B, ret: (f'`parity[{S.v}] = {S.parity[S.v]}` → `odd += {S.parity[S.v] * 2 - 1}`（'
                                      + ('多了一个奇数次的数' if S.parity[S.v] else '少了一个奇数次的数') + f'）→ `odd = {S.odd}`'),
        'return odd == 0': lambda S, B, ret: (f'`odd = {S.odd}`：每种数都出现偶数次 → ==能全部配成对==，返回 `True`' if S.odd == 0
                                             else f'`odd = {S.odd}`：还有出现奇数次的数 → 返回 `False`'),
    },
    cards=dict(
        one_liner='每种数出现偶数次才能配对；一遍扫描里实时维护奇数次的种数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums` 有 `2n` 个整数，要划分成 `n` 个数对，每个数对里两个数相等',
                 '能划分返回 `true`，否则 `false`',
                 '示例：`[3,2,3,2,2,2]` → `true`；`[1,2,3,4]` → `false`'],
        quote='parity[v] ^= 1; if parity[v] == 1 { odd++ } else { odd-- } …… 上面代码也可以进一步简化：odd += parity[v]*2 - 1',
        quote_src='—— 灵茶山艾府题解（Go 原文）',
        idea=['配对成功 ⇔ 每种数的出现次数都是偶数', '不用先统计再检查：遍历时用 `parity[v] ^= 1` 翻转奇偶',
              '奇变成 1 时 `odd` 加一，变回 0 时 `odd` 减一，一行写成 `parity[v]*2 - 1`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`map[int]int` → `defaultdict(int)`）；本视频选第三种（最简）写法，'
                 '前两种是先统计次数再检查偶数、以及用 if/else 维护 odd',
                 '时间 `O(n)`，空间 `O(n)`',
                 '易错：`parity[v]*2 - 1` 在 parity 为 1 时是 +1，为 0 时是 -1',
                 '同类题：136 只出现一次的数字（异或消对）'],
    ),
)
