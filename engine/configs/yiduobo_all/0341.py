NESTED = [[1, 1], 2, [3, [4]]]

SETUP = '''
import itertools as _it
_nid = _it.count(1)

class NestedInteger:
    def __init__(self, x):
        self.uid = next(_nid)
        if isinstance(x, list):
            self._v = None
            self._l = [NestedInteger(y) for y in x]
        else:
            self._v = x
            self._l = None
    def isInteger(self):
        return self._l is None
    def getInteger(self):
        return self._v
    def getList(self):
        return self._l
    def __repr__(self):
        return str(self._v) if self._l is None else '[' + ','.join(map(repr, self._l)) + ']'
'''


def _build():
    cnt = [0]

    def mk(x):
        cnt[0] += 1
        uid = cnt[0]
        if isinstance(x, list):
            return (uid, [mk(y) for y in x])
        return (uid, x)
    return [mk(x) for x in NESTED]


TREE = _build()


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '嵌套列表（黄 = 当前 part，绿 = 已抽出的整数，紫框 = 正在展开的这一层）', 24, T['muted'], bold=True)
    p = S.get('part')
    cur = getattr(p, 'uid', None)
    sub_done = set()
    pi, bi = S.get('_inner', {}).get('part'), B.get('_inner', {}).get('part')
    if (S.get('_line') == 9 and pi is not None and not pi.isInteger() and bi is not None
            and getattr(bi, 'uid', None) == pi.uid):
        def coll(x):
            sub_done.add(x.uid)
            if not x.isInteger():
                for c in x.getList():
                    coll(c)
        coll(pi)
        cur = None
        p_uid = pi.uid
    else:
        p_uid = None
    tl = S.get('target_list')
    tl_ids = {getattr(c, 'uid', None) for c in tl} if tl is not None else None
    finished = 'self.num_list' in S
    toks = []  # (text, depth, uid, kind)

    def walk(lst, depth, own):
        toks.append(('[', depth, own))
        for k, (uid, v) in enumerate(lst):
            if k:
                toks.append((',', depth, None))
            if isinstance(v, list):
                walk(v, depth + 1, uid)
            else:
                toks.append((str(v), depth, uid))
        toks.append((']', depth, own))

    def find(lst, own):
        if {u for u, _ in lst} == tl_ids:
            return own
        for u, v in lst:
            if isinstance(v, list):
                r = find(v, u)
                if r is not None:
                    return r
        return None

    walk(TREE, 0, 0)
    own = find(TREE, 0) if tl_ids is not None and not finished else None
    wd = {'[': 34, ']': 34, ',': 26}
    total = sum(wd.get(t[0], 60) for t in toks)
    x = x0 + max(30, ((x1 - x0) - total) / 2)
    Y = (y0 + y1) / 2 + 14
    cols = [T['cyan'], T['pink'], T['orange'], T['purple']]
    lx = rx = None
    for s_, depth, uid in toks:
        ww = wd.get(s_, 60)
        if s_ in '[],':
            c = cols[depth % len(cols)] if s_ != ',' else T['muted']
            cv.text((x + ww / 2, Y), s_, 46, c, anchor='mm', bold=True)
            if uid == own and s_ == '[' and lx is None:
                lx = x
            if uid == own and s_ == ']':
                rx = x + ww
        else:
            done = finished or (cur is not None and uid < cur) or uid in sub_done or (p_uid is not None and uid < p_uid)
            fill = T['yellow'] if uid == cur else (T['green'] if done else T['panel2'])
            cv.rect((x + 5, Y - 28, x + ww - 5, Y + 28), fill=fill, outline=T['border'], width=2, r=8)
            cv.text((x + ww / 2, Y), s_, 32, T['text'] if fill == T['panel2'] else T['bg'], anchor='mm', bold=True)
        if uid == cur and s_ == '[' and uid != 0:
            cv.rect((x - 2, Y - 36, x + 30, Y + 36), outline=T['yellow'], width=3, r=8)
        x += ww
    if lx is not None and rx is not None:
        cv.rect((lx - 4, Y - 46, rx + 4, Y + 46), outline=T['purple'], width=3, r=12)


def _if(S, B, ret):
    p = S.part
    if p.isInteger():
        return f'`part = {p!r}` 是整数 → 直接加到 `res` 尾部'
    return f'`part = {p!r}` 是列表 → ==递归==把它展开'


