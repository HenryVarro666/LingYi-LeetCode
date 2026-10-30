

CONFIG = dict(
    num=3161, title='物块放置查询', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='倒推 · 并查集合并 + 树状数组',
    tags=['灵神题单·常用数据结构', '难度分 2513'],
    code='''
class Solution(object):
    def getResults(self, queries):

        ma = 16
        f = [0] * (ma + 1)
        left = []
        right = []

        cut_pos = []
        for q in queries:
            if q[0] == 1:
                cut_pos.append(q[1] * 2 + 1)
        cut_pos.sort()
        

        def update(x, v):
            while x <= ma:
                f[x] = max(f[x], v)
                x += x & -x

        pre = 0
        for p in cut_pos:
            for index in range(pre, p):
                left.append(pre)
                right.append(p - 1)
            update(p - 1, p - pre)
            pre = p
        
        for index in range(pre, ma + 1):
            left.append(pre)
            right.append(ma)
        update(ma, ma - pre + 1)

        def get(x):
            v = 0
            while x:
                v = max(v, f[x])
                x -= x & -x
            return v
        
        def find(g, x):
            if g[x] != x:
                g[x] = find(g, g[x])
            return g[x]

        res = []
        for q in queries[::-1]:
            if q[0] == 1:
                q[1] = q[1] * 2 + 1
                if q[1] > ma:
                    continue
                new_l = find(left, q[1] - 1)
                new_r = find(right, q[1])
                
                left[q[1]] = new_l
                right[q[1] - 1] = new_r

                update(new_r, new_r - new_l + 1)
            
            else:
                q[1] *= 2
                q[2] *= 2
                res.append(get(q[1]) >= q[2] or q[1] - find(left, q[1]) + 1 >= q[2])

        res.reverse()
        return res
''',
    call='Solution().getResults([[1,3],[2,3,3],[1,1],[2,3,3],[2,3,2]])',
    expect=[True, False, True],
    views=[
        dict(type='array', var='left', label='left[i]：位置 i 所在区间的起点（并查集）', cell=54, h=150,
             pointers={'new_l': 'blue'}, color=lambda S, i, v: 'blue' if v == i else None),
        dict(type='array', var='right', label='right[i]：位置 i 所在区间的终点（并查集）', cell=54, h=150,
             pointers={'new_r': 'pink'}, color=lambda S, i, v: 'pink' if v == i else None),
        dict(type='array', var='f', label='f：树状数组（前缀内的最长区间长度）', cell=54, h=150,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='text', fn=lambda S: ('倒序处理 `' + str(S['q']) + '`' if 'q' in S and 'res' in S else '坐标全部乘 2：障碍物放在 `2x+1`（右区间起点），查询点在 `2x`'), size=26, h=70),
    ],
    watch=['pre', 'p', 'new_l', 'new_r', ('res', 'res', 'green')],
    captions={
        'ma = 16': '`ma`：值域上限（原文 100000，这里缩成 16 便于演示）；坐标都乘 2，所以够用',
        'f = [0]': '`f`：树状数组，`f[x]` = 到 x 为止最长的完整区间',
        'cut_pos.append': '障碍物 `x={q[1]}` 记为切点 `2x+1 = {cut_pos[-1]}`：==乘 2 再加 1==，让切点属于右区间，避免两区间共用一个点',
        'cut_pos.sort()': '切点排序：`{cut_pos}`。先把所有障碍物一次摆好，得到==最终==的区间划分',
        'for p in cut_pos': lambda S, B, r: ('切点都处理完了，只剩最后一段 `[{}, ma]`'.format(S.pre) if S.pre == S.p else '处理切点 `p = {}`：它左边的区间是 `[{}, {}]`'.format(S.p, S.pre, S.p - 1)),
        'update(p - 1, p - pre)': '区间 `[{pre},{p-1}]` 长 `{p - pre}`，记在右端点 `{p-1}` 的树状数组里',
        'pre = p': '下一段从 `{p}` 开始',
        'update(ma, ma': '最后一段 `[{pre},{ma}]` 长 `{ma - pre + 1}`，记在 `{ma}`',
        'for q in queries[::-1]': '`q = {q}`：==倒序==处理，障碍物只增不减，倒过来就变成「只合并不分裂」',
        'new_l = find': '合并：切点 `{q[1]}` 左边那个区间的起点 = `{new_l}`',
        'new_r = find': '切点 `{q[1]}` 右边那个区间的终点 = `{new_r}`',
        'left[q[1]] = new_l': '把右区间的起点指向 `{new_l}`：拆掉这个障碍物，两个区间并成一个',
        'right[q[1] - 1] = new_r': '左区间的终点指向 `{new_r}`',
        'update(new_r, new_r': '新区间 `[{new_l},{new_r}]` 长 `{new_r - new_l + 1}`，更新树状数组（旧的小区间不必删：它更短，不会影响答案）',
        'q[1] *= 2': '查询点也乘 2：`{q[1]}`；`sz` 同样乘 2 → `{q[2]}`',
        'res.append': '查询点 `{q[1]}`：取前缀内最大完整区间 `get({q[1]})`，再和末段 `{q[1]} - 区间起点 + 1` 比，任一 ≥ `{q[2]}` 就能放',
        'res.reverse()': '倒序算出来的，翻转回原顺序',
    },
    skip=['left.append', 'right.append', 'for index in range', 'cut_pos = []', 'left = []', 'right = []', 'res = []', 'v = 0', 'x -= x & -x', 'x += x & -x', 'while x <= ma', 'while x:', 'v = max', 'f[x] = max', 'if g[x] != x', 'g[x] = find', 'return g[x]', 'return v'],
    max_steps=75,
    cards=dict(
        one_liner='只加障碍不删障碍：倒过来，分裂变成合并，并查集搞定',
        complexity='时间 `O(U + q log U)`，空间 `O(U)`',
        problem=['数轴上两种操作：1 = 在 x 放障碍物；2 = 问 `[0,x]` 内能否放下长 `sz` 的物块',
                 '示例：`[[1,3],[2,3,3],[1,1],[2,3,3],[2,3,2]]` → `[True, False, True]`'],
        quote='注意到本题中只有设置障碍的操作，没有移除障碍的操作，这也就意味着只有区间分割操作，没有区间合并操作。对于这类问题，一种经典的处理方法就是倒推。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把所有障碍物摆好，得到最终的区间；再倒序遍历，每个障碍物变成「合并左右两区间」',
              '合并用并查集 `left/right` 找区间端点；新区间长度写进树状数组（只会变大，取 max 即可）',
              '分割点属于两个区间会冲突：坐标乘 2，障碍物放在 `2x+1`，查询点放在 `2x`'],
        summary=['时间 `O(U + q log U)`，空间 `O(U)`',
                 '原文 `ma = 100000`，为了演示缩成 `16`（逻辑不变）',
                 '查询答案 = 前缀最大完整区间 ∥ 查询点所在区间到查询点的一段',
                 '对比灵神：灵神正序 + 有序集合 + 线段树；yiduobo 倒序 + 并查集 + 树状数组，免去平衡树'],
    ),
)
