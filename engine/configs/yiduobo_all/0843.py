WL = ["acckzz", "ccbazz", "eiowzz", "abcczz"]
SETUP = '''
class Master:
    def __init__(self, secret, words):
        self.secret = secret
        self.words = words
        self.calls = 0
    def guess(self, word):
        self.calls += 1
        if word not in self.words:
            return -1
        return sum(a == b for a, b in zip(word, self.secret))
WL = ["acckzz", "ccbazz", "eiowzz", "abcczz"]
'''


def _cell(S, i, j, v):
    g = S.get('guess_index')
    if g is not None and i == g and i != j:
        return 'purple'
    return None


def _words(S):
    g = S.get('guess_index')
    cand = S.get('candidate')
    out = []
    for k, w in enumerate(WL):
        t = f'{k}:{w}'
        if k == g:
            t = f'=={t}=='
        elif cand is not None and k not in cand:
            t = f'{t}（排除）'
        out.append(t)
    return '　'.join(out)


def _info(S):
    g = S.get('guess_index')
    if 'hits' in S and g is not None:
        return f"猜 `{WL[g]}` → master 返回 =={S['hits']}==：保留与它 match 恰为 {S['hits']} 的单词"
    if g is not None:
        return f"这一轮要猜：`{WL[g]}`（与其他候选的 match 总和 ==最大=={'' if S.get('max_cnt') is None else '，' + str(S['max_cnt'])}）"
    if 'candidate' in S:
        return '幸存候选：' + '、'.join(f'`{WL[k]}`' for k in sorted(S['candidate']))
    return ''


