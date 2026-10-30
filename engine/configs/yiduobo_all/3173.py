NUMS = [2, 5, 4, 9, 6]


def _i(S):
    i = S.get('index')
    return i if isinstance(i, int) and 1 <= i < len(S['nums']) else None


def _show(S):
    n = S['nums']
    i = _i(S)
    if i is None:
        return '`answer[k] = nums[k+1] | nums[k]`：相邻两个数按位或，共 `n − 1` 个'
    return f"`nums[{i}] | nums[{i-1}]` = `{n[i]} | {n[i-1]}` = =={n[i] | n[i-1]}=="


def _bin(S):
    n = S['nums']
    i = _i(S)
    if i is None:
        return ''
    a, b = n[i - 1], n[i]
    return f"二进制：`{a:04b}` | `{b:04b}` = ==`{a | b:04b}`==（有 1 的位保留 1）"


def _pair(S, k):
    n = S['nums']
    if k >= len(n):
        return ''
    a, b = n[k - 1], n[k]
    return f"`nums[{k}] | nums[{k-1}]` = `{b:04b}` | `{a:04b}` = `{a | b:04b}` = =={a | b}=="


CONFIG = dict(
    num=3173, title='相邻元素的按位或', difficulty='Easy', category='位运算',
    author='yiduobo', technique='一趟遍历 · 列表推导式',
    tags=[],
    code='''
class Solution(object):
    def orArray(self, nums):
        return [nums[index] | nums[index - 1] for index in range(1, len(nums))]
''',
    call=f'Solution().orArray({NUMS!r})',
    expect=[7, 5, 13, 15],
    views=[
        dict(type='array', var='nums', label='nums', cell=100, h=170),
        dict(type='text', fn=lambda S: '相邻两数按位或（index 从 1 到 n−1）：', size=28, h=70),
    ] + [
        dict(type='text', size=30, h=75, fn=(lambda k: lambda S: _pair(S, k))(k)) for k in range(1, 5)
    ],
    watch=[('nums', 'nums', 'blue'), ('len(nums)', 'len(nums)')],
    captions={
        'return [': lambda S, B, ret: (f"从下标 1 开始，每个 `index` 把 `nums[index]` 与前一个 `nums[index - 1]` 按位或，收集成答案数组"
                                       + (f"：==`{ret}`==" if ret is not None else '')),
    },
    cards=dict(
        one_liner='下标 1 往后，当前数 | 上一个数',
        complexity='时间 `O(n)`，空间 `O(1)`（不计答案数组）',
        problem=['给数组 `nums`，求长度为 `n − 1` 的数组 `answer`',
                 '`answer[i] = nums[i] | nums[i + 1]`，即相邻两个数的按位或',
                 '示例：`[1,3,7,15]` → `[3,7,15]`',
                 '本视频：`[2,5,4,9,6]` → `[7,5,13,15]`'],
        quote='按照题目要求从下标1开始向后遍历，将当前元素与上一个元素按位或的结果加入到答案数组中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['答案比原数组少一个，所以 `index` 从 1 开始',
              '每个位置计算 `nums[index] | nums[index - 1]`，按顺序放入答案',
              '一行列表推导式搞定，没有任何技巧'],
        after=[dict(heading='按位或怎么算', lines=['逐位比较：两个数只要有一个在这一位是 1，结果这一位就是 1', '`5 | 2`：`0101` 和 `0010` 逐位或得 `0111` = 7', '`4 | 5`：`0100` 与 `0101` 得 `0101` = 5，结果不会比较大的数更小'])],
        summary=['时间 `O(n)`，空间 `O(1)`（不算返回的数组）',
                 '易错：`index` 从 1 开始，不是 0，否则 `nums[-1]` 会取到最后一个元素',
                 '按位或不满足“越或越小”，只会越或越大；这里每对独立计算，不要累积',
                 '原文为 Python 2 风格，只删去 def 后空行，代码无需其他修改'],
    ),
)
