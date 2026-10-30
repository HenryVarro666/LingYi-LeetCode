def _col(S, i, v):
    m = S.get('m')
    if m is None:
        return None
    if v == m:
        return 'green'
    if v % m:
        return 'pink'
    return None


def _text(S):
    if 'm' not in S:
        return '先找最小值 `m`，再看有没有不是 `m` 倍数的数'
    if 'x' in S and S.get('_line') in (4, 5):
        x, m = S['x'], S['m']
        return f'`{x} % {m}` = =={x % m}==' + ('：非 0 → 能造出比 m 更小的正整数' if x % m else '：是 m 的倍数')
    return f'`m = {S["m"]}`，粉色 = 不是 m 倍数的数，绿色 = 最小值'


CONFIG = dict(
    num=3012, title='通过操作使数组长度最小', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='最小值 + 倍数判断',
    tags=['贪心与思维', '难度分 1833'],
    code='''
class Solution:
    def minimumArrayLength(self, nums: List[int]) -> int:
        m = min(nums)
        for x in nums:
            if x % m:
                return 1
        return (nums.count(m) + 1) // 2
''',
    call='Solution().minimumArrayLength([5,5,5,10,5])',
    expect=2,
    views=[
        dict(type='text', fn=_text, size=30, h=90),
        dict(type='array', var='nums', color=_col, h=300, cell=110),
    ],
    watch=[('m', 'm', 'green'), 'x'],
    captions={
        'm = min': '`m = min(nums) = {m}`：用最小值去模别的数，结果还是它自己，等于==直接删掉那个数==',
        'for x in nums': '依次检查每个数 `x` 是不是 `m` 的倍数',
        'if x % m': '`{x} % {m} = {x % m}`' ,
        'return 1': '有数不是 `m` 的倍数：`x % m` 落在 `[1, m-1]`，比 `m` 还小 → ==它成为唯一最小值，能删到只剩 1 个==',
        'return (nums': '全是 `m` 的倍数：先用 `m` 删光更大的数，剩 `{nums.count(m)}` 个 `m`，两两相消 → `({nums.count(m)}+1)//2` = =={ret}==',
    },
    cards=dict(
        one_liner='最小值只有它自己能产生更小的数；造不出就两两抵消',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次选下标 `i≠j`（值都 > 0），把 `nums[i] % nums[j]` 放到末尾，删掉 `nums[i]`、`nums[j]`',
                 '求任意次操作后数组的==最小长度==',
                 '示例：`[5,5,5,10,5]` → `2`'],
        quote='如果能构造出一个小于 m = min(nums) 的正整数，那么也可以返回 1。当且仅当 nums 中有不是 m 的倍数的数，我们才能构造出一个小于 m 的正整数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['拿最小值 `m` 去模更大的数，结果还是 `m` → 等价于==删掉那个大数==',
              '若有 `x % m` 落在 `1..m-1`，就得到新的唯一最小值 → 答案 `1`',
              '否则全是 `m` 的倍数：剩 `cnt` 个 `m` 两两消，剩 `⌈cnt/2⌉` 个'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`(cnt + 1) // 2` 就是向上取整的 `cnt / 2`',
                 '易错：是==不是 m 的倍数==就返回 1，不是“不等于 m”',
                 '最小值恰有一个时，也会走到 `cnt = 1` → 答案 1'],
    ),
)
