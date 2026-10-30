
CONFIG = dict(
    num=1716, title='计算力扣银行的钱', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='整周等差数列 + 零头',
    tags=['灵神题单', '难度分 1295'],
    code='''
class Solution(object):
    def totalMoney(self, n):

        k = n % 7
        n //= 7

        res = (28 + 28 + 7 * (n - 1)) * n // 2
        res += (n + 1 + n + k) * k // 2
        return res
''',
    call='Solution().totalMoney(20)',
    expect=96,
    views=[
        dict(type='text', h=170, size=30, fn=lambda S: (
            '第 20 天：2 个整周 + 6 天零头' if S.get('_line', 0) < 5 else
            f'整周：`m = {S["n"]}`，首项 `w1 = 28`，公差 `7`' + (
                f'　整周总额 = (28 + 28 + 7×({S["n"]}−1)) × {S["n"]} / 2 = =={(56 + 7 * (S["n"] - 1)) * S["n"] // 2}==' if 'res' in S else '') +
            (f'　零头 {S["k"]} 天：起步价 `m+1 = {S["n"]+1}`，末日 `m+k = {S["n"]+S["k"]}`' if 'res' in S else ''))),
        dict(type='array', var=lambda S: [28] + [28 + 7 * i for i in range(1, max(S.get('n', 1), 1))] if S.get('_line', 0) >= 5 and S.get('n', 0) > 0 else [28], h=200, cell=90,
             label='每个完整星期的存款额'),
    ],
    watch=[('n', 'n'), ('k', 'k', 'pink'), ('res', 'res', 'green')],
    captions={
        'k = n % 7': '多出来的零头天数 `k = n % 7 = {k}`',
        'n //= 7': '完整的星期数 `m = n // 7 = {n}`（变量 n 被复用）',
        'res = (28': '首周 28，之后每周多 7：等差数列 `(28 + 28 + 7×({n}-1)) × {n} / 2` = =={res}==',
        'res +=': '零头 {k} 天：已过 {n} 个整周，起步价 `{n}+1`，末日 `{n}+{k}`，累计 `res = {res}`',
        'return res': '总额 `{res}`',
    },
    cards=dict(
        one_liner='先算完整星期的等差数列，再补零头几天',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['周一存 1 元，之后每天比前一天多 1 元',
                 '每个新周一比 ==前一个周一== 多存 1 元',
                 '求第 `n` 天结束时的总额，示例 `n = 20` → `96`'],
        quote='对于完整的星期而言，两个相邻的星期之间可以视为每天有1块钱的差，那么一星期下来就是7块钱。',
        quote_src='—— yiduobo 题解原文',
        idea=['`m = n // 7` 个整周，`k = n % 7` 天零头',
              '首周 `w1 = 28`，之后依次 `28+7, 28+14…`：长度为 m 的等差数列',
              '零头所在的星期起步价是 `m+1`，末日是 `m+k`'],
        after=[dict(heading='验算 n = 20', lines=['`m = 2`，`k = 6`','整周：`28 + 35 = 63`','零头：`3+4+5+6+7+8 = 33`','合计 `63 + 33 = 96`，和公式一致'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：零头的首项是 `m+1`，不是 1',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（`n /= 7` 改成 `n //= 7`）'],
    ),
)
