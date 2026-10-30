CONFIG = dict(
    num=1979, title='找出数组的最大公约数', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='两两一组找最值',
    tags=['灵神题单', '数学算法', '难度分 1184'],
    code='''
class Solution:
    def findGCD(self, nums: List[int]) -> int:
        n = len(nums)
        if n % 2:
            mn = mx = nums[0]
        elif nums[0] < nums[1]:
            mn, mx = nums[0], nums[1]
        else:
            mn, mx = nums[1], nums[0]

        for i in range(2 - n % 2, n, 2):
            x, y = nums[i], nums[i + 1]
            if x > y:
                x, y = y, x
            if x < mn:
                mn = x
            if y > mx:
                mx = y

        return gcd(mn, mx)
''',
    call='Solution().findGCD([4,9,6,2,8,10])',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: (f"当前最小 `mn = {S['mn']}`，最大 `mx = {S['mx']}`" if 'mx' in S else '先确定 mn、mx 的初始值'), size=34),
        dict(type='array', var='nums', pointers={'i': 'blue', 'i + 1': 'pink'}, h=300,
             color=lambda S, i, v: ('green' if 'mn' in S and v in (S['mn'], S['mx']) and i < S.get('i', 99) + (2 if 'x' in S else 0) else None)),
    ],
    watch=['n', ('mn', 'mn', 'cyan'), ('mx', 'mx', 'orange'), 'x', 'y'],
    captions={
        'if n % 2': '`n = {n}`：奇数就用 `nums[0]` 当初值，偶数就先比前两个',
        'mn, mx = nums[0], nums[1]': '前两个先比一次：`nums[0] < nums[1]` → `mn = {mn}`，`mx = {mx}`',
        'mn, mx = nums[1], nums[0]': '前两个先比一次：`nums[0] >= nums[1]` → `mn = {mn}`，`mx = {mx}`',
        'for i in range': lambda S, B, r: ('剩下的数都处理完了，循环结束' if 'i' in B and B.i == S.i else f'剩下的数两两一组：这一组是 `nums[{S.i}]` 和 `nums[{S.i+1}]`'),
        'x, y = nums[i]': '取这一组 `x = {x}`，`y = {y}`',
        'x, y = y, x': '`x > y`，先在组内交换：现在 `x = {x}` 是小的，`y = {y}` 是大的',
        'if x > y': '组内先比一次：`{x} > {y}` → {"成立，要交换" if x > y else "不成立，已经有序"}',
        'if x < mn': '小的那个只可能刷新最小值：`{x} < {mn}` → {"成立" if x < mn else "不成立"}',
        'mn = x': '`mn` 更新为 `{mn}`',
        'if y > mx': '大的那个只可能刷新最大值：`{y} > {mx}` → {"成立" if y > mx else "不成立"}',
        'mx = y': '`mx` 更新为 `{mx}`',
        'return gcd': '`mn = {mn}`，`mx = {mx}`，==最小数和最大数的 GCD== = `{ret}`',
    },
    cards=dict(
        one_liner='先找最小、最大，再求 GCD；两两一组找最值，比较次数少 25%',
        complexity='时间 `O(n + log U)`，空间 `O(1)`',
        problem=['给整数数组 `nums`，求==最小数==和==最大数==的最大公约数',
                 '示例：`[2,5,6,9,10]` → 最小 2，最大 10 → `2`',
                 '本视频：`[4,9,6,2,8,10]` → `2`'],
        quote='把数组中的元素两两一组，每一组内的两个元素先比一次大小，再把二者的最小值和当前最小值比大小，把二者的最大值和当前最大值比大小。',
        quote_src='—— 灵茶山艾府题解',
        idea=['朴素做法找最大最小要 `2(n-1)` 次比较',
              '一组两个数先比一次：小的只跟 `mn` 比，大的只跟 `mx` 比',
              '每组 3 次比较，总数约 `3(n-1)/2`'],
        summary=['时间 `O(n + log U)`，空间 `O(1)`，`gcd` 本身是 `O(log U)`',
                 '奇数长度用 `nums[0]` 起步，偶数长度先比前两个，循环起点是 `2 - n % 2`',
                 '最简写法是 `gcd(min(nums), max(nums))`，这里演示的是少比较的写法',
                 '比较次数 `floor(3(n-1)/2)`，对字符串等比较昂贵的类型更有意义'],
    ),
)
