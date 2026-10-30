# 静态画图用的树结构：叶子 = (值,)，内部节点 = [左上, 右上, 左下, 右下]
SPEC1 = [(0,), (1,), (0,), [(0,), (0,), (1,), (0,)]]
SPEC2 = [[(1,), (0,), (0,), (1,)], (0,), (0,), [(1,), (1,), (0,), (1,)]]
QN = ('左上', '右上', '左下', '右下')


def _sub(spec, path):
    """path 如 'r.3.1'"""
    cur = spec
    for k in path.split('.')[1:]:
        cur = cur[int(k)]
    return cur


def _draw_spec(cv, T, spec, x, y, s, path, cur):
    if isinstance(spec, tuple):
        v = spec[0]
        cv.rect((x + 1, y + 1, x + s - 1, y + s - 1), fill=T['green'] if v else T['panel2'], outline=T['border'])
        cv.text((x + s / 2, y + s / 2), v, max(14, int(s * 0.4)), T['bg'] if v else T['dim'], anchor='mm', bold=True)
    else:
        h = s / 2
        for k, ch in enumerate(spec):
            _draw_spec(cv, T, ch, x + (k % 2) * h, y + (k // 2) * h, h, f'{path}.{k}', cur)
    if path == cur:
        cv.rect((x + 2, y + 2, x + s - 2, y + s - 2), outline=T['yellow'], width=5)


def _draw_node(cv, T, n, x, y, s):
    if n is None:
        cv.rect((x + 1, y + 1, x + s - 1, y + s - 1), fill=T['bg'], outline=T['border'])
        cv.text((x + s / 2, y + s / 2), '?', max(14, int(s * 0.4)), T['dim'], anchor='mm', bold=True)
    elif n.isLeaf:
        v = 1 if n.val else 0
        cv.rect((x + 1, y + 1, x + s - 1, y + s - 1), fill=T['green'] if v else T['panel2'], outline=T['border'])
        cv.text((x + s / 2, y + s / 2), v, max(14, int(s * 0.4)), T['bg'] if v else T['dim'], anchor='mm', bold=True)
    else:
        h = s / 2
        for k, a in enumerate(('topLeft', 'topRight', 'bottomLeft', 'bottomRight')):
            _draw_node(cv, T, getattr(n, a, None), x + (k % 2) * h, y + (k // 2) * h, h)
        cv.rect((x, y, x + s, y + s), outline=T['border'], width=2)


def _cur(S):
    i = S.get('_inner') or {}
    n = i.get('quadTree1')
    return getattr(n, 'path', None) if n is not None else None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cur = _cur(S)
    w = (x1 - x0 - 40) / 3
    s = min(w - 40, y1 - y0 - 90)
    for k, (name, col) in enumerate((('quadTree1', T['blue']), ('quadTree2', T['pink']), ('ret（? = 未填）', T['green']))):
        X = x0 + 20 + k * w + (w - s) / 2
        cv.text((X + s / 2, y0 + 6), name, 22, col, anchor='mt', bold=True)
        Y = y0 + 50
        if k == 0:
            _draw_spec(cv, T, SPEC1, X, Y, s, 'r', cur)
        elif k == 1:
            _draw_spec(cv, T, SPEC2, X, Y, s, 'r', cur)
        else:
            r = S.get('ret')
            if r is None:
                cv.rect((X, Y, X + s, Y + s), outline=T['border'], width=2)
                cv.text((X + s / 2, Y + s / 2), '还没有', 24, T['dim'], anchor='mm')
            else:
                _draw_node(cv, T, r, X, Y, s)
    if cur:
        cv.text((x1 - 20, y1 - 6), f'黄框 = 当前比较的区域（{_where(cur)}）', 20, T['yellow'], anchor='rb', bold=True)


def _where(path):
    ks = path.split('.')[1:]
    return '整个正方形' if not ks else ' → '.join(QN[int(k)] for k in ks)


def _nd(n):
    return ('叶子' + str(1 if n.val else 0)) if n.isLeaf else '非叶子'


def _info(S):
    i = S.get('_inner')
    if not i or 'quadTree1' not in i:
        return '两棵四叉树对应位置做「或」：`1 or X = 1`，`0 or X = X`'
    a, b = i['quadTree1'], i['quadTree2']
    return f"区域 =={_where(a.path)}==：A 是 `{_nd(a)}`，B 是 `{_nd(b)}`"


def _cap_a(S, B, ret):
    a = S['_inner']['quadTree1']
    return f"A（{_where(a.path)}）是{'叶子' if a.isLeaf else '非叶子'} → " + ('进入情况 1 / 2：看 A 的值' if a.isLeaf else '先看 B 是不是叶子')


def _cap_aval(S, B, ret):
    a = S['_inner']['quadTree1']
    return f"A 是叶子且值为 `{int(bool(a.val))}`：" + ('`1 or X = 1`，不管 B 是什么，结果全是 1' if a.val else '`0 or X = X`，结果就是 B')


def _cap_bval(S, B, ret):
    b = S['_inner']['quadTree2']
    return f"A 不是叶子、B 是叶子，值为 `{int(bool(b.val))}`：" + ('`1 or X = 1`，结果全是 1' if b.val else '`0 or X = X`，结果就是 A')


def _cap_ret(S, B, ret):
    if hasattr(ret, 'path'):
        return f"返回原树里 {_where(ret.path)} 处的{_nd(ret)}（直接复用，不新建）"
    return f"返回新建的 `ret`：{_nd(ret)}"


CONFIG = dict(
    num=558, title='四叉树交集', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='递归：对应区域做「或」',
    tags=['链表树与回溯'],
    setup='''
import tracer
class Node(object):
    def __init__(self, val, isLeaf, topLeft=None, topRight=None, bottomLeft=None, bottomRight=None):
        self.val = val
        self.isLeaf = isLeaf
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        self._uid = tracer.next_uid()
    def __repr__(self):
        p = getattr(self, 'path', '新')
        return ('叶' + str(int(bool(self.val)))) + '@' + p if self.isLeaf else '内@' + p

def _build(spec, path='r'):
    if isinstance(spec, tuple):
        n = Node(bool(spec[0]), True)
    else:
        a, b, c, d = [_build(ch, path + '.' + str(k)) for k, ch in enumerate(spec)]
        n = Node(False, False, a, b, c, d)
    n.path = path
    return n

def _ser(n):
    return str(int(bool(n.val))) if n.isLeaf else 'N[' + ','.join(_ser(c) for c in (n.topLeft, n.topRight, n.bottomLeft, n.bottomRight)) + ']'

T1 = _build([(0,), (1,), (0,), [(0,), (0,), (1,), (0,)]])
T2 = _build([[(1,), (0,), (0,), (1,)], (0,), (0,), [(1,), (1,), (0,), (1,)]])
''',
    code='''
class Solution(object):
    def intersect(self, quadTree1, quadTree2):

        return self.dfs(quadTree1, quadTree2)

    def dfs(self, quadTree1, quadTree2):
        if quadTree1.isLeaf:
            if quadTree1.val:
                return quadTree1
            else:
                return quadTree2
        elif quadTree2.isLeaf:
            if quadTree2.val:
                return quadTree2
            else:
                return quadTree1
        else:
            ret = Node(False, False)
            ret.topLeft = self.dfs(quadTree1.topLeft, quadTree2.topLeft)
            ret.topRight = self.dfs(quadTree1.topRight, quadTree2.topRight)
            ret.bottomLeft = self.dfs(quadTree1.bottomLeft, quadTree2.bottomLeft)
            ret.bottomRight = self.dfs(quadTree1.bottomRight, quadTree2.bottomRight)
            if ret.topLeft.isLeaf and ret.topLeft.val and ret.topRight.isLeaf and ret.topRight.val and ret.bottomLeft.isLeaf and ret.bottomLeft.val and ret.bottomRight.isLeaf and ret.bottomRight.val:
                ret.topLeft = ret.topRight = ret.bottomLeft = ret.bottomRight = None
                ret.isLeaf = ret.val = True

        return ret
''',
    call='_ser(Solution().intersect(T1, T2))',
    expect='N[N[1,0,0,1],1,0,1]',
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='calls', h=200, hide=()),
    ],
    watch=[('A', lambda S: repr(S['_inner']['quadTree1']) if 'quadTree1' in S.get('_inner', {}) else None, 'blue'),
           ('B', lambda S: repr(S['_inner']['quadTree2']) if 'quadTree2' in S.get('_inner', {}) else None, 'pink')],
    captions={
        4: '从两棵树的根（整个正方形）开始：对每个对应区域做「或」',
        7: _cap_a,
        8: _cap_aval,
        9: 'A 值为 1 → 直接返回 A（整块都是 1）',
        11: 'A 值为 0 → 或运算后等于 B，直接返回 B（整棵子树原样复用）',
        12: lambda S, B, r: f"A 不是叶子；B 是{'叶子' if S['_inner']['quadTree2'].isLeaf else '非叶子'}",
        13: _cap_bval,
        14: 'B 值为 1 → 返回 B（整块都是 1）',
        16: 'B 值为 0 → 或运算后等于 A，直接返回 A',
        18: '==A、B 都不是叶子==：新建一个非叶子节点 `ret`，四个角分别递归求解',
        19: '递归求左上角：`dfs(A.topLeft, B.topLeft)`',
        20: '递归求右上角',
        21: '递归求左下角',
        22: '递归求右下角',
        23: lambda S, B, r: ('四个角==都是值为 1 的叶子==' if (lambda i: all(getattr(c, 'isLeaf', False) and c.val for c in (i['ret'].topLeft, i['ret'].topRight, i['ret'].bottomLeft, i['ret'].bottomRight)))(S['_inner']) else '四个角里有 0 或非叶子 → 不能合并，保持非叶子'),
        24: '四个角全是 1：丢掉四个孩子',
        25: '`ret` 变成值为 1 的叶子：整块合并成一个 1',
        27: _cap_ret,
    },
    skip=[],
    max_steps=110,
    cards=dict(
        one_liner='对应区域做「或」：见到 1 就整块是 1，见到 0 就听另一棵的',
        complexity='时间 `O(n)`（n 为两棵树节点数的较小者量级），空间 `O(h)`',
        problem=['四叉树每个节点是叶子（整块同值）或有四个孩子（左上、右上、左下、右下）',
                 '给两棵表示 `n×n` 二进制矩阵的四叉树，返回它们按位「或」的四叉树',
                 '本视频：两棵 `2×2` 层的四叉树，结果在 `右下` 合并成一个叶子 `1`'],
        quote='若A是叶子节点，且值为1：由于1 || X = 1，所以此时不论B怎么样，与A进行或运算之后的结果必然也全都是1。若A是叶子节点，且值为0：由于0 || X = X，所以结果必然还是B。',
        quote_src='—— yiduobo 题解原文',
        idea=['分五种情况：A 是叶子（值 1 返回 A，值 0 返回 B）；A 非叶但 B 是叶子（同理）',
              '都不是叶子：新建 `ret`，四个角各递归一次',
              '「或」的结果可能全为 1、不可能全为 0：四个角都是 1 的叶子才合并成一个叶子'],
        summary=['时间 `O(n)`，空间 `O(h)`：每个区域只比较一次',
                 '易错点：合并只判断「四个角都是值为 1 的叶子」；全 0 不会出现，因为或运算里至少一个孩子非叶',
                 '直接返回 `quadTree1` / `quadTree2`：整棵子树被复用，没有拷贝',
                 '合并时要同时设 `isLeaf = val = True` 并清空四个孩子',
                 '原文 `Node` 类定义是注释，视频里在 setup 补上（`val`/`isLeaf` 之外的参数给默认值 `None`），题解代码未改动'],
    ),
)
