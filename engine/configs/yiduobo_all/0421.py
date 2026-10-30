def _b(v):
    return format(v, 'b')


CONFIG = dict(
    num=421, title='数组中两个数的最大异或值', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='逐位试填 + 前缀集合',
    tags=['灵神题单·位运算', '灵神题单·常用数据结构', '难度分 2000'],
    code='''
class Solution(object):
    def findMaximumXOR(self, nums):

        max_num = max(nums)
        if max_num == 0:
            return 0

        l = 0
        while max_num:
            l += 1
            max_num >>= 1

        res = 0
        for index in range(l, -1, -1):
            res <<= 1
            now = res | 1
            prefix_set = set()
            for num in nums:
                prefix_set.add(num >> index)
            
            for prefix in prefix_set:
                if now ^ prefix in prefix_set:
                    res = now
                    break

        return res
''',
    call='Solution().findMaximumXOR([3, 10, 5, 25])',
    expect=28,
    views=[
        dict(type='array', var='nums', h=165, label='nums', cell=90),
        dict(type='text', size=34, fn=lambda S: f"`res = {_b(S['res'])}`   `now = {_b(S['now'])}`   （前缀都右移 {S['index']} 位）" if 'now' in S and 'index' in S else (f"`res = {_b(S['res'])}`" if 'res' in S else '')),
        dict(type='text', size=34, fn=lambda S: (f"`now ^ prefix = {_b(S['now'] ^ S['prefix'])}` " + ('==在集合里==' if (S['now'] ^ S['prefix']) in S['prefix_set'] else '不在集合里')) if 'prefix' in S and 'now' in S and 'prefix_set' in S else ''),
        dict(type='set', var='prefix_set', h=190, label='prefix_set（nums 右移 index 位后的前缀，二进制）', fmt=lambda x: _b(x), font=30),
    ],
    watch=[('index', 'index', 'cyan'), ('num', 'num', 'blue'), ('prefix', 'prefix', 'pink'), ('now', 'now', 'yellow'), ('res', 'res', 'green')],
    captions={
        'max_num = max': '最大数 `{max_num}`，二进制位数决定答案最多几位',
        'if max_num == 0': '全是 0 的话答案只能是 0，直接返回',
        'l = 0': '`l` 用来数 `max_num` 的二进制位数',
        'while max_num': lambda S, B, r: (f'`max_num = {S.max_num}` 还没右移空 → 继续数位' if S.max_num else f'`max_num` 移空了，位数 `l = {S.l}`'),
        'l += 1': '又多一位：`l` → {l}',
        'max_num >>= 1': '右移一位：`max_num` → {max_num}',
        'res = 0': '`res` 是答案的高位前缀，从空开始逐位往后补',
        'for index in range': lambda S, B, r: (f'每个数右移 `{S.index}` 位，只留下高位前缀；这一轮判断答案的下一位' if S.index >= 0 and not (S.index == 0 and B.index == 0) else '所有位都处理完了'),
        'res <<= 1': '答案前缀左移一位给新位腾位置：`res = {res:b}`（新位先当 0）',
        'now = res | 1': '假设新位是 1：`now = {now:b}`',
        'prefix_set = set()': '清空集合，重新收集前缀',
        'for num in nums': lambda S, B, r: (f'取 `num = {S.num}`' if not (S.num == S.nums[-1] and B.num == S.num) else '前缀都收集完了'),
        'prefix_set.add': '`{num}` 右移 `{index}` 位 → 前缀 `{num >> index:b}` 放进集合',
        'for prefix in prefix_set': lambda S, B, r: (f'枚举集合里的前缀 `{S.prefix:b}`' if not (B.get('prefix') == S.prefix and list(S.prefix_set)[-1] == S.prefix) else '集合里的前缀都试过了，没有一对满足 → 这一位只能是 0'),
        'if now ^ prefix in prefix_set': lambda S, B, r: (f'`now ^ prefix = {S.now ^ S.prefix:b}` 也在集合里 → 存在两个数，高位异或 = `{S.now:b}`' if (S.now ^ S.prefix) in S.prefix_set else f'`now ^ prefix = {S.now ^ S.prefix:b}` 不在集合里'),
        'res = now': '新位可以是 1：`res = {res:b}`',
        'break': '已经确定，进入下一位',
        'return res': '最大异或值 `{res}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='高位优先：前 m 位异或能否凑成 now？用集合 O(n) 判断',
        complexity='时间 `O(n log U)`，空间 `O(n)`',
        problem=['给整数数组 `nums`，求任意两数异或的最大值',
                 '本视频：`[3,10,5,25]` → `28`（`5 ^ 25`）'],
        quote='对于判断前m位是否能通过异或得到答案，可以通过set在O(n)的时间复杂度内完成。例如对于nums[i]，首先通过右移操作获取到其最高的m位，设为prefix。',
        quote_src='—— yiduobo 题解原文',
        idea=['最大可能答案是全 1，所以从最高位往下，先假设这一位为 1',
              '每个数右移 `index` 位得到前缀，放进 `prefix_set`',
              '若存在 `prefix` 使 `now ^ prefix` 也在集合里，说明这一位能取 1，否则只能是 0'],
        summary=['时间 `O(n log U)`，空间 `O(n)`',
                 '原文没有用 mask，而是==右移取前缀==，答案 `res` 左移累积',
                 '`index` 从 `l` 开始（比位数多一位），第一轮前缀全为 0，只是白走一轮',
                 '和灵神的试填法同一思路：高位优先 + 两数之和'],
    ),
)
