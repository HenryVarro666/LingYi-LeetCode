CONFIG = dict(
    num=268, title='缺失数字', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='等差求和 · 减去数组和',
    code='''
class Solution(object):
    def missingNumber(self, nums):

        return (1 + len(nums)) * len(nums) // 2 - sum(nums)
''',
    call='Solution().missingNumber([3, 0, 1, 5, 2])',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（n = 5，数应该是 0 到 5 共 6 个，少了一个）', h=200,
             color=lambda S, i, v: 'blue'),
        dict(type='text', size=34, h=80,
             fn=lambda S: (f"0 到 {len(S['nums'])} 的和 = `({len(S['nums'])}+1)×{len(S['nums'])}÷2` = =={(1 + len(S['nums'])) * len(S['nums']) // 2}==；"
                           f"`sum(nums)` = =={sum(S['nums'])}==") if 'nums' in S else ''),
        dict(type='text', size=38, h=90,
             fn=lambda S: (f"缺失的数 = `{(1 + len(S['nums'])) * len(S['nums']) // 2} − {sum(S['nums'])}` = =={(1 + len(S['nums'])) * len(S['nums']) // 2 - sum(S['nums'])}==") if 'nums' in S else ''),
    ],
    watch=[('n', 'len(nums)', 'blue'), ('应有的和', '(1 + len(nums)) * len(nums) // 2', 'cyan'), ('实际的和', 'sum(nums)', 'pink')],
    captions={
        'return': '`0 + 1 + … + n = n(n+1)//2` = `{(1 + len(nums)) * len(nums) // 2}`，减去 `sum(nums) = {sum(nums)}`，差值 `{ret}` 就是缺的那个数',
    },
    cards=dict(
        one_liner='0 到 n 的和已知，减去数组的和，剩下的就是缺失的数',
        complexity='时间 `O(n)`（求和），空间 `O(1)`',
        problem=['`nums` 含 `n` 个互不相同的数，取自 `[0, n]`',
                 '找出 `[0, n]` 中没出现的那个数',
                 '示例：`[3,0,1]` → `2`；本视频 `[3,0,1,5,2]` → `4`'],
        quote='比较简单的数学题。首先我们知道0加到n的和为n * (n + 1) / 2，那么在这里我们只需要计算出nums的和，然后使用n * (n + 1) / 2减去这个和，就能得到缺失的那个数了。',
        quote_src='—— yiduobo 题解原文',
        idea=['完整的 `0..n` 加起来是等差数列求和：`n(n+1)/2`',
              '数组里少了一个数，它的和就比完整的和少了==这个数本身==',
              '两个和一减，缺的数直接出来，不需要排序或哈希'],
        after=[dict(heading='手算验证', lines=['完整的 `0+1+2+3+4+5` = `15`', '数组 `3+0+1+5+2` = `11`', '`15 − 11` = ==4==，正是数组里没有的那个数',
                                              '只要缺的是一个数，这个差就唯一确定它'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：数组长度是 `n`，但完整范围有 `n+1` 个数，公式是 `n(n+1)/2`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '其他解法：异或、排序、哈希表'],
    ),
)
