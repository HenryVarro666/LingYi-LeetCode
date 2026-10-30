def _top(S):
    if 'res' not in S:
        return ''
    return f"当前子串长度 {'—' if S.get('start') is None else S['index'] - S['start'] + 1}，已记录最长美丽子串 `res` = =={S['res']}=="


def _col(S, i, v):
    st = S.get('start')
    if st is None or 'index' not in S:
        return None
    if i == S['index']:
        return 'blue'
    if st <= i < S['index']:
        return 'green' if len(S['char_set']) == 5 else None
    return None


def _dim(S, i, v):
    st = S.get('start')
    return st is not None and 'index' in S and i < st


def _cmp(S, B, r):
    c, l = S.char, S.last
    if c < l:
        return f"`'{c}' < '{l}'` → 顺序倒退了，上一个子串到此结束"
    return f"`'{c}' ≥ '{l}'` → 仍然非降序，子串可以继续延伸"


def _chk(S, B, r):
    if len(S.char_set) == 5:
        if S._line == 21:
            return f'循环结束后检查最后一段：`len(char_set) = 5` → 美丽！长度 `{len(S.word)} − {S.start} = {len(S.word) - S.start}`'
        return f'`len(char_set) = 5` → 五个元音齐了，美丽！长度 `{S.index} − {S.start} = {S.index - S.start}`'
    return f'`len(char_set) = {len(S.char_set)} < 5` → 缺元音（已有 {"".join(sorted(S.char_set))}），不算'


CONFIG = dict(
    num=1839, title='所有元音按顺序排布的最长子字符串', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='非降序分段 · 哈希集合数元音种类',
    tags=['灵神题单', '难度分 1580'],
    code='''
class Solution(object):
    def longestBeautifulSubstring(self, word):

        char_set = set()
        start = None
        last = None
        res = 0

        for index, char in enumerate(word):
            if start is None:
                start = index
            elif char < last:
                if len(char_set) == 5:
                    res = max(res, index - start)
                start = index
                char_set = set()
            
            last = char
            char_set.add(char)
            
        if len(char_set) == 5:
            res = max(res, len(word) - start)
        
        return res
''',
    call='Solution().longestBeautifulSubstring("aeioaeeiouu")',
    expect=7,
    skip=['last = char'],
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='word', label='word（蓝 = 当前字符；起点之前变暗；元音齐了则当前段变绿）', cell=84,
             pointers={'index': 'pink'}, window=('start', 'index'), color=_col, dim=_dim),
        dict(type='set', var='char_set', label='char_set（当前非降序子串里出现过的元音）', fmt=lambda x: str(x)),
        dict(type='text', fn=lambda S: (f"上一个字符 `last = {S['last']!r}`，起点 `start = {S['start']}`" if 'last' in S else ''), size=26),
    ],
    watch=[('index', 'index', 'pink'), ('char', 'char', 'blue'), ('start', 'start', 'orange'), ('res', 'res', 'green')],
    captions={
        4: '`char_set`：收集当前子串里出现过的元音',
        'start = None': '`start`：当前子串的起点，还没开始',
        'last = None': '`last`：上一个字符',
        'res = 0': '`res` 记最长美丽子串长度，没有就是 0',
        'for index, char': lambda S, B, r: ('字符都扫完了，循环结束' if B.get('index') == S.index and 'index' in B
                                           else f"扫到 `word[{S.index}] = '{S.char}'`"),
        'if start is None': lambda S, B, r: ('`start` 还是 None → 这是第一个字符' if B.get('start') is None
                                             else '`start` 已经有了，不是第一个字符，去比较和上一个字符'),
        11: '第一个字符：子串从这里开始，`start = {start}`',
        'elif char < last': _cmp,
        'if len(char_set) == 5': _chk,
        'res = max': '用这个子串的长度更新答案：`res = {res}`',
        15: '顺序倒退 → 新子串从当前位置开始：`start = {start}`',
        16: '集合清空，重新收集（当前字符稍后加入）',
        'char_set.add': '加入集合：`char_set = {sorted(char_set)}`（{len(char_set)} 种）',
        'res = max(res, len(word)': '最后一个子串也要检查！长度 `{len(word)} − {start}` → `res = {res}`',
        'return res': '最长美丽子串长度 `{ret}`',
    },
    cards=dict(
        one_liner='非降序的段里数元音种类，凑齐 5 种就是美丽子串',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['美丽字符串：==五个元音都至少出现一次==，且按字典序 a→e→i→o→u 排列',
                 '`word` 只含元音，求最长美丽子串长度，没有则为 0',
                 '示例：`"aeiaaioaaaaeiiiiouuuooaauuaeiu"` → `13`',
                 '本视频：`"aeioaeeiouu"` → `7`'],
        quote='题目要求的子字符串需要满足单调性，并包含全部五种字符。由于是子字符串，因此在处理单调性上可以直接一趟遍历，对比相邻字符的大小。',
        quote_src='—— yiduobo 题解原文',
        idea=['相邻字符一旦倒退（`char < last`），当前的非降序子串就断了',
              '遍历时用集合收集字符，`len == 5` 说明五个元音都出现过',
              '断开时检查上一段是否美丽并更新答案，然后清空集合重新开始',
              '循环结束后==还要检查最后一段=='],
        summary=['时间 `O(n)`，空间 `O(1)`（集合最多 5 个元素）',
                 '易错：循环后最后一段没有“倒退”触发检查，要再判断一次',
                 '非降序 + 五种齐 ⇒ 必然是 a…e…i…o…u 的形式',
                 '长度是 `index - start`（段在 index 之前结束）与 `len(word) - start`（到末尾）',
                 '原文已是可直接运行的写法，没有改动'],
    ),
)
