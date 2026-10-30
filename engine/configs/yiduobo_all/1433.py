CONFIG = dict(
    num=1433, title='检查一个字符串是否可以打破另一个字符串', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='计数桶 · 从大到小比较',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def checkIfCanBreak(self, s1, s2):

        cnt1 = [0] * 26
        for char in s1:
            cnt1[ord(char) - 97] += 1

        cnt2 = [0] * 26
        for char in s2:
            cnt2[ord(char) - 97] += 1
        
        flag = 0
        for index in range(25, -1, -1):
            if cnt1[index] == cnt2[index]:
                continue
            elif cnt1[index] > cnt2[index]:
                if flag == 2:
                    return False

                flag = 1
                cnt1[index - 1] += cnt1[index] - cnt2[index]
            else:
                if flag == 1:
                    return False
                
                flag = 2
                cnt2[index - 1] += cnt2[index] - cnt1[index]
        
        return True
''',
    call='Solution().checkIfCanBreak("vwz", "xxy")',
    expect=False,
    views=[
        dict(type='text', size=28, fn=lambda S: (f"从 z 往 a 扫：字母 `{chr(97 + S['index'])}`，`s1` 有 {S['cnt1'][S['index']]} 个，`s2` 有 {S['cnt2'][S['index']]} 个；`flag = {S['flag']}`（0 未定 / 1 s1 占优 / 2 s2 占优）" if 'index' in S and 'flag' in S else '先统计两个字符串每个字母出现的次数')),
        dict(type='array', var='cnt1', pointers={'index': 'blue'}, h=200, label='cnt1（s1 = "vwz"）', cell=36,
             color=lambda S, i, v: 'cyan' if v > 0 else None, dim=lambda S, i, v: v == 0 and i != S.get('index', -1)),
        dict(type='array', var='cnt2', pointers={'index': 'pink'}, h=200, label='cnt2（s2 = "xxy"）', cell=36,
             color=lambda S, i, v: 'orange' if v > 0 else None, dim=lambda S, i, v: v == 0 and i != S.get('index', -1)),
        dict(type='text', size=22, fn=lambda S: '下标 0–25 依次对应字母 `a`–`z`'),
    ],
    watch=[('index', 'index', 'blue'), ('flag', 'flag', 'yellow')],
    captions={
        'cnt1 = [0] * 26': '`cnt1` 是 26 个桶，统计 `s1` 里每个字母的个数',
        'for char in s1': lambda S, B, r: ('`s1` 统计完了' if B.get('char') == S.char and len(B.get('cnt1', [])) and sum(S.cnt1) == len(S.s1) else f'统计 `s1` 的字母 `{S.char}`'),
        'cnt1[ord(char) - 97] += 1': '`ord(\'{char}\') - 97 = {ord(char) - 97}`，对应桶 +1',
        'cnt2 = [0] * 26': '同样统计 `s2`',
        'for char in s2': lambda S, B, r: ('`s2` 统计完了' if sum(S.cnt2) == len(S.s2) else f'统计 `s2` 的字母 `{S.char}`'),
        'cnt2[ord(char) - 97] += 1': '`cnt2[{ord(char) - 97}]` +1',
        'flag = 0': '`flag`：记录哪个字符串占优。0 = 还没定，1 = `s1` 大，2 = `s2` 大',
        'for index in range': lambda S, B, r: ('26 个字母都比完了，循环结束' if B.get('index') == S.index else f"比较字母 `{chr(97 + S.index)}`（从大到小，强强对话）"),
        'if cnt1[index] == cnt2[index]': lambda S, B, r: (f"`{S.cnt1[S.index]} == {S.cnt2[S.index]}` → 一样多，同档配对，不分高下" if S.cnt1[S.index] == S.cnt2[S.index]
                                                         else f"`{S.cnt1[S.index]} ≠ {S.cnt2[S.index]}` → 数量不同，要分高下"),
        'continue': '跳过，看下一个更小的字母',
        'elif cnt1[index] > cnt2[index]': lambda S, B, r: (f"`s1` 的 `{chr(97 + S.index)}` 多 `{S.cnt1[S.index] - S.cnt2[S.index]}` 个 → 它们要去压 `s2` 里更小的字母" if S.cnt1[S.index] > S.cnt2[S.index]
                                                       else f"`{S.cnt1[S.index]} < {S.cnt2[S.index]}`：这次是 `s2` 的 `{chr(97 + S.index)}` 更多 → 走 else，`s2` 占优"),
        'if flag == 2': lambda S, B, r: ('`flag = 2`：之前是 `s2` 占优，现在 `s1` 又占优 → ==矛盾==' if S.flag == 2 else f'`flag = {S.flag}` ≠ 2：还没出现 `s2` 占优，没有矛盾'),
        'flag = 1': '`s1` 占优：`flag = 1`',
        'cnt1[index - 1] +=': '`s1` 多出来的 `{cnt1[index] - cnt2[index]}` 个字母没配上，==顺延到更小的字母== `{chr(96 + index)}` 的桶里',
        'if flag == 1': lambda S, B, r: ('`flag = 1`：之前是 `s1` 占优，现在 `s2` 又占优 → ==矛盾==，没法两边都打破' if S.flag == 1 else f'`flag = {S.flag}` ≠ 1：没有矛盾'),
        'flag = 2': '`s2` 占优：`flag = 2`',
        'cnt2[index - 1] +=': '`s2` 多出来的字母顺延到更小的字母 `{chr(96 + index)}` 的桶里',
        'return False': '前后占优方不一致 → 无法打破，返回 `False`',
        'return True': '从头到尾只有一方占优（或持平）→ 可以打破，返回 ==True==',
    },
    cards=dict(
        one_liner='强强对话：排序后逐位比，用计数桶从大到小代替排序',
        complexity='时间 `O(n)`，空间 `O(1)`（26 个桶）',
        problem=['`s1` 能打破 `s2`：存在 `s1` 的一个排列 `x` 和 `s2` 的一个排列 `y`，使 `x[i] >= y[i]` 对所有 `i` 成立（`s2` 打破 `s1` 同理）',
                 '判断两个等长字符串中，是否有一个能打破另一个',
                 '示例：`"abc"` 和 `"xya"` → `True`；本视频：`"vwz"` 和 `"xxy"` → `False`'],
        quote='打破要求字符串中的每一位都满足特定的大小关系，因此在这里我们需要使用强强对话而不是田忌赛马的策略，于是我们可以先对两个字符串中的字符进行排序，然后逐位进行对比。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后逐位比较：每一位 `s1` 都不小于 `s2`，或每一位 `s2` 都不小于 `s1`',
              '用 26 个桶代替排序：从 `z` 往 `a` 扫，对比同一个字母在两个串里的个数',
              '多出来的字母顺延到下一个更小的字母，`flag` 记录谁占优，中途反转就是 `False`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`flag` 只能是一个方向：出现 `1` 之后再遇到 `2`（或反过来）就返回 `False`',
                 '多出来的个数要顺延到 `index - 1`，等价于排序后的逐位比较',
                 '本题库里没有题面，题意按 LeetCode 原题补充；原文为 Python 2 风格，无需修改直接运行',
                 '字母都在 a–z，所以桶只有 26 个，空间是常数'],
    ),
)
