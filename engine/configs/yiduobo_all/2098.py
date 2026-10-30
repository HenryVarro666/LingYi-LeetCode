CONFIG = dict(
    num=2098, title='长度为K的最大偶数和子序列', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='奇偶分组 + 前缀和枚举', tags=['贪心', '排序'],
    code='''
class Solution(object):
    def largestEvenSum(self, nums, k):

        odd = []
        even = []
        for v in nums:
            if v % 2 == 0:
                even.append(v)
            else:
                odd.append(v)
        
        odd.sort(reverse=True)
        even.sort(reverse=True)

        odd_s = [0]
        for v in odd:
            odd_s.append(odd_s[-1] + v)
        
        even_s = [0]
        for v in even:
            even_s.append(even_s[-1] + v)
        
        res = -1
        for odd_cnt in range(0, min(len(odd), k) + 1, 2):
            if odd_cnt + len(even) < k:
                continue
            
            res = max(res, odd_s[odd_cnt] + even_s[k - odd_cnt])
        
        return res
''',
    call='Solution().largestEvenSum([4,1,5,3,1,8,6], 4)',
    expect=22,
    views=[
        dict(type='array', var='odd', label='odd（奇数，降序）', h=130, cell=70),
        dict(type='array', var='even', label='even（偶数，降序）', h=130, cell=70),
        dict(type='array', var='odd_s', label='odd_s（奇数前缀和）', h=130, cell=70, pointers={'odd_cnt': 'blue'}),
        dict(type='array', var='even_s', label='even_s（偶数前缀和）', h=130, cell=70, pointers={'k - odd_cnt': 'pink'}),
    ],
    watch=['odd_cnt', ('even_cnt', 'k - odd_cnt', 'pink'), ('res', 'res', 'green')],
    captions={
        'if v % 2 == 0': lambda S, B, r: (f'`{S.v}` 是偶数 → 放进 even' if S.v % 2 == 0 else f'`{S.v}` 是奇数 → 放进 odd'),
        'odd.sort': '奇数从大到小：`{odd}`，取最大的若干个就是取前缀',
        'even.sort': '偶数从大到小：`{even}`',
        'odd_s = [0]': '`odd_s[i]` = 最大的 i 个奇数之和，先放 0',
        'odd_s.append': '`odd_s` 加入前缀和 `{odd_s[-1]}`',
        'even_s = [0]': '`even_s[i]` = 最大的 i 个偶数之和',
        'even_s.append': '`even_s` 加入前缀和 `{even_s[-1]}`',
        'res = -1': '`res = -1`：凑不出偶数和就返回 -1',
        'for odd_cnt': lambda S, B, r: ('奇数个数都枚举完了' if 'odd_cnt' in B and B.odd_cnt == S.odd_cnt and S.odd_cnt == 4 else f'枚举奇数个数 `odd_cnt = {S.odd_cnt}`：和为偶数，奇数个数必须是==偶数==；偶数要取 `k - odd_cnt = {S.k - S.odd_cnt}` 个'),
        'if odd_cnt + len(even) < k': lambda S, B, r: (f'偶数只有 {len(S.even)} 个，凑不够 `k - odd_cnt = {S.k - S.odd_cnt}` 个 → 这种方案不可行' if S.odd_cnt + len(S.even) < S.k else f'偶数 {len(S.even)} 个够用，方案可行'),
        'continue': '跳过这个 `odd_cnt`',
        'res = max': '`odd_s[{odd_cnt}] + even_s[{k - odd_cnt}] = {odd_s[odd_cnt]} + {even_s[k - odd_cnt]}` = {odd_s[odd_cnt] + even_s[k - odd_cnt]} → `res = {res}`',
        'return res': '最大偶数和 `{res}`',
    },
    cards=dict(
        one_liner='偶数和 = 偶数个奇数 + 若干偶数，各取最大的',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['整数数组 `nums` 和整数 `k`，选长度为 `k` 的子序列，要求元素和为==偶数==',
                 '返回最大的偶数和；不存在返回 `-1`',
                 '本视频：`nums=[4,1,5,3,1,8,6]`，`k=4` → `22`'],
        quote='子序列的和为偶数，那么其中必然包含偶数个奇数，而剩下则由偶数来填充。……枚举最终选择奇数的数量odd_cnt，这里的odd_cnt必须为偶数，那么剩下偶数的数量even_cnt就必然是k - odd_cnt。',
        quote_src='—— yiduobo 题解原文',
        idea=['奇数个数必须为偶数，其余用偶数补满 `k` 个',
              '数量固定后，选最大的奇数 + 最大的偶数最优',
              '分别降序排序，用前缀和 `O(1)` 查询前 `i` 个之和'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`odd_cnt` 步长为 2，上界是 `min(len(odd), k)`',
                 '偶数不够 `k - odd_cnt` 个要 `continue`，否则 `even_s` 下标越界',
                 '一个方案都不可行时保持 `res = -1`'],
    ),
)
