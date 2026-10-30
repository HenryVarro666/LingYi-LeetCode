CONFIG = dict(
    num=3046, title='分割数组', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='频次统计 + 构造性证明',
    tags=[],
    code='''
class Solution(object):
    def isPossibleToSplit(self, nums):

        freq = Counter(nums)
        return max(freq.values()) <= 2
''',
    call='''Solution().isPossibleToSplit([1,1,2,2,3,4])
Solution().isPossibleToSplit([1,1,1,1])''',
    expect=False,
    views=[
        dict(type='text', fn=lambda S: ('出现次数的最大值 `' + str(max(S['freq'].values())) + '`，不超过 2 就能分' if 'freq' in S else '先统计每个数出现几次'), size=28),
        dict(type='array', var='nums', label='nums（黄 = 出现 3 次以上的数）', cell=96,
             color=lambda S, k, v: 'yellow' if (S.get('nums') and S['nums'].count(v) > 2) else None),
        dict(type='map', var='freq', label='freq：数字 → 出现次数', h=260),
    ],
    watch=[('freq', 'freq')],
    captions={
        'freq = Counter': '一趟遍历统计每个数出现的次数：`{dict(freq)}`',
        'return max': lambda S, B, ret: (f"最大频次 `{max(S.freq.values())}` ≤ 2：出现两次的数分给 nums1 和 nums2 各一个，出现一次的补给较短的那个 → ==可以分割=="
                                         if ret else f"最大频次 `{max(S.freq.values())}` ≥ 3：必有两个相同的数进同一个数组 → ==不能分割=="),
    },
    cards=dict(
        one_liner='某个数出现 3 次以上必然失败，否则总能构造出分割',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把偶数长度的 `nums` 平分成 `nums1`、`nums2`',
                 '两个数组内部元素都要互不相同',
                 '示例：`[1,1,2,2,3,4]` → `true`'],
        quote='如果数组中存在某个数v出现了大于等于三次，那么无论怎么分割，必然有至少两个v被分到同一个数组中，不符合题目要求，必然不能分割。',
        quote_src='—— yiduobo 题解',
        idea=['必要性：某个数 ≥ 3 次，抽屉原理，两个数组放不下',
              '充分性：出现 2 次的数一边一个；出现 1 次的数交给当前较短的数组',
              '所以只需统计频次，看最大值是否 ≤ 2'],
        result='`[1,1,2,2,3,4]` 最大频次 2 → True；`[1,1,1,1]` 频次 4 → False ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：次数等于 2 是可以的，只有 ≥ 3 才失败',
                 '这题的关键是构造性证明，代码只剩一行判断'],
    ),
)
