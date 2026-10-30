NUMS, K = [2, 2, 2, 2, 5], 4


def _txt(S):
    if 'cnt_v' not in S:
        return ''
    if S.get('_line', 0) >= 16 and 'num' in S and S.get('v') is not None:
        v = S['v']
        n = S['num']
        return f'全由 `{v}` 组成、长 `{n}` 的子数组：和 `{v}×{n} = {v * n}`，`{v * n} % {K} = {v * n % K}`'
    return f'前缀和模 `{K}` 的余数 `s = {S.get("s")}`；`cnt_v` 记录每个值出现几次'


CONFIG = dict(
    num=3729, title='统计有序数组中可被 K 整除的子数组数量', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='前缀和余数哈希表 + 全相同子数组去重',
    tags=['前缀和与哈希表', '难度分 2248'],
    code='''
class Solution(object):
    def numGoodSubarrays(self, nums, k):

        s = 0
        cnt_v = {}
        cnt_s = {0: 1}
        res = 0

        for v in nums:
            s += v
            s %= k
            res += cnt_s.get(s, 0)
            cnt_s[s] = cnt_s.get(s, 0) + 1
            cnt_v[v] = cnt_v.get(v, 0) + 1

        for v in cnt_v:
            for num in range(1, cnt_v[v]):
                if num * v % k == 0:
                    res -= cnt_v[v] - num

        return res
''',
    call=f'Solution().numGoodSubarrays({NUMS}, {K})',
    expect=2,
    skip=['s = 0', 'cnt_v = {}', 'res = 0', 'cnt_s[s] =', 'for num in range'],
    views=[
        dict(type='array', var='nums', label='nums', cell=96, h=190, pointers={},
             color=lambda S, i, v: 'blue' if S.get('v') == v and S.get('_line', 0) >= 16 else None),
        dict(type='map', var='cnt_s', label='cnt_s（前缀和 % k → 个数）', fmt=lambda k, v: f'{k}: {v}', h=170, font=30),
        dict(type='map', var='cnt_v', label='cnt_v（元素值 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=170, font=30),
        dict(type='text', fn=_txt, size=26, h=70),
    ],
    watch=[('v', 'v', 'blue'), ('s', 's', 'orange'), ('num', 'num', 'pink'), ('res', 'res', 'green')],
    captions={
        'for v in nums': '取下一个数（取完则进入去重）：`v = {v}`',
        's += v': '前缀和 += `{v}` → `{s}`',
        's %= k': '只关心余数：`s % {k}` = `{s}`，和 `{k}` 整除 ⇔ 余数相同',
        'res += cnt_s.get(s, 0)': '余数 `{s}` 之前出现过 `{cnt_s.get(s, 0)}` 次 → 每次对应一个以当前位置结尾、和被 `{k}` 整除的子数组 → `res = {res}`',
        'cnt_v[v] =': '`cnt_v[{v}]` = `{cnt_v[v]}`：记下每个值出现了几次',
        'for v in cnt_v': '去重：取下一个值（取完则结束），当前 `v = {v}`，出现 `{cnt_v[v]}` 次',
        'if num * v % k == 0': lambda S, B, r: (f'全是 `{S.v}`、长度 `{S.num}`：和 `{S.num * S.v}`，`% {S.k} = {S.num * S.v % S.k}` → '
                                                + ('==被整除=='if S.num * S.v % S.k == 0 else '不能整除')),
        'res -= cnt_v[v] - num': '这样的子数组共有 `{cnt_v[v]} − {num} + 1` 个，==只算一次==，要减去 `{cnt_v[v]} − {num}` → `res = {res}`',
        'return res': '去重后一共 `{res}` 个不同的好子数组',
    },
    cards=dict(
        one_liner='先按前缀和余数全数一遍，再减掉“全相同元素”的重复子数组',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['非降序数组 `nums` 和正整数 `k`，和能被 `k` 整除的子数组是好子数组',
                 '数值序列相同的子数组只算一个，求不同好子数组的个数',
                 '本视频：`nums = [2,2,2,2,5]`，`k = 4` → `2`'],
        quote='重复的子数组只可能是由完全相同的元素组成，因为不同元素接壤的部分在nums中都是唯一存在的。',
        quote_src='—— yiduobo 题解原文',
        idea=['先不管去重：前缀和对 `k` 取模，余数相同的前缀就是好子数组，哈希表一趟数完',
              '重复只出现在“全由同一个值 `v`”的子数组：长度 `num`、和 `v×num`',
              '值 `v` 出现 `cnt` 次时，长 `num` 的这类子数组有 `cnt − num + 1` 个，要减去 `cnt − num`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '先全数，再对每个值 `v` 枚举长度 `num` 扣掉重复',
                 '`num` 取 `range(1, cnt)`：长度等于 `cnt` 时只有 1 个，不用扣',
                 '对比灵神：灵神把去重放进遍历里（相同段延迟入表）；yiduobo 是先数后减',
                 '原文本身可直接运行，代码未改'],
    ),
)
