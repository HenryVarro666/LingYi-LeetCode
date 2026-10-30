def _txt(S):
    if 'ori' in S:
        s = f"保持不变 `ori = {S['ori']}`，要修改 `modify = {S['modify']}`"
        if 'ma_o' in S and 'mi_o' in S:
            s += f"    ori：最大 `ma_o = {S['ma_o']}`，最小 `mi_o = {S['mi_o']}`"
        if 'ma_m' in S and 'mi_m' in S and S['_line'] >= 17:
            s += f"    modify：最大 `ma_m = {S['ma_m']}`，最小 `mi_m = {S['mi_m']}`"
        return s
    if 'index' in S:
        return '偶数下标放偶数 / 奇数下标放奇数 → 归入 ==f==；否则归入 ==g==（修改其中一组的奇偶性即可）'
    return ''


CONFIG = dict(
    num=3854, title='使数组奇偶交替的最少操作', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='按下标奇偶分两组 · 改短的一组',
    tags=['贪心算法', '思维题', '难度分 2095'],
    code='''
class Solution(object):
    def makeParityAlternating(self, nums):
        
        def calc(ori, modify):
            ma_o, mi_o = ori[0], ori[0]
            for v in ori[1:]:
                ma_o = max(ma_o, v)
                mi_o = min(mi_o, v)
            
            if not modify:
                return ma_o - mi_o
            
            ma_m, mi_m = modify[0], modify[0]
            for v in modify[1:]:
                ma_m = max(ma_m, v)
                mi_m = min(mi_m, v)
            
            if ma_o > mi_o:
                mi = min(mi_o, mi_m + 1)
                ma = max(ma_o, ma_m - 1)
                return ma - mi
            
            if ma_m == mi_m:
                if ma_m < ma_o:
                    return ma_o - ma_m - 1
                elif ma_m == ma_o:
                    return 1
                else:
                    return ma_m - ma_o - 1
            
            if ma_m <= ma_o:
                return ma_o - mi_m - 1
            elif ma_o <= mi_m:
                return ma_m - ma_o - 1
            else:
                return ma_m - mi_m - 2

        f = []
        g = []
        for index, v in enumerate(nums):
            if index % 2 == v % 2:
                f.append(v)
            else:
                g.append(v)
        
        

        if len(f) > len(g):
            return [len(g), calc(f, g)]
        elif len(f) < len(g):
            return [len(f), calc(g, f)]
        else:
            return [len(f), min(calc(f, g), calc(g, f))]
''',
    call='Solution().makeParityAlternating([4,10,4,12,4])',
    expect=[2, 7],
    views=[
        dict(type='text', fn=_txt, size=24),
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=200, label='nums',
             color=lambda S, i, v: ('green' if i % 2 == v % 2 else 'orange') if 'index' in S and i <= S['index'] else None,
             dim=lambda S, i, v: 'index' in S and i > S['index']),
        dict(type='array', var='f', h=170, label='f（下标奇偶 = 数值奇偶，不用改）', color=lambda S, i, v: 'green'),
        dict(type='array', var='g', h=170, label='g（下标奇偶 ≠ 数值奇偶）', color=lambda S, i, v: 'orange'),
    ],
    watch=['ma_o', 'mi_o', 'ma_m', 'mi_m', ('f', 'len(f)', 'green'), ('g', 'len(g)', 'orange')],
    captions={
        'f = []': '`f`：下标奇偶和数值奇偶一致的数；`g`：不一致的数',
        'if index % 2 == v % 2': lambda S, B, r: (f"`index = {S.index}`（{'偶' if S.index % 2 == 0 else '奇'}），`v = {S.v}`（{'偶' if S.v % 2 == 0 else '奇'}）→ " + ('奇偶一致，放进 ==f==' if S.index % 2 == S.v % 2 else '奇偶不一致，放进 ==g==')),
        'f.append(v)': '`f = {f}`',
        'g.append(v)': '`g = {g}`',
        'if len(f) > len(g)': lambda S, B, r: (f"`len(f) = {len(S.f)}`，`len(g) = {len(S.g)}`：" + ('f 更长 → ==改较短的 g==，操作数 = `len(g)`' if len(S.f) > len(S.g) else '先看 f 是否更短')),
        'return [len(g), calc': '修改 g（短的一组）：操作 `{len(g)}` 次，保持 `ori = f`',
        'elif len(f) < len(g)': '`len(f) = {len(f)} < len(g) = {len(g)}`？→ {"成立，改较短的 f" if len(f) < len(g) else "不成立，两组一样长"}',
        'return [len(f), calc(g, f)]': '修改 f（短的一组）：操作 `{len(f)}` 次',
        'return [len(f), min': '两组一样长：两种方向都要试，取极差较小的',
        'ma_o, mi_o = ori[0]': '先扫 `ori`（不动的一组）：从 `ori[0] = {ori[0]}` 起记最大最小',
        'ma_o = max': '`ma_o = max({B.ma_o}, {v}) = {ma_o}`',
        'mi_o = min': '`mi_o = min({B.mi_o}, {v}) = {mi_o}`',
        'for v in ori[1:]': '依次看 `ori` 里其余的数',
        'for v in modify[1:]': '依次看 `modify` 里其余的数',
        'if not modify': lambda S, B, r: ('`modify` 为空 → 不用改，极差就是 `ma_o - mi_o`' if not S.modify else f'`modify = {S.modify}` 不为空，继续算'),
        'ma_m, mi_m = modify[0]': '再扫 `modify`（要改的一组）：记 `ma_m`、`mi_m`',
        'ma_m = max': '`ma_m = max({B.ma_m}, {v}) = {ma_m}`',
        'mi_m = min': '`mi_m = min({B.mi_m}, {v}) = {mi_m}`',
        'if ma_o > mi_o': lambda S, B, r: (f"`ma_o = {S.ma_o}` > `mi_o = {S.mi_o}`？" + ('成立：x ≤ mi_o 的加 1，x ≥ ma_o 的减 1，其余任意' if S.ma_o > S.mi_o else '不成立：ori 全相等，要细分讨论')),
        'mi = min(mi_o': '最小值 `min({mi_o}, {mi_m} + 1) = {mi}`：modify 的最小值 +1',
        'ma = max(ma_o': '最大值 `max({ma_o}, {ma_m} - 1) = {ma}`：modify 的最大值 −1',
        'return ma - mi': '极差 `{ma} - {mi} = {ma - mi}`',
        'if ma_m == mi_m': lambda S, B, r: (f"`ma_m = {S.ma_m}`，`mi_m = {S.mi_m}`：" + ('modify 全相等 → 向 ma_o 靠拢' if S.ma_m == S.mi_m else '不全相等，继续看与 ma_o 的位置关系')),
        'if ma_m <= ma_o': lambda S, B, r: (f"`ma_m = {S.ma_m}` ≤ `ma_o = {S.ma_o}`？" + ('成立：modify 全在 ma_o 下方，最小的 +1、其余 −1' if S.ma_m <= S.ma_o else '不成立')),
        'return ma_o - mi_m - 1': '极差 `ma_o - (mi_m + 1) = {ma_o - mi_m - 1}`',
        'elif ma_o <= mi_m': lambda S, B, r: (f"`ma_o = {S.ma_o}` ≤ `mi_m = {S.mi_m}`？" + ('成立：modify 全在 ma_o 上方，最大的 −1、其余 +1' if S.ma_o <= S.mi_m else '不成立：ma_o 夹在中间')),
        'return ma_m - ma_o - 1': '极差 `(ma_m - 1) - ma_o = {ma_m - ma_o - 1}`',
        'return ma_m - mi_m - 2': 'ma_o 夹在中间：最小 +1、最大 −1，极差 `{ma_m - mi_m - 2}`',
        'return ma_o - ma_m - 1': '极差 `ma_o - (ma_m + 1) = {ma_o - ma_m - 1}`',
        'return 1': '`ma_m == ma_o`：一个加一个减 → 极差 1',
        'return ma_o - mi_o': '极差 `{ma_o - mi_o}`',
    },
    cards=dict(
        one_liner='先按下标奇偶分两组，改短的那组，再分类讨论极差',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums` 每次可把一个数 `+1` 或 `-1`，要让相邻两数奇偶性不同',
                 '返回 `[最少操作数, 此时 max-min 的最小值]`',
                 '本视频：`[4,10,4,12,4]` → `[2,7]`'],
        quote='为了使得修改的次数最短，在这里就应该先比较f和g的长度，选择修改长度较短的那一个。若二者长度相同，则两种情况都需要考虑。',
        quote_src='—— yiduobo 题解原文',
        idea=['最终只有两种形态，用 `f`、`g` 分别装“已经对”和“不对”的数',
              '改短的一组，次数最少；`ori` 不动，`modify` 里每个数 ±1',
              '极差取决于 `ori` 的最值和 `modify` 的最值，按 `ma_o > mi_o`、`ma_o == mi_o` 细分'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '两组一样长要 `min(calc(f, g), calc(g, f))`',
                 '`ma_o == mi_o` 时 modify 内元素差至少 2，所以最小的 +1、最大的 −1 不会碰撞',
                 '对比灵神：灵神枚举两种模式、只靠全局最值判断；yiduobo 分组后逐类推导'],
    ),
)
