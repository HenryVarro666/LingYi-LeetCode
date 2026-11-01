CONFIG = dict(
    num=2006, title='差的绝对值为 K 的数对数目', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表计数 · 只看 num 与 num+K',
    code='''
class Solution(object):
    def countKDifference(self, nums, k):

        res = 0
        cnt_dict = {}
        for num in nums:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        for num in cnt_dict:
            res += cnt_dict[num] * cnt_dict.get(num + k, 0)
        
        return res
''',
    call='Solution().countKDifference([3,1,3,5,1], 2)',
    expect=6,
    views=[
        dict(type='array', var='nums', h=190, cell=100, label='nums',
             color=lambda S, i, v: 'blue' if S.get('_line') == 10 and 'num' in S and v == S['num'] else None),
        dict(type='map', var='cnt_dict', h=220, label='cnt_dict：数 → 出现次数'),
        dict(type='text', size=28, h=100, fn=lambda S: (f"`{S['num']}` 出现 `{S['cnt_dict'][S['num']]}` 次，`{S['num'] + S['k']}` 出现 `{S['cnt_dict'].get(S['num'] + S['k'], 0)}` 次 → 乘积 ==`{S['cnt_dict'][S['num']] * S['cnt_dict'].get(S['num'] + S['k'], 0)}`==" if S.get('_line') == 10 and 'num' in S else '')),
    ],
    watch=[('k', 'k', 'blue'), ('num', 'num', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计合法数对数',
        'cnt_dict = {}': '`cnt_dict` 统计每个数出现的次数',
        'cnt_dict[num] = ': '数 `{num}` 出现次数 → `{cnt_dict[num]}`',
        'res += ': '只配 `num` 和 `num + k`（`num - k` 在遍历到它时已算过，避免重复）：`{cnt_dict[num]} × {cnt_dict.get(num + k, 0)}` → `res` = =={res}==',
        'return res': '全部数都配对完，答案 `{res}`',
    },
    cards=dict(
        one_liner='次数相乘：num 出现 a 次、num+K 出现 b 次，就有 a×b 对',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数对 `(i, j)` 满足 `i < j` 且 `|nums[i] - nums[j]| == k`，求个数',
                 '本视频：`[3,1,3,5,1], k=2` → `6`'],
        quote='与其差的绝对值为K的数可能是num - K或者num + K。为了避免重复，此时只需要考虑num与num + K，因为num与num - K的情况在遍历到num - K时就考虑过了。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用哈希表 `cnt_dict` 一趟统计每个数出现的次数',
              '再遍历哈希表里的每个不同的数 `num`，只考虑它和 `num + k`',
              '两边分别出现 `a`、`b` 次，就能组成 `a × b` 个数对，累加'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：只取 `num + k` 一个方向，否则每对会被数两遍',
                 '遍历的是哈希表（不同的数），不是原数组，所以要乘出现次数',
                 '对比灵神：灵神遍历原数组、取 `v - k`；yiduobo 遍历哈希表、取 `num + k` 再乘次数',
                 '原文无需改动，直接可在 Python 3 运行'],
    ),
)
