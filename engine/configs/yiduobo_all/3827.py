CONFIG = dict(
    num=3827, title='统计单比特整数', difficulty='Easy', category='位运算',
    author='yiduobo', technique='v = 2v + 1 迭代计数',
    tags=['灵神题单', '位运算'],
    code='''
class Solution(object):
    def countMonobit(self, n):

        res = 1
        v = 1
        while v <= n:
            res += 1
            v = v + v + 1

        return res
''',
    call='Solution().countMonobit(10)',
    expect=4,
    views=[
        dict(type='text', size=32, fn=lambda S: f"上限 `n = {S['n']}`，已数到 `res = {S['res']}` 个（含全 0 的 `0`）" if 'res' in S else ''),
        dict(type='text', size=32, fn=lambda S: (f"当前全 1 数 `v = {S['v']}` = ==`{bin(S['v'])[2:]}`==" if 'v' in S else '')),
        dict(type='text', size=32, fn=lambda S: (('`v <= n`：它在范围内，计数 +1' if S['v'] <= S['n'] else '`v > n`：超出范围，停止') if 'v' in S else '')),
    ],
    watch=[('n', 'n', 'blue'), ('v', 'v', 'orange'), ('res', 'res', 'green')],
    captions={
        'res = 1': '全 0 的情况只有 `0` 一个数，先计 `res = 1`',
        'v = 1': '全 1 的数从 `1` 开始：`v = 1`',
        'while v <= n': lambda S, B, r: (f'`v = {S.v} <= n = {S.n}`：这个全 1 数在 `[0, n]` 里' if S.v <= S.n
                                         else f'`v = {S.v} > n = {S.n}`：之后的全 1 数更大，停止'),
        'res += 1': '又找到一个合法的全 1 数，`res` → {res}',
        'v = v + v + 1': '`2^k − 1` 乘 2 再加 1 → `2^(k+1) − 1`：`{B.v}` → `{v}`',
        'return res': '迭代轮数 + 全 0 的 1 个 = `{res}`',
    },
    cards=dict(
        one_liner='全 0 只有 0；全 1 从 1 开始不断 ×2+1，数几个',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['二进制所有位都相同的数叫 ==单比特数==，问 `0 ~ n` 之间有多少个',
                 '示例：`n = 4` → `3`（`0`、`1`、`3`）',
                 '本视频：`n = 10` → `4`（`0`、`1`、`3`、`7`）'],
        quote='对于v = 2^k - 1，只需将其乘以2再加上1，就可以变为2^(k + 1) - 1。于是可以从1开始向上迭代，每次将当前元素乘以2再加上1，直到大于n为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['全 0 只有 `0` 一个；全 1 是 `1, 11, 111, ...` 即 `2^k − 1`',
              '从 `v = 1` 开始，每轮 `v = 2v + 1` 得到下一个全 1 数',
              '迭代的轮次就是范围内全 1 数的个数，再加上 `0` 这一个'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '`res` 初值是 1，已经算上了 `0`',
                 '循环条件是 `v <= n`（可以相等）：`n = 7` 时 `7` 也要算',
                 '原文为 Python 2 风格，但本题无需改动，代码照搬',
                 '对比灵神：灵神直接用 `(n+1).bit_length()` 一步算出'],
    ),
)
