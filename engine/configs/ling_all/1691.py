C0 = [[50, 45, 20], [95, 37, 53], [45, 23, 12], [60, 10, 10]]


def _boxes(S):
    return ['·'.join(map(str, c)) for c in S['cuboids']]


def _bc(S, k, v):
    i, j = S.get('i'), S.get('j')
    if i is None:
        return None
    if k == i:
        return 'blue'
    if j is not None and k == j and S.get('_line') in (11, 12, 13):
        return 'pink'
    return None


def _txt(S):
    i, j = S.get('i'), S.get('j')
    if i is None or 'f' not in S or 'l2' not in S:
        return '每个长方体先把三条边排序，再按（长, 宽, 高）整体排序；==最长边当高=='
    c = S['cuboids']
    if j is not None and S.get('_line') in (11, 12, 13) and j < i:
        ok = c[j][1] <= S['l2'] and c[j][2] <= S['h2']
        return f'`{c[j][1]} ≤ {S["l2"]}` 且 `{c[j][2]} ≤ {S["h2"]}`：{"==能堆上去==" if ok else "堆不上"}（w 排序后必然 ≤）'
    return f'`f[i]` = 以第 `i` 个长方体为底、能堆出的最大高度'


CONFIG = dict(
    num=1691, title='堆叠长方体的最大高度', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='边排序 + LIS 式 DP',
    tags=['灵神题单', '动态规划', '难度分 2172'],
    code='''
class Solution:
    def maxHeight(self, cuboids: List[List[int]]) -> int:
        for c in cuboids:
            c.sort()
        cuboids.sort()
        f = [0] * len(cuboids)
        for i, (_, l2, h2) in enumerate(cuboids):
            for j, (_, l1, h1) in enumerate(cuboids[:i]):
                if l1 <= l2 and h1 <= h2:  # 排序后，w1 <= w2 恒成立
                    f[i] = max(f[i], f[j])  # cuboids[j] 可以堆在 cuboids[i] 上
            f[i] += h2
        return max(f)
''',
    call=f'Solution().maxHeight({C0})',
    expect=190,
    skip=['for j, (_, l1, h1)'],
    views=[
        dict(type='text', fn=_txt, size=24, h=80),
        dict(type='table', var='cuboids', label='cuboids（每行 = 排好序的 w, l, h；蓝 = i，粉 = j）', h=260, cell=64,
             rows=lambda S: [f'#{k}' for k in range(len(S['cuboids']))], cols=lambda S: ['w', 'l', 'h'],
             color=lambda S, r, c, v: _bc(S, r, v)),
        dict(type='array', var='f', label='f[i]（以 cuboids[i] 为底的最大堆叠高度）', h=180, cell=90,
             pointers={'i': 'blue'}),
    ],
    watch=['i', 'j', 'l2', 'h2', ('max(f)', 'max(f) if "f" in S else 0', 'green')],
    captions={
        'for c in cuboids': lambda S, B, r: (f'逐个处理长方体 `{S.c}`' if 'c' in S and S.c is not B.get('c') else '每个长方体的三边都排好序了'),
        'c.sort()': lambda S, B, r: f'把这个长方体的三条边排序：`{S.c}`，==最长边当高==',
        'cuboids.sort()': '再把所有长方体整体排序：保证可堆叠的长方体 `j` 一定排在 `i` 前面，只需看 `j < i`',
        'f = [0]': '`f[i]`：以 `cuboids[i]` 为最底层、能堆出的最大高度',
        'for i, (_, l2, h2)': lambda S, B, r: (f'`i = {S.i}`：长方体 `{S.cuboids[S.i]}`，当作最底层' if S.get('i') is not None and S.get('i') != B.get('i') else '都算完了'),
        'if l1 <= l2 and h1 <= h2': lambda S, B, r: (f'`j = {S.j}`：`l1 = {S.l1} ≤ l2 = {S.l2}`，`h1 = {S.h1} ≤ h2 = {S.h2}` → ==能堆在上面==（`w1 <= w2` 排序后恒成立）'
                                                     if S.l1 <= S.l2 and S.h1 <= S.h2 else f'`j = {S.j}`：`l1 = {S.l1}`，`h1 = {S.h1}` 放不进 `l2 = {S.l2}`、`h2 = {S.h2}` → 不能堆'),
        'f[i] = max(f[i], f[j])': '`f[{i}] = max({B.f[i]}, f[{j}] = {f[j]})` = =={f[i]}==：把 `j` 能堆出的最好结果接到上面',
        'f[i] += h2': '`f[{i}] += {h2}` → =={f[i]}==：底层自己的高度（最长边）加上去',
        'return max(f)': '最高的堆叠 = `max(f)` = =={ret}==',
    },
    cards=dict(
        one_liner='三边排序后，能放就放；每个长方体都用最长边当高',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['给 `n` 个长方体，可旋转；上面的三条边都不超过下面的，就能堆叠',
                 '选一个子集堆起来，求最大总高度',
                 '示例：`[[50,45,20],[95,37,53],[45,23,12]]` → `190`'],
        quote='排序后，答案对应的长方体子序列可直接按照从左到右的顺序堆叠，从而保证了状态转移的正确性。',
        quote_src='—— 灵茶山艾府题解（答疑）',
        idea=['先对每个长方体的三边排序，再对整个数组排序，==w 自动满足==',
              '`A` 能堆在 `B` 上，等价于把 `A` “装进” `B`：短对短、中对中、长对长，所以最长边竖着放最高',
              '只剩 `l`、`h` 两维：`f[i] = max(f[j]) + h2`，这就是 LIS 的模板'],
        summary=['时间 `O(n^2)`，空间 `O(n)`；灵神提到用动态开点二维线段树可做到 `O(n log^2 n)`',
                 '易错：必须先每个盒子内部排序，再整体排序，顺序不能反',
                 '易错：`f[i]` 要先取子问题最大值，最后才加上自己的高 `h2`',
                 '同类题：300 最长递增子序列、354 俄罗斯套娃'],
    ),
)
