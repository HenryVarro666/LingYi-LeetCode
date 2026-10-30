BOOKS = [7, 0, 3, 4, 5]


def _info(S):
    if 'st' not in S or 'v' not in S:
        return '单调栈里存 `(下标, dp 值)`，哨兵 `(-1, 0)`'
    i, v = S['i'], S['v']
    return f"`books[{i}] − {i} = {v - i}`；栈顶 `left = {S['st'][-1][0]}`"


CONFIG = dict(
    num=2355, title='你能拿走的最大图书数量', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='单调栈优化 DP · 下标作差',
    tags=['灵神题单·单调栈', '灵神题单·动态规划'],
    code='''
class Solution:
    def maximumBooks(self, books: List[int]) -> int:
        ans, st = 0, [(-1, 0)]  # 单调栈里面存 (下标, dp 值)，加个哨兵
        for i, v in enumerate(books):
            while len(st) > 1 and books[st[-1][0]] - st[-1][0] >= v - i:
                st.pop()
            size = min(i - st[-1][0], v)
            s = (v * 2 - size + 1) * size // 2 + st[-1][1]
            ans = max(ans, s)
            st.append((i, s))
        return ans
''',
    call=f'Solution().maximumBooks({BOOKS})',
    expect=12,
    views=[
        dict(type='array', var='books', pointers={'i': 'blue', 'st[-1][0]': 'pink'}, pointer_labels={'i': 'i', 'st[-1][0]': 'left'},
             h=210, label='books（蓝 = 当前 i，粉 = 栈顶 left）',
             color=lambda S, i, v: 'blue' if S.get('i') == i else None),
        dict(type='stack', var='st', fmt=lambda p: f'({p[0]},{p[1]})', label='st（下标, dp 值），栈顶在右', h=170),
        dict(type='text', fn=_info, size=26, h=100),
    ],
    watch=[('i', 'i', 'blue'), ('size', 'size', 'cyan'), ('s', 's', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans, st = 0': '`st` 存 `(下标, dp 值)`，`(-1, 0)` 是哨兵：左边没有更小元素时 `left = -1`',
        'for i, v in enumerate': '枚举以 `books[{i}] = {v}` 结尾的方案，`books[i]` ==必须全拿==',
        'while len(st) > 1': lambda S, B, r: (
            f"比较 `books[{S.st[-1][0]}] − {S.st[-1][0]} = {S.books[S.st[-1][0]] - S.st[-1][0]}` ≥ `{S.v} − {S.i} = {S.v - S.i}` → ==成立==：栈顶不比当前小，不是 `left`，弹出"
            if len(S.st) > 1 and S.books[S.st[-1][0]] - S.st[-1][0] >= S.v - S.i else
            "栈顶（或哨兵）就是左边第一个更小的位置 `left`，停止弹栈"),
        'st.pop()': '弹出栈顶，栈里剩 `{st}`',
        'size = min': '等差数列项数 `size = min(i − left, v) = min({i} − {st[-1][0]}, {v})` = =={size}==，v 太小时递减到 1 就停',
        's = (v * 2': '尾项 `{v}`，共 `{size}` 项：`({v}×2 − {size} + 1)×{size}/2` = {(v*2-size+1)*size//2}，再加 `left` 的 dp 值 `{st[-1][1]}` → `f[i] = ` =={s}==',
        'ans = max': '`ans = max({B.ans}, {s}) = {ans}`',
        'st.append': '`({i}, {s})` 入栈：栈里保持 `books[i] − i` 严格递增，后面的 i 可以直接复用它的 dp 值',
        'return ans': '所有 `f[i]` 的最大值 =={ret}==',
    },
    cards=dict(
        one_liner='每个数减去下标，严格递增变成非严格递增，再套单调栈',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`books[i]` 是第 `i` 层书架的书数，选一段连续书架，每层拿的书要==严格递增==',
                 '每层最多拿 `books[i]` 本，求最多能拿多少本',
                 '本视频：`[7,0,3,4,5]` → `12`（取 `3+4+5`）'],
        quote='通过将每个元素减去其下标这一技巧，可以将原问题的严格递增转换成非严格递增，设转换后的数组为 b，我们可以在 b 上跑单调栈。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i]` = 以 `books[i]` 结尾的最大拿书数，最后一个必然全拿，前面依次少拿 1',
              '递减一直到遇到更小的元素 `left`，或者递减到 1，是一个尾项为 `v` 的等差数列',
              '`f[i] = 等差数列和 + f[left]`，`left` 用单调栈找，dp 值直接存进栈里'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：项数是 `min(i − left, v)`，递减到 1 就不能再往下',
                 '易错：弹栈条件 `≥`（相等也弹），因为转换后允许非严格',
                 '哨兵 `(-1, 0)` 避免栈空判断'],
    ),
)
