CONFIG = dict(
    num=2981, title='找出出现至少三次的最长特殊子字符串 I', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='按字母分组 · 前三长的连续段',
    tags=[],
    code='''
class Solution:
    def maximumLength(self, s: str) -> int:
        groups = defaultdict(list)
        cnt = 0
        for i, ch in enumerate(s):
            cnt += 1
            if i + 1 == len(s) or ch != s[i + 1]:
                groups[ch].append(cnt)  # 统计连续字符长度
                cnt = 0

        ans = 0
        for a in groups.values():
            a.sort(reverse=True)
            a.extend([0, 0])  # 假设还有两个空串
            ans = max(ans, a[0] - 2, min(a[0] - 1, a[1]), a[2])

        return ans if ans else -1
''',
    call='Solution().maximumLength("aaaabbbabb")',
    expect=2,
    views=[
        dict(type='text', size=26, fn=lambda S: (f"这一组 `a = {S['a'][:-2] if len(S['a']) >= 2 and S['a'][-2:] == [0, 0] else S['a']}`：`max({S['a'][0]-2}, {min(S['a'][0]-1, S['a'][1])}, {S['a'][2]})`" if 'a' in S and len(S['a']) >= 3 and S['_line'] == 15 else '同一个字母的连续段长度，决定能切出几个特殊子串')),
        dict(type='string', var='s', label='s（黄 = 当前字符）', cell=70, pointers={'i': 'blue'}, h=170,
             color=lambda S, k, v: 'yellow' if 'i' in S and k == S['i'] and S['_line'] <= 9 else None),
        dict(type='map', var='groups', label='groups：字母 → 连续段长度列表', fmt=lambda k, v: f'{k}: {v}', h=210),
    ],
    watch=[('cnt', 'cnt', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'groups = defaultdict': '`groups[字母]` 存这个字母每一段连续出现的长度',
        4: '`cnt` 记录当前这一段已经连续了几个',
        'for i, ch in enumerate(s)': lambda S, B, r: (f"看 `s[{S.i}] = '{S.ch}'`" if S.get('ch') != B.get('ch') or S.get('i') != B.get('i') else '遍历完了，分组结束'),
        'cnt += 1': "`cnt` → {cnt}：`'{ch}'` 又连续了一个",
        'if i + 1 == len(s) or': lambda S, B, r: ((f"到末尾了 → 这一段结束" if S.i + 1 == len(S.s) else f"下一个 `'{S.s[S.i+1]}'` ≠ `'{S.ch}'` → 这一段结束") if (S.i + 1 == len(S.s) or S.ch != S.s[S.i+1]) else f"下一个还是 `'{S.ch}'` → 这一段还没完，继续"),
        'groups[ch].append(cnt)': "字母 `'{ch}'` 记下一段长度 `{cnt}` → `{groups[ch]}`",
        9: '这一段记完了，`cnt` 清零，重新数下一段',
        'ans = 0': '`ans` 记录答案；0 表示还没找到',
        'for a in groups.values()': lambda S, B, r: (f"处理一个字母的长度列表 `a = {S.a}`" if ('a' in S and S.get('a') != B.get('a')) else '所有字母都处理完了'),
        'a.sort(reverse=True)': '从大到小排序：`a[0]` 最长，`a[1]` 次长，`a[2]` 第三长 → `{a}`',
        'a.extend([0, 0])': '补两个 0，当作还有两个空串，就不用判断 `a` 够不够三段 → `{a}`',
        'ans = max(ans,': lambda S, B, r: f'三种取法：最长段切三份 `a[0]-2 = {S.a[0]-2}`；最长+次长 `min(a[0]-1, a[1]) = {min(S.a[0]-1, S.a[1])}`；前三段 `a[2] = {S.a[2]}` → `ans` = =={S.ans}==',
        'return ans if ans': lambda S, B, r: (f'`ans = {S.ans}`：最长的、至少出现三次的特殊子串长度为 =={r}==' if S.ans else '`ans = 0` → 没有出现三次的特殊子串，返回 `-1`'),
    },
    cards=dict(
        one_liner='相同字母分组，只看每组最长的三段',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['特殊字符串只由同一个字母组成。求在 `s` 中==至少出现三次==的最长特殊子串长度，没有返回 `-1`',
                 '示例：`"aaaa"` → `2`（三个 `"aa"`）；`"abcdef"` → `-1`',
                 '本视频：`"aaaabbbabb"` → `2`'],
        quote='从最长的特殊子串（a[0]）中取三个长度均为 a[0]-2 的特殊子串；或者从最长和次长中取三个长度一样的；又或者从最长、次长、第三长中各取一个长为 a[2] 的特殊子串。',
        quote_src='—— 灵茶山艾府题解',
        idea=['按字母分组，每组记录各连续段的长度，从大到小排序',
              '三种取法取最大：`a[0]-2`、`min(a[0]-1, a[1])`、`a[2]`',
              '数组末尾补两个 `0`，段数不足三个也不用特判'],
        summary=['时间 `O(n log n)`（排序），换成堆维护前三大可做到 `O(n)`',
                 '最长段 `a[0]` 切三份是 `a[0]-2`，不是 `a[0]-3`',
                 '`a[0]==a[1]` 时取 `a[0]-1`，`a[0]>a[1]` 时取 `a[1]`，合起来是 `min(a[0]-1, a[1])`',
                 '答案为 0 说明不存在，要返回 `-1`',
                 '思考题：改成至少 k 次，同样看每组最长的前 k 段'],
    ),
)
