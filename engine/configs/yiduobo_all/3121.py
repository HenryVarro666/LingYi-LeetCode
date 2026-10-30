def _mapview(S):
    return ''


CONFIG = dict(
    num=3121, title='统计特殊字母的数量 II', difficulty='Medium', category='位运算',
    author='yiduobo', technique='哈希表 · 最后小写 < 首个大写', tags=[],
    code='''
class Solution(object):
    def numberOfSpecialChars(self, word):

        last = {}
        first = {}
        for index, char in enumerate(word):
            if 'a' <= char <= 'z':
                last[char] = index
            elif char not in first:
                first[char] = index

        res = 0
        for char in last:
            if first.get(chr(ord(char) - 32), -1) > last[char]:
                res += 1
        
        return res
''',
    call='Solution().numberOfSpecialChars("abAbaBcC")',
    expect=2,
    views=[
        dict(type='string', var='word', h=210, cell=100, pointers={'index': 'blue'}),
        dict(type='map', var='last', label='last：小写字母最后一次出现的下标', h=170),
        dict(type='map', var='first', label='first：大写字母第一次出现的下标', h=170),
    ],
    watch=[('index', 'index', 'blue'), ('char', 'char', 'cyan'), ('res', 'res', 'green')],
    captions={
        'for index, char': lambda S, B, r: ('第一趟遍历完' if S.index == B.get('index') and S.index == len(S.word) - 1 else f'读到下标 `{S.index}` 的字符 `{S.char}`'),
        "'a' <= char <= 'z'": lambda S, B, r: f"`{S.char}` {'是小写 → 每次都覆盖，最后留下的就是最后一次出现' if 'a' <= S.char <= 'z' else '是大写'}",
        'last[char] = index': '`last[{char}]` = {index}：小写 `{char}` 目前最后出现在下标 {index}',
        'elif char not in first': lambda S, B, r: f"大写 `{S.char}` {'还没记过 → 这是它第一次出现' if S.char not in S['first'] else '已经记过了 → 只保留第一次，不更新'}",
        'first[char] = index': '`first[{char}]` = {index}：大写 `{char}` 第一次出现在下标 {index}',
        'res = 0': '两张表记完。判定：==最后一个小写的下标 < 第一个大写的下标==',
        'for char in last': lambda S, B, r: ('last 遍历完' if S.char == B.get('char') else f'检查小写 `{S.char}`，它最后出现在下标 {S["last"][S.char]}'),
        'if first.get': lambda S, B, r: (lambda up, f: f"大写 `{up}` 第一次出现在 {f if f >= 0 else '无（-1）'}，最后小写在 {S['last'][S.char]}：" + ('大写更靠后 → 小写都在大写前，特殊' if f > S['last'][S.char] else '大写不在后面 → 不特殊'))(chr(ord(S.char) - 32), S['first'].get(chr(ord(S.char) - 32), -1)),
        'res += 1': '`{char}` 满足条件，`res` → =={res}==',
        'return': '特殊字母共 ==`{ret}`== 个',
    },
    cards=dict(
        one_liner='所有小写都在首个大写前 ⇔ 最后小写下标 < 首个大写下标',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['小写、大写都出现，且==每个小写都在第一个大写之前==的字母，才是特殊字母', '返回特殊字母的数量',
                 '示例：`"abAbaBcC"` → `2`（b、c 特殊；a 的最后一个小写在大写 A 之后，不算）'],
        quote='若所有小写形式都出现在第一个大写形式之前，就相当于其最后一个小写形式的下标小于第一个大小形式的下标。',
        quote_src='—— yiduobo 题解原文',
        idea=['把「所有小写在大写前」转成两个下标的比较', '`last` 记每个小写最后一次出现，`first` 记每个大写第一次出现',
              '遍历 `last`：对应大写在 `first` 中且下标更大 → 答案加 1'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`first.get(..., -1)`：大写没出现时给 -1，一定不大于 last 下标',
                 '大写只记第一次（`elif char not in first`），小写则每次覆盖',
                 '对比灵神：灵神用状态机/位集合在线判断；这里先记下标，最后比大小'],
    ),
)
