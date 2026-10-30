def _top(S):
    if 'length' not in S:
        return ''
    sub = S.get('sub_s')
    c = f"，当前子串 `{sub!r}`" if sub is not None and S['_line'] >= 13 else ''
    return f"当前枚举长度 `length = {S['length']}`{c}"


CONFIG = dict(
    num=3076, title='数组中的最短非公共子字符串', difficulty='Medium', category='字符串',
    author='yiduobo', technique='暴力枚举 · 逐长度找独有子串',
    tags=['灵神题单', '字符串'],
    code='''
class Solution(object):
    def shortestSubstrings(self, arr):

        n = len(arr)
        res = [""] * n
        for i in range(n):
            s = arr[i]
            for length in range(1, len(s) + 1):
                for start in range(len(s)):
                    end = start + length
                    if end > len(s):
                        break
                    sub_s = s[start : end]
                
                    flag = True
                    for j in range(n):
                        if i == j:
                            continue
                        if arr[j].find(sub_s) != -1:
                            flag = False
                            break
                    
                    if flag and (res[i] == "" or res[i] > sub_s):
                        res[i] = sub_s
                
                if res[i] != "":
                    break

        return res
''',
    call='Solution().shortestSubstrings(["abc", "bcd", "abcd"])',
    expect=['', '', 'abcd'],
    views=[
        dict(type='array', var='arr', label='arr（蓝 = 当前字符串 s）', cell=150, pointers={'i': 'blue', 'j': 'pink'}, h=170,
             color=lambda S, k, v: 'blue' if S.get('i') == k else None),
        dict(type='string', var='s', label='s 与当前子串（绿 = sub_s）', cell=84, h=150,
             color=lambda S, k, v: 'green' if S['_line'] >= 13 and 'start' in S and 'end' in S and S['start'] <= k < S['end'] else None),
        dict(type='text', fn=_top, size=26),
        dict(type='array', var='res', label='res（每个字符串目前的答案）', cell=150, h=170,
             color=lambda S, k, v: 'green' if v != '' else None),
    ],
    watch=[('i', 'i', 'blue'), ('length', 'length', 'pink'), ('sub_s', 'sub_s', 'yellow'), ('flag', 'flag', 'orange')],
    captions={
        'n = len': '`n = {n}` 个字符串',
        'res = [': '`res` 先全是空串，表示暂时没有答案',
        'for i in range(n)': lambda S, B, r: ('每个字符串都处理完了' if B.get('i') == S.i and 'res' in B else f'逐个枚举字符串：`i = {S.i}`'),
        's = arr[i]': '当前字符串 `s = "{s}"`',
        'for length in': '枚举子串长度 `length = {length}`：==从短到长==，第一个有解的长度就是最短',
        'for start in': lambda S, B, r: ('这个长度下的起点枚举结束' if B.get('start') == S.start and 'sub_s' in B else f'枚举起点 `start = {S.start}`'),
        'end = start': '`end = start + length = {end}`',
        'if end > len(s)': lambda S, B, r: (f'`end = {S.end} > len(s) = {len(S.s)}` → 子串越界，这一长度枚举完，==break==' if S.end > len(S.s)
                                            else f'`end = {S.end} <= len(s) = {len(S.s)}`，没越界，继续'),
        'sub_s = s[': '取出子串 `sub_s = "{sub_s}"`',
        'flag = True': '`flag` 先假设：它==没在别的字符串里出现过==',
        'for j in range(n)': lambda S, B, r: ('其他字符串都检查完了，没人有它' if B.get('j') == S.j and 'flag' in B and S.flag else f'检查其他字符串：`j = {S.j}`'),
        'if i == j': lambda S, B, r: ('`i == j`，是自己 → 跳过' if S.i == S.j else '`i != j`，要和它比一比'),
        'if arr[j].find': lambda S, B, r: (
            f'`arr[{S.j}].find("{S.sub_s}") != -1` → ==别人那里出现过==，不独有' if S.arr[S.j].find(S.sub_s) != -1
            else f'`"{S.sub_s}"` 不在 `"{S.arr[S.j]}"` 里，继续检查下一个'),
        'flag = False': '`flag = False`，不用再看别的了，==break==',
        'if flag and': lambda S, B, r: (
            (f'`flag` 为真，且 `res[{S.i}]` 为空 → 它就是候选答案' if S.res[S.i] == ''
             else (f'`flag` 为真，`"{S.res[S.i]}" > "{S.sub_s}"` → 更小，换成它' if S.res[S.i] > S.sub_s
                   else f'`flag` 为真，但 `"{S.res[S.i]}" <= "{S.sub_s}"`，字典序不更小')) if S.flag
            else '`flag` 为假：这个子串别人也有 → 不能作答案'),
        'res[i] = sub_s': '`res[{i}] = "{sub_s}"`',
        'if res[i] != ""': lambda S, B, r: (f'`res[{S.i}] = "{S.res[S.i]}"` 非空：==这个长度已有答案，更长的不用看了== → break'
                                           if S.res[S.i] != '' else f'`res[{S.i}]` 仍为空，`length` 加 1 再找'),
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='每个字符串从短到长找，第一个别人没有的子串就是答案',
        complexity='时间 `O(n^2 L^4)`，空间 `O(L)`',
        problem=['给字符串数组 `arr`，对每个 `arr[i]` 找一个子串：',
                 '它==不是其他任何字符串的子串==，要最短；同样短取字典序最小，没有则为空',
                 '示例：`["abc","bcd","abcd"]` → `["","","abcd"]`'],
        quote='逐个枚举字符串s，然后从1到len(s)枚举最短子串的长度length，接下来枚举s中所有长度为length的子串，并检测该子串是否在其他字符串中出现过。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模很小，直接暴力：枚举 s，枚举长度，枚举子串',
              '用 `flag` 记录子串有没有在别的字符串里出现（`find` 判断）',
              '同长度里用 `res[i] > sub_s` 保留字典序最小；长度有解就 `break`'],
        summary=['时间 `O(n^2 L^4)`，`n ≤ 100`、`L ≤ 20`，暴力足够',
                 '易错：要跳过自己（`i == j`）；`break` 内层 start 循环用的是越界判断',
                 '`length` 有解后马上 `break`，保证答案是最短的',
                 '对比灵神：灵神把检查写成 `check` 函数，并先判 `t < res`；这里用 `flag` 内联'],
    ),
)
