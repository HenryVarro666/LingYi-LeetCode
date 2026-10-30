def _formula(S, B):
    inner = S.get('_inner', {})
    ln = S.get('_line', 0)
    if 'j' in inner and 'old' in inner and ln in (6, 7, 8, 9):
        j, old, new = inner['j'], inner['old'], inner['new']
        f = B.get('f', S['f'])
        if j >= 1:
            return f'第 {j} 轮清掉它：`f[{j-1}] + {old} + {new}×{j}` = =={f[j-1] + old + new * j}==，不清：`f[{j}] = {f[j]}`'
    if 'index' in inner and 'now' in inner and ln >= 11:
        return f'时刻 `{inner["index"]}` 的数组和 `now − v` = {inner["now"]} − {inner["v"]} = =={inner["now"] - inner["v"]}==（x = {S["x"]}）'
    return '`f[j]`：前 i 个位置里清空 j 个，最多少掉多少'


def _fcolor(S, i, v):
    inner = S.get('_inner', {})
    ln = S.get('_line', 0)
    if ln <= 9 and inner.get('j') == i:
        return 'yellow'
    if ln >= 11 and inner.get('index') == i:
        return 'yellow'
    return None


CONFIG = dict(
    num=2809, title='使数组和小于等于 x 的最少时间', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='枚举时刻 + 排序后背包',
    tags=['其他线性 DP', '难度分 2979'],
    code='''
class Solution(object):
    def minimumTime(self, nums1, nums2, x):

        sorted_nums = sorted(zip(nums2, nums1))
        f = [0] * (len(sorted_nums) + 1)
        for i, (new, old) in enumerate(sorted_nums):
            for j in range(i + 1, 0, -1):
                f[j] = max(f[j], f[j - 1] + old + new * j)
        
        now = sum(nums1)
        s = sum(nums2)
        for index, v in enumerate(f):
            if now - v <= x:
                return index
            now += s
        
        return -1
''',
    call='Solution().minimumTime([1,2,3], [1,2,3], 4)',
    expect=3,
    skip=['for j in range'],
    views=[
        dict(type='text', fn=lambda S: ('按 `nums2` 排序：' + '  '.join(f'==({a},{b})==' for a, b in S['sorted_nums'])) if 'sorted_nums' in S else '先按 `nums2` 从小到大排序：增长慢的先清，增长快的后清', size=26, h=60),
        dict(type='array', var='f', label='f[j]：清空 j 个位置的最大收益', h=200, cell=90,
             pointers={'j': 'blue', 'index': 'pink'}, color=_fcolor),
        dict(type='text', fn=_formula, size=26, h=70),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'orange'), ('old', 'old'), ('new', 'new'), ('now', 'now', 'green'), ('s', 's'), ('index', 'index', 'pink')],
    captions={
        'sorted_nums = sorted': '`zip(nums2, nums1)` 直接排序：先按 `nums2` 升序，得 `{sorted_nums}`。若两个位置顺序反了，交换后后半部分变大，所以==增长慢的先清空==',
        'f = [0] *': '`f[j]` 初始全 0：长度 `n + 1`，`f[0] = 0` 表示一个都不清',
        'for i, (new, old)': lambda S, B, r: (f'看第 `{S.i}` 个位置：`nums2 = {S.new}`，`nums1 = {S.old}`' if 'i' not in B or S.i != B.i or S.new != B.new
                                             else '所有位置处理完，`f` 已经算好'),
        'f[j] = max': '`f[{j}] = max(f[{j}], f[{j-1}] + {old} + {new}×{j})` = =={f[j]}==：它 nums2 最大，必在==第 {j} 轮==清，收益 `old + new×j`；倒序省掉 i 维',
        'now = sum': '`now = sum(nums1) = {now}`：时刻 0 什么都不清的数组和',
        's = sum': '`s = sum(nums2) = {s}`：每过一秒，不清的话和就多 `s`',
        'for index, v': lambda S, B, r: (f'枚举时刻 `index = {S.index}`，清空 {S.index} 个位置最多少掉 `v = {S.v}`' if 'index' in S else '枚举完毕，没有时刻满足'),
        'if now - v': '时刻 `{index}` 最小数组和 = `{now} − {v}` = =={now - v}==，{"<= x，找到了" if now - v <= x else "> x，不行"}（x = {x}）',
        'return index': '最少时刻 `{index}`，返回 =={ret}==',
        'now += s': '时刻加一，`now` 加上 `s`：`now = {now}`',
        'return -1': '所有时刻都不够 → 无解，返回 `-1`',
    },
    max_steps=70,
    cards=dict(
        one_liner='清空次序按 nums2 升序，枚举时刻 t 做背包',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['每秒 `nums1[i]` 加上 `nums2[i]`，然后可把一个位置清零',
                 '要让数组和 `<= x`，求最少时间，不行返回 `-1`',
                 '示例：`[1,2,3]`、`[1,2,3]`、`x = 4` → `3`'],
        quote='同一个位置上不会进行多次清空操作，这是因为……会让数组值变为0，这也就意味着前面的情况操作是无效的。',
        quote_src='—— yiduobo 题解',
        idea=['答案 `t <= n`，于是枚举 `t`，算时刻 `t` 的最小数组和',
              '要让 `(nums1[p1] + nums2[p1]) + ... + (nums1[pt] + nums2[pt]×t)` 最大',
              '`nums2` 小的先清，大的后清（交换论证），排序后做 `f[i][j]` 背包'],
        summary=['时间 `O(n^2)`，空间 `O(n)`（倒序更新去掉 i 维）',
                 '易错：排序键是 `nums2`，所以 `zip(nums2, nums1)`',
                 '`now` 每轮加 `s`，减去 `f[t]` 才是时刻 t 的最小和',
                 '原文本身已是 Python 3 可运行写法，无需改动'],
    ),
)
