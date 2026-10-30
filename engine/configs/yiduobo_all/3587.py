CONFIG = dict(
    num=3587, title='最小相邻交换至奇偶交替', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='奇偶下标分组 · 按原顺序分配到 0,2,4…',
    tags=['灵神题单', '难度分 1548'],
    code='''
class Solution(object):
    def minSwaps(self, nums):
        
        odd = []
        even = []
        for index, v in enumerate(nums):
            if v % 2 == 0:
                even.append(index)
            else:
                odd.append(index)
        
        if abs(len(even) - len(odd)) >= 2:
            return -1
        
        if len(even) == len(odd):
            case_even = 0
            case_odd = 0
            for index in range(len(nums) // 2):
                even_index = index * 2
                odd_index = index * 2 + 1
                case_even += abs(even_index - even[index])
                case_odd += abs(even_index - odd[index])
            
            return min(case_even, case_odd)
        
        target_even, target_odd = even, odd
        if len(target_even) < len(target_odd):
            target_even, target_odd = target_odd, target_even
        res = 0
        for index in range(len(nums) // 2 + 1):
            res += abs(target_even[index] - index * 2)
        
        return res
''',
    call='Solution().minSwaps([2,4,6,5,7])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 奇数，灰 = 偶数）', h=190,
             color=lambda S, i, v: 'blue' if v % 2 else None),
        dict(type='array', var='even', label='even：偶数的原始下标', h=160, color=lambda S, i, v: 'green'),
        dict(type='array', var='odd', label='odd：奇数的原始下标', h=160, color=lambda S, i, v: 'blue'),
        dict(type='text', size=26, h=80, fn=lambda S: (
            f"第 {S['index']} 个：目标下标 `{S['index']*2}`，原下标 `{S['target_even'][S['index']]}`，距离 =={abs(S['target_even'][S['index']]-S['index']*2)}=="
            if 'target_even' in S and 'index' in S and S['index'] < len(S['target_even']) and S.get('res', None) is not None else '')),
    ],
    watch=['index', 'res', ('len(even)', 'len(even)', 'green'), ('len(odd)', 'len(odd)', 'blue')],
    captions={
        'odd = []': '`odd` 记录奇数的原始下标',
        'even = []': '`even` 记录偶数的原始下标',
        'if v % 2 == 0': '`nums[{index}] = {v}`：{"偶数，下标进 even" if v % 2 == 0 else "奇数，下标进 odd"}',
        'even.append': '`even` = {even}',
        'odd.append': '`odd` = {odd}',
        'abs(len(even) - len(odd)) >= 2': '`|{len(even)} - {len(odd)}| = {abs(len(even) - len(odd))}`：'
                                          '{"个数差 ≥ 2，奇偶不可能交替 → -1" if abs(len(even) - len(odd)) >= 2 else "差 ≤ 1，有解"}',
        'len(even) == len(odd)': '`{len(even)}` 和 `{len(odd)}` {"相等：奇偶谁排在下标 0 都行，两种都算" if len(even) == len(odd) else "不等：个数多的那组必须占 0、2、4…"}',
        'target_even, target_odd = even, odd': '先假设 even 是多的一组',
        'if len(target_even) < len(target_odd)': '`{len(target_even)} < {len(target_odd)}`：{"odd 更多，交换角色" if len(target_even) < len(target_odd) else "even 更多，不用换"}',
        'target_even, target_odd = target_odd, target_even': '较长的数组记为 `target_even`：它的下标要去 ==0、2、4…==',
        'res = 0': '`res` 累计所有元素的移动距离',
        'res += abs': '按原顺序分配（相对顺序不变，交换同奇偶元素不划算）：`|{target_even[index]} − {index*2}| = {abs(target_even[index]-index*2)}` → `res = {res}`',
        'return res': '总代价 `res` = =={res}==',
    },
    cards=dict(
        one_liner='先按奇偶分组，再把同组下标按原顺序分配到 0,2,4…',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次交换相邻两个数，使相邻元素奇偶交替，求最少交换次数；不可能则 `-1`',
                 '示例：`[2,4,6,5,7]` → `3`'],
        quote='对于target_even中的一组下标对p和q，若最终将p移动到x，q移动到y，那么在这里必然有x < y……但是实际上，本题中只关注元素的奇偶性，而target_even中的所有元素奇偶性相同，因此交换p和q显然是不优的。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历一趟，用 `even` 和 `odd` 分别记下偶数和奇数的==原始下标==',
              '个数差 ≥ 2 无解；差为 1 时，多的那组必须占 0、2、4…',
              '个数相等时两种都算，取较小；代价 = 原下标与目标下标之差的绝对值之和'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：个数差为 1 时只有一种分配，别两种都算',
                 '同组下标保持原来的先后顺序再分配',
                 '对比灵神：灵神只记奇数（车）的下标，用 `(n-start+1)//2` 判断可行；yiduobo 两组都记，按个数差分三种情况'],
    ),
)
