def _j(S):
    """当前 i 对应的二分结果 j（只在 low 已算出的行之后有意义）"""
    if 'low' not in S or 'i' not in S or S['_line'] < 8:
        return None
    return bisect_left(S['s'], S['low'], 0, S['i'] + 1)


def _info(S):
    if 'i' not in S or 'low' not in S or S['_line'] < 8:
        return '横着算每个起点是 `O(n²)`；==竖着算==：每个房间 `i` 有多少个起点能得 1 分'
    i, low = S['i'], S['low']
    if low <= 0:
        return f"房间 `{i}`：`low = {low} ≤ 0`，所有起点 `0..{i}` 都得分 → 贡献 `{i + 1}`，不用减"
    j = _j(S)
    return f"房间 `{i}`：要求 `s[j] ≥ {low}`，最小的 `j = {j}` → 起点 `{j}..{i}` 得分，贡献 `{i - j + 1}`"


def _dim(S, i, v):
    j = _j(S)
    return j is not None and S['low'] > 0 and i < j


CONFIG = dict(
    num=3771, title='探索地牢的得分', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='贡献法 · 前缀和 + 二分',
    tags=['贪心与思维', '难度分 1981'],
    code='''
class Solution:
    def totalScore(self, hp: int, damage: List[int], requirement: List[int]) -> int:
        n = len(damage)
        s = [0] * (n + 1)
        ans = n * (n + 1) // 2
        for i, (dmg, req) in enumerate(zip(damage, requirement)):
            s[i + 1] = s[i] + dmg
            low = s[i + 1] + req - hp
            if low > 0:
                ans -= bisect_left(s, low, 0, i + 1)
        return ans
''',
    call='Solution().totalScore(10, [3,2,4,1,5], [2,5,3,4,1])',
    expect=9,
    views=[
        dict(type='text', fn=_info, size=25, h=60),
        dict(type='array', var='damage', label='damage', pointers={'i': 'blue'}, cell=84, h=150),
        dict(type='array', var='requirement', label='requirement', cell=84, h=135,
             color=lambda S, i, v: 'blue' if 'i' in S and i == S['i'] else None),
        dict(type='array', var='s', label='s 前缀和（灰 = 该起点得不到分）', cell=84, h=150,
             dim=_dim, pointers={'i + 1': 'blue'}),
    ],
    watch=['hp', ('i', 'i', 'blue'), ('low', lambda S: S.get('low') if S['_line'] >= 8 else None, 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'n = len': '`n = len(damage)`，一共 {n} 个房间',
        's = [0]': '`s[i]` 是 `damage` 前 `i` 个数的和，`s[0] = 0`；`damage` 为正，所以 `s` ==严格递增==，能二分',
        'ans = n': '先假设每个房间都能被所有起点得分：`1+2+…+n = {ans}`，后面把不得分的减掉',
        'for i, (dmg': lambda S, B, r: (f'看房间 `{S.i}`：`damage = {S.dmg}`，`requirement = {S.req}`' if B.get('i') != S.i or S.i == 0 and B.get('dmg') is None else '所有房间都处理完了，循环结束'),
        's[i + 1] = s[i] + dmg': '前缀和 `s[{i+1}] = {s[i]} + {dmg} = {s[i+1]}`',
        'low = ': '从起点 `j` 走到房间 `i` 扣血 `s[i+1] − s[j]`；要 `hp − (s[i+1] − s[j]) ≥ req`，即 `s[j] ≥ s[i+1] + req − hp` = `low` = =={low}==',
        'if low > 0': lambda S, B, r: (f'`low = {S.low} > 0`：起点 0 不够，要二分找第一个 `s[j] ≥ {S.low}`' if S.low > 0 else f'`low = {S.low} ≤ 0`：`s[0] = 0 ≥ low`，所有起点都得分，==不用二分，也不用减==（随机数据大多走这里）'),
        'ans -= bisect_left': lambda S, B, r: f'在 `s[0..{S.i}]` 里二分找第一个 `≥ {S.low}` 的下标 `j = {B.ans - S.ans}`：起点 `0..{B.ans - S.ans - 1}` 得不到分，减去 `{B.ans - S.ans}` → `ans` = =={S.ans}==',
        'return ans': '每个房间的贡献累加完毕：总分 `{ans}`',
    },
    cards=dict(
        one_liner='竖着算：每个房间有多少个起点能在这里得 1 分',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`hp` 点生命，进入第 `i` 个房间扣 `damage[i]`',
                 '扣完后生命 `≥ requirement[i]` 就得 1 分',
                 '`score(j)` = 从房间 `j` 开始一路走到底的得分；求 `score(1)+…+score(n)`',
                 '示例：`hp=11, damage=[3,6,7], requirement=[4,2,5]` → `3`；本视频：`hp=10, damage=[3,2,4,1,5], requirement=[2,5,3,4,1]` → `9`'],
        quote='如果问题没有让我们分别计算每个 score(j)，而是计算 score(j) 的总和，通常可以用==贡献法==解决。……横着暴力算是 O(n²) 的，会超时。能不能==竖着算==呢？',
        quote_src='—— 灵茶山艾府题解',
        idea=['起点 `j` 走到房间 `i` 共扣 `s[i+1] − s[j]`，得分条件移项成 `s[j] ≥ s[i+1] + req − hp`',
              '`damage` 为正 → `s` 递增 → 二分找最小的 `j`，起点 `j..i` 都得分，贡献 `i − j + 1`',
              '优化：先令 `ans = n(n+1)/2`（即所有 `j = 0`），只在 `low > 0` 时减去二分得到的 `j`'],
        result='运行结束，返回 `9`：三次二分分别减去 1、2、3',
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '不能用滑动窗口：`requirement[i]` 没有单调性',
                 '`bisect_left(s, low, 0, i + 1)` 的区间是 `[0, i]`；`s[i+1]` 要先算好再用',
                 '优化前写法：每个 `i` 都二分，`ans += i − j + 1`；优化后只在 `low > 0` 时二分',
                 '若 `damage` 可为负，`s` 不再有序，要用有序集合或值域树状数组'],
    ),
)
