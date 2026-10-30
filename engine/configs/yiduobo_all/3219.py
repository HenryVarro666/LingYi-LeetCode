CONFIG = dict(
    num=3219, title='切蛋糕的最小总开销 II', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='贪心：大代价先切 + 二路归并',
    tags=['最小生成树'],
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
    call='Solution().minimumCost(4, 4, [7, 1, 3], [5, 2, 4])',
    expect=44,
    views=[
        dict(type='array', var='horizontalCut', label='horizontalCut（从大到小；i = 下一条要切的）', pointers={'i': 'blue'}, h=230, cell=90,
             dim=lambda S, i, v: 'i' in S and i < S['i']),
        dict(type='array', var='verticalCut', label='verticalCut（从大到小；j = 下一条要切的）', pointers={'j': 'pink'}, h=230, cell=90,
             dim=lambda S, i, v: 'j' in S and i < S['j']),
        dict(type='text', h=90, size=30, fn=lambda S: (f"已切水平 {S['i']} 刀线、垂直 {S['j']} 刀线，总代价 =={S['res']}==" if 'j' in S and 'res' in S else '')),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    captions={
        'horizontalCut.sort': '越晚切的线要切的块越多 → ==代价大的先切==，所以从大到小排：`{horizontalCut}`',
        'verticalCut.sort': '垂直线同样从大到小：`{verticalCut}`',
        'i = j = 0': '`i`、`j` 指向两个数组里还没切的最大代价',
        'res = 0': '`res` 累计总代价',
        'while i < m - 1 and j < n - 1': lambda S, B, r: (f'两个方向都还有线没切（`i={S.i}`，`j={S.j}`）→ 二路归并，继续' if S.i < S.m - 1 and S.j < S.n - 1
                                                          else '有一个方向切完了 → 跳出归并，处理剩下的'),
        'if horizontalCut[i] > verticalCut[j]': lambda S, B, r: (f'水平 `{S.horizontalCut[S.i]}` > 垂直 `{S.verticalCut[S.j]}` → 先切水平线（交换顺序证明：大的先切不亏）' if S.horizontalCut[S.i] > S.verticalCut[S.j]
                                                                  else f'水平 `{S.horizontalCut[S.i]}` ≤ 垂直 `{S.verticalCut[S.j]}` → 先切垂直线'),
        'res += (j + 1) * horizontalCut[i]': '已有 `{B.j}` 刀垂直线，蛋糕分成 `{B.j + 1}` 列，这条水平线要切 `{B.j + 1}` 次：`{B.horizontalCut[B.i]} × {B.j + 1}` → `res` = {res}',
        'res += (i + 1) * verticalCut[j]': '已有 `{B.i}` 刀水平线，分成 `{B.i + 1}` 行，这条垂直线要切 `{B.i + 1}` 次：`{B.verticalCut[B.j]} × {B.i + 1}` → `res` = {res}',
        'res += n * horizontalCut[i]': '垂直线都切完了，共 `{n}` 列，每条水平线切 `{n}` 次：加 `{B.horizontalCut[B.i]} × {n}` → `res` = {res}',
        'res += m * verticalCut[j]': '水平线都切完了，共 `{m}` 行，每条垂直线切 `{m}` 次：加 `{B.verticalCut[B.j]} × {m}` → `res` = {res}',
        'return res': '最小总代价 `{res}`',
    },
    cards=dict(
        one_liner='越晚切的线要切的次数越多，所以代价大的线先切',
        complexity='时间 `O(m log m + n log n)`，空间 `O(1)`',
        problem=['`m × n` 的蛋糕切成 `1 × 1`，水平线、垂直线每刀的代价由数组给出',
                 '切一块蛋糕的代价固定为那条线的代价，求总代价最小',
                 '本视频：`m=4, n=4, [7,1,3], [5,2,4]` → `44`'],
        quote='对于同一方向上的切割，就应该先完成代价较大的切割。……两种切割顺序对应的代价就分别是x * h + y * (v + 1)以及x * (h + 1) + y * v，可以发现，这两种代价的大小关系只与x和y的大小有关',
        quote_src='—— yiduobo 题解原文',
        idea=['线越晚切，已被分成的块越多，要切的次数越多',
              '同方向、不同方向都用交换论证：==大代价先切==更省',
              '两个数组从大到小排序，像归并排序一样每次取较大的'],
        summary=['时间 `O(m log m + n log n)`，空间 `O(1)`',
                 '水平线的切数 = 已切垂直线数 + 1；垂直线同理，不要写反',
                 '一个方向切完后，剩下的线每条切 `n`（或 `m`）次',
                 '原文是 Python 2 风格的类写法，但这段代码在 Python 3 下无需修改',
                 '对比灵神：灵神从小到大、按生成树边数算；yiduobo 从大到小、按切割次数算，结果相同'],
    ),
)
