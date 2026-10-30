A0 = [4, 1, 2, 6, 3]
B0 = [1, 5, 3, 2, 7]


def _i(S):
    return S['energyDrinkA'].index(S['a']) if 'a' in S and 'b' in S else (0 if 'f' in S else -1)


def _txt(S):
    if 'f' not in S:
        return '`f` = 最后一小时喝 A 的最大能量；`g` = 最后一小时喝 B 的最大能量'
    return f"`f` = =={S['f']}==（最后喝 A）　　`g` = =={S['g']}==（最后喝 B）"


CONFIG = dict(
    num=3259, title='超级饮料的最大强化能量', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='两个变量滚动的 DP',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1484'],
    code='''
class Solution(object):
    def maxEnergyBoost(self, energyDrinkA, energyDrinkB):

        f, g = energyDrinkA[0], energyDrinkB[0]

        for a, b in zip(energyDrinkA[1:], energyDrinkB[1:]):
            f, g = max(f + a, g), max(f, g + b)
        
        return max(f, g)
''',
    call=f'Solution().maxEnergyBoost({A0}, {B0})',
    expect=18,
    views=[
        dict(type='array', var='energyDrinkA', label='A 饮料（蓝 = 当前小时）', h=170, cell=80,
             color=lambda S, i, v: 'blue' if i == _i(S) else None, dim=lambda S, i, v: 0 <= _i(S) and i < _i(S)),
        dict(type='array', var='energyDrinkB', label='B 饮料（粉 = 当前小时）', h=170, cell=80,
             color=lambda S, i, v: 'pink' if i == _i(S) else None, dim=lambda S, i, v: 0 <= _i(S) and i < _i(S)),
        dict(type='text', fn=_txt, size=28, h=70),
        dict(type='text', fn=lambda S: (f"本小时 A 给 `{S['a']}`、B 给 `{S['b']}`：继续同一种 = 加上它，换饮料 = 拿对方上一小时的值（本小时 0）" if 'b' in S else '边界：第 0 小时只能选一种，`f = A[0]`、`g = B[0]`'), size=22, h=90),
    ],
    watch=[('f', 'f', 'blue'), ('g', 'g', 'pink'), 'a', 'b'],
    captions={
        'f, g = energyDrinkA[0]': '边界：`f[0] = A[0] = {f}`，`g[0] = B[0] = {g}`',
        'for a, b in zip': lambda S, B, r: (f"看下一小时：A 给 `{S['a']}`，B 给 `{S['b']}`" if 'a' in S and S.get('a') != B.get('a') else '所有小时都处理完了'),
        'f, g = max': '`f = max({B.f} + {a}, {B.g})` = =={f}==（继续喝 A，或从 B 换过来、本小时 0）；`g = max({B.f}, {B.g} + {b})` = =={g}==',
        'return max': '最后一小时喝 A 或 B 取大：`max({f}, {g})` = =={ret}==',
    },
    cards=dict(
        one_liner='f 记最后喝 A，g 记最后喝 B，换饮料就吃掉一小时',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['两个长度为 `n` 的数组是 A、B 饮料每小时的强化能量',
                 '每小时喝一种；从一种切换到另一种，之后一小时拿不到能量',
                 '示例：`A=[4,1,1], B=[1,1,3]` → `7`'],
        quote='令f[index]表示前index个小时，最后这个小时喝了饮料A时可以获得的最大能量值，而g[index]则表示前index个小时，最后这个小时喝了饮料B时可以获得的最大能量值。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i] = max(f[i-1] + A[i], g[i-1])`：上一小时也喝 A 就能加上；上一小时喝 B，则本小时空等，只保留 `g[i-1]`',
              '`g[i]` 与 `f[i]` 完全对称；边界 `f[0]=A[0]`，`g[0]=B[0]`',
              '每轮只依赖上一轮，所以两个变量一起更新'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`f, g = ...` 要用元组同时赋值，否则 `g` 会用到新的 `f`',
                 '换饮料时不是 `+0` 到上一小时，而是直接取对方的 `g[i-1]`/`f[i-1]`',
                 '同类：198 打家劫舍'],
    ),
)
