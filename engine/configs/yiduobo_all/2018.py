CODE_COL_LINE = 35  # 「for j in range(n):」所在代码行（按 --steps 校准）


def _col_phase(S):
    return S.get('_line', 0) >= CODE_COL_LINE


def _live(S):
    """当前是否处于某个槽位的扫描中（避免显示上一轮遗留的变量）"""
    ln = S.get('_line', 0)
    return 11 <= ln <= 33 or 38 <= ln <= 59


def _win(S):
    """当前尝试匹配的槽位格子集合"""
    if 'l' not in S or not _live(S):
        return set()
    l = S['l']
    if not _col_phase(S):
        return {(S['i'], S['j'] + p) for p in range(l)}
    return {(S['i'] + p, S['j']) for p in range(l)}


def _color(S, i, j, v):
    if (i, j) in _win(S):
        return 'red' if v == '#' else 'cyan'
    if v == '#':
        return 'purple'
    return None


def _top(S):
    if 'l' not in S:
        return ''
    ln = S.get('_line', 0)
    if not _live(S):
        return '按行扫描' if ln < 35 else '按列扫描'
    ph = '按列' if _col_phase(S) else '按行'
    s = f"{ph}扫描：槽位起点 `({S.get('i')}, {S.get('j')})`，长度 `{S['l']}`，单词 `{S['word']}`"
    if ln >= (43 if _col_phase(S) else 16):
        f1, f2 = S.get('flag1'), S.get('flag2')
        s += f"　正序 ==" + ('通过' if f1 else '失败') + "==　倒序 ==" + ('通过' if f2 else '失败') + "=="
    return s


