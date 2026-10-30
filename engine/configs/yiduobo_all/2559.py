WORDS = ["acme", "kiwi", "egg", "oboe", "fig", "u"]
QUERIES = [[0, 3], [2, 5], [4, 4]]
VOW = set('aeiou')


def _k(S):
    """index (in words) of the current w while building s"""
    if 'w' not in S or 'x' in S or 's' not in S or S.get('_line') not in (5, 6, 7, 8):
        return None
    k = len(S['s']) - 1 if S['_line'] == 5 else len(S['s']) - 2
    return k if 0 <= k < len(S['words']) else None


def _inq(S):
    return 'x' in S and 'y' in S and S.get('_line') in (11, 12)


XP = lambda S: S['x'] if _inq(S) else None          # noqa: E731
YP = lambda S: S['y'] if _inq(S) else None          # noqa: E731
Y1 = lambda S: S['y'] + 1 if _inq(S) else None      # noqa: E731


def _words_color(S, i, v):
    if _inq(S):
        return 'cyan' if S['x'] <= i <= S['y'] else None
    s = S.get('s')
    if isinstance(s, list) and i + 1 < len(s) and s[i + 1] > s[i]:
        return 'green'
    return None


def _s_color(S, i, v):
    if _inq(S):
        if i == S['y'] + 1:
            return 'green'
        if i == S['x']:
            return 'red'
    return None


def _formula(S):
    ln = S.get('_line')
    if ln == 3:
        return '元音集合 `vowel_set`：`a e i o u`'
    if ln == 4:
        return '`s[k]` = 前 `k` 个单词里==符合要求的个数==，`s[0] = 0`'
    k = _k(S)
    if ln == 5 and k is not None:
        w = S['w']
        return f'第 `{k}` 个单词 `"{w}"`：首字母 `{w[0]}`，尾字母 `{w[-1]}`'
    if ln == 5:
        return '所有单词都扫过了，`s` 建好'
    if ln == 6:
        return '`s` 先多一项，值和上一项相同（先假设它不符合要求）'
    if ln in (7, 8):
        w = S['w']
        ok = w[0] in VOW and w[-1] in VOW
        if ln == 7:
            return f'首尾都是元音吗？ `{w[0]}…{w[-1]}` → ' + ('==是==' if ok else '==不是==')
        return f'符合要求：最后一项 +1 → `s[{len(S["s"]) - 1}] = {S["s"][-1]}`'
    if ln == 10:
        return '`res` 收集每个询问的答案'
    if _inq(S):
        x, y, s = S['x'], S['y'], S['s']
        if ln == 11 and len(S['res']) == len(S['queries']):
            return '所有询问都答完了'
        if ln == 11:
            return f'询问 `[{x}, {y}]`：==`s[{y + 1}] − s[{x}]`=='
        return f'`s[{y + 1}] − s[{x}]` = `{s[y + 1]} − {s[x]}` = =={s[y + 1] - s[x]}=='
    if ln == 14:
        return f'所有询问答完：`res` = =={S["res"]}=='
    return ''


def _for1(S, B, ret):
    if len(S.s) == len(S.words) + 1:
        return f'所有单词扫完，前缀和建好：`s = {S.s}`'
    return f'取下一个单词 `w = "{S.w}"`，它是 `words[{len(S.s) - 1}]`'


def _app(S, B, ret):
    return f'`s` 末尾补一项，先抄上一项 `{S.s[-1]}`：当前单词暂时当作不符合要求'


def _if(S, B, ret):
    w = S.w
    if w[0] not in VOW:
        return f'首字母 `{w[0]}` 不是元音 → 不成立（`and` 短路，尾字母不用看）'
    if w[-1] not in VOW:
        return f'首字母 `{w[0]}` 是元音，但尾字母 `{w[-1]}` 不是 → 不成立'
    return f'首字母 `{w[0]}`、尾字母 `{w[-1]}` 都是元音 → ==成立=='


def _for2(S, B, ret):
    if 'x' in B and (B.x, B.y) == (S.x, S.y) and len(S.res) == len(S.queries):
        return '所有询问都答完了'
    return f'询问 `[x, y] = [{S.x}, {S.y}]`：`words[{S.x}..{S.y}]` 里有几个符合要求？'


