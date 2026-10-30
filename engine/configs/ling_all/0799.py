def _fn(S):
    if 'f' not in S:
        return '`f[j]` = 当前这一层第 `j` 个杯子里的香槟量（可以大于 1，表示要溢出）'
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line') not in (6, 7, 8, 9, 10, 11, 12):
        return f"每层从右往左处理：第 `i` 层处理完后，`f[0..{(i or 0) + 1}]` 变成下一层"
    return f"第 `{i}` 层第 `{j}` 杯：`x = f[{j}] − 1`（超出容量 1 的部分），溢出的一半流向 `f[{j}]`、`f[{j + 1}]`"


CONFIG = dict(
    num=799, title='香槟塔', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='逐层模拟 · 原地滚动数组',
    tags=[],
    code='''
class Solution:
    def champagneTower(self, poured: int, queryRow: int, queryGlass: int) -> float:
        f = [0.0] * (queryRow + 1)
        f[0] = float(poured)
        for i in range(queryRow):
            for j in range(i, -1, -1):
                x = f[j] - 1
                if x > 0:
                    f[j + 1] += x / 2
                    f[j] = x / 2
                else:
                    f[j] = 0.0
        return min(f[queryGlass], 1.0)  # 如果溢出，容量是 1
''',
    call='Solution().champagneTower(8, 3, 1)',
    expect=0.875,
    skip=['for j in range'],
    views=[
        dict(type='text', fn=_fn, size=24, h=60),
        dict(type='array', var='f', label='f（当前这一层每个杯子的香槟量）', cell=120, h=240,
             pointers={'j': 'blue', 'j + 1 if _line in (9, 10) else None': 'pink'},
             color=lambda S, k, v: 'green' if v > 1 else None),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('x', 'x', 'yellow')],
    captions={
        'f = [0.0]': '`f` 只需要 `queryRow + 1` 个格子：一层一层往下，==同一个数组复用==',
        'f[0] = float(poured)': '先把 `poured = {poured}` 杯全倒进顶层 `f[0]`',
        'for i in range': lambda S, B, r: ('每一层都流完了，`f[queryGlass]` 就是答案所在层的香槟量' if 'i' in B and B.i == S.i
                                           else f'开始处理第 `{S.i}` 层，把它溢出的香槟流向第 `{S.i + 1}` 层；`j` ==从右往左==，免得 `f[j+1]` 被当成同层的量重复处理'),
        'x = f[j] - 1': '杯子容量是 1，溢出量 `x = {f[j]} − 1 = {x}`',
        'if x > 0': lambda S, B, r: (f'`x = {S.x} > 0`：这杯满了且溢出，要往下流' if S.x > 0 else f'`x = {S.x} ≤ 0`：没装满，不会溢出'),
        'f[j + 1] += x / 2': '溢出的一半流到右下 `f[{j + 1}]` → {f[j + 1]}',
        'f[j] = x / 2': '另一半流到正下方 `f[{j}]` = {f[j]}（原位置变成下一层的这个杯子）',
        'f[j] = 0.0': '没溢出，下一层这个位置分不到（暂时为 0），清零 `f[{j}]`',
        'return min': '第 `{queryRow}` 层第 `{queryGlass}` 杯里有 `{f[queryGlass]}`，最多装 1 → ==min(..., 1.0)== = {ret}',
    },
    cards=dict(
        one_liner='像 BFS 一层层往下流，溢出的一半各给左右两杯',
        complexity='时间 `O(queryRow^2)`，空间 `O(queryRow)`',
        problem=['杯子摆成金字塔：第 `i` 层有 `i+1` 个，每个杯子容量 1',
                 '从顶层倒 `poured` 杯，满了溢出的香槟等分流向下一层左右两杯',
                 '求第 `queryRow` 行第 `queryGlass` 个杯子的香槟量（不超过 1）',
                 '本视频：`poured=8, queryRow=3, queryGlass=1` → `0.875`'],
        quote='从 $(i,j)$ 溢出的香槟流到 $(i+1,j)$ 和 $(i+1,j+1)$。设溢出的香槟量为 $x$，那么下一层的 $j$ 和 $j+1$ 的香槟量都增加 $x/2$。',
        quote_src='—— 灵茶山艾府题解',
        idea=['类似层序遍历：第 `i` 层溢出的量决定第 `i+1` 层',
              '优化前用两个数组 `cur`/`nxt`；优化后像 0-1 背包，==倒序遍历 `j`== 在同一个数组上改',
              '溢出量 `x = f[j] - 1`，`x > 0` 才往下流，各 `x/2`'],
        summary=['时间 `O(queryRow^2)`，空间 `O(queryRow)`',
                 '易错：返回前要 `min(..., 1.0)`，杯子最多装 1',
                 '易错：`j` 必须倒序，否则 `f[j+1]` 会被当成同层的量重复处理',
                 '优化前版本用 `cur`、`nxt` 两个数组，本视频演示原地版',
                 '相似题：118 杨辉三角'],
    ),
)
