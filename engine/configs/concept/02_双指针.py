def _formula(S):
    if 'a' in S and 'l' in S and S['l'] < S['r']:
        a, l, r, t = S['a'], S['l'], S['r'], S['target']
        s = a[l] + a[r]
        rel = '=' if s == t else ('>' if s > t else '<')
        tail = {'=': '==找到！==', '>': '太大 → 扔掉 `r`', '<': '太小 → 扔掉 `l`'}[rel]
        return f'`a[l] + a[r]` = {a[l]} + {a[r]} = =={s}== {rel} {t}，{tail}'
    if 'nums' in S and 'slow' in S:
        return '`[0, slow)` = 已就位的非零数（绿），`fast` 往右找下一个非零数'
    if 'nums' in S:
        return '模板②：同向（快慢）双指针——原地把非零数往前挪'
    return '模板①：相向双指针——有序数组两数之和'


CONFIG = dict(
    num=None, title='双指针 · 通用思想与模板', author='概念讲解', category='双指针',
    technique='通用思想与模板', kind='concept', difficulty='',
    code='''
def two_sum(a, target):            # 相向双指针：a 已排序
    l, r = 0, len(a) - 1
    while l < r:
        s = a[l] + a[r]
        if s == target:
            return [l, r]
        if s > target:             # a[r] 配谁都太大
            r -= 1                 # 扔掉 a[r]
        else:                      # a[l] 配谁都太小
            l += 1                 # 扔掉 a[l]
    return []

def move_zeroes(nums):             # 同向双指针（快慢）
    slow = 0                       # [0, slow) 都是非零数
    for fast in range(len(nums)):  # fast 负责扫描
        if nums[fast]:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
    return nums
''',
    call='''
p = two_sum([1, 2, 4, 6, 8, 9, 14], 12)
q = move_zeroes([0, 1, 0, 3, 12])
(p, q)
''',
    expect=([2, 4], [1, 3, 12, 0, 0]),
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='array', var=lambda S: S['a'] if 'a' in S else S.get('nums'), label='数组',
             pointers={'l': 'blue', 'r': 'pink', 'slow': 'green', 'fast': 'orange'},
             window=(lambda S: S['l'] if 'l' in S else None, lambda S: S['r'] if 'r' in S else None),
             dim=lambda S, i, v: 'l' in S and not (S['l'] <= i <= S['r']),
             color=lambda S, i, v: 'green' if ('slow' in S and i < S['slow']) else None, h=260),
        dict(type='text', fn=lambda S: ('灰色 = 已被排除的数：==每比较一次，候选区间缩小 1==' if 'l' in S else
                                        ('`nums[fast] ≠ 0` → 和 `nums[slow]` 交换，`slow` 右移' if 'slow' in S else '')),
             size=26, h=60),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('s', 's', 'yellow'), ('slow', 'slow', 'green'),
           ('fast', 'fast', 'orange')],
    captions={
        'l, r = 0': '模板① 相向双指针：`l = 0`、`r = {r}` 从两端出发，答案一定在 `[l, r]` 里',
        'while l < r': lambda S, B, ret: (f'`l < r`（{B.l} < {B.r}）→ 区间里还有两个数，继续'
                                          if 'a' in B and B.l < B.r else '`l == r`：区间只剩一个数，结束'),
        's = a[l]': '`s = a[{l}] + a[{r}] = {a[l]} + {a[r]} = {s}`',
        'if s == target': lambda S, B, ret: ('`s == target` → ==找到了==' if S.s == S.target
                                             else f'`{S.s} ≠ {S.target}`，看看该扔掉哪一端'),
        'return [l, r]': '返回 `[{l}, {r}]`：只比较了几次就找到，==O(n)== 而不是 `O(n²)`',
        'if s > target': lambda S, B, ret: (f'`{S.s} > {S.target}`：`a[r]` 和最小的 `a[l]` 相加都太大' if S.s > S.target
                                            else f'`{S.s} < {S.target}`：`a[l]` 和最大的 `a[r]` 相加都太小'),
        'r -= 1': '`a[r]` 配区间里任何数都 > target → ==安全地扔掉==，`r` 左移到 {r}',
        'l += 1': '`a[l]` 配区间里任何数都 < target → ==安全地扔掉==，`l` 右移到 {l}',
        'slow = 0': '模板② 快慢指针：`slow` 指向 ==下一个非零数该放的位置==',
        'for fast': lambda S, B, ret: (f'`fast = {S.fast}`，看 `nums[{S.fast}] = {S.nums[S.fast]}`'
                                       if B.get('fast') != S.fast else 'fast 扫完整个数组，循环结束'),
        'if nums[fast]': lambda S, B, ret: (f'`nums[{S.fast}] = {S.nums[S.fast]}` 非零 → 要搬到 `slow = {S.slow}`'
                                            if S.nums[S.fast] else f'`nums[{S.fast}] = 0` → 跳过，留给后面的非零数覆盖'),
        'nums[slow], nums[fast]': '交换 `nums[{slow}]` 和 `nums[{fast}]`：非零数归位，0 被换到后面',
        'slow += 1': '`slow` → {slow}：`[0, {slow})` 都是非零数，==相对顺序不变==',
        'return nums': '结果 `{nums}`：一趟扫描、`O(1)` 额外空间',
    },
    cards=dict(
        one_liner='利用单调性，每比较一次就安全地排除一个候选',
        complexity='时间 `O(n)`（三数之和 `O(n²)`），空间 `O(1)`',
        problem_heading='什么时候用？',
        problem=['数组 ==有序==（或可以先排序），找满足条件的一对 / 一组数',
                 '能证明「某一端和谁搭配都不可能更优」→ 可以直接扔掉',
                 '原地修改数组：移除 / 移动元素，要求 `O(1)` 额外空间',
                 '暴力是枚举两个下标 `O(n²)`，想优化到 `O(n)`'],
        before=[dict(heading='核心概念：相向 vs 同向', lines=[
            '相向：`l`、`r` 从两端出发，每次比较后 ==扔掉一端==，最多 `n-1` 次',
            '为什么能扔：`a[l] + a[r] > target` 时，`a[r]` 配更小的数也只会更大',
            '同向（快慢）：`fast` 负责扫描，`slow` 指向下一个写入位置',
            '循环不变量：`[0, slow)` 是处理好的部分，`[slow, fast)` 是待覆盖的部分']),
        ],
        idea_heading='两位作者怎么说',
        quote='每次比较，可以认为是==从 i 到 j 中找出两个满足条件的数==，变成了 i + 1 到 j 中，或者 i 到 j - 1 中找出两个满足条件的数。每次比较问题的规模减少 1……',
        quote_src='—— yiduobo · 1. 两数之和',
        idea=['灵神讲「为什么能扔」：11 题较矮的线 ==与另一侧任意线都组不出更大面积==',
              'yiduobo 先推导面积取决于 ==较短的侧边==，42 题直接复用 11 题的双指针',
              '283 题：灵神维护不变量 `[start0, i-1]` 全是 0；yiduobo 维护「第一个零」'],
        summary_heading='本类 Hot100 题目 & 学习顺序',
        summary=['`283` 移动零：快慢指针，非零数换到 `slow`',
                 '`11` 盛最多水的容器：相向，==谁矮移谁==',
                 '`15` 三数之和：排序 + 枚举 `i` + 两数之和 II',
                 '`42` 接雨水：相向 + 前后缀最大值，谁小移动谁',
                 '易错：15 题 `i` 和 `j`/`k` 都要跳过重复值；循环条件是 `l < r`'],
    ),
)
