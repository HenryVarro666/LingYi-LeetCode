def _cand(S):
    if 'min_d' not in S:
        return ''
    num = S['num']
    md = S['min_d']
    cur = '∞' if md == float('inf') else md
    return f'`num = {num}`，到最近同奇偶回文数的距离 `min_d` = =={cur}=='


def _nums_view(S):
    return S.get('nums')


CONFIG = dict(
    num=4053, title='使每个元素变为回文数的最少操作次数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='只看最多 5 个候选回文数',
    tags=[],
    code='''
class Solution:
    def nearestPalindromicDiff(self, num: int) -> int:
        if num <= 9:
            return 0  # num 已经是回文数

        min_d = inf

        def update(pal: int) -> None:
            nonlocal min_d
            min_d = min(min_d, abs(pal - num))

        s = str(num)
        m = len(s)

        if num % 2:
            update(10 ** (m - 1) - 1)  # 十进制长为 m-1 的最大奇回文数 999..999
            update(10 ** m + 1)  # 十进制长为 m+1 的最小奇回文数 100..001
        else:
            if m == 2:
                update(8)
            else:
                update(10 ** (m - 2) * 9 - 2)  # 十进制长为 m-1 的最大偶回文数 899..998
            update(10 ** m * 2 + 2)  # 十进制长为 m+1 的最小偶回文数 200..002

        high_digit = int(s[0])
        if high_digit % 2 == num % 2:
            left = int(s[:(m + 1) // 2])
            # 枚举十进制长为 m 的邻近回文数
            for l in range(left - 1, left + 2):
                # l 最高位的奇偶性必须与 num 的相同
                sl = str(l)
                if int(sl[0]) % 2 == num % 2:
                    update(int(sl + sl[::-1][m % 2:]))
        else:
            # 最高位为 high_digit - 1
            # 例如 num = 354..676，生成回文数 299..992
            if high_digit > 1:
                update((10 ** (m - 1) + 1) * high_digit - 11)

            # 最高位为 high_digit + 1
            # 例如 num = 354..676，生成回文数 400..004
            if high_digit < 9:
                update((10 ** (m - 1) + 1) * (high_digit + 1))

        return min_d

    def minOperations(self, nums: list[int]) -> int:
        return sum(self.nearestPalindromicDiff(x) for x in nums) // 2
''',
    call='Solution().minOperations([10, 125])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums', cell=120, h=220,
             color=lambda S, i, v: 'blue' if v == S.get('num') else None,
             dim=lambda S, i, v: False),
        dict(type='text', fn=_cand, size=34, h=140),
    ],
    watch=[('num', 'num', 'blue'), ('min_d', 'min_d', 'green'), ('m', 'm', 'cyan')],
    skip=['sl = str(l)', 'm = len(s)', 'high_digit = int'],
    captions={
        'if num <= 9': '`{num} <= 9`？{"是，一位数本身就是回文数，距离 0" if num <= 9 else "不是，要去找最近的回文数"}',
        'min_d = inf': '`min_d` 记录「到候选回文数的最小距离」，先设为无穷大',
        'min_d = min(min_d, abs(pal - num))': '候选回文数 `{pal}`，离 `{num}` 距离 `{abs(pal - num)}` → `min_d = {min_d}`',
        'if num % 2': '`{num}` 是{"奇" if num % 2 else "偶"}数 → 回文数也必须是{"奇" if num % 2 else "偶"}数，先加长度 m±1 的两个边界候选',
        'if high_digit % 2 == num % 2': '最高位 `{high_digit}` 与 `num` 奇偶{"相同" if high_digit % 2 == num % 2 else "不同"} → {"可以直接用前半段生成同长度回文数" if high_digit % 2 == num % 2 else "前半段不能用，只能改最高位"}',
        'left = int': '前半段 `left = {left}`，枚举 `left-1, left, left+1` 生成同长度回文数',
        'for l in range': '前半段 `left-1 ~ left+1` 逐个试，当前 `l = {l}`',
        'if int(sl[0])': '`{l}` 的最高位奇偶须与 `num` 相同 → {"可用" if int(sl[0]) % 2 == num % 2 else "跳过"}',
        'if high_digit > 1': '最高位减 1 的回文数（如 `299..992`）：`high_digit = {high_digit}` {"可以减" if high_digit > 1 else "已经是 1，不能减"}',
        'if high_digit < 9': '最高位加 1 的回文数（如 `400..004`）：`high_digit = {high_digit}` {"可以加" if high_digit < 9 else "已经是 9，不能加"}',
        'return min_d': '最近的同奇偶回文数距离 =={ret}==',
        'return sum(': '各数距离之和 `{ret * 2}`，每次操作走 2，所以答案 `{ret * 2} // 2` = =={ret}==',
    },
    max_steps=110,
    cards=dict(
        one_liner='操作不改变奇偶性 → 找同奇偶的最近回文数',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['一次操作：`nums[i]` 加 2 或减 2，要把每个数都变成正回文数',
                 '不同元素可以变成不同回文数，求最少总操作次数',
                 '示例：`[125]` → 125 减 2 两次变成 121，答案 `2`'],
        quote='操作不改变 nums[i] 的奇偶性。问题相当于：找到与 nums[i] 同奇偶的最近的回文数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['加减 2 不改奇偶 → 目标回文数必须和 `num` ==同奇偶==',
              '最近回文数只可能是：长度 m-1 的最大、长度 m+1 的最小，以及前半段 ±1 生成的几个',
              '每个数只试至多 5 个候选，取最小距离；距离除以 2 就是操作次数'],
        summary=['时间 `O(n log U)`，不用预处理回文数表，空间 `O(1)`',
                 '易错：回文数的==最高位奇偶==也要和 `num` 相同，偶数的最大回文是 `8`、`899..98` 这类',
                 '`num <= 9` 本身就是回文，直接 0',
                 '题解方法一：预处理 2e9 内全部回文数 + 二分，代码更短，但预处理太大，不适合在视频里逐行演示',
                 '最后 `// 2`：距离一定是偶数，每步走 2'],
    ),
)
