def _p_ptr(S):
    p = S.get('p')
    return p if isinstance(p, int) and 0 <= p < len(S['word1']) else None


def _w1_color(S, k, v):
    cp = S.get('change_point')
    if cp is not None and k == cp and 'index' in S:
        return 'pink'
    res = S.get('res')
    if isinstance(res, list):
        return 'green' if k in res else None
    right = S.get('right') or []
    left = S.get('left') or []
    if 'index' in S and 'change_point' not in S:
        return None
    if k in left and k >= 0 and 'right' not in S:
        return 'green'
    if k in right and k >= 0 and 'index' not in S:
        return 'orange'
    if k in left and 'index' in S and k in left[:S['index']]:
        return 'green'
    return None


def _top(S):
    if 'index' in S and 'res' not in S and 'right' in S and len(S['right']) == len(S['word2']) and S['_line'] >= 36:
        i = S['index']
        return f"试 `word2[{i}]` 作为被改的字母，修改点 = `left[{i-1}]+1`"
    if 'res' in S and isinstance(S['res'], list):
        return f"拼出答案：`left[:{S['index']}]` + 修改点 + 之后贪心匹配 = {S['res']}"
    if 'right' in S and 'index' not in S:
        return '第二趟：反向贪心匹配 word2，得到 `right`（最靠后的匹配）'
    return '第一趟：正向贪心匹配 word2，得到 `left`（最靠前的匹配）'


