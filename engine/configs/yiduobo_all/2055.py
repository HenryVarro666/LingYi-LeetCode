def _qline(S):
    if 'x' not in S or 'now' not in S or S.get('_line') is None:
        return '`left[i]` 左侧最近蜡烛 · `right[i]` 右侧最近蜡烛 · `cnt[i]` 前缀蜡烛数（* 盘子 / | 蜡烛）'
    x, y, now = S['x'], S['y'], S['now']
    if now < 2:
        return f'查询 `[{x}, {y}]`：蜡烛只有 `{now}` 根 → 答案 ==0=='
    return f'查询 `[{x}, {y}]`：`left[{y}] − right[{x}] + 1 − now` = `{S["left"][y]} − {S["right"][x]} + 1 − {now}` = =={S["left"][y] - S["right"][x] + 1 - now}=='


def _col(S, i, v):
    if 'x' in S and 'now' in S and 'res' in S and S.get('_line', 0) >= 36:
        x, y = S['x'], S['y']
        if x <= i <= y and S['now'] >= 2:
            l, r = S['right'][x], S['left'][y]
            if l <= i <= r:
                return 'green' if v == '*' else 'yellow'
    return None


CONFIG = dict(
    num=2055, title='蜡烛之间的盘子', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='最近蜡烛 + 蜡烛前缀和',
    tags=['灵神题单·常用数据结构', '难度分 1819'],
    code='''
class Solution(object):
    def platesBetweenCandles(self, s, queries):

        n = len(s)

        left = []
        for index in range(n):
            if s[index] == '|':
                left.append(index)
            elif index == 0:
                left.append(-1)
            else:
                left.append(left[-1])
        
        right = []
        for index in range(n - 1, -1, -1):
            if s[index] == '|':
                right.append(index)
            elif index == n - 1:
                right.append(-1)
            else:
                right.append(right[-1])
        right.reverse()

        if s[0] == '|':
            cnt = [1]
        else:
            cnt = [0]
        
        for char in s[1:]:
            cnt.append(cnt[-1])
            if char == '|':
                cnt[-1] += 1
        
        res = []
        for x, y in queries:
            now = cnt[y]
            if x > 0:
                now -= cnt[x - 1]
            
            if now < 2:
                res.append(0)
            else:
                res.append(left[y] - right[x] + 1 - now)
        
        return res
''',
    call="Solution().platesBetweenCandles('*|**|*|*', [[0, 4], [3, 7], [5, 7]])",
    expect=[2, 1, 0],
    views=[
        dict(type='text', fn=_qline),
        dict(type='string', var='s', pointers={'index': 'blue', 'x': 'pink', 'y': 'purple'}, window=('x', 'y'), color=_col, label='s', h=210),
        dict(type='array', var='left', label='left', h=170),
        dict(type='array', var='right', label='right', h=150),
        dict(type='array', var='cnt', label='cnt', h=150),
        dict(type='array', var='res', label='res', h=150),
    ],
    watch=[('index', 'index', 'blue'), ('x', 'x', 'pink'), ('y', 'y', 'purple'), ('now', 'now', 'orange')],
    skip=['n = len(s)', 'res = []', 'right.reverse'],
    captions={
        "if s[index] == '|'": lambda S, B, r: (f'`s[{S.index}]` 是蜡烛 → 最近蜡烛就是自己' if S.s[S.index] == '|' else f'`s[{S.index}]` 是盘子 → 沿用相邻一侧的最近蜡烛'),
        'left.append(index)': '`left[{index}] = {index}`：自己就是蜡烛',
        'left.append(-1)': '`index = 0` 是盘子且左边没有东西 → `left[0] = -1`（没有蜡烛）',
        'left.append(left[-1])': '盘子：`left[{index}] = left[{index} - 1] = {left[-1]}`，继承左边最近的蜡烛',
        'right.append(index)': '从右往左：`right` 先倒着存，`index` 位是蜡烛 → 记 `{index}`',
        'right.append(-1)': '最右端是盘子 → 右边没有蜡烛，记 `-1`',
        'right.append(right[-1])': '盘子：继承右边最近的蜡烛 `{right[-1]}`（此时列表是倒着存的）',
        'right.reverse()': '倒着存的列表翻回来，现在 `right[i]` 就是下标 i 右侧最近的蜡烛',
        "if s[0] == '|'": '`cnt[i]` 是前缀蜡烛数：先放好 `s[0]` 这一位',
        'cnt.append(cnt[-1])': '先复制前一位的蜡烛数，若这一位是蜡烛再加 1',
        'cnt[-1] += 1': '遇到蜡烛 `cnt[-1] += 1` → `{cnt[-1]}`',
        'for x, y in queries': '取出一个询问 `[{x}, {y}]`',
        'now = cnt[y]': '`now` 先取 `cnt[{y}] = {now}`：前缀到 y 的蜡烛数',
        'now -= cnt[x - 1]': '区间和：减掉前缀 `cnt[{x} - 1]` → 区间 `[{x}, {y}]` 里有 `{now}` 根蜡烛',
        'if now < 2': lambda S, B, r: (f'蜡烛数 `{S.now}` ==不足两根==，没有盘子被夹住 → 答案 0' if S.now < 2 else f'蜡烛数 `{S.now}` ≥ 2：从 `right[{S.x}]` 到 `left[{S.y}]` 之间的盘子都合法'),
        'res.append(0)': '答案 `0`',
        'res.append(left[y] - right[x] + 1 - now)': '`left[y] − right[x] + 1` 是 ==夹在两端蜡烛间的总物件数==，再减蜡烛数 `{now}` 就是盘子数 → `{res[-1]}`',
    },
    cards=dict(
        one_liner='找到区间里最外侧的两根蜡烛，盘子数 = 物件总数 − 蜡烛数',
        complexity='预处理 `O(n)`，每次查询 `O(1)`，空间 `O(n)`',
        problem=['`s` 里 `*` 是盘子，`|` 是蜡烛；每次查询 `[x, y]`，数出区间内左右==都有蜡烛==的盘子',
                 '示例：`s = "**|**|***|"`，`[[2,5],[5,9]]` → `[2,3]`',
                 '本视频：`s = "*|**|*|*"`，查询 `[[0,4],[3,7],[5,7]]` → `[2,1,0]`'],
        quote='设x右侧第一根蜡烛的位置为right[x]……设y左侧第一根蜡烛的位置为left[y]……在right[x]到left[y]之间的盘子都可以加入到答案中。',
        quote_src='—— yiduobo 题解原文',
        idea=['蜡烛少于 2 根：答案必为 0',
              '否则把两端「没被夹住」的盘子削掉：从 `right[x]` 数到 `left[y]`',
              '这一段共 `left[y] − right[x] + 1` 个物件，减去蜡烛数（前缀和相减）就是盘子数'],
        summary=['时间 `O(n + q)`，空间 `O(n)`',
                 '`left` 和 `right` 用 `-1` 表示「没有蜡烛」，但蜡烛数 `< 2` 时不会用到',
                 '`right` 是倒着 `append` 的，别忘了最后 `reverse()`',
                 '原文是 Python 2 风格写法，这份代码本身可直接在 Python 3 运行，未做修改'],
    ),
)
