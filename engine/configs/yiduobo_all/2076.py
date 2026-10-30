REQ = [[0, 2], [2, 1], [3, 2]]
RES = [[0, 1]]
COLS = ['blue', 'pink', 'green', 'purple', 'cyan', 'yellow', 'orange', 'red']


def _root(fa, x):
    while fa[x] != x:
        x = fa[x]
    return x


def _color(S, i, v):
    fa = S.get('fa')
    if fa is None:
        return None
    r = _root(fa, i)
    return COLS[r % len(COLS)] if any(_root(fa, j) == r and j != i for j in range(len(fa))) else None


def _groups(S):
    fa = S.get('fa')
    if fa is None:
        return ''
    roots = sorted({_root(fa, i) for i in range(len(fa))})
    g = ' '.join('{' + ','.join(str(i) for i in range(len(fa)) if _root(fa, i) == r) + '}' for r in roots)
    return f'朋友圈：{g}　　禁止：`{RES}`'


def _req(S):
    if 'x' not in S:
        return '依次处理请求，每个请求要检查所有限制'
    out = S.get('res', [])
    s = f'请求 `({S["x"]}, {S["y"]})`　已有结果 `{out}`'
    if 'u' in S and 'v' in S:
        s += f'　正在对照限制 `({S["u"]}, {S["v"]})`'
    return s


CONFIG = dict(
    num=2076, title='处理含限制条件的好友请求', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='并查集 + 逐条检查限制',
    tags=['七、并查集', '难度分 2131'],
    code='''
class Solution(object):
    def friendRequests(self, n, restrictions, requests):

        fa = list(range(n))

        def find(x):
            if x != fa[x]:
                fa[x] = find(fa[x])
            
            return fa[x]

        res = []
        for x, y in requests:
            fa_x = find(x)
            fa_y = find(y)
            if fa_x == fa_y:
                res.append(True)
            else:
                flag = True
                for u, v in restrictions:
                    fa_u = find(u)
                    fa_v = find(v)
                    if (fa_x == fa_u and fa_y == fa_v) or (fa_x == fa_v and fa_y == fa_u):
                        flag = False
                        break
                
                if flag:
                    fa[fa_x] = fa_y
                    res.append(True)
                else:
                    res.append(False)

        return res
''',
    call=f'Solution().friendRequests(4, {RES}, {REQ})',
    expect=[True, False, True],
    views=[
        dict(type='text', fn=_req, size=24, h=70),
        dict(type='array', var='fa', label='fa（同色 = 已是同一个朋友圈）', color=_color, h=190,
             pointers={'fa_x': 'blue', 'fa_y': 'pink'}),
        dict(type='text', fn=_groups, size=24, h=70),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('flag', 'flag', 'orange'), ('res', 'res', 'green')],
    skip=['fa = list', 'res = []', 'flag = True', 'fa_u = find', 'fa_v = find', 'tmp ='],
    max_steps=110,
    captions={
        'fa_x = find': '`{x}` 的祖先：`fa_x`',
        'fa_y = find': '`{y}` 的祖先：`fa_y`',
        'if fa_x == fa_y': lambda S, B, r: (f'祖先同为 `{S.fa_x}`：已经是同一个圈 → ==请求成功==' if S.fa_x == S.fa_y
                                             else f'祖先 `{S.fa_x}` ≠ `{S.fa_y}`：还不是一个圈，要看合并会不会违反限制'),
        'if (fa_x == fa_u': lambda S, B, r: (f'限制 `({S.u},{S.v})` 的祖先是 `({S.fa_u},{S.fa_v})`，请求祖先是 `({S.fa_x},{S.fa_y})`：'
                                            + ('==两圈恰好对上，合并会让他们成为朋友==' if ((S.fa_x == S.fa_u and S.fa_y == S.fa_v) or (S.fa_x == S.fa_v and S.fa_y == S.fa_u)) else '无冲突')),
        'flag = False': '违反限制：`flag = False`',
        'break': '已经冲突，不用再查其他限制',
        'if flag': lambda S, B, r: ('所有限制都不冲突 → ==可以合并==' if S.flag else '有冲突 → 请求失败'),
        'fa[fa_x] = fa_y': '合并：`fa[{fa_x}] = {fa_y}`，两个朋友圈变成一个',
        'res.append(True)': '这个请求成功：`res` = {res}',
        'res.append(False)': '这个请求失败：`res` = {res}',
        'return res': '所有请求处理完：=={res}==',
        'fa[x] = find': '路径压缩：`fa[{x}]` 直接指向祖先',
    },
    cards=dict(
        one_liner='把两个朋友圈合并前，检查有没有一条限制会被它们连起来',
        complexity='时间 `O(q · r · α(n))`，空间 `O(n)`',
        problem=['`n` 个用户，`restrictions` 里每对 `(x, y)` 不能成为朋友（含间接）',
                 '按顺序处理好友请求：不违反限制就成功，两人成为朋友',
                 '本视频：`n=4`，限制 `[[0,1]]`，请求 `[[0,2],[2,1],[3,2]]` → `[true,false,true]`'],
        quote='若fa_x等于fa_u且fa_y等于fa_v，或者反过来，那么将x和y连通后会使得u和v也连通，说明x和y是不能连通的。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个人是图中的点，成为朋友就连边，并查集维护连通性',
              '处理请求 `(x, y)`：先找各自祖先；已在一个圈就直接成功',
              '否则枚举每条限制 `(u, v)`，若两圈正好分别包含 `u`、`v`，合并就违规'],
        summary=['时间 `O(q · r)`（再乘 `α`），空间 `O(n)`',
                 '比较的是==祖先==，不是原编号；限制要两个方向都判断',
                 '已是朋友的请求仍然成功，要放在限制检查之前',
                 '原文为 Python 2 写法，`fa = range(n)` 已改为 `fa = list(range(n))`'],
    ),
)
