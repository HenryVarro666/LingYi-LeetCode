CONFIG = dict(
    num=1837, title='K进制表示下的各位数字总和', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='取余法 · 进制转换',
    code='''
class Solution(object):
    def sumBase(self, n, k):

        res = 0
        while n:
            res += n % k
            n //= k
        
        return res
''',
    call='Solution().sumBase(34, 6)',
    expect=9,
    views=[
        dict(type='text', size=40, h=80,
             fn=lambda S: f"n = ==({S['n']})== ，已累加的数位和 = ==({S['res']})==" if 'res' in S else ''),
        dict(type='text', size=34, h=80,
             fn=lambda S: f"这一位：`{S['n']} % {S['k']}` = =={S['n'] % S['k']}==" if S.get('n') else ''),
    ],
    watch=['n', 'k', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计各位数字之和',
        'while n': lambda S, B, r: (f'`n = {S.n}` 不为 0，还有数位没取' if S.n else '`n = 0`：所有数位都取完了，退出循环'),
        'res += n % k': '`n % k = {B.n} % {k}` 就是 {k} 进制的最低位 `{B.n % k}`，累加：`res = {res}`',
        'n //= k': '去掉最低位：`n` 从 {B.n} 变成 `{n}`',
        'return res': '各位数字之和 = `{res}`',
    },
    cards=dict(
        one_liner='取余得最低位，整除去掉最低位，位位累加',
        complexity='时间 `O(log_k n)`，空间 `O(1)`',
        problem=['给整数 `n`（10 进制）和进制 `k`', '把 `n` 转成 `k` 进制，求各位数字之和（结果用 10 进制）',
                 '示例：`n=34, k=6` → 34 = `54`（6 进制）→ `9`'],
        quote='比较基础的题目，直接用取余法计算n的k进制表示，将这些余数累加起来即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n % k` 是 k 进制的最低位', '`n // k` 去掉最低位，重复直到 `n` 为 0',
              '不必真的拼出 k 进制串，边取边加'],
        summary=['时间 `O(log_k n)`，空间 `O(1)`',
                 '易错：必须用整除 `//`，用 `/` 会变成浮点数',
                 '原文为 Python 2 写法，`n /= k` 已改为 `n //= k`',
                 '同类：十进制数位和、二进制 1 的个数'],
    ),
)
