C0 = [[50, 45, 20], [95, 37, 53], [45, 23, 12], [60, 10, 10]]


def _bc(S, r, v):
    i, j = S.get('i'), S.get('j')
    if i is None or 'x' not in S:
        return None
    if r == i:
        return 'blue'
    if j is not None and r == j and S.get('_line') in (12, 13):
        return 'pink'
    return None


def _txt(S):
    i, j = S.get('i'), S.get('j')
    if 'x' not in S or i is None:
        return '每个长方体的三边从小到大排好，再整体按 `(x, y, z)` 排序；==最长边 z 当高=='
    c = S['cuboids']
    if j is not None and S.get('_line') in (12, 13) and j < i:
        a = c[j]
        ok = S['x'] >= a[0] and S['y'] >= a[1] and S['z'] >= a[2]
        return f'`{S["x"]} ≥ {a[0]}`、`{S["y"]} ≥ {a[1]}`、`{S["z"]} ≥ {a[2]}` 三条都要成立：{"==能叠在它上面==" if ok else "叠不上"}'
    return '`f[i]` = 以第 `i` 个长方体为最底层时的最大高度（至少是它自己的 `z`）'


CONFIG = dict(
    num=1691, title='堆叠长方体的最大高度', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='三边排序 + 三维 LIS',
    tags=['灵神题单', '动态规划', '难度分 2172'],
    code='''
class Solution(object):
    def maxHeight(self, cuboids):

        cuboids = sorted([sorted(cuboid) for cuboid in cuboids], key=lambda d:(d[0], d[1], d[2]))
        n = len(cuboids)
        f = []
        res = 0
        for i in range(n):
            x, y, z = cuboids[i]
            f.append(z)
            for j in range(i):
                if x >= cuboids[j][0] and y >= cuboids[j][1] and z >= cuboids[j][2]:
                    f[-1] = max(f[-1], f[j] + z)
            res = max(f[-1], res)
        
        return res
''',
    call=f'Solution().maxHeight({C0})',
    expect=190,
    skip=['for j in range(i)', 'n = len'],
    views=[
        dict(type='text', fn=_txt, size=24, h=80),
        dict(type='table', var='cuboids', label='cuboids（每行排好序的 x, y, z；蓝 = i，粉 = j）', h=260, cell=64,
             rows=lambda S: [f'#{k}' for k in range(len(S['cuboids']))] if 'cuboids' in S else [],
             cols=lambda S: ['x', 'y', 'z'], color=lambda S, r, c, v: _bc(S, r, v)),
        dict(type='array', var='f', label='f[i]（以第 i 个为底的最大高度）', h=180, cell=90),
    ],
    watch=['i', 'j', 'z', ('res', 'res', 'green')],
    captions={
        'cuboids = sorted': '先把每个长方体的三边排序（小 → 大），再对所有长方体按 `(x, y, z)` 排序',
        'f = []': '`f[i]`：以第 `i` 个长方体为最底层的最大高度',
        'res = 0': '`res` 记录目前最高的堆叠',
        'for i in range(n)': lambda S, B, r: (f'`i = {S.i}`' if S.i != B.get('i') or 'i' not in B else '所有长方体都处理完了'),
        'x, y, z = cuboids[i]': '取第 `{i}` 个：`x, y, z = {x}, {y}, {z}`，==最长边 `z` 当高=='
        ,
        'f.append(z)': '先假设上面一个也不放：`f[{i}] = z = {z}`',
        'if x >= cuboids[j][0]': lambda S, B, r: (f'`j = {S.j}`：{S.cuboids[S.j]} 三条边都 ≤ `({S.x}, {S.y}, {S.z})` → ==能叠上去=='
                                                  if S.x >= S.cuboids[S.j][0] and S.y >= S.cuboids[S.j][1] and S.z >= S.cuboids[S.j][2]
                                                  else f'`j = {S.j}`：{S.cuboids[S.j]} 有一条边超过 `({S.x}, {S.y}, {S.z})` → 不能叠'),
        'f[-1] = max(f[-1], f[j] + z)': '`f[{i}] = max({B.f[-1]}, f[{j}] + z = {f[j]} + {z})` = =={f[-1]}==',
        'res = max(f[-1], res)': '`res = max(f[{i}] = {f[-1]}, {B.res})` = =={res}==',
        'return res': '最大高度 =={ret}==',
    },
    cards=dict(
        one_liner='三边排序后一一对比，最长边当高，再做最长上升子序列',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`n` 个长方体可以旋转，上面一个的三边都 ≤ 下面一个的才能叠',
                 '选子集堆叠，求最大总高度',
                 '示例：`[[50,45,20],[95,37,53],[45,23,12]]` → `190`'],
        quote='判断一个箱子能否放在另一个箱子上面，只需要将两个箱子的边从小到大进行排序，然后一一对比即可。另外还有一个隐藏条件，最高高度必然是选择箱子的最长边作为高堆叠出来的。',
        quote_src='—— yiduobo 题解原文',
        idea=['证明：三边排序后某一项不满足，调换顺序也不可能同时满足，所以只比较排序后的三边',
              '若某个箱子不是最长边当高，改成最长边当高，上下的堆叠关系仍然成立，结果更优',
              '排序后做 LIS：`f[i] = max(f[i], f[j] + z[i])`，要求 `x,y,z` 三项都 `j ≤ i`'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '易错：先排每个箱子的三边，再整体排序',
                 '易错：`f[i]` 初值是自己的最长边 `z`，不是 0',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神三维排序后只比较 `l`、`h`（`w` 排序后恒成立），yiduobo 三项都比较'],
    ),
)
