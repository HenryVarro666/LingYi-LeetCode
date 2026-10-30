def _txt(S):
    if 'p' not in S or S.get('_line') not in (9, 10, 11, 12):
        return '`g[i]` = 前 `i` 种咒语能造成的最大伤害；`q+1` 指向第一个不冲突的位置'
    p, f, q, g = S['p'], S['f'], S['q'], S['g']
    if S.get('_line') in (9, 10):
        return f'伤害 `{p}`：`power[q+1] = {S["power"][q + 1][0]}`，要 `≥ {p}-2 = {p - 2}` 才不冲突'
    return f'选：`g[q+1] + {p}×{f}` = `{g[q + 1]} + {p * f}` = {g[q + 1] + p * f}；不选：`g[-2]` = {g[-2]}'


CONFIG = dict(
    num=3186, title='施咒的最大总伤害', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='（伤害, 次数）排序 + 单调指针 DP',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1841'],
    code='''
class Solution(object):
    def maximumTotalDamage(self, power):

        power = sorted(Counter(power).items())
        g = [0]
        q = -1
        for p, f in power:
            g.append(g[-1])
            while power[q + 1][0] < p - 2:
                q += 1
            g[-1] = max(g[-1], g[q + 1] + p * f)

        return g[-1]
''',
    call='Solution().maximumTotalDamage([1,1,3,4,7,6,6])',
    expect=15,
    views=[
        dict(type='array', var=lambda S: [f'{a}×{b}' for a, b in S['power']] if isinstance(S['power'][0], tuple) else None,
             label='power：（伤害值 × 次数），已排序（蓝 = 当前，粉 = q+1）', h=190, cell=100,
             pointers={'q + 1': 'pink'}),
        dict(type='array', var='g', label='g：前 i 种咒语的最大伤害（g[0] = 0）', h=200, cell=90),
        dict(type='text', fn=_txt, size=24, h=70),
    ],
    watch=['p', 'f', ('q', 'q', 'pink')],
    captions={
        'power = sorted': '去重并排序：`power = {power}`，每项是（伤害值，次数），同值的咒语要么全用要么不用',
        'g = [0]': '`g[0] = 0`：一种咒语也不选，伤害为 0',
        'q = -1': '`q = -1`：`q+1` 指向最左边',
        'for p, f in power': lambda S, B, r: ('所有伤害值都考虑过了' if B.get('p') == S.p else f'轮到伤害 `{S.p}`（共 `{S.f}` 个）'),
        'g.append(g[-1])': '先假设==不选==这种咒语：`g` 末尾追加 `{g[-2]}`',
        'while power[q + 1]': lambda S, B, r: (f'`power[q+1]` 的伤害 `{S.power[S.q + 1][0]}` < `{S.p}-2`：它不冲突，`q` 还能右移' if S.power[S.q + 1][0] < S.p - 2
                                              else f'`power[q+1]` 的伤害 `{S.power[S.q + 1][0]}` ≥ `{S.p}-2`：和当前冲突，`q` 停下'),
        'q += 1': '`q` 右移到 {q}：`g` 单调不减，所以取最大的不冲突位置最优',
        'g[-1] = max': '`max(不选 {g[-2]}，选 g[{q+1}] + {p}×{f} = {g[q+1] + p*f})` = =={g[-1]}==',
        'return g[-1]': '最大总伤害 = =={ret}==',
    },
    cards=dict(
        one_liner='同值咒语要么全用要么不用，排序后线性 DP',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['用伤害 `power[i]` 的咒语后，不能再用伤害 `±1`、`±2` 的咒语',
                 '同伤害值可以重复使用，求总伤害最大值',
                 '示例：`[1,1,3,4,7,6,6]` → `15`'],
        quote='对于某种伤害值的咒语，要么都用，要么都不用。于是可以使用哈希表为 power 去重，将其重新整理为二维数组 power[i] = [p[i], f[i]]。',
        quote_src='—— yiduobo 题解',
        idea=['`g[i]` = 前 `i` 种咒语的最大伤害，`g[0] = 0`',
              '不选：`g[i] = g[i-1]`；选：`g[q+1] + p×f`，`q` 是最大的满足 `p[q] < p-2` 的下标',
              '`g` 单调不减，所以只需最大的 `q`；`q` 随 `i` 单调右移，不用二分'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '`g` 比 `power` 多一位，所以下标是 `q + 1`',
                 '不用 `q` 回头：`while` 条件里 `power[q+1]` 不会越界，因为当前项自己一定不满足 `< p-2`',
                 '同类题：740 删除并获得点数'],
    ),
)
