A0 = [1, 3, 4, 1, 5]


def _cell(S, r, c, v):
    l, rt = S.get('left'), S.get('right')
    if l is None or rt is None or rt >= len(S['arr']):
        return None
    if r == l and c == rt:
        return 'yellow'
    cp = S.get('cut_pos')
    if S.get('_line') in (CUT_LINE, ) and cp is not None:
        if (r, c) in ((l, cp), (cp + 1, rt)):
            return 'blue'
    if S['arr'][l] == S['arr'][rt] and rt - l >= 2 and (r, c) == (l + 1, rt - 1):
        return 'green'
    return None


CUT_LINE = 26


def _formula(S):
    l, r = S.get('left'), S.get('right')
    if l is None or r is None or r >= len(S['arr']):
        return '`f[l][r]` = 删光 `arr[l..r]` 的最少操作次数；按区间长度从小到大算'
    a = S['arr']
    if l == r:
        return f'`f[{l}][{r}] = 1`：单个元素本身是回文'
    if r == l + 1:
        return f'`arr[{l}] = {a[l]}`，`arr[{r}] = {a[r]}` → ' + ('一次删完 ==1==' if a[l] == a[r] else '只能分两次 ==2==')
    if a[l] == a[r]:
        return f'两端相等：`f[{l}][{r}] = f[{l + 1}][{r - 1}]`（两端附着在里面某次删除上）'
    return f'两端不等：枚举切点 `f[{l}][{r}] = min(f[{l}][cut] + f[cut+1][{r}])`'


CONFIG = dict(
    num=1246, title='删除回文子数组', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间 DP（按区间长度枚举）',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def minimumMoves(self, arr):

        n = len(arr)

        f = [[n] * n for _ in range(n)]

        for length in range(1, n + 1):
            for left in range(n):
                right = left + length - 1
                if right >= n:
                    break
                
                if left == right:
                    f[left][right] = 1
                elif left == right - 1:
                    if arr[left] == arr[right]:
                        f[left][right] = 1
                    else:
                        f[left][right] = 2
                else:
                    if arr[left] == arr[right]:
                        f[left][right] = f[left + 1][right - 1]
                    
                    for cut_pos in range(left, right):
                        f[left][right] = min(f[left][right], f[left][cut_pos] + f[cut_pos + 1][right])
        
        return f[0][n - 1]
''',
    call=f'Solution().minimumMoves({A0!r})',
    expect=3,
    skip=['for length in range', 'for left in range', 'right = left + length', 'for cut_pos in range', 'if right >= n', 'break', 'if left == right:', 'elif left == right - 1:'],
    max_steps=90,
    views=[
        dict(type='array', var='arr', label='arr', h=210, cell=80, window=('left', 'right'),
             pointers={'left': 'blue', 'right': 'pink'}),
        dict(type='text', fn=_formula, size=24, h=80),
        dict(type='table', var='f', label='f[left][right]（黄 = 正在算，绿/蓝 = 依赖的格子）', h=360, cell=66,
             rows=lambda S: [f'{k}:{c}' for k, c in enumerate(A0)], cols=lambda S: [f'{k}:{c}' for k, c in enumerate(A0)],
             color=_cell),
    ],
    watch=[('length', 'length', 'yellow'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('cut_pos', 'cut_pos', 'cyan')],
    captions={
        'n = len(arr)': '`n = {n}`',
        'f = [[n]': '`f[l][r]` 初值设成 `n`（足够大，相当于“无穷”），后面取 `min`',
        'f[left][right] = 1': lambda S, B, r: (f'`left == right`：单个元素 `{S.arr[S.left]}` 自己就是回文 → `f[{S.left}][{S.right}] = 1`'
                                               if S.left == S.right else
                                               f'`arr[{S.left}] = arr[{S.right}] = {S.arr[S.left]}`，两个相同元素是回文 → 1 次'),
        'f[left][right] = 2': '`{arr[left]} ≠ {arr[right]}`：两个不同元素，只能各删一次 → ==2==',
        'if arr[left] == arr[right]:': lambda S, B, r: (
            f'`arr[{S.left}] = {S.arr[S.left]}`，`arr[{S.right}] = {S.arr[S.right]}` → '
            + ('相等' if S.arr[S.left] == S.arr[S.right] else '不相等')),
        'f[left][right] = f[left + 1][right - 1]': '两端相等 → ==附着==在里面任意一次删除的两侧，不增加次数：`f[{left}][{right}] = f[{left+1}][{right-1}] = {f[left][right]}`',
        'f[left][right] = min(': '切点 `{cut_pos}`：`f[{left}][{cut_pos}] + f[{cut_pos+1}][{right}] = {f[left][cut_pos]} + {f[cut_pos+1][right]}`，`f[{left}][{right}]` 取小 → =={f[left][right]}==',
        'return f[0][n - 1]': '整个数组 `arr[0..{n-1}]` 的答案 `f[0][{n-1}]` = =={ret}==',
    },
    cards=dict(
        one_liner='两端相等就附着在里面，不等就枚举切点拆成两段',
        complexity='时间 `O(n^3)`，空间 `O(n^2)`',
        problem=['每次操作可以删除一个==回文子数组==，删完后剩下的部分拼起来',
                 '求删光整个数组 `arr` 所需的==最少操作次数==',
                 '示例：`[1,3,4,1,5]` → `3`（删 `3`、删 `4`，`[1,1]` 再删一次，最后删 `5`）'],
        quote='令f[i][j]表示arr[i]到arr[j]这一段删除所需的最少操作次数',
        quote_src='—— yiduobo 题解原文',
        idea=['区间长度 1：`f = 1`；长度 2：相同 1 次，不同 2 次',
              '两端相等：`f[i][j] = f[i+1][j-1]`，两端附着在里面某次删除两侧',
              '两端不等：枚举切点，`min(f[i][cut] + f[cut+1][j])`'],
        summary=['时间 `O(n^3)`：`O(n^2)` 个区间 × 枚举切点 `O(n)`',
                 '易错：长度 ≥ 3 且两端相等时，先令 `f = f[i+1][j-1]`，再继续枚举切点取 `min`',
                 '长度 1、2 是边界，要单独处理',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行'],
    ),
)
