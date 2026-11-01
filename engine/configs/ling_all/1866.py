def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line') != 7:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if (r, c) == (i - 1, j - 1):
        return 'green'
    if (r, c) == (i - 1, j):
        return 'blue'
    return None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line') != 7:
        return '`f[i][j]` = i 根木棍恰好能看到 j 根的排列数（第一类斯特林数）'
    f = S['f']
    return f'`f[{i}][{j}] = f[{i-1}][{j-1}] + {i-1} × f[{i-1}][{j}] = {f[i-1][j-1]} + {i-1} × {f[i-1][j]}` = =={f[i][j]}=='


CONFIG = dict(
    num=1866, title='恰有 K 根木棍可以看到的排列数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='计数 DP · 第一类斯特林数（Go 原文转写）',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2333'],
    code='''
class Solution:
    def rearrangeSticks(self, n: int, k: int) -> int:
        f = [[0] * 6 for _ in range(6)]
        f[0][0] = 1
        for i in range(1, 6):
            for j in range(1, i + 1):
                f[i][j] = (f[i - 1][j - 1] + (i - 1) * f[i - 1][j]) % (10 ** 9 + 7)
        return f[n][k]
''',
    call='Solution().rearrangeSticks(5, 2)',
    expect=50,
    skip=['for j in range'],
    views=[
        dict(type='text', fn=_formula, size=26, h=70),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，绿 = f[i-1][j-1]，蓝 = f[i-1][j]）', h=420, cell=84,
             rows=lambda S: [f'i={k}' for k in range(6)], cols=lambda S: [f'j={k}' for k in range(6)],
             color=_cell),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('n', 'n'), ('k', 'k')],
    captions={
        'f = [[0] * 6': '建表 `f[i][j]`：i 根木棍、恰好看到 j 根。演示只建到 5×5',
        'f[0][0] = 1': '边界：0 根木棍、看到 0 根，有 `1` 种（空排列）',
        'for i in range': '`i = {i}`：考虑 {i} 根木棍',
        'f[i][j] =': lambda S, B, r: (f'`f[{S.i}][{S.j}] = f[{S.i-1}][{S.j-1}] + {S.i-1} × f[{S.i-1}][{S.j}]`'
                                      f' = {S.f[S.i-1][S.j-1]} + {S.i-1} × {S.f[S.i-1][S.j]} = =={S.f[S.i][S.j]}==：'
                                      f'最矮那根放最左 → 多看到一根；放别处 → 被挡住，有 {S.i-1} 个位置'),
        'return f[n][k]': '答案 `f[{n}][{k}]` = =={ret}==：5 根木棍恰看到 2 根有 50 种',
    },
    cards=dict(
        one_liner='能看到的木棍各领一段，每段是一个圆排列：第一类斯特林数',
        complexity='时间 `O(n·k)`（原文预处理 `O(1000^2)`），空间 `O(n·k)`',
        problem=['`1..n` 的木棍排成一排，从左往右看，左边没有更长木棍的才==看得到==',
                 '求恰好看到 `k` 根的排列数，对 `10^9+7` 取余',
                 '示例：`n = 3, k = 2` → `3`；本视频：`n = 5, k = 2` → `50`'],
        quote='因此原问题本质上就是在问长为 n 的排列划分成 k 个非空圆排列的方案数，这就是==第一类斯特林数==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每根能看到的木棍连同它后面被挡住的，划成一个部分，共 `k` 部分',
              '每部分把最大的放开头，其余随便排：`(m-1)!` 种 = 圆排列数',
              '递推：`f[i][j] = f[i-1][j-1] + (i-1) * f[i-1][j]`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '原文用 `init()` 预处理 `1001×1001` 的表；演示时并入函数并缩成 `6×6`，递推式不变',
                 '易错：`(i-1) * f[i-1][j]` 乘完要取模；边界只有 `f[0][0] = 1`',
                 '同类：第一类斯特林数、圆排列计数'],
    ),
)
