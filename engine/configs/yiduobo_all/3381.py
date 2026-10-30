NUMS = [-5, 1, 2, -3, 4]
K = 2


def _ix(S):
    return S['index'] - 1 if 'index' in S else None


def _text(S):
    if 'p' not in S:
        return '用哈希表 `s_dict` 记录==每种下标余数==对应的最小前缀和'
    return f'当前前缀和 `s` = =={S["s"]}==，下标 `{S["index"]}` 的余数 `p = {S["p"]}`'


def _cap_if(S, B, ret):
    if S.p not in S.s_dict:
        return f'余数 `{S.p}` 还没出现过：没有同余的前缀可减，先记下 `s_dict[{S.p}] = {S.s}`'
    return f'余数 `{S.p}` 已经有记录 `{S.s_dict[S.p]}`：同余前缀相减，长度正好是 `k` 的倍数'


def _cap_res(S, B, ret):
    d = S.s - B.s_dict[S.p]
    old = B.res
    if old is None or old < d:
        return f'`s − s_dict[{S.p}] = {S.s} − ({B.s_dict[S.p]}) = {d}`' + ('，第一个候选 → `res` 记下' if old is None else f' > `res = {old}` → 更新 `res` = =={d}==')
    return f'`s − s_dict[{S.p}] = {d}` 不超过 `res = {old}`，不更新'


CONFIG = dict(
    num=3381, title='长度可被 K 整除的子数组的最大元素和', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和 + 余数哈希表',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1943'],
    code='''
class Solution(object):
    def maxSubarraySum(self, nums, k):
        
        s_dict = {0: 0}
        res = None
        s = 0
        for index, v in enumerate(nums, 1):
            s += v
            p = index % k
            if p not in s_dict:
                s_dict[p] = s
            else:
                if res is None or res < s - s_dict[p]:
                    res = s - s_dict[p]
                s_dict[p] = min(s_dict[p], s)
        
        return res
''',
    call=f'Solution().maxSubarraySum({NUMS}, {K})',
    expect=4,
    views=[
        dict(type='text', fn=_text, size=24, h=70),
        dict(type='array', var='nums', label='nums（蓝 = 当前数，下标从 1 计数）', cell=96, h=200,
             pointers={_ix: 'blue'}, pointer_labels={_ix: 'v'},
             color=lambda S, i, v: 'blue' if _ix(S) == i else None),
        dict(type='map', var='s_dict', label='s_dict：余数 → 最小前缀和', fmt=lambda k, v: f'{k} → {v}', h=230),
    ],
    watch=[('index', 'index', 'blue'), ('s', 's', 'pink'), ('p', 'p', 'yellow'), ('res', 'res', 'green')],
    captions={
        's_dict = {0: 0}': '`s_dict[0] = 0`：空前缀（和为 0，下标 0）先放进去',
        's = 0': '`s` 是当前前缀和，初始为 0',
        'res = None': '`res = None`：还没有合法子数组',
        's += v': '前缀和 `s += {v}` → =={s}==',
        'p = index % k': '`p = {index} % {k} = {p}`：余数相同的前缀相减，长度是 `k` 的倍数',
        'if p not in s_dict': _cap_if,
        's_dict[p] = s': '第一次见余数 `{p}`：`s_dict[{p}] = {s}`',
        'if res is None': _cap_res,
        'res = s - s_dict[p]': '`res` = =={res}==',
        's_dict[p] = min': lambda S, B, r: (f'`s_dict[{S.p}] = min({B.s_dict[S.p]}, {S.s})` = =={S.s_dict[S.p]}==：留最小的前缀和，下次减它更大'),
        'return res': '最大和 = =={ret}==',
    },
    cards=dict(
        one_liner='同余的前缀和相减，长度必是 k 的倍数',
        complexity='时间 `O(n)`，空间 `O(k)`',
        problem=['在 `nums` 里找长度是 `k` 的倍数的非空子数组，求最大和',
                 '示例：`[-5,1,2,-3,4]`，`k=2` → `4`',
                 '`k = 1` 时就是经典最大子段和'],
        quote='可以减的前缀只需满足结尾下标与index关于k同余，就可以使得前缀相减得到的子数组的长度为k的倍数。于是在这里可以使用一个哈希表s_dict记录每种下标余数对应的最小前缀和。',
        quote_src='—— yiduobo 题解原文',
        idea=['从 `k = 1` 的最大子段和出发：当前前缀和减去前面最小的前缀和',
              '加上长度限制：只能减==下标模 k 同余==的前缀',
              '`s_dict` 按余数存最小前缀和，一边算前缀和一边更新答案'],
        summary=['时间 `O(n)`，空间 `O(k)`',
                 '`index` 从 1 开始，`s_dict[0] = 0` 代表空前缀',
                 '余数第一次出现时只记录、不更新答案（没有同余前缀可减）',
                 '`res` 初值 `None`，因为答案可能是负数，不能用 0',
                 '对比灵神：灵神用长为 k 的数组 + `inf`，这里用字典和 `None`'],
    ),
)
