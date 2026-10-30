CONFIG = dict(
    num=3219, title='切蛋糕的最小总开销 II', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='Kruskal + 双指针',
    tags=['最小生成树'],
    code='''
class Solution:
    def minimumCost(self, m: int, n: int, horizontalCut: List[int], verticalCut: List[int]) -> int:
        horizontalCut.sort()
        verticalCut.sort()
        ans = i = j = 0
        for _ in range(m + n - 2):
            if j == n - 1 or i < m - 1 and horizontalCut[i] < verticalCut[j]:
                ans += horizontalCut[i] * (n - j)  # 上下连边
                i += 1
            else:
                ans += verticalCut[j] * (m - i)  # 左右连边
                j += 1
        return ans
''',
    call='Solution().minimumCost(4, 4, [7, 1, 3], [5, 2, 4])',
    expect=44,
    views=[
        dict(type='array', var='horizontalCut', label='horizontalCut（排序后，指针 i = 下一条水平线）', pointers={'i': 'blue'}, h=230, cell=90,
             dim=lambda S, i, v: 'i' in S and i < S['i']),
        dict(type='array', var='verticalCut', label='verticalCut（排序后，指针 j = 下一条垂直线）', pointers={'j': 'pink'}, h=230, cell=90,
             dim=lambda S, i, v: 'j' in S and i < S['j']),
        dict(type='text', h=90, size=30, fn=lambda S: (f"已选 {S['i']} 条水平线、{S['j']} 条垂直线，累计开销 =={S['ans']}==" if 'j' in S and 'ans' in S else '')),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'horizontalCut.sort()': '把切割线看成边：==从小到大排序==，Kruskal 先取最便宜的边 → `{horizontalCut}`',
        'verticalCut.sort()': '垂直线同样排序 → `{verticalCut}`',
        'ans = i = j = 0': '`i`、`j` 分别指向两个数组里还没用的最小边权，`ans` 累计总开销',
        'for _ in range': '一共要选 `m + n - 2` 条边（生成树的边数），所以循环这么多次',
        'if j == n - 1 or': lambda S, B, r: (f'`j == n-1`：垂直线用完了，只能取水平线' if S.j == S.n - 1 else
                                         (f'水平 `{S.horizontalCut[S.i]}` < 垂直 `{S.verticalCut[S.j]}` → 先取水平线' if S.i < S.m - 1 and S.horizontalCut[S.i] < S.verticalCut[S.j]
                                          else (f'水平 `{S.horizontalCut[S.i]}` ≥ 垂直 `{S.verticalCut[S.j]}` → 取垂直线' if S.i < S.m - 1 else f'水平线用完了 → 取垂直线 `{S.verticalCut[S.j]}`'))),
        '上下连边': '水平线 `{B.horizontalCut[B.i]}` 横贯整行：此时已选 `{B.j}` 条垂直线，这条线还要连 `{n - B.j}` 条上下边 → 加 `{B.horizontalCut[B.i]} × {n - B.j}`，`ans` = =={ans}==',
        '左右连边': '垂直线 `{B.verticalCut[B.j]}`：此时已选 `{B.i}` 条水平线，这条线还要连 `{m - B.i}` 条左右边 → 加 `{B.verticalCut[B.j]} × {m - B.i}`，`ans` = =={ans}==',
        'return ans': '所有 `{m + n - 2}` 条边选完，最小总开销 `{ans}`',
    },
    cards=dict(
        one_liner='切割线 = 生成树的边：先选便宜的，双指针归并排序后的两个数组',
        complexity='时间 `O(m log m + n log n)`，空间 `O(1)`',
        problem=['`m × n` 的蛋糕切成 `1 × 1`，水平线 `i` 的每刀开销是 `horizontalCut[i]`，垂直线同理',
                 '每次切一块，开销固定为那条线的开销，求最小总开销',
                 '示例：`m=3, n=2, [1,3], [5]` → `13`'],
        quote='根据最小生成树的 Kruskal 算法，先把边权从小到大排序，然后遍历边，如果边的两个点属于不同连通块，则合并。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把蛋糕画成 `m × n` 个格点，一条水平线 = `n` 条上下连边，一条垂直线 = `m` 条左右连边',
              '取了 `i` 条水平线、`j` 条垂直线后：新水平线只需再连 `n - j` 条，新垂直线只需再连 `m - i` 条',
              '双指针每次取更小的那个边权，共 `m + n - 2` 次'],
        summary=['时间 `O(m log m + n log n)`，瓶颈是排序；空间 `O(1)`',
                 '一条线最多连 `n` 或 `m` 条边，前面已选的另一方向的线会让它少连 `j` 或 `i` 条',
                 '一个数组用完（`j == n - 1`）后要强制取另一个，别越界',
                 '取一次就是一条边权，循环次数固定 `m + n - 2`'],
    ),
)
