BOOKS = [7, 0, 3, 4, 5]


def _info(S):
    if 'f' in S and 'pre' in S and 'index' in S and S.get('_line', 0) >= 16:
        i = S['index']
        j = S['pre'][i]
        if j == -1:
            return f"`pre[{i}] = -1`：左边没有断点，等差数列从 `max(1, books[i] − i)` 开始"
        return f"断点 `j = pre[{i}] = {j}`：`f[{i}] = f[{j}] + 等差数列`"
    if 'pre' in S:
        return f"`pre = {S['pre']}`（每个位置左边最近的更小数的下标）"
    return ''


CONFIG = dict(
    num=2355, title='你能拿走的最大图书数量', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='单调栈预处理断点 + 等差数列 DP',
    tags=['灵神题单·单调栈', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def maximumBooks(self, books):

        n = len(books)
        pre = [-1] * n
        stack = []
        for index in range(n - 1, -1, -1):
            while stack and books[stack[-1]] - stack[-1] >= books[index] - index:
                pre[stack[-1]] = index
                stack.pop()
            
            stack.append(index)
        

        f = [books[0]]
        for index in range(1, n):
            if pre[index] == -1:
                start = max(1, books[index] - index)
                f.append((start + books[index]) * (books[index] - start + 1) // 2)
            else:
                start = max(1, books[index] - (index - pre[index]) + 1)
                f.append(f[pre[index]] + (start + books[index]) * (books[index] - start + 1) // 2)

        return max(f)
''',
    call=f'Solution().maximumBooks({BOOKS})',
    expect=12,
    views=[
        dict(type='array', var='books', pointers={'index': 'blue'}, h=240, label='books',
             color=lambda S, i, v: 'blue' if S.get('index') == i else None),
        dict(type='array', var='pre', label='pre（左边最近的断点 j，-1 = 没有）', h=170,
             color=lambda S, i, v: 'yellow' if S.get('index') == i and S.get('_line', 0) >= 16 else None),
        dict(type='stack', var='stack', fmt=lambda i: f'{i}:{BOOKS[i]-i}', label='stack（下标:books[i]−i，栈顶在右）', h=130),
        dict(type='array', var='f', label='f（以 books[i] 结尾的最大拿书数）', h=170),
        dict(type='text', fn=_info, size=24, h=70),
    ],
    watch=[('index', 'index', 'blue'), ('stack', 'stack', 'cyan'), ('start', 'start', 'yellow')],
    captions={
        'pre = [-1] * n': '`pre[i]` 记录 `i` 左边最近的“转换值不大于它”的下标，-1 表示没有',
        'for index in range(n - 1, -1, -1)': lambda S, B, r: (
            f"==从右往左==扫，当前 `index = {S.index}`，转换值 `books[i] − i = {S.books[S.index] - S.index}`"
            if S.index >= 0 else '预处理完成'),
        'while stack and books[stack[-1]]': lambda S, B, r: (
            "栈空，没有可弹出的" if not S.stack else
            f"栈顶 `{S.stack[-1]}` 的转换值 `{S.books[S.stack[-1]] - S.stack[-1]}` ≥ 当前 `{S.books[S.index] - S.index}` → ==当前是它左边第一个转换值不大于它的=="
            if S.books[S.stack[-1]] - S.stack[-1] >= S.books[S.index] - S.index else
            f"栈顶转换值 `{S.books[S.stack[-1]] - S.stack[-1]}` < 当前 `{S.books[S.index] - S.index}` → 停止"),
        'pre[stack[-1]] = index': '`pre[{stack[-1]}] = {index}`：下标 {stack[-1]} 的断点找到了',
        'stack.pop()': '弹出下标，`stack = {stack}`',
        'stack.append(index)': '`{index}` 入栈等待它右边的数',
        'f = [books[0]]': '`f[0] = books[0]`，只有一层，只能全拿',
        'for index in range(1, n)': '按顺序算 `f[{index}]`，`books[{index}] = {books[index]}` 必须全拿',
        'if pre[index] == -1': lambda S, B, r: (
            f"`pre[{S.index}] = -1`：左边没有断点 → 情况 1：只受 `books[i] < i` 限制" if S.pre[S.index] == -1
            else f"`pre[{S.index}] = {S.pre[S.index]}`：左边有断点 → 情况 2：要接上 `f[{S.pre[S.index]}]`"),
        'start = max(1, books[index] - index)': '起点 `max(1, {books[index]} − {index})` = =={start}==：太小时递减到 1 就停',
        'start = max(1, books[index] - (index - pre': '起点 `max(1, {books[index]} − ({index} − {pre[index]}) + 1)` = =={start}==：只覆盖断点右边 `{index - pre[index]}` 层',
        'f.append((start + books[index])': '等差数列 `{start}..{books[index]}`，和 `({start}+{books[index]})×{books[index]-start+1}/2` → `f[{index}] = ` =={f[-1]}==',
        'f.append(f[pre[index]]': '`f[{pre[index]}] = {f[pre[index]]}` + 等差数列 `{start}..{books[index]}` → `f[{index}] = ` =={f[-1]}==',
        'return max(f)': '答案是所有 `f[i]` 里最大的 =={ret}==',
    },
    cards=dict(
        one_liner='枚举最后一层全拿，断点用单调栈找，其余是等差数列',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['选一段连续书架，每层拿的书数==严格递增==，且第 `i` 层最多 `books[i]` 本',
                 '求最多能拿多少本',
                 '本视频：`[7,0,3,4,5]` → `12`（`3+4+5`）'],
        quote='books[j] - j < books[i] - i，那么如果在最开始将原始数组中的每个数减去其所在的下标，问题就转化成了左侧第一个更小的数的下标问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['最后一项必然全拿；理想情况是 `books[i]−i` 到 `books[i]` 的等差数列',
              '断开有两种：`books[i] < i`（递减到 1 为止）、中间某项 `j` 不够大（用 `f[j]` 接上）',
              '`books[j] < books[i] − (i−j)` 移项就是 `books[j]−j < books[i]−i`，单调栈预处理出 `pre`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '两种断裂可叠加：先看 `pre`，再用 `max(1, …)` 限制起点',
                 '原文为 Python 2 写法，两处等差数列求和的 `/ 2` 已改为 `// 2`（整数除法）',
                 '对比灵神：灵神把 dp 值直接存进单调栈，一趟完成；这里分成预处理 + DP 两趟'],
    ),
)
