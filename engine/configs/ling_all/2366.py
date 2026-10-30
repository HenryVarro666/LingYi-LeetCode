def _idx(S):
    if 'num' in S and 'nums' in S and S['num'] in S['nums']:
        return S['nums'].index(S['num'])
    return None


def _txt(S):
    if 'm' not in S:
        return ''
    n = S.get('num')
    if _idx(S) is None:
        return f"从最后一个数开始，上限 `m = {S['m']}`（最后一个数不用拆）"
    k = (n - 1) // S['m'] if S['_line'] < 9 else None
    if S['_line'] >= 9:
        return f"`{n}` 拆成 `{S['k'] + 1}` 份：最小的一份 `{n} // {S['k'] + 1}` = =={S['m']}==，累计操作 `{S['ans']}`"
    return f"当前数 `{n}`，后面最小值上限 `m = {S['m']}`"


CONFIG = dict(
    num=2366, title='将数组排序的最少替换次数', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='倒序贪心 · 向上取整拆分',
    tags=['灵神题单', '贪心算法', '难度分 2060'],
    code='''
class Solution:
    def minimumReplacement(self, nums: List[int]) -> int:
        ans, m = 0, nums[-1]
        for num in reversed(nums):
            k = (num - 1) // m
            ans += k
            m = num // (k + 1)
        return ans
''',
    call='Solution().minimumReplacement([4, 10, 3, 7])',
    expect=4,
    views=[
        dict(type='text', fn=_txt, size=34, h=90),
        dict(type='array', var='nums', h=300, label='nums（从右往左处理）',
             dim=lambda S, i, v: _idx(S) is not None and i > _idx(S),
             color=lambda S, i, v: 'blue' if i == _idx(S) else None),
    ],
    watch=[('num', 'num', 'blue'), ('m', 'm', 'pink'), 'k', ('ans', 'ans', 'green')],
    captions={
        'ans, m = 0': '最后一个数不用拆（拆了前面只会更难）：`m = nums[-1] = {m}`，`m` 是==后面一段的最小值==，当前数拆出来的每份都不能超过它',
        'for num in reversed': lambda S, B, r: ('数组倒着走完了，结束循环' if B.get('num') == S.get('num') else f"倒着看，当前数 `num = {S.num}`，上限 `m = {S.m}`"),
        'k = (num - 1)': '拆成 `x` 份，每份 `≤ m` → `x = ceil({num}/{m})`，操作次数 `k = x − 1 = ({num}−1)//{m}` = =={k}==（无需判断 num 与 m 的大小，num ≤ m 时 k = 0）',
        'ans += k': '累计操作次数：`ans = {B.ans} + {k}` = =={ans}==',
        'm = num // (k + 1)': '拆成 `{k + 1}` 份，让最小的一份尽量大：`m = {num} // {k + 1}` = =={m}==，给前面留出最宽的限制',
        'return ans': '全部处理完，最少操作 `{ans}` 次',
    },
    cards=dict(
        one_liner='倒着扫，每个数拆成尽量少、且最小份尽量大',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一次操作：把任意一个数替换成两个和为它的数',
                 '要把数组变成==非递减==，求最少操作次数',
                 '示例：`[3,9,3]` → `2`；本视频：`[4,10,3,7]` → `4`'],
        quote='倒着遍历 nums。设当前操作出的最小值为 m，如果 nums[i] > m，那么需要拆分 nums[i]，使得拆分出的数字的最大值不超过 m。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最后一个数不拆；往前看，每个数拆出的各份都要 `≤ m`',
              '份数 `x ≥ ceil(num/m)`，取等号最省，操作 `k = x − 1`',
              '各份尽量均分，最小份 `num // x` 越大，前面越好办 → 作为新的 `m`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`ceil(num/m) - 1` 写成 `(num - 1) // m`，避免浮点',
                 '`num <= m` 时 `k = 0`，`m = num`，不用单独判断',
                 '思考题：拆成实数时答案不同，如 `[5,5,3]` 整数拆分要 3 次'],
    ),
)
