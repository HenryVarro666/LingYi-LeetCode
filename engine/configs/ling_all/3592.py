def _chk(S, B, ret):
    i, w, f = S.i, S.ways, S.f
    if w == f[i]:
        return f'金额 {i} 的目标方案数 `{w}` 等于 `f[{i}] = {f[i]}`：和为 {i} 的方案全由更小面值凑出 → =={i} 不是面值=='
    if w - 1 == f[i]:
        return f'金额 {i} 的目标方案数 `{w}` = `f[{i}] + 1`：比已知面值凑出的多 1 种 → =={i} 单独成一枚硬币=='
    return f'金额 {i} 的目标方案数 `{w}` 与 `f[{i}] = {f[i]}` 差的不是 0 或 1：没有面值集合能生成它'


CONFIG = dict(
    num=3592, title='硬币面值还原', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='反向构造 · 完全背包',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1701'],
    code='''
class Solution:
    def findCoins(self, numWays: List[int]) -> List[int]:
        n = len(numWays)
        f = [1] + [0] * n
        ans = []
        for i, ways in enumerate(numWays, 1):
            if ways == f[i]:
                continue
            if ways - 1 != f[i]:
                return []
            ans.append(i)
            # 现在得到了一个大小为 i 的物品，用 i 计算完全背包（空间优化写法）
            for j in range(i, n + 1):
                f[j] += f[j - i]
        return ans
''',
    call='Solution().findCoins([1,2,2,3,4])',
    expect=[1, 2, 5]
    ,skip=['for j in range'],
    max_steps=70,
    views=[
        dict(type='text', size=24, h=50, fn=lambda S: '`numWays` 下标从 0 起，对应金额 `i` = 下标 + 1；`f[j]` = 目前已知面值凑出金额 j 的方案数'),
        dict(type='array', var='numWays', label='numWays', h=190, cell=80,
                          color=lambda S, k, v: 'blue' if S.get('i') is not None and k == S['i'] - 1 else None),
        dict(type='array', var='f', label='f（f[0..n]）', h=190, cell=80, pointers={'j': 'pink'},
             color=lambda S, k, v: 'blue' if S.get('i') is not None and k == S['i'] and S.get('_line', 0) < 11 else None),
        dict(type='array', var='ans', label='ans（已还原的面值）', h=130, cell=80),
    ],
    watch=[('i', 'i', 'blue'), ('ways', 'ways', 'yellow'), ('f[i]', 'f[i]', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'f = [1]': '`f[0] = 1`：和为 0 有 1 种方案（什么都不选）；其余先记 0',
        'for i, ways': '看金额 `i = {i}`，目标方案数 `{ways}`（numWays 第 {i} 项）',
        'if ways == f[i]': _chk,
        'continue': '`{i}` 不是面值 → 跳过，看下一个金额',
        'if ways - 1': lambda S, B, r: ('恰好多 1 种 → 继续' if S.ways - 1 == S.f[S.i] else '不是多 1 种 → 无解，返回空列表'),
        'ans.append': '把 `{i}` 加入答案：`ans = {ans}`',
        'f[j] += f[j - i]': '加入面值 `{i}` 后更新：`f[{j}] += f[{j - i}]` → =={f[j]}==（正序遍历 = 可重复选）',
        'return ans': '遍历完都对得上，面值集合 `{ans}`',
    },
    cards=dict(
        one_liner='最小的非零方案数，必然来自一个单独的面值',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`numWays[i]` 是用若干种固定面值（每种无限枚）凑出金额 `i` 的方案数',
                 '面值丢失了，还原所有可能的面值，从小到大返回；不存在返回 `[]`',
                 '示例：`[1,2,2,3,4]` → `[1,2,5]`'],
        quote='如果 numWays[i] = f[i]+1，意味着 i 可以单独一个数，贡献 1 个和为 i 的方案，所以 a 中一定有 i。',
        quote_src='—— 灵茶山艾府题解',
        idea=['这是 518 零钱兑换 II 的反向构造：已知 DP 结果，还原物品',
              '边扫金额边维护「已知面值」的完全背包数组 `f`',
              '`ways == f[i]` 不用选；`ways == f[i]+1` 必有面值 `i`；否则无解'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '`f[0] = 1` 不能漏，它是转移的起点',
                 '完全背包：内层从小到大遍历 `j`',
                 '数据范围 n 变大会溢出时，`f[j]` 超过 max(numWays) 就可直接返回空列表'],
    ),
)
