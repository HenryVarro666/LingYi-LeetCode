import math as _m

# 灵神原文：MX = 10000，在类外预处理一次，所有测试数据共享。
# 演示时只把常数 MX 改成 12（= 示例 n），其余逐字照搬；
# 为了让引擎追踪到类外的预处理，call 里用 '<solution>' 文件名重新执行一遍这段代码。
CODE = '''
MX = 12
f = [0] + [inf] * MX
for i in range(1, isqrt(MX) + 1):
    for j in range(i * i, MX + 1):
        f[j] = min(f[j], f[j - i * i] + 1)  # 不选 vs 选

class Solution:
    def numSquares(self, n: int) -> int:
        return f[n]
'''.strip('\n')

_MX = 12
F_FINAL = [0] + [_m.inf] * _MX
for _i in range(1, _m.isqrt(_MX) + 1):
    for _j in range(_i * _i, _MX + 1):
        F_FINAL[_j] = min(F_FINAL[_j], F_FINAL[_j - _i * _i] + 1)


def _f(S):
    return S['f'] if 'f' in S else (F_FINAL if 'n' in S else None)


def _f_color(S, k, v):
    if 'n' in S and 'f' not in S:
        return 'green' if k == S['n'] else None
    if 'j' not in S or 'i' not in S:
        return None
    if k == S['j']:
        return 'green'
    if k == S['j'] - S['i'] * S['i']:
        return 'blue'
    return None


def _formula(cv, S, B, box, T):
    s = ''
    if 'j' in S and 'i' in S and 'f' in S and 'f' in B:
        i, j = S['i'], S['j']
        old, new = B['f'][j], S['f'][j - i * i] + 1
        fm = lambda x: '∞' if x == _m.inf else str(x)
        s = (f'`f[{j}] = min(f[{j}], f[{j - i * i}] + 1)` = min({fm(old)}, {fm(S["f"][j - i * i])} + 1) = '
             f'=={fm(min(old, new))}==')
    elif 'f' in S and 'i' not in S:
        s = '`f[0] = 0`：和为 0 一个数都不用选；其余先设 ==∞==（还凑不出来）'
    elif 'i' in S and 'f' in S:
        s = f'考虑第 `{S["i"]}` 个完全平方数 `{S["i"] * S["i"]}`：能选就==反复选=='
    elif 'n' in S:
        s = f'预处理完毕，查表：`f[{S["n"]}]`'
    if s:
        cv.rich(box[0] + 22, box[1] + 8, s, box[2] - box[0] - 44, size=28, accent=(255, 166, 87), max_lines=2,
                line_gap=1.4)


def _legend(cv, S, B, box, T):
    x, y = box[0] + 24, (box[1] + box[3]) / 2
    for c, t in [('green', 'f[j]：更新前是旧值 = 不选 i²'), ('blue', 'f[j-i²]：本轮新值，+1 = 选 i²（还能再选）')]:
        cv.rect((x, y - 11, x + 22, y + 11), fill=T[c], r=5)
        cv.text((x + 32, y), t, 22, T['muted'], anchor='lm')
        x += 32 + cv.tlen(t, 22) + 36


def _cap_f(S, B, ret):
    i, j = S.i, S.j
    sq = i * i
    old, sel = B.f[j], S.f[j - sq] + 1
    fm = lambda x: '∞' if x == _m.inf else str(x)
    if i == 1:
        return f'只有 `1` 可选：`f[{j}] = f[{j - 1}] + 1` = =={fm(S.f[j])}=='
    if sel < old:
        tail = f'选更少 → `f[{j}]` 变成 =={fm(S.f[j])}=='
    else:
        tail = f'不选更好（或一样）→ `f[{j}]` 保持 =={fm(S.f[j])}=='
    return f'不选 `{sq}`：`f[{j}] = {fm(old)}`；选 `{sq}`：`f[{j - sq}] + 1 = {fm(sel)}` → {tail}'


