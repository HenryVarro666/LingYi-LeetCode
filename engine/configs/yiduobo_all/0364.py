SETUP = '''
class NestedInteger:
    def __init__(self, value=None):
        self._v = value if value is not None else []
        self._int = value is not None
    def isInteger(self):
        return self._int
    def add(self, elem):
        self._v.append(elem)
    def setInteger(self, value):
        self._v, self._int = value, True
    def getInteger(self):
        return self._v if self._int else None
    def getList(self):
        return None if self._int else self._v
    def __repr__(self):
        return str(self._v) if self._int else '[' + ','.join(map(repr, self._v)) + ']'

def _mk(x):
    if isinstance(x, int):
        return NestedInteger(x)
    r = NestedInteger()
    for y in x:
        r.add(_mk(y))
    return r

nestedList = _mk([[1, 1], 2, [1, 1]]).getList()
'''


def _txt(S):
    nl = S.get('nestedList')
    head = f"输入 `{nl}`" if nl is not None else ''
    g = S['_inner'].get('_g')
    if g is None:
        return head
    return f"{head}　全局：不加权和 `s = {g[0]}`　最大深度 `max_depth = {g[1]}`"


def _final(S):
    g = S['_inner'].get('_g')
    if g is None or 'res' not in S:
        return '先按「越深权重越大」算 `res`，再用 `s × (max_depth + 1) − res` 反转'
    return f"`s × (max_depth + 1) − res = {g[0]} × {g[1] + 1} − {S['res']}` = =={g[0] * (g[1] + 1) - S['res']}=="


ST = {'s': 0, 'md': 0, 'k': {}}


def trk(kind, fn):
    """引擎只记录局部变量，global 的 s / max_depth 看不到；这里按步骤顺序重放它们的变化并写进 S / B。"""
    def cap(S, B, ret):
        B['s'], B['max_depth'] = ST['s'], ST['md']
        if kind == 'init':
            ST['s'] = ST['md'] = 0
        elif kind == 'depth':
            ST['md'] = max(ST['md'], S['depth'])
        elif kind == 's':
            ST['s'] += S['num']
        S['s'], S['max_depth'] = ST['s'], ST['md']
        S['_inner']['_g'] = (ST['s'], ST['md'])  # _inner 是共享引用，视图从这里读
        if kind == 'cnt0':
            ST['k'][S['depth']] = 0
        elif kind == 'for':
            ST['k'][S['depth']] = ST['k'].get(S['depth'], 0) + 1
            S['_k'] = ST['k'][S['depth']]
        if callable(fn):
            return fn(S, B, ret)
        from make import render_caption
        return render_caption(fn, S, B, ret)
    return cap


def _for(S, B, r):
    p = S.get('part')
    if p is None:
        return '遍历这一层的元素'
    if S['_k'] > len(S['now']):
        return '这一层的元素都处理完了，退出循环'
    return f'取这一层的下一个元素：`{p}`'


def _isint(S, B, r):
    return f'`{S.part}` 是整数，直接算' if S.part.isInteger() else f'`{S.part}` 是嵌套列表 → 往里钻，深度 +1'


CAPS = {
    'max_depth = s = 0': trk('init', '全局记录两样东西：==最大深度== `max_depth` 和不加权的数字总和 `s`'),
    'if not now': trk('', lambda S, B, r: '空列表，没有数字 → 返回 0' if not S.now else '列表非空，继续处理'),
    'return 0': trk('', '空列表：什么都没有，权重和为 0'),
    'max_depth = max': trk('depth', '深度 `{depth}`，更新最大深度：`max_depth = max({B.max_depth}, {depth})` = =={max_depth}=='),
    'cnt = 0': trk('cnt0', '`cnt` 累计这一层（含更深子层）的 数字×深度'),
    'for part in now': trk('for', _for),
    'if part.isInteger()': trk('', _isint),
    'num = part.getInteger()': trk('', '取出数字 `num = {num}`'),
    's += num': trk('s', '不加权总和：`s` 加上 `{num}` → =={s}=='),
    'cnt += num * depth': trk('', '正向权重：`{num} × {depth}` = {num * depth}，`cnt` → =={cnt}=='),
    'cnt += calc': trk('', '递归进入子列表：`calc(part.getList(), {B.depth} + 1)`，进入深度 {depth}'),
    'return cnt': trk('', '这一层的正向加权和 ==`{cnt}`== 返回给上一层'),
    'res = calc': trk('', '正向加权和 `res = {res}`：深度 1 的数字权重 1，越深越大'),
    'return s *': trk('', '逆向：`s × (max_depth + 1) − res` = `{s} × {max_depth + 1} − {res}` = =={ret}=='),
}


CONFIG = dict(
    num=364, title='加权嵌套序列和II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='先算正向权重和，再用逆向思维反转',
    tags=[],
    code='''
class Solution(object):
    def depthSumInverse(self, nestedList):

        global max_depth, s
        max_depth = s = 0

        def calc(now, depth):
            if not now:
                return 0

            global max_depth, s
            max_depth = max(max_depth, depth)

            cnt = 0
            for part in now:
                if part.isInteger():
                    num = part.getInteger()
                    s += num
                    cnt += num * depth
                else:
                    cnt += calc(part.getList(), depth + 1)

            return cnt

        res = calc(nestedList, 1)
        return s * (max_depth + 1) - res
''',
    setup=SETUP,
    call='Solution().depthSumInverse(nestedList)',
    expect=8,
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='calls', h=330, hide=('depthSumInverse',)),
        dict(type='text', fn=_final, size=28),
    ],
    watch=[('depth', 'depth', 'blue'), ('num', 'num', 'cyan'), ('cnt', 'cnt', 'yellow'),
           ('s', lambda S: S['_inner'].get('_g', (0, 0))[0], 'green'), ('max_depth', lambda S: S['_inner'].get('_g', (0, 0))[1], 'orange'), ('res', 'res', 'pink')],
    captions=CAPS,
    cards=dict(
        one_liner='权重倒过来算，就用「总深度 × 总和」减去正向权重和',
        complexity='时间 `O(n)`，空间 `O(d)`（d 为嵌套深度）',
        problem=['嵌套列表里有整数和子列表。一个整数的权重 = ==最大深度 − 它的深度 + 1==（越浅权重越大）',
                 '求所有整数 ×权重 的和',
                 '示例：`[[1,1],2,[1,1]]` → `8`（四个 1 在深度 2 权重 1，2 在深度 1 权重 2）'],
        quote='与之前的区别是计算深度的方法刚好相反，那么可以利用逆向思维，按照之前的计算方法计算原始版本的权重和，同时在这个过程中计算总深度以及不加权的数值总和，然后使用这二者的乘积减去原始版本的权重和',
        quote_src='—— yiduobo 题解原文',
        idea=['先按 339 题的方法，一遍递归算出：正向加权和 `res`、总深度 `max_depth`、总和 `s`',
              '真实权重 `w = max_depth + 1 − depth`',
              '所以 `Σ num × w = s × (max_depth + 1) − Σ num × depth`'],
        summary=['时间 `O(n)`，空间 `O(d)`',
                 '`max_depth` 取的是有数字的最深层；空列表直接返回 0，不参与深度',
                 '用 `global` 在递归里共享 `max_depth` 和 `s`，每次调用前要先重置为 0',
                 '同系列：339 题 嵌套列表权重和（深度越深权重越大）；原文代码未改动'],
    ),
)
