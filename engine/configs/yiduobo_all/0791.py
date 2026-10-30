def _fn(S):
    if 'order_dict' not in S:
        return '按 `S` 里字符出现的先后给 `T` 排序，`S` 里没有的字符放最前面'
    return f"`res` = =={S.get('res', '')!r}==（不在 S 中）　`char_list` = =={''.join(S.get('char_list', []))!r}==（待排序）"


CONFIG = dict(
    num=791, title='自定义字符串排序', difficulty='Medium', category='字符串',
    author='yiduobo', technique='下标字典 + 自定义排序',
    tags=[],
    code='''
class Solution(object):
    def customSortString(self, S, T):

        order_dict = {}
        for index, char in enumerate(S):
            order_dict[char] = index
        
        res = ''
        char_list = []
        for char in T:
            if char not in order_dict:
                res += char
            else:
                char_list.append(char)
        
        return res + ''.join(sorted(char_list, key=lambda d:order_dict[d]))
''',
    call="Solution().customSortString('cba', 'abxcd')",
    expect='xdcba',
    views=[
        dict(type='string', var='S', label='S（顺序）', h=130, cell=70),
        dict(type='map', var='order_dict', label='order_dict：字符 → 顺序', h=150),
        dict(type='string', var='T', label='T', h=150, cell=70, pointers={}),
        dict(type='text', fn=_fn, size=26, h=60),
    ],
    watch=['char', ('res', 'res', 'green')],
    captions={
        'order_dict[char] = index': '记下字符 `{char}` 在 S 中的位置：`order_dict[{char!r}] = {index}`',
        'res = \'\'': '`res` 存 S 里没有的字符，它们顺序随意，直接放最前面',
        'char_list = []': '`char_list` 存 S 里有的字符，稍后排序',
        'for char in T': '看 T 的字符 `{char}`',
        'if char not in': lambda S, B, r: (f"`{S.char}` 不在 order_dict 里 → 不受 S 约束" if S.char not in S.order_dict
                                           else f"`{S.char}` 在 order_dict 里，顺序号 `{S.order_dict[S.char]}`"),
        'res += char': '不在 S 中 → 直接拼到 `res`：=={res!r}==',
        'char_list.append': '在 S 中 → 先收进 `char_list`：=={char_list}==',
        'return res': '`res` 接上排好序的 `char_list` → =={ret!r}==',
    },
    cards=dict(
        one_liner='不在 S 里的直接放，在 S 里的按下标排序',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`S` 中的字符互不相同，规定了字符的先后顺序',
                 '把 `T` 重排，使其中出现在 `S` 里的字符按 `S` 的顺序排列，其余字符位置任意',
                 '示例：`S="cba", T="abcd"` → `"cbad"`；本视频 `T="abxcd"`'],
        quote='对于T中的每个字符，若其没有出现在S中，那么就直接将该字符加入到答案中，否则将该字符加入到一个list中。',
        quote_src='—— yiduobo 题解原文',
        idea=['先扫 `S`，用字典记下每个字符的下标',
              '扫 `T`：不在字典里的拼到 `res`，在的放进 `char_list`',
              '`char_list` 用 `sorted(key=下标)` 排序，再接到 `res` 后面'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '不在 S 中的字符放前面或后面都合法',
                 '重复字符会在 `char_list` 里保留，不会丢',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行'],
    ),
)
