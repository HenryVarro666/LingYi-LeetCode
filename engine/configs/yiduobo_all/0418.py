ROWS, COLS = 4, 6


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    x, y = S.get('x'), S.get('y')
    cv.text((x0 + 18, y0 + 30), f'屏幕 {ROWS} 行 × {COLS} 列（蓝 = 当前行已填的列，灰 = 已填满的行，黄线 = y）', 22, T['muted'], bold=True)
    if x is None or y is None:
        return
    cell = min(62, (x1 - x0 - 60) / COLS, (y1 - y0 - 80) / ROWS)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * COLS) / 2
    sy = y0 + 96
    for r in range(ROWS):
        for c in range(COLS):
            X, Y = sx + c * cell, sy + r * cell
            if r < x:
                fill = (70, 78, 90)
            elif r == x and c < y:
                fill = T['blue']
            else:
                fill = T['panel2']
            cv.rect((X + 2, Y + 2, X + cell - 2, Y + cell - 2), fill=fill, r=6, outline=T['border'])
        cv.text((sx - 10, sy + r * cell + cell / 2), f'x={r}', 20, T['yellow'] if r == x else T['dim'], anchor='rm', bold=True, mono=True)
    if x < ROWS:
        X = sx + y * cell
        cv.line([(X, sy - 4 if x == 0 else sy + x * cell - 4), (X, sy + (x + 1) * cell + 4)], T['yellow'], 5)
        cv.text((X, sy - 8), f'y={y}', 22, T['yellow'], anchor='mb', bold=True)


def _cap_len(S, B, r):
    return f'`len({S.word!r}) = {len(S.word)}` {">" if len(S.word) > S.cols else "≤"} `cols = {S.cols}`' + ('：放不下任何一行 → 答案 ==0==' if len(S.word) > S.cols else '：能放进一行')


def _cap_fit(S, B, r):
    ok = S.s + S.y + S.delta <= S.cols
    return (f'`s + y + delta = {S.s} + {S.y} + {S.delta} = {S.s + S.y + S.delta}` ' +
            (f'≤ `cols = {S.cols}` → 这一行还能整句填一次（不跨行）' if ok else f'> `cols = {S.cols}` → 整句放不下，要逐词模拟'))


def _cap_wf(S, B, r):
    word, y = S.word, S.y
    need = len(word) + S.delta
    if y + need <= S.cols:
        return f'`{y} + len({word!r}) + {S.delta} = {y + need}` ≤ `{S.cols}` → ==本行放得下=='
    return f'`{y} + {need} = {y + need}` > `{S.cols}` → ==放不下，单词不能拆开，换到下一行=='


