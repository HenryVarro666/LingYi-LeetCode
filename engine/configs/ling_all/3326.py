CONFIG = dict(
    num=3326, title='使数组非递减的最少除法操作次数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='倒序贪心 · 最小质因子 LPF',
    tags=['贪心与思维', '难度分 1864'],
    setup='''
MX = 1_000_001
LPF = [0] * MX
for i in range(2, MX):
    if LPF[i] == 0:
        for j in range(i, MX, i):
            if LPF[j] == 0:
                LPF[j] = i
''',
    code='''
class Solution:
    def minOperations(self, nums: List[int]) -> int:
        ans = 0
        for i in range(len(nums) - 2, -1, -1):
            if nums[i] > nums[i + 1]:
                nums[i] = LPF[nums[i]]
                if nums[i] > nums[i + 1]:
                    return -1
                ans += 1
        return ans
''',
    call='Solution().minOperations([3, 9, 25, 8, 49])',
    expect=2,
    views=[
        dict(type='text', h=90, size=30, fn=lambda S: (
            f"`nums[{S['i']}] = {S['nums'][S['i']]}` 对比右邻 `{S['nums'][S['i']+1]}`" if 'i' in S and S['i'] + 1 < len(S['nums'])
            else '从倒数第二个数开始，最后一个数不动')),
        dict(type='array', var='nums', label='nums（蓝 = 当前 i，右邻在它右边）', pointers={'i': 'blue'}, cell=110, h=300,
             color=lambda S, i, v: ('green' if 'i' in S and i > S['i'] else None)),
    ],
    watch=['i', ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 记操作次数；==最后一个数不用动==，所以从倒数第二个往前扫',
        'for i in range': '倒序枚举 `i`：右边已经定好，当前数只需 ==不超过右邻== 即可',
        5: lambda S, B, r: (
            f"`nums[{S.i}] = {S.nums[S.i]}` 比右邻 `{S.nums[S.i+1]}` 大 → ==必须操作==" if S.nums[S.i] > S.nums[S.i + 1]
            else f"`{S.nums[S.i]} ≤ {S.nums[S.i + 1]}`：已经不降，==能不操作就不操作==（保留大值给更左边的数让路）"),
        7: lambda S, B, r: (f"操作后 `nums[{S.i}] = {S.nums[S.i]}` 仍比右邻 `{S.nums[S.i+1]}` 大 → ==无解==" if S.nums[S.i] > S.nums[S.i+1]
                           else f"操作后 `{S.nums[S.i]} ≤ {S.nums[S.i+1]}`：已经不降，这次操作有效"),
        'nums[i] = LPF': '合数除以最大真因数，结果就是最小质因子：`nums[i]` 变成 ==`{nums[i]}`==（质数/1，不能再小）',
        'return -1': '变成最小质因子后仍比右邻大，再也变不小了 → ==返回 -1==',
        'ans += 1': '这次操作有效，`ans` → =={ans}==',
        'return ans': '全部不降，最少操作 =={ans}== 次',
    },
    cards=dict(
        one_liner='倒着扫：大了才除，且一次就除到最小质因子',
        complexity='预处理 `O(U log log U)`，查询 `O(n)`，`U = 10^6`',
        problem=['一次操作：把 `nums[i]` 除以它的==最大真因数==',
                 '求让 `nums` 变成非递减所需的最少操作次数，做不到返回 `-1`',
                 '示例：`[25,7]` → `1`；`[7,7,6]` → `-1`'],
        quote='如果 LPF(x)<x，说明 x 是合数，可以变小。由于题目规定只能除以最大真因数，我们可以把 x 除以 x/LPF(x)，得到 LPF(x)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['除以最大真因数，等价于把合数变成它的==最小质因子 LPF==',
              '最后一个数无需变小，从右往左贪心：比右邻大才操作',
              '操作后是质数或 1，再大于右邻就==无解=='],
        summary=['预处理 LPF 筛在配置的 setup 中执行（不逐行演示），视频只演示 `minOperations`',
                 '时间 `O(n)`（不计预处理），空间 `O(1)`',
                 '操作后变成质数或 1，不能重复操作；所以只判一次就够',
                 '同类：数学题单 §1.3 质因数分解、贪心 §1.4 从最左/最右开始贪心'],
    ),
)
