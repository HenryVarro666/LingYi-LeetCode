import views as V

BOARD = [['o', 'a', 'b'],
         ['e', 't', 'h']]
WORDS = ['oat', 'oath', 'oe']

CODE = '''
class Solution(object):
    def findWords(self, board, words):
        trie = [{}, len(words), False]
        for word in words:
            now = trie
            for char in word:
                if char not in now[0]:
                    now[0][char] = [{}, 1, False]
                else:
                    now[0][char][1] += 1
                now = now[0][char]
            now[2] = True

        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]

        res = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if trie[1] == 0:
                    return res
                if board[i][j] in trie[0] and trie[0][board[i][j]][1] > 0:
                    next_char = board[i][j]
                    board[i][j] = ' '
                    trie[1] -= self.dfs(board, i, j, trie[0][next_char], next_char, res, dx, dy)
                    board[i][j] = next_char

        return res

    def dfs(self, board, x, y, trie, now, res, dx, dy):
        cnt = 0
        if trie[2]:
            res.append(now)
            cnt = 1
            trie[2] = False

        if trie[1] > cnt:
            for index in range(4):
                next_x = x + dx[index]
                next_y = y + dy[index]
                if next_x >= 0 and next_x < len(board) and next_y >= 0 and next_y < len(board[0]):
                    next_char = board[next_x][next_y]
                    if next_char in trie[0] and trie[0][next_char][1] > 0:
                        board[next_x][next_y] = ' '
                        cnt += self.dfs(board, next_x, next_y, trie[0][next_char], now + next_char, res, dx, dy)
                        board[next_x][next_y] = next_char
            trie[1] -= cnt

        return cnt
'''
_LINES = CODE.strip('\n').split('\n')
L_END = [i + 1 for i, t in enumerate(_LINES) if 'now[2] = True' in t][0]
L_FORW = [i + 1 for i, t in enumerate(_LINES) if 'for word in words' in t][0]


def _draw_trie(cv, spec, st, box, vi, ctx):
    T = V.T
    x0, y0, x1, y1 = box
    V.label(cv, box, 'trie（橙数字 = 计数器，绿 = 单词结尾，黄圈 = DFS 路径）')
    frames = st.get('_frames', [])
    if not frames:
        return
    root = frames[0]['locals'].get('trie')
    if not isinstance(root, list):
        cv.text((x0 + 18, y0 + 44), '（尚未创建）', 24, T['dim'])
        return
    path = [fr['locals'].get('trie') for fr in frames[1:] if fr['name'] == 'dfs']
    path_ids = {id(t) for t in path if isinstance(t, list)}
    cur = path[-1] if path else None
    line = st['_S'].get('_line')
    if not path and line in (L_END, L_FORW):
        nw = frames[0]['locals'].get('now')
        cur = nw if isinstance(nw, list) else None
    # layout: x by leaf order
    nodes, leaves = [], [0]

    def walk(nd, ch, pre, d):
        kids = list(nd[0].items())
        rec = dict(nd=nd, ch=ch, pre=pre, d=d)
        nodes.append(rec)
        if not kids:
            rec['x'] = leaves[0]
            leaves[0] += 1
        else:
            xs = [walk(k, c, pre + c, d + 1)['x'] for c, k in kids]
            rec['x'] = (xs[0] + xs[-1]) / 2
        rec['kids'] = [id(k) for _, k in kids]
        return rec
    walk(root, '根', '', 0)
    nl = max(1, leaves[0])
    maxd = max(r['d'] for r in nodes) + 1
    sp = min(150, (x1 - x0 - 80) / nl)
    dy = min(92, (y1 - y0 - 80) / max(1, maxd))
    sx = x0 + 40 + ((x1 - x0 - 80) - sp * nl) / 2 + sp / 2
    pos = {id(r['nd']): (sx + r['x'] * sp, y0 + 66 + r['d'] * dy) for r in nodes}
    rad = min(24, dy * 0.38)
    for r in nodes:
        X, Y = pos[id(r['nd'])]
        for k in r['kids']:
            X2, Y2 = pos[k]
            cv.line([(X, Y), (X2, Y2)], T['border'], 3)
    for r in nodes:
        nd = r['nd']
        X, Y = pos[id(nd)]
        is_word = r['pre'] in WORDS
        fill = T['panel2']
        tc = T['text']
        if nd[2]:
            fill, tc = T['green'], T['bg']
        elif nd[1] == 0:
            fill, tc = (40, 45, 53), T['dim']
        oc, w = T['border'], 2
        if id(nd) in path_ids:
            oc, w = T['yellow'], 4
        if cur is not None and nd is cur:
            oc, w = T['pink'], 5
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=oc, width=w)
        cv.text((X, Y), r['ch'], 24 if r['d'] else 18, tc, anchor='mm', bold=True)
        cv.text((X + rad + 2, Y + rad - 4), nd[1], 21, T['orange'] if nd[1] else T['dim'], anchor='lm', bold=True, mono=True)
        if is_word and not nd[2]:
            cv.text((X - rad - 6, Y), '已找到', 18, T['green'], anchor='rm', bold=True)


