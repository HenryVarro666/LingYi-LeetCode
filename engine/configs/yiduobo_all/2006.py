CONFIG = dict(
    num=2006, title='差的绝对值为 K 的数对数目', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希计数 · 只配 num + k',
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
    call='Solution().countKDifference([1,2,2,1,3], 1)',
    expect=6,
    views=[
        dict(type='array', var='nums', pointers={}, h=150, label='nums'),
        dict(type='map', var='cnt_dict', label='cnt_dict（数字 → 出现次数）', fmt=lambda k, v: f'{k} → {v}', h=170),
        dict(type='text', fn=lambda S: (f"数 `{S['num']}` 与 `{S['num'] + S['k']}`：`{S['cnt_dict'].get(S['num'], 0)} × {S['cnt_dict'].get(S['num'] + S['k'], 0)}`，累计 res 为 =={S['res']}=="
                                         if S['_line'] >= 9 and 'num' in S and 'res' in S else '先统计出现次数，再配对'), h=60),
    ],
    watch=[('k', 'k', 'blue'), 'num', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计合法数对的数目',
        'cnt_dict = {}': '`cnt_dict` 统计每个数出现的次数',
        'cnt_dict[num] = cnt_dict.get': '`{num}` 出现次数 → `{cnt_dict[num]}`',
        'for num in cnt_dict': '遍历哈希表里的每个不同的数（不是遍历原数组）',
        'res += ': '`{num}` 出现 `{cnt_dict[num]}` 次，`{num + k}` 出现 `{cnt_dict.get(num + k, 0)}` 次：乘积 `{cnt_dict[num] * cnt_dict.get(num + k, 0)}` 对 → `res = {res}`；只看 `num + k`，`num - k` 在遍历到 `num - k` 时已算过，不会重复',
        'return res': '所有乘积累加，答案 `{res}`',
    },
    cards=dict(
        one_liner='先计数，再让每个数只和 num + k 配对',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给整数数组 `nums` 和整数 `k`，数对 `(i, j)` 满足 `i < j` 且 `|nums[i] - nums[j]| == k`',
                 '返回这样的数对数目',
                 '示例：`[1,2,2,1]`，`k = 1` → `4`；本视频用 `[1,2,2,1,3]` → `6`'],
        quote='与其差的绝对值为K的数可能是num - K或者num + K。为了避免重复，此时只需要考虑num与num + K',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历，哈希表 `cnt_dict` 记下每个数出现几次',
              '再遍历哈希表：`num` 出现 a 次，`num + k` 出现 b 次，就能配出 ==a × b== 对',
              '`num - k` 那一边留给 `num - k` 自己算，不重复'],
        summary=['时间 `O(n)`，空间 `O(n)`；数据范围小，双重循环 `O(n^2)` 也能过',
                 '==只配 num + k==，同时配 num - k 会把每对算两遍',
                 '`cnt_dict.get(num + k, 0)`：不存在时按 0 处理',
                 '原文本身就是 Python 3 可运行的写法，未做修改'],
    ),
)
