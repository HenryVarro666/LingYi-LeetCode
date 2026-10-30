G0 = [[3, 5, 7], [11, 13, 1]]

CONFIG = dict(
    num=2906, title='构造乘积矩阵', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解（单变量滚动）',
    tags=['动态规划', '专题：前后缀分解', '难度分 2075'],
    code='''
class Solution:
    def constructProductMatrix(self, grid: List[List[int]]) -> List[List[int]]:
        MOD = 12345
        n, m = len(grid), len(grid[0])
        p = [[0] * m for _ in range(n)]

        suf = 1  # 后缀乘积
        for i in range(n - 1, -1, -1):
            for j in range(m - 1, -1, -1):
                p[i][j] = suf  # p[i][j] 先初始化成后缀乘积
                suf = suf * grid[i][j] % MOD

        pre = 1  # 前缀乘积
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                p[i][j] = p[i][j] * pre % MOD  # 乘上前缀乘积
                pre = pre * x % MOD

        return p
''',
    call=f'Solution().constructProductMatrix({G0!r})',
    expect=[[5005, 3003, 2145], [1365, 1155, 2670]],
    skip=['for j in range', 'for j, x in', 'for i, row in', 'for i in range', 'n, m ='],
    views=[
        dict(type='text', fn=lambda S: (f"后缀 `suf` = =={S['suf']}==（位置 ({S['i']},{S['j']}) 右边所有数之积 % 12345）" if S.get('_line', 0) < 15 and 'suf' in S and 'i' in S
                                        else f"前缀 `pre` = =={S['pre']}==（位置 ({S['i']},{S['j']}) 左边所有数之积）" if 'pre' in S and 'i' in S else '先倒着算后缀，再正着乘前缀'), size=26, h=60),
        dict(type='grid', var='grid', label='grid（黄 = 当前格）', h=200, cell=80,
             cursors=[('i', 'j', 'yellow', '(i,j)')]),
        dict(type='grid', var='p', label='p[i][j] = 后缀 × 前缀', h=250, cell=110,
             cursors=[('i', 'j', 'yellow', '(i,j)')]),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('suf', 'suf', 'cyan'), ('pre', 'pre', 'orange')],
    captions={
        'MOD = 12345': '乘积要对 `12345` 取余；==中途取模==不影响结果',
        'p = [[0]': '`p` 先全填 0，稍后分两趟填',
        'suf = 1': '`suf` 是后缀乘积，空后缀乘积 = 1',
        'p[i][j] = suf': '`p[{i}][{j}] = suf` = =={suf}==：这是 `({i},{j})` ==右边所有数==之积（不含自己）',
        'suf = suf * grid': '把自己乘进去：`suf = {B.suf} × {grid[i][j]} % MOD` = {suf}，留给前一个位置用',
        'pre = 1': '`pre` 是前缀乘积，空前缀乘积 = 1',
        'p[i][j] * pre': '`p[{i}][{j}] = {B.p[i][j]} × pre({pre}) % MOD` = =={p[i][j]}==：后缀 × 前缀 = 除自己外全部之积',
        'pre = pre * x': '把 `{x}` 乘进前缀：`pre` → {pre}',
        'return p': '两趟遍历完成，返回乘积矩阵 `p`',
    },
    cards=dict(
        one_liner='除自己外的乘积 = 左边所有数之积 × 右边所有数之积',
        complexity='时间 `O(nm)`，空间 `O(1)`（返回值不计）',
        problem=['矩阵 `grid`，`p[i][j]` = 除 `grid[i][j]` 外所有元素的乘积，对 `12345` 取余',
                 '示例：`[[1,2],[3,4]]` → `[[24,12],[8,6]]`',
                 '本视频：`[[3,5,7],[11,13,1]]`，总积 15015 超过 12345，要取余'],
        quote='把矩阵平铺成一维数组，就是 238 题了。我们需要算出每个数左边所有数的乘积，以及右边所有数的乘积。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把矩阵按行展开成一条线：`p = pre × suf`',
              '先倒着遍历，把后缀乘积直接存进 `p`',
              '再正着遍历，用变量 `pre` 乘上去；==pre 和 suf 都不用数组==',
              '为什么可以中途取模：乘法对取模封闭，`(a×b) % M` 可以先对 a、b 取模'],
        summary=['时间 `O(nm)`，空间 `O(1)`',
                 '易错：`p[i][j]` 先赋值后缀，再更新 `suf`，顺序不能反（后缀不含自己）',
                 '不能用「总乘积 ÷ 自己」：取模后没有除法，且元素可能是 12345 的倍数',
                 '一维版本：238. 除自身以外数组的乘积'],
    ),
)
