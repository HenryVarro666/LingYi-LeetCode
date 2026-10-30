CONFIG = dict(
    num=1636, title='按照频率将数组升序排序', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希计数 + 双关键字排序',
    tags=[],
    code='''
class Solution(object):
    def frequencySort(self, nums):

        cnt_dict = {}
        for num in nums:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        res = []
        for num, cnt in sorted(cnt_dict.items(), key=lambda d:(d[1], -d[0])):
            res.extend([num] * cnt)
        
        return res
''',
    call='Solution().frequencySort([1,1,2,2,2,3,4,4])',
    expect=[3, 4, 4, 1, 1, 2, 2, 2],
    views=[
        dict(type='array', var='nums', h=170, cell=80, label='nums', pointers={}),
        dict(type='map', var='cnt_dict', h=170, fmt=lambda k, v: f'{k}: {v}次', label='cnt_dict'),
        dict(type='array', var='res', h=170, cell=80, label='res'),
    ],
    watch=['num', 'cnt'],
    captions={
        'cnt_dict = {}': '先建哈希表，统计每个数出现几次',
        'cnt_dict[num] =': '`{num}` 出现次数 +1 → `{cnt_dict[num]}`',
        'res = []': '`res` 用来按顺序存放最终结果',
        'for num, cnt in sorted': lambda S, B, r: f"按 (频率, −数值) 升序取出：`{S.num}` 出现 `{S.cnt}` 次",
        'res.extend': '把 `{num}` 重复 `{cnt}` 次接到 `res` 后面：`{res}`',
        'return res': '频率低的在前；频率相同则数值大的在前：`{res}`',
    },
    cards=dict(
        one_liner='先数频率，再按（频率升序，数值降序）排',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['把 `nums` 按每个数出现的==频率升序==排列；频率相同的，==数值大的排前面==',
                 '示例：`[1,1,2,2,2,3,4,4]`',
                 '结果 `[3,4,4,1,1,2,2,2]`（频率 1 → 3；频率 2 → 4,4,1,1；频率 3 → 2,2,2）'],
        quote='按频率为第一关键字，数值大小的相反数为第二关键字从小到大进行排序。',
        quote_src='—— yiduobo 题解原文',
        idea=['哈希表记下每个数的频率',
              '排序键 `(频率, −数值)`：取负让相同频率时数值从大到小',
              '按排序后的顺序，每个数重复 `cnt` 次加入答案'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错点：同频率时是数值==降序==，所以第二关键字取 `-d[0]`',
                 '原文为 Python 2 风格，代码未改动（`items()` 在 Python 3 同样可用）'],
    ),
)
