def _w0(S):
    if 'now_cnt' not in S or S.get('_line', 0) < 11:
        return None
    return S['index'] - len(S['p']) + 1 if 'index' in S else 0


def _w1(S):
    if 'now_cnt' not in S or S.get('_line', 0) < 11:
        return None
    return S['index'] if 'index' in S else len(S['p']) - 1


def _idx(S):
    return S['index'] if 'index' in S else None


def _cmp_text(S):
    ln = S.get('_line', 0)
    if 'now_cnt' not in S:
        return '按 p 的长度开一个==定长窗口==，比较两份计数'
    if ln < 12:
        return f"初始化窗口 `s[0:{len(S['p'])}]` = `\"{S['s'][:len(S['p'])]}\"`"
    if 'index' not in S:
        return f"窗口 `\"{S['s'][:len(S['p'])]}\"`：`now_cnt == p_cnt`？"
    l = S['index'] - len(S['p']) + 1
    w = S['s'][l:S['index'] + 1]
    if ln in (25, 26, 27, 28) and 'char' in S and S['char'] in S['p_cnt']:
        ch = S['char']
        return f"窗口 `\"{w}\"`：对比 `\"{ch}\"`，窗口 `{S['now_cnt'].get(ch, 0)}` 个 vs p `{S['p_cnt'][ch]}` 个"
    return f"窗口 `\"{w}\"`（左边界 `{l}`）"


def _init_eq(S, B, ret):
    if S.now_cnt == S.p_cnt:
        return f'初始窗口计数 `{S.now_cnt}` 与 `p_cnt` 相同 → `0` 是一个可行的解'
    return '初始窗口不是异位词'


def _ne(S, B, ret):
    ch, cnt = S.char, S.cnt
    k = S.now_cnt.get(ch, 0)
    if k != cnt:
        return f'窗口里 `"{ch}"` 有 `{k}` 个，p 里有 `{cnt}` 个 → ==不同=='
    return f'`"{ch}"`：都是 `{cnt}` 个，相同'