CONFIG = dict(
    num=341, title='扁平化嵌套列表迭代器', difficulty='Medium', category='设计',
    author='yiduobo', technique='初始化时递归展开成普通列表',
    tags=['labuladong'],
    setup=SETUP,
    code='''
class NestedIterator(object):

    def __init__(self, nestedList):
        self.num_list = self.split_list(nestedList)
        self.pos = 0

    def split_list(self, target_list):
        res = []
        for part in target_list:
            if part.isInteger():
                res.append(part.getInteger())
            else:
                res.extend(self.split_list(part.getList()))

        return res

    def next(self):
        self.pos += 1
        return self.num_list[self.pos - 1]

    def hasNext(self):
        return self.pos < len(self.num_list)
''',
    call=f'''root = [NestedInteger(x) for x in {NESTED}]
it = NestedIterator(root)
out = []
while it.hasNext(): out.append(it.next())
out''',
    expect=[1, 1, 2, 3, 4],
    views=[
        dict(type='custom', draw=_draw, h=230),
        dict(type='array', var=lambda S: S.get('self.num_list', S.get('res', [])),
             label='res（当前这一层展开的结果）/ 展开后的 self.num_list', cell=80,
             pointers={'self.pos': 'blue'}),
        dict(type='calls', h=170),
    ],
    watch=[('pos', 'self.pos', 'blue'), ('len(num_list)', lambda S: len(S['self.num_list']) if 'self.num_list' in S else '-', 'green')],
    captions={
        'self.num_list = self.split_list': lambda S, B, r: (f'初始化完成：`num_list = {S["self.num_list"]}`' if 'self.num_list' in S
                                                            else '初始化时就调用 `split_list`，==一次性==把整个嵌套列表展开'),
        'self.pos = 0': '`pos` 指向下一个要返回的数',
        'res = []': '新的一层：`res` 存这一层展开后的整数',
        'for part in target_list': lambda S, B, r: (
            (f'子列表结果已 extend → `res = {S.res}`；' if 'part' in B['_inner'] and not B['_inner']['part'].isInteger() else '')
            + (f'取出元素 `part = {S.part!r}`' if 'part' in S['_inner'] and (
                B.get('part') is None or getattr(B.get('part'), 'uid', 0) != S.part.uid) else '这一层的元素都处理完了')),
        'if part.isInteger()': _if,
        'res.append(part.getInteger())': '`res` 尾部加入 `{res[-1]}` → `{res}`',
        'res.extend(self.split_list': lambda S, B, r: (f'进入递归：先把子列表 `{S.part!r}` 展开' if 'res' not in S['_inner']
                                                       else f'递归结果 extend 到尾部 → `res = {S.res}`'),
        'return res': lambda S, B, r: f'这一层展开完毕，返回 `{r}`',
        'self.pos += 1': '`pos` 后移 → {self.pos}',
        'return self.num_list[self.pos - 1]': '返回 `num_list[{self.pos - 1}]` = =={ret}==',
        'return self.pos < len': '`pos = {self.pos}`，`len = {len(self.num_list)}` → hasNext 为 =={ret}==',
    },
    max_steps=80,
    cards=dict(
        one_liner='初始化时一次性递归展开，之后就是普通列表的遍历',
        complexity='初始化 `O(N)`，`next`/`hasNext` `O(1)`，空间 `O(N)`',
        problem=['给一个嵌套整数列表，每个元素是整数或者又一个列表',
                 '实现迭代器 `NestedIterator`：`next()` 返回下一个整数，`hasNext()` 判断是否还有',
                 '示例：`[[1,1],2,[1,1]]` → `[1,1,2,1,1]`',
                 '本视频：`[[1,1],2,[3,[4]]]` → `[1,1,2,3,4]`'],
        quote='对于list中每个元素，如果其为整数，那么将其加入到标准list的尾部，否则递归处理该元素，然后将递归的结果extend到list尾部。',
        quote_src='—— yiduobo 题解原文',
        idea=['`split_list`：遇到整数直接 `append`，遇到列表递归后 `extend`',
              '展开后的 `num_list` 加一个下标 `pos` 就是迭代器',
              '作者自评：「总感觉不够优美」——一次性展开要预先占 `O(N)` 空间'],
        summary=['初始化 `O(N)`，之后每次操作 `O(1)`；空间 `O(N)`',
                 '`next` 先 `pos += 1` 再返回 `num_list[pos - 1]`',
                 '更「惰性」的做法：用栈保存迭代状态，`hasNext` 时才展开',
                 '原文为 Python 2 写法，删去了接口注释和 `:type` 文档字符串，其余不变'],
    ),
)

