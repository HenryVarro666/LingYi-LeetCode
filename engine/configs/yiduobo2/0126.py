_IDX = "index if 'now' in vars() and 'res' not in vars() else None"


def _phase(S):
    if 'res' in S:
        return '③ 从 `endWord` 沿着 `fa` ==倒推==，生成所有最短路径'
    if 'q' in S:
        if 'left' in S and 'right' in S:
            return f"② 分层 BFS：`q[{S['left']}:{S['right']}]` 是当前这一层（框出的部分）"
        return '② 分层 BFS：记录每个词的最少步数和「上一个词」'
    if 'leak_dict' in S:
        return '① 建图：挖掉一个字母得到 key，同一个 key 下的词互相连边'
    return '先把 `beginWord` 放进词表；`endWord` 不在词表里就无解'


def _famap(S):
    if 'fa' not in S:
        return None
    lv = S.get('level_dict') or {}
    return {w: (lv.get(w), f) for w, f in S['fa'].items()}


def _fafmt(k, v):
    lv, f = v
    a = f'第{lv}层' if isinstance(lv, int) and lv >= 0 else '未到达'
    b = ','.join(f) if f else '·'
    return f'{k}: {a} ← {b}'


def _cap_if_fa(S, B, ret):
    w, now = S.next_word, S.now
    if B.fa[w] is None:
        extra = '（==起点没设上一个词==，所以会被再次入队）' if w == S.beginWord else '，这就是到它的最少步数'
        return f'`{now}` 的邻居 `{w}`：`fa[{w}]` 是 None → ==第一次被到达=={extra}'
    return f'`{now}` 的邻居 `{w}`：之前已被到达（`fa[{w}] = {B.fa[w]}`）→ 看看是不是同样的最少步数'


def _cap_fa_new(S, B, ret):
    w, now = S.next_word, S.now
    s = f'`{w}` 入队，层数 `{B.level_dict[now] + 1}`，上一个词 `fa[{w}] = [{now}]`'
    if w == S.beginWord:
        s += '；起点被当成第 2 层的词，==不在任何最短路上，不影响答案=='
    return s


def _cap_elif(S, B, ret):
    w, now = S.next_word, S.now
    a, b = B.level_dict[w], B.level_dict[now] + 1
    if a == b:
        return f'`level[{w}] = {a}` == `level[{now}] + 1`：经过 `{now}` 也是最少步数 → ==多记一个上一个词=='
    return f'`level[{w}] = {a}` ≠ `level[{now}] + 1 = {b}`：绕远了，不记'


