CONFIG = dict(
    num=4058, title='一个子数组循环移动后的最大脉冲值', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='转化为偶数长度最大子数组和',
    tags=['灵神题单·常用数据结构', '难度分 1899'],
    code='''
class Solution:
    def maxValue(self, nums: list[int]) -> int:
        alter_sum = nums[0]
        f0 = f1 = mx = 0
        for i in range(1, len(nums)):
            x = nums[i]
            alter_sum += -x if i % 2 else x
            d = x - nums[i - 1]
            f0, f1 = f1, max(f0, 0) + (d if i % 2 else -d)
            mx = max(mx, f1)
        return alter_sum + mx * 2
''',
    call='Solution().maxValue([2,6,3,7,1])',
    expect=11,
    views=[
        dict(type='array', var='nums', label='nums（奇数下标取负号；箭头 i = 当前元素）', pointers={'i': 'blue'}, h=240,
             color=lambda S, i, v: ('pink' if i % 2 else 'cyan') if 'i' in S and i <= S['i'] else None,
             dim=lambda S, i, v: 'i' in S and i > S['i']),
        dict(type='text', h=110, size=30,
             fn=lambda S: (f"`d = nums[{S['i']}] − nums[{S['i']-1}] = {S['d']}`，以 i 结尾的偶数长度段增量 `f1 = {S['f1']}`"
                           if 'f1' in S and 'd' in S and 'i' in S else '`f` 表示：以当前位置结尾、偶数长度的最大子数组和（取反收益的一半）')),
    ],
    watch=['alter_sum', 'f0', 'f1', ('mx', 'mx', 'green')],
    captions={
        'alter_sum = nums[0]': '先算原数组的脉冲值（交替和），第 0 项符号为正：`alter_sum = {alter_sum}`',
        'f0 = f1 = mx': '`f0`、`f1` 是上上一格、上一格的 f，`mx` 是最大增量的一半，都从 0 开始（也可以不操作）',
        'alter_sum += ': '累加交替和：下标 `{i}` 是{"奇数，减去" if i % 2 else "偶数，加上"} `{x}` → =={alter_sum}==',
        'd = x': '相邻两项之差 `d = {x} − {nums[i-1]} = {d}`：一对 `(i−1, i)` 取反后交替和的变化是 `2d`，`2` 留到最后统一乘',
        'f0, f1 =': '以 `i` 结尾的偶数长度段：把 `f0` 里 >0 的部分接上（`max({B.f0}, 0)`），再加这一对的贡献 `{d if i % 2 else -d}` → `f1 = {f1}`',
        'mx = max': '`mx = max({B.mx}, {f1}) = {mx}`：记录任意位置结尾的最大增量',
        'return': '答案 = 原脉冲值 `{alter_sum}` + 最大增量 `2 × {mx}` = =={ret}==',
    },
    cards=dict(
        one_liner='循环左移 = 对一段偶数长度的区间整体取反',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['脉冲值 = `a0 − a1 + a2 − …`（交替和）',
                 '可以选一段子数组循环左移一位，至多一次，求最大脉冲值',
                 '示例：`[2,6,3,7,1]` → 11'],
        quote='操作相当于：选择 nums 中的一个长为偶数的子数组，把每个元素都取反。',
        quote_src='—— 灵茶山艾府题解',
        idea=['偶数长段：所有元素符号翻转；奇数长段：只有第一个符号不变，其余翻转，等价于翻转偶数个元素',
              '于是问题变成：求 `b[i] = 2(−1)^(i+1)·nums[i]` 里偶数长度的最大子数组和',
              '两两一对，`f[i+1] = max(f[i−1], 0) + b[i−1] + b[i]`，答案 = 原交替和 + `max(f)`'],
        summary=['时间 `O(n)`，空间 `O(1)`（优化前用 `f` 数组，空间 `O(n)`）',
                 '易错点：不操作也是一种选择，所以 `mx` 从 0 开始',
                 '易错点：`d` 的符号随下标奇偶变化，`2` 倍留到最后一行',
                 '同类：53 最大子数组和、3381 长度可被 K 整除的子数组的最大元素和'],
    ),
)
