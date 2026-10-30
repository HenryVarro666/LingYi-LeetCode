SETUP = '''
class Node(object):
    def __init__(self, val=None, children=[]):
        self.val = val
        self.children = children
    def __repr__(self):
        return f'Node({self.val})'

class Tracked(str):
    """遍历时记录当前下标 pos，仅供动画定位当前字符"""
    pos = -1
    def __iter__(self):
        for i, ch in enumerate(str.__iter__(self)):
            self.pos = i
            yield ch

root = Node(1, [Node(2, []), Node(3, [Node(4, [])])])
'''


def _ser(t):
    if t is None:
        return ''
    s = str(t.val)
    if t.children:
        s += '(' + ' '.join(_ser(c) for c in t.children) + ')'
    return s


def _lay(root):
    pos, dep, nxt = {}, {}, [0]

    def go(nd, d):
        if not nd.children:
            pos[id(nd)] = nxt[0]
            nxt[0] += 1
        else:
            for c in nd.children:
                go(c, d + 1)
            pos[id(nd)] = (pos[id(nd.children[0])] + pos[id(nd.children[-1])]) / 2
        dep[id(nd)] = d
    go(root, 0)
    return pos, dep, max(dep.values()), max(nxt[0] - 1, 1)


def _built(S):
    st = S.get('stack')
    if st:
        return st[0]
    return S.get('now_root')


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    des = 'now_root' in S['_inner'] and 'data' in S['_inner']
    root = _built(S['_inner']) if des else S.get('root')
    if des:
        cv.text((x0 + 18, y0 + 4), '反序列化：正在还原的树（黄 = now_root）', 22, T['muted'], bold=True)
    else:
        cv.text((x0 + 18, y0 + 4), '序列化：原树（黄 = 当前递归的节点）', 22, T['muted'], bold=True)
    if root is None:
        return
    cur = S['_inner'].get('now_root') if des else S['_inner'].get('root')
    pos, dep, md, mw = _lay(root)
    R = 30
    w, h = x1 - x0 - 2 * R - 160, y1 - y0 - 2 * R - 80
    nodes, P = [], {}

    def walk(nd):
        nodes.append(nd)
        P[id(nd)] = (x0 + 80 + R + pos[id(nd)] / mw * w, y0 + 50 + R + dep[id(nd)] / max(md, 1) * h)
        for c in nd.children:
            walk(c)
    walk(root)
    for nd in nodes:
        for c in nd.children:
            cv.line([P[id(nd)], P[id(c)]], T['dim'], 4)
    for nd in nodes:
        cx, cy = P[id(nd)]
        on = nd is cur
        cv.d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=T['yellow'] if on else T['panel2'],
                     outline=T['border'], width=3)
        cv.text((cx, cy), nd.val, 28, T['bg'] if on else T['text'], anchor='mm', bold=True)


def _strdraw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    I = S['_inner']
    if 'now_root' in I and 'data' in I:
        data = str(I['data'])
        pos = getattr(I['data'], 'pos', -1)
        cv.text((x0 + 18, y0 + 4), 'data（黄框 = 正在读的字符）', 22, T['muted'], bold=True)
        n = len(data)
        cell = min(64, (x1 - x0 - 40) / n)
        sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
        yy = y0 + 50
        for i, ch in enumerate(data):
            X = sx + i * cell
            hit = i == pos
            cv.rect((X + 2, yy, X + cell - 2, yy + cell - 6), fill=T['yellow'] if hit else T['panel2'],
                    outline=T['border'], r=6)
            cv.text((X + cell / 2, yy + (cell - 6) / 2), ch if ch != ' ' else '␣', 30, T['bg'] if hit else T['text'],
                    anchor='mm', bold=True, mono=True)
        now = I.get('now')
        cv.text((x1 - 20, y0 + 4), f'now = {now}', 26, T['blue'], anchor='ra', bold=True, mono=True)
    else:
        res = I.get('res') or []
        cv.text((x0 + 18, y0 + 4), '当前这一层的 res（拼起来就是这棵子树的字符串）', 22, T['muted'], bold=True)
        cv.text((x0 + 20, y0 + 52), ''.join(map(str, res)) if res else '（空）', 36, T['green'], bold=True, mono=True)
        out = S.get('data')
        if out is not None:
            cv.text((x0 + 20, y0 + 110), f'data = {out}', 26, T['blue'], bold=True, mono=True)


