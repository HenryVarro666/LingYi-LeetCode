CONFIG = dict(
    num=2643, title='一最多的行', difficulty='Easy', category='网格图',
    author='yiduobo', technique='遍历行 sum 统计 1 的数目', tags=[],
    code='''
class Solution(object):
    def rowAndMaximumOnes(self, mat):

        res = [0, 0]
        for i in range(len(mat)):
            cnt = sum(mat[i])
            if cnt > res[1]:
                res = [i, cnt]
        
        return res
''',
    call='Solution().rowAndMaximumOnes([[0,0,1,0],[1,1,0,1],[1,1,0,0],[0,0,0,0]])',
    expect=[1, 3],
    views=[
        dict(type='grid', var='mat', h=330,
             color=lambda S, i, j, v: ('green' if i == S['res'][0] and S['res'][1] > 0 else 'blue' if i == S.get('i') else None) if 'res' in S else None),
        dict(type='text', fn=lambda S: f"当前最优：第 `{S['res'][0]}` 行，`{S['res'][1]}` 个 1" if 'res' in S else '', h=60),
    ],
    watch=[('i', 'i', 'blue'), ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'res = [0, 0]': '答案先设 `[0, 0]`：第 0 行、0 个 1',
        'cnt = sum': '每行只有 0/1，行的和就是 1 的数目：第 `{i}` 行 `cnt` = =={cnt}==',
        'if cnt > res[1]': '`{cnt} > {res[1]}`？严格大于才替换，并列时保留行号小的',
        'res = [i, cnt]': '更新答案为 `{res}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='每行 sum 就是 1 的个数，取最大',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['二进制矩阵，求 1 最多的行下标及 1 的数量',
                 '并列时取行下标最小的',
                 '示例：`[[0,0],[1,1],[0,0]]` → `[1,2]`'],
        quote='直接遍历每一行，统计行中一的数目并取最大值作为答案就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['Python 可以直接用 `sum` 求一行的和，等于 1 的数目',
              '答案用 `res = [行号, 个数]` 保存，初值 `[0, 0]`',
              '只在 `cnt > res[1]` 时替换，所以并列取靠前的行'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '全 0 矩阵时答案保持 `[0, 0]`，符合题意',
                 '必须严格大于，不能用 `>=`'],
    ),
)
