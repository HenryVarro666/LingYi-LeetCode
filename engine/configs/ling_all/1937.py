def _cap_res(S, B, ret):
    v, j = S.v, S.j
    return (f'选 `points[{S.i}][{j}] = {v}`：左侧 `{v} − {j} + preMax({S.preMax})` = {v - j + S.preMax}，'
            f'右侧 `{v} + {j} + sufMax[{j}]({S.sufMax[j]})` = {v + j + S.sufMax[j]} → `res` = =={S.res}==')


CONFIG = dict(
    num=1937, title='扣分后的最大得分', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='网格 DP · 拆绝对值 + 前后缀最大值（Go 原文转写）',
    tags=['动态规划', '难度分 2106'],
    code='''
class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        ans = 0
        n = len(points[0])
        f = [[0, 0] for _ in range(n)]
        sufMax = [0] * n # 后缀最大值
        for i, row in enumerate(points):
            if i == 0:
                for j, v in enumerate(row):
                    ans = max(ans, v)
                    f[j][0] = v + j
                    f[j][1] = v - j
            else:
                preMax = -2 ** 31
                for j, v in enumerate(row):
                    preMax = max(preMax, f[j][0])
                    res = max(v - j + preMax, v + j + sufMax[j]) # 左侧和右侧的最大值即为选择 points[i][j] 时的计算结果
                    ans = max(ans, res) # 直接更新答案，这样下面就不直接存储 res 了，改为存储 res + j 和 res - j
                    f[j][0] = res + j
                    f[j][1] = res - j
            # 计算完一整行 f 后，对于每个位置 j，计算其右侧的所有 f[k] - k 的最大值
            # 这可以通过倒着遍历 f 求出
            sufMax[n - 1] = f[n - 1][1]
            for j in range(n - 2, -1, -1):
                sufMax[j] = max(sufMax[j + 1], f[j][1])
        return ans
''',
    call='Solution().maxPoints([[1,2,3],[1,5,1],[3,1,1]])',
    expect=9,
    skip=['f = [[0, 0]', 'sufMax = [0]', 'f[j][1] = v - j', 'f[j][1] = res - j', 'preMax = -2', 'for j, v in enumerate', 'for j in range(n - 2', 'n = len', 'ans = 0'],
    max_steps=60,
    views=[
        dict(type='table', var='points', label='points（黄 = 当前格子）', h=190, cell=62,
             cursors=[('i', 'j', 'yellow', '')]),
        dict(type='array', var=lambda S: [p[0] for p in S['f']], label='f[j][0] = res + j（左侧用：取前缀最大）', h=170, cell=70,
             pointers={'j': 'blue'}),
        dict(type='array', var=lambda S: [p[1] for p in S['f']], label='f[j][1] = res − j（右侧用：取后缀最大）', h=140, cell=70),
        dict(type='array', var='sufMax', label='sufMax[j] = j 及右侧 f[k][1] 的最大值', h=140, cell=70),
    ],
    watch=['i', 'j', 'v', 'preMax', 'res', ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 记录所有行、所有选择里的最大得分',
        'n = len': '`n = {n}` 列',
        'for i, row': lambda S, B, r: (f'处理第 `{S.i}` 行 `{S.row}`' if S.i != B.get('i') else '所有行都处理完了'),
        'if i == 0': lambda S, B, r: ('第 0 行：没有上一行，没有扣分，得分就是格子本身' if S.i == 0 else f'第 {S.i} 行：要考虑从上一行转移过来的扣分'),
        'ans = max(ans, v)': '第 0 行直接选 `{v}`，`ans` 取最大 → {ans}',
        'f[j][0] = v + j': '第 0 行也按同样形式存：`f[{j}] = [v + j, v − j]` = [{v + j}, {v - j}]',
        'preMax = max': '`preMax = max({B.preMax}, f[{j}][0] = {f[j][0]})` = {preMax}：==左侧==（含自己）`f[k] + k` 的最大值',
        'res = max(': _cap_res,
        'ans = max(ans, res)': '`ans = max({B.ans}, {res})` = =={ans}==',
        'f[j][0] = res + j': '存 `f[{j}] = [res + j, res − j]` = [{res + j}, {res - j}]：下一行的左侧用 `+j`，右侧用 `−j`',
        'sufMax[n - 1]': '这一行算完。最右边的后缀最大值就是 `f[{n-1}][1]` = {sufMax[n-1]}',
        'sufMax[j] = max': '倒着扫：`sufMax[{j}] = max(sufMax[{j+1}], f[{j}][1])` = =={sufMax[j]}==',
        'return ans': '所有行处理完，最大得分 = =={ret}==',
    },
    cards=dict(
        one_liner='绝对值拆成两半：左边取 f+k 的前缀最大，右边取 f−k 的后缀最大',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['每行选一个格子得分，相邻行的列差 `|c1−c2|` 会扣分',
                 '求最大总得分，`m·n ≤ 10^5`',
                 '示例：`[[1,2,3],[1,5,1],[3,1,1]]` → `9`'],
        quote='拆掉绝对值符号……在计算 f[i][j] 时，我们需要知道位置 j 左侧的 f[i-1][k] + k 的最大值，以及位置 j 右侧的 f[i-1][k] - k 的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i][j] = points[i][j] + max(f[i-1][k] − |k−j|)`，直接枚举 k 是 `O(n²)`',
              '`k ≤ j` 时拆成 `−j + (f + k)`；`k > j` 时拆成 `+j + (f − k)`',
              '一边扫一边维护 `preMax`，`sufMax` 在一行算完后倒着预处理'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(mn)`，空间 `O(n)`',
                 '易错：`f` 存的是 `res + j` 和 `res − j`，不是 `res` 本身，答案要在算出 `res` 时就更新',
                 '第 0 行只初始化，不做转移；`preMax` 初值是 `math.MinInt32`（这里写 `-2 ** 31`）',
                 '同类题：滑动窗口最值 / 拆绝对值的 DP 优化'],
    ),
)
