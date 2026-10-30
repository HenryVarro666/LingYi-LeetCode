_IX = 'index if _line in (8, 9, 12, 13) else None'


def _txt(S):
    if 'j' in S:
        j = S['j']
        p, s, x = S['prefix'][j - 1], S['suffix'][j + 1], S['nums'][j]
        return f"`(prefix[{j - 1}] − nums[{j}]) × suffix[{j + 1}]` = `({p} − {x}) × {s}` = =={(p - x) * s}=="
    if 'suffix' in S:
        return '`suffix` 从右往左追加，最后 `reverse()` 成正常顺序'
    return '`prefix[i]`：`nums[0..i]` 的最大值'


CONFIG = dict(
    num=2874, title='有序三元组中的最大值 II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举中间 j · 前后缀最大值',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1583'],
    code='''
class Solution(object):
    def maximumTripletValue(self, nums):

        res = 0
        n = len(nums)

        prefix = [nums[0]]
        for index in range(1, n):
            prefix.append(max(prefix[-1], nums[index]))

        suffix = [nums[-1]]
        for index in range(n - 2, -1, -1):
            suffix.append(max(suffix[-1], nums[index]))
        suffix.reverse()

        for j in range(1, n - 1):
            res = max(res, (prefix[j - 1] - nums[j]) * suffix[j + 1])

        return res
''',
    call='Solution().maximumTripletValue([3,12,6,1,9,2,7])',
    expect=99,
    views=[
        dict(type='array', var='nums', label='nums', pointers={_IX: 'cyan', 'j': 'blue'}, pointer_labels={_IX: 'index'}, h=190),
        dict(type='array', var='prefix', label='prefix（前缀最大值）', pointers={'j - 1': 'orange'}, pointer_labels={'j - 1': 'j−1'}, h=190),
        dict(type='array', var='suffix', label='suffix（后缀最大值）', pointers={'j + 1': 'pink'}, pointer_labels={'j + 1': 'j+1'}, h=190),
        dict(type='text', fn=_txt, h=80, size=28),
    ],
    watch=[('index', 'index', 'cyan'), ('j', 'j', 'blue'), ('res', 'res', 'green')],
    skip=['for index in range'],
    captions={
        'res = 0': '答案只取非负数，`res` 从 0 开始',
        'n = len': '`n = {n}`',
        'prefix = [nums[0]]': '正着一趟：`prefix` 先放 `nums[0] = {nums[0]}`',
        'prefix.append': '`prefix` 追加 `max({prefix[-2]}, {nums[index]}) = {prefix[-1]}`',
        'suffix = [nums[-1]]': '反着一趟：`suffix` 先放 `nums[-1] = {nums[-1]}`',
        'suffix.append': '`suffix` 追加 `max({suffix[-2]}, {nums[index]}) = {suffix[-1]}`',
        'suffix.reverse()': '反转后 `suffix[i]` 就是 `nums[i..]` 的最大值：`{suffix}`',
        'for j in range(1, n - 1)': lambda S, B, r: (f'枚举中间元素 `j = {S.j}`：左边挑最大的 i，右边挑最大的 k' if B.get('j') != S.j else '枚举结束'),
        'res = max(res': lambda S, B, r: (
            (f'`prefix[{S.j - 1}] = {S.prefix[S.j - 1]} < nums[{S.j}] = {S.nums[S.j]}`：乘积为负，`res` 保持 {S.res}' if S.prefix[S.j - 1] < S.nums[S.j]
             else f'`({S.prefix[S.j - 1]} − {S.nums[S.j]}) × {S.suffix[S.j + 1]} = {(S.prefix[S.j - 1] - S.nums[S.j]) * S.suffix[S.j + 1]}` → `res = {S.res}`')),
        'return res': '最大值为 `{res}`',
    },
    cards=dict(
        one_liner='枚举中间的 j，左取前缀最大、右取后缀最大',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['求 `i < j < k` 时 `(nums[i] − nums[j]) * nums[k]` 的最大值，全为负数则返回 `0`',
                 '`nums[i]` 都是正数；示例：`[12,6,1,2,7]` → `77`',
                 '本视频：`[3,12,6,1,9,2,7]` → `(12 − 1) × 9 = 99`'],
        quote='对于这类三元组的求解，常见的做法是==枚举中间元素的下标==，本题就是枚举j，然后尝试找出适配j的最优的i和k。',
        quote_src='—— yiduobo 题解原文（2873 & 2874 合并题解）',
        idea=['元素都是正数、答案取非负 → 只需考虑 `nums[i] ≥ nums[j]`',
              '此时 `nums[i]`、`nums[k]` 都应==尽量大==',
              '变成前缀最大值与后缀最大值问题：正反两趟遍历预处理'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`j` 只能取 `1..n−2`：两边都至少要有一个元素',
                 '`suffix` 是倒着 append 的，记得 `reverse()`',
                 '原文已是 `range`，代码在 Python 3 下可直接运行，未做修改'],
    ),
)
