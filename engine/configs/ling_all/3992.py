CONFIG = dict(
    num=3992, title='重新排列字符串以避免字符对', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='相向双指针 · 原地交换', tags=['灵神题单'],
    code='''
class Solution:
    def rearrangeString(self, s: str, x: str, y: str) -> str:
        t = list(s)
        l, r = 0, len(t) - 1
        while l < r:  # 循环直到不足两个字母
            if t[l] != x:  # 寻找最左边的 x
                l += 1
            elif t[r] != y:  # 寻找最右边的 y
                r -= 1
            else:
                t[l], t[r] = t[r], t[l]
                # 交换后，[0,l] 都不含 x，[r,n-1] 都不含 y，问题变成 [l+1,r-1] 的子问题
                l += 1
                r -= 1
        return ''.join(t)
''',
    call='Solution().rearrangeString("xaxbycyd", "x", "y")',
    expect='yaybxcxd',
    views=[
        dict(type='array', var='t', pointers={'l': 'blue', 'r': 'pink'}, h=300,
             label='t（黄 = x，青 = y）',
             color=lambda S, i, v: 'yellow' if v == S['x'] else ('cyan' if v == S['y'] else None)),
        dict(type='text', size=28, fn=lambda S: (f"目标：所有 `{S['y']}` 在所有 `{S['x']}` 之前；`l` 找 ==x==，`r` 找 ==y==" if 'l' in S else '')),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), 'x', 'y'],
    captions={
        't = list(s)': '字符串不能原地改，先转成列表 `t`',
        'l, r = 0, len': '`l` 在最左、`r` 在最右：左边要清掉 x，右边要清掉 y',
        'while l < r': lambda S, B, r_: (f'`l = {S.l} < r = {S.r}`，还有至少两个字母 → 继续' if S.l < S.r else f'`l = {S.l} >= r = {S.r}`：不足两个字母 → 结束'),
        't[l] != x': lambda S, B, r_: (f'`t[{S.l}] = {S.t[S.l]!r}` 不是 x，已在合适的左边 → `l += 1`' if S.t[S.l] != S.x
                                       else f'`t[{S.l}] = {S.t[S.l]!r}` 是 x，它挡在最左边，必须换到右边'),
        't[r] != y': lambda S, B, r_: (f'`t[{S.r}] = {S.t[S.r]!r}` 不是 y，已在合适的右边 → `r -= 1`' if S.t[S.r] != S.y
                                       else f'`t[{S.r}] = {S.t[S.r]!r}` 是 y，它挡在最右边，必须换到左边'),
        't[l], t[r] =': '左边的 x 和右边的 y ==互换==：y 去了左边，x 去了右边',
        'l += 1': '`l` → {l}',
        'r -= 1': '`r` → {r}',
        'return': '所有 y 都在 x 前面：`{ret!r}`',
    },
    cards=dict(
        one_liner='把左边的 x 和右边的 y 互换，直到双指针相遇',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计入）',
        problem=['给字符串 `s` 和不同的字母 `x`、`y`',
                 '重排 `s`，让所有 `y` 都在所有 `x` 之前，返回任意一个',
                 '示例：`"aabc", x="a", y="c"` → `"cbaa"`'],
        quote='做法同 905. 按奇偶排序数组，交换后，[0,l] 都不含 x，[r,n-1] 都不含 y，问题变成 [l+1,r-1] 的子问题。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['左边不能有 x，右边不能有 y，两端各自清理',
              '左边遇到 x、右边遇到 y，==换一次就同时修好两处==',
              '换完两端各收缩一格，是同样的更小子问题'],
        after=[dict(heading='另一种写法：排序', lines=['`x < y` 时从大到小排，`x > y` 时从小到大排',
                                                       '一行 `sorted(s, reverse = x < y)` 搞定',
                                                       '代价是 `O(n log n)`，双指针做到 `O(n)`'])],
        summary=['时间 `O(n)`，空间 `O(1)`（不计列表本身）',
                 '循环 `while l < r`：不足两个字母就不用换了',
                 '三个分支每次只动指针一步或换一对，不要漏掉 `l += 1; r -= 1`',
                 '同类题：905 按奇偶排序数组、922、75 颜色分类'],
    ),
)