CONFIG = dict(
    num=418, title='屏幕可显示句子的数量', difficulty='Medium', category='模拟',
    author='yiduobo', technique='模拟填充 + 哈希记忆跨行结果',
    tags=[],
    code='''
class Solution(object):
    def wordsTyping(self, sentence, rows, cols):

        s = 0
        for word in sentence:
            if len(word) > cols:
                return 0
            s += len(word)
        
        s += len(sentence) - 1

        x = 0
        y = 0
        first = True
        f = {}
        res = 0
        while x < rows:
            if first:
                delta = 0
            else:
                delta = 1

            if s + y + delta <= cols:
                y += s + delta
                res += 1
                first = False
            
                tmp = (cols - y) // (s + 1)
                res += tmp
                y += tmp * (s + 1)

            if y in f:
                x += f[y][0]
                y = f[y][1]
                if x >= rows:
                    return res
                else:
                    res += 1
                
                continue
            
            last_x, last_y = x, y
            for word in sentence:
                if first:
                    delta = 0
                else:
                    delta = 1

                if y + len(word) + delta <= cols:
                    y += len(word) + delta
                else:
                    x += 1
                    if x == rows:
                        return res
                    y = len(word)

                first = False

            res += 1
            f[last_y] = [x - last_x, y]

        return res
''',
    call=f'Solution().wordsTyping(["a", "bc", "d"], {ROWS}, {COLS})',
    expect=4,
    views=[
        dict(type='array', var='sentence', label='sentence（单词不能拆开、不能换序）', h=230, cell=90,
             pointers={'sentence.index(word)': 'pink'}, pointer_labels={'sentence.index(word)': 'word'}),
        dict(type='custom', draw=_draw, h=480),
        dict(type='map', var='f', label='f：句子起点 y → [跨了几行, 句子结束列]', h=130,
             fmt=lambda k, v: f'{v[0]} 行, 列 {v[1]}'),
    ],
    watch=[('x 行', 'x', 'yellow'), ('y 列', 'y', 'yellow'), 's', 'first', ('res', 'res', 'green')],
    captions={
        'if len(word) > cols': _cap_len,
        's += len(sentence) - 1': '句子里单词间要 `{len(sentence)-1}` 个空格 → 整句占 `s = {s}` 列',
        'x = 0': '`x` 是当前行，`y` 是当前行已用的列数',
        'first = True': '`first`：这一行（整个屏幕）还没放过东西，放词前不用补空格',
        'f = {}': '`f` 记录「从列 y 开始填完一句」的结果，下次直接跳',
        'if first:': '`first = {first}` → 前面要不要空格：`delta = {0 if first else 1}`',
        'delta = 0': '首次填充，不需要间隔空格：`delta = 0`',
        'delta = 1': '不是首次，词前要补一个空格：`delta = 1`',
        'if s + y + delta <= cols': _cap_fit,
        'y += s + delta': '整句填一次：`y` → =={y}==（一句占 `s + delta` 列）',
        'tmp = (cols - y)': '后面每整句花 `s + 1 = {s+1}` 列，用除法一次算出还能塞几句：`tmp = {tmp}`',
        'res += tmp': '`res` += `{tmp}` → {res}',
        'y += tmp': '`y` 跳到 `{y}`，一次性填完这些整句',
        'if y in f': lambda S, B, r: (f'`y = {S.y}` 在 `f` 里 → 之前模拟过，直接用结果' if S.y in S.f
                                      else f'`y = {S.y}` 不在 `f` 里 → 需要逐词模拟一整句'),
        'x += f[y][0]': '用记忆：跨 `{f[B.y][0]}` 行，`x` → {x}，`y` → `{y}`',
        'return res': '`return res` = =={res}==',
        'last_x, last_y = x, y': '记下起点 `({x}, {y})`，句子填完后存入 `f`',
        43: '逐个单词填：`word = {word!r}`',
        5: '先扫一遍单词：`word = {word!r}`，累加长度',
        'if y + len(word) + delta': _cap_wf,
        'y += len(word) + delta': '放进本行：`y` → =={y}==',
        'x += 1': '换行：`x` → =={x}==',
        'y = len(word)': '新的一行从这个单词开始：`y = len({word!r}) = {y}`',
        'first = False': '放过东西了，之后词前都要空格',
        'res += 1': '一整句填完，`res` → =={res}==',
        'f[last_y] =': '存记忆：从列 `{last_y}` 开始填一句，==跨 {x-last_x} 行，结束于列 {y}==',
    },
    cards=dict(
        one_liner='整句不跨行用除法一次算，跨行用哈希记住',
        complexity='时间 约 `O(rows + 句子长度 × 列数)`，空间 `O(cols)`',
        problem=['给定 `rows × cols` 的屏幕和一个单词列表 `sentence`',
                 '按顺序循环填入句子，==单词不能拆开==，相邻单词间至少一个空格',
                 '求整个句子完整出现了几次。示例：`["a","bc","d"]`，4 行 6 列 → `4`'],
        quote='因此可以将所有模拟跨行的结果都以句子的起始位置为key储存起来，在后续遇到相同情况时就可以直接定位到句子的终点了。',
        quote_src='—— yiduobo 题解原文',
        idea=['单词不能跨行，不能直接用除法算总长度；但「不跨行的整句」可以除',
              '用 `first` 记录是否首次填充：非首次词前补空格 `delta = 1`',
              '逐词模拟一句后，把「起点列 → (跨行数, 终点列)」存进 `f`，以后遇到同样起点直接跳'],
        summary=['先检查：任何单词长度超过 `cols` → 答案 `0`',
                 '整句不跨行：`tmp = (cols - y) // (s + 1)` 一次塞完',
                 '易错：`first` 为真时 `delta = 0`；换行后 `y = len(word)`，并把 `first` 置假',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`，并删去了类型说明文档字符串'],
    ),
)
