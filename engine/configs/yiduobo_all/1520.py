def _cnt(S):
    """当前 [l, r] 区间内（前缀和相减）出现的字母及次数"""
    if 'new_l' not in S or 'new_r' not in S:
        return None
    nl, nr, cl = S['new_l'], S['new_r'], S['cnt_list']
    d = {}
    for ch, c in cl[nr].items():
        k = c - cl[nl - 1].get(ch, 0)
        if k > 0:
            d[ch] = k
    return d


def _lr(S):
    for a, b in (('now_l', 'now_r'), ('new_l', 'new_r'), ('l', 'r')):
        if S.get('_line', 0) >= 36 and a != 'now_l':
            continue
        if a in S and b in S:
            return S[a], S[b]
    return None


def _s_color(S, i, v):
    lr = _lr(S)
    if lr and lr[0] - 1 <= i <= lr[1] - 1:
        return 'yellow'
    return None


_SEEN = set()


def _round(S, B, ret):
    _SEEN.clear()
    return f'进入一轮检查：看看区间 `[{S.l}, {S.r}]` 里有哪些字母，它们的位置是否超出区间'


def _for_char(S, B, ret):
    c = S.get('char')
    if c in _SEEN:
        return '区间里的字母都检查完了'
    _SEEN.add(c)
    return f'检查区间里的字母 `{c}`'


def _top(S):
    line = S.get('_line', 0)
    if line >= 33:
        if 'now_l' in S:
            return f"待比较区间 `[now_l, now_r] = [{S['now_l']}, {S['now_r']}]`，已选 `{S.get('res', [])}`"
        return '把各字母的区间按左端点排序，再扫一遍选出互不相交的'
    if 'new_l' in S and 'l' in S:
        d = _cnt(S)
        return f"当前区间 `[{S['l']}, {S['r']}]`，前缀和得区间内出现：`{d}`"
    return '为每个字母求「包含它所有出现位置的最短合法区间」（下标从 1 开始）'


