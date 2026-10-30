def _text(S):
    if 'new_nums' not in S:
        return '一层一层往下算：每层由上一层相邻两数相加得到'
    return f'上一层 `nums`（{len(S["nums"])} 个）→ 正在生成的 `new_nums`（已有 {len(S["new_nums"])} 个）'


def _nn(S):
    return S.get('new_nums', [])


CONFIG = dict(
    num=2221, title='数组的三角和', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='逐层模拟',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def triangularSum(self, nums):

        n = len(nums)
        for i in range(n - 1):
            new_nums = []
            for j in range(1, len(nums)):
                new_nums.append((nums[j] + nums[j - 1]) % 10)
            nums = new_nums[:]
        
        return nums[0]
''',
    call='Solution().triangularSum([1,2,3,4,5])',
    expect=8,
    views=[
        dict(type='text', fn=_text),
        dict(type='array', var='nums', label='nums（上一层）', pointers={'j': 'blue'}, h=250, cell=96,
             color=lambda S, i, v: 'blue' if 'j' in S and i == S['j'] and S.get('_line') == 8 else ('cyan' if 'j' in S and i == S['j'] - 1 and S.get('_line') == 8 else None)),
        dict(type='array', var=lambda S: S.get('new_nums', []), label='new_nums（新一层）', h=250, cell=96,
             color=lambda S, i, v: 'green' if i == len(S.get('new_nums', [])) - 1 and S.get('_line') == 8 else None),
    ],
    watch=[('i', 'i', 'purple'), ('j', 'j', 'blue'), ('new_nums', 'new_nums', 'green')],
    captions={
        'for i in range(n - 1)': lambda S, B, ret: ('`n - 1` 层全部做完' if 'i' in B and B.i == S['i'] else f'一共要做 `n - 1 = {S["n"] - 1}` 层，第 `{S["i"]}` 层开始（每层少一个数）'),
        'new_nums = []': '新开一个空列表，用来装下一层',
        'for j in range': lambda S, B, ret: f'`j = {S["j"]}`：取 `nums[{S["j"] - 1}]` 和 `nums[{S["j"]}]` 这相邻一对' if 'j' in S and S.get('j') != B.get('j') else '这一层的相邻对都处理完了',
        'new_nums.append': '`({nums[j]} + {nums[j - 1]}) % 10 = {new_nums[-1]}`：加完立刻取模，数字不会变大',
        'nums = new_nums': '用新一层 `{new_nums}` 替换 `nums`，长度少 1',
        'return nums[0]': '只剩一个数 `{nums[0]}`，就是三角和',
    },
    cards=dict(
        one_liner='n 不大，直接一层一层模拟',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`nums` 每个数 0–9：每层把相邻两数之和取模 10，得到短一格的新数组',
                 '重复到只剩一个数，返回它',
                 '示例：`[1,2,3,4,5]` → `8`'],
        quote='看上去应该可以利用组合数学在O(n)的时间内求出结果，但是这里n的规模比较小，我就直接从上到下一层一层模拟计算了。',
        quote_src='—— yiduobo 题解',
        idea=['作者没有走组合数学：`n <= 1000`，`O(n^2)` 够用',
              '每层新建 `new_nums`，装满后整体替换 `nums`',
              '共 `n - 1` 层，最后 `nums[0]` 就是答案'],
        summary=['时间 `O(n^2)`，空间 `O(n)`（每层新建列表）',
                 '易错点：新值是 `(nums[j] + nums[j-1]) % 10`，别忘了取模',
                 '`nums = new_nums[:]` 复制一份，防止和 `new_nums` 共用同一个列表',
                 '数据更大时用组合数 `C(n-1,i)` 加权求和，见 3463'],
    ),
)
