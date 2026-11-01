CONFIG = dict(
    num=2283, title='判断一个数的数字计数是否等于数位的值', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='计数数组（Go 原文转写）', tags=[],
    code='''
class Solution:
    def digitCount(self, num: str) -> bool:
        cnt = [0] * 10
        for ch in num:
            cnt[ord(ch) & 15] += 1
        for i, ch in enumerate(num):
            if cnt[i] != ord(ch) & 15:
                return False
        return True
''',
    call='Solution().digitCount("1210")',
    expect=True,
    views=[
        dict(type='string', var='num', pointers={'i': 'blue'}, h=200, label='num（第 i 位应该等于「数字 i 出现的次数」）'),
        dict(type='array', var='cnt', h=230, color=lambda S, i, v: 'green' if 'i' in S and S.get('_line') == 7 and i == S['i'] else None, label='cnt[d]：数字 d 出现的次数'),
    ],
    watch=['i', 'ch', ('num[i]', 'int(num[i])', 'blue')],
    captions={
        'cnt = [0] * 10': '数字只有 0-9，开 10 个计数器',
        'cnt[ord(ch) & 15] += 1': '数字 `{ord(ch) & 15}` 又出现一次 → `cnt[{ord(ch) & 15}] = {cnt[ord(ch) & 15]}`',
        'if cnt[i] != ord(ch) & 15': lambda S, B, r: (f'数字 `{S.i}` 实际出现 `{S.cnt[S.i]}` 次，要求 `{ord(S.ch) & 15}` 次 → 相等，通过' if S.cnt[S.i] == ord(S.ch) & 15 else f'数字 `{S.i}` 实际出现 `{S.cnt[S.i]}` 次，要求 `{ord(S.ch) & 15}` 次 → 不等，直接失败'),
        'return False': '有一位不满足 → `False`',
        'return True': '每一位都满足 → `True`',
    },
    cards=dict(
        one_liner='先数每个数字出现几次，再逐位对照',
        complexity='时间 `O(n)`，空间 `O(1)`（计数数组固定 10 项）',
        problem=['字符串 `num`，对每个下标 `i`',
                 '数字 `i` 在 `num` 中出现的次数必须等于 `num[i]`',
                 '示例：`"1210"` → `True`；`"030"` → `False`'],
        quote='（灵神题解仅给出 Go 代码：先用 `cnt` 数组统计各数字出现次数，再遍历 num，检查 `cnt[i] != int(ch&15)`）',
        quote_src='—— 灵茶山艾府题解代码',
        idea=['第一遍：`cnt[d]` 记录数字 `d` 出现的次数',
              '第二遍：下标 `i` 对应的次数 `cnt[i]` 必须等于 `num[i]`',
              '`ch & 15` 取出字符对应的数字，`"0"` 到 `"9"` 的低 4 位正好是 0 到 9'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python：`ch&15` → `ord(ch) & 15`，`[10]int` → `[0] * 10`',
                 '时间 `O(n)`，空间 `O(1)`',
                 '易错点：下标 `i` 可能超过 9 吗？不会，`n ≤ 10`，所以 `cnt[i]` 不越界',
                 '要先统计完整个字符串，再比较，不能边数边比'],
    ),
)
