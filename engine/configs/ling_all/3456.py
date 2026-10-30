CONFIG = dict(
    num=3456, title='找出长度为 K 的特殊子字符串', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环 · 数连续相同段',
    tags=['灵神题单', '难度分 1244'],
    code='''
class Solution:
    def hasSpecialSubstring(self, s: str, k: int) -> bool:
        cnt = 0
        for i, c in enumerate(s):
            cnt += 1
            if i == len(s) - 1 or c != s[i + 1]:
                if cnt == k:
                    return True
                cnt = 0
        return False
''',
    call="Solution().hasSpecialSubstring('aaabbcc', 2)",
    expect=True,
    views=[
        dict(type='string', var='s', pointers={'i': 'blue'}, h=200,
             color=lambda S, i, v: ('green' if 'cnt' in S and 'i' in S and S['cnt'] > 0 and S['i'] - S['cnt'] < i <= S['i'] else None)),
        dict(type='text', h=90, fn=lambda S: f"当前连续相同段长度 cnt = =={S['cnt']}==，目标 k = =={S['k']}==" if 'cnt' in S else ''),
    ],
    watch=['i', 'c', ('cnt', 'cnt', 'blue'), 'k'],
    captions={
        3: '`cnt` 记录当前这段连续相同字符的长度',
        9: '这一段处理完了，`cnt` 清零，从下一段重新数',
        'cnt += 1': '`{c}` 属于当前这一段：`cnt` → =={cnt}==',
        'if i == len(s) - 1': lambda S, B, r: ('到了段尾（' + ('已是最后一个字符' if S.i == len(S.s) - 1 else f'下一个 `{S.s[S.i+1]}` ≠ `{S.c}`') + '）→ 这一段结束了，可以检查长度'
                                               if (S.i == len(S.s) - 1 or S.c != S.s[S.i + 1]) else f'下一个还是 `{S.c}` → 这一段还没完，继续数'),
        'if cnt == k': lambda S, B, r: (f'段长 `cnt = {S.cnt}` {"==" if S.cnt == S.k else "≠"} `k = {S.k}`：' + ('==恰好是 k，而且两边字符都不同（段尾才判断）==' if S.cnt == S.k else '长度不对，这段不行')),
        'return True': '找到恰好长 `k` 的整段 → 返回 `True`',
        'return False': '所有段都不满足 → `False`',
    },
    cards=dict(
        one_liner='把字符串切成连续相同的段，只看段长是不是 k',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找长度恰好为 `k`、只含一种字符的子串，且它前后的字符都和它不同',
                 '换句话说：它必须是一整段连续相同字符',
                 '示例：`aaabaaa, k=3` → `true`；本视频：`aaabbcc, k=2` → `true`'],
        quote='遍历 s 的同时，维护连续相同子串长度 cnt，遇到子串末尾就看看 cnt=k 是否成立，成立就立刻返回 true。',
        quote_src='—— 灵茶山艾府题解',
        idea=['前后字符都不同 ⇔ 这个子串是一整段「极大」相同段',
              '边走边数 `cnt`，到段尾（下一个不同或到末尾）才判断',
              '`aaa` 里虽然含有 `aa`，但整段长 3 ≠ 2，不算'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：必须到段尾才比较，否则会把长段的一部分误判',
                 '`i == len(s) - 1` 要放在 `s[i + 1]` 之前，防止越界',
                 '另两种写法：`groupby(s)` 数每组长度，思路相同'],
    ),
)
