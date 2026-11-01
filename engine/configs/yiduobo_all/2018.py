BOARD = [['#', 'c', '#'], ['a', ' ', ' ']]
WORD = 'ca'

CODE = '''
class Solution(object):
    def placeWordInCrossword(self, board, word):

        m = len(board)
        n = len(board[0])
        l = len(word)

        for i in range(m):
            j = 0
            while j + l - 1 < n:
                while j + l - 1 < n and board[i][j] == '#':
                    j += 1
                if j + l - 1 >= n:
                    break

                flag1 = flag2 = True
                for p in range(l):
                    if board[i][j + p] == ' ':
                        continue
                    if board[i][j + p] != word[p]:
                        flag1 = False
                    if board[i][j + p] != word[l - p - 1]:
                        flag2 = False
                    if not flag1 and not flag2:
                        break

                
                if (flag1 or flag2) and (j + l == n or board[i][j + l] == '#'):
                    return True
                
                j += p
                while j + l - 1 < n and board[i][j] != '#':
                    j += 1
        
        for j in range(n):
            i = 0
            while i + l - 1 < m:
                while i + l - 1 < m and board[i][j] == '#':
                    i += 1
                if i + l - 1 >= m:
                    break

                flag1 = flag2 = True
                for p in range(l):
                    if board[i + p][j] == ' ':
                        continue
                    if board[i + p][j] != word[p]:
                        flag1 = False
                    if board[i + p][j] != word[l - p - 1]:
                        flag2 = False
                    if not flag1 and not flag2:
                        break
                
                if (flag1 or flag2) and (i + l == m or board[i + l][j] == '#'):
                    return True
                
                i += p
                while i + l - 1 < m and board[i][j] != '#':
                    i += 1
        
        return False
'''
_L = CODE.strip('\n').splitlines()
COL_START = next(k for k, t in enumerate(_L, 1) if t.strip() == 'for j in range(n):')
M0 = next(k for k, t in enumerate(_L, 1) if 'flag1 = flag2 = True' in t)
M_END = [k for k, t in enumerate(_L, 1) if t.strip().startswith('if (flag1 or flag2)')]


def _phase(S):
    return 'col' if S.get('_line', 0) >= COL_START else 'row'


def _in_match(S):
    ln = S.get('_line', 0)
    ph = _phase(S)
    end = M_END[1] if ph == 'col' else M_END[0]
    start = [k for k, t in enumerate(_L, 1) if 'flag1 = flag2 = True' in t][1 if ph == 'col' else 0]
    return start <= ln <= end and 'flag1' in S


def _cur_a(S):
    if 'i' not in S or 'j' not in S:
        return None
    return S['i']


def _cur_b(S):
    if 'i' not in S or 'j' not in S:
        return None
    return S['j']


def _col(S, r, c, v):
    if not _in_match(S):
        return None
    l, p = S['l'], S.get('p', -1)
    if _phase(S) == 'row':
        if r != S['i'] or not (S['j'] <= c <= S['j'] + min(p, l - 1)):
            return None
    else:
        if c != S['j'] or not (S['i'] <= r <= S['i'] + min(p, l - 1)):
            return None
    return 'blue' if (S['flag1'] or S['flag2']) else 'red'


def _txt(S):
    if 'flag1' not in S or not _in_match(S):
        return f"word = `{WORD}`：从每个槽位的起点试，正序和倒序各一个标记"
    return f"正序 `flag1 = {S['flag1']}`    倒序 `flag2 = {S['flag2']}`    已比较到第 `p = {S.get('p', '-')}` 个字母"