CONFIG = dict(
    num=126, title='单词接龙 II', difficulty='Hard', category='图论',
    author='yiduobo', technique='挖空建图 + 分层 BFS 记录所有父节点',
    tags=['字节30天'],
    code='''
class Solution(object):
    def findLadders(self, beginWord, endWord, wordList):
        if beginWord not in wordList:
            wordList.append(beginWord)
        if endWord not in wordList:
            return []

        wordNum = len(wordList)
        wordLen = len(wordList[0])
        g = {word : [] for word in wordList}

        leak_dict = {}
        for word in wordList:
            for index in range(wordLen):
                key = word[:index] + '_' + word[index + 1:]
                if key not in leak_dict:
                    leak_dict[key] = []
                leak_dict[key].append(word)

        for key in leak_dict:
            leak_len = len(leak_dict[key])
            for i in range(leak_len - 1):
                for j in range(i + 1, leak_len):
                    g[leak_dict[key][i]].append(leak_dict[key][j])
                    g[leak_dict[key][j]].append(leak_dict[key][i])

        q = [beginWord]
        fa = {word : None for word in wordList}
        left = 0
        right = 1
        level_dict = {word : -1 for word in wordList}
        level_dict[beginWord] = 0
        while left < right:
            new_right = right
            for index in range(left, right):
                now = q[index]
                for next_word in g[now]:
                    if fa[next_word] is None:
                        q.append(next_word)
                        fa[next_word] = [now]
                        new_right += 1
                        level_dict[next_word] = level_dict[now] + 1
                    elif level_dict[next_word] == level_dict[now] + 1:
                        fa[next_word].append(now)
            if fa[endWord] is not None:
                break
            left = right
            right = new_right

        if fa[endWord] is None:
            return []

        res = [[endWord]]
        for index in range(level_dict[endWord]):
            res = [[y] + x for x in res for y in fa[x[0]]]

        return res
''',
    call="Solution().findLadders('ab', 'cd', ['ad', 'cb', 'cd'])",
    expect=[['ab', 'ad', 'cd'], ['ab', 'cb', 'cd']],
    views=[
        dict(type='text', fn=_phase, size=26, h=52),
        dict(type='map', var='leak_dict', label='leak_dict（挖空后的 key → 词）', h=96,
             fmt=lambda k, v: f"{k}: {','.join(v)}"),
        dict(type='map', var='g', label='g（邻接表：只差一个字母的词）', h=96,
             fmt=lambda k, v: f"{k}→{','.join(v) if v else '·'}"),
        dict(type='array', var='q', label='q（BFS 队列，框 = 当前层）', cell=72,
             window=('left', 'right - 1'), pointers={_IDX: 'yellow'}, pointer_labels={_IDX: 'now'}),
        dict(type='map', var=_famap, label='每个词：最少步数（层）← 上一个词 fa', h=96, fmt=_fafmt),
        dict(type='stack', var='res', label='res（倒推出的路径）', h=100, fmt=lambda x: '→'.join(x)),
    ],
    watch=[('now', 'now', 'yellow'), ('next_word', 'next_word', 'cyan'), ('left', 'left', 'blue'),
           ('right', 'right', 'pink'), ('new_right', 'new_right')],
    captions={
        'if beginWord not in wordList': '`{beginWord}` 不在词表里',
        'wordList.append(beginWord)': '起点 `{beginWord}` 不在词表里 → 加进去，它也是图中的一个点',
        'if endWord not in wordList': lambda S, B, ret: ('终点 `' + S.endWord + '` 在词表里 → 有可能变过去'
                                                         if S.endWord in S.wordList else '终点不在词表 → 无解'),
        'g = {word : []': '`g`：图的邻接表，每个词是一个点（`wordNum`、`wordLen` 记下词数和词长）',
        'leak_dict = {}': '`leak_dict`：把词==挖掉一个字母==，剩下的部分当 key',
        'leak_dict[key].append(word)': '`{word}` 挖掉第 {index} 个字母 → key `{key}`：`leak_dict[{key}] = {leak_dict[key]}`',
        'g[leak_dict[key][i]].append': lambda S, B, ret: (
            f'`{S.leak_dict[S.key][S.i]}` 和 `{S.leak_dict[S.key][S.j]}` 都能变成 `{S.key}` → '
            f'==只差一个字母==，两两连边'),
        'q = [beginWord]': '从起点 `{beginWord}` 开始 BFS',
        'fa = {word : None': '`fa[w]`：以最少步数到达 w 时，==上一个词有哪些==（可能不止一个）',
        'level_dict[beginWord] = 0': '`level_dict[w]`：到达 w 的最少步数，起点是 0',
        'while left < right': lambda S, B, ret: (f'`q[{B.left}:{B.right}]` 不为空 → 处理这一层' if B.left < B.right
                                                 else '队列空了 → 结束'),
        'new_right = right': '`new_right` 记录下一层的右边界：新入队的词都在下一层',
        'now = q[index]': '取出这一层的 `{now}`（第 `{level_dict[now]}` 层），枚举它的邻居 `g[{now}] = {g[now]}`',
        'if fa[next_word] is None': _cap_if_fa,
        'level_dict[next_word] = level': _cap_fa_new,
        'elif level_dict[next_word]': _cap_elif,
        'fa[next_word].append(now)': '`fa[{next_word}] = {fa[next_word]}`：两条最短路在这里汇合',
        'if fa[endWord] is not None': lambda S, B, ret: (
            f'终点 `{S.endWord}` 已经被到达：这一层处理完，所有最短路的「上一个词」都记全了 → 停止 BFS'
            if S.fa[S.endWord] is not None else f'终点还没到 → 进入下一层'),
        'break': '跳出 BFS',
        'left = right': '下一层：`q[{left}:{new_right}]`',
        'res = [[endWord]]': '从终点出发倒推：`res = [[{endWord}]]`，需要倒推 `level_dict[{endWord}] = {level_dict[endWord]}` 步',
        'res = [[y] + x': lambda S, B, ret: (
            f'倒推第 {S.index + 1} 步：每条路径 x 前面拼上 `fa[x[0]]` 里的每个词 → '
            + '、'.join('`' + '→'.join(p) + '`' for p in S.res)),
        'return res': '得到所有最短转换序列：==共 {len(ret)} 条==',
    },
    skip=['if beginWord not in wordList', '                break', 'wordNum = len', 'wordLen = len',
          'for word in wordList:', 'for next_word in g[now]', 'for index in range(wordLen)', 'key = word[:index]',
          'if key not in leak_dict', 'leak_dict[key] = []', 'for key in leak_dict', 'leak_len =',
          'for i in range(leak_len', 'for j in range(i + 1', 'g[leak_dict[key][j]]', 'left = 0', 'right = 1',
          'level_dict = {word : -1', 'q.append(next_word)', 'new_right += 1', 'fa[next_word] = [now]',
          'right = new_right', 'for index in range(left, right)', 'for index in range(level_dict',
          'if fa[endWord] is None'],
    max_steps=60,
    cards=dict(
        one_liner='挖空一个字母建图，分层 BFS 记下所有「上一个词」，再从终点倒推',
        complexity='建图 `O(N·L²)`，BFS `O(边数)`，输出与路径数成正比',
        problem=['每次只能改一个字母，且中间词必须在 `wordList` 里',
                 '返回从 `beginWord` 到 `endWord` 的==所有最短==转换序列；不存在返回 `[]`',
                 "示例：`hit → cog`，词表 `[hot,dot,dog,lot,log,cog]` → 2 条",
                 "本视频：`ab → cd`，词表 `[ad,cb,cd]` → `ab→ad→cd`、`ab→cb→cd`"],
        quote='逐个枚举每个词，并得到其==删去一个字符后剩下的部分，作为key==保存起来。……==只有是通过最少的操作数达到某个词时才会将上一个词记录下来==。',
        quote_src='—— yiduobo 题解原文（126 & 127 合写）',
        idea=['`hit` 和 `hot` 都能形成 `h_t` → 同一个 key 下的词只差一个字母，两两连边',
              '分层 BFS：第一次到达某词时记下步数和上一个词；==同样步数再次到达==，上一个词再多记一个',
              '终点所在层处理完就停；从终点沿 `fa` 倒推，用列表生成式展开所有路径'],
        result='两条最短路径：`ab→ad→cd`、`ab→cb→cd` ✓',
        summary=['关键：`fa` 存==列表==，只在 `level[next] == level[now] + 1` 时追加，保证只记最短路',
                 '起点的 `fa` 也是 None，会被再次入队（层数记成 2）；它不在最短路上，不影响答案',
                 '易错：要把这一层处理完再判断终点，否则会漏掉同层的其他上一个词',
                 '127 题只要最短步数：同一张图直接 BFS；原文为 Python 2 写法，只删去了文档字符串'],
    ),
)
