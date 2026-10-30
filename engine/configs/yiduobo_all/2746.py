WORDS = ['aa', 'ab', 'bc']


def _st(st):
    return chr(97 + st // 26) + chr(97 + st % 26)


def _items(lst):
    return [(_st(k), v) for k, v in enumerate(lst) if v is not None] if lst else []


def _chips(cv, T, x, y, items, title, color, hl=None):
    cv.text((x, y), title, 24, color, bold=True)
    if not items:
        cv.text((x, y + 44), '（空）', 24, T['dim'])
        return
    for n, (name, v) in enumerate(items):
        yy = y + 44 + n * 52
        on = hl is not None and name == hl
        cv.rect((x, yy, x + 330, yy + 44), fill=T['yellow'] if on else T['panel2'], outline=T['border'], r=8)
        cv.text((x + 16, yy + 22), f'首尾 {name[0]}…{name[1]}', 24, T['bg'] if on else T['text'], anchor='lm', bold=True)
        cv.text((x + 314, yy + 22), f'长度 {v}', 24, T['bg'] if on else T['green'], anchor='rm', bold=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    words = S['words']
    cv.text((x0 + 18, y0 + 4), 'words（粉框 = 当前拼接的 w）', 24, T['muted'], bold=True)
    w = S.get('w')
    cell = 130
    for k, wd in enumerate(words):
        X = x0 + 20 + k * (cell + 14)
        cur = wd == w
        cv.rect((X, y0 + 44, X + cell, y0 + 104), fill=T['panel2'], outline=T['pink'] if cur else T['border'], width=5 if cur else 1, r=10)
        cv.text((X + cell / 2, y0 + 74), wd, 34, T['text'], anchor='mm', bold=True, mono=True)
    f, g = S.get('f'), S.get('g')
    y = y0 + 140
    if g is not None:
        _chips(cv, T, x0 + 20, y, _items(g), 'g：上一轮各种首尾的最短长度', T['blue'], S.get('pre_state') is not None and _st(S['pre_state']))
        _chips(cv, T, x0 + 400, y, _items(f), 'f：这一轮', T['yellow'])
    else:
        _chips(cv, T, x0 + 20, y, _items(f), 'f：目前只有 words[0]', T['yellow'])


CONFIG = dict(
    num=2746, title='字符串连接删减字母', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='状态压缩 DP：只记首尾字符',
    tags=[],
    code='''
class Solution(object):
    def minimizeConcatenatedLength(self, words):

        f = [None] * 676
        left = ord(words[0][0]) - 97
        right = ord(words[0][-1]) - 97
        f[left * 26 + right] = len(words[0])
        for w in words[1:]:
            g = f[:]
            f = [None] * 676
            left = ord(w[0]) - 97
            right = ord(w[-1]) - 97
            for pre_state in range(676):
                if g[pre_state] is None:
                    continue

                pre_left = pre_state // 26
                pre_right = pre_state % 26

                left_delta = right_delta = 0
                if right == pre_left:
                    left_delta = -1
                if left == pre_right:
                    right_delta = -1
                
                left_state = left * 26 + pre_right
                right_state = pre_left * 26 + right
                if f[left_state] is None or f[left_state] > g[pre_state] + len(w) + left_delta:
                    f[left_state] = g[pre_state] + len(w) + left_delta
                if f[right_state] is None or f[right_state] > g[pre_state] + len(w) + right_delta:
                    f[right_state] = g[pre_state] + len(w) + right_delta
                
        

        res = None
        for state in range(676):
            if f[state] is not None and (res is None or res > f[state]):
                res = f[state]
        
        return res
''',
    call=f'Solution().minimizeConcatenatedLength({WORDS})',
    expect=4,
    skip=['for pre_state in range(676)', 'if g[pre_state] is None', 'continue', 'for state in range(676)', 'if f[state] is not None'],
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('pre_left', 'pre_left', 'cyan'), ('pre_right', 'pre_right', 'cyan'),
           ('res', 'res', 'green')],
    captions={
        'f = [None] * 676': '`f[state]`：当前字符串首尾字符编码为 `state = 首×26 + 尾` 时的最短长度；`None` = 不可达',
        'left = ord(words[0][0])': '首字符编号 `left = {left}`（`a` = 0）',
        'right = ord(words[0][-1])': '尾字符编号 `right = {right}`',
        'f[left * 26 + right] = len': '`words[0]` 的状态 `{left}×26+{right}` 长度是 `{f[left * 26 + right]}`',
        'for w in words[1:]': lambda S, B, r: (f'接下来拼 `w = "{S.w}"`：只有首尾字符影响拼接，所以只记首尾' if S.get('w') != B.get('w')
                                               else '所有单词拼完，从 `f` 里取最小'),
        'g = f[:]': '`g` 存上一轮的结果，`f` 清空来存这一轮（滚动数组）',
        'f = [None] * 676': '`f` 重置为全 `None`',
        'left = ord(w[0])': '`w` 的首字符编号 `left = {left}`',
        'right = ord(w[-1])': '`w` 的尾字符编号 `right = {right}`',
        'pre_left = pre_state': '枚举上一轮一个可达状态 `pre_state = {pre_state}`，首字符 `pre_left = {pre_left}`',
        'pre_right = pre_state % 26': '尾字符 `pre_right = {pre_right}`',
        'left_delta = right_delta = 0': '先假设拼接都不能省字符',
        'if right == pre_left': lambda S, B, r: (f'`w` 放左边：`w` 的尾 `{S.right}` 等于旧串的首 `{S.pre_left}` → 相接处省 1 个字符' if S.right == S.pre_left
                                                 else f'`w` 放左边：`w` 的尾 `{S.right}` ≠ 旧串的首 `{S.pre_left}` → 不能省'),
        'left_delta = -1': '放左边省 1 个字符：`left_delta = -1`',
        'if left == pre_right': lambda S, B, r: (f'`w` 放右边：旧串的尾 `{S.pre_right}` 等于 `w` 的首 `{S.left}` → 省 1 个字符' if S.left == S.pre_right
                                                  else f'`w` 放右边：旧串的尾 `{S.pre_right}` ≠ `w` 的首 `{S.left}` → 不能省'),
        'right_delta = -1': '放右边省 1 个字符：`right_delta = -1`',
        'left_state = left': '放左边：新串首字符变成 `w` 的首，尾保持 `pre_right` → 状态 `{left_state}`',
        'right_state = pre_left': '放右边：首字符保持 `pre_left`，尾变成 `w` 的尾 → 状态 `{right_state}`',
        'if f[left_state] is None': lambda S, B, r: (f'放左边候选长度 `{S.g[S.pre_state]} + {len(S.w)}{" − 1" if S.left_delta else ""}` = `{S.g[S.pre_state] + len(S.w) + S.left_delta}`；'
                                                     f'状态 `{S.left_state}` 目前{"还没有" if B.f[S.left_state] is None else "是 " + str(B.f[S.left_state])}'
                                                     + ('，更小 → 更新' if B.f[S.left_state] is None or B.f[S.left_state] > S.g[S.pre_state] + len(S.w) + S.left_delta else '，不更优 → 保留')),
        'f[left_state] = g[pre_state]': '`f[{left_state}] = {f[left_state]}`：放左边的最短长度',
        'if f[right_state] is None': lambda S, B, r: (f'放右边候选长度 `{S.g[S.pre_state]} + {len(S.w)}{" − 1" if S.right_delta else ""}` = `{S.g[S.pre_state] + len(S.w) + S.right_delta}`；'
                                                      f'状态 `{S.right_state}` 目前{"还没有" if B.f[S.right_state] is None else "是 " + str(B.f[S.right_state])}'
                                                      + ('，更小 → 更新' if B.f[S.right_state] is None or B.f[S.right_state] > S.g[S.pre_state] + len(S.w) + S.right_delta else '，不更优 → 保留')),
        'f[right_state] = g[pre_state]': '`f[{right_state}] = {f[right_state]}`：放右边的最短长度',
        'res = None': '`res` 用来取所有末状态里的最小长度',
        'res = f[state]': '状态 `{state}` 的长度 `{f[state]}` 更小 → `res = {res}`',
        'return res': '最短长度 ==`{ret}`==',
    },
    cards=dict(
        one_liner='拼接只看首尾字符，所以状态只记「首字符 + 尾字符」',
        complexity='时间 `O(n·26^2)`，空间 `O(26^2)`',
        problem=['把 `words` 依次拼接：每步可把下一个词放在当前串的左边或右边',
                 '拼接时若前一个串的尾字符 == 后一个串的首字符，==删掉其中一个==',
                 '求最后得到的字符串的最短长度；本视频 `["aa","ab","bc"]` → `4`'],
        quote='注意到字符串在连接时只有首尾两字符会影响最终连接的长度，因此可以使用状态压缩动态规划来求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][state]`：前 `i` 个串连接后，首尾字符编码为 `state = 首×26 + 尾` 时的最短长度',
              '枚举上一轮的可行状态，新词放左：新首 = `w` 的首，能否省字符看 `w` 的尾是否等于旧首',
              '放右同理；滚动数组 `g` / `f` 省掉第一维'],
        summary=['时间 `O(n·26^2)`，空间 `O(26^2)`',
                 '易错：放左边时看 `w` 的==尾==和旧串的==首==，放右边看旧串的尾和 `w` 的首',
                 '原文为 Python 2 写法，`pre_state / 26` 已改为 `pre_state // 26`',
                 '`None` 表示不可达；比较前先判 `None`，最后取最小值时同理',
                 '演示里 `for pre_state` 等 676 次枚举的循环行没有单独展示，只展示有可达状态的那几次'],
    ),
)
