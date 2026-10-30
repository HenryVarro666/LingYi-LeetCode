CONFIG = dict(
    num=1624, title='两个相同字符之间的最长子字符串', difficulty='Easy', category='字符串',
    author='yiduobo', technique='哈希表记首次位置',
    code='''
class Solution(object):
    def maxLengthBetweenEqualCharacters(self, s):
        last_pos = {}
        res = -1
        for index, char in enumerate(s):
            if char not in last_pos:
                last_pos[char] = index
            else:
                dis = index - last_pos[char] - 1
                res = max(dis, res)
        
        return res
''',
    call="Solution().maxLengthBetweenEqualCharacters('cabbac')",
    expect=4,
    views=[
        dict(type='string', var='s', pointers={'index': 'blue'}, h=200, cell=90,
             color=lambda S, i, v: ('green' if 'last_pos' in S and S['last_pos'].get(v) == i else None)),
        dict(type='map', var='last_pos', h=230, label='last_pos（字符 → 首次出现的位置）'),
        dict(type='text', fn=lambda S: (f"当前最长间隔 `res = {S['res']}`" if 'res' in S else ''), size=28),
    ],
    watch=[('index', 'index', 'blue'), 'char', 'dis', ('res', 'res', 'green')],
    captions={
        'last_pos = {}': '哈希表：字符 → ==首次出现==的下标',
        'res = -1': '`res = -1`：没有重复字符时返回 -1',
        'for index, char in enumerate(s)': '扫描到 `s[{index}] = {char!r}`',
        'if char not in last_pos': lambda S, B, r: (f'`{S.char!r}` 还没出现过 → 记下首次位置' if S.char not in S.last_pos else f'`{S.char!r}` 之前出现过（首次在 {S.last_pos[S.char]}）→ 可以算间隔'),
        'last_pos[char] = index': '记录 `{char!r}` 首次位置为 `{index}`，之后不再覆盖',
        'dis = index - last_pos[char] - 1': '两个相同字符之间的长度 = `{index} - {last_pos[char]} - 1` = =={dis}==',
        'res = max(dis, res)': '`res = max({dis}, {B.res}) = {res}`',
        'return res': '扫描结束，最长间隔为 `{ret}`',
    },
    cards=dict(
        one_liner='只记首次位置，后面每遇到重复就算一次间隔',
        complexity='时间 `O(n)`，空间 `O(字符集)`',
        problem=['给字符串 `s`，找两个相同字符之间的最长子字符串长度（不含这两个字符）',
                 '不存在相同字符返回 `-1`',
                 '示例：`"cabbac"` → `4`（两个 c 之间是 `abba`）'],
        quote='直接一趟扫描，记录每个字符首次出现的位置，并使用当前位置与该字符首次出现位置之间的差来更新答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['同一字符的间隔以==最早==出现的位置算最长',
              '所以只在第一次见到字符时写入哈希表，之后只读不改',
              '后面每次重复都用 `index - 首次位置 - 1` 去更新答案'],
        summary=['时间 `O(n)`，空间 `O(字符集)`',
                 '易错：长度要再 `- 1`，因为不含两端的字符',
                 '不能用最近一次的位置覆盖，否则会漏掉更长的间隔',
                 '没有重复字符时 `res` 保持初始的 `-1`'],
    ),
)
