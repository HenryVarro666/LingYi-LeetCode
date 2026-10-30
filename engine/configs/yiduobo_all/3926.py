def _cur(S):
    if 'c' not in S:
        return ''
    c = S['c']
    shown = {' ': '空格', '-': '连字符'}.get(c, f"字母 '{c}'")
    return f"当前字符：{shown}"


def _col(S, k, v):
    if v == ' ':
        return 'yellow'
    if v == '-':
        return 'orange'
    return None


CONFIG = dict(
    num=3926, title='有效单词计数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='边拼接边清洗 · split 后哈希计数',
    tags=['灵神题单·滑动窗口与双指针', '难度分 1608'],
    code='''
class Solution(object):
    def countWordOccurrences(self, chunks, queries):
        s = []
        for ch in chunks:
            for c in ch:
                if c == '-' or c == ' ':
                    if s:
                        if s[-1] == '-':
                            s[-1] = ' '
                        elif s[-1] == ' ':
                            continue
                        else:
                            s.append(c)
                else:
                    s.append(c)

        if s and (s[-1] == ' ' or s[-1] == '-'):
            s.pop()
        words = ''.join(s).split()
        cnt = {}
        for w in words:
            cnt[w] = cnt.get(w, 0) + 1

        return [cnt.get(q, 0) for q in queries]
''',
    call='Solution().countWordOccurrences(["ab- c", "--d- ", "e-f"], ["ab", "d", "e-f", "e"])',
    expect=[1, 1, 1, 0],
    views=[
        dict(type='text', fn=lambda S: _cur(S) + (f"　｜　`s` 末尾是 '{S['s'][-1]}'" if S.get('s') and 'c' in S and S['_line'] < 16 else '') if 'c' in S else '', size=26),
        dict(type='array', var='s', label='s（只保留有效字符；黄 = 空格分隔符，橙 = 连字符）', cell=60, color=_col, h=240),
        dict(type='text', fn=lambda S: (f"`words = {S['words']}`" if 'words' in S else ''), size=26),
        dict(type='map', var='cnt', label='cnt：单词 → 出现次数', h=220),
    ],
    watch=[('c', 'c', 'blue'), ('len(s)', 'len(s)', 'cyan'), ('w', 'w', 'green')],
    captions={
        's = []': '`s` 用来逐字符收集清洗后的字符串：只留小写字母，以及合法的分隔符',
        'for ch in chunks': '按顺序遍历每个 chunk：`ch = "{ch}"`',
        'for c in ch': '`c = "{c}"`',
        "if c == '-' or c == ' '": lambda S, B, r: ("`c` 是 `-` 或空格：可能是连字符，也可能是分隔符，要看 `s` 末尾" if S.c in '- ' else "`c` 是小写字母：直接放进 `s`"),
        'if s:': lambda S, B, r: ("`s` 还是空的：`c` 排在最前面，一定是无用的分隔符 → ==直接跳过==" if not S.s else f"`s` 非空，末尾是 `'{S.s[-1]}'`，分情况看"),
        "if s[-1] == '-'": lambda S, B, r: (f"`s` 末尾是 `-`，又来一个 `{S.c}` → 连着两个符号，这个 `-` 不再合法 → ==整体视为分隔符==" if S.s[-1] == '-' else "末尾不是 `-`，继续看"),
        "s[-1] = ' '": '把末尾的 `-` 改成空格，作为分隔符：`s` 末尾现在是空格',
        "elif s[-1] == ' '": lambda S, B, r: ("末尾已经是空格 → 再来空格/连字符也是同一个分隔符 → ==忽略 c==" if S.s[-1] == ' ' else "末尾是字母 → `c` 可以保留"),
        'continue': '忽略这个字符，不重复加分隔符',
        15: '`c` 是字母 → 加到末尾：`s` 长度 `{len(s)}`',
        13: '末尾是字母，`c` 可以是合法连字符，也可以是空格 → 先加进去（连字符到底合不合法由后面的字符决定）',
        'if s and (s[-1]': lambda S, B, r: ("遍历完了：末尾若是空格或连字符，后面再没有字母，这个符号==无效== → 删掉" if S.s and S.s[-1] in '- ' else "末尾是字母，不用处理"),
        's.pop()': '删掉末尾无效的符号',
        'words =': "`''.join(s).split()` 把清洗后的字符串按空格切开，得到单词数组：`{words}`",
        'cnt = {}': '`cnt` 记每个单词出现次数',
        'for w in words': '`w = "{w}"`',
        'cnt[w] =': '`cnt["{w}"]` → =={cnt[w]}==',
        'return': '每个询问查表，没有的取 0：`{ret}`',
    },
    cards=dict(
        one_liner='边拼接边清洗：非法连字符先变成空格，再 split',
        complexity='时间 `O(C+Q)`，空间 `O(C)`',
        problem=['拼接 `chunks` 得到 `s`；单词 = 小写字母，`-` 只有被字母夹住才合法',
                 '其余字符（空格、非法 `-`）都是分隔符，单词要尽可能长',
                 '示例：`["ab- c","--d- ","e-f"]` 查 `["ab","d","e-f","e"]` → `[1,1,1,0]`'],
        quote='根据题目中对于单词的定义，实际上就是要求将chunks先合并成一个大的字符s，然后将非法的连字符视为空格，再进行split，并丢弃掉其中的空串，从而得到单词数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['用一个数组 `s` 逐字符收集，根据末尾字符决定符号怎么处理',
              '空 `s` 开头的符号丢掉；连续的符号压成一个空格；字母后的符号先留着',
              '清洗完直接 `split()`，再用字典计数、查询'],
        summary=['时间 `O(C+Q)`，空间 `O(C)`',
                 '易错：`-` 后面接 `-` 或空格，就==不再合法==，要把已放进去的 `-` 改成空格',
                 '易错：遍历结束后，末尾残留的 `-` 或空格要删掉',
                 '对比灵神：灵神用分组循环一次找出每个单词；yiduobo 先清洗再 split'],
    ),
)
