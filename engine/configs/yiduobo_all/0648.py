def _trie(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'Trie（绿 = 单词结尾 end_flag，黄 = 当前节点 now）', 24, T['muted'], bold=True)
    root = S.get('trie')
    if root is None or not hasattr(root, 'next_dict'):
        return
    cur = S.get('now')

    def leaves(n):
        return max(1, sum(leaves(c) for c in n.next_dict.values())) if n.next_dict else 1
    total = leaves(root)
    unit = min(120, (x1 - x0 - 60) / total)
    pos = {}

    def place(n, lo, depth):
        w = leaves(n) * unit
        pos[id(n)] = (x0 + 30 + lo + w / 2, y0 + 110 + depth * 70)
        off = lo
        for c in n.next_dict.values():
            place(c, off, depth + 1)
            off += leaves(c) * unit
    place(root, 0, 0)
    nodes = []

    def draw(n):
        x, y = pos[id(n)]
        nodes.append(n)
        for ch, c in n.next_dict.items():
            cx, cy = pos[id(c)]
            cv.line([(x, y), (cx, cy)], T['muted'], 2)
            cv.text(((x + cx) / 2 + 10, (y + cy) / 2), ch, 22, T['cyan'], anchor='lm', bold=True)
            draw(c)
    draw(root)
    for n in nodes:
        x, y = pos[id(n)]
        is_cur = cur is not None and n is cur
        fill = T['yellow'] if is_cur else (T['green'] if n.end_flag else T['border'])
        cv.rect((x - 16, y - 16, x + 16, y + 16), fill=fill, r=16,
                outline=T['yellow'] if is_cur else T['muted'], width=2)
    cv.text((pos[id(root)][0] - 30, pos[id(root)][1]), 'root', 20, T['dim'], anchor='rm')


CONFIG = dict(
    num=648, title='单词替换', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='Trie 树 · 找最短词根',
    tags=[],
    code='''
class Node(object):

    def __init__(self):
        self.end_flag = False
        self.next_dict = {}

class Solution(object):
    def replaceWords(self, dictionary, sentence):

        trie = Node()
        for word in sorted(dictionary, key=lambda d:len(d)):
            now = trie
            for char in word:
                if char not in now.next_dict:
                    tmp = Node()
                    now.next_dict[char] = tmp
                
                now = now.next_dict[char]
                if now.end_flag:
                    break
            
            now.end_flag = True

        res = []
        for word in sentence.split(' '):
            now = trie
            flag = False
            for index, char in enumerate(word):
                if char not in now.next_dict:
                    break
                now = now.next_dict[char]
                if now.end_flag:
                    res.append(word[:index + 1])
                    flag = True
                    break
            
            if not flag:
                res.append(word)

        return ' '.join(res)
''',
    call='Solution().replaceWords(["cat", "ca", "rat"], "the cattle was rattled")',
    expect='the ca was rat',
    views=[
        dict(type='custom', draw=_trie, h=380),
        dict(type='array', var='res', label='res（已处理的单词）', h=120),
    ],
    skip=['tmp = Node()', 'flag = False', 'res = []', 5, 12, 16, 20, 30, 34, 35],
    max_steps=100,
    watch=[('word', 'word', 'orange'), ('char', 'char', 'cyan'), ('flag', 'flag', 'green')],
    captions={
        'trie = Node()': '建一棵空 Trie：每个节点有 `end_flag`（是否是某个词根的结尾）和 `next_dict`（孩子）',
        'for word in sorted(dictionary': lambda S, B, r: '所有词根都插入完了' if B.get('word') == S.word else f'词根按长度从短到长处理（`{S.dictionary}` 排序后），现在插入 `{S.word}`',
        'now = trie': '从根开始往下走',
        'for char in word': lambda S, B, r: '这个词的字符都处理完了' if B.get('char') == S.char else f'看字符 `{S.char}`',
        14: lambda S, B, r: f'`{S.char}` 在当前节点的孩子里吗？' + ('不在 → 新建一个节点，挂在它下面（`now.next_dict[char]`）' if S.char not in S.now.next_dict else '在 → 沿着已有的路走'),
        18: '走到孩子 `{char}`',
        31: '走到孩子 `{char}`',
        19: lambda S, B, r: ('当前节点已是某个词根的结尾 → 更短的词根已存在，==当前词不用再往下建==，break' if S.now.end_flag else '当前节点还不是词根结尾，继续'),
        32: lambda S, B, r: ('当前节点是词根结尾 → 找到最短词根，准备替换' if S.now.end_flag else '还不是词根结尾，继续往下走'),
        'now.end_flag = True': lambda S, B, r: ('这个节点本来就是结尾（更短的词根），`' + S.word + '` 被它覆盖，没有新增节点' if B.now.end_flag else f'给 `{S.word}` 的末尾节点打上结束标记（绿色）'),
        'for word in sentence.split': lambda S, B, r: '句子里的单词都处理完了' if B.get('word') == S.word else f'处理句子里的单词 `{S.word}`：看它有没有词根前缀',
        'for index, char in enumerate(word)': '逐字符走 Trie：`{char}`',
        29: lambda S, B, r: f'`{S.char}` 在当前节点的孩子里吗？' + ('不在 → 没有词根是它的前缀，停止' if S.char not in S.now.next_dict else '在 → 继续往下走'),
        'res.append(word[:index + 1])': '走到词根结尾：用最短词根 `{word[:index + 1]}` 替换整个单词，`flag = True`',
        'if not flag': lambda S, B, r: ('`flag` 是 False：没命中任何词根 → 保留原单词' if not S.flag else '`flag` 为 True：已经替换过了'),
        'res.append(word)': '原样保留 `{word}`',
        "return ' '.join(res)": '用空格拼回句子：`{ret}`',
    },
    cards=dict(
        one_liner='词根建成 Trie，单词走到第一个结尾标记，就是最短前缀',
        complexity='时间 `O(Σ词根长度 + 句子长度)`，空间 `O(Σ词根长度)`',
        problem=['给词根字典和句子，句子里每个单词若有词根作前缀，就用==最短的词根==替换它',
                 '没有词根前缀的单词保持不变，返回新句子',
                 '本视频：词根 `cat, ca, rat`，句子 `the cattle was rattled` → `the ca was rat`'],
        quote='看到前缀和字典，很自然就想到了使用trie树来解决。',
        quote_src='—— yiduobo 题解原文',
        idea=['用词根建 Trie；建树前按长度排序，短的先建',
              '建树时碰到已有结束标记，说明当前词的前缀已是词根，不用再处理',
              '查单词时一路往下走，第一次遇到结束标记就是最短词根'],
        summary=['原文为 Python 2 写法，`split(sentence, \' \')` 已改为 `sentence.split(\' \')`',
                 '时间 `O(Σ词根长度 + 句子长度)`，空间 `O(Σ词根长度)`',
                 '`flag` 记录有没有命中词根；没命中要把原单词放回 `res`',
                 '先排序再建树，保证先走到的结束标记就是最短词根'],
    ),
)
