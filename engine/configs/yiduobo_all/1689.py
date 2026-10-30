CONFIG = dict(
    num=1689, title='十-二进制数的最少数目', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='逐位取最大数位',
    tags=['贪心与思维', '脑筋急转弯', '难度分 1355'],
    code='''
class Solution(object):
    def minPartitions(self, n):

        res = 0
        for char in n:
            res = max(res, int(char))
        
        return res
''',
    call="Solution().minPartitions('27346')",
    expect=7,
    views=[
        dict(type='string', var='n', label='n 的每一位（绿 = 当前最大值所在位）', h=240,
             color=lambda S, i, v: 'green' if 'res' in S and int(v) == S['res'] and S['res'] > 0 and i == S['n'].index(v) else None),
        dict(type='text', fn=lambda S: f"当前最大数位 `res = {S['res']}`：至少要 =={S['res']}== 个数" if 'res' in S else '', size=30),
    ],
    watch=[('char', 'char', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录目前见到的最大数位，从 0 开始',
        'res = max': '数位 `{char}`：`res = max({B.res}, {char})` = =={res}=={"（更新了）" if res != B.res else "（没变）"}',
        'return res': '最大的数位就是答案：返回 =={res}==',
    },
    skip=['for char in n'],
    cards=dict(
        one_liner='每一位要几个 1 就要几个数，取最大的一位',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把整数 `n`（字符串）拆成若干只含 0 和 1 的十进制数之和',
                 '求最少需要几个数',
                 '本视频：`"27346"` → `7`'],
        quote='对于n的某一位，不妨设其为k，就需要分解出来的数中有k个该位为1。由于位与位之间是相互独立的，那么就只需找出n中最大的位k，这个k就是最终答案了。',
        quote_src='—— yiduobo 题解原文',
        idea=['某一位是 `k`，每个数这一位最多是 1 → 需要 `k` 个数在该位为 1',
              '位与位互相独立，互不影响',
              '所以答案是所有位里最大的 `k`，一趟遍历取 max'],
        after=[dict(heading='为什么够用', lines=['最大位 `k` 个数里，每一位 `d` 让其中 `d` 个数取 1，其余取 0', '位与位独立，所以这样一定能拼出 `n`', '于是下界 `k` 也能达到'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：`n` 是字符串，要 `int(char)` 再比较',
                 '原文为 Python 2 风格，代码无需改动',
                 '对比灵神：灵神一行 `int(max(n))`，yiduobo 手写循环逐位取最大'],
    ),
)
