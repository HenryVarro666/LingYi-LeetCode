def _text(S):
    if 'f' not in S:
        return '`F(i) = F(i-1) + S − n × a[n−i]`：每次旋转，每个数系数 +1，末尾那个数从最大系数掉到 0'
    n, a = S['n'], S['nums']
    if 'i' in S and S.get('_line', 0) >= 8:
        return f"`F` 从 `F({n - S['i'] - 1})` 推到 `F({n - S['i']})`：`+ {S['s']} − {n}×{a[S['i']]}`"
    return f"`F(0) = {S['f']}`，`S = {S.get('s', '?')}`" if 's' in S else f"`F(0) = {S['f']}`"


def _color(S, k, v):
    if 'i' in S and S.get('_line', 0) >= 8 and k == S['i']:
        return 'pink'
    return None


CONFIG = dict(
    num=396, title='旋转函数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='相邻两项递推',
    tags=[],
    code='''
class Solution:
    def maxRotateFunction(self, nums: list[int]) -> int:
        n = len(nums)
        f = sum(i * x for i, x in enumerate(nums))  # F(0)
        s = sum(nums)  # nums 的总和

        ans = f
        for i in range(n - 1, 0, -1):
            f += s - n * nums[i]
            ans = max(ans, f)
        return ans
''',
    call='Solution().maxRotateFunction([4, 3, 2, 6])',
    expect=26,
    views=[
        dict(type='text', fn=_text, h=80),
        dict(type='array', var='nums', label='nums（粉 = 这一步移到最前面、系数掉到 0 的数）', cell=110,
             pointers={'i': 'pink'}, color=_color, h=230),
        dict(type='text', fn=lambda S: (f"当前 F = =={S['f']}==，最大值 ans = =={S['ans']}==" if 'ans' in S else ''), h=70),
    ],
    watch=[('n', 'n'), ('s', 's', 'cyan'), ('f', 'f', 'blue'), ('i', 'i', 'pink'), ('ans', 'ans', 'green')],
    skip=['n = len(nums)'],
    captions={
        'f = sum': '先直接算 `F(0) = 0×{nums[0]} + 1×{nums[1]} + …` = =={f}==，只算这一次，花 `O(n)`',
        's = sum': '`s` = 所有数之和 = =={s}==：旋转一次，每个数的系数都 +1，总共多出 `s`',
        'ans = f': '`F(0)` 也是候选，`ans = {f}`',
        'for i in range': lambda S, B, r: (f"`i = {S['i']}`：这一轮从 `F({len(S['nums']) - S['i'] - 1})` 推出 `F({len(S['nums']) - S['i']})`，掉到最前面的是 `nums[{S['i']}]`"
                                           if S['i'] != B.get('i') or 'i' not in B else '每个 F 都算过了'),
        'f += s - n': '其余数系数各 +1 共 `+{s}`，`nums[{i}] = {nums[i]}` 从 `{n - 1}` 掉到 0，相当于再减 `{n}×{nums[i]}`：`F` → =={f}==',
        'ans = max': '`ans = max({B.ans}, {f})` = =={ans}==',
        'return ans': '最大的旋转函数值 `{ret}`',
    },
    cards=dict(
        one_liner='相邻两个 F 只差一个公式，O(1) 递推，不用每次重算',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`arr_k` 是 `nums` 顺时针旋转 `k` 位后的数组',
                 '`F(k) = 0·arr_k[0] + 1·arr_k[1] + … + (n−1)·arr_k[n−1]`',
                 '求 `F(0), F(1), …, F(n−1)` 的最大值',
                 '示例：`[4,3,2,6]` → `26`（`F(3)` 最大）'],
        quote='考察相邻两项之差，能否加快计算过程？……F(i) = F(i-1) + S - n·a[n-i]',
        quote_src='—— 灵茶山艾府题解',
        idea=['`F(0)` → `F(1)`：`a0,a1,a2` 往右移一位，系数各 `+1`；`a3` 跑到最前面，系数 `−(n−1)`',
              '等价于「所有数系数 `+1`（共 `+S`）」再让 `a3` 的系数 `−n`',
              '所以 `F(i) = F(i−1) + S − n·a[n−i]`，从 `F(0)` 一路递推，取最大值'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：下标是 `a[n−i]`，循环从 `n−1` 倒着走到 `1`',
                 '`ans` 初始为 `F(0)`，不要从 0 开始（可能全是负数）',
                 '`n = 1` 时循环不执行，答案就是 `F(0) = 0`',
                 '同类：2121. 相同元素的间隔之和（相邻项递推）'],
    ),
)
