CONFIG = dict(
    num=3597, title='分割字符串', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='Trie 树逐段检测',
    tags=[],
    code='''
class Node(object):
    def __init__(self):
        self.children = {}

class Solution(object):
    def partitionString(self, s):
        
        root = Node()
        res = []
        p = 0
        start = 0
        while p < len(s):
            curr = root
            start = p
            while p < len(s) and s[p] in curr.children:
                curr = curr.children[s[p]]
                p += 1
            
            if p == len(s):
                break
            
            node = Node()
            curr.children[s[p]] = node
            res.append(s[start: p + 1])
            p += 1
        
        return res
''',
    call='Solution().partitionString("abbccccd")',
    expect=["a", "b", "bc", "c", "cc", "d"],
    views=[
        dict(type='string', var='s', pointers={'start': 'blue', 'p': 'pink'}, h=190,
             label='s（蓝 = 当前段起点 start，粉 = 指针 p）'),
        dict(type='custom', h=270, draw=lambda cv, S, B, box, T: _trie(cv, S, B, box, T)),
        dict(type='text', h=70, fn=lambda S: '已分出的段：' + ' , '.join(f'`{x}`' for x in S.get('res', [])) if S.get('res') else '已分出的段：（空）'),
    ],
    skip=[3, 'start = 0', 'node = Node()'],
    max_steps=90,
    watch=[('start', 'start', 'blue'), ('p', 'p', 'pink'), ('res', 'res', 'green')],
    captions={
        'root = Node()': '建一棵空 Trie，`root` 是根节点，`children` 存字符到孩子的映射',
        'p = 0': '`p` 是扫描指针，`start` 记录当前段的开头',
        'curr = root': '每个新段都从根出发检测',
        'start = p': '这一段从下标 `{start}` 开始',
        'while p < len(s) and s[p] in curr.children': lambda S, B, r: (
            f'`p = {S.p}`，字符 `{S.s[S.p]}` 在 curr 的孩子里吗？' + ('在：这个前缀以前出现过，走到孩子，段继续变长' if S.s[S.p] in S.curr.children else '==不在==：当前前缀独一无二') if S.p < len(S.s)
            else f'`p = {S.p}` 已到末尾，没法再扩展'),
        'curr = curr.children[s[p]]': '走进孩子节点（前缀见过，段继续变长）',
        'if p == len(s)': lambda S, B, r: ('字符串用完了，最后这段以前出现过，不能算新段 → break' if S.p == len(S.s) else '`p` 还没到末尾：当前段是新的'),
        'node = Node()': '新建一个节点，准备挂到 curr 下面',
        'curr.children[s[p]] = node': '把新前缀挂进 Trie：以后再遇到它就是"出现过"',
        'res.append': '当前段 `s[{start}:{p + 1}]` = =={res[-1]}== 加入答案',
        17: '`p` 后移一位，继续看下一个字符',
        25: '`p` 移到下一个位置 {p}，下一段从这里开始',
        'return res': '返回所有段：`{ret}`',
    },
    cards=dict(
        one_liner='用 Trie 记住所有出现过的段，新前缀一旦"无路可走"就切一段',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['按规则把 `s` 分段：每段逐字符扩展，直到这个段之前没出现过为止',
                 '按顺序返回所有段，例如 `"aaaa"` → `["a", "aa"]`',
                 '本视频：`"abbccccd"` → `["a","b","bc","c","cc","d"]`'],
        quote='在这里使用trie树进行构造和检测是非常合适的。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个新段都从 Trie 根开始：字符已在孩子里 → 前缀见过，往下走',
              '遇到不在孩子里的字符 → 当前前缀独一无二：新建节点、记录这一段',
              '字符串在走 Trie 的过程中用完了，最后一段不算新段，直接结束'],
        summary=['时间 `O(n)`，空间 `O(n)`：每次只新增一个节点',
                 '`if p == len(s): break`：末尾那段若是旧前缀，不能加入答案',
                 '写法与灵神的差别：这里用 `Node` 类，外层 `while` 手动控制每段的起点',
                 '原文代码在 Python 3 下可直接运行，未做修改'],
    ),
)


def _trie(cv, S, B, box, T):
    ch = lambda n: n.children
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '字典树 root（黄 = 当前所在节点 curr）', 24, T['muted'], bold=True)
    root = S.get('root')
    cur = S.get('curr')
    if root is None:
        return
    # 布局：叶子数决定宽度
    def leaves(n):
        return max(1, sum(leaves(c) for c in n.children.values())) if n.children else 1
    total = leaves(root)
    W = x1 - x0 - 60
    unit = min(120, W / total)
    pos = {}
    def place(n, lo, depth, label):
        w = leaves(n) * unit
        x = x0 + 30 + lo + w / 2
        y = y0 + 120 + depth * 70
        pos[id(n)] = (x, y)
        off = lo
        for ch, c in n.children.items():
            cw = leaves(c) * unit
            place(c, off, depth + 1, ch)
            off += cw
    place(root, 0, 0, '')
    def draw(n, label):
        x, y = pos[id(n)]
        off = None
        for ch, c in n.children.items():
            cx, cy = pos[id(c)]
            cv.line([(x, y), (cx, cy)], T['muted'], 2)
            cv.text(((x + cx) / 2 + 10, (y + cy) / 2), ch, 22, T['cyan'], anchor='lm', bold=True)
            draw(c, ch)
    draw(root, '')
    for k, (x, y) in [(None, pos[id(root)])]:
        pass
    for n_id, (x, y) in pos.items():
        is_cur = cur is not None and id(cur) == n_id
        cv.rect((x - 16, y - 16, x + 16, y + 16), fill=T['yellow'] if is_cur else T['border'], r=16,
                outline=T['yellow'] if is_cur else T['muted'], width=2)
    cv.text((pos[id(root)][0] - 30, pos[id(root)][1]), 'root', 20, T['dim'], anchor='rm')
