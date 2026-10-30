_ST = {}


def _pl(S, B, r):
    _ST['first_i'] = True
    return f'把 `vis` 拷成列表 `points`（{len(S.points)} 个点）：==本轮只用上一代及之前的点==配对'


def _fi(S, B, r):
    if _ST.get('first_i'):
        _ST['first_i'] = False
    elif S.i == B.get('i'):
        return '`i` 枚举完了，这一代的点对算完'
    _ST['new_i'] = True
    return f'`i = {S.i}`：固定第一个点 `{S.points[S.i]}`'


def _fj(S, B, r):
    if _ST.get('new_i'):
        _ST['new_i'] = False
    elif S.j == B.get('j'):
        return f'`j` 枚举完了，换下一个 `i`'
    return f'`j = {S.j}`：配对第二个点 `{S.points[S.j]}`（`j > i` 保证每对只算一次、不会和自己配）'


CONFIG = dict(
    num=3923, title='得到目标点的最少代数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='暴力模拟 · changed 标记',
    tags=[],
    code='''
class Solution(object):
    def minGenerations(self, points, target):
        
        vis = set()
        for x, y, z in points:
            vis.add((x, y, z))
        
        changed = True
        t = (target[0], target[1], target[2])
        res = 0
        while t not in vis and changed:
            changed = False
            points = list(vis)
            for i in range(len(points) - 1):
                for j in range(i + 1, len(points)):
                    x = (points[i][0] + points[j][0]) // 2
                    y = (points[i][1] + points[j][1]) // 2
                    z = (points[i][2] + points[j][2]) // 2
                    p = (x, y, z)
                    if p not in vis:
                        vis.add(p)
                        changed = True
            res += 1
        
        if t not in vis:
            return -1
        return res
''',
    call='Solution().minGenerations([[0,0,0],[5,5,5]], [1,1,1])',
    expect=2,
    views=[
        dict(type='text', size=26, fn=lambda S: (f"目标 `t = {S['t']}`　已经生成了 `res = {S['res']}` 代，`changed = {S['changed']}`" if 't' in S and 'res' in S else '')),
        dict(type='set', var='vis', label='vis（所有出现过的点，黄框 = 刚加入）', fmt=lambda p: f'{p[0]},{p[1]},{p[2]}', h=230),
        dict(type='array', var='points', label='points（本轮开始时 vis 的快照，i / j 是枚举的一对）', h=260,
             pointers={'i': 'blue', 'j': 'pink'}, cell=150,
             color=lambda S, k, v: 'blue' if S.get('i') == k else ('pink' if S.get('j') == k else None)),
    ],
    skip=['y = (', 'p = (x'],
    watch=[('res', 'res', 'green'), ('changed', 'changed', 'orange'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('len(vis)', 'len(vis)')],
    captions={
        'vis = set()': '`vis` 记录所有出现过的点，集合自动去重',
        'vis.add((x, y, z))': '初始点入集合：`vis` 有 {len(vis)} 个点',
        8: '`changed` 标记上一轮有没有出现新点；先设成 `True` 让循环能开始',
        't = (': '目标转成元组 `t = {t}`，才能放进集合里查',
        'res = 0': '`res` 记录已经生成了几代',
        'while t not in vis': lambda S, B, r: ((f'`t = {S.t}` 还不在 vis，且上一轮 `changed = {S.changed}` → 再生成一代'
                                               if S.changed else f'`changed = False`：上一轮没有新点 → 结束循环')
                                              if S.t not in S.vis else f'`t = {S.t}` 已经在 `vis` 里 → ==结束循环=='),
        'changed = False': '本轮先把 `changed` 清零：只有真的加入新点才再置 `True`',
        'points = list': _pl,
        'for i in range': _fi,
        'for j in range': _fj,
        'x = (': '`x = ({points[i][0]} + {points[j][0]}) // 2 = {x}`，向下取整',
        'z = (': '`y = {y}`，`z = {z}` → 中点 `p = ({x}, {y}, {z})`',
        'if p not in vis': lambda S, B, r: (f'`p = {S.p}` 不在 `vis` → ==新点=={""}' if S.p not in S.vis else f'`p = {S.p}` 已经在 `vis` → 跳过'),
        'vis.add(p)': '`vis` 加入新点 `{p}`，现在 {len(vis)} 个点',
        22: '出现了新点 → `changed = True`，说明还可能继续生成',
        'res += 1': '这一代生成完毕：`res` → {res}',
        'if t not in vis': lambda S, B, r: (f'循环结束了 `t = {S.t}` 仍不在 vis → 永远出不来' if S.t not in S.vis else f'`t = {S.t}` 在 `vis` 里 → 能得到'),
        'return -1': '没有新点了还没出现目标 → 返回 `-1`',
        'return res': '`t` 在第 `{res}` 代出现 → 返回 =={res}==',
    },
    cards=dict(
        one_liner='暴力一代代生成中点，直到目标出现或者不再有新点',
        complexity='时间 `O(U^9)`（`U = 7`），空间 `O(U^3)`',
        problem=['三维整数点集 `points`，每代取不同点对的中点（向下取整）收进点集',
                 '求目标点最少在第几代出现；一开始就有返回 `0`，出不来返回 `-1`',
                 '示例：`[[0,0,0],[5,5,5]]`，目标 `[1,1,1]` → `2`'],
        quote='由于题目中元素的取值范围都在0到6之间，那么就意味着最多也只有7 * 7 * 7 = 343种不同的点，因此在这里完全可以直接暴力计算。',
        quote_src='—— yiduobo 题解原文',
        idea=['用 `changed` 标记上一轮有没有出现新点，没有就不用再算了',
              '每轮先把 `vis` 拷成 `points` 快照，两两枚举（`i < j`）算中点',
              '中点第一次出现才加入 `vis` 并把 `changed` 置 `True`'],
        summary=['每轮至少一个新点，最多 343 轮，每轮 `O(343^2)` 对',
                 '易错：枚举用的是快照 `points`，新点要到下一轮才参与配对',
                 '易错：`t not in vis and changed` 退出后还要再判断一次 `t` 在不在',
                 '原文已是 Python 3 可运行写法（`//` 整除），代码未改',
                 '对比灵神：灵神用 `combinations` 和集合长度判断是否有新点，这里手写双重循环 + `changed`'],
    ),
)
