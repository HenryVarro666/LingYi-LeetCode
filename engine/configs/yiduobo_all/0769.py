CONFIG = dict(
    num=769, title='最多能完成排序的块', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='扩展区间到最大值',
    code='''
class Solution(object):
    def maxChunksToSorted(self, arr):

        res = 0
        n = len(arr)
        now = 0
        while now < n:
            end_pos = arr[now]
            max_num = 0
            while True:
                max_num = 0
                for index in range(now, end_pos + 1):
                    max_num = max(max_num, arr[index])
                if max_num == end_pos:
                    res += 1
                    now = end_pos + 1
                    break
                else:
                    end_pos = max_num
        
        return res
''',
    call='Solution().maxChunksToSorted([1,0,2,4,3,5])',
    expect=4,
    views=[
        dict(type='text', fn=lambda S: (f"当前块：下标 `{S['now']}` ~ `{S['end_pos']}`，块内最大值 ==" + str(S.get('max_num', 0)) + "==") if 'end_pos' in S and S['now'] <= S['end_pos'] else ''),
        dict(type='array', var='arr', pointers={'now': 'blue', 'end_pos': 'pink'}, window=('now', 'end_pos'), h=300,
             dim=lambda S, i, v: 'now' in S and i < S['now'],
             color=lambda S, i, v: ('green' if i < S['now'] else None) if 'now' in S else None),
    ],
    watch=[('now', 'now', 'blue'), ('end_pos', 'end_pos', 'pink'), 'max_num', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计能分成的块数',
        'now = 0': '从下标 `0` 开始切第一块',
        'end_pos = arr[now]': '`arr[{now}] = {arr[now]}` 最终要排到下标 `{arr[now]}` → 这一块至少要盖住 `{now}` ~ `{end_pos}`',
        'for index': '扫描块内下标 `{index}`：`max_num = max({B.max_num}, {arr[index]}) = {max_num}`',
        'if max_num == end_pos': lambda S, B, r: (f'块内最大值 `{S.max_num}` == 右端 `{S.end_pos}`：块里恰好是这段下标对应的数 → ==合法=='
                                                  if S.max_num == S.end_pos else f'块内最大值 `{S.max_num}` != 右端 `{S.end_pos}`：说明有数要排到块外，不合法'),
        'res += 1': '切出一块：`res` → {res}',
        'now = end_pos + 1': '下一块从 `{now}` 开始',
        'end_pos = max_num': '有数 `{max_num}` 超出范围 → 块必须==扩展==到下标 `{end_pos}`，再检查一遍',
        'return res': '一共 `{res}` 块',
    },
    cards=dict(
        one_liner='从左往右切块，数值超出范围就把块扩展到它',
        complexity='时间 `O(n^2)`（扩展时重扫），空间 `O(1)`',
        problem=['`arr` 是 `[0, n-1]` 的一个排列，把它分成若干块，每块单独排序后拼起来要等于整体排序结果',
                 '求最多能分成几块',
                 '本视频：`[1,0,2,4,3,5]` → `4`'],
        quote='对于arr[0]，其在数组中的最终位置应该就是arr[0]，那么我们至少要将0到arr[0]这一段划在一起，才能保证arr[0]能顺利归位。',
        quote_src='—— yiduobo 题解原文',
        idea=['块从 `now` 出发，右端先取 `arr[now]`：这个数必须能归位',
              '块内若有更大的数 `x`，它也要归位 → 右端扩展到 `x`，重复检查',
              '最大值恰好等于右端时，块内恰好是这段下标的数，切一刀，从下一位继续'],
        summary=['时间 `O(n^2)`，空间 `O(1)`',
                 '原理：块内最大值等于右端，说明块内正好是 `now` ~ `end_pos` 的排列',
                 '内层 `while True` 每次扩展右端至少加一，必然终止',
                 '原文为 Python 2 风格，只是类的写法 `class Solution(object)`，代码无需改动',
                 '升级版 768 题允许重复元素，需要换思路'],
    ),
)
