def _edge(S):
    if 'v' in S and 'res' in S:
        return f"当前边 `({S['x']}, {S['y']}, 权 {S['v']})`　已加入 ==`{S['res']}`== 条"
    return ''


CONFIG = dict(
    num=3887, title='增量偶权环查询', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='带权并查集 · 奇偶性 xor',
    tags=['灵神题单', '常用数据结构', '难度分 2128'],
    code='''
class Solution(object):
    def numberOfEdgesAdded(self, n, edges):
        
        fa = [index for index in range(n)]
        xor = [0] * n

        def find(fa, xor, x):
            if fa[x] != x:
                ori = fa[x]
                fa[x] = find(fa, xor, fa[x])
                xor[x] ^= xor[ori]
            return fa[x]

        res = 0
        for x, y, v in edges:
            fa_x = find(fa, xor, x)
            fa_y = find(fa, xor, y)
            if fa_x == fa_y:
                if xor[x] ^ xor[y] == v:
                    res += 1
            else:
                res += 1
                fa[fa_x] = fa_y
                xor[fa_x] = xor[x] ^ xor[y] ^ v

        return res
''',
    call='Solution().numberOfEdgesAdded(4, [[0,1,1],[1,2,1],[0,2,1],[2,3,0],[1,3,0]])',
    expect=3,
    views=[
        dict(type='text', h=70, size=30, fn=_edge),
        dict(type='array', var='fa', label='fa（最高祖先）', h=190),
        dict(type='array', var='xor', label='xor（到 fa 的边权和奇偶性）', h=190,
             color=lambda S, i, v: 'orange' if v else None),
        dict(type='calls', h=220),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), 'v', ('res', 'res', 'green')],
    captions={
        'fa = [index': '`fa[i] = i`：开始每个点自成一块',
        'xor = [0]': '`xor[i]`：i 到最高祖先的边权和==奇偶性==，开始都是 0',
        'for x, y, v in edges': '处理下一条边 `({x}, {y}, {v})`',
        'if fa[x] != x': lambda S, B, r: (f'`fa[{S.x}] != {S.x}`：还没到最高祖先，继续往上找' if S.fa[S.x] != S.x
                                          else f'`fa[{S.x}] = {S.x}`：{S.x} 就是最高祖先'),
        'ori = fa[x]': '先记下原来的父亲 `ori = {ori}`：压缩后 `fa[x]` 会变，`xor[ori]` 还要用',
        'fa[x] = find': '递归找到最高祖先，`fa[x]` 直接指向它 → {fa[x]}',
        'xor[x] ^= xor[ori]': 'x 到祖先 = x 到 ori ^ ori 到祖先：`xor[x]` → =={xor[x]}==',
        'return fa[x]': '返回最高祖先 `{ret}`',
        'fa_x = find': '`find(x)`：找 x 的最高祖先，并把 `xor[x]` 更新为到祖先的奇偶性',
        'fa_y = find': '同理 `find(y)`：找 y 的最高祖先',
        'if fa_x == fa_y': lambda S, B, r: (f'`fa_x == fa_y == {S.fa_x}`：同一连通块，加边会成环' if S.fa_x == S.fa_y
                                            else f'`fa_x = {S.fa_x} != fa_y = {S.fa_y}`：不同连通块，必然能连'),
        'if xor[x] ^ xor[y] == v': lambda S, B, r: (f'`xor[x] ^ xor[y] = {S.xor[S.x] ^ S.xor[S.y]}`，边权 `v = {S.v}`：'
                                                    + ('相等，环权和为偶数 → ==可以加==' if S.xor[S.x] ^ S.xor[S.y] == S.v
                                                       else '不等，环权和为奇数 → ==舍弃==')),
        'res += 1': '这条边加入，`res` = =={res}==',
        'fa[fa_x] = fa_y': '把 x 这块的祖先接到 y 的祖先下：`fa[{fa_x}] = {fa_y}`',
        'xor[fa_x] = ': '`fa_x → x → y → fa_y` 三段奇偶性异或：`xor[fa_x] = {xor[x]} ^ {xor[y]} ^ {v}` = =={xor[fa_x]}==',
        'return res': '最终加入 `{res}` 条边',
    },
    skip=['return fa[x]'],
    max_steps=110,
    cards=dict(
        one_liner='两点间所有简单路径的奇偶性相同，用 xor 数组维护到祖先的奇偶性',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`n` 个点的无向图，初始没有边；边权 `w` 为 `0` 或 `1`',
                 '按顺序处理每条边：加入后每个环的边权和仍为偶数才加入，否则舍弃',
                 '返回最终加入的边数。示例：`n=3, [[0,1,1],[1,2,1],[0,2,1]]` → `2`',
                 '本视频：`n=4`，5 条边 → `3`'],
        quote='若两个点u和v是环上的两点，那么u到v的所有简单路径的权重和的奇偶性必然相同。理由是任取两条简单路径，都可以形成一个环，而题目要求环的权重和为偶数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`xor[x]` 记录 x 到最高祖先的边权和奇偶性，`find` 时路径压缩并同步异或',
              '同一块里的边：`xor[x] ^ xor[y] == v` 才不会产生奇环',
              '不同块：连上，把 `fa_x` 接到 `fa_y`，只需改 `xor[fa_x]` 为 `xor[x] ^ xor[y] ^ v`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`find` 里要先记 `ori = fa[x]`，再递归，再异或 `xor[ori]`',
                 '合并只修正 `xor[fa_x]`：该树上所有点查祖先都会经过它',
                 '被舍弃的边不改变并查集，只有成功加入的才合并',
                 '对比灵神：灵神把 find/merge 封装成类并让 merge 返回布尔值，思路相同'],
    ),
)
