CONFIG = dict(
    num=1983, title='范围和相等的最宽索引对', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='差值前缀和 · 哈希表记首次位置',
    tags=['常用数据结构', '前缀和'],
    code='''
class Solution(object):
    def widestPairOfIndices(self, nums1, nums2):

        res = 0
        first_pos = {0: 0}
        s = 0
        n = len(nums1)
        for index in range(n):
            s += nums1[index] - nums2[index]
            if s in first_pos:
                res = max(res, index - first_pos[s] + 1)
            else:
                first_pos[s] = index + 1
        
        return res
''',
    call='Solution().widestPairOfIndices([1,1,0,1], [0,1,1,0])',
    expect=3,
    views=[
        dict(type='array', var='nums1', label='nums1', pointers={'index': 'blue'}, cell=90, h=210),
        dict(type='array', var='nums2', label='nums2', cell=90, h=150,
             color=lambda S, i, v: 'blue' if S.get('index') == i else None),
        dict(type='map', var='first_pos', label='first_pos：前缀和 → 首次出现的位置（前缀长度）',
             fmt=lambda k, v: f'{k}: {v}', h=130, font=32),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"差值前缀和 `s = {S['s']}`，当前最宽 `res = {S['res']}`" if 's' in S and 'res' in S else '令 d[i] = nums1[i] − nums2[i]，找和为 0 的最长区间')),
    ],
    watch=[('index', 'index', 'blue'), ('s', 's', 'yellow'), ('res', 'res', 'green')],
    captions={
        'first_pos = {0: 0}': '`first_pos[0] = 0`：空前缀的和为 0，位置记为 0',
        's += nums1': '把 `nums1[{index}] − nums2[{index}] = {nums1[index] - nums2[index]}` 并入前缀和，`s` = =={s}==',
        'if s in first_pos': lambda S, B, r: (f'前缀和 `{S.s}` ==以前出现过==（首次位置 {S.first_pos[S.s]}）→ 中间这段 d 的和为 0'
                                             if S.s in S.first_pos else f'前缀和 `{S.s}` 第一次出现 → 先记下位置'),
        'res = max': '区间长度 = `{index} − {first_pos[s]} + 1` = =={index - first_pos[s] + 1}==，`res = max({B.res}, …) = {res}`',
        'first_pos[s] = index + 1': '只记==首次==位置：`first_pos[{s}] = {index + 1}`，越靠左区间越宽',
        'return res': '最宽区间长度 `{res}`',
    },
    cards=dict(
        one_liner='两数组区间和相等 = 差值数组区间和为 0，转前缀和查哈希',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给两个 0/1 数组 `nums1`、`nums2`，找最宽的 `[left, right]`',
                 '要求这一段 `nums1` 的和等于 `nums2` 的和，返回宽度',
                 '示例：`[1,1,0,1]`、`[0,1,1,0]` → `3`'],
        quote='用nums1中每个数减去nums2中下标相同的数得到新数组d，那么问题就转化成了找出d中最长的区间[left，right]，要求区间中数值之和为0。',
        quote_src='—— yiduobo 题解原文',
        idea=['区间和为 0 等价于两个前缀和相等：`d[0..left-1]` 与 `d[0..right]` 的和一样',
              '一趟遍历，哈希表只记每种前缀和==第一次==出现的位置',
              '再次遇到同一个前缀和，就用当前下标减首次位置更新答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`first_pos` 初始化 `{0: 0}`，才能处理从下标 0 开始的区间',
                 '已出现的前缀和不再覆盖：保留最左位置才最宽',
                 '原文已是 Python 3 可运行写法，未作修改'],
    ),
)
