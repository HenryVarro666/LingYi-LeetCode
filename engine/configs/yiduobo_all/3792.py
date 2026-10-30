CONFIG = dict(
    num=3792, title='递增乘积块之和', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='暴力遍历 + 取模',
    code='''
class Solution(object):
    def sumOfBlocks(self, n):
        
        start = 1
        mod = 10 ** 9 + 7
        res = 0
        for index in range(1, n + 1):
            v = 1
            for x in range(start, start + index):
                v = v * x % mod
            res = (res + v) % mod
            start += index
        
        return res
''',
    call='Solution().sumOfBlocks(4)',
    expect=5167,
    views=[
        dict(type='text', size=34, fn=lambda S: f"第 `{S['index']}` 块：`{S['start']}` 起连乘 {S['index']} 个数，当前 `v = {S['v']}`" if 'v' in S and 'index' in S else '第 index 块 = 接下来 index 个连续整数的乘积'),
        dict(type='text', size=30, fn=lambda S: f"前几块之和 `res = {S['res']}`" if 'res' in S else ''),
    ],
    watch=['index', 'start', 'x', 'v', ('res', 'res', 'green')],
    captions={
        'mod =': '结果对 `10^9 + 7` 取模，记作 `mod`',
        'v = 1': '开始算第 `{index}` 块，从 `start={start}` 起连乘 `{index}` 个数，`v` 初值 1',
        'v = v * x': '`v = v * {x} % mod` = =={v}==',
        'res = (res': '第 {index} 块乘积 =={v}==，加到 `res` 并取模 → =={res}==',
        'start += index': '下一块的起点后移 `index` 位：`start` → {start}',
        'return res': '前 n 块之和已经取过模，直接返回 =={ret}==',
    },
    cards=dict(
        one_liner='n 不大，直接一趟遍历每块乘积并累加',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['数列：第 1 项 `1`，第 2 项 `2*3`，第 3 项 `4*5*6`，……第 index 块是之后 index 个连续整数的乘积',
                 '求前 n 项之和，对 `10^9 + 7` 取模（n 不超过 1000）',
                 '演示用：`n=4` → `1 + 6 + 120 + 5040 = 5167`'],
        quote='计算数列中第index项的时间复杂度是O(index)的。由于n的规模不大，因此在这里万千可以直接一趟遍历，计算出数列中的前n项对10^9 + 7取模的结果，然后将这些结果累加起来再取模',
        quote_src='—— yiduobo 题解',
        idea=['`start` 是当前块的第一个数，块内数字为 `start ... start+index-1`',
              '每块用内层循环连乘，每乘一次取模',
              '块结束后累加到 `res` 并取模，`start` 前移'],
        summary=['时间 `O(n^2)`，n 最大 1000 完全够用',
                 '每步取模防止数字过大',
                 '易错点：`start += index`，别写成 `+= 1`'],
    ),
)
