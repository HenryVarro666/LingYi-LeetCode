CONFIG = dict(
    num=820, title='单词的压缩编码', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='长词优先 + 后缀哈希集合',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution(object):
    def minimumLengthEncoding(self, words):

        words = sorted(words, key=lambda d:len(d), reverse=True)
        suffix_set = set()
        res = 0
        for word in words:
            if word not in suffix_set:
                res += len(word) + 1
                tmp = ''
                for char in word[::-1]:
                    tmp = char + tmp
                    suffix_set.add(tmp)
        
        return res
''',
    call='Solution().minimumLengthEncoding(["time", "me", "bell", "ell"])',
    expect=10,
    views=[
        dict(type='array', var='words', label='words（执行完排序后：从长到短）', cell=130, h=240,
             color=lambda S, i, v: ('yellow' if v == S.get('word') and 'word' in S else None)),
        dict(type='set', var='suffix_set', label='suffix_set（已保留的词的所有后缀）', fmt=lambda x: x, h=210, font=28),
        dict(type='text', h=90, size=32,
             fn=lambda S: ('已保留的编码长度 `res = %d`（每个词占 长度+1，含一个 `#`）' % S['res']) if 'res' in S
             else '长词不会是短词的后缀；先处理长词，短词若是它的后缀就可以省掉'),
    ],
    watch=[('word', 'word', 'yellow'), ('tmp', 'tmp', 'blue'), ('res', 'res', 'green')],
    captions={
        'words = sorted': '按长度从长到短排序：`{words}`；只可能短词是长词的后缀',
        'suffix_set = set()': '`suffix_set` 记录所有已保留单词的后缀，先是空集合',
        'res = 0': '`res` 累计编码总长度',
        'for word in words': lambda S, B, ret: ('所有单词处理完毕' if ('word' in B and B.word == S.word)
                                               else f'取下一个单词 `{S.word}`'),
        'if word not in suffix_set': lambda S, B, ret: (
            f'`{S.word}` 在 `suffix_set` 里吗？' + ('不在 → ==必须单独保留==' if S.word not in S.suffix_set
                                                    else '在 → 它是某个长词的后缀，==直接跳过==')),
        'res += len(word) + 1': '保留 `{word}`：编码里占 `len + 1 = {len(word) + 1}`（末尾加 `#`），`res` = =={res}==',
        "tmp = ''": '`tmp` 用来拼后缀，从空串开始',
        'for char in word[::-1]': lambda S, B, ret: (f'`{S.word}` 的字符取完了，后缀都已入集合' if S.tmp == S.word
                                                    else f'从末尾往前取字符 `{S.char!r}`'),
        'tmp = char + tmp': '后缀变长一位：`tmp` = `{tmp}`',
        'suffix_set.add(tmp)': '把后缀 `{tmp}` 加进集合，以后遇到它就知道可以省略',
        'return res': '返回最短编码长度 `{ret}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='长词能“吃掉”它所有的后缀词，把后缀都记进集合',
        complexity='时间 `O(L²)`（L 为单词长度，生成后缀），空间 `O(总长度²)`',
        problem=['给一个单词列表 `words`，把它们编码成一个字符串 `s`，每个词以 `#` 结尾',
                 '一个词只要是 `s` 中某个词的后缀，就不必单独写出来，求 `s` 的最短长度',
                 '本视频：`["time","me","bell","ell"]` → `time#bell#`，长度 10'],
        quote='若其中一个是另一个的后缀，那么就可以只保留较长的那个单词。……将单词按长度从长到短进行排序，然后逐个遍历。若该单词在哈希表中，那么就跳过，否则将答案加上当前单词长度加一，然后从末尾往前遍历单词中的每个字符，将单词的所有后缀加入到哈希表中。',
        quote_src='—— yiduobo 题解',
        idea=['只有短词才可能是长词的后缀，所以==从长到短==处理',
              '遇到一个词不在集合里：它必须保留，答案加 `len+1`',
              '然后把它的所有后缀（`e`、`me`、`ime`、`time`）都放进集合，之后的短词一查便知'],
        summary=['时间 `O(L²)`：每个词要生成所有后缀；空间同阶',
                 '==必须先按长度从长到短排序==，否则短词先保留了，后面还得回头扣除',
                 '另一种写法：把单词倒转后用字典树，思路相同'],
    ),
)
