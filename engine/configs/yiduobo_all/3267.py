CONFIG = dict(
    num=3267, title='统计近似相等数对 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='大数先行 · 变体都记进 freq',
    tags=['常用枚举技巧', '回溯', '难度分 2545'],
    code='''
class Solution(object):
    def countPairs(self, nums):

        nums.sort(reverse=True)

        freq = {}
        res = 0

        def get_new_v(v_set):
            new_v_set = set()
            for v in v_set:
                digits = list(str(v))
                for i in range(len(digits) - 1):
                    for j in range(len(digits)):
                        if digits[i] == digits[j]:
                            continue
                        digits[i], digits[j] = digits[j], digits[i]
                        new_v = int(''.join(digits))
                        if new_v not in v_set:
                            new_v_set.add(new_v)
                        digits[i], digits[j] = digits[j], digits[i]
            
            return new_v_set

        for v in nums:
            res += freq.get(v, 0)
            one_step = get_new_v(set([v]))
            one_step.add(v)
            two_step = get_new_v(one_step)
            for new_v in one_step:
                freq[new_v] = freq.get(new_v, 0) + 1
            for new_v in two_step:
                freq[new_v] = freq.get(new_v, 0) + 1
        
        return res
''',
    call='Solution().countPairs([12, 102])',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（从大到小；蓝 = 当前 v）', cell=100, h=140,
             color=lambda S, i, v: 'blue' if S.get('_inner') is not None and v == S.get('v') and S.get('freq') is not None else None),
        dict(type='set', var='one_step', label='one_step = v 交换 0 或 1 次', h=130, fmt=lambda x: str(x), font=30),
        dict(type='set', var='two_step', label='two_step = 再多换一次得到的新数', h=130, fmt=lambda x: str(x), font=30),
        dict(type='map', var='freq', label='freq = 已处理的数能变成的各个数 → 个数', h=170, fmt=lambda k, v: f'{k}: {v}', font=30),
    ],
    watch=[('v', 'v', 'blue'), ('res', 'res', 'green'), ('new_v', 'new_v', 'yellow')],
    skip=['one_step.add(v)', 'if digits[i] == digits[j]', 'continue', 'new_v_set.add', 'new_v_set = set()', 'digits = list', 'for i in range', 'for j in range', 'for v in v_set', 'for v in nums',
          'for new_v in one_step', 'for new_v in two_step', 'digits[i], digits[j] = digits[j], digits[i]'],
    max_steps=95,
    captions={
        'nums.sort(reverse=True)': '==从大到小==排序：位数多的先处理，它们的变体先进 `freq`，后面位数少的才能查到',
        'freq = {}': '`freq[x]`：前面处理过的数里，有多少个能（交换至多两次）变成 `x`',
        'if digits[i] == digits[j]': lambda S, B, r: (f'`digits[{S.i}] = digits[{S.j}] = {S.digits[S.i]}`：换了也一样 → 跳过'
                                                     if S.digits[S.i] == S.digits[S.j] else f'`{S.digits[S.i]} ≠ {S.digits[S.j]}`：交换会产生新数'),
        'new_v = int': '交换 `digits[{i}]` 与 `digits[{j}]` → `new_v = {new_v}`，再换回来',
        'if new_v not in v_set': lambda S, B, r: f'`{S.new_v}` 不在原集合里 → 是新数，加入' if S.new_v not in S.v_set else f'`{S.new_v}` 已在原集合里 → 不重复收集',
        'new_v_set.add': '`new_v_set` 加入 `{new_v}`',
        'return new_v_set': '这一轮交换一次能得到的新数：`{sorted(new_v_set)}`',
        'res += freq.get(v, 0)': '`freq` 里已经记着前面各数的变体，查 `v = {v}` 命中 `{freq.get(v, 0)}` 个 → `res` = =={res}==',
        'one_step = get_new_v': '`one_step`：`{v}` 交换一次能得到的数',
        'one_step.add(v)': '再把「不交换」的 `{v}` 自己放进 `one_step`',
        'two_step = get_new_v': '对 `one_step` 里每个数再交换一次 → `two_step`（交换两次的新数）',
        'freq[new_v] = freq.get(new_v, 0) + 1': lambda S, B, r: f'`{S.v}` 能变成 `{S.new_v}` → `freq[{S.new_v}]` = {S.freq[S.new_v]}',
        'return res': '近似相等的数对一共 `{res}` 个',
    },
    cards=dict(
        one_liner='把每个数的所有变体登记进 freq，后来的数直接查自己',
        complexity='时间 `O(n·d^4)`，空间 `O(n·d^4)`（`d` 为位数）',
        problem=['正整数数组 `nums`，一个数可交换两个数位，==至多两次==',
                 '`nums[i]` 与 `nums[j]`（`i < j`）能变成相等则算一对（可有前导 0）',
                 '求这样的数对个数。本视频：`[12,102]` → `1`'],
        quote='最好的处理方法应该是在上一题的基础上，检测当前元素x在操作后的所有新元素，而不是只是x自身，与freq中新元素的匹配情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['不是拿 `v` 的变体去查，而是把 `v` 的变体都登记到 `freq`',
              '先处理大数：`102` 能变成 `12`，所以 `102` 的变体里有 `12`',
              '后来的 `12` 直接查 `freq[12]`，就知道前面有几个数能变成它',
              '换数位时跳过相同数字，并用集合去掉重复结果'],
        summary=['时间约 `O(n·d^4)`，原文说加上「相同数位不交换」的优化就能通过',
                 '必须 `reverse=True`：保证位数多的先进 `freq`，前导 0 才能被匹配',
                 '`one_step` 含 `v` 自己，`two_step` 只收新数，同一个数不会被登记两次',
                 '对比灵神：灵神用公式 O(1) 算交换结果，并枚举「右边」去查左边计数'],
    ),
)
