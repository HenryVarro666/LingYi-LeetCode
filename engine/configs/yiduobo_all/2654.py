CONFIG = dict(
    num=2654, title='使数组所有元素变成 1 的最少操作次数', difficulty='Medium', category='位运算',
    author='yiduobo', technique='1 向两侧传播 + 枚举 GCD 为 1 的最短子数组',
    tags=['GCD', '难度分 1929'],
    code='''
class Solution(object):
    def minOperations(self, nums):

        def gcd(x, y):
            while y > 0:
                x, y = y, x % y
            return x

        cnt = 0
        for v in nums:
            if v == 1:
                cnt += 1
        
        if cnt > 0:
            return len(nums) - cnt

        g = nums[0]
        for v in nums[1:]:
            g = gcd(g, v)
        
        if g > 1:
            return -1
        
        mi = len(nums)
        for left in range(len(nums) - 1):
            g = nums[left]
            for right in range(left + 1, len(nums)):
                g = gcd(g, nums[right])
                if g == 1:
                    mi = min(mi, right - left + 1)
                    break
        
        return len(nums) + mi - 2
''',
    call='Solution().minOperations([2,6,3,4])',
    expect=4,
    skip=['x, y = y, x % y', 'return x', 'while y > 0'],
    views=[
        dict(type='array', var='nums', pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), h=230,
             color=lambda S, i, v: 'green' if v == 1 else None),
        dict(type='text', fn=lambda S: (
            f"子数组 `[{S['left']}..{S['right']}]` 的 GCD = ==`{S['g']}`==，目前最短长度 `mi = {S['mi']}`"
            if 'right' in S and 'mi' in S and S.get('_line', 0) >= 33 and S['right'] > S['left'] else
            (f"每个 1 都能感染邻居：`cnt = {S['cnt']}`" if 'cnt' in S and 'mi' not in S else ''))),
    ],
    watch=[('cnt', 'cnt', 'cyan'), ('g', 'g', 'orange'), ('left', 'left', 'blue'), ('right', 'right', 'pink'),
           ('mi', 'mi', 'green')],
    captions={
        'cnt = 0': '`cnt` 数一数数组里已经有几个 1',
        'if v == 1': lambda S, B, r: f'`{S.v}` ' + ('是 1，`cnt` 加一' if S.v == 1 else '不是 1'),
        'cnt += 1': '`cnt = {cnt}`',
        'if cnt > 0': lambda S, B, r: ('`cnt = %d` > 0：有 1 就能把它不断传给相邻的数 → ==答案 `n − cnt`==' % S.cnt if S.cnt > 0
                                       else '`cnt = 0`：没有 1，得先造出一个 1'),
        'return len(nums) - cnt': '`{len(nums)} − {cnt}` = =={ret}==',
        'g = nums[0]': '`g` 先取第一个数，准备求整个数组的 GCD',
        'for v in nums[1:]': '依次并入 `v = {v}`',
        'g = gcd(g, v)': '`gcd({B.g}, {v})` = `{gcd(B.g, v)}`',
        'if g > 1': lambda S, B, r: (f'整体 GCD = `{S.g}` > 1 → ==每次操作都只会得到它的倍数==，永远得不到 1，返回 -1' if S.g > 1
                                     else f'整体 GCD = `{S.g}`，一定有解，继续'),
        'return -1': '无解',
        'mi = len(nums)': '`mi`：GCD 为 1 的最短子数组长度，先设成 `n`',
        'for left in range': '枚举子数组左端点 `left = {left}`',
        'g = nums[left]': '`g` 从 `nums[{left}] = {g}` 开始',
        'for right in range': '右端点 `right = {right}`，向右并入',
        'g = gcd(g, nums[right])': '`gcd({B.g}, {nums[right]})` = ==`{gcd(B.g, nums[right])}`==，即子数组 `[{left}..{right}]` 的 GCD',
        'if g == 1': lambda S, B, r: (f'`g = {S.g}` ==等于 1== → 找到 GCD 为 1 的子数组，长度 `{S.right - S.left + 1}`' if S.g == 1
                                      else f'`g = {S.g}` > 1，继续往右'),
        'mi = min': '`mi = min({B.mi}, {right} − {left} + 1)` = =={mi}==',
        'break': '再往右只会更长，换下一个左端点',
        'return len(nums) + mi - 2': '`n + mi − 2` = `{len(nums)} + {mi} − 2` = =={ret}==：造 1 花 `mi − 1` 次，传播花 `n − 1` 次',
    },
    cards=dict(
        one_liner='1 能感染整个数组；没有 1 就先造一个',
        complexity='时间 `O(n^2 log U)`，空间 `O(1)`',
        problem=['每次选相邻两数，把其中一个换成它们的最大公约数，问最少几次能让==全部变成 1==，不行返回 -1',
                 '示例：`[2,6,3,4]` → `4`'],
        quote='1和任意大于1的数的最大公约数都为1，因此只要数组中存在1，那么这个1就可以不断感染相邻的数……不妨设这个子数组的长度为k，那么想得到1就需要k - 1次操作，而将1传播到整个数组则需要n - 1次操作，因此最终答案就是n + k - 2。',
        quote_src='—— yiduobo 题解原文',
        idea=['有 1：每个非 1 的数各花一次，答案 `n − cnt`',
              '没有 1：整体 GCD > 1 就无解；否则必有某个子数组 GCD 为 1',
              '枚举左右端点，找 GCD 为 1 的==最短==子数组（长度 `mi`），答案 `n + mi − 2`'],
        summary=['时间 `O(n^2 log U)`，`n ≤ 50` 够用',
                 '三步顺序：先数 1 → 再判整体 GCD → 最后枚举子数组',
                 '易错：`mi` 存的是长度，所以是 `n + mi − 2`（造 1 花 `mi−1`、传播花 `n−1`）',
                 '对比灵神：灵神把 `+1` 提进 return，存 `j − i`；yiduobo 直接存长度'],
    ),
)
