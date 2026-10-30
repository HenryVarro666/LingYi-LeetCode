_I = lambda S, k: S['_inner'].get(k)
_P = lambda S: S['_inner'].get('p')
_N = lambda S: S['_inner'].get('now')


def _info(S):
    i = S['_inner']
    if 'now' not in i:
        return '从 pattern 头部开始，逐位给字母分配单词'
    return f"pattern 第 `{i['now']}` 位，s 从第 `{i['p']}` 位往后匹配；映射 `{i['mapping']}`"


CONFIG = dict(
    num=291, title='单词规律 II', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='暴力 DFS 回溯（枚举映射的子串）',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def wordPatternMatch(self, pattern, s):

        m = len(pattern)
        n = len(s)

        def dfs(now, p, mapping, mapped):
            if now == m or p == n:
                return now == m and p == n
            
            key = pattern[now]
            if key in mapping:
                if len(mapping[key]) + p - 1 >= n:
                    return False
                flag = True
                for index, char in enumerate(mapping[key]):
                    if s[index + p] != char:
                        flag = False
                        break
                
                if flag:
                    return dfs(now + 1, p + len(mapping[key]), mapping, mapped)
                else:
                    return False
            
            else:
                for q in range(p, n):
                    val = s[p : q + 1]
                    if val not in mapped:
                        mapping[key] = val
                        mapped.add(val)
                        if dfs(now + 1, q + 1, mapping, mapped):
                            return True
                        mapped.remove(val)
                        mapping.pop(key)
                return False

        return dfs(0, 0, {}, set())
''',
    call='Solution().wordPatternMatch("aba", "xyyx")',
    expect=True,
    views=[
        dict(type='text', fn=_info, h=60),
        dict(type='string', var='pattern', label='pattern（蓝 = 当前要映射的字母）', h=130, cell=70, pointers={_N: 'blue'}, pointer_labels={_N: 'now'}),
        dict(type='string', var='s', label='s（粉 = 已匹配到的位置 p）', h=130, cell=70, pointers={_P: 'pink'}, pointer_labels={_P: 'p'}),
        dict(type='map', var=lambda S: S['_inner'].get('mapping', {}), label='mapping：字母 → 单词', h=120, font=30),
        dict(type='calls', h=200),
    ],
    watch=[('now', _N, 'blue'), ('p', _P, 'pink'), ('key', lambda S: _I(S, 'key')), ('val', lambda S: _I(S, 'val'), 'yellow')],
    skip=['m = len(pattern)', 'n = len(s)', 'flag = True'],
    captions={
        'if now == m or p == n': lambda S, B, ret: (
            f'pattern 用完（`now = {S.now}`）或 s 用完（`p = {S.p}`）？' +
            (' ==两者同时到头 → 找到一种合法映射==' if S.now == S.m and S.p == S.n
             else ' 只有一边到头 → 这条路失败，返回 False' if (S.now == S.m or S.p == S.n)
             else ' 都还有剩 → 继续')),
        'key = pattern[now]': '当前字母 `key = {key!r}`',
        'if key in mapping': lambda S, B, ret: (
            f'`{S.key}` 已有映射 `{S.mapping[S.key]!r}` → 只能检查 s 从 `p={S.p}` 开始是否==正好是它==' if S.key in S.mapping
            else f'`{S.key}` 还没有映射 → 从 `p={S.p}` 开始枚举它对应的子串'),
        13: lambda S, B, ret: (f'映射串 `{S.mapping[S.key]!r}` 太长，s 剩下的装不下 → ==越界，直接失败==' if len(S.mapping[S.key]) + S.p - 1 >= S.n
                               else f'映射串长 `{len(S.mapping[S.key])}`，s 从 `p={S.p}` 起装得下 → 逐字符核对'),
        14: '越界 → 返回 False，上一层换别的映射',
        16: '逐字符比较 s 与已映射的单词',
        17: lambda S, B, ret: (f'`s[{S.index + S.p}] = {S.s[S.index + S.p]!r}` 与 `{S.char!r}` 不同 → ==这个映射对不上==' if S.s[S.index + S.p] != S.char
                               else f'`s[{S.index + S.p}] = {S.s[S.index + S.p]!r}` 与 `{S.char!r}` 相同 → 继续比下一个字符'),
        18: '有字符不同，标记 `flag = False`',
        19: '不用再比了，跳出循环',
        21: lambda S, B, ret: '整个单词都匹配 → 沿着这个映射往后走' if S.flag else '没匹配上 → 失败',
        'return dfs(now + 1, p + len': '匹配成功，两个指针一起前进：`now + 1`，`p + {len(mapping[key])}`',
        24: '映射对不上 → 返回 False，上一层==撤销映射换下一种==',
        36: '所有候选子串都试过仍无解 → 返回 False，上一层回溯',
        'for q in range(p, n)': '枚举子串 `s[p..q]` 作为 `{key}` 的映射，`q = {q}`',
        'val = s[p : q + 1]': '候选单词 `val = {val!r}`',
        'if val not in mapped': lambda S, B, ret: (
            f'`{S.val!r}` 没被别的字母用过 → 可以试' if S.val not in S.mapped
            else f'`{S.val!r}` 已被别的字母占用 → ==不同字母不能映射同一个串==，跳过'),
        'mapping[key] = val': '建立映射 `{key} → {val!r}`',
        'mapped.add(val)': '记入 `mapped`：这个单词已被占用',
        'if dfs(now + 1, q + 1': '带着新映射往后 dfs：`now + 1`，`p` 跳到 `q + 1 = {q + 1}`',
        'mapped.remove': '这条路走不通 → ==回溯==：把 `{val!r}` 从 `mapped` 删掉',
        'mapping.pop': '撤销映射 `{key}`，试下一个更长的子串',
        'return dfs(0, 0': '从 `now = 0, p = 0` 开始，空映射、空已用集合',
        33: '找到了合法映射 → ==一路返回 True==',
    },
    max_steps=90,
    cards=dict(
        one_liner='数据规模小，直接 DFS：给每个字母试各种子串',
        complexity='时间指数级（暴力枚举切分），空间 `O(n)`',
        problem=['给定 `pattern` 和字符串 `s`，判断 `s` 能否按 pattern 切成若干单词',
                 '==每个字母对应一个固定的非空串，不同字母对应不同的串==',
                 '示例：`pattern = "abab"`，`s = "redblueredblue"` → `True`',
                 '本视频：`"aba"` 与 `"xyyx"`（要回溯一次）'],
        quote='没有什么特别好的思路，不过好在本题的数据规模比较小，可以直接暴力dfs解决。',
        quote_src='—— yiduobo 题解',
        idea=['pattern 逐位向后走；字母已有映射 → 在 s 里核对是否匹配',
              '字母没有映射 → 从当前位置枚举 s 的前缀作为映射，记录后继续 dfs',
              '两边==恰好同时走到末尾==才算成功；失败则撤销映射换下一个前缀'],
        result='找到合法映射 a → x，b → yy ✓',
        summary=['时间指数级，空间 `O(n)`；靠小数据规模通过',
                 '易错点：要同时维护 `mapping`（字母→串）和 `mapped`（已用串），保证是==双射==',
                 '回溯时 `mapping` 和 `mapped` 两处都要撤销',
                 '已有映射时先判越界 `len + p - 1 >= n`，再逐字符比较'],
    ),
)
