CONFIG = dict(
    num=768, title='最多能完成排序的块 II', difficulty='Hard', category='单调栈',
    author='yiduobo', technique='最低排位 + 从头扩展右边界',
    tags=['单调栈'],
    code='''
class Solution(object):
    def maxChunksToSorted(self, arr):

        rate_dict = {}
        for index, num in enumerate(sorted(arr)):
            if num not in rate_dict:
                rate_dict[num] = index

        res = 0
        n = len(arr)
        now = 0
        while now < n:
            end_pos = rate_dict[arr[now]]
            max_num = arr[now]
            now += 1
            while now <= end_pos:
                if arr[now] == max_num:
                    end_pos += 1
                elif arr[now] > max_num:
                    max_num = arr[now]
                    end_pos = rate_dict[max_num]
                now += 1
            res += 1
        
        return res
''',
    call='Solution().maxChunksToSorted([2,1,3,4,4,3])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f'当前块至少要盖到下标 ==`{S["end_pos"]}`==，块内最大值 `{S["max_num"]}`' if 'end_pos' in S and 'max_num' in S else '')),
        dict(type='array', var='arr', label='arr（蓝 = now，粉 = end_pos）', pointers={'now': 'blue', 'end_pos': 'pink'}, h=230),
        dict(type='map', var='rate_dict', label='rate_dict：值 → 排序后最靠前的位置（最低排位）', fmt=lambda k, v: f'{k} → {v}', h=250),
    ],
    watch=[('now', 'now', 'blue'), ('end_pos', 'end_pos', 'pink'), ('max_num', 'max_num', 'cyan'), ('res', 'res', 'green')],
    skip=['n = len(arr)'],
    captions={
        'rate_dict = {}': '先排序，记下每个数==排序后最靠前==的位置，叫最低排位',
        'if num not in rate_dict': lambda S, B, ret: (f'`{S.num}` 第一次出现 → 它的最低排位是 `{S.index}`' if S.num not in S.rate_dict
                                                     else f'`{S.num}` 已有排位 `{S.rate_dict[S.num]}`，重复值不覆盖'),
        'rate_dict[num] = index': '`rate_dict[{num}] = {index}`',
        'res = 0': '`res` 统计块数',
        'while now < n': lambda S, B, ret: ('还有元素没分块，开一个新块' if S.now < S.n else '所有元素都分进块了'),
        'end_pos = rate_dict[arr[now]]': '块首 `{arr[now]}` 排序后最早在位置 `{end_pos}` → 这个块至少要覆盖到 `{end_pos}`',
        'max_num = arr[now]': '块内当前最大值 `{max_num}`',
        'while now <= end_pos': lambda S, B, ret: (f'`now = {S.now}` ≤ `end_pos = {S.end_pos}` → 块还没盖够，继续吞入' if S.now <= S.end_pos
                                                  else f'`now = {S.now}` > `end_pos = {S.end_pos}` → 块可以封口'),
        'if arr[now] == max_num': lambda S, B, ret: (f'`arr[{S.now}] = {S.arr[S.now]}` 等于块内最大值 → 多了一个相同的数，右边界要多挪一位' if S.arr[S.now] == S.max_num
                                                    else f'`arr[{S.now}] = {S.arr[S.now]}` 不等于最大值 `{S.max_num}` → 看是不是更大'),
        'end_pos += 1': '`end_pos` 右移到 `{end_pos}`，兼容这个相同的数',
        'elif arr[now] > max_num': lambda S, B, ret: (f'`arr[{S.now}] = {S.arr[S.now]}` > 最大值 `{S.max_num}` → 成立，最大值变了，右边界也要变' if S.arr[S.now] > S.max_num
                                                      else f'`arr[{S.now}] = {S.arr[S.now]}` 没超过最大值 `{S.max_num}` → 右边界不变'),
        'max_num = arr[now]': '最大值更新为 `{max_num}`',
        'end_pos = rate_dict[max_num]': '右边界扩展到 `{max_num}` 的最低排位 `{end_pos}`',
        'now += 1': '`now` → {now}',
        'res += 1': '块封口，块数 `res = {res}`',
        'return res': '最多分成 `{res}` 块',
    },
    cards=dict(
        one_liner='先算每个数的最低排位，再从头扩展块的右边界',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['把数组 `arr`（可含重复值）分成若干块，各块分别排序后拼起来 == 整个数组排序',
                 '求最多能分成几块',
                 '本视频：`[2,1,3,4,4,3]` → `3`（[2,1] [3] [4,4,3]）'],
        quote='这里可能出现重复的元素，因此需要优先进行排序，确定每个数的最低排位。这里的最低排位指的是其在排序完成的数组中所处的最靠前的位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['块首的数排序后在位置 p，这个块至少要盖到 p',
              '块里出现更大的数，右边界延伸到它的最低排位',
              '遇到相同的数，右边界右移一位容纳它'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '`rate_dict` 只记第一次出现的位置，才是最低排位',
                 '遇到和最大值相等的数，==`end_pos += 1`== 不能漏',
                 '原文为 Python 2 风格，代码无需改动即可运行；原文无题面，题意按 LeetCode 768 整理',
                 '与灵神的单调栈思路不同：这是 769 题扩展法的升级版'],
    ),
)