V.VIEWS.setdefault('trie_0212', (_draw_trie, lambda spec: spec.get('h', 330)))


def _cmp_main(S, B, ret):
    c = B.board[B.i][B.j]
    kids = B.trie[0]
    if c in kids and kids[c][1] > 0:
        return f"`board[{B.i}][{B.j}] = '{c}'`：根下有 '{c}' 且计数 {kids[c][1]} > 0 → 从这里开始搜"
    return f"`board[{B.i}][{B.j}] = '{c}'`：没有以 '{c}' 开头的待找单词 → 跳过"


def _cmp_next(S, B, ret):
    nx, ny, c = B.next_x, B.next_y, B.next_char
    kids = B.trie[0]
    if c == ' ':
        return f'邻居 `({nx},{ny})` 已经在当前路径上（空格）→ 不能重复用'
    if c not in kids:
        return f"邻居 `({nx},{ny}) = '{c}'`：trie 里没有前缀 \"{B.now + c}\" → 剪掉"
    if kids[c][1] == 0:
        return f"邻居 `({nx},{ny}) = '{c}'`：\"{B.now + c}\" 的计数器为 0，单词已全部找到 → 剪掉"
    return f"邻居 `({nx},{ny}) = '{c}'`：\"{B.now + c}\" 计数 {kids[c][1]} > 0 → ==往下搜=="


def _need(S, B, ret):
    if B.trie[1] > B.cnt:
        return f'计数器 `{B.trie[1]} > cnt = {B.cnt}`：以 "{B.now}" 为前缀的单词还没找全 → 继续搜邻居'
    return f'计数器 `{B.trie[1]} = cnt = {B.cnt}`：以 "{B.now}" 为前缀的单词==全找到了== → 不用再往下搜'


