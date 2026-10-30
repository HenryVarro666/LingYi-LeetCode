NUMS = [4, 2, 9, 2, 4, 6]

CONFIG = dict(
    num=2404, title='出现最频繁的偶数元素', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='一趟遍历 · 哈希表计数',
    tags=[],
    code='''
class Solution(object):
    def mostFrequentEven(self, nums):

        cnt = {}
        res = -1
        cnt[-1] = 0

        for num in nums:
            if num % 2 == 0:
                cnt[num] = cnt.get(num, 0) + 1
            
                if cnt[num] > cnt[res] or (cnt[num] == cnt[res] and num < res):
                    res = num
        
        return res
''',
    call=f'Solution().mostFrequentEven({NUMS})',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（灰色 = 奇数，不参与）', pointers={'num': 'blue'}, cell=96, h=190,
             color=lambda S, i, v: 'green' if 'res' in S and v == S['res'] and v % 2 == 0 else None,
             dim=lambda S, i, v: v % 2 == 1),
        dict(type='map', var='cnt', label='cnt（偶数 → 次数；-1 是哨兵，次数 0）', fmt=lambda k, v: f'{k}: {v}', h=190, font=32),
        dict(type='text', h=90, size=30,
             fn=lambda S: f"答案 `res = {S['res']}`，次数 `{S['cnt'].get(S['res'])}`" if 'res' in S and 'cnt' in S else ''),
    ],
    watch=[('num', 'num', 'blue'), ('res', 'res', 'green')],
    captions={
        'cnt = {}': '哈希表 `cnt`：记录每种偶数出现的次数',
        'res = -1': '`res` 是当前答案，没有偶数就返回 `-1`',
        'cnt[-1] = 0': '放一个哨兵 `cnt[-1] = 0`：这样第一个偶数比较时 `cnt[res]` 不会报错',
        'for num in nums': lambda S, B, ret: ('遍历结束' if 'num' in B and B.num == S.num and S.num == NUMS[-1] else f'取下一个数 `num = {S.num}`'),
        'if num % 2 == 0': lambda S, B, ret: (f'`{S.num}` 是偶数，要统计' if S.num % 2 == 0 else f'`{S.num}` 是奇数，直接跳过'),
        'cnt[num] = cnt.get': '`cnt[{num}]` 加一 → `{cnt[num]}`',
        'if cnt[num] > cnt[res]': lambda S, B, ret: (
            f'`cnt[{S.num}] = {S.cnt[S.num]}` 大于答案 {S.res} 的次数 `{S.cnt[S.res]}` → ==更新答案=='
            if S.cnt[S.num] > S.cnt[S.res]
            else ('`num` 本身就是答案 `res`，次数涨了但答案不变 → 不更新' if S.num == S.res else None) or (f'次数相同（{S.cnt[S.num]}），且 `{S.num} < {S.res}` → ==选较小的偶数==，更新答案'
                  if S.cnt[S.num] == S.cnt[S.res] and S.num < S.res
                  else (f'次数相同（{S.cnt[S.num]}），但 `{S.num} > {S.res}`，不更小 → 不更新'
                        if S.cnt[S.num] == S.cnt[S.res]
                        else f'`cnt[{S.num}] = {S.cnt[S.num]}` 少于答案的 `{S.cnt[S.res]}` 次 → 不更新'))),
        'res = num': '`res = {res}`',
        'return res': '返回 `{res}`：2 出现 2 次，和 4 并列时取较小的',
    },
    cards=dict(
        one_liner='一趟遍历计数，次数并列时选较小的偶数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['返回 `nums` 中出现次数最多的偶数；并列时返回最小的；没有偶数返回 `-1`',
                 '本视频：`[4,2,9,2,4,6]` → `2`（2 和 4 都出现 2 次）'],
        quote='一趟遍历，使用哈希表记录每种偶数出现的次数，选其中出现次数最多的作为答案即可。需要注意的是，当两种偶数出现次数相同时，需要选择较小的偶数作为答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`cnt` 是偶数到次数的哈希表，奇数不用管',
              '每统计一次，就和当前答案 `res` 比一下次数',
              '用 `cnt[-1] = 0` 当哨兵，第一个偶数自然能顶掉 `-1`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：次数相同要比数值，较小者当答案',
                 '哨兵 `cnt[-1] = 0` 避免了第一次比较时的特判',
                 '对比灵神：灵神用 `Counter`，访问不存在的键直接是 0，不需要哨兵'],
    ),
)
