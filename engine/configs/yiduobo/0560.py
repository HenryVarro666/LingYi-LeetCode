def _formula(S):
    if 'pre_sum' not in S or 'res' not in S:
        return ''
    p, k = S['pre_sum'], S['k']
    have = S['pre_dict'].get(p - k, 0)
    return (f'`f[{S["index"]}] = {p}`　要找 `f[i] = {p} − {k} = {p - k}`（前面有 =={have}== 个）　'
            f'`f[{S["index"]}] == k`？{"==是==" if p == k else "否"}')


def _f_color(S, i, v):
    if 'pre_sum' not in S or 'index' not in S:
        return None
    if i == S['index']:
        return 'pink'
    if i < S['index'] and v == S['pre_sum'] - S['k']:
        return 'green'
    return None


CONFIG = dict(
    num=560, title='和为 K 的子数组', difficulty='Medium', category='子串',
    author='yiduobo', technique='前缀和 + 一趟扫描哈希',
    code='''
class Solution(object):
    def subarraySum(self, nums, k):
        f = [nums[0]]
        for index in range(1, len(nums)):
            f.append(f[-1] + nums[index])

        pre_dict = {}
        res = 0
        for index, pre_sum in enumerate(f):
            res += pre_dict.get(pre_sum - k, 0)
            if pre_sum == k:
                res += 1
            pre_dict[pre_sum] = pre_dict.get(pre_sum, 0) + 1

        return res
''',
    call='Solution().subarraySum([1, 2, -1, 3, -2], 3)',
    expect=3,
    views=[
        dict(type='text', fn=_formula),
        dict(type='array', var='nums', pointers={'index': 'blue'}, cell=80),
        dict(type='array', var='f', label='f（前缀和，f[i] 含 nums[i]）', pointers={'index': 'pink'}, cell=80,
             color=_f_color, min_slots=5),
        dict(type='map', var='pre_dict', label='pre_dict：前缀和 → 出现次数', h=120),
    ],
    skip=['for index in range'],
    watch=['index', 'pre_sum', ('pre_sum - k', 'pre_sum - k', 'green'), ('res', 'res', 'orange')],
    captions={
        'f = [nums[0]]': '`f[i]` = `nums[0] + … + nums[i]`（==包含 nums[i]==），先放 `f[0] = {f[0]}`',
        'f.append': '`f[{index}] = f[{index - 1}] + nums[{index}] = {f[-2]} + ({nums[index]}) = {f[-1]}`',
        'pre_dict = {}': '前缀和 `f = {f}` 算好了。`pre_dict` 记录前面每个前缀和出现过几次（一趟扫描 + 哈希）',
        'res = 0': '答案 `res` 从 0 开始',
        'for index, pre_sum': lambda S, B, ret: (f'扫描前缀和：`index = {S.index}`，`pre_sum = f[{S.index}] = {S.pre_sum}`'
                                                 if 'pre_sum' not in B or S.index != B.index else '前缀和扫描完毕'),
        'res += pre_dict.get': lambda S, B, ret: (
            f'`f[{S.index}] − f[i] = k` ⇔ 找 `f[i] = {S.pre_sum - S.k}`：前面==没有==，`res` 不变'
            if S.res == B.res else
            f'`f[{S.index}] − f[i] = k` ⇔ 找 `f[i] = {S.pre_sum - S.k}`：前面有 {S.res - B.res} 个（如 `f[{S.f.index(S.pre_sum - S.k)}]`）'
            f' → 子数组 `nums[{S.f.index(S.pre_sum - S.k) + 1}..{S.index}]`，`res = {S.res}`'),
        'if pre_sum == k': lambda S, B, ret: (f'`pre_sum = {S.pre_sum}` 直接等于 `k`：前缀 `nums[0..{S.index}]` 本身就是解'
                                              if S.pre_sum == S.k else f'`pre_sum = {S.pre_sum} ≠ k`，前缀本身不是解'),
        'res += 1': '==需要特别注意==：从下标 0 开始的子数组没有 `f[i]` 可减，单独加一 → `res = {res}`',
        'pre_dict[pre_sum] =': '查完再把 `{pre_sum}` 记进字典：`pre_dict[{pre_sum}] = {pre_dict[pre_sum]}`',
        'return res': '扫描结束：和为 `k` 的子数组一共 =={ret}== 个',
    },
    cards=dict(
        one_liner='前缀和数组 + 一趟扫描哈希，前缀和直接等于 k 时单独算一个',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给整数数组 `nums` 和整数 `k`，统计==和为 k 的子数组==的个数',
                 '子数组 = 连续、非空的一段；`nums` 里可能有负数',
                 '示例：`nums = [1,2,-1,3,-2], k = 3` → `3`（`[1,2]`、`[3]`、整个数组）'],
        quote='看到子数组和这类问题，很自然就联想到使用前缀和来进行处理。……需要特别注意的是，若prefix_sum[j]直接就等于k，也是一个可行的解。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]` 是 `nums[0..i]` 的和，子数组 `nums[i+1..j]` 的和 = `f[j] − f[i]`',
              '扫描到 `f[j]` 时，字典里记着前面每个前缀和出现几次，==查 f[j] − k 即可==',
              '从下标 0 开始的子数组没有 `f[i]` 可减 → ==f[j] 恰好等于 k 时单独加一=='],
        summary=['时间 `O(n)`（建前缀和 + 一趟扫描），空间 `O(n)`',
                 '`f` 不含「空前缀 0」，所以要 `if pre_sum == k: res += 1`（灵神写法用 `cnt[0] = 1` 代替）',
                 '==先查字典，再存入==：反过来 `k = 0` 时会和自己配对',
                 '原文代码可直接在 Python 3 运行，只删去了 docstring'],
    ),
)
