CONFIG = dict(
    num=4013, title='按奇偶比统计子数组 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='通分 + 前缀和 + 归并排序数非逆序对',
    tags=['树状数组', '难度分 2156'],
    code='''
class Solution(object):
    def countRatioSubarrays(self, nums, a, b):
        
        s = [0]
        for v in nums:
            if v % 2 == 0:
                s.append(s[-1] - b)
            else:
                s.append(s[-1] + a)
        
        def calc(left, right, s):
            if left == right:
                return 0
            
            mid = (left + right) // 2
            tot = calc(left, mid, s) + calc(mid + 1, right, s)
            tmp = []
            
            i, j = left, mid + 1
            while i <= mid and j <= right:
                if s[i] <= s[j]:
                    tot += right - j + 1
                    tmp.append(s[i])
                    i += 1
                else:
                    tmp.append(s[j])
                    j += 1
            
            tmp.extend(s[i: mid + 1])
            tmp.extend(s[j: right + 1])

            for index in range(left, right + 1):
                s[index] = tmp[index - left]
            return tot

        return calc(0, len(s) - 1, s)
''',
    call='Solution().countRatioSubarrays([1,2,1], 3, 2)',
    expect=5,
    views=[
        dict(type='text', fn=lambda S: (f"区间 `[{S['left']}, {S['right']}]`，mid = {S['mid']}：左半 `[{S['left']}, {S['mid']}]` 与右半 `[{S['mid']+1}, {S['right']}]` 都已有序；数 s[i] <= s[j] 的跨半数对" if 'mid' in S and 'left' in S else '【前缀和 s：数 L<R 且 s[L] <= s[R] 的下标对（非逆序对）】'), h=60),
        dict(type='array', var='nums', label='nums（奇数 → +a，偶数 → -b）', h=110),
        dict(type='array', var='s', label='前缀和 s（框 = 当前归并区间）', pointers={'i': 'blue', 'j': 'pink'}, window=('left', 'right'), h=190),
        dict(type='array', var='tmp', label='tmp：归并后的有序结果', h=130),
        dict(type='calls', h=170, hide=('s',)),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'tot'],
    captions={
        's = [0]': '前缀和从 `s[0] = 0` 开始',
        'if v % 2 == 0': '`v = {v}`：偶数 → 贡献 `-b`，奇数 → 贡献 `+a`',
        's.append(s[-1] - b)': '偶数：`s` 末尾加 `s[-1] - b` = {s[-1]}',
        's.append(s[-1] + a)': '奇数：`s` 末尾加 `s[-1] + a` = {s[-1]}',
        'if left == right': lambda S, B, r: ('只剩一个前缀和，没有数对 → 返回 0' if S.left == S.right else f'区间 `[{S.left}, {S.right}]` 继续二分'),
        'mid = (left': '`mid = {mid}`：数对分三类，左半内、右半内、跨 mid',
        'tot = calc': '先递归：两半内部的数对数好，并且各自排好序',
        'while i <= mid': '两半都还有数，继续归并',
        'if s[i] <= s[j]': lambda S, B, r: (f'`s[{S.i}] = {S.s[S.i]} <= s[{S.j}] = {S.s[S.j]}` → 左边这个数和右半 j 及之后的所有数都成对' if S.s[S.i] <= S.s[S.j] else f'`s[{S.i}] = {S.s[S.i]} > s[{S.j}] = {S.s[S.j]}` → 右边更小，它不能和 i 配对，先放进 tmp'),
        'tot += right - j + 1': '右半从 j 到 right 都 `>= s[i]`（右半有序）→ 加 `right - j + 1 = {right - j + 1}`，`tot` = =={tot}==',
        'tmp.append(s[i])': '`s[i]` 进 tmp',
        'i += 1': '`i` → {i}',
        'tmp.append(s[j])': '`s[j]` 进 tmp',
        'j += 1': '`j` → {j}',
        'tmp.extend(s[i': '一半取完了：左半剩下的（已有序）直接接到 tmp 后面',
        'tmp.extend(s[j': '右半剩下的（已有序）也接到 tmp 后面，tmp = {tmp}',
        'return tot': 'tmp 已写回 s（区间有序），本层数对共 `{tot}` 个，返回上一层',
        'return calc(0': '从整个前缀和数组 `[0, {len(s) - 1}]` 开始：先递归，再数跨半数对，再合并',
    },
    skip=['tmp = []', 'i, j = left', 'for index in range', 's[index] = tmp', 'return 0', 'for v in nums'],
    max_steps=130,
    cards=dict(
        one_liner='通分成 bx <= ay，换成前缀和，非逆序对用归并排序数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['数组 `nums`，正整数 `a`、`b`',
                 '子数组偶数 x 个、奇数 y 个；`y > 0` 且 `x / y <= a / b` 为有效',
                 '示例：`[1,2,1,2]`，`a=3, b=2` → `7`；本视频用 `[1,2,1]` → `5`'],
        quote='将其通分后可得bx <= ay时数组有效。……将nums中的所有偶数都替换为-b，所有奇数都替换为a，……子数组和大于等于0的子数组就是要找有效子数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['滑窗不行：固定一端，`x / y` 随另一端移动没有单调性',
              '通分后偶数换成 `-b`、奇数换成 `a`，有效 = 子数组和 >= 0，再用前缀和 `s`',
              '右端 R 要数 `s[0..R-1]` 里 <= `s[R]` 的个数，这就是非逆序对，归并排序顺手数'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`y = 0` 时 `ay - bx < 0` 必不成立，所以不用单独判断 `y > 0`',
                 '归并时 `s[i] <= s[j]` 就加 `right - j + 1`，相等也算（题目是 <=）',
                 '原文已使用 `//` 整数除法，是 Python 3 可运行写法，未做修改',
                 '对比灵神：灵神主推离散化树状数组，yiduobo 用归并排序'],
    ),
)
