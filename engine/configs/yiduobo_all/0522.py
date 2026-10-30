CONFIG = dict(
    num=522, title='最长特殊序列 II', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='按长度排序 + 贪心判子序列',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1700'],
    code='''
class Solution(object):
    def findLUSlength(self, strs):

        strs = sorted(strs, key=lambda d:-len(d))
        for i in range(len(strs)):
            for j in range(len(strs)):
                if i == j:
                    continue
                pos = 0
                flag = True
                for char in strs[j]:
                    if strs[i][pos] == char:
                        pos += 1
                        if pos == len(strs[i]):
                            flag = False
                            break
                if not flag:
                    break
            
            if flag:
                return len(strs[i])
        
        return -1
''',
    call="Solution().findLUSlength(['aba', 'cd', 'aba'])",
    expect=2,
    views=[
        dict(type='array', var='strs', label='strs（按长度从大到小）', h=200, cell=130,
             color=lambda S, i, v: 'blue' if 'i' in S and i == S['i'] else ('pink' if 'j' in S and i == S['j'] else None)),
        dict(type='text', fn=lambda S: (f"候选 `strs[{S['i']}] = {S['strs'][S['i']]!r}`（蓝），对手 `strs[{S['j']}] = {S['strs'][S['j']]!r}`（粉）" if 'j' in S and 'i' in S else ''), size=26, h=90),
        dict(type='string', var='char', label='当前字符 char', h=140) if False else dict(type='text', fn=lambda S: (f"已匹配 `pos = {S['pos']}` 个字符，当前 `char = {S['char']!r}`" if 'pos' in S and 'char' in S else ''), size=26, h=90),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('pos', 'pos', 'cyan'), ('flag', 'flag', 'orange')],
    captions={
        'strs = sorted': '按长度从大到小排序：第一个“不是别人子序列”的字符串就是答案',
        'for i in range': lambda S, B, r: ('所有字符串都试完了' if S.i >= len(S.strs) else f'候选 `strs[{S.i}] = {S.strs[S.i]!r}`：它是别人的子序列吗？'),
        'for j in range': lambda S, B, r: ('所有对手都比完了，没有一个包含它' if B.get('j') == S.j else f'拿它和 `strs[{S.j}] = {S.strs[S.j]!r}` 比较'),
        'if i == j': lambda S, B, r: ('`i == j`：不和自己比 → continue' if S.i == S.j else f'`i ≠ j`，开始检查 `strs[{S.i}]` 是否是 `strs[{S.j}]` 的子序列'),
        'pos = 0': '`pos` 指向候选里下一个待匹配的字符',
        'flag = True': '先假设候选==不是==对手的子序列，`flag = True`',
        'for char in strs[j]': lambda S, B, r: (f"取对手的下一个字符 `char = {S.char!r}`" if 'char' in S else '开始扫描对手的字符'),
        'if strs[i][pos] == char': lambda S, B, r: (f"`strs[{S.i}][{S.pos}] = {S.strs[S.i][S.pos]!r}` == `{S.char!r}` → ==匹配上==" if S.strs[S.i][S.pos] == S.char
                                                    else f"`strs[{S.i}][{S.pos}] = {S.strs[S.i][S.pos]!r}` ≠ `{S.char!r}` → 跳过这个字符"),
        'pos += 1': '匹配成功，`pos` → {pos}',
        'if pos == len': lambda S, B, r: (f'`pos = {S.pos}` == 候选长度：候选全部匹配完 → 它==是==对手的子序列' if S.pos == len(S.strs[S.i])
                                          else f'`pos = {S.pos}` < {len(S.strs[S.i])}，还没匹配完，继续扫'),
        'flag = False': '候选是对手的子序列 → `flag = False`，它不独有',
        16: '不用再扫对手剩下的字符了，跳出',
        18: '候选已被包含，不用再比其他对手，跳出 j 循环',
        'if not flag': lambda S, B, r: ('`flag = False`：已被某个对手包含，不用再比其他字符串 → 换下一个候选' if not S.flag
                                         else '`flag = True`：这个对手不包含它，继续比下一个对手'),
        'if flag:': lambda S, B, r: ('`flag = True`：所有对手都不包含它 → 它就是答案' if S.flag else '`flag = False`，换下一个候选'),
        'return len(strs[i])': '最长的独有字符串是 `{strs[i]!r}`，返回 ==`{len(strs[i])}`==',
        'return -1': '每个字符串都是别人的子序列 → 返回 -1',
    },
    cards=dict(
        one_liner='先按长度排序，从长到短找第一个不被包含的串',
        complexity='时间 `O(n²m)`，空间 `O(n)`（排序）',
        problem=['在字符串列表里找最长的==独有子序列==：不能是其他字符串的子序列，没有则返回 `-1`',
                 '视频示例：`["aba","cd","aba"]` → `2`',
                 '两个相同的字符串彼此是子序列，都不独有'],
        quote='若A是B的子序列，那么A的任意子序列也一定是B的子序列，换言之，就是A的任意子序列必然不是特殊子序列。',
        quote_src='—— yiduobo 题解原文',
        idea=['A 是 B 的子序列 → A 的所有子序列都被 B 包含，所以只看整个字符串',
              '先按长度从大到小排序，一旦某个串不是别人的子序列就是答案',
              '检测子序列用贪心：同时扫两个串，能匹配就匹配，匹配完即是子序列'],
        summary=['时间 `O(n²m)`，空间 `O(n)`',
                 '`flag` 为 True 才说明没有任何对手包含候选；内层 break 只跳出字符循环',
                 '`i == j` 要跳过，否则自己必然是自己的子序列',
                 '对比灵神：灵神把子序列判断抽成 `is_subseq` 函数，yiduobo 直接内联在三层循环里',
                 '原文为 Python 2 风格，本题无需改动，可直接在 Python 3 运行'],
    ),
)
