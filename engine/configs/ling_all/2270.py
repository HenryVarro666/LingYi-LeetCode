def _pre(S):
    out, s = [], 0
    for x in S['nums'][:-1]:
        s += x
        out.append(s)
    return out


def _text(S):
    nums = S['nums']
    if 't' not in S:
        return f"总和 `total = {sum(nums)}`"
    t = S['t']
    pre = _pre(S)
    return f"总和 `{sum(nums)}`，阈值 `t = (total + 1) // 2 = {t}`；前缀和 `{pre}`，其中 ==≥ {t}== 的有 =={sum(p >= t for p in pre)}== 个"


def _color(S, i, v):
    if 't' not in S:
        return None
    return 'green' if _pre(S)[i] >= S['t'] else 'pink'


CONFIG = dict(
    num=2270, title='分割数组的方案数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='前缀和 · s ≥ ⌈total/2⌉',
    tags=['灵神题单', '动态规划', '难度分 1334'],
    code='''
class Solution:
    def waysToSplitArray(self, nums: List[int]) -> int:
        t = (sum(nums) + 1) // 2
        return sum(s >= t for s in accumulate(nums[:-1]))
''',
    call='Solution().waysToSplitArray([10,4,-8,7,3,-2])',
    expect=4,
    views=[
        dict(type='text', fn=_text, size=28),
        dict(type='array', var='nums', label='nums（最后一个不参与分割）', h=230,
             dim=lambda S, i, v: i == len(S['nums']) - 1),
        dict(type='array', var=lambda S: _pre(S), label='前缀和 s = accumulate(nums[:-1])（绿 = s ≥ t，合法分割）', h=260,
             color=_color),
    ],
    watch=[('t', 't', 'purple'), ('total', 'sum(nums)', 'blue')],
    captions={
        't = (sum': '`2s ≥ total` 等价于 `s ≥ ceil(total/2)`：`t = ({sum(nums)} + 1) // 2 = {t}`，前缀和只要 ≥ `t` 就合法',
        'return sum': '对 `accumulate(nums[:-1])` 的每个前缀和 `s` 判断 `s >= t`，True 记 1：共 =={ret}== 种合法分割（`nums[:-1]` 保证右边至少剩一个数）',
    },
    cards=dict(
        one_liner='把「左 ≥ 右」改写成「左前缀和 ≥ ceil(总和/2)」',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['在下标 `i` 切开：前 `i+1` 个数之和 ≥ 剩下的数之和，才算合法分割',
                 '`i` 的右边至少要有一个元素；返回合法分割的个数',
                 '示例：`[10,4,-8,7]` → `2`'],
        quote='题目要求 s ≥ total − s，即 2s ≥ total，也就是 s ≥ ceil(total/2) = floor((total+1)/2)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设前缀和 `s`，右边就是 `total - s`，不等式化简为 `2s ≥ total`',
              '向上取整写成整数除法：`t = (total + 1) // 2`，负数总和同样成立',
              '`accumulate(nums[:-1])` 恰好枚举 `i = 0 … n-2`，数一数 `s >= t` 的个数'],
        after=[dict(heading='逐个看前缀和', lines=[
            '`[10,4,-8,7,3,-2]`：`total = 14`，`t = 7`',
            '前缀和 `10, 14, 6, 13, 16`，只有 `6 < 7` 不合法',
            '所以合法分割有 `4` 种',
        ])],
        summary=['时间 `O(n)`，空间 `O(1)`（`accumulate` 是迭代器）',
                 '易错点：`nums[:-1]` 保证右边非空；漏掉它会多算整段',
                 '向上取整 `(x + 1) // 2` 在 Python 对负数也是向下取整的正确结果',
                 '同类：前后缀分解专题'],
    ),
)
