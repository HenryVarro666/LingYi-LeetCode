S_IN = 'abbaabab'
WORDS = ['ab', 'ba']
WL = 2


def _ok(S):
    return isinstance(S.get('left'), int) and isinstance(S.get('right'), int) and 'index' in S


def _color(S, i, v):
    if not _ok(S):
        return None
    line = S.get('_line') or 0
    l, r = S['left'], S['right']
    if line in (31, 32) and l <= i < l + WL:
        return 'red'
    if line in (33, 34) and l - WL <= i < l:
        return 'red'
    bad = S.get('now_word') not in S.get('word_dict', {})
    if line == 21 and r <= i < r + WL:
        return 'red' if bad else 'blue'
    if line in (23,) and bad and r - WL <= i < r:
        return 'red'
    if 22 <= line <= 30 and r - WL <= i < r and S.get('now_word') in S.get('word_dict', {}):
        return 'blue'
    if line == 37 and l <= i < r:
        return 'green'
    return None


def _text(S):
    if not _ok(S):
        if 'max_start_pos' in S:
            return f"`max_start_pos = {S['s_len']} − {WL}×{len(WORDS)} = {S['max_start_pos']}`：左端点超过它就凑不够了"
        return ''
    l, r = S['left'], S['right']
    parts = [S_IN[k:k + WL] for k in range(l, r, WL)] if r > l else []
    return (f"`index = {S['index']}`，窗口 `[{l},{r})`：`{' | '.join(parts) or '空'}`　"
            f"`word_cnt = {S['word_cnt']}` / `{len(WORDS)}`")


def _cap_while(S, B, ret):
    l, r = S.left, S.right
    if l <= S.max_start_pos and r + WL <= S.s_len:
        return f'`left = {l} ≤ {S.max_start_pos}`，继续读词'
    if l > S.max_start_pos:
        return f'`left = {l} > {S.max_start_pos}`：剩下的放不下所有单词 → 这一轮结束'
    return f'`right + {WL} = {r + WL} > {S.s_len}`：后面没有完整的词了 → 这一轮结束'


def _cap_shrink(S, B, ret):
    w = S.now_word
    c, t = S.now_word_dict[w], S.word_dict[w]
    if c > t:
        lw = S_IN[S.left:S.left + WL]
        extra = '' if lw == w else f'（`"{lw}"` 不是 `"{w}"`，也得==误杀==）'
        return f'`"{w}"` 有 `{c}` 个 > 需要的 `{t}` 个 → 从左端点开始去掉一个词{extra}'
    return f'`"{w}"` 有 `{c}` 个，不超'


