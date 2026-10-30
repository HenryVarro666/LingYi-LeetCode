def _c1(S, i, v):
    L = S['_line']
    if 9 <= L <= 12 and 'j' in S and S.get('i') is not None:
        return 'blue' if i == S['i'] else 'pink' if i == S['j'] else None
    if 21 <= L <= 22 and 'num' in S and v == S['num']:
        return 'yellow'
    return None


def _c2(S, i, v):
    L = S['_line']
    if 17 <= L <= 20 and 'j' in S and S.get('i') is not None:
        return 'blue' if i == S['i'] else 'pink' if i == S['j'] else None
    if 13 <= L <= 14 and 'num' in S and v == S['num']:
        return 'yellow'
    return None


def _done(S, B):
    a = S['nums1'] if S['_line'] == 10 else S['nums2']
    return 'tmp' in B and B['j'] == S['j'] and B['tmp'] == a[B['i']] * a[B['j']]


def _txt(S):
    L = S['_line']
    if L <= 8:
        return '类型 1：`nums1[i]^2 == nums2[j] * nums2[k]`；类型 2 把两个数组对调'
    if L <= 14:
        return '类型 1：先统计 ==nums1== 里所有两数乘积，再拿 nums2 的平方去查'
    return '类型 2：先统计 ==nums2== 里所有两数乘积，再拿 nums1 的平方去查'


CONFIG = dict(
    num=1577, title='数的平方等于两数乘积的方法数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='暴力枚举 + 乘积计数',
    tags=['滑动窗口与双指针'],
    code='''
class Solution(object):
    def numTriplets(self, nums1, nums2):

        m = len(nums1)
        n = len(nums2)
        res = 0

        count_dict = {}
        for i in range(m - 1):
            for j in range(i + 1, m):
                tmp = nums1[i] * nums1[j]
                count_dict[tmp] = count_dict.get(tmp, 0) + 1
        for num in nums2:
            res += count_dict.get(num * num, 0)
        
        count_dict = {}
        for i in range(n - 1):
            for j in range(i + 1, n):
                tmp = nums2[i] * nums2[j]
                count_dict[tmp] = count_dict.get(tmp, 0) + 1
        for num in nums1:
            res += count_dict.get(num * num, 0)
        
        return res
''',
    call='Solution().numTriplets([4,7,3], [2,8,1,9])',
    expect=2,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var='nums1', h=130, label='nums1', color=_c1),
        dict(type='array', var='nums2', h=130, label='nums2', color=_c2),
        dict(type='map', var='count_dict', h=200, fmt=lambda k, v: f'{k} : {v} 次'),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'tmp', ('res', 'res', 'green')],
    captions={
        'm = len': '`m = {m}`，`n` 稍后取',
        'res = 0': '`res` 累计三元组个数',
        'count_dict = {}': '清空哈希表：记录「两数乘积 → 出现次数」',
        'for i in range': lambda S, B, r: ('外层枚举完' if 'i' in B and B['i'] == S.i else f'`i = {S.i}`：固定第一个数'),
        'for j in range': lambda S, B, r: ('内层枚举完' if _done(S, B) else f'`j = {S.j}`：取第二个数，保证 `i < j`'),
        'tmp = nums1[i]': '乘积 `{nums1[i]} × {nums1[j]}` = =={tmp}==',
        'tmp = nums2[i]': '乘积 `{nums2[i]} × {nums2[j]}` = =={tmp}==',
        'count_dict[tmp]': '乘积 `{tmp}` 的次数记为 `{count_dict[tmp]}`',
        'for num in nums2': lambda S, B, r: '`nums2` 遍历完，开始类型 2' if B.get('num') == S.num else f'取 `nums2` 的数 `{S.num}`，平方 = `{S.num*S.num}`',
        'for num in nums1': lambda S, B, r: '`nums1` 遍历完' if B.get('num') == S.num else f'取 `nums1` 的数 `{S.num}`，平方 = `{S.num*S.num}`',
        'res += count_dict.get': '平方 `{num*num}` 在表里出现 `{count_dict.get(num*num, 0)}` 次 → `res` = =={res}==',
        'return res': '一共 =={res}== 个三元组',
    },
    cards=dict(
        one_liner='先统计两数乘积的次数，再用平方去查表',
        complexity='时间 `O(m^2 + n^2)`，空间 `O(m^2 + n^2)`',
        problem=['给两个整数数组 `nums1`、`nums2`，数两类三元组的个数',
                 '类型 1：`nums1[i]^2 == nums2[j] * nums2[k]`（`j < k`）',
                 '类型 2：`nums2[i]^2 == nums1[j] * nums1[k]`（`j < k`）',
                 '本视频：`[4,7,3]`、`[2,8,1,9]` → `2`'],
        quote='注意到题目中nums1和nums2的规模都很小，因此可以直接暴力枚举。',
        quote_src='—— yiduobo 题解原文',
        idea=['类型 1：枚举 `nums2[j]`、`nums2[k]`，把乘积的出现次数记进哈希表',
              '再枚举 `nums1[i]`，用 `nums1[i]` 的平方去表里取次数累加',
              '类型 2 同样做法，把两个数组对调'],
        summary=['时间 `O(m^2 + n^2)`，空间同阶',
                 '易错：每组乘积要 ==先统计、后查询==，且第二轮前要重置 `count_dict`',
                 '`j` 从 `i + 1` 开始，每对只算一次；相同数值不同下标算不同三元组',
                 '难度库里未标注；原文已是 Python 3 可运行写法，代码未改动'],
    ),
)