CONFIG = dict(
    num=2018, title='判断单词是否能放入填字游戏内', difficulty='Medium', category='模拟',
    author='yiduobo', technique='按行按列枚举槽位 · 正倒序匹配',
    tags=[],
    code='''
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
''',
    call='Solution().placeWordInCrossword([["#", " ", "#"], [" ", " ", "#"], ["#", "c", " "]], "abc")',
    expect=True,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='grid', var='board', label='board（紫 = 障碍 #，空白 = 空格，青 = 当前槽位）', cell=110, h=420,
             color=_color),
        dict(type='string', var='word', label='word', cell=84, h=130),
    ],
    watch=['i', 'j', 'p', 'flag1', 'flag2'],
    captions={
        6: '`l = {l}`：单词长度，槽位必须==恰好==这么长',
        10: lambda S, B, r: f"剩余格子够放 `{S.l}` 个字母吗：`{S.j} + {S.l} - 1 < {S.n}` → " + ('够，找槽位' if S.j + S.l - 1 < S.n else '不够，这一行结束'),
        11: lambda S, B, r: (f"从 `j = {S.j}` 起不够放 `{S.l}` 个字母了，不再找起点" if S.j + S.l - 1 >= S.n else f"`board[{S.i}][{S.j}]` 是障碍 `#`，不能当槽位起点，往右跳" if S.board[S.i][S.j] == '#' else f"`board[{S.i}][{S.j}]` 不是障碍 → ==槽位起点找到=="),
        13: lambda S, B, r: ('起点之后放不下整个单词 → 这一行没有槽位了，`break`' if S.j + S.l - 1 >= S.n else f'从 `j = {S.j}` 起还放得下 `{S.l}` 个字母，继续验证'),
        16: '假设正序、倒序都能放，下面逐格验证',
        18: lambda S, B, r: (f"`board[{S.i}][{S.j + S.p}]` 是空格：和任何字母都兼容，跳过" if S.board[S.i][S.j + S.p] == ' ' else f"`board[{S.i}][{S.j + S.p}]` 已有字母 `{S.board[S.i][S.j + S.p]}`，要和单词对上"),
        20: lambda S, B, r: f"槽位 `{S.board[S.i][S.j + S.p]!r}` 对 正序 `word[{S.p}] = {S.word[S.p]!r}`：" + ('不等 → ==正序失败==' if S.board[S.i][S.j + S.p] != S.word[S.p] else '相等，正序继续'),
        22: lambda S, B, r: f"槽位 `{S.board[S.i][S.j + S.p]!r}` 对 倒序 `word[{S.l - S.p - 1}] = {S.word[S.l - S.p - 1]!r}`：" + ('不等 → ==倒序失败==' if S.board[S.i][S.j + S.p] != S.word[S.l - S.p - 1] else '相等，倒序继续'),
        24: lambda S, B, r: ('两个方向都失败 → 不用再看后面的格子，`break`' if not S.flag1 and not S.flag2 else f"还有一个方向没失败（正序 {S.flag1}，倒序 {S.flag2}），继续往后比"),
        28: lambda S, B, r: (f"匹配成功（正序 {S.flag1}，倒序 {S.flag2}），且槽位右边是行尾或 `#`，说明==恰好填满==" if (S.flag1 or S.flag2) and (S.j + S.l == S.n or S.board[S.i][S.j + S.l] == '#') else f"不能放：正序 {S.flag1}，倒序 {S.flag2}，没有哪个方向能放下"),
        29: '行里找到恰好能放下 `word` 的槽位 → ==返回 True==',
        31: '这一段前面的字符已经没用了：直接从 `j = {j}` 往后找下一个 `#`',
        32: '一直往右走到下一个障碍 `#`，下一个槽位从它后面开始',
        35: '行都找完了，按列再来一遍：坐标互换，`j = {j}`',
        37: lambda S, B, r: f"剩余格子够放 `{S.l}` 个字母吗：`{S.i} + {S.l} - 1 < {S.m}` → " + ('够，找槽位' if S.i + S.l - 1 < S.m else '不够，这一列结束'),
        38: lambda S, B, r: (f"从 `i = {S.i}` 起不够放 `{S.l}` 个字母了，不再找起点" if S.i + S.l - 1 >= S.m else f"`board[{S.i}][{S.j}]` 是障碍 `#`，往下跳" if S.board[S.i][S.j] == '#' else f"`board[{S.i}][{S.j}]` 不是障碍 → ==槽位起点找到=="),
        40: lambda S, B, r: ('起点之下放不下整个单词 → 这一列没有槽位了，`break`' if S.i + S.l - 1 >= S.m else f'从 `i = {S.i}` 起还放得下 `{S.l}` 个字母，继续验证'),
        43: '假设正序（从上到下）、倒序都能放，下面逐格验证',
        45: lambda S, B, r: (f"`board[{S.i + S.p}][{S.j}]` 是空格：和任何字母都兼容，跳过" if S.board[S.i + S.p][S.j] == ' ' else f"`board[{S.i + S.p}][{S.j}]` 已有字母 `{S.board[S.i + S.p][S.j]}`，要和单词对上"),
        47: lambda S, B, r: f"槽位 `{S.board[S.i + S.p][S.j]!r}` 对 正序 `word[{S.p}] = {S.word[S.p]!r}`：" + ('不等 → ==正序失败==' if S.board[S.i + S.p][S.j] != S.word[S.p] else '相等，正序继续'),
        49: lambda S, B, r: f"槽位 `{S.board[S.i + S.p][S.j]!r}` 对 倒序 `word[{S.l - S.p - 1}] = {S.word[S.l - S.p - 1]!r}`：" + ('不等 → ==倒序失败==' if S.board[S.i + S.p][S.j] != S.word[S.l - S.p - 1] else '相等，倒序继续'),
        51: lambda S, B, r: ('两个方向都失败 → `break`' if not S.flag1 and not S.flag2 else f"还有一个方向没失败（正序 {S.flag1}，倒序 {S.flag2}），继续"),
        54: lambda S, B, r: (f"匹配成功（正序 {S.flag1}，倒序 {S.flag2}），且槽位下边是列尾或 `#`，说明==恰好填满==" if (S.flag1 or S.flag2) and (S.i + S.l == S.m or S.board[S.i + S.l][S.j] == '#') else f"不能放：正序 {S.flag1}，倒序 {S.flag2}，没有哪个方向能放下"),
        55: '列里找到恰好能放下 `word` 的槽位 → ==返回 True==',
        57: '这一段前面的字符已经没用了：直接从 `i = {i}` 往下找下一个 `#`',
        58: '一直往下走到下一个障碍 `#`，下一个槽位从它后面开始',
        61: '行和列都找遍了没有合适槽位 → 返回 False',
    },
    skip=['m = len(board)', 'n = len(board[0])', 'continue'],
    max_steps=110,
    cards=dict(
        one_liner='老老实实按行按列找槽位，正序倒序各比一遍',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['矩阵里 `#` 是障碍，空格可填，小写字母是已填的字',
                 '单词可横放/竖放，正着或倒着，必须==恰好填满==两个障碍之间的槽位',
                 '示例：`[["#"," ","#"],[" "," ","#"],["#","c"," "]]`，`word="abc"` → `true`'],
        quote='没有想到什么特别好的做法，只能老老实实按行按列来进行匹配。……由于前面这些字符已经没有用了，题目又要求是恰好填进去，因此接下来就可以直接跳过这些字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['每行从行首跳过障碍，找到第一个非障碍格作为槽位起点',
              '从起点逐格比对 `word`，==正序、倒序==各用一个 flag',
              '匹配成功后，还要看后一格是行尾或 `#`，才算恰好填满',
              '失败就直接跳过已看过的字符，找下一个 `#` 之后的槽位；列的做法只需交换坐标'],
        summary=['时间 `O(mn)`：每个格子只被扫常数次，空间 `O(1)`',
                 '易错：匹配成功后==必须检查槽位后一格==是边界或 `#`',
                 '易错：空格 `\' \'` 与任何字母兼容，只有字母不同才算失败',
                 '行扫完再按列扫，写法相同、坐标互换',
                 '原文已是 Python 3 可运行写法，代码未改动'],
    ),
)
