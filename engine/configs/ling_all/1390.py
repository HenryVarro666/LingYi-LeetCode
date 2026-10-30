def _nd(x):
    return [d for d in range(1, x + 1) if x % d == 0]


CONFIG = dict(
    num=1390, title='四因数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='倍数筛预处理因子个数与因子和',
    tags=['灵神题单', '数学算法', '难度分 1478'],
    code='''
MX = 100_001
divisor_num = [0] * MX
divisor_sum = [0] * MX
for i in range(1, MX):
    for j in range(i, MX, i):  # 枚举 i 的倍数 j
        divisor_num[j] += 1  # i 是 j 的因子
        divisor_sum[j] += i

class Solution:
    def sumFourDivisors(self, nums: List[int]) -> int:
        ans = 0
        for x in nums:
            if divisor_num[x] == 4:
                ans += divisor_sum[x]
        return ans
''',
    call='Solution().sumFourDivisors([21, 4, 7, 8])',
    expect=47,
    views=[
        dict(type='array', var='nums', h=200, label='nums（黄 = 当前 x，绿 = 恰有 4 个因子）',
             color=lambda S, i, v: ('green' if len(_nd(v)) == 4 and 'x' in S and (S['nums'].index(S['x']) > i or S['nums'].index(S['x']) == i and S['ans'] > 0 and S['_line'] > 13) else 'yellow' if 'x' in S and S['nums'][i] == S['x'] else None) if 'x' in S else None),
        dict(type='text', fn=lambda S: (f"`x = {S['x']}` 的因子：{'、'.join(map(str, _nd(S['x'])))}（共 =={len(_nd(S['x']))}== 个，和 {sum(_nd(S['x']))}）" if 'x' in S else ''), size=26),
    ],
    watch=[('x', 'x', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '预处理已经在题目开始前做完：`divisor_num[x]` 是 x 的因子个数，`divisor_sum[x]` 是因子和',
        'for x in nums': '依次看每个数 `x = {x}`',
        'if divisor_num[x] == 4': lambda S, B, r: (f'`divisor_num[{S.x}] = {len(_nd(S.x))} == 4`：恰有四个因子，要算' if len(_nd(S.x)) == 4 else f'`divisor_num[{S.x}] = {len(_nd(S.x))} != 4`：因子个数不对，跳过'),
        'ans += divisor_sum[x]': '`ans += divisor_sum[{x}] = {sum(_nd(x))}` → =={ans}==',
        'return ans': '所有恰有四个因子的数，因子和累加得 `{ans}`',
    },
    cards=dict(
        one_liner='反过来想：枚举 i，把它的所有倍数的因子数加一',
        complexity='预处理 `O(U log U)`，查询时间 `O(n)`，空间 `O(U)`',
        problem=['返回 `nums` 中恰有 4 个因子的整数的因子之和，没有则返回 `0`',
                 '示例：`[21,4,7]` → `32`（只有 21 有 4 个因子：1,3,7,21）',
                 '本视频：`[21,4,7,8]` → `47`（21 的 32 + 8 的 15）'],
        quote='对于一个数，它有哪些因子？这不能一眼看出来。但反过来，对于一个数 i，i 的倍数都有因子 i。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举 `i` 和它的倍数 `j`：`divisor_num[j] += 1`，`divisor_sum[j] += i`',
              '预处理放在类外面，所有测试数据共用一次',
              '每个数只需查表：因子个数是 4 就累加因子和'],
        summary=['预处理是调和级数 `O(U log U)`，`U = 10^5`，只做一次',
                 '查询只有 `O(n)`：查表比较、累加',
                 '预处理在类外，视频里不逐行演示（量太大），只演示查询',
                 '另一种思路是分解质因数，但预处理更好写'],
    ),
)
