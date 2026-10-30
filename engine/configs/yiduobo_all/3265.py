CONFIG = dict(
    num=3265, title='统计近似相等数对 I', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='从大到小遍历 + 哈希表记录可达状态',
    code='''
class Solution(object):
    def countPairs(self, nums):

        nums.sort(reverse=True)

        res = 0
        freq = {}

        for v in nums:
            res += freq.get(v, 0)
            digits = list(str(v))
            new_v_set = set([v])
            for i in range(len(digits) - 1):
                for j in range(i + 1, len(digits)):
                    digits[i], digits[j] = digits[j], digits[i]
                    new_v_set.add(int(''.join(digits)))
                    digits[i], digits[j] = digits[j], digits[i]
            
            for new_v in new_v_set:
                freq[new_v] = freq.get(new_v, 0) + 1
        
        return res
''',
    call='Solution().countPairs([3,12,30,17,21])',
    expect=2,
    views=[
        dict(type='array', var='nums', h=170, label='nums（从大到小，黄 = 当前 v）', color=lambda S, i, v: 'yellow' if 'v' in S and v == S['v'] else None,
             dim=lambda S, i, v: 'v' in S and v > S['v']),
        dict(type='set', var='new_v_set', h=170, label='new_v_set = v 本身 + 交换一次的结果'),
        dict(type='map', var='freq', h=220, label='freq：左边的数操作后能变成 key 的个数'),
    ],
    watch=[('v', 'v', 'yellow'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    captions={
        'nums.sort(reverse=True)': '==从大到小排序==：位数多的先处理，只让位数多的去匹配位数少的（前导 0）',
        'freq = {}': '`freq[t]` = 已遍历的数经过一次操作后能变成 `t` 的个数',
        'res += freq.get': '`freq[{v}]` = {freq.get(v, 0)}：左边有这么多数能变成 `{v}` → `res` = =={res}==',
        'digits = list': '把 `{v}` 拆成数位 `{digits}`',
        'new_v_set = set': '`new_v_set` 先放入不操作的 `{v}`',
        "new_v_set.add": '交换第 `{i}`、`{j}` 位得到 `{int("".join(digits))}`，加入集合',
        'for new_v in': '`{new_v}` 是 {v} 能变成的数',
        'freq[new_v] =': '`freq[{new_v}]` → {freq[new_v]}',
    },
    cards=dict(
        one_liner='从大到小遍历，用哈希表记录左边的数能变成什么',
        complexity='时间 `O(n log n + n·d²)`，空间 `O(n·d²)`（d 为位数）',
        problem=['交换一个数中两个数位至多一次，若能与另一个数相等就是近似相等，允许前导 0',
                 '求下标 `i<j` 的近似相等数对数目',
                 '示例：`[3,12,30,17,21]` → `2`'],
        quote='只要按照元素从大到小的顺序遍历nums执行上面的算法，就一定不会出现x左侧元素操作后无法匹配x，但是x操作后可以匹配左侧元素的情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['经典数对写法：一趟遍历，哈希表 `freq` 记录左边元素能变成的所有状态',
              '没有前导 0 时，x 变 y 等价于 y 变 x；有前导 0 时只有位数长的那个能变',
              '所以从大到小排序，保证“左边操作后变成 x”覆盖所有情况'],
        summary=['时间 `O(n log n + n·d²)`，d ≤ 7',
                 '易错：必须 `reverse=True`，顺序错了会漏掉前导 0 的数对',
                 '集合去重：同一个数多种交换得到同一结果只记一次',
                 '对比灵神：灵神从小到大并用公式算交换结果；yiduobo 从大到小，直接交换字符再还原'],
    ),
)
