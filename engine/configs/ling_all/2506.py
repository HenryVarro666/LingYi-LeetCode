_P = 'sum(cnt.values()) - (_line == 10) if _line != 11 else None'


def _letters(m):
    return '{' + ','.join(chr(97 + i) for i in range(26) if m >> i & 1) + '}'


def _txt(S):
    if 'mask' not in S or S.get('_line') in (5, 11):
        return '把字符串看成==字母集合==，压缩成二进制数 `mask`'
    m = S['mask']
    return f"`mask = {m:b}`（二进制）= 集合 =={_letters(m)}=="


CONFIG = dict(
    num=2506, title='统计相似字符串对的数目', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右，维护左 · 位运算压缩集合',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution:
    def similarPairs(self, words: List[str]) -> int:
        ans = 0
        cnt = defaultdict(int)
        for s in words:
            mask = 0  # 初始化一个空的集合
            for c in s:
                mask |= 1 << (ord(c) - ord('a'))  # 把 c 加到集合中
            ans += cnt[mask]
            cnt[mask] += 1
        return ans
''',
    call='Solution().similarPairs(["aba","ab","cab","bca","b"])',
    expect=2,
    views=[
        dict(type='array', var='words', label='words（s = 当前字符串）', pointers={_P: 'blue'}, pointer_labels={_P: 's'}, h=210,
             cell=110, dim=lambda S, i, v: 'cnt' in S and S.get('_line') != 11 and i > sum(S['cnt'].values()) - (S.get('_line') == 10)),
        dict(type='text', fn=_txt, h=100, size=32),
        dict(type='map', var='cnt', label='cnt：mask（字母集合）→ 出现次数', fmt=lambda k, v: f'{_letters(k)}: {v}', h=170, font=34),
    ],
    watch=[('s', 's', 'blue'), 'c', ('mask', 'mask', 'orange'), ('ans', 'ans', 'green')],
    skip=['for c in s'],
    captions={
        'ans = 0': '`ans` 统计相似字符串对',
        'cnt = defaultdict': '`cnt[mask]`：左边字母集合为 `mask` 的字符串个数',
        'for s in words': lambda S, B, r: (f'枚举右边的字符串 `s = {S.s!r}`' if sum(S.cnt.values()) < len(S.words) else '遍历结束'),
        'mask = 0': '`mask = 0`：空集合',
        'mask |= 1 <<': lambda S, B, r: (f"把 `{S.c!r}` 加入集合：第 `{ord(S.c) - 97}` 位置 1 → `mask = {S.mask:b}`" if S.mask != B.mask
                                         else f"`{S.c!r}` 已在集合中，`mask` 不变（重复字母不影响）"),
        'ans += cnt[mask]': lambda S, B, r: (f'左边有 `{S.cnt[S.mask]}` 个字符串的集合也是 {_letters(S.mask)} → `ans = {S.ans}`' if S.cnt[S.mask]
                                             else f'左边还没有集合为 {_letters(S.mask)} 的字符串'),
        'cnt[mask] += 1': lambda S, B, r: f'==先查后加==，不会把自己配成一对：集合 {_letters(S.mask)} 的计数 → `{S.cnt[S.mask]}`',
        'return ans': '一共 `{ans}` 对',
    },
    cards=dict(
        one_liner='把字母集合压成二进制 mask，同 mask 的字符串就相似',
        complexity='时间 `O(L)`，空间 `O(n)`，`L` 为总长度',
        problem=['两个字符串由==相同的字符集合==组成，就称它们相似',
                 '求 `i < j` 且 `words[i]`、`words[j]` 相似的下标对数',
                 '示例：`["aba","aabb","abcd","bac","aabc"]` → `2`'],
        quote='把字符串 s 中出现过的字母视作一个集合，把这个集合压缩成一个二进制数 mask。其中 mask 第 i 位为 1 表示第 i 个小写字母在 s 中，为 0 表示不在。',
        quote_src='—— 灵茶山艾府题解',
        idea=['相似 ⇔ ==mask 相等==，问题变成 1512. 好数对的数目',
              '遍历时用 `cnt` 维护左边每个 mask 的出现次数',
              '先把 `cnt[mask]` 加到答案，再把 `cnt[mask]` 加一'],
        summary=['时间 `O(L)`，空间 `O(n)`',
                 '`mask |= 1 << (ord(c) - ord(\'a\'))`：重复字母不会改变 mask',
                 '顺序：先累加再计数，只统计 `i < j`',
                 '写法二：`\'\'.join(sorted(set(s)))` 作为哈希表的 key'],
    ),
)
