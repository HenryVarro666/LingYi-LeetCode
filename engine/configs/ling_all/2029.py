CONFIG = dict(
    num=2029, title='石子游戏 IX', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='模 3 计数 · 分类讨论',
    tags=['博弈论', '贪心与思维', '难度分 2277'],
    code='''
class Solution:
    def stoneGameIX(self, stones: List[int]) -> bool:
        cnt = [0] * 3
        for x in stones:
            cnt[x % 3] += 1

        if cnt[0] % 2 == 0:
            return cnt[1] > 0 and cnt[2] > 0
        return abs(cnt[1] - cnt[2]) > 2
''',
    call='Solution().stoneGameIX([5,1,2,4,3])',
    expect=False,
    views=[
        dict(type='array', var='stones', label='stones（颜色 = 模 3 的余数：绿 0 / 蓝 1 / 粉 2）', h=220, cell=100,
             color=lambda S, i, v: {0: 'green', 1: 'blue', 2: 'pink'}[v % 3]),
        dict(type='array', var='cnt', label='cnt[r] = 模 3 余 r 的石子个数', h=220, cell=120,
             color=lambda S, i, v: {0: 'green', 1: 'blue', 2: 'pink'}[i]),
        dict(type='text', h=70, size=30,
             fn=lambda S: (f"0 的个数 =={S['cnt'][0]}== ({'偶数' if S['cnt'][0] % 2 == 0 else '奇数'})　　|cnt[1]−cnt[2]| = =={abs(S['cnt'][1] - S['cnt'][2])}==" if S.get('_line', 0) > 6 else '')),
    ],
    watch=[('x', 'x', 'yellow'), ('cnt[0]', 'cnt[0]', 'green'), ('cnt[1]', 'cnt[1]', 'blue'), ('cnt[2]', 'cnt[2]', 'pink')],
    captions={
        'cnt = [0]': '只关心模 3 的余数：`cnt[0]`、`cnt[1]`、`cnt[2]` 分别统计余 0、1、2 的石子',
        'cnt[x % 3] += 1': '`{x} % 3 = {x % 3}` → `cnt[{x % 3}]` 加 1，现在 `cnt = {cnt}`',
        'if cnt[0] % 2 == 0': lambda S, B, r: (f'`cnt[0] = {S.cnt[0]}` 是偶数：Bob 取 0 时 Alice 跟着取 0，0 互相抵消 → 只看 1 和 2 是否都有'
                                              if S.cnt[0] % 2 == 0 else
                                              f'`cnt[0] = {S.cnt[0]}` 是奇数：0 会让先后手互换 → 要看 1 和 2 的个数差'),
        'return cnt[1] > 0': 'Alice 先取 1 或 2 起手，序列固定为 `1,1,2,1,2…` 或 `2,2,1,2,1…`，1 和 2 都有则 Alice 必胜 → =={ret}==',
        'return abs': lambda S, B, r: (f'0 为奇数个：`|cnt[1] − cnt[2]| = {abs(S.cnt[1] - S.cnt[2])}`，'
                                       + ('至少差 3，另一种石子先耗尽、Bob 被迫凑成 3 的倍数 → ==Alice 必胜==' if r else '差不到 3：石子被取完或 Alice 先无路可走 → ==Bob 必胜==')),
    },
    cards=dict(
        one_liner='石子只看模 3；0 偶数个看 1、2 是否都有，奇数个看个数差是否 ≥ 3',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['Alice、Bob 轮流从 `stones` 取走一颗石子，Alice 先手',
                 '取走后已取石子的和被 3 整除，该玩家输；石子全取完仍没人输则 Bob 赢',
                 '示例：`[5,1,2,4,3]` → `false`'],
        quote='如果 stones 有偶数个 0（包括 0 个 0），那么当且仅当 stones 包含 1 和 2 的情况下 Alice 必胜。如果有奇数个 0，那么当且仅当 |cnt1 − cnt2| ≥ 3 成立时 Alice 必胜。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['只关心已取之和模 3：石子 `x` 与 `x % 3` 等价',
              '不含 0 时，取石序列固定为 `1,1,2,1,2…` 或 `2,2,1,2,1…`',
              '0 不改变余数，相当于「交换先后手」→ 按 0 的奇偶分类，得到简短结论'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：Alice 第一步不能取 0，否则立刻输',
                 '奇数个 0 时，条件是 `abs(cnt[1]-cnt[2]) > 2`，不是「1 和 2 都有」',
                 '方法一：计算最大回合数，枚举 Alice 先取 1 或 2，`rounds` 为奇数且还有剩余石子则 Alice 赢'],
    ),
)
