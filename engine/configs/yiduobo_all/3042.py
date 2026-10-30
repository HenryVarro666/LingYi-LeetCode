def _flat(S):
    root = S.get('root')
    out = {}
    if root is None:
        return out

    def go(node, path):
        for k, ch in node.childs.items():
            p = path + [f'{k[0]}{k[1]}']
            out['→'.join(p)] = ch.weight
            go(ch, p)
    go(root, [])
    return out


def _top(S):
    if 'w' not in S:
        return '把 `w` 的第 i 个字符和倒数第 i 个字符配成一对，当作 trie 的一条边'
    w = S['w']
    pairs = ' '.join(f'({w[i]},{w[-i - 1]})' for i in range(len(w)))
    return f"`{w}` 的字符对序列：{pairs}"


CONFIG = dict(
    num=3042, title='统计前后缀下标对 I', difficulty='Easy', category='字符串',
    author='yiduobo', technique='前后缀字符对 trie',
    tags=[],
    code='''
class Node():
    def __init__(self):
        self.childs = {}
        self.weight = 0

class Solution(object):
    def countPrefixSuffixPairs(self, words):

        root = Node()
        res = 0
        for w in words[::-1]:
            now = root
            for index in range(len(w)):
                key = (w[index], w[-index - 1])
                if key not in now.childs:
                    now.childs[key] = Node()
                now = now.childs[key]
                now.weight += 1
            
            res += now.weight - 1
        
        return res
''',
    call='Solution().countPrefixSuffixPairs(["a", "aba", "aa"])',
    expect=2,
    skip=['self.childs', 'self.weight = 0'],
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='array', var='words[::-1]', label='words 从后往前遍历（蓝 = 当前 w）', cell=90, index=False, h=200,
             color=lambda S, k, v: 'blue' if S.get('w') == v else None),
        dict(type='map', var=_flat, label='trie：路径（字符对 前缀字符+后缀字符）→ 权重', h=260, font=26),
    ],
    watch=[('w', 'w', 'blue'), ('index', 'index'), ('key', 'key', 'pink'), ('res', 'res', 'green')],
    captions={
        'root = Node': '建一棵空 trie：每条边是==(前缀字符, 后缀字符)==一对，节点权重 = 经过它的字符串个数',
        'res = 0': '`res` 统计满足条件的下标对数量',
        'for w in words': '从后往前取字符串 `w = {w!r}`：它的前面已经插入了==后面的字符串==',
        'now = root': '每个字符串都从根出发',
        'for index in range': '`index = {index}`：配对 `w[{index}] = {w[index]!r}` 与 `w[-{index+1}] = {w[-index-1]!r}`',
        'key = (': '字符对 `key = {key}`：前缀第 {index+1} 位 + 后缀倒数第 {index+1} 位，一起比',
        'if key not in': lambda S, B, ret: (f"`{S.key}` 不在当前节点的孩子里 → 需要新建" if S.key not in S.now.childs
                                            else f"`{S.key}` 已存在 → 说明以前有字符串同样的前后缀对"),
        'now.childs[key] = Node': '新建孩子节点',
        'now = now.childs[key]': '走到孩子节点',
        'now.weight += 1': '节点权重 +1：经过它的字符串数 = =={now.weight}==',
        'res += now.weight': lambda S, B, ret: f"终点权重 `{S.now.weight}` 包含 `w` 自己，要减 1：这些后面的字符串把 `w` 当作前后缀 → `res = {S.res}`",
        'return res': '全部处理完，返回满足条件的下标对数 =={ret}==',
    },
    cards=dict(
        one_liner='把前后缀合并成字符对，一棵 trie 同时匹配前缀和后缀',
        complexity='时间 `O(总字符数)`，空间 `O(总字符数)`',
        problem=['`isPrefixAndSuffix(a, b)`：a 既是 b 的前缀又是 b 的后缀',
                 '统计 `i < j` 且 `words[i]` 是 `words[j]` 前后缀的下标对数',
                 '示例：`["pa","papa","ma","mama"]` → `2`'],
        quote='既然words[i]在前缀trie树和后缀trie树中匹配的长度相同，那么不妨将二者合并，即构造trie树以及进行匹配时，使用(words[0], words[-1])，(words[1], words[-2])，...这样的字符对来作为树中的节点。',
        quote_src='—— yiduobo 题解',
        idea=['前缀和后缀分开建 trie，还要求下标集合的交集，最坏 `O(n^2)`',
              '改用字符对 `(w[i], w[-i-1])` 作边：沿路径匹配成功就==前后缀同时成功==',
              '从后往前插入，结束时终点权重 − 1（减去自己）就是答案增量'],
        result='`"a"` 的终点权重 3，减去自己 → 2 对（`"aba"`、`"aa"`）✓',
        summary=['时间、空间都是 `O(总字符数)`，II 的大数据同样适用',
                 '易错：终点权重包含 `w` 自己，必须 `- 1`',
                 '要从后往前遍历：这样 trie 里装的都是下标更大的字符串',
                 '原文是 Python 2 风格写法，但在 Python 3 下无需修改即可运行'],
    ),
)
