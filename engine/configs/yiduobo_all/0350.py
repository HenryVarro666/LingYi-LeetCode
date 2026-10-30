CONFIG = dict(
    num=350, title='两个数组的交集 II', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='两个字典计数 · 取较小次数',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution(object):
    def intersect(self, nums1, nums2):

        num_dict1 = {}
        for num in nums1:
            num_dict1[num] = num_dict1.get(num, 0) + 1

        num_dict2 = {}
        for num in nums2:
            num_dict2[num] = num_dict2.get(num, 0) + 1
        
        res = []
        for num, weight in num_dict1.items():
            if num in num_dict2:
                res.extend([num] * min(weight, num_dict2[num]))

        return res
''',
    call='Solution().intersect([1,2,2,1,3], [2,2,2,1,4])',
    expect=[1, 2, 2],
    views=[
        dict(type='map', var='num_dict1', h=190),
        dict(type='map', var='num_dict2', h=190),
        dict(type='array', var='res', label='res', h=170),
    ],
    watch=[('num', 'num', 'yellow'), ('weight', 'weight', 'cyan')],
    max_steps=80,
    captions={
        'num_dict1 = {}': '`num_dict1` 统计 `nums1` 中每个数出现几次',
        'for num in nums1': '逐个取 `nums1` 的数来计数',
        'num_dict1[num] =': '`num` = {num}：`num_dict1[{num}]` 变成 =={num_dict1[num]}==',
        'num_dict2 = {}': '`num_dict2` 统计 `nums2` 中每个数出现几次',
        'for num in nums2': '逐个取 `nums2` 的数来计数',
        'num_dict2[num] =': '`num` = {num}：`num_dict2[{num}]` 变成 =={num_dict2[num]}==',
        'res = []': '两个字典都统计好了，开始求交集',
        'for num, weight in': '看 `nums1` 里的数 `{num}`，它出现了 `{weight}` 次',
        'if num in num_dict2': lambda S, B, r: (f'`{S.num}` 也在 `num_dict2` 中（出现 {S.num_dict2[S.num]} 次）→ 是交集元素' if S.num in S.num_dict2 else f'`{S.num}` 不在 `num_dict2` 中 → 跳过'),
        'res.extend': '交集里 `{num}` 出现次数取较小值 `min({weight}, {num_dict2[num]})` = =={min(weight, num_dict2[num])}==，`res = {res}`',
        'return res': '交集是 `{ret}`（顺序不限）',
    },
    cards=dict(
        one_liner='350 要统计次数，用 dict 存次数，再取较小值',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['返回两个数组的交集，每个元素出现次数取两边较小值，顺序不限',
                 '示例：`[4,9,5]` 和 `[9,4,9,8,4]` → `[4,9]`',
                 '本视频：`[1,2,2,1,3]` 和 `[2,2,2,1,4]` → `[1,2,2]`'],
        quote='349不需要考虑出现的次数，因此使用set统计一下即可。350则需要使用dict来进行统计。',
        quote_src='—— yiduobo 题解原文',
        idea=['两个数组各用一个 dict 统计每个数的出现次数',
              '遍历 `num_dict1`，若也在 `num_dict2` 中，把它重复 `min(次数1, 次数2)` 次放进 `res`',
              '结果按 `nums1` 的首次出现顺序排，题目不要求顺序'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '易错：次数要取 `min`，不是直接取某一边',
                 '原文为 Python 2 风格，本题代码无需改动（`items()` 在 Python 3 同样可用）',
                 '数组已排序时，原文提到可用类似二路归并的做法，空间更小',
                 '对比灵神：灵神只建一个哈希表，边扫 `nums2` 边把次数减一'],
    ),
)
