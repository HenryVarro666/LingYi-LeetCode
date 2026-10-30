def _color(S, i, v):
    if 'x' not in S:
        return None
    if v == S['x']:
        return 'green'
    return 'blue' if v < S['x'] else None


CONFIG = dict(
    num=2681, title='英雄的力量', difficulty='Hard', category='贪心算法',
    author='灵茶山艾府', technique='排序 + 贡献法（枚举最大值）',
    tags=['灵神题单·贪心与思维', '难度分 2060'],
    code='''
class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 1_000_000_007
        nums.sort()
        ans = s = 0
        for x in nums:  # x 作为最大值
            ans = (ans + x * x * (x + s)) % MOD
            s = (s * 2 + x) % MOD  # 递推计算下一个 s
        return ans
''',
    call='Solution().sumOfPower([2, 1, 4, 3])',
    expect=316,
    views=[
        dict(type='text', size=30, fn=lambda S, B: '排序后从小到大枚举最大值 `x`，`s` = 左边每个数当最小值的 ==贡献之和==' if 'x' not in S else
             (f"x = {S['x']} 作最大值：`x² × (x + s)` = {S['x']**2} × ({S['x']} + {B['s']}) ，累计 ans = =={S['ans']}==" if S.get('_line') in (7, 8, 9) else f"x = {S['x']} 作最大值")),
        dict(type='array', var='nums', color=_color, h=300,
             label='nums（排序后）：绿 = 当前最大值 x，蓝 = 它左边的数'),
    ],
    watch=[('x', 'x', 'green'), ('s', 's', 'blue'), ('ans', 'ans', 'orange')],
    captions={
        'nums.sort()': '先排序：只关心最大/最小，元素顺序不影响答案 → `{nums}`',
        'ans = s = 0': '`ans` 是答案，`s` 表示「左边所有数当最小值」的贡献和 `a·2^2 + b·2^1 + c·2^0`，初始为 0',
        'for x in nums': lambda S, B, r: ('`nums` 枚举完了，循环结束' if 'x' in B and B.x == S.x else f'枚举最大值 `x = {S.x}`：它左边的数都不比它大，可以当最小值'),
        'ans = (ans': '`x` 作最大值的所有子序列力量 = `x³`（只选 x）+ `x²·s` = `x²·(x+s)` = `{x}²×({x}+{B.s})` = {x*x*(x+B.s)}；`ans` {B.ans} → =={ans}==',
        's = (s * 2': '换下一个最大值时，原来每个最小值的方案数翻倍，再多一个 `x` 单独当最小值：`s = 2×{B.s} + {x}` = =={s}==',
        'return ans': '所有最大值的贡献加完，返回 `{ans}`',
    },
    cards=dict(
        one_liner='排序后只枚举最大值，最小值的贡献用 s 递推',
        complexity='时间 `O(n log n)`（排序），空间 `O(1)`',
        problem=['选出一组英雄，力量 = `max² × min`，求所有非空组力量之和（对 `10^9+7` 取模）',
                 '示例：`[2,1,4]` → `141`',
                 '本视频演示：`[2,1,4,3]` → `316`'],
        quote='这意味着，我们不需要枚举最小值，只需要枚举最大值，就可以把 s 递推计算出来。',
        quote_src='—— 灵茶山艾府题解',
        idea=['元素顺序不影响答案，先排序；设 `d` 为最大值，左边 `a,b,c` 当最小值分别有 `2²,2¹,2⁰` 种选法',
              '`d` 作最大值的总贡献 = `d³ + d²·s` = `d²·(d+s)`',
              '换成下一个最大值 `e`：`s` 变成 `2·s + d`，所以边遍历边更新'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`',
                 '易错点：每一步都要取模，`s` 也要取模',
                 '先用旧的 `s` 算贡献，再更新 `s`，顺序不能反',
                 '思考题：改成「子数组」要用单调栈（见 §5.5 贡献法专题训练）'],
    ),
)
