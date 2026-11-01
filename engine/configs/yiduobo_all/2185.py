def _trie(S):
    root = S.get('root')
    if root is None:
        return ''
    out = []

    def dfs(node, pre):
        for ch, nx in node.childs.items():
            out.append(f'{pre + ch}({nx.w})')
            dfs(nx, pre + ch)
    dfs(root, '')
    return 'trie 节点（括号内 = 权重 w）：' + '  '.join(out) if out else ''


CONFIG = dict(
    num=2185, title='统计包含给定前缀的字符串', difficulty='Easy', category='字符串',
    author='yiduobo', technique='trie 树 · 节点带权重',
    tags=[],
    code='''
class Node(object):
    def __init__(self):
        self.w = 1
        self.childs = {}

class Solution(object):
    def prefixCount(self, words, pref):

        root = Node()
        for word in words:
            now = root
            for char in word:
                if char in now.childs:
                    now = now.childs[char]
                    now.w += 1
                else:
                    tmp = Node()
                    now.childs[char] = tmp
                    now = tmp

        now = root
        for char in pref:
            if char not in now.childs:
                return 0
            now = now.childs[char]
        
        return now.w
''',
    call='Solution().prefixCount(["at", "ate", "pa", "pat"], "at")',
    expect=2,
    views=[
        dict(type='array', var='words', label='words', cell=120, h=250, pointers={'words.index(word)': 'blue'},
             pointer_labels={'words.index(word)': 'word'}),
        dict(type='text', fn=_trie, size=26, h=130),
        dict(type='text', fn=lambda S: f"当前字符 `char = {S['char']!r}`，所在节点权重 =={S['now'].w}==" if 'char' in S and 'now' in S else '', size=28),
    ],
    watch=[('word', 'word', 'blue'), ('char', 'char', 'pink'), ('now.w', 'now.w', 'green')],
    captions={
        'root = Node()': '建一个空的根节点，作为 trie 的起点',
        'for word in words': lambda S, B, ret: (f'插入 `"{S.word}"`' if 'word' in S and S.get('word') != B.get('word') else '所有单词都插入完了'),
        11: '每次从根出发往下走',
        3: '新节点权重初始为 `w = 1`',
        4: '`childs` 是空字典，用来放子节点',
        'if char in now.childs': lambda S, B, ret: (f"已有 `'{S.char}'` 这条边 → 走过去并把权重加一" if S.char in S.now.childs
                                                    else f"没有 `'{S.char}'` 这条边 → 要新建节点"),
        'now.w += 1': '经过该节点又多一个单词：`w` → =={now.w}==（就是包含此前缀的单词数）',
        'tmp = Node()': '新建节点，权重初始为 1（当前单词经过一次）',
        'now.childs[char] = tmp': '把新节点挂到父节点的 `childs` 上',
        'now = tmp': '移到新节点继续',
        14: '沿着已有的边走到子节点',
        21: '建树完成，现在从根开始查找 `pref`',
        'if char not in now.childs': lambda S, B, ret: (f"`pref` 的字符 `'{S.char}'` 在 trie 里找不到 → 没有单词以它开头" if S.char not in S.now.childs
                                                        else f"`'{S.char}'` 存在，继续往下"),
        'return 0': '前缀走不通，答案 `0`',
        25: '沿着 `pref` 往下走一步',
        'return now.w': '走完 `pref`，该节点的权重 `{now.w}` 就是答案',
    },
    cards=dict(
        one_liner='trie 的每个节点记下“经过几次”，查前缀即得答案',
        complexity='时间 `O(总字符数)`，空间 `O(总字符数)`',
        problem=['返回 `words` 中以 `pref` 作为==前缀==的字符串数目',
                 '示例：`["pay","attention","practice","attend"]`，`pref = "at"` → `2`',
                 '本视频：`["at","ate","pa","pat"]`，`pref = "at"` → `2`'],
        quote='在常规trie树的基础上给每个节点额外设置了一个权重，表示建树时经过这个节点的次数，这个次数实际上就是数组中包含该前缀的字符串数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['建树时每经过一个节点权重加一，新节点权重为 1', '查找 `pref`：途中断了答案就是 0，否则取终点权重'],
        summary=['题目数据很小，暴力法也可以；这里用 trie 展示更通用的做法',
                 '易错：新建节点权重要初始为 1（本次也算一次经过）',
                 '`pref` 查找中途缺边要立即返回 0'],
    ),
)