CONFIG = dict(
    num=843, title='猜猜这个单词', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='预处理 match · 选总匹配最大的词猜',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def findSecretWord(self, wordlist, master):

        n = len(wordlist)
        candidate = set(range(n))

        match_list = [[0] * n for _ in range(n)]
        for i in range(n - 1):
            for j in range(i +1, n):
                cnt = 0
                for pos in range(6):
                    if wordlist[i][pos] == wordlist[j][pos]:
                        cnt += 1
                match_list[i][j] = cnt
                match_list[j][i] = cnt

        while True:
            guess_index = None
            max_cnt = 0
            for i in candidate:
                cnt = 0
                for j in candidate:
                    if i != j:
                        cnt += match_list[i][j]
                if cnt > max_cnt:
                    max_cnt = cnt
                    guess_index = i
            
            if guess_index is None:
                guess_index = candidate.pop()
            else:
                candidate.remove(guess_index)

            hits = master.guess(wordlist[guess_index])
            if hits == 6:
                return wordlist[guess_index]
            for i in list(candidate):
                if match_list[guess_index][i] != hits:
                    candidate.remove(i)
''',
    setup=SETUP,
    call="Solution().findSecretWord(WL, Master('abcczz', WL))",
    expect='abcczz',
    skip=['for pos in range(6)', 'if wordlist[i][pos]', 'cnt += 1', 'cnt = 0', 'if i != j', 'while True', 'for j in candidate', 'cnt += match_list', 'match_list[j][i] = cnt', 'n = len(wordlist)', 'for j in range(i'],
    max_steps=110,
    views=[
        dict(type='text', fn=_words, size=28, h=90),
        dict(type='table', var='match_list', label='match_list[i][j]：两个单词相同位置的字母数（紫 = 本轮猜的词所在行）', h=300, cell=64,
             rows=lambda S: list(range(len(S['wordlist']))), cols=lambda S: list(range(len(S['wordlist']))),
             cursors=[('i', 'j', 'yellow')], color=_cell),
        dict(type='set', var='candidate', label='candidate（还可能是答案的单词下标）', h=100),
        dict(type='text', fn=_info, size=26, h=60),
    ],
    watch=[('guess_index', 'guess_index', 'pink'), ('max_cnt', 'max_cnt', 'orange'), ('hits', 'hits', 'green'), ('猜了几次', 'master.calls', 'blue')],
    captions={
        'n = len(wordlist)': '`n = {n}` 个单词，每个都是 6 个字母',
        'candidate = set(': '一开始每个单词都有可能是答案：`candidate = {candidate}`',
        'match_list = [[0]': '`match_list[i][j]` 记录单词 i 和 j ==相同位置字母相同的个数==',
        'for i in range(n - 1)': lambda S, B, r: (f'枚举单词对 `(i, j)`，`i < j`，先固定 `i = {S.i}`（{S.wordlist[S.i]}）' if S.get('i') != B.get('i') else '所有单词对的 match 都算完了'),
        'match_list[i][j] = cnt': '`{wordlist[i]}` 与 `{wordlist[j]}` 有 `{cnt}` 个位置相同 → `match_list[{i}][{j}]` 和 `match_list[{j}][{i}]` 都记 =={cnt}==',
        'guess_index = None': '新一轮：还没选出要猜的单词',
        'for i in candidate': lambda S, B, r: (f'统计候选 `{S.i}`（{S.wordlist[S.i]}）与其他候选的 match 总和 `cnt = {S.cnt}`' if (S.get('i') != B.get('i') or (B.get('max_cnt') == 0 and B.get('cnt') != 0)) else '候选都统计完了'),
        'if cnt > max_cnt': lambda S, B, r: (f'`{S.cnt} > {S.max_cnt}` → 成立：`{S.wordlist[S.i]}` 与其他候选的 match 总和 `{S.cnt}`，暂时最大' if S.cnt > S.max_cnt else f'`{S.cnt} > {S.max_cnt}` → 不成立'),
        'max_cnt = cnt': '更新最大值：`max_cnt = {max_cnt}`',
        'guess_index = i': '`{wordlist[i]}` 成为本轮暂定要猜的词：`guess_index = {guess_index}`',
        'if guess_index is None': lambda S, B, r: ('`guess_index` 还是 None：候选之间没有任何 match，随便猜一个' if S.guess_index is None else f'选出了 `{S.guess_index}`（{S.wordlist[S.guess_index]}）：它能排除最多候选'),
        'candidate.pop()': '随便取一个候选：`guess_index = {guess_index}`',
        'candidate.remove(guess_index)': '这个词马上要猜了，先从候选中拿掉：`{candidate}`',
        'hits = master.guess': '猜 `{wordlist[guess_index]}`，master 返回 `hits = {hits}`',
        'if hits == 6': lambda S, B, r: ('`hits == 6`：6 个位置全对，就是答案' if S.hits == 6 else f'`hits = {S.hits}` ≠ 6：不是答案，用 hits 过滤候选'),
        'return wordlist': '答案是 `{ret}`，一共猜了 `{master.calls}` 次',
        'for i in list(candidate)': lambda S, B, r: (f'检查每个幸存候选 `{S.i}`：若它是答案，就必须满足 `match[guess][i] == hits`' if S.get('i') != B.get('i') else '候选都检查完了，进入下一轮'),
        'for j in range(i': lambda S, B, r: (f'取下一个 `j = {S.j}`：算 `{S.wordlist[S.i]}` 与 `{S.wordlist[S.j]}`' if (S.j != B.get('j') or B.match_list[S.i][S.j] == 0) else f'`i = {S.i}` 的配对都算完了'),
        'if match_list[guess_index][i] != hits': lambda S, B, r: (f'`match[{S.guess_index}][{S.i}] = {S.match_list[S.guess_index][S.i]}` ≠ `hits = {S.hits}` → 它不可能是答案' if S.match_list[S.guess_index][S.i] != S.hits else f'`match[{S.guess_index}][{S.i}] = {S.hits}` 与 hits 相同 → 保留'),
        'candidate.remove(i)': '剔除候选 `{i}`（{wordlist[i]}），剩 `{candidate}`',
    },
    cards=dict(
        one_liner='每次猜与其他候选 match 总和最大的词，猜完按 match 过滤',
        complexity='预处理 `O(n²·6)`，每轮选词 `O(m²)`（m 为候选数），空间 `O(n²)`',
        problem=['给定 `wordlist`（互不相同的 6 字母单词）和未知的秘密单词 `secret`',
                 '`master.guess(word)` 返回 word 与 secret ==同位置同字母的个数==',
                 '要求在 10 次猜测内猜中（返回 6）',
                 '本视频：`wordlist = [acckzz, ccbazz, eiowzz, abcczz]`，secret = `abcczz`'],
        quote='若此时的B恰好就是最终答案，那么A中所有与B匹配的字母都是正确的字母，而其他字母都是不正确的，也就是说guess(A) = match[A][B]。',
        quote_src='—— yiduobo 题解原文',
        idea=['若 B 是答案，则 `guess(A) == match[A][B]`；不相等的词一定不是答案',
              '先预处理出所有词两两的 match',
              '每轮挑与其他候选 match 总和最大的词来猜，期望排除得最多',
              '猜完用 `hits` 过滤候选，直到 `hits == 6`'],
        summary=['时间：预处理 `O(n²·6)`，每轮 `O(m²)`，空间 `O(n²)`',
                 '选词只是启发式（match 总和），不保证最优，但满足 10 次限制',
                 '候选之间 match 都为 0 时 `guess_index` 仍是 None，所以要用 `candidate.pop()` 兜底',
                 '遍历 `candidate` 时删元素会出错，所以用 `list(candidate)` 拷贝再删',
                 '原文开头的 `#class Master(object):` 接口注释已删去，Master 在 setup 中定义；原文代码未改动'],
    ),
)