CONFIG = dict(
    num=438, title='找到字符串中所有字母异位词', difficulty='Medium', category='滑动窗口',
    author='yiduobo', technique='定长滑动窗口 · 逐字母对比计数',
    code='''
class Solution(object):
    def findAnagrams(self, s, p):
        if len(s) < len(p):
            return []

        p_cnt = {}
        for char in p:
            p_cnt[char] = p_cnt.get(char, 0) + 1

        now_cnt = {}
        for char in s[:len(p)]:
            now_cnt[char] = now_cnt.get(char, 0) + 1

        res = []

        if now_cnt == p_cnt:
            res.append(0)

        for index in range(len(p), len(s)):
            add_char = s[index]
            del_char = s[index - len(p)]
            now_cnt[add_char] = now_cnt.get(add_char, 0) + 1
            now_cnt[del_char] -= 1
            flag = True
            for char, cnt in p_cnt.items():
                if now_cnt.get(char, 0) != cnt:
                    flag = False
                    break
            if flag:
                res.append(index - len(p) + 1)

        return res
''',
    call='Solution().findAnagrams("abba", "ab")',
    expect=[0, 2],
    views=[
        dict(type='text', fn=_cmp_text),
        dict(type='string', var='s', pointers={_idx: 'pink'}, pointer_labels={_idx: 'index'}, window=(_w0, _w1),
             color=lambda S, i, v: 'green' if 'res' in S and i in S['res'] else None, cell=110, h=270, label='s'),
        dict(type='map', var='p_cnt', fmt=lambda k, v: f'{k}: {v}', font=30, h=110, label='p_cnt：p 中每个字符的次数'),
        dict(type='map', var='now_cnt', fmt=lambda k, v: f'{k}: {v}', font=30, h=110, label='now_cnt：窗口中每个字符的次数'),
    ],
    watch=[('index', 'index', 'pink'), ('add_char', 'add_char', 'green'), ('del_char', 'del_char', 'red'),
           'flag', ('res', 'res', 'green')],
    captions={
        'if len(s) < len(p)': 's 比 p 还短就不可能有解；这里 `len(s) = {len(s)}`，`len(p) = {len(p)}`',
        'p_cnt = {}': '先统计 p 中每个字符出现的次数 `p_cnt`',
        'for char in p': lambda S, B, r: ('统计完毕' if 'char' in B and B.char == S.char and S.get('p_cnt') == B.get('p_cnt')
                                          and sum(S.p_cnt.values()) == len(S.p) else f'p 的字符 `"{S.char}"`'),
        'p_cnt[char] = p_cnt.get': '`p_cnt["{char}"]` = {p_cnt[char]}',
        'now_cnt = {}': '按照 p 的长度在 s 中==初始化窗口== `s[0:{len(p)}]`',
        'for char in s[:len(p)]': lambda S, B, r: (f'窗口字符 `"{S.char}"`' if sum(S.now_cnt.values()) < len(S.p) else '初始窗口统计完毕'),
        'now_cnt[char] = now_cnt.get': '`now_cnt["{char}"]` = {now_cnt[char]}',
        'res = []': '`res` 收集答案',
        'if now_cnt == p_cnt': _init_eq,
        'res.append(0)': '`0` 加入答案',
        'for index in range(len(p), len(s))': lambda S, B, r: ('滑到底了' if 'index' in B and B.index == S.index
                                                               else f'窗口往右滑一格：新右边界 `index = {S.index}`'),
        'add_char = s[index]': '右边界进来 `add_char = "{add_char}"`',
        'del_char = s[index - len(p)]': '左边界出去 `del_char = "{del_char}"`',
        'now_cnt[add_char] =': '`now_cnt["{add_char}"]` +1 → {now_cnt[add_char]}',
        'now_cnt[del_char] -= 1': lambda S, B, r: (f'`now_cnt["{S.del_char}"]` −1 → {S.now_cnt[S.del_char]}'
                                                   + ('（减到 0 也不删，所以下面对比用 `.get(char, 0)`）' if S.now_cnt[S.del_char] == 0 else '')),
        'flag = True': '逐个对比 p 的每种字符，先假设是异位词',
        'for char, cnt in p_cnt.items()': lambda S, B, r: ('对比完毕：每种字符都相同' if B.get('char') == S.char == list(S.p_cnt)[-1] and B.get('cnt') == S.cnt
                                                           else f'对比字符 `"{S.char}"`'),
        'if now_cnt.get(char, 0) != cnt': _ne,
        'flag = False': '`flag = False`',
        'break': '已经不是异位词了，提前 `break`',
        'if flag': lambda S, B, r: (f'`flag = True`：新的窗口左边界 `{S.index - len(S.p) + 1}` 是一个可行的解' if S.flag
                                    else '`flag = False`：不是异位词'),
        'res.append(index - len(p) + 1)': '`{index - len(p) + 1}` 加入答案',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='定长窗口每次右移一格：进一个字符、出一个字符，再对比计数',
        complexity='时间 `O(m·|Σ|)`，空间 `O(|Σ|)`',
        problem=['找出 `s` 中所有是 `p` 的==字母异位词==的子串，返回这些子串的起始下标',
                 '示例：`s = "cbaebabacd", p = "abc"` → `[0,6]`',
                 '本视频：`s = "abba", p = "ab"` → `[0,2]`（`"bb"` 不是）'],
        quote='接下来将窗口往右滑动，每次移动==将窗口左边界的字符从now_cnt中移除，同时将窗口右边界的字符加入到now_cnt中==，再判断now_cnt是否与p_cnt相同。',
        quote_src='—— yiduobo 题解原文',
        idea=['异位词就是字母出现次数相同的子串 → 很自然想到滑动窗口',
              '窗口长度固定为 `len(p)`：先统计 `p_cnt` 和初始窗口 `now_cnt`',
              '每滑一格只改两个计数，再逐个字符对比，不同就 `break`'],
        summary=['时间 `O(m·|Σ|)`：每个窗口最多对比 |Σ| 种字符',
                 '易错：新的左边界是 `index − len(p) + 1`，不是 `index − len(p)`',
                 '只对比 p 中的字符就够：长度相同，若窗口有 p 没有的字符，必有 p 的字符不够',
                 '原文为 Python 2 风格（`.items()` 两版通用），只删去了类型说明文档字符串',
                 '对比灵神：灵神用不定长滑窗 + 单个 `cnt`，做到 `O(m + n)`'],
    ),
)
