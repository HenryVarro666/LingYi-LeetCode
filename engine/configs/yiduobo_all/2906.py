G0 = [[3, 5, 7], [11, 13, 1]]

CONFIG = dict(
    num=2906, title='构造乘积矩阵', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='拉直矩阵 · 前缀积数组 × 后缀积数组',
    tags=['动态规划', '专题：前后缀分解', '难度分 2075'],
    code='''
class Solution(object):
    def constructProductMatrix(self, grid):

        nums = []
        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            for j in range(n):
                nums.append(grid[i][j])
        
        mod = 12345
        prefix = [nums[0] % mod]
        for index in range(1, m * n):
            prefix.append(prefix[-1] * nums[index] % mod)
        
        suffix = [nums[-1] % mod]
        for index in range(m * n - 2, -1, -1):
            suffix.append(suffix[-1] * nums[index] % mod)
        suffix.reverse()

        res = []
        for index in range(m * n):
            if index % n == 0:
                res.append([])
            v = 1
            if index > 0:
                v = v * prefix[index - 1] % mod
            if index < m * n - 1:
                v = v * suffix[index + 1] % mod
            res[-1].append(v)
        
        return res
''',
    call=f'Solution().constructProductMatrix({G0!r})',
    expect=[[5005, 3003, 2145], [1365, 1155, 2670]],
    skip=['for i in range(m)', 'for j in range(n)', 'm = len', 'n = len', 'mod = 12345', 'v = 1', 'for index in range'],
    views=[
        dict(type='array', var='nums', label='nums（拉直后）', h=150, cell=90,
             color=lambda S, i, v: 'blue' if i == S.get('index') else None),
        dict(type='array', var='prefix', label='prefix[i] = nums[0..i] 的积', h=150, cell=90,
             color=lambda S, i, v: 'blue' if i == S.get('index') else None),
        dict(type='array', var='suffix', label='suffix[i] = nums[i..] 的积（reverse 后）', h=150, cell=90,
             color=lambda S, i, v: 'pink' if i == S.get('index') else None),
        dict(type='grid', var='res', label='res（逐行填回矩阵）', h=210, cell=130),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'green')],
    captions={
        'nums.append': '按先行后列拉直：`nums` = {nums}',
        'prefix = [': '`prefix[0] = nums[0] % mod` = {prefix[0]}',
        'prefix.append': '`prefix[{index}] = prefix[{index-1}] × nums[{index}] % mod` = =={prefix[-1]}==',
        'suffix = [': '`suffix` 从最后一个数开始倒着建：{suffix}',
        'suffix.append': '倒着乘进来：`nums[{index}]` 使 `suffix` 末尾变成 =={suffix[-1]}==（此时是倒序存放）',
        'suffix.reverse()': '`reverse` 后下标对齐：`suffix[i]` = `nums[i]` 到末尾的积 → {suffix}',
        'res = []': '前后缀都有了，再一趟遍历：每个位置 `前缀[i-1] × 后缀[i+1]`',
        'if index % n == 0': lambda S, B, r: (f'`index % n = {S.index % S.n}`' + ('，==新的一行开始==，先放一个空列表' if S.index % S.n == 0 else '，还在同一行')),
        'if index > 0': lambda S, B, r: ('左边有数：要乘上前缀 `prefix[index-1]`' if S.index > 0 else '`index = 0`：左边没有数，不乘前缀'),
        'v = v * prefix': '`v = 1 × prefix[{index-1}]` = =={v}==（左边所有数之积）',
        'if index < m * n - 1': lambda S, B, r: ('右边有数：要乘上后缀 `suffix[index+1]`' if S.index < S.m * S.n - 1 else '最后一个位置：右边没有数，不乘后缀'),
        'v = v * suffix': '再乘 `suffix[{index+1}]`：`v` = =={v}==（除 `nums[{index}]` 外全部之积）',
        'res[-1].append(v)': '`p` 的这个位置填 =={v}==，当前 `res` = {res}',
        'return res': '全部位置填完，返回 `res`',
    },
    cards=dict(
        one_liner='先拉直成一维，再用前缀积 × 后缀积',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['矩阵 `grid`，`p[i][j]` = 除 `grid[i][j]` 外所有元素之积，对 `12345` 取余',
                 '示例：`[[1,2],[3,4]]` → `[[24,12],[8,6]]`',
                 '本视频：`[[3,5,7],[11,13,1]]`，总积 15015 超过 12345，要取余'],
        quote='题目虽然给出的是矩阵，但是……并没有涉及到矩阵横纵坐标相关的东西，因此在这里可以先将这个矩阵拉直，将其变为一个m * n的一维数组然后求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['计算每个位置都要用到其它所有位置，和横纵坐标无关 → 拉直成一维',
              '正反各一趟：建前缀积数组 `prefix`、后缀积数组 `suffix`',
              '再一趟：`prefix[index-1] × suffix[index+1]`，按先行后列填回矩阵'],
        summary=['时间 `O(mn)`，空间 `O(mn)`（`nums`、`prefix`、`suffix` 三个数组）',
                 '易错：头尾位置只有一侧，要判断 `index > 0` 和 `index < m*n-1`',
                 '`suffix` 是倒着建的，==必须 reverse== 才能让下标对齐',
                 '对比灵神：灵神用 `pre`、`suf` 两个变量滚动，空间 `O(1)`；本做法更直观'],
    ),
)
