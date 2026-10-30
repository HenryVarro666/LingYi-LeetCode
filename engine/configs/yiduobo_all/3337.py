def _info(S):
    t = S.get('t')
    if t is None or 'base' not in S or S.get('_line', 0) < 29:
        return '`f[idx][c]` = 执行 idx 次后第 c 种字符的个数（行向量）；`B[i][j] = 1` 表示字符 i 下一步会变出字符 j'
    return f'剩余次数 `t = {t}`（二进制 `{bin(t)[2:] if t else "0"}`）；`res` = 当前字符计数行向量'


CONFIG = dict(
    num=3337, title='字符串转换后的长度 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='字符计数向量 × 转移矩阵快速幂',
    tags=['难度分 2412'],
    code='''
class Solution(object):
    def lengthAfterTransformations(self, s, t, nums):
        
        def generate(nums):
            n = len(nums)
            base = [[0] * n for _ in range(n)]
            for i, x in enumerate(nums):
                for j in range(i + 1, i + x + 1):
                    base[i][j % n] = 1
            
            return base
            
        base = generate(nums)

        res = [[0] * 26]
        for char in s:
            res[0][ord(char) - 97] += 1
        
        mod = 10 ** 9 + 7

        def mul(a, b):
            m = len(a)
            n = len(a[0])
            o = len(b[0])

            c = [[0] * o for _ in range(m)]
            for i in range(m):
                for j in range(n):
                    for k in range(o):
                        c[i][k] = (c[i][k] + a[i][j] * b[j][k]) % mod
            
            return c

        while t:
            if t & 1:
                res = mul(res, base)
            
            base = mul(base, base)
            t >>= 1

        return sum(res[0]) % mod
''',
    call='Solution().lengthAfterTransformations("abcyy", 5, [1]*25 + [2])',
    expect=7,
    skip=['for i, x in enumerate', 'for j in range(i + 1', 'base[i][j % n] = 1', 'm = len(a)', 'n = len(a[0])', 'o = len(b[0])',
          'c = [[0] * o', 'for i in range(m)', 'for j in range(n)', 'for k in range(o)', 'c[i][k] =', 'return c', 'return base', 'n = len(nums)', 'base = [[0] * n'],
    max_steps=60,
    max_events=900000,
    views=[
        dict(type='text', fn=_info, size=22, h=90),
        dict(type='table', var=lambda S: S.get('base') or [[0] * 26 for _ in range(26)],
             label='base（26×26：蓝格 = 1，行 i 列 j 表示 i → j）', h=520, cell=19, values=False,
             color=lambda S, i, j, v: 'blue' if v else None),
        dict(type='array', var=lambda S: S['res'][0] if S.get('res') else [0] * 26,
             label='res[0]（a 到 z 各字符的个数）', h=130, cell=34),
    ],
    watch=[('t', 't', 'blue'), ('sum(res[0])', 'sum(res[0])', 'green')],
    captions={
        'base = generate': '`base` 就是转移矩阵 `B`：`B[i][j % 26] = 1` 表示字符 i 变成 i+1 … i+nums[i]（`z` 后回绕）',
        'res = [[0] * 26]': '`res` 是 1×26 的行向量，放初始 `s` 里各字符的个数',
        'for char in s': '逐个读 `s` 的字符，统计各字母出现次数（读完为止）',
        'res[0][ord': '`{char}` 的计数 +1 → `res[0][{ord(char) - 97}] = {res[0][ord(char) - 97]}`',
        'mod = ': '所有乘法都要对 `10^9 + 7` 取模',
        'while t': lambda S, B, r: (f'`t = {S.t}` 还没用完 → 看最低位' if S.t else '次数用完了，`res` 就是 `f[0] × B^t`，对所有位求和即答案'),
        'if t & 1': lambda S, B, r: ('`t & 1 = 1`：最低位是 1 → ==把当前 base（B 的 2^k 次幂）乘到 res 右边==' if S.t & 1
                                     else '`t & 1 = 0`：最低位是 0 → 这一块不用'),
        'res = mul(res, base)': '`res = res × base`：向量再走 `2^k` 次变换（行向量在左边）',
        'base = mul(base, base)': '`base` 自乘：一次走 `2^k` 步 → 一次走 `2^(k+1)` 步',
        't >>= 1': '`t` 右移一位 → {t}',
        'return sum': '`sum(res[0])` 就是最终字符串长度 = =={ret}==',
    },
    cards=dict(
        one_liner='把「各字符的个数」当向量，每次变换是同一个矩阵',
        complexity='时间 `O(n + 26^3 log t)`，空间 `O(26^2)`',
        problem=['`s` 的每个字符每次变成后面 `nums[c]` 个字母（`z` 后回绕），做 `t` 次',
                 '求最终字符串长度，对 `10^9+7` 取模，`t` 最大 `10^9`',
                 '本视频：`s = "abcyy", t = 5`，`nums` 只有 `z` 为 2，其余为 1 → `7`'],
        quote='令f[index][c]表示执行index次操作后，字符串中第c种字符的数量。……f[t] \\= f[0] \\* B \\* B \\* ... \\* B，这里一共是t个B。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[index]` 是 1×26 行向量：第 c 种字符的个数',
              '字符 i 变成 i+1 … i+nums[i]，所以 `B[i][i+1..i+nums[i]] = 1`，乘一次 B 就是变换一次',
              '`f[t] = f[0] × B^t`，矩阵乘法有结合律 → 对 B 做快速幂'],
        summary=['时间 `O(n + 26^3 log t)`，空间 `O(26^2)`',
                 '易错：行向量乘矩阵，`res` 在左、`base` 在右，写反会变成转置',
                 '下标 `j % n` 处理 `z` 之后回绕；每次 `mul` 都要取模',
                 '原文本身是 Python 3 兼容的写法，代码没有改动',
                 '对比灵神：灵神算每个字母的长度再按个数加权，yiduobo 直接推字符个数向量']
    ),
)
