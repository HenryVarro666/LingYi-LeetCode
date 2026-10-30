CONFIG = dict(
    num=2900, title='最长相邻不相等子序列 I', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环 · 鸽巢原理',
    tags=['六、分组循环', '难度分 1469'],
    code='''
class Solution:
    def getLongestSubsequence(self, words: List[str], groups: List[int]) -> List[str]:
        n = len(groups)
        ans = []
        for i, g in enumerate(groups):
            if i == n - 1 or g != groups[i + 1]:  # i 是连续相同段的末尾
                ans.append(words[i])
        return ans
''',
    call='Solution().getLongestSubsequence(["a","b","c","d","e","f","g"], [0,0,0,1,1,0,0])',
    expect=['c', 'e', 'g'],
    views=[
        dict(type='array', var='groups', h=170, label='groups（连续相同为一组）', pointers={'i': 'blue'},
             color=lambda S, i, v: 'green' if 'i' in S and i <= S['i'] and (i == len(S['groups']) - 1 or S['groups'][i] != S['groups'][i+1]) else None),
        dict(type='array', var='words', h=170, label='words', pointers={'i': 'blue'},
             color=lambda S, i, v: 'green' if v in S['ans'] else None),
        dict(type='array', var='ans', h=170, label='ans（已选）'),
    ],
    watch=['i', 'g', ('ans', 'ans', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'ans = []': '`ans` 存每一组选出的单词',
        'for i, g in enumerate': lambda S, B, r: ('遍历完毕，循环结束' if B.get('i') == S['i'] else f'枚举 `i = {S["i"]}`，`groups[i] = {S["g"]}`'),
        'if i == n - 1 or g != groups[i + 1]': '`i` 是不是本组末尾：{"是最后一个元素，必是末尾" if i == n - 1 else ("`" + str(g) + " ≠ " + str(groups[i+1]) + "`，下一个换组了 → 是末尾" if g != groups[i+1] else "`" + str(g) + " = " + str(groups[i+1]) + "`，下一个还是同组 → 不是末尾")}',
        'ans.append(words[i])': '每组只能选一个（选两个就相邻相等了）：选 `{words[i]}`，`ans` = {ans}',
        'return ans': '组数就是最长长度：==`{len(ans)}`== 个：{ans}',
    },
    cards=dict(
        one_liner='groups 分成几段连续相同组，就能选几个',
        complexity='时间 `O(n)`，空间 `O(1)`（不计返回值）',
        problem=['选 `words` 的子序列，相邻两项在 `groups` 里对应的值必须不同',
                 '返回最长的一个，多解任选',
                 '本视频：`groups = [0,0,0,1,1,0,0]` → `[c, e, g]`'],
        quote='比如 groups=0001100，分成三组 000,11,00。根据题意，每一组内只能选一个 words[i]，所以一共选 3 个字符串。如果选超过 3 个字符串，根据鸽巢原理，一定有两个字符串在同一组。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把 `groups` 当作 01 字符串，切成连续相同的组',
              '每组至多选一个，所以长度上限 = 组数；每组选一个就能达到',
              '判断 `i` 是组末尾：到头了，或和下一个不同'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '末尾判断要先写 `i == n - 1`，避免 `groups[i + 1]` 越界',
                 '题解还给了 `groupby` 一行写法：每组取第一个，思路相同',
                 '同类：分组循环模板题'],
    ),
)
