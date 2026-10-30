NUMS = [2, 4, 3, 3, 5, 4, 9, 6]
K = 4


def _cond(S):
    if 'x' not in S or S.get('_line') not in (5, 6, 7, 8):
        return '能弹栈的三个条件：栈非空、`x < 栈顶`、`len(st) + (n − i) > k`'
    st, x, i = S['st'], S['x'], S['i']
    n = len(S['nums'])
    if not st:
        return f'`x = {x}`：栈空，没得弹'
    rest = len(st) + n - i
    a = x < st[-1]
    b = rest > K
    return (f'`x = {x}` {"<" if a else "≥"} 栈顶 `{st[-1]}`；`len(st) + n − i = {len(st)} + {n - i} = {rest}` '
            f'{">" if b else "≤"} `k = {K}`')


def _cap_while(S, B, ret):
    st, x, i = B.st, B.x, B.i
    n = len(B.nums)
    if not st:
        return '栈空 → 停止弹栈'
    if x >= st[-1]:
        return f'`x = {x} ≥ 栈顶 {st[-1]}`：替换掉栈顶不会让字典序变小 → 停止'
    if len(st) + n - i <= K:
        return f'`{x} < {st[-1]}`，但 `{len(st)} + {n - i} = {len(st) + n - i} ≤ k`：==弹了就凑不够 k 个== → 不能弹'
    return f'`{x} < 栈顶 {st[-1]}`，且弹完还凑得够 k 个（`{len(st)} + {n - i} > {K}`）→ 弹出栈顶让字典序更小'


CONFIG = dict(
    num=1673, title='找出最具竞争力的子序列', difficulty='Medium', category='栈',
    author='灵茶山艾府', technique='单调栈（最小字典序）',
    tags=['字节30天'],
    code='''
class Solution:
    def mostCompetitive(self, nums: List[int], k: int) -> List[int]:
        st = []
        for i, x in enumerate(nums):
            while st and x < st[-1] and len(st) + len(nums) - i > k:
                st.pop()
            if len(st) < k:
                st.append(x)
        return st
''',
    call=f'Solution().mostCompetitive({NUMS}, {K})',
    expect=[2, 3, 3, 4],
    views=[
        dict(type='text', fn=_cond, h=60, size=26),
        dict(type='array', var='nums', label='nums（i 往右扫）', cell=96, pointers={'i': 'blue'},
             dim=lambda S, j, v: 'i' in S and j < S['i'],
             color=lambda S, j, v: 'blue' if j == S.get('i') else None),
        dict(type='stack', var='st', label=f'st（目标长度 k = {K}，单调递增）', h=150, font=36),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x'), ('len(st)', 'len(st)'), ('剩余 n − i', 'len(nums) - i')],
    captions={
        'st = []': '用栈维护==目前生成的子序列==（栈底到栈顶就是子序列的顺序）',
        'for i, x in enumerate': lambda S, B, r: (f'`nums[{S.i}] = {S.x}`' if B.get('i') != S.get('i') else '遍历结束'),
        'while st and': _cap_while,
        'st.pop()': '弹出 `{B.st[-1]}`：后面换成更小的 `{x}`，字典序更小',
        'if len(st) < k': lambda S, B, r: (f'`len(st) = {len(S.st)} < k`：还没满 → 把 `{S.x}` 加进来' if len(S.st) < K
                                           else f'`len(st) = {len(S.st)} = k`：已经满了，`{S.x}` 不要'),
        'st.append(x)': '`{x}` 入栈：子序列变成 `{st}`',
        'return st': '栈从底到顶就是答案：=={ret}==',
    },
    cards=dict(
        one_liner='遇到更小的数就弹掉栈顶，但要保证弹完还凑得够 k 个',
        complexity='时间 `O(n)`，空间 `O(k)`',
        problem=['返回 `nums` 长度为 `k` 且==最具竞争力==的子序列',
                 '即长度恰好为 `k` 的==字典序最小==子序列',
                 '示例：`nums = [3,5,2,6], k = 2` → `[2,6]`',
                 '示例 2：`[2,4,3,3,5,4,9,6], k = 4` → `[2,3,3,4]`（本视频）'],
        quote='在弹出栈顶元素==之前==，必须保证栈中元素个数加上剩余元素个数是大于 k 的。如果代码中不写这个判断，最后可能会得到一个长度小于 k 的子序列。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`3 < 4`：把末尾的 4 换成 3，字典序变小 → 弹出 4',
              '假如 `k = 7`，看到 4 时就不能弹 5：弹了即使后面全加上也不够 7 个',
              '栈满 k 个以后，后面更大的数直接不要'],
        result='`[2,3,3,4]`，和灵神手动过一遍示例 2 的结果一致',
        summary=['时间 `O(n)`：每个元素至多入栈、出栈各一次；空间 `O(k)`',
                 '易错：弹栈条件是 `len(st) + len(nums) - i > k`（严格大于）',
                 '易错：入栈前要判 `len(st) < k`，否则栈可能超过 k 个',
                 '写法 2：直接把 nums 当栈，`m` 记栈大小，空间 `O(1)`',
                 '同类题：402. 移掉 K 位数字、316. 去除重复字母'],
    ),
)