CONFIG = dict(
    num=1520, title='最多的不重叠子字符串', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='前缀和 + 反复扩展区间 + 区间贪心',
    tags=['灵神题单·贪心与思维', '贪心算法', '难度分 2363'],
    code='''
class Solution(object):
    def maxNumOfSubstrings(self, s):

        cnt_list = [{}]
        pos_dict = {}
        for index, char in enumerate(s):
            cnt_list.append(cnt_list[-1].copy())
            cnt_list[-1][char] = cnt_list[-1].get(char, 0) + 1
        
            if char not in pos_dict:
                pos_dict[char] = [index + 1, index + 1]
            else:
                pos_dict[char][1] = index + 1
        
        intervals = []
        for asc in range(97, 123):
            char = chr(asc)
            if char in pos_dict:
                l, r = pos_dict[char]
                while True:
                    new_l, new_r = l, r
                    for char in cnt_list[new_r]:
                        if cnt_list[new_r][char] - cnt_list[new_l - 1].get(char, 0) > 0:
                            if pos_dict[char][0] < new_l or pos_dict[char][1] > new_r:
                                new_l, new_r = min(new_l, pos_dict[char][0]), max(new_r, pos_dict[char][1])
                    
                    if l == new_l and r == new_r:
                        break
                    l, r = new_l, new_r

                intervals.append([l, r])
        
        intervals = sorted(intervals, key=lambda d:d[0])
        res = []
        now_l, now_r = intervals[0]
        for l, r in intervals[1:]:
            if l > now_r:
                res.append(s[now_l - 1:now_r])

            now_l, now_r = l, r
        
        res.append(s[now_l - 1 : now_r])
        return res
''',
    call='Solution().maxNumOfSubstrings("ababc")',
    expect=['abab', 'c'],
    views=[
        dict(type='text', fn=_top, size=24, h=70),
        dict(type='string', var='s', label='s（黄 = 当前区间；下标从 1 开始，即格子下标 + 1）', cell=84, h=130, color=_s_color),
        dict(type='map', var='pos_dict', label='pos_dict：每个字母第一次、最后一次出现的位置（从 1 开始）', h=110, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='array', var='intervals', label='intervals：每个字母扩展出的合法区间 [l, r]', h=170, cell=110, index=False),
        dict(type='array', var='res', label='res：已选出的子串', h=140, cell=110, index=False),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('new_l', 'new_l', 'orange'), ('new_r', 'new_r', 'orange'), ('now_l', 'now_l', 'purple'), ('now_r', 'now_r', 'purple')],
    skip=['for index, char in enumerate', 'cnt_list.append(', 'cnt_list[-1][char] =', 'if char not in pos_dict', 'pos_dict[char] = [',
          'pos_dict[char][1] = index', 'for asc in range', 'pos_dict = {}', 'while True', 'if cnt_list[new_r][char]', 'char = chr(asc)', 'if char in pos_dict', 'new_l, new_r = l, r'],
    max_steps=64,
    captions={
        'cnt_list = [{}]': '一趟扫描：记每个字母第一次/最后一次出现的位置，并算每个字母出现次数的==前缀和== `cnt_list`',
        'intervals = []': lambda S, B, ret: f'`pos_dict = {S.pos_dict}`：位置从 1 开始。接下来按字母顺序，为每个字母求包含它全部出现位置的==最短合法区间==',
        'l, r = pos_dict[char]': lambda S, B, ret: (_SEEN.clear(), f'字母 `{chr(S.asc)}`：先取第一次和最后一次出现位置 `[l, r] = [{S.l}, {S.r}]`，再反复检查区间里有哪些字母')[1],
        22: _for_char,
        'if pos_dict[char][0] < new_l': lambda S, B, ret: (
            f'前缀和相减：`{S.char}` 在区间里出现，但它的位置 `{S.pos_dict[S.char]}` 超出了 `[{S.new_l}, {S.new_r}]` → ==要扩展=='
            if S.pos_dict[S.char][0] < S.new_l or S.pos_dict[S.char][1] > S.new_r else f'前缀和相减：`{S.char}` 在区间里出现，所有位置 `{S.pos_dict[S.char]}` 都在区间内，不用扩展'),
        'new_l, new_r = min': '用字母 `{char}` 的首尾位置扩展：`[new_l, new_r] = [{new_l}, {new_r}]`',
        'if l == new_l and r == new_r': lambda S, B, ret: (f'区间没变（`[{S.l}, {S.r}]`）→ 定住了，==break==' if (S.l, S.r) == (S.new_l, S.new_r)
                                                          else f'区间从 `[{S.l}, {S.r}]` 扩成了 `[{S.new_l}, {S.new_r}]` → 可能又带进新字母，再来一轮'),
        'break': '区间不再变化，这个字母的合法区间求出来了',
        'l, r = new_l, new_r': lambda S, B, ret: (_SEEN.clear(), f'更新 `[l, r] = [{S.l}, {S.r}]`，再来一轮检查')[1],
        'intervals.append': '字母 `{chr(asc)}` 对应的区间 `[{l}, {r}]` 记入 `intervals`',
        'sorted(intervals': '得到至多 26 个区间。==按左端点排序==：区间只会「不相交」或「一个套另一个」',
        'res = []': '`res` 保存答案；`[now_l, now_r]` 是待比较的区间',
        'now_l, now_r = intervals[0]': '先把第 0 个区间当作待比较区间：`[{now_l}, {now_r}]`',
        'for l, r in intervals[1:]': lambda S, B, ret: (f'看下一个区间 `[{S.l}, {S.r}]`' if (S.l, S.r) != (B.get('l'), B.get('r')) or 'now_l' not in B else '区间都看完了'),
        'if l > now_r': lambda S, B, ret: (f'`l = {S.l} > now_r = {S.now_r}`：它和待比较区间不相交 → 后面的也不会相交，待比较区间可以==加入答案=='
                                           if S.l > S.now_r else f'`l = {S.l} <= now_r = {S.now_r}`：被待比较区间套住，选更短的这个更优，不加入答案'),
        'res.append(s[now_l - 1:now_r])': '加入答案：`s[{now_l - 1}:{now_r}] = "{res[-1]}"`',
        'now_l, now_r = l, r': '待比较区间换成 `[{now_l}, {now_r}]`',
        'res.append(s[now_l - 1 :': '循环结束后，最后一个待比较区间也要加入答案：`"{res[-1]}"`',
        'return res': '所选子串：=={ret}==',
    },
    cards=dict(
        one_liner='每个字母扩出最短合法区间，再选不重叠的',
        complexity='时间 `O(26n + 26²)`，空间 `O(26n)`',
        problem=['在小写字母串 `s` 中选最多的==互不重叠==子串；子串含某字母，就必须含 `s` 里该字母的全部',
                 '数量相同时选总长度最短的',
                 '本视频：`"ababc"` → `["abab", "c"]`'],
        quote='对于l到r之间的所有字符，同样是需要找到这个字符第一次和最后一次出现的位置，并用这两个位置来更新l和r。若这一轮l和r被更新过，说明区间扩展了，需要再次进行扩展，直到l和r定住不动位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['每种字符只对应一个最短合法区间：从首尾出现位置开始，反复==扩展==直到不动',
              '先扫一遍求每个字符的首尾位置和出现次数前缀和，区间内有没有某字符 `O(1)` 判断',
              '这些区间只会不相交或互相包含：左端点排序后，遇到被套住的区间就换成更短的那个',
              '遇到不相交的区间，说明待比较区间是最内层的，可以加入答案'],
        summary=['时间 `O(26n + 26²)`，空间 `O(26n)`（前缀和用了字典）',
                 '循环里的 `char` 被内层 `for char in cnt_list[new_r]` 覆盖，但外层每轮重新取，不影响',
                 '遍历完后，最后一个 `[now_l, now_r]` 还要加入答案，别漏了',
                 '下标从 1 开始存，所以切片是 `s[now_l - 1 : now_r]`',
                 '对比灵神：灵神建有向图 + DFS 求区间、按右端点排序；yiduobo 用前缀和反复扩展、按左端点排序'],
    ),
)