CONFIG = dict(
    num=279, title='完全平方数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='完全背包：记忆化搜索 → 递推 → 空间优化',
    code=CODE,
    setup=f'CODE = {CODE!r}\ndel MX, f, i, j',
    call="exec(compile(CODE, '<solution>', 'exec'), globals())\nSolution().numSquares(12)",
    expect=3,
    views=[
        dict(type='custom', draw=_formula, h=60),
        dict(type='array', var=lambda S: [k * k for k in range(1, _m.isqrt(_MX) + 1)],
             label='物品：完全平方数（体积 i²，价值 1，可重复选）',
             color=lambda S, k, v: 'orange' if 'i' in S and 'f' in S and k + 1 == S['i'] else None,
             index=False, cell=90, h=150),
        dict(type='array', var=_f, label='f[j] = 恰好凑出 j 最少要几个完全平方数', color=_f_color,
             pointers={'j': 'green', 'j - i * i': 'blue'}, pointer_labels={'j - i * i': 'j-i²'}, cell=74, h=250),
        dict(type='custom', draw=_legend, h=50),
    ],
    watch=[('i', 'i', 'orange'), ('i²', 'i * i', 'orange'), ('j', 'j', 'green'), ('j-i²', 'j - i * i', 'blue')],
    skip=['for j in'],
    captions={
        'MX = 12': '原文 `MX = 10000`（题目上限），==在类外预处理一次==，所有测试共享；演示取 `MX = 12`',
        'f = [0]': '初始值翻译自递归边界：`dfs(0, 0) = 0`，`dfs(0, j>0) = ∞`',
        'for i in': lambda S, B, ret: (f'物品 `{S.i}² = {S.i * S.i}`：`j` 从 `{S.i * S.i}` ==从小到大==枚举（完全背包，可重复选）'
                                       if B.get('i') != S.i else '所有完全平方数都考虑完了，`f` 预处理完毕'),
        'f[j] = min': _cap_f,
        'return f[n]': '每个测试只需 `O(1)` 查表：`f[{n}]` = =={ret}==（`12 = 4 + 4 + 4`）',
    },
    cards=dict(
        one_liner='把完全平方数当物品、可以无限选：标准完全背包，求恰好装满的最少件数',
        complexity='预处理 `O(N√N)`，`N = 10⁴`；每次查询 `O(1)`；空间 `O(N)`',
        problem=['给你整数 `n`，返回==和为 n 的完全平方数的最少数量==',
                 '完全平方数：`1, 4, 9, 16, …`',
                 '示例：`n = 12` → `3`（`4 + 4 + 4`）；`n = 13` → `2`（`4 + 9`）'],
        before=[dict(heading='第一步：选或不选，写出记忆化搜索', chapter='② 思路', lines=[
            '`dfs(i, j)`：从前 `i` 个完全平方数中选（可重复），和==恰好==为 `j`，最少选几个',
            '不选 `i²`：`dfs(i-1, j)`；选（需 `j ≥ i²`）：`dfs(i, j - i²) + 1`',
            '注意选了之后还是 `i`，不是 `i-1`：==可以继续选==第 `i` 个',
            '边界 `dfs(0, 0) = 0`，`dfs(0, j>0) = ∞`；入口 `dfs(isqrt(n), n)`',
        ])],
        quote='在计算 n=7 的时候，如果选了 4，会递归到 n=3 的情况。这个例子意味着==多个测试数据之间可以共享记忆化搜索的结果==。',
        quote_src='—— 灵茶山艾府题解',
        idea_heading='第二步：翻译成递推，再压成一维',
        idea=['`f[i][j]` 定义同 `dfs(i, j)`：`f[i][j] = min(f[i-1][j], f[i][j-i²] + 1)`',
              '算 `f[i]` 只用到 `f[i-1]` 和 `f[i]` 本身 → 去掉第一维，反复用一个数组',
              '`f[j] = min(f[j], f[j - i²] + 1)`：`f[j]` 是旧的（不选），`f[j-i²]` 是==本轮新算的==（选）',
              '共享 → 把 `f` 放在==类外==预处理 `MX = 10⁴`，每次查询直接返回 `f[n]`'],
        after=[dict(heading='为什么 j 要从小到大', lines=[
            '`f[j - i²]` 必须是==本轮==（已考虑过 `i²`）的值，才代表「还能继续选 `i²`」',
            '从小到大枚举，`f[j - i²]` 恰好先被更新过 → 完全背包',
            '若从大到小，`f[j - i²]` 还是上一轮的值 → 变成每个数只能选一次（0-1 背包）',
        ])],
        summary=['预处理时间 `O(N√N)`、空间 `O(N)`；单次查询 `O(1)`',
                 '演示把原文 `MX = 10000` 改成 `12`，其余代码未改',
                 '`f[0] = 0`，其余初始化为 `inf`：表示「还凑不出来」',
                 '另一种方法：和当节点、加一个平方数当边，==BFS 求 0 到 n 的最短路=='],
    ),
)
