WORD = 'CAKE'


def _nm(c):
    return '·' if c == 0 else chr(64 + c)


def _chips(cv, T, x, y, W, tbl, hot, cold, size=24):
    items = []
    if tbl is None:
        return y
    for a in range(27):
        for b in range(27):
            v = tbl[a][b]
            if v is not None:
                items.append((a, b, v))
    cx, cy = x, y
    for a, b, v in items:
        s = f'({_nm(a)},{_nm(b)})={v}'
        w = cv.tlen(s, size, mono=True) + 22
        if cx + w > x + W:
            cx, cy = x, cy + 44
        col = None
        if (a, b) == hot:
            col = T['yellow']
        elif (a, b) in cold:
            col = T['green']
        cv.rect((cx, cy, cx + w, cy + 38), fill=col or T['panel2'], r=8, outline=T['border'])
        cv.text((cx + w / 2, cy + 19), s, size, T['bg'] if col else T['text'], anchor='mm', mono=True, bold=bool(col))
        cx += w + 8
    return cy + 44


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    f, g = S.get('f'), S.get('g')
    num = S.get('num')
    first, second = S.get('first'), S.get('second')
    live = isinstance(first, int) and isinstance(second, int) and g is not None
    hot = (first, second) if live else None
    cold = set()
    if live and isinstance(num, int):
        cold = {(num, second), (first, num)}
    cv.text((x0 + 18, y0 + 4), '上一轮 f：(第一根手指, 第二根手指)=最小距离（· = 还没用过）', 22, T['muted'], bold=True)
    yy = _chips(cv, T, x0 + 18, y0 + 44, x1 - x0 - 36, f, hot, set())
    yy = max(yy, y0 + 250) + 6
    cv.text((x0 + 18, yy), '本轮 g：打完当前字母后的状态（绿 = 本次可能更新的）', 22, T['muted'], bold=True)
    if g is not None and live:
        _chips(cv, T, x0 + 18, yy + 40, x1 - x0 - 36, g, None, cold)
    elif g is not None:
        _chips(cv, T, x0 + 18, yy + 40, x1 - x0 - 36, g, None, set())


def _cap(S, B, ret):
    first, second, num = S.first, S.second, S.num
    f0 = S.f[first][second]
    c1 = S.dis[first][num]
    c2 = S.dis[second][num]
    return (f'状态 `({_nm(first)},{_nm(second)})` = {f0}：① 第一根手指走到 `{_nm(num)}`，代价 `{c1}`，得 `g[{_nm(num)}][{_nm(second)}]`；'
            f'② 第二根走到 `{_nm(num)}`，代价 `{c2}`，得 `g[{_nm(first)}][{_nm(num)}]`')


CONFIG = dict(
    num=1320, title='二指输入的的最小距离', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='f[first][second] 逐字符滚动 DP',
    tags=['其他线性 DP', '难度分 2028'],
    code='''
class Solution(object):
    def minimumDistance(self, word):

        dis = [[0] * 27 for _ in range(27)]
        x = [index // 6 for index in range(26)]
        y = [index % 6 for index in range(26)]
        for i in range(1, 27):
            for j in range(1, 27):
                dis[i][j] = abs(x[i - 1] - x[j - 1]) + abs(y[i - 1] - y[j - 1])
        
        f = [[None] * 27 for _ in range(27)]
        f[0][0] = 0
        for char in word:
            num = ord(char) - 64
            g = [[None] * 27 for _ in range(27)]
            for first in range(27):
                for second in range(27):
                    if f[first][second] is not None:
                        if g[num][second] is None or g[num][second] > f[first][second] + dis[first][num]:
                            g[num][second] = f[first][second] + dis[first][num]
                        if g[first][num] is None or g[first][num] > f[first][second] + dis[second][num]:
                            g[first][num] = f[first][second] + dis[second][num]
            
            f = g[:]
        
        res = None
        for first in range(27):
            for second in range(27):
                if f[first][second] is not None and (res is None or res > f[first][second]):
                    res = f[first][second]
        
        return res
''',
    call=f'Solution().minimumDistance({WORD!r})',
    expect=3,
    skip=['dis = [[0]', 'x = [index', 'y = [index', 'for i in range(1, 27)', 'for j in range(1, 27)', 'dis[i][j] =',
          'for first in range', 'for second in range', 'is not None:', 'is not None and', 'g = [[None]', 'res = f[first][second]'],
    max_steps=50, max_events=60000,
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('char', "char", 'cyan'), ('first', 'first', 'blue'), ('second', 'second', 'pink'), ('res', 'res', 'green')],
    captions={
        'f[0][0] = 0': '`f[0][0] = 0`：两根手指都还没用过（用 0 表示），起点免费，距离为 0',
        'for char in word': lambda S, B, r: ('逐个字母处理：每个字母都要有一根手指去打' if 'char' in S else ''),
        'num = ord': '`num = {num}`：字母 `{char}` 编号为 1–26',
        'if g[num][second]': _cap,
        'g[num][second] = f': lambda S, B, r: f'`g[{_nm(S.num)}][{_nm(S.second)}]` 写入 =={S.g[S.num][S.second]}==：第一根手指落在 `{_nm(S.num)}`',
        'if g[first][num]': lambda S, B, r: (f'`g[{_nm(S.first)}][{_nm(S.num)}]` 还是空的 → 直接写入' if B.g[S.first][S.num] is None else f'`g[{_nm(S.first)}][{_nm(S.num)}]` 已有 {B.g[S.first][S.num]}，新值 {S.f[S.first][S.second] + S.dis[S.second][S.num]}：只有更小才更新'),
        'g[first][num] = f': lambda S, B, r: f'`g[{_nm(S.first)}][{_nm(S.num)}]` 写入 =={S.g[S.first][S.num]}==：第二根手指落在 `{_nm(S.num)}`',
        'f = g[:]': '这一个字母处理完，`g` 成为下一轮的 `f`',
        'res = None': '`res` 记录所有状态里的最小距离',
        'return res': '所有手指位置里最小的距离 = =={ret}==',
    },
    cards=dict(
        one_liner='状态 = 两根手指的位置，每个字母由其中一根去打',
        complexity='时间 `O(729·n)`，空间 `O(729)`',
        problem=['键盘按 A–Z 每行 6 个排列，两根手指起点免费、不必在首字母',
                 '距离是曼哈顿距离，求打出 `word` 的最小总移动距离',
                 '示例：`CAKE` → `3`'],
        quote='令f[i][first][second]表示前i步，第一个手指在first上，第二个手指在second上所需的最小移动步数，那么这里一共有27 * 27 = 729中可能性。',
        quote_src='—— yiduobo 题解原文',
        idea=['27 = 26 个字母 + 「手指还没用过」（编号 0，到任何字母距离都是 0）',
              '打 `char` 时：第一根走过去，或者第二根走过去，两种转移取最小',
              '每轮只依赖上一轮，用 `f`、`g` 两张表滚动'],
        summary=['时间 `O(729·n)`，空间 `O(729)`（滚动数组）',
                 '用 `None` 表示不可达状态，更新前要先判断 `is None`',
                 '字母编号 `ord(char) - 64` 对应 1–26，`dis` 里用 `i-1` 取坐标',
                 '原文为 Python 2 写法，`index / 6` 是整数除法，已改为 `index // 6`'],
    ),
)
