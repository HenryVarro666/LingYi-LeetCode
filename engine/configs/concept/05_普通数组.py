def _formula(S):
    if 'f' in S and 'i' in S:
        i = S['i']
        a, x = S['f'][i - 1], S['nums'][i]
        how = '左边为负，==另起炉灶==' if a < 0 else '左边非负，==拼上去=='
        return f'`f[{i}] = max(f[{i - 1}], 0) + nums[{i}]` = max({a}, 0) + ({x})：{how}'
    if 'f' in S:
        return '模板①「拼接」型 DP：`f[0] = nums[0]`'
    if 'suf' in S and 'pre' in S and 'i' in S:
        return f"`ans[{S['i']}]` = 左边之积 × 右边之积，左边之积 `pre = {S['pre']}`"
    if 'suf' in S:
        return '模板② 前后缀分解：先倒序算出每个位置 ==右边所有数之积=='
    return ''


def _aux(S):
    if 'f' in S:
        return S['f']
    return S.get('suf')


def _aux_label(S):
    if 'f' in S:
        return '`f[i]`：以 `nums[i]` 结尾的最大子数组和（绿 = 目前最大）'
    if 'suf' in S:
        return '`suf[i]`：倒序时 = 右边之积；正序乘上 `pre` 后 = 答案（绿 = 已完成）'
    return ''


def _aux_color(S, i, v):
    if 'f' in S:
        done = S['f'][:S['i'] + 1] if 'i' in S else S['f'][:1]
        return 'green' if i < len(done) and v == max(done) else None
    if 'suf' in S and 'pre' in S and 'i' in S and i < S['i']:
        return 'green'
    return None


