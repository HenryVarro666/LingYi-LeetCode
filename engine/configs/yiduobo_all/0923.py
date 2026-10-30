CONFIG = dict(
    num=923, title='三数之和的多种可能', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='计数 DP（选 j 个数凑和 k）',
    tags=[],
    code='''
class Solution(object):
    def threeSumMulti(self, arr, target):

        f = [[0] * (target + 1) for _ in range(4)]
        f[0][0] = 1
        mod = 10 ** 9 + 7

        for num in arr:
            for j in range(target, num - 1, -1):
                f[3][j] = (f[3][j] + f[2][j - num]) % mod
                f[2][j] = (f[2][j] + f[1][j - num]) % mod
                f[1][j] = (f[1][j] + f[0][j - num]) % mod

        return f[3][target]
''',
    call='Solution().threeSumMulti([1,2,2,3], 6)',
    expect=2,
    skip=['for j in range'],
    max_steps=45,
    views=[
        dict(type='array', var='arr', label='arr', h=150, cell=80,),
        dict(type='text', size=26, h=60, fn=lambda S: (f"选 `{S['num']}`：f[3][{S['j']}] += f[2][{S['j']-S['num']}]，f[2][{S['j']}] += f[1][{S['j']-S['num']}]，f[1][{S['j']}] += f[0][{S['j']-S['num']}]" if 'j' in S and 'num' in S else '`f[c][s]` = 选 c 个数、和为 s 的方案数')),
        dict(type='table', var='f', label='f[选几个数][和]（黄 = 正在更新的列）', h=300, cell=70,
             rows=['选0个', '选1个', '选2个', '选3个'], cols=lambda S: list(range(S['target'] + 1)),
             cursors=[(lambda S: 3, 'j', 'yellow', '')]),
    ],
    watch=[('num', 'num', 'blue'), ('j', 'j', 'pink'), ('f[3][target]', 'f[3][target]', 'green')],
    captions={
        'f = [[0]': '`f[c][s]`：选 `c` 个数、和为 `s` 的方案数，`c` 只有 0 到 3',
        'f[0][0] = 1': '什么都不选、和为 0：==1 种方案==，所有计数从它长出来',
        'mod =': '答案可能很大，对 `{mod}` 取模',
        'for num in arr': lambda S, B, r: (f'处理第 `{S.num}`：每个数只能用一次' if 'num' in S else '所有数处理完'),
        'f[3][j] =': '选 `{num}` 当第 3 个数：`f[3][{j}] += f[2][{j-num}]` → =={f[3][j]}==。==先更新 3，再 2，再 1==，保证用的是上一轮的值',
        'f[2][j] =': '选 `{num}` 当第 2 个数：`f[2][{j}] += f[1][{j-num}]` → =={f[2][j]}==',
        'f[1][j] =': '选 `{num}` 当第 1 个数：`f[1][{j}] += f[0][{j-num}]` → =={f[1][j]}==',
        'return f[3][target]': '选 3 个数、和为 `{target}` 的方案：=={f[3][target]}==',
    },
    cards=dict(
        one_liner='target 只有几百，直接 DP：选几个数、和是多少',
        complexity='时间 `O(n·target)`，空间 `O(target)`',
        problem=['给整数数组 `arr` 和 `target`，数 `i<j<k` 且 `arr[i]+arr[j]+arr[k]==target` 的三元组个数',
                 '结果对 `10^9+7` 取模',
                 '示例：`[1,2,2,3]`, `target=6` → `2`（两种 `1+2+3`）'],
        quote='注意到这里的target最大只到300，那么也可以用动态规划来求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想到枚举第一个数再配对两数之和，但 target 很小',
              '`f[c][s]`：前若干个数里选 `c` 个、和为 `s`',
              '每个数选或不选，压掉 i 一维后，`j` 要从大到小防止同一数用两次'],
        summary=['时间 `O(3·n·target)`，空间 `O(4·target)`',
                 '易错：`j` 倒序，且按 3、2、1 的顺序更新',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
