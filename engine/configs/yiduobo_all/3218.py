def _cap_cmp(S, B, r):
    h, v, i, j = S.horizontalCut, S.verticalCut, S.i, S.j
    if h[i] > v[j]:
        return (f'水平线 `{h[i]}` > 垂直线 `{v[j]}` → ==先切水平线==；此时竖向已切成 `{j + 1}` 列，'
                f'要切 `{j + 1}` 次')
    return (f'水平线 `{h[i]}` ≤ 垂直线 `{v[j]}` → ==先切垂直线==；此时横向已切成 `{i + 1}` 行，'
            f'要切 `{i + 1}` 次')


CONFIG = dict(
    num=3218, title='切蛋糕的最小总开销 I', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='贪心 · 大代价先切（双路归并）',
    tags=['灵神题单', '其他线性 DP'],
    code='''
class Solution(object):
    def minimumCost(self, m, n, horizontalCut, verticalCut):

        horizontalCut.sort(reverse=True)
        verticalCut.sort(reverse=True)
        i = j = 0
        res = 0
        while i < m - 1 and j < n - 1:
            if horizontalCut[i] > verticalCut[j]:
                res += (j + 1) * horizontalCut[i]
                i += 1
            else:
                res += (i + 1) * verticalCut[j]
                j += 1
        
        while i < m - 1:
            res += n * horizontalCut[i]
            i += 1
        
        while j < n - 1:
            res += m * verticalCut[j]
            j += 1
        
        return res
''',
    call='Solution().minimumCost(4, 3, [2, 7, 4], [3, 5])',
    expect=40,
    views=[
        dict(type='array', var='horizontalCut', label='horizontalCut（从大到小）：水平线的代价', h=190, cell=100,
             pointers={'i': 'blue'}, color=lambda S, k, v: 'green' if k < S.get('i', 0) else None),
        dict(type='array', var='verticalCut', label='verticalCut（从大到小）：垂直线的代价', h=190, cell=100,
             pointers={'j': 'pink'}, color=lambda S, k, v: 'green' if k < S.get('j', 0) else None),
        dict(type='text', size=26, h=70,
             fn=lambda S: (f'已切 `{S["i"]}` 条水平线 → 现有 `{S["i"] + 1}` 行；已切 `{S["j"]}` 条垂直线 → 现有 `{S["j"] + 1}` 列'
                           if S.get('i') is not None and S.get('j') is not None else '先把两个数组都按代价从大到小排好')),
    ],
    watch=[('i（水平已切）', 'i', 'blue'), ('j（垂直已切）', 'j', 'pink'), ('res', 'res', 'green')],
    captions={
        'horizontalCut.sort': '水平线代价从大到小：`{horizontalCut}`',
        'verticalCut.sort': '垂直线代价从大到小：`{verticalCut}`',
        'i = j = 0': '`i`、`j` 是已经切掉的水平 / 垂直线条数',
        'res = 0': '`res` 累计总开销',
        'while i < m - 1 and j < n - 1': lambda S, B, r: ('两个方向都还有线没切，像归并一样比较队头' if S.i < S.m - 1 and S.j < S.n - 1
                                                          else '有一个方向切完了，剩下的方向直接切完'),
        'if horizontalCut[i] > verticalCut[j]': _cap_cmp,
        'res += (j + 1) * horizontalCut[i]': '水平线 `{horizontalCut[i]}` 要切 `{j+1}` 次 → `res` += `{j+1}×{horizontalCut[i]}` = =={res}==',
        'res += (i + 1) * verticalCut[j]': '垂直线 `{verticalCut[j]}` 要切 `{i+1}` 次 → `res` += `{i+1}×{verticalCut[j]}` = =={res}==',
        'while i < m - 1:': lambda S, B, r: (f'只剩水平线：每条都要切 `n = {S.n}` 次（竖向已经全切开了）' if S.i < S.m - 1 else '水平线都切完了'),
        'res += n * horizontalCut[i]': '水平线 `{horizontalCut[i]}` × `n={n}` 次 → `res` = =={res}==',
        'while j < n - 1:': lambda S, B, r: (f'只剩垂直线：每条都要切 `m = {S.m}` 次（横向已经全切开了）' if S.j < S.n - 1 else '垂直线都切完了'),
        'res += m * verticalCut[j]': '垂直线 `{verticalCut[j]}` × `m={m}` 次 → `res` = =={res}==',
        'i += 1': '水平方向多切一条：`i` → {i}',
        'j += 1': '垂直方向多切一条：`j` → {j}',
        'return res': '最小总开销 = =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='越晚切的线，要切的次数越多 → 代价大的先切',
        complexity='时间 `O(m log m + n log n)`，空间 `O(1)`',
        problem=['`m × n` 的蛋糕切成 `1 × 1`，切第 i 条水平线花 `horizontalCut[i]`，垂直线同理',
                 '每次只能切一块蛋糕，代价是固定的，每切一刀分成两块',
                 '示例：`m=3, n=2, horizontalCut=[1,3], verticalCut=[5]` → `13`',
                 '本视频：`m=4, n=3, [2,7,4], [3,5]`'],
        quote='对于同一方向上的切割，就应该先完成代价较大的切割。……对于不同方向上的切割，同样应该先完成代价较大的切割。',
        quote_src='—— yiduobo 题解原文',
        idea=['同一条线切的次数 = 另一方向当前的块数；越晚切，块数越多，次数越多',
              '两条线 x、y，先后顺序代价差只取决于 x 和 y 谁大 → 大的先切',
              '两个数组从大到小排序，二路归并取较大者，乘上另一方向已有的份数'],
        summary=['时间 `O(m log m + n log n)`（排序），空间 `O(1)`',
                 '易错：乘数是另一方向「已切条数 + 1」，不是已切的条数',
                 '一个方向切完后，另一方向每条线要切满 `n` 或 `m` 次',
                 '原文为 Python 2 风格，除删去类型说明外无改动',
                 '3219 题 II 同一做法，只是数据范围更大'],
    ),
)
