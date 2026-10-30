def _books(S):
    return [f'{t}×{h}' for t, h in S['books']]


def _fi(S):
    return [S['f'][k] if S['f'][k] != float('inf') else '∞' for k in range(len(S['f']))]


def _txt(S):
    if 'max_h' not in S or 'i' not in S:
        return ''
    if 'j' in S and S.get('_line', 0) >= 9:
        used = S['shelf_width'] - S['left_w']
        return f"最后一层放 `books[{S['j']}..{S['i']}]`：厚度和 `{used}` / {S['shelf_width']}，层高 `max_h` = =={S['max_h']}=="
    return f"枚举最后一层的第一本书 `j`（从 `i = {S['i']}` 往前）"


CONFIG = dict(
    num=1105, title='填充书架', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP · 枚举最后一层',
    tags=[],
    code='''
class Solution:
    def minHeightShelves(self, books: List[List[int]], shelf_width: int) -> int:
        n = len(books)
        f = [0] + [inf] * n  # 在前面插入一个状态表示 dfs(-1)=0
        for i in range(n):
            max_h, left_w = 0, shelf_width
            for j in range(i, -1, -1):
                left_w -= books[j][0]
                if left_w < 0: break  # 空间不足，无法放书
                max_h = max(max_h, books[j][1])  # 从 j 到 i 的最大高度
                f[i + 1] = min(f[i + 1], f[j] + max_h)
        return f[n]  # 翻译自 dfs(n-1)
''',
    call='Solution().minHeightShelves([[1,1],[2,3],[2,3],[1,2]], 4)',
    expect=6,
    views=[
        dict(type='array', var=_books, label='books（厚度×高度），蓝框 = 当前最后一层', window=('j', 'i'), pointers={'j': 'blue', 'i': 'pink'}, h=210),
        dict(type='text', fn=_txt, size=28, h=80),
        dict(type='array', var=_fi, label='f[k]：前 k 本书的最小总高度（f[i+1] 正在被更新）', pointers={'j': 'blue'}, h=210),
    ],
    watch=[('i', 'i', 'pink'), ('j', 'j', 'blue'), ('left_w', 'left_w', 'cyan'), ('max_h', 'max_h', 'orange')],
    captions={
        'f = [0]': '`f[k]` = 前 `k` 本书的最小高度；`f[0] = 0` 对应“没有书”',
        'for i in range': '计算 `f[i+1]`：把 `books[0..i]` 摆好的最小高度',
        'max_h, left_w =': '最后一层还没放书：最大高度 `0`，剩余宽度 `{shelf_width}`',
        'left_w -= ': '把 `books[{j}]` 放进最后一层（厚度 {books[j][0]}）→ 剩余宽度 `{left_w}`',
        'if left_w < 0': lambda S, B, r: (f'剩余宽度 `{S.left_w} < 0`：放不下，==停止往前枚举==' if S.left_w < 0 else f'剩余宽度 `{S.left_w} ≥ 0`：还放得下，继续'),
        'max_h = max': '层高取这层最高的书：`max_h = {max_h}`',
        'f[i + 1] = min': '`f[{i+1}] = min(旧值, f[{j}] + {max_h})`：前 {j} 本书的最优 `{f[j]}` + 最后一层高 `{max_h}` → =={f[i+1]}==',
        'return f[n]': '`f[{n}]` 就是全部书的最小高度：=={ret}==',
    },
    cards=dict(
        one_liner='枚举最后一层放哪几本书，剩下的是更短前缀的子问题',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['按顺序把书放进宽 `shelfWidth` 的书架，每层厚度和不超过它，层高 = 该层最高的书',
                 '求书架总高度的最小值',
                 '本视频：`[[1,1],[2,3],[2,3],[1,2]]`，宽度 `4`'],
        quote='考虑书架的最底层，可以放 books 的最后 1 到 4 本书（题目要求按顺序摆放，且书的厚度之和不能超过 shelfWidth）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最底层放 `books[j..i]`，剩下的是 `books` 前 `j` 本的子问题 → `f[j]`',
              '从 `i` 往前倒着枚举 `j`，边放边累计厚度和最大高度',
              '灵神从暴力递归 → 记忆化 → 1:1 翻译成递推，本视频演示最后的递推'],
        summary=['时间 `O(n^2)`：状态 `O(n)` 个，每个枚举 `O(n)` 次',
                 '`f` 前面插一个 `f[0] = 0` 表示递归边界 `dfs(-1)`',
                 '厚度超限要 `break`：再往前只会更超',
                 '灵神还给出了暴力递归和记忆化写法，递推是它们的 1:1 翻译'],
    ),
)
