def _top(S):
    if 'pair' not in S:
        return ''
    return f"字符对 `pair = {S['pair']}`，落单字符 `single = {S['single']}`"


CONFIG = dict(
    num=3035, title='回文字符串的最大数量', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='字符对 / 落单字符 · 由短到长构造',
    tags=['灵神题单', '难度分 1857'],
    code='''
class Solution(object):
    def maxPalindromesAfterOperations(self, words):

        freq = Counter()
        length_list = []
        for w in words:
            for char in w:
                freq[char] += 1
            length_list.append(len(w))
        length_list.sort()
        
        pair = 0
        single = 0
        for f in freq.values():
            if f % 2 == 1:
                single += 1
            pair += f // 2
        
        res = 0
        for l in length_list:
            need_pair = l // 2
            need_single = l % 2

            if need_pair > pair:
                break
            pair -= need_pair
            if need_single:
                if single > 0:
                    single -= 1
                elif pair > 0:
                    pair -= 1
                    single += 1
                else:
                    break
            
            res += 1

        return res
''',
    call='Solution().maxPalindromesAfterOperations(["abbb","ba","aa","cde"])',
    expect=3,
    views=[
        dict(type='map', var='freq', label='freq（字母 → 总出现次数）', fmt=lambda k, v: f"'{k}': {v}", h=190),
        dict(type='array', var='length_list', label='length_list（所有字符串的长度，排序后由短到长构造）', cell=90, h=190,
             color=lambda S, i, v: 'green' if 'res' in S and i < S['res'] else None,
             dim=lambda S, i, v: 'res' in S and 'l' in S and i < S['res']),
        dict(type='text', fn=_top, size=28),
    ],
    watch=['l', ('need_pair', 'need_pair', 'cyan'), ('need_single', 'need_single', 'orange'), ('pair', 'pair', 'cyan'), ('single', 'single', 'orange'), ('res', 'res', 'green')],
    skip=['for char in w', 'freq[char] += 1'],
    captions={
        'freq = Counter()': '`freq` 统计每个字母的总个数：字母可以跨字符串随便交换',
        'length_list = []': '`length_list` 收集每个字符串的长度',
        'for w in words': lambda S, B, r: ('所有字符串都统计完了' if len(S.length_list) == len(S.words) and 'w' in B and B.w == S.w else f'统计 `"{S.w}"` 的字母，再记下它的长度'),
        'single = 0': '`single` 初始为 0',
        'length_list.append': '`"{w}"` 的字母已计入 `freq`；长度 `{len(w)}` 记入 → `{length_list}`',
        'length_list.sort': '回文串越短越省字母 → 长度==从小到大==排序：`{length_list}`',
        'pair = 0': '`pair`：现在能凑出多少==对==相同字符；`single`：有多少==落单==字符',
        'for f in freq.values()': lambda S, B, r: ('每种字母都看完了' if B.pair == sum(v // 2 for v in S.freq.values()) and B.single == sum(v % 2 for v in S.freq.values()) and B.get('f') == S.f else f'该字母出现 `{S.f}` 次'),
        'if f % 2 == 1': lambda S, B, r: (f'`{S.f}` 是奇数 → 会剩 1 个落单字符' if S.f % 2 == 1 else f'`{S.f}` 是偶数 → 全部能成对'),
        16: '`single` → `{single}`',
        'pair += f // 2': '`{f}` 个字符能成 `{f // 2}` 对 → `pair = {pair}`',
        'res = 0': '`res` 记录能构造出几个回文串',
        'for l in length_list': '尝试构造长度为 `{l}` 的回文串',
        'need_pair = l // 2': '长度 `{l}` 需要 `{l} // 2` = `{l // 2}` 对字符',
        'need_single = l % 2': '长度 `{l}` 是{"奇" if l % 2 else "偶"}数 → 需要 `{l % 2}` 个落单字符放中心',
        'if need_pair > pair': lambda S, B, r: (f'需要 `{S.need_pair}` 对 > 现有 `{S.pair}` 对：字符对不够 → ==break==，更长的更造不出' if S.need_pair > S.pair
                                                else f'需要 `{S.need_pair}` 对 ≤ 现有 `{S.pair}` 对 → 够用'),
        'pair -= need_pair': '用掉 `{need_pair}` 对 → `pair = {pair}`',
        'if need_single:': lambda S, B, r: ('需要中心字符' if S.need_single else '长度为偶数，不需要中心字符'),
        'if single > 0': lambda S, B, r: (f'`single = {S.single} > 0`：用一个落单字符放中心' if S.single > 0
                                          else '没有落单字符了 → 看能不能拆一对'),
        'single -= 1': '落单字符放到中心 → `single = {single}`',
        'elif pair > 0': lambda S, B, r: (f'`pair = {S.pair} > 0`：拆开 1 对，变成 2 个落单字符，一个放中心' if S.pair > 0
                                          else '对也没有了 → 造不出，==break=='),
        'pair -= 1': '拆 1 对 → `pair = {pair}`',
        32: '拆出来的 2 个字符：1 个放中心、1 个落单 → `single = {single}`',
        'res += 1': '成功构造 → `res = {res}`',
        'return res': '最多 `{res}` 个回文串',
    },
    cards=dict(
        one_liner='成对字符才能成回文；先造最短的，省下字符造更多',
        complexity='时间 `O(L + n log n)`，空间 `O(1)`',
        problem=['`words` 中任意两个字符可以交换（可跨字符串、不限次数）',
                 '求最多能让==多少个字符串变成回文==',
                 '示例：`["abbb","ba","aa"]` → `3`；`["abc","ab"]` → `2`',
                 '本视频：`["abbb","ba","aa","cde"]` → `3`'],
        quote='只需要字符串中的字符成对出现，那么就一定可以将其调整为回文串。……因此就应该优先构造长度较短的回文串以节省字符的使用。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历统计字符：每种字符 `f // 2` 对，`f` 为奇数就多 1 个落单 → `pair`、`single`',
              '长度 `l` 的回文串需要 `l // 2` 对，奇数还要 1 个中心字符',
              '没有落单字符时，==拆开一对==变成 2 个落单字符（1 个放中心，1 个留着）'],
        result='`ba`、`aa`、`cde` 依次造成；`abbb` 需要 2 对但只剩 1 对 → 3',
        summary=['时间 `O(L + n log n)`，空间 `O(1)`',
                 '易错：先判断 `need_pair > pair` 再扣除；中心字符不足时才拆对',
                 '拆对：`pair -= 1`、`single += 1` —— 拆出 2 个，1 个立刻放中心，所以净增 1 个落单',
                 '对比灵神：灵神一次扣掉落单字母后只算左右字母数 `tot`；yiduobo 分开维护 `pair` 和 `single`'],
    ),
)
