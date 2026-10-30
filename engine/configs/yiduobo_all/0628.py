def _cand(S):
    if 'max1' not in S:
        return '最终答案里正负数的个数分五种情况，归结为两种选法'
    v = [S[k] for k in ('max1', 'max2', 'max3', 'min1', 'min2')]
    if None in v:
        return '还没扫够：`None` 表示这个位置还空着'
    a, b, c, m1, m2 = v
    return f'选最大三个 `{a}×{b}×{c}` = =={a*b*c}==　选一大两小 `{a}×{m1}×{m2}` = =={a*m1*m2}=='


def _c(old, num, op, name):
    if old is None:
        return f'这个位置还是空的（`None`）→ num = {num} 直接填进去，成为{name}'
    ok = num > old if op == '>' else num < old
    return f'`{num} {op} {old}` → ' + (f'成立，num 是新的{name}' if ok else '不成立，继续往下比')


CONFIG = dict(
    num=628, title='三个数的最大乘积', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='分情况讨论 · 一趟扫描选 5 个数',
    tags=['贪心与思维', '乘积贪心'],
    code='''
class Solution(object):
    def maximumProduct(self, nums):

        max1 = max2 = max3 = min1 = min2 = None
        for num in nums:
            if max1 is None or max1 < num:
                max1, max2, max3 = num, max1, max2
            elif max2 is None or max2 < num:
                max2, max3 = num, max2
            elif max3 is None or max3 < num:
                max3 = num

            if min1 is None or min1 > num:
                min1, min2 = num, min1
            elif min2 is None or min2 > num:
                min2 = num

        return max(max1 * max2 * max3, max1 * min1 * min2)
''',
    call='Solution().maximumProduct([4, -7, 1, -6, 2, 3])',
    expect=168,
    views=[
        dict(type='text', fn=_cand, h=90),
        dict(type='array', var='nums', h=260, label='nums（绿 = 最大三个，粉 = 最小两个）',
             color=lambda S, i, v: ('green' if v in (S.get('max1'), S.get('max2'), S.get('max3')) else
                                    'pink' if v in (S.get('min1'), S.get('min2')) else None)),
    ],
    watch=[('num', 'num', 'yellow'), ('max1', 'max1', 'green'), ('max2', 'max2', 'green'),
           ('max3', 'max3', 'green'), ('min1', 'min1', 'pink'), ('min2', 'min2', 'pink')],
    captions={
        'max1 = max2 = max3 = min1': '五个位置先都空着（`None`），扫描时再填',
        'for num in nums': '看下一个数 `num = {num}`',
        'if max1 is None or max1 < num': lambda S, B, r: _c(B.max1, S.num, '>', '最大，原来的依次后移'),
        'elif max2 is None': lambda S, B, r: _c(B.max2, S.num, '>', '第二大'),
        'elif max3 is None': lambda S, B, r: _c(B.max3, S.num, '>', '第三大'),
        'if min1 is None or min1 > num': lambda S, B, r: _c(B.min1, S.num, '<', '最小，原来的变次小'),
        'elif min2 is None or min2 > num': lambda S, B, r: _c(B.min2, S.num, '<', '第二小'),
        'max1, max2, max3 = num': '`max1, max2, max3` = `{max1}, {max2}, {max3}`：新数插到最前，旧的整体后移',
        'max2, max3 = num': '`max2, max3` = `{max2}, {max3}`',
        'max3 = num': '`max3 = {max3}`',
        'min1, min2 = num': '`min1, min2` = `{min1}, {min2}`',
        'return max': lambda S, B, ret: f'比较两种选法：`{S.max1}×{S.max2}×{S.max3}` = {S.max1*S.max2*S.max3}，`{S.max1}×{S.min1}×{S.min2}` = {S.max1*S.min1*S.min2} → =={ret}==',
    },
    cards=dict(
        one_liner='讨论答案里有几个负数，结论只剩两种选法',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给整数数组 `nums`（可能有负数），选三个数使乘积最大',
                 '示例：`[1,2,3,4]` → `24`；`[-1,-2,-3]` → `-6`',
                 '本视频：`[4,-7,1,-6,2,3]` → `168`'],
        quote='综合上面几种情况，可以发现最终答案必然是从选择3个最大的数，或者选择1个最大的数和两个最小的数之间产生，于是可以一趟扫描，选出这5个数。',
        quote_src='—— yiduobo 题解原文',
        idea=['不讨论候选集，转而讨论==最终答案==里正、负、零的个数',
              '3 正、含 0、2 正 1 负、3 负：都等价于选最大的 3 个数',
              '1 正 2 负：要负数绝对值大，选最小两个 + 最大一个'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '用 `None` 表示还没填；比较前要先判 `is None`',
                 '`max1, max2, max3 = num, max1, max2` 右边先整体求值，再赋值，旧值不会丢',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