def _stk(S):
    return [x.val for x in (S['_inner'].get('stack') or [])]


CONFIG = dict(
    num=428, title='序列化和反序列化N叉树', difficulty='Hard', category='二叉树与回溯',
    author='yiduobo', technique='括号序列化 · 栈反序列化',
    tags=['链表树与回溯', '灵神题单·链表树与回溯'],
    code='''
class Codec:
    def serialize(self, root):
        if not root:
            return ''

        first = True
        res = [str(root.val)]
        if len(root.children) > 0:
            res.append('(')
            for child in root.children:
                if first:
                    first = False
                else:
                    res.append(' ')
                res.append(self.serialize(child))
            res.append(')')

        return ''.join(res)

    def deserialize(self, data):
        now = None
        stack = []
        now_root = None

        for char in data:
            if char >= '0' and char <= '9':
                if now is None:
                    now = 0
                now = now * 10 + int(char)
            elif char == '(':
                if now_root is not None:
                    stack.append(now_root)
                    tmp = Node(now, [])
                    now_root.children.append(tmp)
                    now_root = tmp
                else:
                    now_root = Node(now, [])

                now = None
            elif char == ' ':
                if now is not None:
                    now_root.children.append(Node(now, []))
                    now = None
            else:
                if now is not None:
                    now_root.children.append(Node(now, []))
                    now = None
                if stack:
                    now_root = stack.pop()
                else:
                    return now_root

        if len(data) == 0:
            return None
        else:
            return Node(now, [])
''',
    setup=SETUP,
    call='c = Codec()\ndata = c.serialize(root)\nc.deserialize(Tracked(data))',
    expect='1(2 3(4))',
    result_fn=_ser,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='custom', draw=_strdraw, h=150),
        dict(type='stack', var=_stk, h=110, label='stack（还没处理完的祖先）', fmt=lambda x: str(x)),
        dict(type='calls', h=130, hide=('self', 'data', 'root')),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'blue'),
           ('now_root', lambda S: getattr(S['_inner'].get('now_root'), 'val', None), 'yellow'),
           ('char', lambda S: S['_inner'].get('char'), 'pink')],
    skip=['first = True', 'stack = []', 'now_root = None', 'now = None'],
    captions={
        'if not root': lambda S, B, r: ('空节点 → 返回空串' if not S._inner.get('root') else f'节点 `{S._inner["root"].val}` 非空，继续'),
        'res = [str(root.val)]': '先放进自己的值：`res = {res}`',
        'if len(root.children) > 0': lambda S, B, r: ('有孩子 → 需要加括号并递归孩子' if S._inner['root'].children else '没有孩子 → 不加括号，这个节点就是它的值'),
        "res.append('(')": '有孩子：先写左括号 `(`',
        'for child in root.children': lambda S, B, r: ('孩子都处理完，循环结束' if getattr(B._inner.get('child'), 'val', None) is not None and B._inner['child'].val == S._inner['child'].val else f'取下一个孩子 `{S.child.val}`'),
        'if first': lambda S, B, r: ('第一个孩子前面不用空格' if S._inner['first'] else '不是第一个孩子 → 先补一个空格间隔'),
        'first = False': '之后的孩子都要先加空格',
        "res.append(' ')": '孩子之间用空格隔开',
        'res.append(self.serialize(child))': '递归求孩子 `{child.val}` 的序列化字符串，返回后接在 `res` 后面',
        "res.append(')')": '孩子都处理完：补右括号收尾',
        "return ''.join": '拼起来返回：`{ret}`',
        'for char in data': '逐个读字符 `char = {char}`',
        "if char >= '0'": lambda S, B, r: (f'`{S.char}` 是数字 → 用来拼数值' if S.char.isdigit() else f'`{S.char}` 不是数字，看是什么符号'),
        'if now is None': '`now` 还是空 → 先置 0，再往末尾拼数字',
        'now = 0': '开始一个新数值',
        'now = now * 10': '`now = now * 10 + {char}` = =={now}==（节点值可能不止一位）',
        "elif char == '('": lambda S, B, r: ('是 `(`：它左边的 `now` 是一个有孩子的节点' if S.char == '(' else '不是 `(`，继续判断'),
        'if now_root is not None': lambda S, B, r: ('已经有 now_root：新节点是它的孩子' if S.now_root is not None else '还没有 now_root：这是整棵树的根'),
        'stack.append(now_root)': '把还没处理完的 `now_root` ({now_root.val}) 压栈，等孩子们处理完再回来',
        'tmp = Node(now, [])': '为 `now = {now}` 建节点 `tmp`',
        'now_root.children.append(tmp)': '`tmp` 挂到 `now_root` 的孩子里',
        'now_root = tmp': '往下一层：`now_root` 换成 `tmp`（{tmp.val}）',
        'now_root = Node(now, [])': '遇到根的左括号：建根节点 `{now_root.val}`',
        'elif char': lambda S, B, r: ('是空格：孩子之间的分隔' if S.char == ' ' else '既不是数字、`(` 也不是空格 → 一定是 `)`'),
        'if now is not None': lambda S, B, r: (f'`now = {S.now}` 非空：左边紧挨着一个叶子值，要建节点' if S.now is not None else '`now` 为空：左边是 `)`，没有待建的节点'),
        'now_root.children.append(Node(now, []))': '建叶子 `{now}` 并加入 `now_root` 的孩子 → {[c.val for c in now_root.children]}',
        'if stack': lambda S, B, r: ('栈非空 → 回到父节点' if S.stack else '栈空 → `now_root` 就是整棵树的根'),
        'now_root = stack.pop()': '`now_root` 这棵子树完成了：弹出父节点 `{now_root.val}` 继续',
        'return now_root': '栈空：最外层的 `)`，整棵树还原完成',
        'if len(data) == 0': '循环没返回过 → 看 `data` 有没有括号',
    },
    cards=dict(
        one_liner='括号序列化：值(孩子 孩子)；反序列化用栈记住还没处理完的祖先',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['设计 `serialize` / `deserialize`，把 N 叉树和字符串互相转换',
                 '格式不限，本解用题面给的括号方案（去掉最外层括号）',
                 '本视频：树 `1(2 3(4))` → 字符串 → 还原为同一棵树'],
        quote='对于以root为根节点的子树，其序列化过程是首先将root.val加入到序列化的结果res中。接下来，若root有孩子节点，那么就在res中加入左括号……各个孩子节点的序列化结果间需要使用空格来间隔。',
        quote_src='—— yiduobo 题解原文',
        idea=['序列化：先写 `val`，有孩子就 `(` + 递归每个孩子（空格隔开）+ `)`',
              '反序列化：`now` 拼数值；遇 `(` 建节点并把父节点压栈',
              '遇空格或 `)` 时若 `now` 非空，说明是叶子，直接挂到 `now_root`；`)` 再弹栈回到父节点'],
        summary=['时间 `O(n)`，空间 `O(n)`（栈深度 = 树高）',
                 '易错：数值可能多位，所以用 `now * 10 + 数字` 累积',
                 '易错：`(` 左边的数建节点，空格/`)` 左边的数建叶子，别重复建',
                 '特殊情况：`data` 没有括号时，要么为空，要么只是根的值',
                 '原文为 Python 2 风格，这里只删去了类型文档字符串；Node 定义放在 setup 中'],
    ),
)
