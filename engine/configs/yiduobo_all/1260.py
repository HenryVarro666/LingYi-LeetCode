CONFIG = dict(
    num=1260, title='二维网格迁移', difficulty='Easy', category='模拟',
    author='yiduobo', technique='展平成一维 · 截断拼接',
    tags=[],
    code='''
class Solution(object):
    def shiftGrid(self, grid, k):

        m = len(grid)
        n = len(grid[0])
        k %= (m * n)
        if k == 0:
            return grid

        tmp = [grid[i][j] for i in range(m) for j in range(n)]
        tmp = tmp[m * n - k:] + tmp[:m * n - k]
        return [tmp[i * n : (i + 1) * n] for i in range(m)]
''',
    call='Solution().shiftGrid([[1,2,3],[4,5,6],[7,8,9]], 4)',
    expect=[[6, 7, 8], [9, 1, 2], [3, 4, 5]],
    views=[
        dict(type='grid', var='grid', h=260, cell=90),
        dict(type='array', var='tmp', label='tmp（展平后的一维数组）', h=170, cell=76),
        dict(type='text', size=30, h=60, fn=lambda S: f"后 `k` = {S['k']} 个数挪到最前面" if 'tmp' in S and 'k' in S else ''),
    ],
    watch=[('k', 'k', 'yellow'), ('m', 'm', 'blue'), ('n', 'n', 'pink')],
    skip=['m = len', 'n = len'],
    captions={
        'k %= (m * n)': '迁移 `m*n` = {m*n} 次会回到原样，所以 `k %= (m*n)` → =={k}==',
        'if k == 0': lambda S, B, r: ('`k = 0`：网格不用动' if S.k == 0 else f'`k = {S.k}` ≠ 0：需要真正移动'),
        'tmp = [grid[i][j]': '按从上到下、从左到右的顺序展平：=={tmp}==',
        'tmp = tmp[m * n - k:]': '后 `k` 个数 `tmp[{m*n-k}:]` 截下来拼到前面 → =={tmp}==',
        'return [tmp': lambda S, B, r: f'每 `n` = {S.n} 个一行切回二维网格：{r}',
    },
    cards=dict(
        one_liner='按行展平后，迁移 k 次就是把后 k 个数挪到最前面',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['每次迁移：每个数右移一格，行末的数跳到下一行行首，最后一个跳回左上角',
                 '求迁移 `k` 次后的网格',
                 '示例：`[[1,2,3],[4,5,6],[7,8,9]]`，`k = 4` → `[[6,7,8],[9,1,2],[3,4,5]]`'],
        quote='如果我们按照从上到下从左到右的顺序来看这个矩阵，实际上就是每个数字都向后推移了k位',
        quote_src='—— yiduobo 题解原文',
        idea=['网格按行读出来，迁移 `k` 次 = 每个数向后推 `k` 位，末尾的绕到开头',
              '展平成一维数组 `tmp`，截下后 `k` 个，拼在前面',
              '再每 `n` 个一行切回二维'],
        after=[dict(heading='为什么这样截断', lines=['示例里 `k = 4`：最后 4 个数 `6,7,8,9` 会绕到最前面', '其余的 `1,2,3,4,5` 顺次后移 4 格，接在它们后面', '展平后的下标 `i` 的数，去了 `(i + k) % (m*n)`，截断拼接正好等价'])],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '易错：先 `k %= (m*n)`，否则切片位置会越界',
                 '代码本身 Python 3 可直接运行，无需修改'],
    ),
)
