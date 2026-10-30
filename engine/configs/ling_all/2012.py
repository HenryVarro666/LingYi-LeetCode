def _beauty(a, i):
    if max(a[:i]) < a[i] < min(a[i + 1:]):
        return 2
    return 1 if a[i - 1] < a[i] < a[i + 1] else 0


def _color(S, i, v):
    if S['_line'] < 10 or 'x' not in S:
        return None
    cur = S['i']
    if i == cur:
        return 'blue'
    if 1 <= i < cur or (i == cur and False):
        b = _beauty(S['nums'], i)
        return 'green' if b == 2 else 'yellow' if b == 1 else None
    return None


def _txt(S):
    if 'x' not in S or S['_line'] < 10:
        return '先倒序算出后缀最小值 `suf_min`'
    i, x = S['i'], S['x']
    return f"`pre_max = {S['pre_max']}`（`[0,{i-1}]` 最大）　`x = {x}`　`suf_min[{i+1}] = {S['suf_min'][i+1]}`（`[{i+1},n-1]` 最小）"


CONFIG = dict(
    num=2012, title='数组美丽值求和', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解 · 后缀最小值数组 + 前缀最大值变量',
    tags=['灵神题单', '动态规划', '难度分 1468'],
    code='''
class Solution:
    def sumOfBeauties(self, nums: List[int]) -> int:
        n = len(nums)
        suf_min = [0] * n  # 后缀最小值
        suf_min[n - 1] = nums[n - 1]
        for i in range(n - 2, 1, -1):
            suf_min[i] = min(suf_min[i + 1], nums[i])

        ans = 0
        pre_max = nums[0]  # 前缀最大值
        for i in range(1, n - 1):
            x = nums[i]
            # 此时 pre_max 表示 [0, i-1] 中的最大值
            if pre_max < x < suf_min[i + 1]:
                ans += 2
            elif nums[i - 1] < x < nums[i + 1]:
                ans += 1
            # 更新后 pre_max 表示 [0, i] 中的最大值
            pre_max = max(pre_max, x)
        return ans
''',
    call='Solution().sumOfBeauties([1,3,2,4,5,6,5,7,8])',
    expect=5,
    views=[
        dict(type='text', fn=_txt, size=24),
        dict(type='array', var='nums', label='nums（蓝 = 当前，绿 = 美丽值 2，黄 = 美丽值 1）', h=220, pointers={'i': 'blue'}, color=_color),
        dict(type='array', var='suf_min', label='suf_min[i]：后缀 [i, n-1] 的最小值', h=220, pointers={'i + 1': 'pink'}, pointer_labels={'i + 1': 'i+1'},
             color=lambda S, i, v: 'cyan' if S['_line'] < 10 and i >= S['i'] else None),
    ],
    watch=['i', ('pre_max', 'pre_max', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'suf_min = [0]': '`suf_min[i]` 表示后缀 `[i, n-1]` 的最小值',
        'suf_min[n - 1]': '最后一个后缀只有 `nums[n-1] = {nums[n-1]}`',
        'suf_min[i] =': '倒序：`suf_min[{i}] = min(suf_min[{i+1}], nums[{i}])` = =={suf_min[i]}==',
        'pre_max = nums[0]': '`pre_max` 初始为 `nums[0] = {pre_max}`：下标 0 左边只有它自己',
        'for i in range(1': lambda S, B, r: ('枚举完了，`i = n-2` 已是最后一个' if B.get('x') is not None and S.i == B.get('i') else f'枚举 `i = {S.i}`（下标 0 和 n-1 不算美丽值）'),
        'x = nums[i]': '`x = nums[{i}] = {x}`',
        'if pre_max <': '`pre_max = {pre_max} < x = {x} < suf_min[{i+1}] = {suf_min[i+1]}`？ → {"==左边都更小、右边都更大，美丽值 2==" if pre_max < x < suf_min[i+1] else "不成立"}',
        'ans += 2': '美丽值 2：`ans` → =={ans}==',
        'elif nums[i - 1]': '只看相邻：`{nums[i-1]} < {x} < {nums[i+1]}`？ → {"==成立，美丽值 1==" if nums[i-1] < x < nums[i+1] else "不成立，美丽值 0"}',
        'ans += 1': '美丽值 1：`ans` → =={ans}==',
        'pre_max = max': '`pre_max` 更新为 =={pre_max}==，现在表示 `[0, {i}]` 的最大值',
        'return ans': '美丽值总和 =={ans}==',
    },
    cards=dict(
        one_liner='大于前缀最大值、小于后缀最小值，就是美丽值 2',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['对 `1 <= i <= n-2`：左边全比 `nums[i]` 小、右边全比它大，美丽值 `2`',
                 '否则若 `nums[i-1] < nums[i] < nums[i+1]`，美丽值 `1`；都不满足为 `0`',
                 '求美丽值之和；本视频：`[1,3,2,4,5,6,5,7,8]` → `5`'],
        quote='nums[i] 要大于 i 左边的所有数，也就是大于前缀 [0,i-1] 中的最大值。nums[i] 要小于 i 右边的所有数，也就是小于后缀 [i+1,n-1] 中的最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把「左边都更小、右边都更大」翻译成：比前缀最大值大、比后缀最小值小',
              '`suf_min` 必须倒序算；`pre_max` 只要一个变量，边算边用',
              '先用旧的 `pre_max` 判断，最后才更新它'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：判断时 `pre_max` 是 `[0,i-1]` 的最大值，==判断完才把 x 并进去==',
                 '`suf_min` 只需算到下标 2（循环 `range(n-2, 1, -1)`），因为用到的最小下标是 `i+1 >= 2`',
                 '同类题见灵神动态规划题单「前后缀分解」专题'],
    ),
)
