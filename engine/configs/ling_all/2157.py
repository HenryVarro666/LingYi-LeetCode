WORDS = ["a", "b", "ab", "cde", "ba"]


def _L(m):
    return ''.join(chr(97 + i) for i in range(26) if m >> i & 1) or '∅'


def _bits(m):
    return '{' + ','.join(chr(97 + i) for i in range(26) if m >> i & 1) + '}'


def _info(S):
    if 'groups' not in S:
        return ''
    g, mx = S['groups'], S.get('max_size', 0)
    return f'当前 ==组数 {g}==，最大组 ==大小 {mx}=='


def _pair(S):
    if 'fa' not in S or 'x' not in S or 'y' not in S or not isinstance(S.get('y'), int):
        return ''
    if S['_line'] in (2, 3, 4):
        return ''
    return f"正在合并：`{_L(S['x'])}` 与 `{_L(S['y'])}`（字母集合相差一次 添加 / 删除 / 替换）"


CONFIG = dict(
    num=2157, title='字符串分组', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='位运算 · 并查集（哈希表）',
    tags=['七、并查集', '§7.2 进阶', '难度分 2499'],
    code='''
class Solution:
    def groupStrings(self, words: List[str]) -> List[int]:
        # 并查集模板（哈希表写法）
        fa, size = {}, defaultdict(int)
        groups, max_size = len(words), 0
        def find(x: int) -> int:
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]
        def merge(x: int, y: int):
            nonlocal groups, max_size
            if y not in fa:
                return
            x, y = find(x), find(y)
            if x == y:
                return
            fa[x] = y
            size[y] += size[x]
            max_size = max(max_size, size[y])  # 维护答案
            groups -= 1

        for word in words:
            x = 0
            for ch in word:
                x |= 1 << (ord(ch) - ord('a'))  # 计算 word 的二进制表示
            fa[x] = x  # 添加至并查集
            size[x] += 1
            max_size = max(max_size, size[x])  # 维护答案
            if size[x] > 1:
                groups -= 1

        for x in fa:  # 枚举所有字符串（二进制表示）
            for i in range(26):
                merge(x, x ^ (1 << i))  # 添加或删除字符 i
                if (x >> i) & 1:
                    for j in range(26):
                        if ((x >> j) & 1) == 0:
                            merge(x, x ^ (1 << i) | (1 << j))  # 替换字符 i 为 j
        return [groups, max_size]
''',
    call=f'Solution().groupStrings({WORDS})',
    expect=[2, 4],
    views=[
        dict(type='array', var='words', label='words（每个字符串 = 一个 26 位二进制数 = 一个字母集合）', cell=90, h=165),
        dict(type='map', var='fa', label='fa：集合 → 父亲（并查集，键值都显示成字母集合）', fmt=lambda k, v: f'{_L(k)} → {_L(v)}', h=120),
        dict(type='map', var='size', label='size：集合 → 这个集合代表的组里有多少字符串', fmt=lambda k, v: f'{_L(k)} : {v}', h=120),
        dict(type='text', fn=_info, size=30),
        dict(type='text', fn=_pair, size=28),
    ],
    watch=[('groups', 'groups', 'green'), ('max_size', 'max_size', 'orange'), ('x', 'x', 'blue'), ('y', 'y', 'pink')],
    skip=['fa, size = {}', 'def find', 'def merge', 'nonlocal', 'for ch in word', 'x = 0', 'if y not in fa', 'x, y = find(x)',
          'if x == y', 'if fa[x] != x', 'return fa[x]', 'for i in range(26)', 'merge(x, x', 'if (x >> i)', 'for j in range(26)',
          'if ((x >> j)', 13, 16],
    captions={
        'groups, max_size = len(words), 0': '先假设每个字符串各成一组：`groups = {groups}`，最大组 `max_size = 0`',
        'for word in words': '取下一个字符串，把它变成二进制数',
        'x |= 1 <<': lambda S, B, r: f'字母 `{S.ch}` 对应第 `{ord(S.ch) - 97}` 位：`x` = 集合 `{_L(S.x)}`（二进制 `{bin(S.x)}`）',
        'fa[x] = x': lambda S, B, r: f'集合 `{_L(S.x)}` 加入并查集，自己是代表元',
        'size[x] += 1': lambda S, B, r: f'`size[{_L(S.x)}] = {S.size[S.x]}`：这个集合出现的次数',
        'max_size = max(max_size, size[x])  #': '更新最大组：`max_size = {max_size}`',
        'if size[x] > 1': lambda S, B, r: (f'`size = {S.size[S.x]} > 1`：集合 `{_L(S.x)}` 重复出现，字符串相同必然同组' if S.size[S.x] > 1
                                           else '第一次出现，不用减'),
        30: '重复的字符串不算新的一组：`groups` 减 1 → ==`{groups}`==',
        'for x in fa': '枚举每个集合 `x`：试 26 个字母的 加 / 删 / 换，命中 `fa` 才合并',
        'fa[x] = y': lambda S, B, r: f'两边的代表元 `{_L(B.x)}`、`{_L(B.y)}` 不同 → 两个组相关，合并：`fa[x] = y`',
        8: '路径压缩：找到代表元后，让 `fa[x]` 直接指向它',
        'size[y] += size[x]': lambda S, B, r: f'合并 `size`：`size[{_L(S.y)}] = {S.size[S.y]}`',
        'max_size = max(max_size, size[y])': '组变大了，更新最大组：`max_size = {max_size}`',
        20: '两个组并成一个，`groups` 减 1 → ==`{groups}`==',
        'return [groups': '组数 `{groups}`，最大组 `{max_size}` → 返回 `[{groups}, {max_size}]`',
    },
    cards=dict(
        one_liner='字母集合压成二进制，枚举 加 / 删 / 换 找邻居并查集合并',
        complexity='时间 `O(n·U^2)`（U=26），空间 `O(n)`',
        problem=['`words` 每个字符串字母互不重复；字母集合经 ==添加 / 删除 / 替换一个字母== 能变成另一个，就「关联」',
                 '关联的字符串必须同组，求总组数和最大组的大小',
                 '示例：`["a","b","ab","cde"]` → `[2,3]`',
                 '本视频：`["a","b","ab","cde","ba"]` → `[2,4]`'],
        quote='字符串不含重复字母且只由小写字母组成，我们可以用一个二进制数来表示字符串，二进制数的第 i 位为 1 则表示第 i 个小写字母出现在 s 中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['字符串 -> 26 位整数，`"ab"` 与 `"ba"` 是同一个数',
              '枚举每个数的 加 / 删 / 换 得到 `t`，`t` 在 words 里就用并查集合并',
              '合并时顺便维护组数 `groups` 和最大组 `max_size`，不用最后再统计',
              '注意：并查集的键是二进制数，不是下标（哈希表写法）'],
        summary=['时间 `O(n·U^2)`，`U = 26`；空间 `O(n)`',
                 '易错：重复字符串集合相同，先让 `size` 记次数，并在 `groups` 里减掉重复的',
                 '合并前先判断 `y not in fa`，不在 words 里的集合不能合并',
                 '视频里 26 次枚举里没有命中的不再逐步展示，只演示真正发生的合并'],
    ),
)
