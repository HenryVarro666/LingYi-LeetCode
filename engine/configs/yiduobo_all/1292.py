def _sq(S, i, j, v):
    if 'res' not in S or 'i' not in S or 'j' not in S:
        return None
    r = S['res']
    if S['i'] <= i <= S['i'] + r and S['j'] <= j <= S['j'] + r:
        return 'yellow'
    return None


def _txt(S):
    if 'res' not in S or 'i' not in S or 'j' not in S:
        return ''
    r = S['res']
    i, j = S['i'], S['j']
    if 'tmp' in S and i + r < S['m'] and j + r < S['n']:
        return f"右下角 `({i + r},{j + r})`：矩形和 tmp = =={S['tmp']}==，阈值 `{S['threshold']}`"
    return f"左上角 `({i},{j})`，已知最大边长 res = `{r}`"


CONFIG = dict(
    num=1292, title='元素和小于等于阈值的正方形的最大边长', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='二维前缀和 + 从已知答案+1 检测',
    tags=['二维前缀和', '难度分 1735'],
    code='''
class Solution(object):
    def maxSideLength(self, mat, threshold):

        m = len(mat)
        n = len(mat[0])
        s = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                s[i][j] = mat[i][j]
                if i == 0:
                    if j == 0:
                        continue
                    else:
                        s[i][j] += s[i][j - 1]
                elif j == 0:
                    s[i][j] += s[i - 1][j]
                else:
                    s[i][j] += s[i][j - 1] + s[i - 1][j] - s[i - 1][j - 1]
        
        f = [[0] * n for _ in range(m)]
        res = 0
        for i in range(m):
            for j in range(n):
                while res < min(m - i, n - j):
                    if i == 0:
                        if j == 0:
                            tmp = s[i + res][j + res]
                        else:
                            tmp = s[i + res][j + res] - s[i + res][j - 1]
                    elif j == 0:
                        tmp = s[i + res][j + res] - s[i - 1][j + res]
                    else:
                        tmp = s[i + res][j + res] - s[i - 1][j + res] - s[i + res][j - 1] + s[i - 1][j - 1]

                    if tmp > threshold:
                        break
                
                    res += 1

        return res
''',
    call='Solution().maxSideLength([[1,1,3],[1,1,3],[1,1,3]], 4)',
    expect=2,
    views=[
        dict(type='grid', var='mat', cursors=[('i', 'j', 'yellow', '')], color=_sq, h=200, label='mat（黄=正在检测的正方形）'),
        dict(type='table', var='s', h=250, label='s[i][j] = 以 (0,0) 为左上角、(i,j) 为右下角的矩形和'),
        dict(type='text', fn=_txt, size=26),
    ],
    watch=['i', 'j', ('res', 'res', 'green'), 'tmp', 'threshold'],
    skip=['m = len', 'n = len', 's = [[0]', 'f = [[0]', 's[i][j] = mat', 'continue', 'if i == 0:', 'if j == 0:'],
    captions={
        14: '第 0 行：只能累加左边，`s[{i}][{j}] = {s[i][j]}`',
        16: '第 0 列：只能累加上边，`s[{i}][{j}] = {s[i][j]}`',
        18: '一般格：加左加上、减左上（左上被算了两次），`s[{i}][{j}]` = =={s[i][j]}==',
        'res = 0': '`res = 0`：已知的最大合法边长，之后只增不减',
        'while res <': lambda S, B, ret: (f"从 `res+1 = {S['res']+1}` 开始检测：边长 {S['res']+1} 的正方形还没出界吗？" if S['res'] < min(S['m'] - S['i'], S['n'] - S['j']) else f"边长 `{S['res']+1}` 会出界 → 跳过这个格子，==res 不回退=="),
        27: 'i、j 都是 0：矩形左上就是原点，`tmp = {tmp}`',
        29: '只有左边要扣：`tmp = {tmp}`',
        31: '只有上边要扣：`tmp = {tmp}`',
        33: '四项容斥：大块 − 上 − 左 + 左上 = =={tmp}==',
        'if tmp > threshold': '`tmp = {tmp}` {"大于" if tmp > threshold else "不大于"} `{threshold}` → {"太大，当前格子放弃，换下一个" if tmp > threshold else "合法，可以扩大 res"}',
        'res += 1': '合法 → `res` 增到 =={res}==，再试更大的一圈',
        'return res': '检测完所有格子，最大边长 =={res}==',
    },
    max_steps=75,
    cards=dict(
        one_liner='前缀和算矩形，边长从已知最大值 +1 开始检测',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['给矩阵 `mat` 和阈值 `threshold`，求元素和不超过阈值的正方形最大边长',
                 '示例：3×3 矩阵，`threshold = 4`，答案 `2`'],
        quote='实际上总共检测的次数就只有 mn + res 次，其中 res 为最终的答案。',
        quote_src='—— yiduobo 题解',
        idea=['`s[i][j]` 表示以 (0,0) 为左上角、(i,j) 为右下角的矩形和，转移 `左 + 上 − 左上 + 自己`',
              '任意矩形和 = 大块 − 上块 − 左块 + 左上块',
              '不必二分：遍历格子，==从当前 res+1 开始检测==，合法就 res 加一，否则换下一格'],
        summary=['复杂度：检测次数 `mn + res`，整体 `O(mn)`',
                 '易错点：第 0 行/第 0 列没有「上」或「左」，要分四种情况取值',
                 '代码中的 `f` 数组没有用到，原文保留',
                 '原文已是 Python 3 写法，未做修改'],
    ),
)