CONFIG = dict(
    num=2559, title='统计范围内的元音字符串数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和 · 一趟遍历建 s',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1435'],
    code='''
class Solution(object):
    def vowelStrings(self, words, queries):
        vowel_set = set(['a', 'e', 'i', 'o', 'u'])
        s = [0]
        for w in words:
            s.append(s[-1])
            if w[0] in vowel_set and w[-1] in vowel_set:
                s[-1] += 1

        res = []
        for x, y in queries:
            res.append(s[y + 1] - s[x])

        return res
''',
    call=f'Solution().vowelStrings({WORDS}, {QUERIES})',
    expect=[2, 2, 0],
    views=[
        dict(type='text', fn=_formula, h=56),
        dict(type='array', var='words', label='words（绿 = 已确认符合要求；青 = 当前询问区间）', cell=84, h=215,
             color=_words_color, pointers={_k: 'blue', XP: 'red', YP: 'green'},
             pointer_labels={_k: 'w', XP: 'x', YP: 'y'}),
        dict(type='array', var='s', label='s（s[k] = 前 k 个单词里符合要求的个数）', cell=84, h=190, min_slots=len(WORDS) + 1,
             color=_s_color, pointers={XP: 'red', Y1: 'green'}, pointer_labels={XP: 'x', Y1: 'y+1'}),
        dict(type='array', var='res', label='res（每个询问的答案）', cell=84, h=130, min_slots=len(QUERIES)),
    ],
    watch=['x', 'y'],
    captions={
        'vowel_set = set': '`vowel_set` 放五个元音，判断时 `in` 是 `O(1)`',
        's = [0]': '`s = [0]`：`s[0] = 0`，表示前 0 个单词里有 0 个符合要求',
        'for w in words': _for1,
        's.append(s[-1])': _app,
        'if w[0] in vowel_set': _if,
        's[-1] += 1': '符合要求：最后一项 +1 → `s[{len(s) - 1}] = {s[-1]}`',
        'res = []': '`res` 按顺序收集每个询问的答案',
        'for x, y in queries': _for2,
        'res.append(s[y + 1]': lambda S, B, r: (
            f'`[{S.x}, {S.y}]` 的个数 = `s[{S.y + 1}] − s[{S.x}]` = `{S.s[S.y + 1]} − {S.s[S.x]}` = =={S.s[S.y + 1] - S.s[S.x]}==，加入 `res`'),
        'return res': '所有询问答完，返回 `{ret}`',
    },
    cards=dict(
        one_liner='首尾都是元音记 1，其余记 0：区间个数 = 前缀和之差',
        complexity='时间 `O(n+q)`，空间 `O(n)`',
        problem=['`words` 是小写字符串数组，`queries[i] = [l, r]` 问下标 `l..r`（含）里==首尾都是元音==的字符串个数',
                 '元音：`a e i o u`',
                 '示例：`["aba","bcb","ece","aa","e"]`，`[[0,2],[1,4],[1,1]]` → `[2,3,0]`',
                 '本视频：`["acme","kiwi","egg","oboe","fig","u"]` → `[2,2,0]`'],
        quote='如果将元音字符串视为1，非元音字符串视为0，那么本题就是一个经典的区间和问题。对于区间和问题，经典的做法是将区间和转化为前缀和之差',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历 `words`：每来一个单词，`s` 多一项，符合要求就 `+1`',
              '`s[k]` 是前 `k` 个单词里符合要求的个数，`s[0] = 0`',
              '查询 `[x, y]` 的答案 = `s[y + 1] − s[x]`，依次放进 `res`'],
        summary=['时间 `O(n+q)`，空间 `O(n)`；判断一个单词只看首尾字母，是 `O(1)`',
                 '易错：`s` 从 `[0]` 开始，所以右端要用 `s[y + 1]`',
                 '`s.append(s[-1])` 先抄上一项，符合要求再 `s[-1] += 1`',
                 '对比灵神：灵神用 `accumulate` 加列表推导式一行写完；这里展开成循环，能看清 `s` 怎么一项项长出来'],
    ),
)
