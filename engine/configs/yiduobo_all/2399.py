DIST = [1, 3, 0, 5] + [0] * 22

CONFIG = dict(
    num=2399, title='检查相同字母间的距离', difficulty='Easy', category='字符串',
    author='yiduobo', technique='哈希表记最后位置',
    tags=[],
    code='''
class Solution(object):
    def checkDistances(self, s, distance):

        last_pos = {}
        for index, char in enumerate(s):
            if char in last_pos:
                if index - last_pos[char] - 1 != distance[ord(char) - 97]:
                    return False
            
            last_pos[char] = index
        
        return True
''',
    call=f'Solution().checkDistances("abaccb", {DIST!r})',
    expect=True,
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前字母）', cell=100, h=190, pointers={'index': 'blue'},
             color=lambda S, k, v: 'green' if 'last_pos' in S and v in S['last_pos'] and k < S.get('index', 0) else None),
        dict(type='map', var='last_pos', label='last_pos（字母 → 上次出现的下标）', fmt=lambda k, v: f"'{k}': {v}", h=170, font=34),
        dict(type='text', size=26, h=110,
             fn=lambda S: (f"`{S['char']}` 对应 `distance[{ord(S['char']) - 97}] = {S['distance'][ord(S['char']) - 97]}`；"
                           + (f"实际间隔 `{S['index']} − {S['last_pos'][S['char']]} − 1` = =={S['index'] - S['last_pos'][S['char']] - 1}==" if S['last_pos'].get(S['char']) is not None and S['last_pos'][S['char']] < S['index'] else ('已记下本次位置' if S['last_pos'].get(S['char']) == S['index'] else '第一次见这个字母'))
                           ) if 'char' in S and 'last_pos' in S and 'index' in S else ''),
    ],
    watch=[('index', 'index', 'blue'), ('char', 'char', 'pink')],
    captions={
        'last_pos = {}': '`last_pos` 存每个字母==最后一次==出现的下标',
        'for index, char': lambda S, B, ret: ('遍历完了，没有违反要求' if 'index' in B and S.index == B.index
                                              else f"`index = {S.index}`，字母 `{S.char!r}`"),
        'if char in last_pos': lambda S, B, ret: (f'`{S.char!r}` 已出现过（上次在 {S.last_pos[S.char]}）→ 这是第二次，要检查间隔'
                                                  if S.char in S.last_pos else f'`{S.char!r}` 第一次出现，直接记录位置'),
        'if index - last_pos': lambda S, B, ret: (
            f'间隔 `{S.index} - {S.last_pos[S.char]} - 1` = {S.index - S.last_pos[S.char] - 1}，'
            f'`distance[{ord(S.char) - 97}] = {S.distance[ord(S.char) - 97]}` → '
            + ('==不相等，不是匀整串==' if S.index - S.last_pos[S.char] - 1 != S.distance[ord(S.char) - 97] else '相等，通过')),
        'return False': '有字母间隔不符，直接返回 `False`',
        'last_pos[char] = index': '更新 `last_pos[{char!r}] = {index}`',
        'return True': '`s` 顺利遍历完，返回 `True`',
    },
    cards=dict(
        one_liner='哈希表记每个字母的位置，第二次遇到时核对距离',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['每个字母恰好出现两次，`distance[i]` 是第 i 个字母两次出现之间隔的字母数',
                 '所有出现过的字母都满足才返回 `true`',
                 '示例：`"abaccb"`，`distance = [1,3,0,5,…]` → `true`'],
        quote='可以使用一个哈希表last_pos储存每个字符最后一次出现的位置，然后遍历s。对于当前字符char，若char出现在last_pos中，那么就需要计算当前位置和last_pos[char]之间的距离，并检测这个距离是否符合distance中的规定。',
        quote_src='—— yiduobo 题解',
        idea=['遍历 `s`，`char` 不在 `last_pos` 里 → 第一次出现，只记录',
              '在的话 → 第二次出现，间隔 = `index - last_pos[char] - 1`，与 `distance[ord(char) - 97]` 比较',
              '不符立刻 `False`，遍历完返回 `True`'],
        result='`a`、`b`、`c` 间隔分别是 1、3、0，都符合 → True ✓',
        summary=['时间 `O(n)`，空间 `O(|Σ|)`',
                 '易错：两下标之差还要再 `- 1` 才是中间字母数',
                 '字母编号用 `ord(char) - 97`（`ord("a") = 97`）',
                 '`last_pos[char]` 更新放在比较之后；每个字母只出现两次，所以其实只会比较一次'],
    ),
)
