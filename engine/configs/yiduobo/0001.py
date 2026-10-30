def _vals(S):
    return [p[0] for p in S['sorted_list']] if 'sorted_list' in S else None


def _sum_text(S):
    if 'right' not in S:
        return '先排序，再从两端开始考察'
    a = S['sorted_list']
    l, r, t = S['left'], S['right'], S['target']
    s = a[l][0] + a[r][0]
    rel = '等于' if s == t else ('大于' if s > t else '小于')
    return f"`a[i] + a[j] = {a[l][0]} + {a[r][0]} = {s}` =={rel}== `target = {t}`"


def _orig_color(S, i, v):
    if 'sorted_list' not in S:
        return 'yellow' if S.get('index') == i else None
    if 'right' not in S:
        return None
    a = S['sorted_list']
    if i == a[S['left']][1]:
        return 'blue'
    if i == a[S['right']][1]:
        return 'pink'
    return None


def _cmp(S, B, ret):
    a, l, r, t = S.sorted_list, S.left, S.right, S.target
    s = a[l][0] + a[r][0]
    if s == t:
        return f'`{a[l][0]} + {a[r][0]} = {t}`：==情况 1==，`a[i]` 就是 x，`a[j]` 就是 y'
    return f'`{a[l][0]} + {a[r][0]} = {s}` ≠ `{t}`，不是情况 1'


def _gt(S, B, ret):
    a, l, r, t = S.sorted_list, S.left, S.right, S.target
    s = a[l][0] + a[r][0]
    if s > t:
        return f'`{s} > {t}`：==情况 3==，`x + a[j] ≥ a[i] + a[j] > x + y` ⇒ `a[j] > y`'
    return f'`{s} < {t}`：==情况 2==，`a[i] + y ≤ a[i] + a[j] < x + y` ⇒ `a[i] < x`'


CONFIG = dict(
    num=1, title='两数之和', difficulty='Easy', category='哈希',
    author='yiduobo', technique='排序 + 双指针（O(n log n) 做法）',
    code='''
class Solution(object):
    def twoSum(self, nums, target):
        sorted_list = sorted([[x, index] for index, x in enumerate(nums)], key=lambda d:d[0])
        left = 0
        right = len(sorted_list) - 1
        while True:
            if sorted_list[left][0] + sorted_list[right][0] == target:
                return[sorted_list[left][1], sorted_list[right][1]]
            elif sorted_list[left][0] + sorted_list[right][0] > target:
                right -= 1
            else:
                left += 1
''',
    call='Solution().twoSum([13,2,9,16,7,5], 20)',
    expect=[4, 0],
    views=[
        dict(type='text', fn=_sum_text),
        dict(type='array', var='nums', color=_orig_color, h=190, cell=76,
             label='nums（原数组，下标就是要返回的答案）'),
        dict(type='array', var=_vals, pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), h=250,
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right']),
             label='sorted_list（数值）'),
        dict(type='text', size=24, fn=lambda S: ('原下标：' + '  '.join(f"`{x}→{i}`" for x, i in S['sorted_list']) + '　答案一定在框内') if 'sorted_list' in S else ''),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'target'],
    captions={
        'sorted_list = sorted': lambda S, B, r: ('再按数值从小到大排序：==排序会打乱位置，所以原下标要一起带着走=='
                                                 if 'sorted_list' in S else f'打包 `[数值, 原下标]`：`[{S.x}, {S.index}]`'),
        'left = 0': '`i = 0` 从最左（最小）开始',
        'right = len': '`j = len − 1 = {right}` 从最右（最大）开始；设答案 `x ≤ y`，则 `a[i] ≤ x ≤ y ≤ a[j]`',
        'while True': lambda S, B, r: ('题目保证有解，直接 `while True`' if S.left == 0 and S.right == len(S.sorted_list) - 1
                                       else f'继续考察 `[{S.left}, {S.right}]`'),
        '== target:': _cmp,
        '> target:': _gt,
        'right -= 1': '`a[j]` 比 y 还大，不可能是答案 → 问题变成在 `[i, j−1]` 中找：`right` → {right}',
        'left += 1': '`a[i]` 比 x 还小，不可能是答案 → 问题变成在 `[i+1, j]` 中找：`left` → {left}',
        'return[': '返回两数的==原下标==：`[{sorted_list[left][1]}, {sorted_list[right][1]}]`（`nums[{sorted_list[left][1]}] + nums[{sorted_list[right][1]}] = {target}`）',
    },
    cards=dict(
        one_liner='排序后两端夹逼：每比较一次，问题规模减一',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['在 `nums` 中找出和为 `target` 的==两个==整数，返回它们的下标',
                 '同一个元素不能用两次；保证只有一个答案',
                 '示例：`nums = [2,7,11,15], target = 9` → `[0,1]`',
                 '本视频：`nums = [13,2,9,16,7,5], target = 20` → `[4,0]`'],
        quote='每次比较，可以认为是==从i到j中找出两个满足条件的数==，变成了==i + 1到j中，或者i到j - 1中==找出两个满足条件的数。每次比较问题的规模减少1。',
        quote_src='—— yiduobo 题解原文',
        idea=['数组从小到大排好，设答案两数 `x ≤ y`，始终有 `a[i] ≤ x ≤ y ≤ a[j]`',
              '和偏小：`a[i]+y ≤ a[i]+a[j] < x+y` ⇒ `a[i] < x`，扔掉 `a[i]`',
              '和偏大：`x+a[j] ≥ a[i]+a[j] > x+y` ⇒ `a[j] > y`，扔掉 `a[j]`'],
        summary=['排序 `O(n log n)` + 双指针 `O(n)`；空间 `O(n)` 存 `[数值, 原下标]`',
                 '易错：返回的是==原下标==，所以排序前要把 index 绑在数值上',
                 '原文还给了 `O(n²)` 的二重循环做法；哈希表可做到 `O(n)`',
                 '原文为 Python 2 风格（`class Solution(object)`），只删去了类型说明文档字符串，其余照搬'],
    ),
)
