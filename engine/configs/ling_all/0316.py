LINE_FOR = 6  # "for c in s" 所在行（去掉首个空行后 1 起算）


def _idx(S):
    """当前处理到 s 的第几个字符（for 行刚取出字符时 left 还没减）"""
    if 'c' not in S or 'left' not in S:
        return None
    done = len(S['s']) - sum(S['left'].values())
    i = done if S['_line'] == LINE_FOR else done - 1
    return i if 0 <= i < len(S['s']) else None


def _show(S):
    if 'ans' not in S:
        return '目标：每个字母只留一个，字典序最小'
    ans = ''.join(S['ans'])
    i = _idx(S)
    if i is None:
        return f'栈 `ans = "{ans}"`'
    c = S['c']
    top = S['ans'][-1] if S['ans'] else None
    extra = ''
    if top is not None and c != top and c not in S['in_ans']:
        extra = f'　栈顶 `{top}` 右边还有？ ==`left[{top}] = {S["left"][top]}`=='
    return f'读到 `{c}`　栈 `"{ans}"`{extra}'


CONFIG = dict(
    num=316, title='去除重复字母', difficulty='Medium', category='单调栈',
    author='灵茶山艾府', technique='单调栈 · 右边还有才能弹',
    tags=['最小字典序', '难度分 2185'],
    code='''
class Solution:
    def removeDuplicateLetters(self, s: str) -> str:
        left = Counter(s)  # 统计每个字母的出现次数
        ans = []  # 当作栈
        in_ans = set()
        for c in s:
            left[c] -= 1
            if c in in_ans:  # ans 中不能有重复字母
                continue
            # (设 x=ans[-1]) 如果 c < x，且右边还有 x，那么可以把 x 去掉，
            # 因为后面可以重新把 x 加到 ans 中
            while ans and c < ans[-1] and left[ans[-1]]:
                in_ans.remove(ans.pop())  # 标记栈顶不在 ans 中
            ans.append(c)  # 把 c 加到 ans 的末尾
            in_ans.add(c)  # 标记 c 在 ans 中
        return ''.join(ans)
''',
    call='Solution().removeDuplicateLetters("cbacdcbc")',
    expect='acdb',
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前字母，灰 = 已读过）', cell=90, h=215,
             pointers={_idx: 'blue'}, pointer_labels={_idx: 'c'},
             dim=lambda S, i, v: _idx(S) is not None and i < _idx(S),
             color=lambda S, i, v: 'blue' if i == _idx(S) else None),
        dict(type='stack', var='ans', label='ans（栈，栈顶在右）', h=150, font=34),
        dict(type='map', var='left', label='left（右边还剩几个，读到就减一）', fmt=lambda k, v: f"'{k}': {v}", h=160, font=30),
        dict(type='text', fn=_show, size=28, h=90),
    ],
    watch=[('c', 'c', 'blue'), ('ans', "''.join(ans)", 'green'), ('in_ans', 'sorted(in_ans)', 'cyan')],
    captions={
        'left = Counter': '先数好每个字母出现几次，记在 `left` 里：以后 `left[x] == 0` 就表示右边没有 x 了',
        'ans = []': '`ans` 当栈用，里面始终是目前字典序最小的答案',
        'in_ans = set()': '`in_ans` 记录哪些字母已在 `ans` 里，判重 `O(1)`',
        'for c in s': lambda S, B, ret: (f'读入第 `{_idx(S)}` 个字母 `{S.c}`' if _idx(S) is not None else '所有字母读完'),
        'left[c] -= 1': '读到 `{c}`，右边剩下的 `{c}` 少一个：`left[{c!r}] = {left[c]}`',
        'if c in in_ans': lambda S, B, ret: (f"`{S.c}` 已经在 `ans` 里 → ==跳过==（ans 不能有重复字母）" if S.c in S.in_ans
                                              else f"`{S.c}` 还不在 `ans` 里，继续处理"),
        'while ans and': lambda S, B, ret: (
            '栈为空，没有可以弹的，直接入栈' if not S.ans else
            f"`{S.c} < {S.ans[-1]}`，且右边还有 `{S.ans[-1]}`（`left = {S.left[S.ans[-1]]}`）→ ==弹出栈顶=="
            if S.c < S.ans[-1] and S.left[S.ans[-1]] else
            (f"`{S.c} > {S.ans[-1]}`，放在它后面更小，不弹" if S.c > S.ans[-1] else
             f"`{S.c} < {S.ans[-1]}` 但右边没有 `{S.ans[-1]}` 了，==不能弹==（弹了就丢字母）")),
        'in_ans.remove': '弹出 `{B.ans[-1]}`，同时标记它不在 `ans` 里：后面还会再遇到它，那时重新加进来',
        'ans.append(c)': lambda S, B, ret: f'`{S.c}` 入栈 → `ans = "{"".join(S.ans)}"`',
        'in_ans.add(c)': '标记 `{c}` 已在 `ans` 中',
        'return': '遍历完毕，栈里就是答案 `"{ret}"`',
    },
    cards=dict(
        one_liner='右边还有更大的就先弹掉，换成更小的字母',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['去掉重复字母，==每个字母只留一个==，使结果字典序最小，且不能打乱相对顺序',
                 '示例：`"bcabc"` → `"abc"`',
                 '本视频：`"cbacdcbc"` → `"acdb"`'],
        quote='如果 c < x，且右边还有 x，那么可以把 x 去掉，因为后面可以重新把 x 加到 ans 中',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['从左到右遍历，`ans` 当栈：新字母比栈顶小，就想把栈顶换掉',
              '但==只有右边还有这个字母==才能换，否则丢了字母就错了',
              '用 `left` 计数判断右边还有没有，`in_ans` 判断是否已在栈中'],
        summary=['时间 `O(n)`：每个字母最多入栈一次、出栈一次',
                 '空间 `O(|Σ|)`：`ans` 长度不超过 26',
                 '易错：==先减 `left[c]` 再判断==，否则 `left` 里还包含当前这个字母',
                 '易错：弹栈要同步 `in_ans.remove`，否则之后无法重新加入',
                 '同类题：1081 同一道题，3816 删除重复字符后的字典序最小字符串'],
    ),
)
