def _in_bit(S):
    return 'self.tree' in S.get('_inner', {})


def _ptr_tree(S):
    return S['_inner'].get('i') if _in_bit(S) else None


def _idx(S):
    x = S.get('x')
    return S['nums'].index(x) if x is not None and x in S['nums'] else None


def _formula(S):
    i = _idx(S)
    if i is None or 'j' not in S:
        return '`b[i] = nums[i] − i`：平衡条件变成 ==b 非降==；`f` 用树状数组维护前缀最大'
    x = S['x']
    if 'f' in S and S.get('_line') in (9, 10):
        return f'`f = max(前缀最大, 0) + nums[{i}]` = =={S["f"]}=='
    return f'`nums[{i}] − {i} = {x - i}`，离散化后是 `j = {S["j"]}`'


CONFIG = dict(
    num=2926, title='平衡子序列的最大和', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='离散化 + 树状数组维护前缀最大值',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构', '难度分 2448'],
    code='''
class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        b = sorted(set(x - i for i, x in enumerate(nums)))  # 离散化 nums[i]-i
        t = BIT(len(b) + 1)
        for i, x in enumerate(nums):
            j = bisect_left(b, x - i) + 1  # nums[i]-i 离散化后的值（从 1 开始）
            f = max(t.pre_max(j), 0) + x
            t.update(j, f)
        return t.pre_max(len(b))  # 所有 f 的最大值

# 树状数组模板（维护前缀最大值）
class BIT:
    def __init__(self, n: int):
        self.tree = [-inf] * n

    def update(self, i: int, val: int) -> None:
        while i < len(self.tree):
            self.tree[i] = max(self.tree[i], val)
            i += i & -i

    def pre_max(self, i: int) -> int:
        mx = -inf
        while i > 0:
            mx = max(mx, self.tree[i])
            i &= i - 1
        return mx
''',
    call='Solution().maxBalancedSubsequenceSum([5,-1,-3,8])',
    expect=13,
    skip=['self.tree = [-inf]', 'def __init__', 'mx = -inf'],
    views=[
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='array', var='nums', label='nums', h=190, cell=90, pointers={'nums.index(x) if x in nums else None': 'blue'}, pointer_labels={'nums.index(x) if x in nums else None': 'i'},
             color=lambda S, k, v: 'blue' if k == _idx(S) else None),
        dict(type='array', var='b', label='b：nums[i]−i 排序去重（第 k 个 ↔ 树状数组位置 k+1）', h=200, cell=90,
             pointers={'j - 1': 'pink'}, pointer_labels={'j - 1': 'j'},
             color=lambda S, k, v: 'pink' if 'j' in S and k == S['j'] - 1 else None),
        dict(type='array', var='t.tree', label='树状数组 tree：每格 = 一段位置上 f 的最大值（0 不用）', h=210, cell=90,
             pointers={"_inner.get('i') if 'self.tree' in _inner else None": 'yellow'}, pointer_labels={"_inner.get('i') if 'self.tree' in _inner else None": 'i'},
             color=lambda S, k, v: 'yellow' if _in_bit(S) and k == S['_inner'].get('i') else None),
    ],
    max_steps=70,
    watch=[('i', 'i', 'yellow'), ('x', 'x', 'blue'), ('j', 'j', 'pink'), ('f', 'f', 'green'), ('mx', 'S["_inner"].get("mx")', 'cyan')],
    captions={
        'b = sorted': '`nums[i] − i` 一律算出来：{b}。条件 `nums[i]−nums[j] >= i−j` 等价于 ==b[j] <= b[i]==，选一条 ==非降子序列==',
        't = BIT': '建树状数组，初值全是 `-inf`；它用来回答 "b 不超过某值的所有 f 的最大值"',
        'j = bisect_left': '`x − i = {x - i}` 在 b 里的名次 → 树状数组位置 `j = {j}`',
        'f = max': '先查 b 名次不超过 `{j}` 的 f 最大值 `t.pre_max({j})`，再 `max(它, 0) + ({x})`',
        't.update(j, f)': '`f = max(前缀最大, 0) + ({x})` = =={f}==（前面和为负就不接）；写进位置 `j = {j}`，之后 b 更大的元素能从它转移',
        'return t.pre_max': '全部 f 的最大值就是答案：查询整棵树的前缀最大',
        'while i < len': lambda S, B, r: (f'`i = {S.i} < {len(S.self.tree) if hasattr(S, "self") else len(S["self.tree"])}`：位置没出界，更新它' if S.i < len(S['self.tree']) else f'`i = {S.i}` 已出界 → 更新结束'),
        'self.tree[i] = max': '`tree[{i}] = max(旧值, {val})` = =={self.tree[i]}==',
        'i += i & -i': '`i` 加上自己的最低位 1 → 跳到管着我的上一层：`i = {i}`',
        'mx = -inf': '查询前缀最大：从 `-inf` 开始',
        'while i > 0': lambda S, B, r: ('`i = %s > 0`：还有区间没看' % S.i) if S.i > 0 else '`i = 0`：前缀都看完了',
        'mx = max(mx': '`mx = max({B.mx}, tree[{i}]) = {mx}`：并入这一段的最大值',
        'i &= i - 1': '`i &= i - 1` 去掉最低位 1 → 跳到前一段：`i = {i}`',
        'return mx': '前缀最大值 = =={mx}==',
    },
    cards=dict(
        one_liner='令 b = nums[i] − i，平衡子序列就是 b 的非降子序列',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['选一个下标递增的子序列，相邻两项满足 `nums[j]−nums[i] >= j−i`，求它的最大元素和',
                 '示例：`[5,-1,-3,8]` → `13`（选 5 和 8）',
                 '本视频：`[5,-1,-3,8]` → `13`'],
        quote='定义 b[i] = nums[i] − i，问题变成从 b 中选出一个非降子序列，求对应的 nums 的元素和的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i]` = 以 `i` 结尾的最大和，从 `b[j] <= b[i]` 的 `j` 转移：`max(f[j], 0) + nums[i]`',
              '"b 不超过某值的最大 f" 就是==前缀最大值==，用权值树状数组 `O(log n)` 查询、更新',
              'b 取值范围很大，先排序去重离散化成名次 `1..m`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '前面的和为负就不接：`max(pre_max, 0)`，所以全负数时答案是最大的那个数',
                 '树状数组下标从 1 开始，所以离散化名次要 `+1`，树大小 `len(b)+1`',
                 '树状数组这里只能 "变大"（前缀最大），不能做减小的修改',
                 '同类题：2407 最长递增子序列 II'],
    ),
)
