NUMS = [51, 71, 17, 24, 42, 93, 39]


def _txt(S):
    if 'max_d' not in S:
        return '`max_val[d]`：最大数位为 `d` 的==左边==元素里，最大的那个'
    v, d = S['v'], S['max_d']
    other = S['max_val'][d] if S['_line'] != 8 else None
    if S['_line'] == 8:
        return f"`max_val[{d}]` 更新为 =={S['max_val'][d]}==，留给右边的数配对"
    if other == float('-inf'):
        return f"`{v}` 的最大数位是 =={d}==；左边还没有最大数位为 {d} 的数"
    return f"`{v}` 的最大数位是 =={d}==，左边同类最大的是 `{other}`：数对和 `{v} + {other}` = =={v + other}=="


CONFIG = dict(
    num=2815, title='数组中的最大数对和', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右，维护左',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution:
    def maxSum(self, nums: List[int]) -> int:
        ans = -1
        max_val = [-inf] * 10  # 表示不存在最大值
        for v in nums:
            max_d = max(map(int, str(v)))
            ans = max(ans, v + max_val[max_d])
            max_val[max_d] = max(max_val[max_d], v)
        return ans
''',
    call=f'Solution().maxSum({NUMS})',
    expect=132,
    views=[
        dict(type='array', var='nums', label='nums（枚举右边的 v）', h=200,
             color=lambda S, i, v: 'blue' if 'v' in S and S['nums'].index(S['v']) == i else None,
             dim=lambda S, i, v: 'v' in S and i > S['nums'].index(S['v'])),
        dict(type='array', var='max_val', label='max_val[d]（下标 = 最大数位 d）', h=200, cell=80,
             pointers={'max_d': 'pink'},
             color=lambda S, i, v: 'pink' if i == S.get('max_d') else None),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    watch=[('v', 'v', 'blue'), ('max_d', 'max_d', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = -1': '`ans = -1`：没有合法数对时就返回它',
        'max_val = [': '长为 10 的数组，`-inf` 表示这个数位还没有数',
        'for v in nums': lambda S, B, r: (f'枚举右边的数 `v = {S.v}`' if B.get('v') != S.v or 'max_d' not in B else '遍历结束'),
        'max_d = max(': '`{v}` 各数位中最大的是 `{max_d}`',
        'ans = max(ans': lambda S, B, r: (f'左边没有最大数位为 {S.max_d} 的数，`{S.v} + (-inf)` 不会更新答案' if S.max_val[S.max_d] == float('-inf')
                                         else f'和左边同类最大值配对：`max({B.ans}, {S.v} + {S.max_val[S.max_d]})` = =={S.ans}=='),
        'max_val[max_d] = max(': lambda S, B, r: (f'维护左：`max_val[{S.max_d}]` 变成 =={S.v}==（==先算答案再更新==，避免和自己配对）' if B.max_val[S.max_d] != S.max_val[S.max_d]
                                                  else f'`{S.v} < {S.max_val[S.max_d]}`：`max_val[{S.max_d}]` 保持 {S.max_val[S.max_d]}'),
        'return ans': '最大数对和为 `{ans}`',
    },
    cards=dict(
        one_liner='枚举右边的数，和左边同类（最大数位相同）的最大值配对',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['找一对数，它们==数位上最大的数字相等==，求最大的和；不存在返回 `-1`',
                 '示例：`[51,71,17,24,42]` → `88`（71 + 17）',
                 f'本视频：`{NUMS}` → `132`（93 + 39）'],
        quote='用一个长为 10 的数组 maxVal[i] 维护最大数位为 i 的元素的最大值。遍历到 nums[i] 时，用 ==nums[i] + maxVal[maxD]== 更新答案的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举右边的数 `v`，要找左边最大数位相同、且==最大==的数',
              '数位只有 0~9：一个长为 10 的数组就能维护“左边”',
              '`-inf` 表示不存在，加上它不会影响 `ans`，省掉特判'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '==先更新 ans，再更新 max_val==：否则 v 会和自己配对',
                 '`[-inf] * 10` 代替“不存在”的判断，代码更短',
                 '同类模板：「枚举右，维护左」，如 1. 两数之和'],
    ),
)
