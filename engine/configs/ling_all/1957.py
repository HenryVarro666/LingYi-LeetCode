CONFIG = dict(
    num=1957, title='删除字符使字符串变好', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环 · 每段保留至多 2 个',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1358'],
    code='''
class Solution:
    def makeFancyString(self, s: str) -> str:
        ans = []
        cnt = 0
        for i, ch in enumerate(s):
            cnt += 1
            if cnt < 3:
                ans.append(ch)
            if i < len(s) - 1 and ch != s[i + 1]:
                cnt = 0  # 当前字母和下个字母不同，重置计数器
        return ''.join(ans)
''',
    call='Solution().makeFancyString("aaabaaaa")',
    expect='aabaa',
    views=[
        dict(type='string', var='s', pointers={'i': 'blue'}, h=240,
             color=lambda S, i, v: 'pink' if 'i' in S and 'cnt' in S and i <= S['i'] and S['i'] - i < S['cnt'] and S['cnt'] >= 3 and S['i'] - i >= 2 else None),
        dict(type='array', var='ans', label='ans（保留的字符）', h=200, index=False),
    ],
    watch=['i', ('cnt', 'cnt', 'pink'), ('ch', 'ch', 'blue')],
    captions={
        3: '`ans` 存放保留下来的字符',
        4: '`cnt` 统计当前这一段相同字母已经数到几个',
        'cnt += 1': '又见到一个 `{ch}`，当前段长度 `cnt = {cnt}`',
        'if cnt < 3': lambda S, B, r: (f'`cnt = {S.cnt} < 3` → 还不会出现三连，保留 `{S.ch}`' if S.cnt < 3 else f'`cnt = {S.cnt} ≥ 3` → 再留就是三连了，丢掉这个 `{S.ch}`'),
        'ans.append(ch)': '保留：`ans` = `{"".join(ans)}`',
        'if i < len(s) - 1': lambda S, B, r: ('已经是最后一个字符，不用再看下一个' if S.i == len(S.s) - 1 else (f'下一个字符 `{S.s[S.i+1]}` 与当前 `{S.ch}` 不同 → 这一段结束' if S.ch != S.s[S.i+1] else f'下一个字符还是 `{S.ch}` → 这一段继续')),
        10: '下一段从头数：`cnt = 0`',
        "return ''.join": '拼接保留的字符：=={ret!r}==',
    },
    cards=dict(
        one_liner='把字符串按相同字母分段，每段最多保留 2 个',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['没有三个连续相同字符的字符串是好字符串',
                 '删除最少的字符使 `s` 变好，返回结果',
                 '示例：`"aaabaaaa"` → `"aabaa"`'],
        quote='把 s 按照连续相同字母分成若干段，每段保留至多 2 个字母。用一个计数器 cnt 统计每一段的当前长度，如果 cnt<3 就把当前字母加入答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['分组循环：`cnt` 数当前段已有几个字母',
              '`cnt < 3` 才保留，所以每段至多留 2 个',
              '当前字母与下一个不同，就把 `cnt` 清零开始新段'],
        after=[dict(heading='另一种写法', lines=['用 `groupby(s)` 分组，每组取 `list(group)[:2]`', '思路相同，代码更短'])],
        summary=['时间 `O(n)`，空间 `O(n)`（`ans` 列表），不计返回值可视为 `O(1)`',
                 '`cnt` 的清零放在循环末尾，要判断 `i < len(s) - 1` 防止越界',
                 '最少删除 = 每段只多出的那部分，答案唯一',
                 '相比 yiduobo：灵神靠计数器，不回看已保留的字符'],
    ),
)
