NUMS = [3, 4, 6, 2, 5]
K = 30


def _color(S, i, v):
    if 'index' not in S:
        return None
    if S['p'] <= i <= S['index']:
        return 'green' if S['_line'] == 17 else 'cyan'
    if i < S['p']:
        return None
    return None


def _top(S):
    if 'index' not in S:
        return f'`k = {K}`：元素都是正数，==乘积随长度单调增=='
    p, r = S['p'], S['index']
    if S['_line'] == 15:
        return f"除掉 `nums[{p}] = {NUMS[p]}` 后 `now = {S['now']}`，接着 p 右移"
    win = NUMS[p:r + 1]
    expr = ' × '.join(map(str, win)) if win else '空'
    ok = S['now'] < K
    return f"`nums[{p}..{r}]`：`{expr} = {S['now']}` {'<' if ok else '≥'} `{K}`" + ('' if ok else ' → p 右移')


def _ends(S):
    if 'index' not in S or S['_line'] != 17:
        return ''
    p, r = S['p'], S['index']
    parts = ['[' + ','.join(map(str, NUMS[i:r + 1])) + ']' for i in range(p, r + 1)]
    return f"以 {r} 结尾：{'、'.join(parts)}"


def _while(S, B, ret):
    if S.now >= S.k:
        return f'`now = {S.now} ≥ {S.k}`：这一段乘积太大 → ==把 p 往右移=='
    return f'`now = {S.now} < {S.k}`：`p..index` 这一段已经小于 k'


CONFIG = dict(
    num=713, title='乘积小于 K 的子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='滑动窗口 · 以 index 结尾计数',
    tags=['labuladong', '灵神核心路线'],
    code='''
class Solution(object):
    def numSubarrayProductLessThanK(self, nums, k):

        if k <= 1:
            return 0

        n = len(nums)
        now = 1
        p = 0
        res = 0

        for index in range(n):
            now *= nums[index]
            while now >= k:
                now //= nums[p]
                p += 1
            res += index - p + 1

        return res
''',
    call=f'Solution().numSubarrayProductLessThanK({NUMS}, {K})',
    expect=9,
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='array', var='nums', label='nums（青 = 当前一段 p..index，绿 = 以 index 结尾的合法子数组起点）',
             pointers={'p': 'blue', 'index': 'pink'}, window=('p', 'index'), color=_color, cell=120, h=300),
        dict(type='text', fn=_ends, size=26, h=80),
    ],
    watch=[('p', 'p', 'blue'), ('index', 'index', 'pink'), ('now', 'now', 'orange'), ('res', 'res', 'green')],
    captions={
        'if k <= 1': '元素都是正数，乘积 ≥ 1；`k = {k}` 大于 1，继续',
        'n = len': '`n = {n}`',
        'now = 1': '`now`：`p` 到 `index` 这一段的乘积',
        'p = 0': '`p`：左指针，从 0 开始',
        'res = 0': '`res`：答案计数',
        'for index in': lambda S, B, r: ('index 已到末尾，扫描结束' if 'index' in B and B.index == S.index
                                         else f'right 指针 `index` 右移到 {S.index}'),
        'now *= nums[index]': '把 `nums[{index}] = {nums[index]}` 乘进来：`now = {now}`',
        'while now >= k': _while,
        'now //= nums[p]': '除掉 `nums[{p}]`：`now = {B.now} // {nums[p]} = {now}`',
        'p += 1': '`p` → {p}',
        'res += index': '以 `index = {index}` 结尾的合法子数组有 `{index} − {p} + 1` 个 → `res = {res}`',
        'return res': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='right 每走一步，p 追到乘积小于 k，再加上以 right 结尾的个数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给正整数数组 `nums` 和整数 `k`',
                 '统计==乘积严格小于 k== 的连续子数组数目',
                 '示例：`[10,5,2,6], k = 100` → `8`；本视频 `[3,4,6,2,5], k = 30` → `9`'],
        quote='若当前left到right这一段的乘积大于等于k，那么就将left往右移动直到乘积小于k。此时就得到以right结尾的乘积小于k的子数组一共有==right - left + 1==个。',
        quote_src='—— yiduobo 题解原文',
        idea=['元素都是正数，==k ≤ 1 时答案必然是 0==',
              '代码里 `p` 是 left，`index` 是 right，`now` 是这一段乘积',
              '按「以 index 结尾」分类计数，每个子数组恰好数一次'],
        summary=['时间 `O(n)`：`p` 只往右走；空间 `O(1)`',
                 '`now` 只有乘和整除，始终是整数；p 右移时用除法撤销',
                 '先判 `k <= 1`，否则 `while now >= k` 会让 p 越界',
                 '原文为 Python 2 写法，`now /= nums[p]` 已改为 `now //= nums[p]`'],
    ),
)
