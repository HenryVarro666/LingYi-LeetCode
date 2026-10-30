def _top(S):
    if 'tot' not in S:
        return ''
    return f"可往左右填的字母 `tot = {S['tot']}`" + ('（还没扣掉出现奇数次的字母）' if 'cnt' not in S or S.get('_line', 0) < 8 else '')


CONFIG = dict(
    num=3035, title='回文字符串的最大数量', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='正向思维 · 按长度从小到大填',
    tags=['灵神题单', '难度分 1857'],
    code='''
class Solution:
    def maxPalindromesAfterOperations(self, words: List[str]) -> int:
        ans = tot = 0
        cnt = Counter()
        for w in words:
            tot += len(w)
            cnt += Counter(w)
        tot -= sum(c % 2 for c in cnt.values())  # 减去出现次数为奇数的字母

        words.sort(key=len)  # 按照长度从小到大排序
        for w in words:
            tot -= len(w) // 2 * 2  # 长为奇数的字符串，长度要减一
            if tot < 0: break
            ans += 1
        return ans
''',
    call='Solution().maxPalindromesAfterOperations(["abbb","ba","aa","cde"])',
    expect=3,
    views=[
        dict(type='array', var='words', label='words（黄 = 当前要填的字符串）', cell=110, h=190,
             color=lambda S, i, v: ('yellow' if S.get('w') == v else None) if S.get('_line', 0) >= 11 else None),
        dict(type='map', var='cnt', label='cnt（字母 → 总出现次数）', fmt=lambda k, v: f"'{k}': {v}", h=190),
        dict(type='text', fn=_top, size=28),
    ],
    watch=['w', ('tot', 'tot', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = tot = 0': '`ans` 是回文串个数；`tot` 是能填在==左右==的字母个数',
        'cnt = Counter()': '`cnt` 统计全体字母的总出现次数（交换随意，字母可以随便分配）',
        5: lambda S, B, r: ('每个字符串都统计完了' if 'w' in B and B.w == S.w and B.get('cnt') is not None and B.tot == S.tot and B.w == 'cde' else f'取出 `"{S.w}"`'),
        11: lambda S, B, r: f'按从短到长取出 `"{S.w}"`，长度 `{len(S.w)}`',
        'tot += len(w)': '`tot += len("{w}")` → `{tot}`',
        'cnt += Counter(w)': '累加 `"{w}"` 的字母 → `cnt = {dict(cnt)}`',
        'tot -= sum': '出现奇数次的字母有 `{sum(c % 2 for c in cnt.values())}` 个，各有一个没法成对 → 它们只能放正中间，`tot` = =={tot}==',
        'words.sort': '字符串越短需要的字母越少 → 按长度==从小到大==填：`{words}`',
        'tot -= len(w)': '`"{w}"` 需要左右各一半：`{len(w)} // 2 * 2 = {len(w) // 2 * 2}` 个字母（奇数长度的正中间不算）→ `tot = {tot}`',
        'if tot < 0': lambda S, B, r: (f'`tot = {S.tot} < 0`：字母不够填 `"{S.w}"`，更长的更填不了 → ==break==' if S.tot < 0
                                       else f'`tot = {S.tot} ≥ 0`：字母够用，`"{S.w}"` 能变成回文'),
        'ans += 1': '又多了一个回文串 → `ans = {ans}`',
        'return ans': '最多能得到 `{ans}` 个回文串',
    },
    cards=dict(
        one_liner='字母随便交换，先扣掉落单字母，再从短到长一个个填',
        complexity='时间 `O(L + n log n)`，空间 `O(1)`',
        problem=['`words` 里的字符串，可以任意次交换任意两个字符（可跨字符串）',
                 '求操作后==最多有多少个字符串是回文==',
                 '示例：`["abbb","ba","aa"]` → `3`；`["cd","ef","a"]` → `1`'],
        quote='不妨先把左右的字母填了，最后在往正中间填入字母。……字符串越短，需要的字母越少。所以按照字符串的长度从小到大填。',
        quote_src='—— 灵茶山艾府题解',
        idea=['字母能任意分配 → 统计总长度，减去出现奇数次的字母，得到能放左右的字母数 `tot`',
              '奇数长度字符串的正中间填什么都行，所以==先填左右，最后填中间==',
              '按长度从小到大，每个字符串扣 `len // 2 * 2`；扣成负数就停'],
        result='`tot` 够填 `ba`、`aa`、`cde`，不够填 `abbb` → 3',
        summary=['时间 `O(L + n log n)`，空间 `O(1)`（忽略排序栈）',
                 '易错：奇数长度字符串的中间字母不占 `tot`，所以扣的是 `len // 2 * 2`',
                 '易错：必须先排序再填，先填长的会浪费字母',
                 '另一种写法（方法二，逆向思维）：算最少有几个不是回文串，按长度从大到小排'],
    ),
)
