def _sig(s):
    d, out = {}, []
    for c in s:
        d.setdefault(c, len(d))
        out.append(d[c])
    return out


def _match(S, B, r):
    sg = _sig(S.word)
    if sg == S.pattern_list:
        return f'`{S.word}` 转成 `{sg}` == `{S.pattern_list}` → ==结构相同，匹配=='
    return f'`{S.word}` 转成 `{sg}` ≠ `{S.pattern_list}` → 结构不同，跳过'


CONFIG = dict(
    num=890, title='查找和替换模式', difficulty='Medium', category='字符串',
    author='yiduobo', technique='字符串转成出现顺序编号再比较',
    tags=[],
    code='''
class Solution(object):
    def findAndReplacePattern(self, words, pattern):

        pattern_list = self.get_list(pattern)

        res = []
        for word in words:
            if self.get_list(word) == pattern_list:
                res.append(word)
        
        return res

    def get_list(self, s):
        num_dict = {}
        now = 0
        ret = []
        for char in s:
            if char not in num_dict:
                num_dict[char] = now
                now += 1
            ret.append(num_dict[char])
        
        return ret
''',
    call='Solution().findAndReplacePattern(["abc", "mee", "aqq", "ccc"], "abb")',
    expect=['mee', 'aqq'],
    views=[
        dict(type='array', var='words', h=170, label='words（黄 = 当前 word，绿 = 已匹配）',
             color=lambda S, i, v: 'green' if v in S.get('res', []) else ('yellow' if S.get('word') == v else None)),
        dict(type='array', var='pattern_list', h=170, label='pattern_list（pattern 的编号串）'),
        dict(type='string', var='s', h=170, label='正在转换的字符串 s', pointers={}),
        dict(type='map', var='num_dict', h=190, label='num_dict：字符 → 第几个出现的字符', fmt=lambda k, v: f'{k} → {v}'),
        dict(type='array', var='ret', h=170, label='ret：转换结果'),
    ],
    watch=['word', 'char', 'now', ('res', 'res', 'green')],
    captions={
        'pattern_list = self': '先把 `pattern` 转成数字串：进入 `get_list`，不直接比字符',
        'num_dict = {}': '`num_dict` 记录每个字符第一次出现时分到的编号',
        'now = 0': '`now` = 已经出现过的不同字符个数，也是下一个新字符的编号',
        'for char in s': '看 `s` 的下一个字符 `{char}`',
        'if char not in num_dict': lambda S, B, r: (f'`{S.char}` 之前没出现过 → 要给它分一个新编号 `{S.now}`' if S.char not in S.num_dict else f'`{S.char}` 出现过，沿用旧编号 `{S.num_dict[S.char]}`'),
        'num_dict[char] = now': '建立映射 `{char} → {now}`',
        'now += 1': '下次的新字符编号加一：`now` = {now}',
        'ret.append': '把 `{char}` 的编号 `{num_dict[char]}` 追加到 `ret`',
        'return ret': '字符串 `{s}` 转成了数字串 `{ret}`',
        'res = []': '`res` 存放匹配成功的单词',
        'for word in words': '检查下一个单词 `{word}`',
        'if self.get_list(word)': _match,
        'res.append(word)': '`{word}` 加入答案：`res` = {res}',
        'return res': '所有结构和 `{pattern}` 相同的单词：`{res}`',
    },
    cards=dict(
        one_liner='不两两比字符，把字符串都转成「出现顺序编号」再比',
        complexity='时间 `O(n·L)`，空间 `O(L)`（n 个单词，每个长 L）',
        problem=['给定单词列表 `words` 和模式 `pattern`，返回能和 `pattern` 匹配的单词',
                 '匹配：存在字母的一一映射，把 `pattern` 的每个字母换掉就得到该单词',
                 '示例：`words = [abc,mee,aqq,ccc]`，`pattern = abb` → `[mee, aqq]`'],
        quote='直觉上不应该两两比较pattern以及word中的字符串，而是应该将pattern和word中的字符都转化为某种相似的结构然后进行比较。',
        quote_src='—— yiduobo 题解原文',
        idea=['从左往右扫，新字符分配 `now` 作编号，`now` 再加一',
              '`abb` → `[0,1,1]`，`mee` → `[0,1,1]`：编号串相同就是同一种结构',
              '编号串相同，等价于字母之间存在一一映射'],
        summary=['时间 `O(n·L)`，空间 `O(L)`',
                 '`ccc` → `[0,0,0]`：不同位置必须对应不同字母，编号串自然保证了双射',
                 '不用单独检查映射是否重复，转换成编号串后一次比较就够',
                 '原文为 Python 2 风格，代码无需修改，直接可在 Python 3 运行'],
    ),
)
