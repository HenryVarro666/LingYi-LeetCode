CONFIG = dict(
    num=3370, title='仅含置位位的最小整数', difficulty='Easy', category='位运算',
    author='yiduobo', technique='从 1 开始 res×2+1 枚举',
    tags=['灵神题单', '位运算', '难度分 1199'],
    code='''
class Solution(object):
    def smallestNumber(self, n):

        res = 1
        while res < n:
            res = res * 2 + 1
        return res
''',
    call='Solution().smallestNumber(10)',
    expect=15,
    views=[
        dict(type='text', size=34, fn=lambda S: f"目标 `n = {S['n']}` = ==`{bin(S['n'])[2:]}`==" if 'n' in S else ''),
        dict(type='text', size=34, fn=lambda S: (f"当前候选 `res = {S['res']}` = ==`{bin(S['res'])[2:]}`==（{len(bin(S['res'])) - 2} 个 1）" if 'res' in S else '')),
        dict(type='text', size=34, fn=lambda S: (('`res < n`：还不够大，再加一位 1' if S['res'] < S['n'] else '`res >= n`：够了，停') if 'res' in S else '')),
    ],
    watch=[('n', 'n', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 1': '最小的全 1 数是 `1`（二进制 `1`）：从它开始往上找',
        'while res < n': lambda S, B, r: (f'`res = {S.res} < n = {S.n}`：还没到 n，继续' if S.res < S.n
                                          else f'`res = {S.res} >= n = {S.n}`：第一个不小于 n 的全 1 数，退出'),
        'res = res * 2 + 1': '左移一位再补 1：`{B.res}` → `{res}`，二进制 ==多了一个 1==',
        'return res': '全 1 数增长是指数级，只用几轮就停：答案 `{res}`',
    },
    cards=dict(
        one_liner='全 1 数下一个就是 res×2+1，暴力往上数几轮就到',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['给整数 `n`，求 ==大于等于 n== 且二进制全是 1 的最小整数',
                 '示例：`n = 5` → `7`；`n = 10` → `15`',
                 '本视频：`n = 10` → `15`'],
        quote='满足条件的元素增长速度是指数级的，因此在这里就可以从res = 1开始暴力向上枚举答案，每一轮都将res更新为res * 2 + 1，直到res大于等于n为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['全 1 数依次是 `1, 3, 7, 15, ...`',
              '`k` 个 1 变成 `k+1` 个 1：左移一位再加 1，即 `res * 2 + 1`',
              '数量只有 `log n` 个，直接从 1 枚举到 `res >= n` 就行'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '循环条件是 `res < n`：`n` 本身是全 1 时（如 3）不会多走一步',
                 '原文为 Python 2 风格，但本题无需改动，代码照搬',
                 '对比灵神：灵神用 `bit_length` 一步算出，这里是逐位生长'],
    ),
)
