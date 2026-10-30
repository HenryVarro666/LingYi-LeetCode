def _col(S, i, v):
    if 'num' in S and v == S['num']:
        return 'green'
    return None


def _txt(S):
    if 'cnt' not in S:
        return ''
    return f"当前「最大值的个数」`cnt = {S['cnt']}`　　已做操作 `res = {S['res']}`"


CONFIG = dict(
    num=1887, title='使数组元素相等的减少操作次数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='计数 + 从大到小累加 cnt',
    tags=['灵神题单·滑动窗口与双指针', '难度分 1428'],
    code='''
class Solution(object):
    def reductionOperations(self, nums):

        cnt_dict = {}
        for num in nums:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        res = 0
        cnt = 0
        for num in sorted(cnt_dict.keys(), reverse=True):
            res += cnt
            cnt += cnt_dict[num]
        
        return res
''',
    call='Solution().reductionOperations([5, 1, 3, 3, 1])',
    expect=4,
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='array', var='nums', label='nums（绿 = 和当前 num 相等的元素）', cell=96, color=_col),
        dict(type='map', var='cnt_dict', label='cnt_dict：每个数出现几次', fmt=lambda k, v: f'{k}: {v} 次', h=200),
    ],
    watch=[('num', 'num', 'blue'), ('cnt', 'cnt', 'yellow'), ('res', 'res', 'green')],
    captions={
        'cnt_dict = {}': '先数一遍：每个数出现了几次',
        'for num in nums': lambda S, B, r: ('`nums` 数完了，每个数的次数都记好了' if sum(S.cnt_dict.values()) == len(S.nums)
                                            else f'取 `num = {S.num}`'),
        'cnt_dict[num] =': '`cnt_dict[{num}]` = `{cnt_dict[num]}`',
        'res = 0': '`res` 累计总操作次数',
        'cnt = 0': '`cnt`：比当前数大的数一共有几个（它们都要降到当前数）',
        'for num in sorted': lambda S, B, r: ('不同的数都处理完了' if B.get('num') == S.num and S.num == min(S.cnt_dict)
                                                    else f'从大到小处理 `num = {S.num}`（出现 `{S.cnt_dict[S.num]}` 次）'),
        'res += cnt': '比 `{num}` 大的共 `cnt = {B.cnt}` 个，每个降到 `{num}` 要 ==1 次操作== → `res` += {B.cnt} → {res}',
        'cnt += cnt_dict[num]': '`{num}` 也要被降下去，计入 `cnt`：`cnt` += {cnt_dict[num]} → =={cnt}==',
        'return res': '总操作数 `{res}`',
    },
    cards=dict(
        one_liner='最大值出现 k 次，就要 k 次操作把它们降到次大值',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每次把最大值（多个取最左）减到次大值，直到所有数相等',
                 '求操作次数',
                 '示例：`[5,1,3]` → `3`；`[1,1,2,2,3]` → `4`'],
        quote='某一时刻，若数组中的最大值出现了k次，那么就需要执行k次操作让这些数变成次大值，也就是说每次操作都需要直到当前数组中最大值出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用字典统计每个数出现的次数',
              '从大到小遍历不同的数：`cnt` 是「比当前数大、已经被降下来」的个数',
              '降到当前数需要 `cnt` 次操作，之后当前数也加入 `cnt`'],
        result='`5 → 3`：1 次；`5、3、3 → 1`：3 次；共 `4` 次 ✓',
        summary=['时间 `O(n log n)`（对不同的数排序），空间 `O(n)`',
                 '易错：先 `res += cnt` 再 `cnt += 出现次数`，==顺序不能反==，反了会把自己算进去',
                 '最小的数不需要降，但循环里照样累加，没有影响',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，其余未改',
                 '对比灵神：灵神排序整个数组再分组；yiduobo 先计数、再只排序不同的值'],
    ),
)