CONFIG = dict(
    num=None, title='普通数组 · 通用思想与模板', author='概念讲解', category='普通数组',
    technique='通用思想与模板', kind='concept', difficulty='',
    code='''
def max_subarray(nums):            # 53. 最大子数组和
    f = nums[:]                    # f[i]：以 nums[i] 结尾的最大和
    for i in range(1, len(nums)):
        f[i] = max(f[i - 1], 0) + nums[i]  # 左边为负就不拼
    return max(f)                  # 答案是 max(f)，不是 f[-1]

def product_except_self(nums):     # 238. 除自身以外数组的乘积
    n = len(nums)
    suf = [1] * n                  # suf[i] = nums[i+1:] 之积
    for i in range(n - 2, -1, -1):
        suf[i] = suf[i + 1] * nums[i + 1]
    pre = 1                        # pre = nums[:i] 之积
    for i, x in enumerate(nums):
        suf[i] *= pre              # 右边之积 × 左边之积
        pre *= x
    return suf
''',
    call='''
a = max_subarray([-2, 1, -3, 4, -1, 2, 1, -5])
b = product_except_self([1, 2, 3, 4])
(a, b)
''',
    expect=(6, [24, 12, 8, 6]),
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='array', var='nums', label='nums', pointers={'i': 'blue'}, h=180),
        dict(type='text', fn=_aux_label, size=24, h=44),
        dict(type='array', var=_aux, label=' ', color=_aux_color, h=150,
             dim=lambda S, i, v: 'f' in S and 'i' in S and i > S['i']),
    ],
    watch=[('i', 'i', 'blue'), 'x', ('pre', 'pre', 'pink'), ('n', 'n')],
    captions={
        'f = nums[:]': '模板①：`f` 先复制一份 nums，`f[0] = nums[0]` 已经对了',
        'for i in range(1': lambda S, B, ret: (f'计算 `f[{S.i}]`：以 `nums[{S.i}] = {S.nums[S.i]}` 结尾'
                                               if B.get('i') != S.i else 'f 全部算完'),
        'f[i] = max': lambda S, B, ret: (
            f'`f[{S.i - 1}] = {S.f[S.i - 1]} < 0`：前面的子数组 ==还不如不要==，从 `nums[{S.i}]` 重新开始 → {S.f[S.i]}'
            if S.f[S.i - 1] < 0 else
            f'`f[{S.i - 1}] = {S.f[S.i - 1]} ≥ 0`：拼上去不亏 → `f[{S.i}] = {S.f[S.i - 1]} {"+" if S.nums[S.i] >= 0 else "-"} {abs(S.nums[S.i])} = {S.f[S.i]}`'),
        'return max(f)': '答案 `max(f) = {ret}`：最优子数组可以在 ==任意位置结尾==',
        'n = len': '模板② 前后缀分解：`ans[i]` = ==左边所有数之积 × 右边所有数之积==',
        'suf = [1] * n': '`suf[n-1] = 1`：最后一个数右边是空的，空积规定为 1',
        'for i in range(n - 2': lambda S, B, ret: (f'倒序：算 `suf[{S.i}]`' if B.get('i') != S.i
                                                   else '右边之积全部算好'),
        'suf[i] = suf[i + 1]': '`suf[{i}] = suf[{i + 1}] × nums[{i + 1}] = {suf[i + 1]} × {nums[i + 1]} = {suf[i]}`',
        'pre = 1': '正序扫描，用一个变量 `pre` 维护左边之积，==省掉 pre 数组==',
        'for i, x': lambda S, B, ret: (f'`i = {S.i}`：左边之积 `pre = {S.pre}`' if B.get('i') != S.i or 'x' not in B
                                       else '扫描结束'),
        'suf[i] *= pre': '`suf[{i}]` = 右边之积 × 左边之积 `{pre}` = =={suf[i]}==，这一位完成',
        'pre *= x': '`pre` 乘上 `{x}` → {pre}，留给下一位',
        'return suf': '返回 `{ret}`：没用除法，两趟 `O(n)`，输出数组之外 `O(1)` 空间',
    },
    cards=dict(
        one_liner='一次遍历，维护「左边的信息」：最优结尾、前缀积、前缀和',
        complexity='时间 `O(n)`（合并区间 `O(n log n)`），空间 `O(1)`',
        problem_heading='什么时候用？',
        problem=['子数组和最大 / 以某处结尾的最优值 → 「拼接」型 DP（53）',
                 '答案依赖「左边所有」和「右边所有」→ 前后缀分解（238）',
                 '区间重叠 → 按左端点排序后一次扫描（56）',
                 '要求原地 `O(1)` 空间 → 三次翻转（189）/ 下标当哈希（41）'],
        before=[dict(heading='核心概念：拼接 & 前后缀分解', lines=[
            '拼接：`f[i] = max(f[i-1], 0) + nums[i]`，左边和为负就另起炉灶',
            '子数组要 ==连续==，所以想「和左边拼不拼」，而不是「选或不选」',
            '前后缀分解：`ans[i] = pre[i] × suf[i]`，先倒序算 suf 再正序乘 pre',
            '空前缀 / 空后缀的初始值：和为 `0`，积为 `1`']),
        ],
        idea_heading='两位作者怎么说',
        quote='选或不选无法保证子数组是连续的……对于子数组问题，更适合用==「拼接」的思路==，即如果 nums[i] 左边的子数组元素和是负的，就不用和左边的子数组拼在一起了。',
        quote_src='—— 灵茶山艾府 · 53. 最大子数组和',
        idea=['灵神 53 还给了「前缀和 + 贪心」：子数组和 = 前缀和之差 → ==121 买卖股票==',
              'yiduobo 53：前面的子序列 ==还不如不要== 就从 0 开始；238 用 `now` 存后缀积',
              '41 题两人都是「下标当哈希」：把 `p` 换到下标 `p-1`，每次交换归位一个数'],
        summary_heading='本类 Hot100 题目 & 学习顺序',
        summary=['`53` 最大子数组和：拼接 DP，或前缀和 − 最小前缀和',
                 '`238` 除自身以外的乘积：前后缀分解，输出数组复用',
                 '`56` 合并区间：按左端点排序，和上一个区间比右端点',
                 '`189` 轮转数组：整体翻转，再翻转前 `k` 个和后 `n-k` 个',
                 '`41` 缺失的第一个正数：把 `x` 换到下标 `x-1`，找第一个不匹配',
                 '易错：53 答案是 `max(f)` 而不是 `f[-1]`；189 先 `k %= n`'],
    ),
)
