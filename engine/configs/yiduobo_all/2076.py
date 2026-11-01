def _groups(S):
    fa = S.get('fa')
    if fa is None:
        return ''
    g = {}
    for i in range(len(fa)):
        x = i
        while fa[x] != x:
            x = fa[x]
        g.setdefault(x, []).append(i)
    return '朋友圈：' + '　'.join('{' + ','.join(map(str, v)) + '}' for v in g.values())


def _fml(S):
    g = _groups(S)
    if 'x' in S and 'y' in S and S.get('_line', 0) >= 11:
        return f"请求 `({S['x']}, {S['y']})`　" + g
    return g




CONFIG = dict(
    num=2076, title='处理含限制条件的好友请求', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='并查集 + 每次扫描全部限制',
    tags=['常用数据结构', '难度分 2131'],
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
    call='Solution().friendRequests(5, [[0,1],[1,2],[2,3]], [[0,4],[1,2],[3,1],[3,4]])',
    expect=[True, False, True, False],
    max_steps=76,
    skip=['res = []', 'flag = True', 'def find'],
    views=[
        dict(type='text', fn=_fml, size=24, h=60),
        dict(type='array', var='fa', label='fa 并查集（fa[i] = i 的是代表元）', cell=80, h=150,
             color=lambda S, i, v: 'blue' if S['fa'][i] == i else None),
        dict(type='array', var=lambda S: [f'{a}-{b}' for a, b in S['restrictions']], label='restrictions（黄 = 当前检查的一条）', cell=90, h=140,
             color=lambda S, i, v: 'yellow' if S.get('_line', 0) >= 20 and S.get('u') is not None and [S['u'], S['v']] == S['restrictions'][i] else None),
        dict(type='array', var='res', label='res（True = 请求成功）', cell=80, h=140,
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), 'fa_x', 'fa_y', ('flag', 'flag', 'yellow')],
    captions={
        'fa = list': '并查集初始化：每个用户自己是自己的祖先',
        'for x, y in requests': lambda S, B, r: (f'处理请求：用户 `{S.x}` 和 `{S.y}`' if B.get('x') != S.get('x') or B.get('y') != S.get('y') else '所有请求处理完了'),
        'fa_x = find(x)': '用户 `x` 所在朋友圈的祖先 `fa_x`',
        'fa_y = find(y)': '用户 `y` 所在朋友圈的祖先 `fa_y`',
        'if fa_x == fa_y': lambda S, B, r: (f'祖先相同 `{S.fa_x}`：已经是朋友（直接或间接）→ ==请求成功==' if S.fa_x == S.fa_y
                                           else f'祖先不同（`{S.fa_x}` ≠ `{S.fa_y}`）：合并会让两个圈连通，先检查限制'),
        'res.append(True)': '成功：`res` 末尾加上 True',
        'for u, v in restrictions': '逐条检查限制（检查完则结束）：合并后 `u`、`v` 会不会连通',
        'fa_u = find(u)': '限制里 `u` 的祖先 `fa_u`',
        'fa_v = find(v)': '限制里 `v` 的祖先 `fa_v`',
        'if (fa_x == fa_u': lambda S, B, r: (f'`x、y` 的两个圈恰好分别装着 `u={S.u}`、`v={S.v}` → 合并会==违反这条限制==' if (S.fa_x == S.fa_u and S.fa_y == S.fa_v) or (S.fa_x == S.fa_v and S.fa_y == S.fa_u)
                                            else f'限制 `({S.u}, {S.v})`（祖先 `{S.fa_u}`、`{S.fa_v}`）不是「一端在 x 圈、一端在 y 圈」，不受影响'),
        'flag = False': '违反限制，`flag = False`，不用再看后面的限制了',
        'break': '跳出限制循环',
        'if flag': lambda S, B, r: ('没有任何限制被违反 → 可以成为朋友' if S.flag else '有限制被违反 → 请求失败'),
        'fa[fa_x] = fa_y': '合并两个圈：`fa[{fa_x}] = {fa_y}`',
        'res.append(False)': '失败：`res` 末尾加上 False',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='每来一个请求，扫一遍所有限制，看会不会误连',
        complexity='时间 `O(q·r·α)`，空间 `O(n)`',
        problem=['`restrictions` 里的两人不能成为朋友（直接或间接），按顺序处理 `requests`',
                 '请求不违反任何限制才成功，成功后两人成为直接朋友',
                 '示例：`n=5`，限制 `[[0,1],[1,2],[2,3]]`，请求 `[[0,4],[1,2],[3,1],[3,4]]` → `[true,false,true,false]`'],
        quote='若fa_x等于fa_u且fa_y等于fa_v，或者反过来fa_x等于fa_v，fa_y等于fa_u，那么将x和y连通后会使得u和v也连通，说明x和y是不能连通的。',
        quote_src='—— yiduobo 题解原文',
        idea=['看成图：人是点，朋友关系是边；限制是「不许连通」的点对',
              '请求 `(x, y)`：用并查集找到两个圈的祖先',
              '逐条枚举限制 `(u, v)`：若它们恰好分属这两个圈，合并就会连通 → 失败；否则合并'],
        summary=['时间 `O(q·r)`（每个请求扫全部限制，数据范围 1000 够用），空间 `O(n)`',
                 '原文为 Python 2 写法，`fa = range(n)` 已改为 `fa = list(range(n))`（Python 3 的 range 不能赋值）',
                 '易错点：限制的两端要先 `find` 成祖先再比较；两种方向（正、反）都要判断',
                 '对比灵神：灵神把限制记在代表元上并启发式合并，yiduobo 每次暴力扫描限制，更直接'],
    ),
)
