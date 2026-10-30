def _k(S):
    """x 现在对应 nums 里的哪个下标（x 是 nums[k] 反复 //100 得到的）"""
    if 'x' not in S:
        return None
    for k, v in enumerate(S['nums']):
        while True:
            if v == S['x']:
                return k
            if v < 100:
                break
            v //= 100
    return None


def _color(S, i, v):
    k = _k(S)
    if k is None:
        return None
    if i == k:
        return 'blue'
    return None


def _text(S):
    if 'x' not in S:
        return '每次拿走两位数字（除以 100），看最后剩 1 位还是 2 位'
    k = _k(S)
    x = S['x']
    if k is None:
        return '所有数都处理完了'
    orig = S['nums'][k]
    if x >= 100:
        return f'`{orig}` 当前剩 `{x}`，还有 3 位以上 → 继续去掉两位'
    return f'`{orig}` 当前剩 `{x}`：' + ('==两位== → 原长度是偶数' if x >= 10 else '==一位== → 原长度是奇数')


CONFIG = dict(
    num=1295, title='统计位数为偶数的数字', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='每次去掉两位',
    code='''
class Solution:
    def findNumbers(self, nums: List[int]) -> int:
        ans = 0
        for x in nums:
            while x >= 100:
                x //= 100
            if x >= 10:
                ans += 1
        return ans
''',
    call='Solution().findNumbers([12, 345, 2, 6, 7896, 100000])',
    expect=3,
    views=[
        dict(type='text', fn=_text, h=90),
        dict(type='array', var='nums', color=_color, h=260, label='nums', cell=120),
    ],
    watch=['x', ('ans', 'ans', 'green')],
    captions={
        'while x >= 100': '`x = {x}`：' + '{"还有至少 3 位 → 再去掉个位和十位" if x >= 100 else "已不到 3 位，停止去位"}',
        'x //= 100': '`x //= 100`：同时去掉个位和十位 → `{x}`',
        'if x >= 10': '`x = {x}`：{"仍是 2 位 → 原位数为偶数" if x >= 10 else "只剩 1 位 → 原位数为奇数"}',
        'ans += 1': '位数为偶数，计数 +1 → `ans = {ans}`',
        'return ans': '共有 `{ans}` 个数字位数为偶数',
    },
    cards=dict(
        one_liner='不数位数：两位两位地去掉，看最后剩几位',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['给整数数组 `nums`，统计其中==十进制位数为偶数==的数字个数',
                 '示例：`[12,345,2,6,7896]` → `2`（12 和 7896）',
                 '本视频：`[12,345,2,6,7896,100000]` → `3`'],
        quote='好比数苹果，两个两个地拿走苹果，如果最终剩下一个，那么就有奇数个苹果；如果最终剩下两个，那么就有偶数个苹果。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只关心位数的==奇偶==，不需要知道具体位数',
              '每次 `x //= 100`，一次去掉两位，直到 `x < 100`',
              '最后 `x >= 10` 说明剩两位，原长度为偶数'],
        summary=['时间 `O(n log U)`，`U` 是最大值；空间 `O(1)`',
                 '循环条件是 `x >= 100`，不是 `x >= 10`，否则会少去一步',
                 '另一种写法：`len(nums) - sum(len(str(x)) % 2 for x in nums)`，用字符串长度判断奇偶'],
    ),
)
