def _cap_cell(S, B, ret):
    i, j = S.i, S.j
    return (f'`f[{i}][{j}] = f[{i}][{j-1}] + f[{i-1}][{j}]` = `{S.f[i][j-1]} + {S.f[i-1][j]}`'
            f'：前 j 个数之和 = 左边那格（到 j−1 的和）+ 上一秒的自己 = =={S.f[i][j]}==')


CONFIG = dict(
    num=3179, title='K 秒后第 N 个元素的值', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='前缀和递推 · f[i][j] = f[i][j−1] + f[i−1][j]',
    tags=['灵神题单', '组合数学'],
    code='''
class Solution(object):
    def valueAfterKSeconds(self, n, k):

        mod = 10 ** 9 + 7
        f = [[0] * n for _ in range(k + 1)]
        for i in range(n):
            f[0][i] = 1
        for i in range(1, k + 1):
            f[i][0] = 1
            for j in range(1, n):
                f[i][j] = f[i][j - 1] + f[i - 1][j]
                if f[i][j] >= mod:
                    f[i][j] -= mod
        
        return f[-1][-1]
''',
    call='Solution().valueAfterKSeconds(4, 3)',
    expect=20,
    views=[
        dict(type='grid', var='f', cursors=[('i', 'j', 'yellow', '(i,j)')], rows=lambda S: [f'{t} 秒' for t in range(len(S['f']))],
             cols=lambda S: [f'a[{c}]' for c in range(len(S['f'][0]))],
             color=lambda S, i, j, v: ('green' if v else None), h=360, cell=110),
        dict(type='text', fn=lambda S: '行 = 第几秒，列 = 数组下标；绿格是已经算出的值', h=70),
    ],
    watch=['i', 'j'],
    captions={
        'mod = 10': '结果对 `10^9 + 7` 取模',
        'f = [[0]': '`f[i][j]` = 第 `i` 秒时数组第 `j` 个元素，共 `k+1` 行（含第 0 秒）',
        'f[0][i] = 1': '第 0 秒：所有元素都是 1',
        'f[i][0] = 1': '第 `{i}` 秒：`a[0]` 前面没有数，永远是 1',
        'f[i][j] = f[i][j - 1]': _cap_cell,
        'if f[i][j] >= mod': lambda S, B, r: ('超过 mod，下一行减掉 mod' if S.f[S.i][S.j] >= 1000000007 else f'`{S.f[S.i][S.j]}` < mod，不用取模'),
        'f[i][j] -= mod': '用减法代替取模，保持在 mod 之内',
        'return f[-1][-1]': lambda S, B, r: f'最后一行最后一列 `f[{S.k}][{S.n-1}]` = =={r}==，即 {S.k} 秒后 `a[n-1]`',
    },
    cards=dict(
        one_liner='f[i][j] = f[i][j−1] + f[i−1][j]：前缀和拆成两项',
        complexity='时间 `O(nk)`，空间 `O(nk)`',
        problem=['长度为 `n` 的数组，初始全是 1；每秒同时把每个元素变成「前面所有元素 + 自己」',
                 '求 `k` 秒后 `a[n-1]`，对 `10^9 + 7` 取模',
                 '示例：`n = 4, k = 5` → `56`；本视频：`n = 4, k = 3` → `20`'],
        quote='f[i][j] = f[i - 1][0] + f[i - 1][1] + ... + f[i - 1][j]，另一方面f[i][j - 1] = f[i - 1][0] + ... + f[i - 1][j - 1]，那么就有f[i][j] = f[i][j - 1] + f[i - 1][j]',
        quote_src='—— yiduobo 题解原文',
        idea=['第 i 秒的 `a[j]` 是上一秒前 `j+1` 个数之和',
              '`a[j−1]` 恰好是上一秒前 `j` 个数之和，所以只差上一秒的 `a[j]`',
              '于是每格只由左边和上边两格推出，一趟双重循环就够了'],
        summary=['时间 `O(nk)`，空间 `O(nk)`',
                 '值始终保持 `< mod`，用 `if >= mod: -= mod` 代替 `%`',
                 '第 0 行全 1，第 0 列也全 1，递推从 `j = 1` 开始',
                 '原文最后提到：值就是组合数 `C(n+k−1, k)`，可以用乘法逆元 `O(n)` 直接算'],
    ),
)
