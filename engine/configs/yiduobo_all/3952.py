def _txt(S):
    if 'p' not in S:
        return '把 s 切成 `011..1` 的段：段内的数加起来，再减去最小值'
    return f"当前段最小值 `mi = {S['mi']}`；累计 `res` = =={S['res']}=="


CONFIG = dict(
    num=3952, title='下标覆盖处的最大总和', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='贪心 · 按 011..1 分段，段和减最小值',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1763'],
    code='''
class Solution(object):
    def maxTotal(self, nums, s):
        
        mi = 0
        res = 0

        p = 0
        while p < len(nums):
            while p < len(nums) and s[p] == '0':
                mi = nums[p]
                p += 1

            if p == len(nums):
                break
            
            res += mi
            while p < len(nums) and s[p] == '1':
                mi = min(mi, nums[p])
                res += nums[p]
                p += 1
            
            res -= mi
        
        return res
''',
    call="Solution().maxTotal([9,3,5,2,7,4,6], '0110101')",
    expect=27,
    views=[
        dict(type='array', var='nums', label='nums', h=200, cell=86, pointers={'p': 'blue'},
             color=lambda S, i, v: ('blue' if i == S['p'] else None) if 'p' in S else None),
        dict(type='string', var='s', label='s（标记）', h=190, cell=86, pointers={'p': 'blue'},
             color=lambda S, i, v: 'green' if v == '1' else None),
        dict(type='text', fn=_txt, size=26, h=80),
    ],
    watch=[('p', 'p', 'blue'), ('mi', 'mi', 'orange'), ('res', 'res', 'green')],
    captions={
        'mi = 0': '`mi`：当前段的最小值。初值 0 相当于在最前面补一个 `0`，应对 s 以 1 开头',
        'res = 0': '`res` 累计答案',
        'p = 0': '`p` 从头扫描整个字符串',
        'while p < len(nums):': lambda S, B, r: (f'`p = {S.p} < {len(S.nums)}`：还有没处理的位置，开始找下一段' if S.p < len(S.nums) else f'`p = {S.p}`：扫完了'),
        "s[p] == '0'": lambda S, B, r: (f"`s[{S.p}] = 0`：跳过这个 0（相邻的 0 可直接跳过）" if S.p < len(S.s) and S.s[S.p] == '0'
                                       else ('0 跳完了，`p` 到了末尾' if S.p >= len(S.s) else f"`s[{S.p}] = 1`：段的 1 开始了，不再跳")),
        'mi = nums[p]': '记住最近一个 0 对应的数：`mi = {mi}`，它是这一段 `011..1` 里的第一个，可能最小',
        'p += 1': '`p` → {p}',
        'if p == len(nums)': '{"字符串走完，没有新的一段，结束" if p == len(nums) else "后面还有 1，新的一段开始"}',
        'res += mi': '把段头 0 位置的数先加上：`res` → {res}（它能被右边的 1 左移覆盖）',
        "s[p] == '1'": lambda S, B, r: (f"`s[{S.p}] = 1`：属于这一段" if S.p < len(S.s) and S.s[S.p] == '1' else '这一段的 1 走完了'),
        'mi = min(mi, nums[p])': '取段内最小：`mi = min({B.mi}, {nums[p]}) = {mi}`',
        'res += nums[p]': '`nums[{p}] = {nums[p]}` 加进来：`res` → {res}',
        'res -= mi': '这一段总有一个位置覆盖不到，把最小的 `{mi}` 减掉 → ==`res = {res}`==',
        'return res': '最大总和 `{res}`',
    },
    cards=dict(
        one_liner='每段 011..1 把 0 移到最小值处：段和减最小值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s[i] = 1` 表示下标 `i` 有标记，每个标记最多向左移一格',
                 '标记覆盖到的下标，`nums` 之和最大是多少',
                 '示例：`nums=[9,3,5,2,7,4,6], s="0110101"` → `27`'],
        quote='相当于让这个0保持不变，或者与后续这一中的任意1进行交换。为了使得最终答案最大，在这里就相当于在这一段连续下标中找到nums最小的位置，然后将这个\'0\'移动到该位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['标记不应重叠（`nums` 都是正数），重叠等于浪费一个标记',
              '`011..1` 里把 0 与某个 1 交换，等价于选一个位置不覆盖',
              '不覆盖最小值最优；以 1 开头时用初值 `mi = 0` 补一个虚拟的 0'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '相邻的 `0` 直接跳过，只有最后一个 0 才带着下一段 1',
                 '易错：`mi` 要包含段头 0 位置的数；`p == len(nums)` 时必须 `break`',
                 '原文为 Python 2 风格，无需改动即可在 Python 3 运行',
                 '对比灵神：灵神一次 for 同时判断段头/段尾；这里用嵌套 while 显式分段'],
    ),
)
