NUMS = [2, 1, 2, 2, 3, 1, 2]
SHOW = 8  # 只画 cnt_list[0..7]


def NUMP(S):
    """cnt_list 上的指针：下标就是数值 num（超出画出范围时不画）"""
    v = S.get('num')
    return v if isinstance(v, int) and v < SHOW and 'cnt_list' in S else None


def _cur_i(S):
    """第一个循环里 num 对应 nums 的下标：已经计数的个数 - 1"""
    if S.get('_line') != 5 or 'cnt_list' not in S:
        return None
    return sum(S['cnt_list']) - 1


def _nums_color(S, i, v):
    if S.get('_line') in (9, 10) and v == S.get('num'):
        return 'green'  # 第二步：值等于 num 的下标，任选两个就是一组好数对
    k = _cur_i(S)
    if k is None:
        return None
    return 'blue' if i == k else None


def _cnt_color(S, i, v):
    if S.get('_line') in (9, 10) and i == S.get('num'):
        return 'green' if v >= 2 else None
    return 'purple' if v >= 2 and 'res' in S else None


def _formula(S):
    if 'res' not in S:
        return '第一步：一趟扫描，统计每个数出现的次数'
    num = S.get('num')
    if not isinstance(num, int) or S.get('_line') not in (9, 10):
        return f"第二步：枚举数值 1~100，`res = {S['res']}`"
    k = S['cnt_list'][num]
    if k < 2:
        return f'`{num}` 出现 `{k}` 次：凑不出数对'
    return f'`{num}` 出现 `{k}` 次 → `C({k}, 2) = {k}×{k - 1}/2` = =={k * (k - 1) // 2}== 组'


def _if_cap(S, B, ret):
    num = S.num
    k = S.cnt_list[num]
    if k >= 2:
        return f'`cnt_list[{num}] = {k} ≥ 2`：`{num}` 出现了 {k} 次 → ==能凑出好数对=='
    if k == 1:
        return f'`cnt_list[{num}] = 1`：`{num}` 只出现 1 次，凑不出数对'
    return f'`cnt_list[{num}] = 0`：`{num}` 没出现过，跳过'


def _res_cap(S, B, ret):
    num, k = S.num, S.cnt_list[S.num]
    return f'从 {k} 个 `{num}` 里任选 2 个：`{k}×({k}-1)//2 = {k * (k - 1) // 2}` → `res = {B.res} + {k * (k - 1) // 2} = {S.res}`'


CONFIG = dict(
    num=1512, title='好数对的数目', difficulty='Easy', category='哈希',
    author='yiduobo', technique='计数 + 组合数 C(k, 2)',
    tags=['List.md'],
    code='''
class Solution(object):
    def numIdenticalPairs(self, nums):
        cnt_list = [0] * 101
        for num in nums:
            cnt_list[num] += 1

        res = 0
        for num in range(1, 101):
            if cnt_list[num] >= 2:
                res += cnt_list[num] * (cnt_list[num] - 1) // 2

        return res
''',
    call=f'Solution().numIdenticalPairs({NUMS})',
    expect=7,
    skip=['for num in nums', 'for num in range'],
    max_steps=24,
    views=[
        dict(type='array', var=lambda S: NUMS, label='nums（第二步：绿 = 值等于 num 的位置）', cell=76, color=_nums_color),
        dict(type='array', var=lambda S: S['cnt_list'][:SHOW] if 'cnt_list' in S else None,
             label='cnt_list[0..7]（下标 = 数值，8~100 全是 0 未画出）', cell=76,
             pointers={NUMP: 'blue'}, pointer_labels={NUMP: 'num'}, color=_cnt_color),
        dict(type='text', h=70, fn=_formula, size=27),
    ],
    watch=[('num', 'num', 'blue'), ('cnt_list[num]', lambda S: S['cnt_list'][S['num']] if 'num' in S else None),
           ('res', 'res', 'green')],
    captions={
        'cnt_list = [0] * 101': '`1 ≤ nums[i] ≤ 100`：直接开长度 101 的数组当==计数表==',
        'cnt_list[num] += 1': '`num = {num}`：`cnt_list[{num}]` 加一 → `{cnt_list[num]}`',
        'res = 0': '第二步：对每个数值==分别计算方案数==再求和',
        'if cnt_list[num] >= 2': _if_cap,
        'res += cnt_list[num]': _res_cap,
        'return res': '一共 =={ret}== 组好数对',
    },
    cards=dict(
        one_liner='某个数出现 k 次，就贡献 C(k, 2) = k(k-1)/2 组好数对',
        complexity='时间 `O(n + U)`，空间 `O(U)`，`U = 100` 为值域',
        problem=['给你整数数组 `nums`，若 `nums[i] == nums[j]` 且 `i < j`，`(i, j)` 就是==好数对==',
                 '返回好数对的数目（`1 ≤ nums[i] ≤ 100`）',
                 '示例：`[1,2,3,1,1,3]` → `4`；本视频 `[2,1,2,2,3,1,2]` → `7`'],
        quote='若某一个数出现了k次，那么可以形成==C(k, 2)也就是k * (k - 1) / 2组好数对==，那么可以一趟扫描，统计每个数出现的次数，然后分别计算方案数再求和。',
        quote_src='—— yiduobo 题解原文',
        idea=['好数对只和“值相等”有关：==相同值的下标里任选两个==就是一组',
              '先一趟扫描数出每个值出现几次（值域小，用数组计数）',
              '再枚举每个值：出现 `k ≥ 2` 次就加上 `k(k-1)/2`'],
        result='运行结束，返回 `7`：`2` 出现 4 次贡献 6 组，`1` 出现 2 次贡献 1 组',
        summary=['时间 `O(n + 100)`，空间 `O(100)`',
                 '`k(k-1)/2` 一定是整数；==原文 Python 2 的 `/` 已改为整除 `//`==，否则会得到浮点数',
                 '`if cnt_list[num] >= 2` 只是跳过无用计算，去掉也对（`k = 0, 1` 时贡献为 0）',
                 '对比灵神：边遍历边 `ans += cnt[x]`，本质是把 `0+1+…+(k-1) = C(k,2)` 拆开累加',
                 '原文还删去了 docstring，其余照搬'],
    ),
)
