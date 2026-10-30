G = [[0, 0, 1], [1, 1, 0], [1, 0, 0]]

CONFIG = dict(
    num=1536, title='排布二进制网格的最少交换次数', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='转成尾零数组 · 找最近的满足者',
    tags=['贪心与思维', '难度分 1881'],
    code='''
class Solution:
    def minSwaps(self, grid: List[List[int]]) -> int:
        # 预处理每一行的尾零个数
        n = len(grid)
        tail_zeros = [n] * n
        for i in range(n):
            for j in range(n - 1, -1, -1):
                if grid[i][j]:
                    tail_zeros[i] = n - 1 - j
                    break

        ans = 0
        for i in range(n - 1):
            need_zeros = n - 1 - i
            for j in range(i, n):
                if tail_zeros[j] >= need_zeros:
                    ans += j - i
                    # 从 j 换到 i，原来 [i, j-1] 中的数据全体右移一位
                    tail_zeros[i + 1: j + 1] = tail_zeros[i: j]
                    break
            else:  # 没找到符合要求的 tail_zeros[j]
                return -1
        return ans
''',
    call=f'Solution().minSwaps({G})',
    expect=3,
    views=[
        dict(type='grid', var='grid', h=260,
             cursors=[(lambda S: None if 'ans' in S else S.get('i'), lambda S: S.get('j'), 'yellow')],
             color=lambda S, i, j, v: 'blue' if v == 1 else None),
        dict(type='array', var='tail_zeros', label='tail_zeros（每行尾零个数）', h=200,
             pointers={'need_zeros and i': 'blue', 'need_zeros and j': 'pink'},
             pointer_labels={'need_zeros and i': 'i', 'need_zeros and j': 'j'}),
        dict(type='text', fn=lambda S: (f"第 `{S['i']}` 个位置至少要 ==`{S['need_zeros']}`== 个尾零" if 'need_zeros' in S else ''), size=30),
    ],
    watch=['i', 'j', 'need_zeros', ('ans', 'ans', 'green')],
    captions={
        'tail_zeros = [n] * n': '先默认每行全是 0，尾零数为 `n = {n}`',
        'tail_zeros[i] = n - 1 - j': '第 `{i}` 行最后的 1 在列 `{j}` → 尾零 `n-1-j = {tail_zeros[i]}`',
        'need_zeros = n - 1 - i': '第 `{i}` 行必须有至少 ==`{need_zeros}`== 个尾零，才能让它右边全是 0',
        'if tail_zeros[j] >= need_zeros': lambda S, B, r: (
            f'`tail_zeros[{S.j}] = {S.tail_zeros[S.j]} >= {S.need_zeros}` → 满足；==最近的就选它==，越靠后的位置要求越宽松'
            if S.tail_zeros[S.j] >= S.need_zeros else
            f'`tail_zeros[{S.j}] = {S.tail_zeros[S.j]} < {S.need_zeros}` → 不够，继续往后找'),
        'ans += j - i': '把第 `{j}` 行换到第 `{i}` 行要相邻交换 `j - i = {j - i}` 次 → `ans = {ans}`',
        'tail_zeros[i + 1: j + 1]': '`[i, j-1]` 整体右移一位（相当于冒泡）；位置 `{i}` 已满足，之后不再看它：{tail_zeros}',
        'for j in range(n - 1': '第 `{i}` 行：从最右一列往左，找最后一个 1',
        'if grid[i][j]': lambda S, B, r: (f'`grid[{S.i}][{S.j}] = 1` → 这就是最后一个 1' if S.grid[S.i][S.j] else f'`grid[{S.i}][{S.j}] = 0` → 还是尾零，继续往左'),
        'for j in range(i, n)': '从位置 `{i}` 往后，找第一个尾零数够的行（最近的）',
        'return -1': '一直找到末尾都没有满足的行 → 不可能，返回 `-1`',
        'return ans': '最少交换 `{ans}` 次',
    },
    cards=dict(
        one_liner='只看每行的尾零数，从上到下逐位找最近的满足者',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`n x n` 的 0/1 网格，每次可交换相邻两行',
                 '目标：主对角线以上全是 0，求最少交换次数，不行返回 `-1`',
                 '示例：`[[0,0,1],[1,1,0],[1,0,0]]` → `3`'],
        quote='问题等价于：交换 tailZeros 中的相邻元素，使得 tailZeros[i] ≥ n-1-i，至少要交换多少次？',
        quote_src='—— 灵茶山艾府题解',
        idea=['第 `i` 行右边要全是 0，等价于尾零数 `>= n-1-i`；从上往下，位置 `i` 找第一个满足的行换上来',
              '选最近的：越靠后要求越宽松，能去 0 号位的也能去后面所有位置，谁近用谁'],
        summary=['时间 `O(n^2)`（预处理和贪心都是双重循环），空间 `O(n)`',
                 '外层只到 `n-2`：最后一行要求尾零 `>= 0`，一定满足',
                 '`for ... else` 的 else：找不到满足者才返回 `-1`',
                 '全 0 的行尾零数记为 `n`，这样什么要求都能满足'],
    ),
)