CONFIG = dict(
    num=3302, title='字典序最小的合法序列', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='贪心匹配 + 枚举修改点',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·动态规划', '难度分 2474'],
    code='''
class Solution(object):
    def validSequence(self, word1, word2):

        left = []
        p = 0
        for char in word2:
            while p < len(word1) and word1[p] != char:
                p += 1
            
            if p == len(word1):
                break
            
            left.append(p)
            p += 1
        
        left.extend([-1] * (len(word2) - len(left)))
    
        if left[-1] == len(word2) - 1:
            return left

        right = []
        p = len(word1) - 1
        for char in word2[::-1]:
            while p >= 0 and word1[p] != char:
                p -= 1
            
            if p < 0:
                break
            
            right.append(p)
            p -= 1
        
        right.extend([-1] * (len(word2) - len(right)))
        right.reverse()

        for index in range(len(word2)):
            if left[index] == index:
                continue
                
            if index == 0:
                change_point = 0
            elif left[index - 1] == -1:
                break
            else:
                change_point = left[index - 1] + 1

            if change_point < len(word1) and (index == len(word2) - 1 or right[index + 1] > change_point):
                res = left[:index] + [change_point]
                p = change_point + 1
                for char in word2[index + 1:]:
                    while word1[p] != char:
                        p += 1
                    res.append(p)
                    p += 1
                
                return res

        return []
''',
    call="Solution().validSequence('bacdc', 'abc')",
    expect=[1, 2, 4],
    views=[
        dict(type='text', fn=_top, size=24),
        dict(type='string', var='word1', label='word1（绿 = left 的位置，橙 = right 的位置，粉 = 修改点）', cell=84, h=150,
             pointers={_p_ptr: 'blue'}, pointer_labels={_p_ptr: 'p'}, color=_w1_color),
        dict(type='string', var='word2', label='word2', cell=84, h=215, pointers={'index': 'pink'}),
        dict(type='array', var='left', label='left[i]：word2[i] 贪心靠前匹配的下标（-1 = 匹配不上）', cell=84, h=150, min_slots=3),
        dict(type='array', var='right', label='right[i]：word2[i] 贪心靠后匹配的下标（-1 = 匹配不上）', cell=84, h=150, min_slots=3),
    ],
    watch=[('p', 'p', 'blue'), ('index', 'index', 'pink'), ('change_point', 'change_point', 'yellow'), ('res', 'res', 'green')],
    captions={
        'left = []': '先不考虑修改：`left` 记录 word2 每个字母贪心匹配到 word1 的下标——越靠前越好',
        'p = 0': '`p` 在 word1 上从左往右走',
        'for char in word2:': lambda S, B, r: (f"要匹配 word2 的 `'{S.char}'`" if S.get('char') != B.get('char') or S.get('char') is None else '全部匹配完'),
        'while p < len(word1) and word1[p] != char': lambda S, B, r: (
            f"`word1[{S.p}] = '{S.word1[S.p]}'` ≠ `'{S.char}'` → `p` 往右" if S.p < len(S.word1) and S.word1[S.p] != S.char
            else (f"`word1[{S.p}] = '{S.word1[S.p]}'` == `'{S.char}'` → 找到" if S.p < len(S.word1) else '`p` 走出 word1')),
        'if p == len(word1)': lambda S, B, r: ('走出 word1 → 再往后的字母都匹配不上，`break`' if S.p == len(S.word1) else '没越界，继续'),
        'left.append(p)': '`left` 追加 `{p}`：`word2[{len(left)-1}]` 匹配在 `word1[{p}]`',
        'p += 1': lambda S, B, r: (f'`p` → {S.p}' if S['_line'] in (8, 52) else f'`p` → {S.p}：下一个字母只能用它右边的'),
        'left.extend': '匹配不上的位置补 `-1`：`left = {left}`',
        'if left[-1] == len(word2) - 1': lambda S, B, r: ('`left[-1] = len(word2) - 1`：word2 就是 word1 的前缀 → 无需修改，直接返回 `left`' if S.left[-1] == len(S.word2) - 1
                                                       else f'`left[-1] = {S.left[-1]}` 不是 `{len(S.word2)-1}`：有字母的位置被占了或匹配不上 → 需要修改'),
        'return left': '不修改就满足，返回 `{left}`',
        'right = []': '`right` 同理，但从后往前贪心：位置越靠后，留给修改点的空间越大',
        'p = len(word1) - 1': '`p` 从 word1 末尾往左：`p = {p}`',
        'for char in word2[::-1]': lambda S, B, r: (f"倒着匹配 `'{S.char}'`" if S.get('char') != B.get('char') or S.get('char') is None else '倒着匹配完了'),
        'while p >= 0 and word1[p] != char': lambda S, B, r: (
            f"`word1[{S.p}] = '{S.word1[S.p]}'` ≠ `'{S.char}'` → `p` 往左" if S.p >= 0 and S.word1[S.p] != S.char
            else (f"`word1[{S.p}] = '{S.word1[S.p]}'` == `'{S.char}'` → 找到" if S.p >= 0 else '`p < 0`：走出 word1')),
        'if p < 0': lambda S, B, r: ('`p < 0` → 后面的字母匹配不上，`break`' if S.p < 0 else '没越界，继续'),
        'right.append(p)': '`right` 追加 `{p}`',
        'p -= 1': lambda S, B, r: (f'`p` → {S.p}' if S['_line'] == 25 else f'`p` → {S.p}：前一个字母只能用它左边的'),
        'right.extend': '补 `-1`',
        'right.reverse()': '翻转后 `right[i]` 对应 `word2[i]`：`right = {right}`',
        'for index in range(len(word2))': lambda S, B, r: (f'假设 `word2[{S.index}]` 是被修改的那个字母' if S.get('index') != B.get('index') or 'index' not in B else '没找到修改点'),
        'if left[index] == index': lambda S, B, r: (f'`left[{S.index}] = {S.index}`：已经和 word1 对齐，无需在这里修改 → `continue`' if S.left[S.index] == S.index
                                                     else f'`left[{S.index}] = {S.left[S.index]}` ≠ `{S.index}`：没有和 word1 的第 {S.index} 位对齐（被挤后或匹配不上）→ 可以考虑在这里修改'),
        'continue': '跳过这个 index',
        'if index == 0': lambda S, B, r: ('`index = 0`：前面没有字母，修改点就是 `word1[0]`' if S.index == 0 else '`index > 0`：修改点要接在 `left[index-1]` 后面'),
        'change_point = 0': '`change_point = 0`',
        'elif left[index - 1] == -1': lambda S, B, r: (f'`left[{S.index-1}] = -1`：前面就已经匹配不上了，改后面没用 → `break`' if S.left[S.index - 1] == -1
                                                    else f'`left[{S.index-1}] = {S.left[S.index-1]}`：前缀匹配得上，继续'),
        'change_point = left[index - 1] + 1': '修改点放在前缀匹配位置的下一格：`change_point = {left[index-1]} + 1 = {change_point}`',
        'if change_point < len(word1)': lambda S, B, r: (
            f'`right[{S.index+1}] = {S.right[S.index+1]} > change_point = {S.change_point}`：修改点右边还放得下 `word2[{S.index+1}:]` → ==就是它=='
            if S.index < len(S.word2) - 1 and S.right[S.index + 1] > S.change_point and S.change_point < len(S.word1)
            else (f'`index` 是最后一个字母，改 `word1[{S.change_point}]` 即可 → ==就是它==' if S.index == len(S.word2) - 1 and S.change_point < len(S.word1)
                  else f'`right[{S.index+1}] = {S.right[S.index+1]} ≤ change_point = {S.change_point}`：右边放不下 `word2[{S.index+1}:]` → 这个修改点不行')),
        'res = left[:index]': '前缀保持 `left[:{index}]`，再接修改点 `{change_point}` → `res = {res}`',
        'p = change_point + 1': '后缀从修改点右边一格开始贪心匹配：`p = {p}`',
        'for char in word2[index + 1:]': lambda S, B, r: (f"后缀匹配 `'{S.char}'`" if S.get('char') != B.get('char') else '后缀匹配完'),
        'while word1[p] != char': lambda S, B, r: (f"`word1[{S.p}] = '{S.word1[S.p]}'` ≠ `'{S.char}'` → `p` 往右" if S.word1[S.p] != S.char
                                                 else f"`word1[{S.p}] = '{S.word1[S.p]}'` == `'{S.char}'` → 找到"),
        'res.append(p)': '`res` 追加 `{p}`：`{res}`',
        'return res': '得到答案 `{res}`',
        'return []': '每个 index 都不行 → 返回空数组',
    },
    max_steps=110,
    cards=dict(
        one_liner='先按不修改贪心求 left / right，再找最靠前的可修改位置',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['在 `word1` 里选升序下标，对应字母修改至多一个后等于 `word2`，求字典序最小的下标序列；无解返回空',
                 '示例：`word1 = "bacdc"`，`word2 = "abc"` → `[1,2,4]`',
                 '`word1 = "aaaaaa"`，`word2 = "aaabc"` → `[]`'],
        quote='对于word2[0 : index]这个前缀，最优的匹配方式依然不变……index越小越好……right[index + 1]大于修改点，就说明存在可用的子序列了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`left`：不修改时每个字母尽量靠前匹配（保留更多字符给后面）；`right`：尽量靠后匹配，用来判断后缀是否放得下',
              '修改点 `index` 越小，答案前面的下标越小；满足 `left[index] != index`、前缀匹配得上、`right[index+1] > change_point`',
              '找到后，前缀取 `left[:index]`，修改点取 `left[index-1]+1`，其余再贪心匹配'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`index = 0` 的修改点是 `word1[0]`，没有 `left[-1]` 可用',
                 '`left[index - 1] == -1` 说明前缀已经匹配不上，直接 `break`',
                 '最后一个字母 `index = len(word2) - 1` 不需要判断 `right`',
                 '对比灵神：灵神用 `suf` 一次扫描，边匹配边决定要不要改；yiduobo 先算 left/right，再找修改点'],
    ),
)
