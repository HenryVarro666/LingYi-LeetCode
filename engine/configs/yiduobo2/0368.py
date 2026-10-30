NUMS = [6, 1, 3, 2, 12]


def _ncolor(S, k, v):
    i, j, line = S.get('i'), S.get('j'), S.get('_line', 0)
    if line >= 18 and 'res' in S:
        return 'green' if v in S['res'] else None
    if line >= 13 and 'pos' in S:
        return 'yellow' if k == S['pos'] else None
    if i is None:
        return None
    if k == i:
        return 'blue'
    if j is not None and k == j and line in (8, 9, 10):
        return 'pink'
    return None


def _info(S):
    line = S.get('_line', 0)
    if line >= 18 and 'res' in S:
        return f'从 `pos` 顺着 `fa` 往回找：`res = {S["res"]}`'
    if line >= 13 and 'pos' in S:
        return '找 `f` 最大的位置 `pos`：最大子集的==最大元素=='
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or line not in (8, 9, 10):
        return '`f[i]`：以 `nums[i]` 为==最大元素==的整除子集的最大元素数'
    a, b = S['nums'][i], S['nums'][j]
    return f'`x = {a}` 能否加入以 `S_max = {b}` 结尾的子集？`{a} % {b} = {a % b}`'


def _if_cap(S, B, ret):
    i, j = S.i, S.j
    a, b = S.nums[i], S.nums[j]
    if a % b:
        return f'`{a} % {b} ≠ 0`：加入后就==不是==整除子集了'
    if S.f[j] + 1 > S.f[i]:
        return f'`{a} % {b} = 0`：{a} 是 S_max 的倍数 → 也是子集里所有数的倍数，`f[{j}] + 1 = {S.f[j] + 1} > {S.f[i]}`'
    return f'`{a} % {b} = 0`，但 `f[{j}] + 1 = {S.f[j] + 1}` 不比 `f[{i}] = {S.f[i]}` 大'


CONFIG = dict(
    num=368, title='最大整除子集', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='排序 + DP · fa 数组回溯方案',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def largestDivisibleSubset(self, nums):
        nums = sorted(nums)
        f = [1] * len(nums)
        fa = [None] * len(nums)
        for i in range(1, len(nums)):
            for j in range(i):
                if nums[i] % nums[j] == 0 and f[j] + 1 > f[i]:
                    f[i] = f[j] + 1
                    fa[i] = j

        pos = None
        for i in range(len(nums)):
            if pos is None or f[i] > f[pos]:
                pos = i

        res = []
        while pos is not None:
            res.append(nums[pos])
            pos = fa[pos]

        return res
''',
    call=f'Solution().largestDivisibleSubset({NUMS})',
    expect=[12, 6, 2, 1],
    skip=['for j in range(i)'],
    views=[
        dict(type='text', h=70, size=26, fn=_info),
        dict(type='array', var='nums', label='nums（排序后；蓝 = i，粉 = j）', cell=84, h=210,
             pointers={'i': 'blue', 'j': 'pink'}, color=_ncolor),
        dict(type='array', var='f', label='f', cell=76, h=140),
        dict(type='array', var='fa', label='fa（加入前子集的最大元素下标）', cell=76, h=140),
        dict(type='array', var='res', label='res', cell=76, h=140, color=lambda S, k, v: 'green'),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('pos', 'pos', 'yellow')],
    captions={
        'nums = sorted(nums)': '先从小到大排序 → `{nums}`：新来的 x 只需和子集==最大元素==比较',
        'f = [1] * len(nums)': '`f[i]`：以 `nums[i]` 为最大元素的整除子集最多几个数，初始只有自己 = 1',
        'fa = [None] * len(nums)': '`fa[i]`：`nums[i]` 加入前，子集最大元素的下标（用来找具体方案）',
        'for i in range(1, len(nums))': lambda S, B, ret: (f'考虑新来的 `x = nums[{S.i}] = {S.nums[S.i]}`' if 'i' not in B or S.i != B.i
                                                            else 'DP 算完'),
        'if nums[i] % nums[j] == 0 and f[j] + 1 > f[i]': _if_cap,
        'f[i] = f[j] + 1': '`f[{i}] = f[{j}] + 1 = {f[i]}`',
        'fa[i] = j': '`fa[{i}] = {j}`：{nums[i]} 加入前，子集最大元素是 {nums[j]}',
        'pos = None': '`pos`：f 最大的位置',
        'for i in range(len(nums))': lambda S, B, ret: ('找完了：`pos = {}`'.format(S.pos) if 'i' in B and S.i == B.i
                                                         else f'看 `f[{S.i}] = {S.f[S.i]}`'),
        'if pos is None or f[i] > f[pos]': lambda S, B, ret: ('`pos` 还是 None → 先取 i' if S.pos is None
                                                               else (f'`f[{S.i}] = {S.f[S.i]} > f[{S.pos}] = {S.f[S.pos]}` → 更新' if S.f[S.i] > S.f[S.pos]
                                                                     else f'`f[{S.i}] = {S.f[S.i]}` 不更大')),
        'pos = i': '`pos = {pos}`',
        'res = []': '从 `pos` 开始，顺着 `fa` 回溯出子集',
        'while pos is not None': lambda S, B, ret: (f'`pos = {S.pos}`，继续' if S.pos is not None else '`pos = None`：回溯到头了'),
        'res.append(nums[pos])': '加入 `nums[{pos}] = {nums[pos]}`',
        'pos = fa[pos]': '`pos = fa[{B.pos}] = {pos}`',
        'return res': '返回 `{ret}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='子集最大元素是“代表”：x 是它的倍数就能加进来',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['给一个==无重复==正整数集合 `nums`，找最大的子集',
                 '子集中任意两数，一个是另一个的倍数',
                 '示例：`[1,2,3]` → `[1,2]`；本视频：`[6,1,3,2,12]` → `[12,6,2,1]`'],
        quote='对于新来的一个x，若x % S_max = 0，那么对于任意的Sk，一定有x % Sk = 0，这就意味着将x加入S之后一定也是整除子集。',
        quote_src='—— yiduobo 题解',
        idea=['整除子集 S 的最大元素 S_max 是所有元素的倍数',
              '排序后：`f[i] = f[j] + 1`，`j < i` 且 `nums[i] % nums[j] == 0`',
              '`fa[i]` 记录加入前的最大元素，最后从 f 最大处回溯'],
        result='`f = [1, 2, 2, 3, 4]`，回溯 12 → 6 → 2 → 1',
        summary=['时间：排序 `O(nlogn)` + DP `O(n^2)` = `O(n^2)`',
                 '易错：`fa` 用 `None` 表示“没有前驱”，回溯时 `while pos is not None`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：同样排序后 DP，灵神强调“相邻满足倍数 ⇒ 任意两数满足”，类比 300 题'],
    ),
)
