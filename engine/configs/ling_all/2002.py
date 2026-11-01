_I = lambda S: S['_inner'].get('i')


def _leaf(S):
    if S['_inner'].get('i') is None or 'a' not in S:
        return '每个字符三种选择：==不选 / 放入 a / 放入 b=='
    a, b = S['a'], S['b']
    ja, jb = ''.join(a) or '空', ''.join(b) or '空'
    return f"a = {ja}（长 {len(a)}），b = {jb}（长 {len(b)}），乘积 {len(a) * len(b)}，ans = ==" + str(S.get('ans', 0)) + '=='


CONFIG = dict(
    num=2002, title='两个回文子序列长度的最大乘积', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='子集型回溯：每个字符三选一（Go 原文转写）',
    tags=['灵神题单·动态规划', '灵神题单·链表树与回溯', '难度分 1869'],
    code='''
class Solution:
    def maxProduct(self, s: str) -> int:
        ans = 0
        a = []
        b = []

        def f(i: int) -> None:
            nonlocal ans
            if i == len(s):
                if len(a) * len(b) > ans and isPalindromic(a) and isPalindromic(b):
                    ans = len(a) * len(b)
                return

            # 不选
            f(i + 1)

            # 放入 a
            a.append(s[i])
            f(i + 1)
            a.pop()

            # 放入 b
            b.append(s[i])
            f(i + 1)
            b.pop()

        f(0)
        return ans


def isPalindromic(a: List[str]) -> bool:
    n = len(a)
    for i in range(n // 2):
        if a[i] != a[n - 1 - i]:
            return False
    return True
''',
    call="Solution().maxProduct('aba')",
    expect=2,
    views=[
        dict(type='string', var='s', label='s（蓝箭头 = 当前决定的字符 i）', cell=84, h=150, pointers={_I: 'blue'},
             pointer_labels={_I: 'i'}),
        dict(type='array', var='a', label='a', cell=64, h=120),
        dict(type='array', var='b', label='b', cell=64, h=120),
        dict(type='text', fn=_leaf, size=24, h=60),
        dict(type='calls', h=200),
    ],
    watch=[('i', _I, 'blue'), ('ans', 'ans', 'green')],
    skip=['ans = 0', 'a = []', 'b = []', 'a.pop()', 'b.pop()', 'def f'],
    max_steps=72,
    captions={
        'if i == len(s)': lambda S, B, r: ('`i == len(s)`：每个字符都决定完了，检查 a、b' if S['_inner']['i'] == len(S.s)
                                           else f'`i = {S["_inner"]["i"]} < {len(S.s)}`：还要决定 `s[{S["_inner"]["i"]}] = {S.s[S["_inner"]["i"]]}`'),
        'if len(a) * len(b) > ans': lambda S, B, r: (f'乘积 `{len(S.a)} × {len(S.b)}` = {len(S.a) * len(S.b)}，'
                                                      + ('比 ans 大才有必要检查回文（短路）' if len(S.a) * len(S.b) > S.ans
                                                         else f'不比 ans = {S.ans} 大，不用检查回文')),
        'ans = len(a)': '两个都是回文 → `ans` 更新为 =={ans}==',
        'f(i + 1)': '递归决定下一个字符 `i + 1`',
        'a.append': '`s[i]` 放入 a：a = `{"".join(a)}`',
        'b.append': '`s[i]` 放入 b：b = `{"".join(b)}`',
        12: '这个叶子处理完，返回上一层，继续试上一个字符的下一种选择',
        'return True': '两两对称相等 → 是回文，返回 `True`',
        'return False': '有一对不相等 → ==不是回文==，返回 `False`',
        'f(0)': '从第 0 个字符开始搜索',
        'return ans': '搜索完所有 `3^n` 种分配，最大乘积 `{ret}`',
        'if a[i] != a[n - 1 - i]': '`a[{i}] = {a[i]}` 与 `a[{n-1-i}] = {a[n-1-i]}` {"不等 → 不是回文" if a[i] != a[n-1-i] else "相等"}',
        'for i in range(n // 2)': '从两端向中间比较',
        'n = len(a)': '`n = {n}`',
    },
    cards=dict(
        one_liner='每个字符三选一：不选、进 a、进 b，叶子处判回文',
        complexity='时间 `O(3^n · n)`，空间 `O(n)`',
        problem=['在 `s` 里选两个==下标不相交==的回文子序列，使长度乘积最大',
                 '`2 <= s.length <= 12`，字符串很短',
                 '本视频：`s = "aba"` → `2`（`aa` 和 `b`）'],
        quote='由于两个子序列不能相交，因此每个字符只有三种选择：不选、放到其中一个子序列中、放到另一个子序列中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['字符串很短，==暴力搜索==：对每个字符枚举三种情况',
              '放入 a / b 后递归，回来要 `pop` ==恢复现场==',
              '搜到末尾再判断：乘积比 ans 大且两边都是回文才更新'],
        summary=['时间 `O(3^n · n)`，`n ≤ 12` 可行',
                 '原文为 Go，已按原逻辑逐行转写为 Python：`isPalindromic` 作为模块级函数，`ans` 用 `nonlocal`',
                 '先判乘积是否大于 ans，再判回文，省掉不少检查',
                 '易错点：a、b 追加后必须 `pop` 恢复；这里 3^3 = 27 个叶子，动画中间部分快进'],
    ),
)