CONFIG = dict(
    num=2018, title='判断单词是否能放入填字游戏内', difficulty='Medium', category='模拟',
    author='yiduobo', technique='按行按列匹配 · 跳过无用字符',
    tags=[],
    code=CODE,
    call=f'Solution().placeWordInCrossword({BOARD}, {WORD!r})',
    expect=True,
    max_steps=110,
    skip=['flag1 = False', 'flag2 = False', 'continue', 'break', 'j = 0', 'i = 0', 'l = len(word)', 'm = len(board)', 'n = len(board[0])'],
    views=[
        dict(type='grid', var='board', label='board（蓝 = 匹配中的格子，红 = 正反都失败，黄框 = 起点）', cell=100, h=300,
             color=_col, cursors=[(_cur_a, _cur_b, 'yellow')]),
        dict(type='string', var='word', label='word', cell=70, h=130),
        dict(type='text', fn=_txt, size=24, h=60),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('p', 'p', 'blue'), ('flag1', 'flag1', 'green'), ('flag2', 'flag2', 'pink')],
    captions={
        'for i in range(m)': lambda S, B, r: ('每一行都找过了，没有合适的槽位，改按列找' if B.get('i') == S.i and 'i' in B
                                              else f'按行枚举：第 `{S.i}` 行'),
        'for j in range(n)': lambda S, B, r: ('每一列也都找过了' if B.get('j') == S.j and S.j > 0 else f'按列枚举：第 `{S.j}` 列'),
        'while j + l - 1 < n:': lambda S, B, r: (f'从 `j = {S.j}` 开始还放得下长度 `{S.l}` 的单词（`{S.j} + {S.l} - 1 < {S.n}`）' if S.j + S.l - 1 < S.n
                                                else '剩下的格子不够放单词了，这一行结束'),
        'while j + l - 1 < n and board[i][j] == ': lambda S, B, r: (f"`board[{S.i}][{S.j}] = '#'` → 跳过障碍" if S.j + S.l - 1 < S.n and S.board[S.i][S.j] == '#'
                                                                  else f"`j = {S.j}`：起点不是障碍了"),
        'if j + l - 1 >= n': lambda S, B, r: (f'从 `j = {S.j}` 起已经放不下单词 → `break`，换下一行' if S.j + S.l - 1 >= S.n
                                              else '剩余空间够用，开始匹配'),
        'flag1 = flag2 = True': lambda S, B, r: (f'从 `i = {S.i}` 起向下匹配：先假设正序（`flag1`）、倒序（`flag2`）都行' if _phase(S) == 'col'
                                                 else f'从 `j = {S.j}` 起向右匹配：先假设正序（`flag1`）、倒序（`flag2`）都行'),
        "board[i][j + p] == ' '": lambda S, B, r: (f"`board[{S.i}][{S.j + S.p}]` 是空格 → 随便填，看下一个" if S.board[S.i][S.j + S.p] == ' '
                                                  else f"`board[{S.i}][{S.j + S.p}] = '{S.board[S.i][S.j + S.p]}'` 不是空格，要和单词对上"),
        'board[i][j + p] != word[p]': lambda S, B, r: (f"正序：`'{S.board[S.i][S.j + S.p]}'` ≠ `word[{S.p}] = '{S.word[S.p]}'` → `flag1 = False`" if S.board[S.i][S.j + S.p] != S.word[S.p]
                                                       else f"正序：`'{S.board[S.i][S.j + S.p]}'` = `word[{S.p}]` → `flag1` 保持 {S.flag1}"),
        'board[i][j + p] != word[l - p - 1]': lambda S, B, r: (f"倒序：`'{S.board[S.i][S.j + S.p]}'` ≠ `word[{S.l - S.p - 1}] = '{S.word[S.l - S.p - 1]}'` → `flag2 = False`" if S.board[S.i][S.j + S.p] != S.word[S.l - S.p - 1]
                                                               else f"倒序：`'{S.board[S.i][S.j + S.p]}'` = `word[{S.l - S.p - 1}]` → `flag2` 保持 {S.flag2}"),
        'if not flag1 and not flag2': lambda S, B, r: ('正序、倒序都失败了 → `break`，不用再比' if not S.flag1 and not S.flag2 else '至少还有一个方向没失败，继续'),
        'if (flag1 or flag2) and (j + l == n': lambda S, B, r: (f"匹配成功（`flag1 = {S.flag1}`、`flag2 = {S.flag2}`），再看槽位是否到此结束：`j + l = {S.j + S.l}`，行宽 `{S.n}`"
                                                                + (' → ==恰好填满，返回 True==' if (S.flag1 or S.flag2) and (S.j + S.l == S.n or S.board[S.i][S.j + S.l] == '#') else ' → 槽位比单词长，不行')
                                                                if (S.flag1 or S.flag2) else '两个方向都失败 → 这个起点不行'),
        'j += p': lambda S, B, r: f'前面比过的 `{S.p + 1}` 个字符已经没用 → `j` 前进 `p = {S.p}` 到 {S.j}，再去找下一个障碍',
        'while j + l - 1 < n and board[i][j] != ': lambda S, B, r: (f"`board[{S.i}][{S.j}]` 不是 `#`：继续往后走，直到碰到障碍" if S.j + S.l - 1 < S.n and S.board[S.i][S.j] != '#'
                                                                  else '走到障碍（或放不下了），回到外层找下一个槽位'),
        'while i + l - 1 < m:': lambda S, B, r: (f'从 `i = {S.i}` 开始还放得下长度 `{S.l}` 的单词（`{S.i} + {S.l} - 1 < {S.m}`）' if S.i + S.l - 1 < S.m
                                                else '剩下的格子不够放单词了，这一列结束'),
        'while i + l - 1 < m and board[i][j] == ': lambda S, B, r: (f"`board[{S.i}][{S.j}] = '#'` → 跳过障碍" if S.i + S.l - 1 < S.m and S.board[S.i][S.j] == '#'
                                                                  else f"`i = {S.i}`：起点不是障碍了"),
        'if i + l - 1 >= m': lambda S, B, r: (f'从 `i = {S.i}` 起已经放不下单词 → `break`，换下一列' if S.i + S.l - 1 >= S.m
                                              else '剩余空间够用，开始匹配'),
        "board[i + p][j] == ' '": lambda S, B, r: (f"`board[{S.i + S.p}][{S.j}]` 是空格 → 随便填，看下一个" if S.board[S.i + S.p][S.j] == ' '
                                                  else f"`board[{S.i + S.p}][{S.j}] = '{S.board[S.i + S.p][S.j]}'` 不是空格，要和单词对上"),
        'board[i + p][j] != word[p]': lambda S, B, r: (f"正序：`'{S.board[S.i + S.p][S.j]}'` ≠ `word[{S.p}] = '{S.word[S.p]}'` → `flag1 = False`" if S.board[S.i + S.p][S.j] != S.word[S.p]
                                                       else f"正序：`'{S.board[S.i + S.p][S.j]}'` = `word[{S.p}]` → `flag1` 保持 {S.flag1}"),
        'board[i + p][j] != word[l - p - 1]': lambda S, B, r: (f"倒序：`'{S.board[S.i + S.p][S.j]}'` ≠ `word[{S.l - S.p - 1}] = '{S.word[S.l - S.p - 1]}'` → `flag2 = False`" if S.board[S.i + S.p][S.j] != S.word[S.l - S.p - 1]
                                                               else f"倒序：`'{S.board[S.i + S.p][S.j]}'` = `word[{S.l - S.p - 1}]` → `flag2` 保持 {S.flag2}"),
        'if (flag1 or flag2) and (i + l == m': lambda S, B, r: (f"匹配成功（`flag1 = {S.flag1}`、`flag2 = {S.flag2}`），再看槽位是否到此结束：`i + l = {S.i + S.l}`，列高 `{S.m}`"
                                                                + (' → ==恰好填满，返回 True==' if (S.flag1 or S.flag2) and (S.i + S.l == S.m or S.board[S.i + S.l][S.j] == '#') else ' → 槽位比单词长，不行')
                                                                if (S.flag1 or S.flag2) else '两个方向都失败 → 这个起点不行'),
        'i += p': lambda S, B, r: f'前面比过的 `{S.p + 1}` 个字符已经没用 → `i` 前进 `p = {S.p}` 到 {S.i}，再去找下一个障碍',
        'while i + l - 1 < m and board[i][j] != ': lambda S, B, r: (f"`board[{S.i}][{S.j}]` 不是 `#`：继续往下走，直到碰到障碍" if S.i + S.l - 1 < S.m and S.board[S.i][S.j] != '#'
                                                                  else '走到障碍（或放不下了），回到外层找下一个槽位'),
        'return True': '找到了：返回 `True`',
        'return False': '行列都没找到合适的槽位，返回 `False`',
    },
    cards=dict(
        one_liner='老老实实按行按列匹配：正序倒序各试一遍，再看槽位是否恰好填满',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`board` 里有字母、空格和障碍 `#`，问单词能否水平或竖直、正着或倒着填进去',
                 '要求：不碰 `#`、字母要对上、==单词两端必须紧挨 `#` 或边界==',
                 '示例：`[["#","c","#"],["a"," "," "]]`，`"ca"` → `true`（第 1 列从上往下）'],
        quote='没有想到什么特别好的做法，只能老老实实按行按列来进行匹配。……由于前面这些字符已经没有用了，题目又要求是恰好填进去，因此接下来就可以直接跳过这些字符',
        quote_src='—— yiduobo 题解原文',
        idea=['每行：先跳过障碍，找到第一个非障碍字符，从它开始和 `word` 正序、倒序同时匹配',
              '匹配成功后还要检查：是否到了行尾，或者下一个字符是障碍 → 才算恰好',
              '否则这几个字符没用了：`j += p` 之后直接跳到下一个障碍，再重复；列的做法一样，只是把坐标互换'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '`while j + l - 1 < n`：剩余长度不够单词就不用再找了',
                 '空格直接 `continue`（随便填），其他字符和 `word[p]`、`word[l-p-1]` 分别比较',
                 '匹配成功后别忘了检查末尾：槽位必须==恰好==等于单词长度',
                 '对比灵神：灵神把 `#` 之间的整段当槽位一次扫完；这里是从起点试长度 `l` 再跳到下一个 `#`'],
    ),
)