CONFIG = dict(
    num=30, title='串联所有单词的子串', difficulty='Hard', category='滑动窗口',
    author='yiduobo', technique='按模 word_len 分组 · 滑动窗口 + 计数 dict',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def findSubstring(self, s, words):
        if not s or not words:
            return []

        word_dict = {}
        for word in words:
            word_dict[word] = word_dict.get(word, 0) + 1

        word_len = len(words[0])
        s_len = len(s)
        max_start_pos = s_len - word_len * len(words)
        res = []

        for index in range(word_len):
            left = index
            right = index
            now_word_dict = {}
            word_cnt = 0
            while left <= max_start_pos and right + word_len <= s_len:
                now_word = s[right : right + word_len]
                right += word_len
                if now_word not in word_dict:
                    now_word_dict = {}
                    left = right
                    word_cnt = 0
                else:
                    word_cnt += 1
                    now_word_dict[now_word] = now_word_dict.get(now_word, 0) + 1
                    while now_word_dict[now_word] > word_dict[now_word]:
                        left_word = s[left : left + word_len]
                        now_word_dict[left_word] -= 1
                        left += word_len
                        word_cnt -= 1

                    if word_cnt == len(words):
                        res.append(left)

        return res
''',
    call=f'Solution().findSubstring({S_IN!r}, {WORDS!r})',
    expect=[0, 2],
    views=[
        dict(type='text', fn=_text, size=26, h=64),
        dict(type='string', var='s', label='s（框 = [left, right)，蓝 = 新读入的词，红 = 被去掉的词）', cell=90, h=230,
             window=('left', lambda S: S['right'] - 1 if _ok(S) and S['right'] > S['left'] else None),
             pointers={'left': 'blue', 'right': 'pink'}, color=_color),
        dict(type='map', var='word_dict', label='word_dict（每个单词需要的个数）', h=100, font=26, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='map', var='now_word_dict', label='now_word_dict（当前窗口里有的词）', h=110, font=26,
             fmt=lambda k, v: f'{k}: {v}'),
    ],
    watch=[('index', 'index', 'purple'), ('left', 'left', 'blue'), ('right', 'right', 'pink'),
           ('word_cnt', 'word_cnt'), ('res', 'res', 'green')],
    skip=['word_dict = {}', 's_len = len(s)', 'res = []', 17, 18, 19, 'for word in words', 'right += word_len',
          'if not s or not words', 'word_dict[word] = word_dict.get', 'word_cnt += 1', 'left_word = s[left', 'word_cnt -= 1'],
    captions={
        'word_len = len': '先数好每个单词需要几个：`word_dict = {word_dict}`；每个词长 `word_len = {word_len}`',
        'max_start_pos = ': '合法起点最大是 `{max_start_pos}`',
        'for index in range': lambda S, B, ret: (
            f'枚举 `p = index = {S.index}`：一次扫描解决所有 ==模 {WL} 等于 {S.index}== 的起点；窗口清空'
            if S.get('index') != B.get('index') or 'index' not in B else '所有余数都扫完了'),
        'left = index': '`left = right = {index}`：窗口 `[left, right)` 为空',
        'while left <= max_start_pos': _cap_while,
        'now_word = s[right': lambda S, B, ret: f'读入下一个词 `"{S.now_word}"`，然后 `right += {WL}`',
        'if now_word not in word_dict': lambda S, B, ret: (
            f'`"{S.now_word}"` ==不在 words 中==：包含它的窗口都不合法' if S.now_word not in S.word_dict
            else f'`"{S.now_word}"` 在 words 中'),
        '                    left = right': '清空 `now_word_dict`，`left` 直接跳到这个词的末尾 `{left}`',
        '                    word_cnt = 0': '`word_cnt = 0`，从头再来',
        'now_word_dict[now_word] = now_word_dict.get': '`"{now_word}"` 进窗口，`word_cnt = {word_cnt}`',
        'while now_word_dict[now_word] >': _cap_shrink,
        'now_word_dict[left_word] -= 1': '去掉左端点的词 `"{left_word}"`：`now_word_dict["{left_word}"]` → {now_word_dict[left_word]}',
        'left += word_len': '`left` 右移到 {left}，`word_cnt` 减一 → {word_cnt - 1}',
        'if word_cnt == len(words)': lambda S, B, ret: (
            f'`word_cnt = {S.word_cnt} == len(words)`：==没有误杀==，窗口正好由所有单词组成' if S.word_cnt == len(S.words)
            else f'`word_cnt = {S.word_cnt}` 还不够 `{len(S.words)}`'),
        'res.append(left)': '找到一个答案：`left = {left}`，`res = {res}`',
        'return res': '返回 =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='起点按模 word_len 分组，每组一趟滑窗：去头一个词、加尾一个词',
        complexity='时间 `O(len(s)·word_len)`（原文含 dict 的 log），空间 `O(m)`',
        problem=['`words` 里的单词==长度相同==；`s` 中由所有单词（任意顺序）拼成的子串叫「串联子串」',
                 '返回所有串联子串在 `s` 中的起始下标',
                 '示例：`s = "barfoothefoobarman"`，`words = ["foo","bar"]` → `[0,9]`',
                 f'本视频：`s = "{S_IN}"`，`words = {WORDS}` → `[0,2]`'],
        quote='二者相比，后面这种情况其实就是==去掉了头部的那个串，加入了尾部的这个串==，因此利用滑动窗口的思想，可以一次扫描解决掉所有模word_len等于p的情况。',
        quote_src='—— yiduobo 题解',
        idea=['新词不在 words 中：清空 dict，`left` 跳到这个词末尾',
              '新词在 words 中但个数超了：==从 left 开始去掉词==，不是这个词也要误杀，直到不超',
              '`word_cnt == len(words)` 说明没有误杀 → `left` 是一个答案'],
        result='`index = 0` 找到 `[0,4)`、`[2,6)`；`index = 1` 遇到 `bb`、`aa` 直接跳过 → `[0,2]` ✓',
        summary=['时间 `O(len(s)·word_len)`：每个词最多进出窗口各一次',
                 '收缩不能「拦腰斩断」：只能从左端点一个词一个词地去掉',
                 '原文为 Python 2 风格，仅删去文档字符串，代码未改',
                 '对比灵神：灵神用 `overload` 计数做定长滑窗；这里是不定长窗口，遇到非法词直接跳'],
    ),
)