CONFIG = dict(
    num=212, title='单词搜索 II', difficulty='Hard', category='回溯',
    author='yiduobo', technique='Trie（带计数器剪枝）+ 回溯',
    tags=['面试经典150'],
    code=CODE,
    call=f'Solution().findWords({BOARD}, {WORDS})',
    expect=['oe', 'oat', 'oath'],
    skip=['now = trie', 'for char in word', 'if char not in now[0]', 'now[0][char] = [', 'else:', 'now[0][char][1] += 1',
          'now = now[0][char]', 'dx = [', 'dy = [', 'next_x = x', 'next_y = y', 'if next_x >= 0',
          'next_char = board[next_x]', 'for index in range(4)', "board[next_x][next_y] = ' '", 'cnt = 1',
          'next_char = board[i][j]', 'for i in range', "board[i][j] = ' '"],
    max_steps=80,
    views=[
        dict(type='trie_0212', h=360),
        dict(type='grid', var=lambda S: BOARD, label='board（黄 = 当前路径已用，蓝框 = 起点，粉框 = 当前）', cell=52, h=150,
             color=lambda S, i, j, v: 'yellow' if 'board' in S and S['board'][i][j] == ' ' else None,
             cursors=[('i', 'j', 'blue'), ('x', 'y', 'pink')]),
        dict(type='calls', h=150, hide=('board', 'trie', 'res', 'dx', 'dy', 'self')),
    ],
    watch=[('cnt', 'cnt', 'pink'), ('res', 'res', 'green')],
    captions={
        'trie = [': '节点 = `[孩子, 计数器, 是否结尾]`；根的计数器 = 单词数 `{len(words)}`',
        'for word in words': lambda S, B, r: (f'插入 "{S.word}"：路径上==每个节点计数器 +1==（新建的节点计数为 1）'
                                              if S.get('word') != B.get('word') else 'trie 建好了'),
        'now[2] = True': '"{word}" 插入完毕：结尾节点标记为单词结尾',
        'res = []': '开始在 board 上搜索；计数器 = 以这个前缀开头、==还没找到==的单词数',
        'for j in range': lambda S, B, r: f'起点 `({S.i},{S.j})`',
        'if trie[1] == 0': lambda S, B, r: ('根计数器为 0：==所有单词都找到了== → 直接返回' if B.trie[1] == 0
                                            else f'根计数器 = {B.trie[1]}：还有单词没找到'),
        'if board[i][j] in trie[0]': _cmp_main,
        'trie[1] -= self.dfs': lambda S, B, r: f"格子改成空格（==标记已访问==），从 `({B.i},{B.j})` 出发 DFS；找到几个单词，根计数器就减几",
        'board[i][j] = next_char': '回溯：恢复 `board[{i}][{j}]`；根计数器剩 `{trie[1]}`',
        'cnt = 0': '进入 `({x},{y})`，前缀 "{now}"；`cnt` 记录这棵子树找到的单词数',
        'if trie[2]': lambda S, B, r: (f'"{B.now}" 是单词结尾 → ==找到一个==！' if B.trie[2] else f'"{B.now}" 还不是完整单词'),
        'res.append(now)': '加入答案：`res = {res}`',
        'trie[2] = False': '清掉结尾标记：同一个单词==不会被找两次==',
        'if trie[1] > cnt': _need,
        'if next_char in trie[0]': _cmp_next,
        'cnt += self.dfs': lambda S, B, r: f'递归进入 `({B.next_x},{B.next_y})`，前缀 "{B.now + B.next_char}"',
        'board[next_x][next_y] = next_char': '子树返回，`cnt = {cnt}`；恢复 `({next_x},{next_y})`，回溯',
        'trie[1] -= cnt': '计数器减去找到的 `{cnt}` 个 → `{trie[1]}`：这些单词以后不用再搜',
        'return cnt': '`({x},{y})` 搜完，返回找到 =={ret}== 个单词',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='把所有单词放进 trie，节点计数器 = 还没找到的单词数，为 0 就剪枝',
        complexity='最坏 `O(mn · 4·3^(L-1))`，trie 空间 `O(Σ|word|)`',
        problem=['给定 `m × n` 字符网格 `board` 和单词列表 `words`，返回所有能在网格中找到的单词',
                 '单词由==相邻==（上下左右）格子的字母组成，==同一格==在一个单词里不能重复用',
                 '示例：4×4 网格 + 4 个单词 → `["eat","oath"]`',
                 '本视频：2×3 网格 `oab / eth`，`["oat","oath","oe"]`'],
        quote='额外添加一个计数器，表示从根节点到这个叶子节点形成的前缀是几个单词的公共前缀，那么在之后的搜索过程中，==若当前节点的计数器大于0，说明有继续往下搜索的必要==，否则就可以直接进行回溯了。',
        quote_src='—— yiduobo 题解原文',
        idea=['79 题的升级版：多个单词共享前缀 → 用 trie，一次 DFS 同时搜所有单词',
              '建树：每走过一个节点，计数器 +1',
              '搜完一个孩子，计数器减去它找到的单词数；为 0 说明这个前缀==全找到了=='],
        summary=['剪枝 1：邻居字母不在当前节点的孩子里，或孩子计数为 0 → 不走',
                 '剪枝 2：`trie[1] == cnt` 时这个前缀下的单词已全找到，不再搜邻居',
                 '找到单词后 `trie[2] = False`，避免重复加入答案',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
