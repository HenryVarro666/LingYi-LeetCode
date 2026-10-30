WORD = 'HAPPY'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '键盘 6 列（格内：字母 + f[字母] = 另一根手指停在该字母时的最小总距离）', 22, T['muted'], bold=True)
    f = S.get('f')
    if f is None or not isinstance(f, list) or len(f) != 26:
        f = None
    cell = min(118, (x1 - x0 - 60) / 6, (y1 - y0 - 150) / 5)
    sx = x0 + ((x1 - x0) - cell * 6) / 2
    sy = y0 + 46
    x, y, a = S.get('x'), S.get('y'), S.get('another_finger')
    inloop = 'another_finger' in S and S.get('_line', 0) == 14
    for c in range(26):
        r_, c_ = divmod(c, 6)
        X, Y = sx + c_ * cell, sy + r_ * cell
        fill = T['panel2']
        if x is not None and c == x:
            fill = T['cyan']
        if y is not None and c == y:
            fill = T['orange']
        if inloop and c == a and c not in (x, y):
            fill = T['pink']
        dark = fill != T['panel2']
        cv.rect((X + 4, Y + 4, X + cell - 4, Y + cell - 4), fill=fill, r=10, outline=T['border'])
        cv.text((X + cell / 2, Y + cell * 0.36), chr(65 + c), 34, T['bg'] if dark else T['text'], anchor='mm', bold=True)
        if f is not None:
            cv.text((X + cell / 2, Y + cell * 0.74), f[c], 26, T['bg'] if dark else T['green'], anchor='mm', bold=True, mono=True)
    yy = sy + 5 * cell + 18
    items = [('x = 刚打的', T['cyan']), ('y = 要打的', T['orange']), ('another_finger = 另一根', T['pink'])]
    X = x0 + 24
    for s, c in items:
        cv.rect((X, yy + 6, X + 22, yy + 28), fill=c, r=4)
        cv.text((X + 32, yy + 4), s, 22, T['text'])
        X += 32 + cv.tlen(s, 22) + 40


def _fml(S):
    if 'another_finger' not in S or S.get('_line', 0) != 14:
        return '`f[a]`：一根手指在当前字母，另一根在 `a` 时，已输入部分的最小总距离'
    x, y, a = S['x'], S['y'], S['another_finger']
    return f'`min(f[a] + dis[x][y], f[y] + dis[x][a])`，x = {chr(65+x)}，y = {chr(65+y)}，a = {chr(65+a)}'


CONFIG = dict(
    num=1320, title='二指输入的的最小距离', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='f[另一根手指] 空间优化的线性 DP',
    tags=['其他线性 DP', '难度分 2028'],
    code='''
COLUMN = 6
get_dis = lambda a, b: abs(a // COLUMN - b // COLUMN) + abs(a % COLUMN - b % COLUMN)
dis = [[get_dis(i, j) for j in range(26)] for i in range(26)]

class Solution:
    def minimumDistance(self, word: str) -> int:
        f = [0] * 26
        for x, y in pairwise(word):
            x = ord(x) - ord('A')
            y = ord(y) - ord('A')
            dis_x = dis[x]
            fy = f[y]
            for another_finger in range(26):
                f[another_finger] = min(f[another_finger] + dis_x[y], fy + dis_x[another_finger])
        return min(f)
''',
    call=f'Solution().minimumDistance({WORD!r})',
    expect=6,
    skip=['COLUMN = 6', 'get_dis = ', 'dis = [[', 'for another_finger', 'dis_x = dis[x]'],
    max_steps=40,
    views=[
        dict(type='text', fn=_fml, size=24, h=60),
        dict(type='custom', draw=_draw, h=620),
    ],
    watch=[('x', lambda S: chr(65 + S['x']) if isinstance(S.get('x'), int) else '', 'cyan'), ('y', lambda S: chr(65 + S['y']) if isinstance(S.get('y'), int) else '', 'orange'),
           ('another_finger', 'another_finger', 'pink'), ('fy', 'fy', 'yellow')],
    captions={
        'f = [0] * 26': '`f[a] = 0`：两根手指的起点免费，所以一开始另一根停在哪都是 0',
        'for x, y in pairwise': '取下一对相邻字母 `x → y`（取完就结束循环）：手指从打完 `x` 到要打 `y`',
        'x = ord': '`x` = 字母下标 {x}（`{chr(65 + x)}`）',
        'y = ord': '`y` = 字母下标 {y}（`{chr(65 + y)}`）',
        'fy = f[y]': '先记下 `fy = f[{y}]`：这一轮要用旧的 `f[y]`，因为 `f` 马上被原地覆盖',
        'f[another_finger] = min': ('另一根在 `{chr(65 + another_finger)}`：① 同一根手指 x→y，`{B.f[another_finger]} + {dis_x[y]}`；'
                                    '② 换另一根打 y，`{fy} + {dis_x[another_finger]}` → =={f[another_finger]}=='),
        'return min(f)': '另一根手指停在哪都行，取最小 → =={ret}==',
    },
    cards=dict(
        one_liner='只记「另一根手指在哪」，当前手指一定在刚打的字母上',
        complexity='时间 `O(n·26)`，空间 `O(26)`',
        problem=['键盘按 A–Z 每行 6 个排列，两根手指起点免费、不必在首字母',
                 '距离是曼哈顿距离，求打出 `word` 的最小总移动距离',
                 '示例：`HAPPY` → `6`'],
        quote='去掉 f 的第一个维度，把 f[i+1] 和 f[i] 保存到同一个数组中。此外，由于 dis[x][y] = dis[y][x]，我们可以交换转移方程中的 dis 的两个维度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先写 `dfs(i, another_finger)`：一根手指一定在 `word[i+1]`，只用记另一根',
              '转移两种：同一根手指走过去，或换另一根手指去打，原来那根改去 `another_finger`',
              '1:1 翻译成递推，再去掉第一维，原地更新，要先存好 `fy = f[y]`'],
        summary=['时间 `O(n|Σ|)`，`|Σ| = 26`；空间 `O(|Σ|)`',
                 '原地更新必须先保存旧的 `fy = f[y]`，否则被覆盖',
                 '起点免费，所以 `f` 初始全 0，答案取 `min(f)`',
                 '题解有记忆化、递推、空间优化多种写法，这里选最后的空间优化；`dis` 预处理不计入复杂度'],
    ),
)
