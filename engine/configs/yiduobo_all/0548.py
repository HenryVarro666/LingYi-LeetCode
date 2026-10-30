def _txt(S):
    if 'v' not in S or 'j' not in S:
        return ''
    s = S['s']
    return (f"第一段 s[i-1]、第二段 v：`s[i-1] = {s[S['i'] - 1]}`  与 `v = {S['v']}`；"
            f"后段：`s[-1] − s[j] = {s[-1] - s[S['j']]}`")


CONFIG = dict(
    num=548, title='将数组分割成和相等的子数组', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='前缀和 + 哈希表合并双重循环',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution(object):
    def splitArray(self, nums):

        n = len(nums)

        s = [nums[0]]
        for num in nums[1:]:
            s.append(s[-1] + num)

        left = {}
        for i in range(1, n - 3):
            for j in range(i + 2, n - 1):
                v = s[j - 1] - s[i]
                if s[i - 1] == v:
                    if j not in left:
                        left[j] = set()
                    left[j].add(v)
                
                if v == s[-1] - s[j] and i in left and v in left[i]:
                    return True

        return False
''',
    call='Solution().splitArray([1,2,1,2,1,2,1])',
    expect=True,
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue', 'j': 'pink'}, label='nums（i、j 是被拿掉的分割点）', h=210),
        dict(type='array', var='s', pointers={}, label='s（前缀和）', h=150),
        dict(type='map', var='left', fmt=lambda k, v: f'以 {k} 结尾，能二分出和 {sorted(v)}', h=140, font=26),
        dict(type='text', size=26, h=80, fn=_txt),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('v', 'v', 'yellow')],
    captions={
        'n = len': '`n = {n}`：要拿掉 3 个分割点，所以 i 从 1 起、j 至少隔一个',
        's = [nums[0]]': '`s` 是前缀和数组，`s[x]` = nums[0..x] 的和',
        's.append': '`s` 追加 `{s[-1]}`',
        'left = {}': '`left[j]`：以 j 为结尾，前两段（含分割点 i）已经相等的和的集合',
        'for i in': '枚举第一个分割点 `i = {i}`',
        'for j in': '枚举第二个分割点 `j = {j}`',
        'v = s[j - 1]': '第二段（i 与 j 之间）的和 `v = s[{j-1}] − s[{i}] = {v}`',
        'if s[i - 1] == v': lambda S, B, r: (f'第一段和 `s[{S.i-1}] = {S.s[S.i-1]}` == `v = {S.v}` → 前两段相等' if S.s[S.i-1] == S.v else f'第一段和 `{S.s[S.i-1]}` ≠ `v = {S.v}` → 前两段不相等'),
        'if j not in left': '`left[{j}]` 还没有 → 先建一个空集合',
        'left[j] = set()': '`left[{j}]` 建好',
        'left[j].add': '记下：以 `{j}` 结尾，已能凑出和 ==`{v}`==',
        'if v == s[-1] - s[j]': lambda S, B, r: (f'后段和 `s[-1] − s[j] = {S.s[-1]-S.s[S.j]}`，与 `v = {S.v}` ' + ('相等；再查 `left[i]` 里有没有 `v`' if S.v == S.s[-1]-S.s[S.j] else '不相等 → 这对 (i, j) 不能当后两个分割点') + ('' if S.v != S.s[-1]-S.s[S.j] else (f'：`left[{S.i}]` 含 {sorted(S.left[S.i])}' if S.i in S.left else f'：`left[{S.i}]` 不存在'))),
        'return True': '`left[i]` 里已有 `v`：前两段和 = 中间两段和 = 后两段和 → 找到合法划分，返回 ==True==',
        'return False': '所有 (i, j) 都没配上对 → `False`',
    },
    cards=dict(
        one_liner='把「前两段」和「后两段」用哈希表配对，三重循环降成二重',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['在数组里取下标 `i < j < k`，把它们拿掉后剩下四段，要求四段和==全相等==',
                 '`i, j, k` 之间、两端都要至少留一个数',
                 '示例：`[1,2,1,2,1,2,1]` → `True`'],
        quote='若当前的s[i - 1] = s[j - 1] - s[i]，说明如果选择i和j来进行前两次的划分，就可以使得划分出来的前两个子数组之和相等。',
        quote_src='—— yiduobo 题解原文',
        idea=['区间和用前缀和 `s` 求：`s[j-1] − s[i]` 是 i、j 之间那段',
              '先用 `left[j]` 存「以 j 结尾能凑出的相等和」，再在后半段查表',
              '`i < j < k` 顺序枚举，两个二重循环合并成一次'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`（哈希表）',
                 '边界：`i ∈ [1, n-4]`，`j ∈ [i+2, n-2]`，每段至少一个数',
                 '后半段检查用的是 `left[i]`：此时 i 扮演「第二个分割点」',
                 '原文为 Python 2 风格，本题代码无需修改即可在 Python 3 运行'],
    ),
)
