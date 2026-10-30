def _top(S):
    if 'rest' in S and S.get('_line', 0) >= 14:
        return f"频次 = `{S['ma']}` 的字母集合：`{sorted(S['rest'])}`，按 `last` 排序后拼接"
    if 'ma' in S:
        return f"最大频次 `ma = {S['ma']}`：倒数第二轮剩下的就是这些字母"
    return '一趟遍历同时记：每个字母的出现次数 `freq` 和最后位置 `last`'


CONFIG = dict(
    num=3039, title='进行操作使字符串为空', difficulty='Medium', category='字符串',
    author='yiduobo', technique='频次 + 最后位置，排序',
    tags=[],
    code='''
class Solution(object):
    def lastNonEmptyString(self, s):

        freq = Counter()
        last = {}
        for index, char in enumerate(s):
            freq[char] += 1
            last[char] = index
        ma = max(freq.values())

        rest = set()
        for char in freq:
            if freq[char] == ma:
                rest.add(char)
        
        return ''.join(sorted(list(rest), key=lambda d:last[d]))
''',
    call='Solution().lastNonEmptyString("aabcbbca")',
    expect='ba',
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='s', label='s（蓝 = 当前遍历到的位置）', cell=84, pointers={'index': 'blue'},
             color=lambda S, k, v: 'green' if ('rest' in S and v in S['rest'] and k == S['last'][v]) else None),
        dict(type='map', var='freq', label='freq：字母 → 出现次数', h=150),
        dict(type='map', var='last', label='last：字母 → 最后出现的下标', h=150),
        dict(type='set', var='rest', label='rest：频次最大的字母', h=110),
    ],
    watch=[('index', 'index'), ('char', 'char', 'blue'), ('ma', 'ma', 'green')],
    captions={
        'freq = Counter': '准备两个表：`freq` 记次数，`last` 记最后一次出现的位置',
        'for index, char': '遍历 s：`index = {index}`，`char = {char!r}`',
        'freq[char] += 1': '`{char!r}` 出现次数 → `{freq[char]}`',
        'last[char] = index': '`last[{char!r}] = {index}`：后来的覆盖前面的，最终留下==最后一次==位置',
        'ma = max': '每轮每种字母只删一个，次数最多的撑到最后：`ma = {ma}`',
        'for char in freq': '检查字母 `{char!r}`：次数 `{freq[char]}`',
        'if freq[char] == ma': lambda S, B, ret: (f"`freq[{S.char!r}] = {S.freq[S.char]}` == `ma = {S.ma}` → ==它会留到最后一轮==" if S.freq[S.char] == S.ma
                                                  else f"`freq[{S.char!r}] = {S.freq[S.char]}` < `ma = {S.ma}` → 前面几轮就删光了"),
        'rest.add': '加入候选集：`rest = {rest}`',
        'return': '候选字母按 `last` 从小到大排，还原它们在原串里的相对顺序 → =={ret!r}==',
    },
    cards=dict(
        one_liner='倒数第二轮剩下的，必是频次最大字母的最后一个',
        complexity='时间 `O(n + k log k)`，空间 `O(k)`，k 为字母种类数',
        problem=['每轮从 a 到 z，各删掉出现位置最早的一个',
                 '求最后一次操作前的字符串',
                 '示例：`"aabcbbca"` → `"ba"`'],
        quote='由于题目每轮操作都会移除每种字符各一个，因此倒数第二轮剩下的必然是出现次数最多的字符。另一方面，由于移除的操作使从前往后进行的，因此倒数第二轮剩下的字符必然是其所有出现位置中最靠后的那个。',
        quote_src='—— yiduobo 题解',
        idea=['先推结论：每轮删一个，剩到最后的字母 = 频次最大者',
              '从前往后删，所以留下的是最靠后的那个位置',
              '答案里的相对顺序，就看各字母 `last` 的大小'],
        result='`a`、`b` 频次都是 3，`last[b] = 5 < last[a] = 7` → `"ba"` ✓',
        summary=['一趟遍历，时间 `O(n)`，再对至多 26 个字母排序',
                 '易错：`last` 要不断覆盖取最后位置；不要用第一次出现',
                 '最后别忘了按 `last` 排序，而不是按字母表顺序',
                 '原文用了 `Counter`，Python 3 直接可用'],
    ),
)
