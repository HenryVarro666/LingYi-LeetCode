NUMS = [2, 1, 2, 0, 0, 0]
L_CNT, L_PRE = 5, 18  # `total[v] = ...` 与 `prefix[v] = ...` 所在行


def _idx(S):
    """当前正在处理的下标：第一趟 = 已统计个数，第二趟 = 前缀里的个数"""
    if 'v' not in S:
        return None
    if 'prefix' in S:
        k = sum(S['prefix'].values()) - (1 if S['_line'] == L_PRE else 0)
    else:
        k = sum(S['total'].values()) - (1 if S['_line'] == L_CNT else 0)
    return k if 0 <= k < len(S['nums']) else None


def _color(S, i, v):
    k = _idx(S)
    if k is None:
        return None
    if 'prefix' not in S:
        return 'blue' if i == k else ('purple' if i < k or (S['_line'] == L_CNT and i == k) else None)
    ln = S['_line']
    if i == k:
        return 'orange' if (ln in (13, 14) and S.get('dv') == S['v']) else 'blue'
    if 12 <= ln <= 17 and 'dv' in S and v == S['dv']:
        return 'green' if i < k else 'orange'
    return 'cyan' if i < k else None


def _formula(S):
    k = _idx(S)
    if 'v' not in S:
        return '先数一遍全数组，再枚举中间的 `j`：前缀里数 `i`，后缀里数 `k`，两者相乘'
    if 'prefix' not in S:
        return f'第一趟：统计每个数出现几次，放进 `total`'
    if k is None:
        return '所有 `j` 都枚举完了'
    dv = S['v'] * 2
    ln = S['_line']
    if ln >= 13 and 'right' in S and ln <= 17:
        base = f'`left = {S["left"]}`，`right = total[{dv}] − left = {S["total"].get(dv, 0)} − {S["left"]}`'
        if S['v'] == dv and ln >= 15:
            return base + f' `− 1` = =={S["right"]}== （去掉 j 自己）'
        return base + f' = =={S["right"]}=='
    return f'`j = {k}`，`nums[j] = {S["v"]}`，要找的数 `{dv}`'


CONFIG = dict(
    num=3583, title='统计特殊三元组', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举中间 · 前缀哈希表 + 全局哈希表做差',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1510'],
    code='''
class Solution(object):
    def specialTriplets(self, nums):
        total = {}
        for v in nums:
            total[v] = total.get(v, 0) + 1

        prefix = {}
        res = 0
        mod = 10 ** 9 + 7
        for v in nums:
            dv = v + v
            left = prefix.get(dv, 0)
            right = total.get(dv, 0) - left
            if v == dv:
                right -= 1

            res = (res + left * right) % mod
            prefix[v] = prefix.get(v, 0) + 1

        return res
''',
    call=f'Solution().specialTriplets({NUMS})',
    expect=2,
    skip=[4, 'res = 0', 'mod = ', 'dv = v + v'],
    views=[
        dict(type='text', fn=_formula, size=28, h=70),
        dict(type='array', var='nums', label='nums（蓝 = j，青 = 前缀，绿 = 前缀里的 2v，橙 = 后缀里的 2v）', cell=96,
             pointers={_idx: 'blue'}, pointer_labels={_idx: 'j'}, color=_color, h=230),
        dict(type='map', var='total', label='total：整个数组里每个数出现几次', fmt=lambda k, v: f'{k}: {v}', h=120, font=30),
        dict(type='map', var=lambda S: S.get('prefix'), label='prefix：前缀 [0, j-1] 里每个数出现几次',
             fmt=lambda k, v: f'{k}: {v}', h=120, font=30),
    ],
    watch=['v', ('dv', 'dv', 'pink'), ('left', 'left', 'cyan'), ('right', 'right', 'orange'), ('res', 'res', 'green')],
    captions={
        'total = {}': '`total` 记录整个数组里每种数出现的次数',
        'for v in nums': lambda S, B, ret: (f'第一趟：数到 `v = {S.v}`' if 'prefix' not in S
                                            else ('第二趟结束，所有 `j` 都处理完了' if _idx(S) is None
                                                  else f'第二趟：枚举中间的 `j = {_idx(S)}`，`v = nums[j] = {S.v}`')),
        'total[v] = total.get': '第一趟：数到 `{v}`，`total[{v}]` → {total[v]}',
        'prefix = {}': '`prefix` 记录当前 `j` 前缀里每种数的次数，开始为空',
                'left = prefix.get': '`i`、`k` 处的数都得是 `nums[j]` 的两倍 `dv = {v} + {v} = {dv}`；`prefix` 里 `{dv}` 出现 `{left}` 次 → 合法的 `i` 有 ==`{left}`== 个',
        'right = total.get': ('`total[{dv}] − left`：全数组 `{dv}` 的个数 `{total.get(dv, 0)}` 减去前缀的 `{left}` '
                              '→ 下标 `j` 到 `n-1` 里有 `{right}` 个'),
        'if v == dv': lambda S, B, ret: (f'`v == dv == 0`：`j` 自己也是 `{S.dv}`，刚才被算进后缀了，要==减 1=='
                                         if S.v == S.dv else f'`v = {S.v} ≠ dv = {S.dv}`：`j` 自己不会被数进去，不用减'),
        'right -= 1': '减去 `j` 自己 → 合法的 `k` 有 ==`{right}`== 个',
        'res = (res + left * right) % mod': '左 `{left}` 个 × 右 `{right}` 个 = `{left * right}`，累加：`res = {res}`',
        'prefix[v] = prefix.get': '`j` 处理完，`v = {v}` 加入前缀：`prefix[{v}]` → {prefix[v]}',
        'return res': '返回 `res = {res}`',
    },
    max_steps=80,
    cards=dict(
        one_liner='枚举中间 j：前缀里的 2v 个数 × 后缀里的 2v 个数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数三元组 `i < j < k`，要求 `nums[i]` 和 `nums[k]` 都是 `nums[j]` 的两倍',
                 '答案对 `10^9 + 7` 取模',
                 '示例：`[0,1,0,0]` → `1`（三元组 `(0, 2, 3)`）',
                 '本视频：`[2,1,2,0,0,0]` → `2`'],
        quote='枚举正中间的下标j，然后分别检测0到j - 1这个前缀以及j + 1到n - 1这个后缀中有多少满足条件的i和k，然后将二者相乘后累加到答案中。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟遍历，用 `total` 记录每个数在整个数组里出现几次',
              '第二趟遍历 `j`，`prefix` 记录前缀的次数：`left = prefix[2v]`',
              '后缀里 `2v` 的个数用做差得到：`right = total[2v] − left`',
              '`v = 0` 时 `2v` 还是 `0`，做差时把 `j` 自己也数进去了，要 ==再减 1=='],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`nums[j] = 0` 时 `right` 要额外减 1，否则多算',
                 '`total − prefix` 得到的是下标 `[j, n-1]` 的个数，包含 `j` 自己',
                 '每步都取模，防止数值过大；Python 本身不会溢出',
                 '原文为 Python 2 风格写法（`class Solution(object)`），代码未改，只删去了类型说明文档字符串',
                 '对比灵神：灵神是边遍历边==撤销== `suf` 的计数，yiduobo 是用 `total − prefix` 做差'],
    ),
)
