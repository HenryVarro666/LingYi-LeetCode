CONFIG = dict(
    num=2549, title='统计桌面上的不同数字', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='分情况：n<=2 与 n>=3',
    tags=['贪心与思维', '脑筋急转弯', '难度分 1266'],
    code='''
class Solution(object):
    def distinctIntegers(self, n):

        if n == 1 or n == 2:
            return 1
        
        return n - 1
''',
    call='Solution().distinctIntegers(6)',
    expect=5,
    views=[
        dict(type='array', var=lambda S: list(range(1, S['n'] + 1)) if 'n' in S else [], label='最终桌面上的数字（绿 = 在桌面上，灰 = 不会出现）', h=240,
             color=lambda S, i, v: 'green' if v >= 2 else None, dim=lambda S, i, v: v < 2),
        dict(type='text', fn=lambda S: f"`n = {S['n']}`：桌面最终是 `2 ~ {S['n']}`，一共 `{S['n']} - 1` = =={S['n'] - 1}== 个" if 'n' in S and S['n'] >= 3 else ('' if 'n' not in S else '`n <= 2`：桌面不会变，只有 n 自己'), size=30),
    ],
    watch=[('n', 'n', 'blue')],
    captions={
        'n == 1 or n == 2': '`n = {n}`：是 1 或 2 吗？→ {"是，桌面不变" if n <= 2 else "不是，说明 n >= 3，走通用公式"}',
        'return n - 1': '`n >= 3` 时桌上是 2 到 n，共 `n - 1 = {n - 1}` 个，返回 =={ret}==',
        'return 1': '桌面上的数字不会发生改变，只有 1 个',
    },
    cards=dict(
        one_liner='n >= 3 时桌上是 2 到 n；n <= 2 时桌面不变',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['桌上放着正整数 `n`，每天把满足 `x % i == 1` 的 `i` 也放上桌，持续 `10^9` 天',
                 '问最后桌面上有几个不同整数',
                 '本视频：`n = 6` → `5`'],
        quote='对于任意大于等于3的整数n，都有n % (n - 1) = 1，也就是说桌面上最后的数字必然是2到n，一共是n - 1个数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n >= 3`：`n % (n-1) = 1`，递推下去，2 到 n 全部出现，共 `n-1` 个',
              '`n = 1`：没有 `i` 满足 `1 % i == 1`，桌面不变，答案 1',
              '`n = 2`：`2 % 1 = 0`、`2 % 2 = 0`，也不变，答案 1'],
        after=[dict(heading='为什么要分开写', lines=['`n = 2` 时公式 `n - 1` 也得 1，但 yiduobo 把 1、2 一起当「不变」处理', '这样每个分支的理由都一目了然', '`n >= 3` 才真正有新数字上桌'])],
        summary=['时间、空间都是 `O(1)`',
                 '易错点：`n = 1, 2` 不能用 `n - 1` 去想成「新增了数」',
                 '原文为 Python 2 风格，代码无需改动',
                 '对比灵神：灵神用 `n - 1 if n > 1 else 1` 一句话，yiduobo 显式分 `n <= 2` 与 `n >= 3`'],
    ),
)
