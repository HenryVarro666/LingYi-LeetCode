CONFIG = dict(
    num=661, title='图片平滑器', difficulty='Easy', category='模拟',
    author='yiduobo', technique='逐格累加邻居再取平均',
    code='''
class Solution(object):
    def imageSmoother(self, M):

        m = len(M)
        n = len(M[0])

        res = [[0] * n for _ in range(m)]

        for i in range(m):
            for j in range(n):
                res[i][j] = M[i][j]
                cnt = 1

                if i > 0:
                    if j > 0:
                        res[i][j] += M[i - 1][j - 1]
                        cnt += 1
                    res[i][j] += M[i - 1][j]
                    cnt += 1
                    if j < n - 1:
                        res[i][j] += M[i - 1][j + 1]
                        cnt += 1
                
                if j > 0:
                    res[i][j] += M[i][j - 1]
                    cnt += 1
                if j < n - 1:
                    res[i][j] += M[i][j + 1]
                    cnt += 1
                
                if i < m - 1:
                    if j > 0:
                        res[i][j] += M[i + 1][j - 1]
                        cnt += 1
                    res[i][j] += M[i + 1][j]
                    cnt += 1
                    if j < n - 1:
                        res[i][j] += M[i + 1][j + 1]
                        cnt += 1

                res[i][j] //= cnt

        return res
''',
    call='Solution().imageSmoother([[100,200,100],[200,50,200]])',
    expect=[[137, 141, 137], [137, 141, 137]],
    skip=['m = len', 'n = len', 'res = [[0]', 'cnt = 1', 'cnt += 1'],
    max_steps=90,
    views=[
        dict(type='grid', var='M', label='M（原图；蓝框 = 当前格子 (i,j)）', cell=84, h=300,
             cursors=[('i', 'j', 'blue')]),
        dict(type='grid', var='res', label='res（平滑结果，边累加边更新）', cell=84, h=300,
             cursors=[('i', 'j', 'yellow')]),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('cnt', 'cnt', 'orange'), ('res[i][j]', 'res[i][j]', 'green')],
    captions={
        'res = [[0]': '建一个同样大小的 `res`，用来存累加和再变成平均值',
        'res[i][j] = M[i][j]': '先放入自己：`res[{i}][{j}] = {M[i][j]}`，`cnt` 记已累加的格子数',
        'if i > 0:': lambda S, B, r: (f'`i = {S.i} > 0` → 有上一行，累加上方三个邻居' if S.i > 0 else f'`i = 0`：没有上一行 → 跳过上方'),
        'if j > 0:': lambda S, B, r: (f'`j = {S.j} > 0` → 有左邻居，累加' if S.j > 0 else '`j = 0`：没有左邻居 → 跳过'),
        'if j < n - 1:': lambda S, B, r: (f'`j = {S.j} < n - 1 = {S.n - 1}` → 有右邻居，累加' if S.j < S.n - 1 else f'`j = {S.j}` 已是最后一列：没有右邻居 → 跳过'),
        'if i < m - 1:': lambda S, B, r: (f'`i = {S.i} < m - 1 = {S.m - 1}` → 有下一行，累加下方三个邻居' if S.i < S.m - 1 else f'`i = {S.i}` 已是最后一行：没有下一行 → 跳过下方'),
        'res[i][j] += M[': '累加邻居：`res[{i}][{j}]` → =={res[i][j]}==',
        'res[i][j] //= cnt': '累加完毕：和 `{B.res[i][j]}` ÷ 个数 `{cnt}`，向下取整 → ==`{res[i][j]}`==',
        'return res': '全部格子处理完，返回 `res`',
    },
    cards=dict(
        one_liner='每格累加自己和八邻域，再除以实际格子数',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['给一张灰度图 `M`，每个格子换成它自己和周围 8 个格子的平均值（向下取整）',
                 '边和角上的格子，邻居不足 8 个，只算存在的格子',
                 '本视频：`[[100,200,100],[200,50,200]]` → 2 行 3 列，角上只有 4 个格子，中间列有 6 个'],
        quote='将该点以及周围8个点的值累加到答案矩阵的对应位置上，累加过程中需要注意判断边和角上的特殊情况。累加完成后，最后只需要再除以周围格子总数即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['对每个 `(i,j)`：先放入自己，`cnt = 1`',
              '逐个判断 8 个方向是否越界，没越界就累加并 `cnt += 1`',
              '最后用累加和除以 `cnt`，边和角自然少除几个'],
        summary=['时间 `O(mn)`，空间 `O(mn)`（结果另存，不能原地改 `M`）',
                 '易错：必须读原图 `M`，写到 `res`，否则会被已平滑的值污染',
                 '易错：用实际邻居个数 `cnt` 做除数，不是固定的 9',
                 '原文为 Python 2 写法，整数除法 `/=` 已改为 `//=`'],
    ),
)
