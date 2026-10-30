def _c(S, i, j, v):
    return 'green' if v else None


CONFIG = dict(
    num=3153, title='所有数对中数位差之和', difficulty='Medium', category='位运算',
    author='yiduobo', technique='按位统计 k·(n−k)',
    tags=['灵神题单·位运算', '难度分 1645'],
    code='''
class Solution(object):
    def sumDigitDifferences(self, nums):

        res = 0
        freq = [[0] * 10 for _ in range(9)]
        for v in nums:
            p = 0
            while v:
                freq[p][v % 10] += 1
                p += 1
                v //= 10

        for index in range(9):
            for d in range(10):
                res += freq[index][d] * (len(nums) - freq[index][d])

        return res // 2
''',
    call='Solution().sumDigitDifferences([13, 23, 12])',
    expect=4,
    views=[
        dict(type='array', var='nums', h=160, label='nums（每个数逐位拆进 freq）'),
        dict(type='table', var='freq', h=420, cell=50, label='freq[p][x]：第 p 位上数字 x 出现的次数（黄 = 正在累加的格子）',
             rows=lambda S: [f'p={k}' for k in range(len(S['freq']))], cols=list(range(10)),
             color=lambda S, i, j, v: ('yellow' if 'index' in S and 'd' in S and i == S['index'] and j == S['d'] else None) or ('green' if v else None)),
        dict(type='text', size=28, fn=lambda S: (f"第 `{S['index']}` 位：数字 `{S['d']}` 出现 `{S['freq'][S['index']][S['d']]}` 次 → 与另外 `{len(S['nums']) - S['freq'][S['index']][S['d']]}` 个都不同" ) if 'index' in S and 'd' in S and S['freq'][S['index']][S['d']] else ''),
    ],
    watch=[('v', 'v', 'blue'), ('p', 'p', 'cyan'), ('index', 'index', 'pink'), ('d', 'd', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计「有序」数位差对数，最后要除以 2',
        'freq = ': '`freq[p][x]`：==第 p 位==上数字 `x` 一共出现了几次，共准备 9 位（`nums[i] < 10^9`）',
        'for v in nums': '取出 `v = {v}`，逐位拆开统计',
        'p = 0': '`p = 0`：从个位开始',
        'while v': lambda S, B, r: (f'`v = {S.v}` 还有数位 → 继续拆' if S.v else '`v = 0`：这个数拆完了'),
        'freq[p][v % 10] += 1': '第 `{p}` 位上数字 `{v % 10}` 的出现次数加 1 → `{freq[p][v % 10]}`',
        'p += 1': '换到更高一位：`p` → {p}',
        'v //= 10': '去掉个位：`v` → {v}',
        'for index in range': '统计完成，开始逐位算：第 `{index}` 位',
        'for d in range': '枚举数字 `d = {d}`',
        'res +=': lambda S, B, r: (f'第 `{S.index}` 位数字 `{S.d}` 出现 `k = {S.freq[S.index][S.d]}` 次：它与另外 `n − k = {len(S.nums) - S.freq[S.index][S.d]}` 个都不同 → `k·(n−k)` = {S.freq[S.index][S.d] * (len(S.nums) - S.freq[S.index][S.d])}，`res` → {S.res}' if S.freq[S.index][S.d] else f'数字 `{S.d}` 没出现（k = 0），贡献 0'),
        'return': '每一对被 `(a,b)` 与 `(b,a)` 数了两次 → `res // 2` = =={res // 2}==',
    },
    skip=['for d in range'],
    max_steps=64,
    cards=dict(
        one_liner='每一位单独算：数字 d 出现 k 次，就能配出 k·(n−k) 个不同',
        complexity='时间 `O(n · 位数)`，空间 `O(位数 · 10)`',
        problem=['数组里每个数位数相同；两数的数位不同 = 相同位置上数字不同的个数',
                 '求所有数对的数位不同之和',
                 '本视频：`[13,23,12]` → `4`'],
        quote='对于其中某一位，若这一位上数字d一共出现了k次，那么其他的n - k个数字都可以与d形成一组不同的数位，一共就可以形成k * (n - k)组不同的数位。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把每个数逐位拆开，用 `freq[p][x]` 记下每一位上各数字的出现次数',
              '再逐位、逐数字累加 `k * (n - k)`',
              '每个数对在 d 一侧、另一侧各算一次 → 最后除以 2'],
        summary=['时间 `O(n · 位数)`，空间 `O(位数 · 10)`',
                 '==别忘了除以 2==：`k·(n−k)` 把每个无序数对算了两遍',
                 '`range(9)` 因 `nums[i] < 10^9` 最多 9 位；不足的位 `freq` 全 0，贡献为 0',
                 '对比灵神：灵神边遍历边查「前面有几个不同」，不用最后除 2'],
    ),
)
