def _paths(g):
    m, n = len(g), len(g[0])
    d = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if g[i][j] == '#':
                continue
            d[i][j] = 1 if i == j == 0 else (d[i - 1][j] if i else 0) + (d[i][j - 1] if j else 0)
    return d[-1][-1]


def _top(S):
    if 'k' not in S:
        return ''
    k, w = S['k'], S.get('w')
    b = bin(k)[2:]
    s = f"`k = {k}` 的二进制是 `{b}`，共 `{len(b)}` 位"
    if 'a' in S and isinstance(S['a'], list) and S['a'] and isinstance(S['a'][0], str):
        s += f"；网格从左上走到右下共 =={_paths(S['a'])}== 条路径"
    return s


CONFIG = dict(
    num=3990, title='创建一个恰好有 K 条路径的网格图 II', difficulty='Hard', category='贪心算法',
    author='灵茶山艾府', technique='按二进制位构造',
    tags=['贪心与思维', '构造题'],
    code='''
class Solution:
    def createGrid(self, k: int) -> list[str]:
        w = k.bit_length()
        m = w * 2
        n = w + 3
        a = [['#'] * (n - 1) + ['.'] for _ in range(m)]
        for j in range(w):
            i = j * 2
            a[i][j] = a[i][j + 1] = a[i + 1][j] = a[i + 1][j + 1] = '.'

        for i in range(w):
            if k >> i & 1:
                for j in range(i + 2, n - 1):
                    a[i * 2][j] = '.'

        return [''.join(row) for row in a]
''',
    call='Solution().createGrid(5)',
    expect=['......', '..###.', '#..##.', '#..##.', '##....', '##..#.'],
    skip=['for j in range(i + 2', 'for j in range(w)'],
    views=[
        dict(type='text', fn=_top),
        dict(type='grid', var='a', h=470, cell=64, label='网格 a（. 可走，# 墙）',
             color=lambda S, i, j, v: 'green' if v == '.' else None),
    ],
    watch=[('k', 'k', 'yellow'), ('w', 'w', 'cyan'), ('m', 'm', 'blue'), ('n', 'n', 'pink')],
    captions={
        'w = k.bit_length()': '`k = {k}` 二进制有 `w = {w}` 位：造 `w` 个 2×2 的块，每个块让路径数翻倍',
        'm = w * 2': '每个块占 2 行：行数 `m = w × 2 = {m}`',
        'n = w + 3': '列数 `n = w + 3 = {n}`（最后一列是汇总列）',
        'a = [': '先全是墙 `#`，只有最右一列是 `.`：这条竖路把各行的路径汇总到右下角',
        'for j in range(w)': '依次放第 `{j}` 个 2×2 块',
        'a[i][j] = a[i][j + 1]': '在 `({i}, {j})` 放一个 2×2 的空地块：==沿对角线连成一串，每经过一块路径数 ×2==，到第 `{j}` 块左上角的路径数为 `2^{j}`',
        'for i in range(w)': '处理 `k` 的第 `{i}` 位',
        'if k >> i & 1': lambda S, B, r: (f'`k` 的第 `{S.i}` 位是 `{S.k >> S.i & 1}`：' + (f'是 1 → 要让这 `{2 ** S.i}` 条路径通到终点' if S.k >> S.i & 1 else '是 0 → 这一块不连出去')),
        'a[i * 2][j] = ': '打通第 `{i*2}` 行第 `{j}` 列：从第 `{i}` 个块的上面一行向右开通道直达最后一列，把 `2^{i}` 条路径加进答案',
        'return': '`k = {k}` = 二进制各位为 1 的 `2^i` 之和；网格按行拼成字符串返回',
    },
    cards=dict(
        one_liner='k 写成二进制：对角线上的 2×2 块造出 2 的幂，为 1 的位接到终点',
        complexity='时间 `O(log² k)`，空间 `O(1)`（不计返回值）',
        problem=['构造不超过 25×25 的 `.`/`#` 网格，只能向右或向下走，不能走 `#`',
                 '要求从左上走到右下角恰好有 `k` 条路径（`1 ≤ k ≤ 1000`）',
                 '本视频：`k = 5`，得到 6×6 的网格'],
        quote='本题是 3988. 创建一个恰好有 K 条路径的网格图 I 的加强版，做法见 我的题解 中的「更一般的构造方法」，包含图片解释。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`w` 个 2×2 空地块沿对角线排开，走到第 `i` 个块的路径数是 `2^i`',
              '`k` 的第 `i` 位为 1，就从第 `i` 块往右开一条横向通道，直达最后一列',
              '总路径数 = 所有为 1 的位对应的 `2^i` 之和 = `k`',
              '尺寸 `2w × (w+3)`：`k ≤ 1000` 时 `w ≤ 10`，远小于 25'],
        summary=['时间 `O(log² k)`（网格大小），空间 `O(1)`（不计返回值）',
                 '易错：通道从 `j = i + 2` 开始，避免和 2×2 块重叠、重复计数',
                 '最右一列全是 `.`，负责把各通道的路径汇总到右下角',
                 '题解只给了一种写法；更详细的图解在灵神对第 3988 题的题解里'],
    ),
)
