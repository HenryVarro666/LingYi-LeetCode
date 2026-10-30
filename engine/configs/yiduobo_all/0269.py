WORDS = ['wrt', 'wrf', 'er', 'ett', 'rftt']


def _pair(S):
    if 'i' not in S or 'words' not in S or S['i'] >= len(S['words']):
        return '相邻两个单词的首个不同字符，给出字符先后顺序'
    w = S['words']
    return f"比较 `{w[S['i'] - 1]}` 与 `{w[S['i']]}`"


CONFIG = dict(
    num=269, title='火星词典', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='相邻单词建图 + 拓扑排序',
    tags=['灵神题单', '拓扑排序'],
    code='''
class Solution(object):
    def alienOrder(self, words):

        ind = {}
        g = {}

        for word in words:
            for char in word:
                if char not in ind:
                    ind[char] = 0
                if char not in g:
                    g[char] = set()

        for i in range(1, len(words)):
            flag = True
            for j in range(min(len(words[i - 1]), len(words[i]))):
                if words[i][j] != words[i - 1][j]:
                    flag = False
                    x, y = words[i - 1][j], words[i][j]
                    if y not in g[x]:
                        g[x].add(y)
                        ind[y] += 1
                    break
            
            if flag and len(words[i - 1]) > len(words[i]):
                return ""
        
        q = []
        for char in ind:
            if ind[char] == 0:
                q.append(char)
        
        head, tail = 0, len(q)
        while head < tail:
            now = q[head]
            head += 1
            for next in g[now]:
                ind[next] -= 1
                if ind[next] == 0:
                    q.append(next)
                    tail += 1
        
        if len(q) == len(ind):
            return "".join(q)
        
        return ""
''',
    call=f'Solution().alienOrder({WORDS})',
    expect='wertf',
    views=[
        dict(type='array', var='words', label='words（已按火星字典序排好）', cell=130, h=215, pointers={'i': 'blue'}),
        dict(type='map', var='g', label='g（x → 必须排在 x 后面的字符）', fmt=lambda k, v: f"{k} → {''.join(sorted(v)) or '∅'}", h=130, font=28),
        dict(type='map', var='ind', label='ind（入度）', fmt=lambda k, v: f"{k}: {v}", h=130, font=30),
        dict(type='array', var='q', label='q（拓扑序，head 指向当前处理的字符）', cell=90, h=200, pointers={'head': 'pink'}),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'cyan'), ('head', 'head', 'pink'), ('tail', 'tail', 'orange')],
    skip=['if char not in', 'ind[char] = 0', 'g[char] = set()', 'flag = True', 'for word in words', 'for char in word', 'flag = False', 'head += 1', 'tail += 1'],
    max_steps=110,
    captions={
        'ind = {}': '`ind` 记每个字符的入度，`g` 记「谁排在谁前面」的边',
        'for i in range(1, len(words))': lambda S, B, r: ('所有相邻单词都比较完了' if B.get('i') == S.i and 'j' in B else f'比较第 {S.i - 1} 个与第 {S.i} 个单词：`{S.words[S.i - 1]}` 和 `{S.words[S.i]}`'),
        'for j in range': lambda S, B, r: f'逐位对比，找首个不同的字符：`j = {S.j}`',
        'if words[i][j] != words[i - 1][j]': lambda S, B, r: (
            f"`{S.words[S.i][S.j]}` ≠ `{S.words[S.i - 1][S.j]}` → ==首个不同字符==，决定顺序" if S.words[S.i][S.j] != S.words[S.i - 1][S.j]
            else f"`{S.words[S.i][S.j]}` = `{S.words[S.i - 1][S.j]}` → 相同，看下一位"),
        'x, y =': '前一个单词的 `{x}` 一定排在后一个单词的 `{y}` 前面：边 `{x} → {y}`',
        'if y not in g[x]': lambda S, B, r: (f'边 `{S.x} → {S.y}` 还没有' if S.y not in S.g[S.x] else f'边 `{S.x} → {S.y}` 已有，不能重复加入度'),
        'g[x].add(y)': '加边 `{x} → {y}`',
        'ind[y] += 1': '`{y}` 入度 +1 → {ind[y]}',
        'break': '只有首个不同字符有用，后面的位不再比较',
        'if flag and len': lambda S, B, r: (f'没找到不同字符，且前一个更长 → 矛盾，返回空串' if S.flag and len(S.words[S.i - 1]) > len(S.words[S.i])
                                           else '没有矛盾，继续下一对'),
        'q = []': '建图完成：先把所有入度为 0 的字符放进队列',
        'if ind[char] == 0': lambda S, B, r: f"`{S.char}` 入度 {S.ind[S.char]}" + ('，==没有前驱== → 入队' if S.ind[S.char] == 0 else '，有前驱 → 先不入队'),
        'q.append(char)': '`{char}` 入队：`q` = {q}',
        'head, tail = 0, len(q)': '`head` 指向当前处理的位置，`tail` 是队尾',
        'while head < tail': lambda S, B, r: ('队列里还有字符，继续' if S.head < S.tail else '队列处理完毕'),
        'now = q[head]': '取出 `{now}`：它前面的字符都已确定，可以放到答案里',
        'for next in g[now]': lambda S, B, r: (f'`{S.now}` 没有后继了' if not S.g[S.now] else f'`{S.now}` 的后继：`{S.next}`'),
        'ind[next] -= 1': '去掉边 `{now} → {next}`：`{next}` 入度变为 {ind[next]}',
        'if ind[next] == 0': lambda S, B, r: (f'`{S.next}` 入度为 0 → 前驱都已排好，入队' if S.ind[S.next] == 0 else f'`{S.next}` 还有 {S.ind[S.next]} 个前驱未处理'),
        'q.append(next)': '`{next}` 入队：`q` = {q}',
        'if len(q) == len(ind)': lambda S, B, r: (f'排出 {len(S.q)} 个，共 {len(S.ind)} 个字符 → 没有环，顺序合法' if len(S.q) == len(S.ind)
                                                 else f'只排出 {len(S.q)} 个，共 {len(S.ind)} 个 → 有环'),
        'return "".join(q)': '返回拓扑序 =={"".join(q)}==',
    },
    cards=dict(
        one_liner='相邻单词的首个不同字符给出边，拓扑排序出字母表',
        complexity='时间 `O(C + 26)`，C 为所有单词总长；空间 `O(26)`',
        problem=['外星语言用拉丁字母，但字母顺序未知；给一组已按其字典序排好的单词',
                 '推出字母顺序；无法成立（有环/前缀矛盾）返回空串',
                 '示例：`["wrt","wrf","er","ett","rftt"]` → `"wertf"`'],
        quote='遍历所有单词，对于当前单词与其上一个单词，再遍历这两个单词中相同下标的所有字符并找出首个不相同的字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['相邻两词的首个不同字符 `x, y`：建边 `x → y`，`y` 入度 +1',
              '没有不同字符但前词更长（如 `abc` 在 `ab` 前）→ 矛盾，返回空串',
              '入度为 0 的先入队做拓扑；队列长度等于字符数才无环'],
        summary=['同一对 `x → y` 只能加一次，所以先判断 `y not in g[x]`',
                 '`ind` 要收录所有出现过的字符，包括没有边的孤立字符',
                 '前缀矛盾：`["abc","ab"]` 必须返回空串',
                 '队列长度 ≠ 字符数说明有环',
                 '原文已是 Python 3 可运行写法，无需修改（类型注释无）'],
    ),
)
