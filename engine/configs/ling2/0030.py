S_IN = 'abbaabab'
WORDS = ['ab', 'ba']


def _has(S):
    return 'right' in S and 'start' in S and isinstance(S.get('right'), int)


def _win(S):
    """当前窗口 [a, b)（右开）"""
    if not _has(S):
        return None
    r, wl, W = S['right'], S['word_len'], S['window_len']
    line = S.get('_line') or 0
    if line >= 34 and 'left' in S and S['left'] >= 0 and S['left'] == r - W:
        return S['left'] + wl, r
    return max(S['start'], r - W), r


def _color(S, i, v):
    if not _has(S):
        return None
    r, wl = S['right'], S['word_len']
    line = S.get('_line') or 0
    if 'left' in S and line >= 33 and S['left'] == r - S['window_len'] and S['left'] <= i < S['left'] + wl:
        return 'red'
    if r - wl <= i < r and 15 <= line <= 21:
        return 'blue'
    if 'ans' in S and line in (29, 30) and S['ans'] and S['ans'][-1] == r - S['window_len'] and S['ans'][-1] <= i < r:
        return 'green'
    return None


def _win_text(S):
    w = _win(S)
    if w is None:
        if 'target_cnt' in S:
            return f"`word_len = {S['word_len']}`，`window_len = {S['window_len']}`：在 `{len(S_IN) // S['word_len']}` 个单词上做定长滑窗"
        return ''
    a, b = w
    wl = S['word_len']
    parts = [S['s'][k:k + wl] for k in range(a, b, wl)]
    full = b - a == S['window_len']
    tail = ''
    if full:
        tail = '　→ ==合法==' if S['overload'] == 0 else f"　→ 过多 `{S['overload']}` 个，不合法"
    return f"起点 `start = {S['start']}`，窗口 `[{a},{b})`：`{' | '.join(parts) or '空'}`　`overload = {S['overload']}`{tail}"


def _cap_if_in(S, B, ret):
    w, c, t = S.in_word, S.cnt[S.in_word], S.target_cnt[S.in_word]
    if c == t:
        return (f'`cnt["{w}"] = {c}` 已等于目标 `{t}`' + ('（==不在 words 里==）' if t == 0 else '') +
                ' → 加一后==过多==')
    return f'`cnt["{w}"] = {c} < {t}`：加一后 `{c + 1}`，不超'


def _cap_if_out(S, B, ret):
    w, c, t = S.out_word, S.cnt[S.out_word], S.target_cnt[S.out_word]
    if c == t:
        return f'`cnt["{w}"]` 回到目标 `{t}`：`{w}` 不再过多'
    return f'`cnt["{w}"] = {c}` ≠ 目标 `{t}`：overload 不变'


CONFIG = dict(
    num=30, title='串联所有单词的子串', difficulty='Hard', category='滑动窗口',
    author='灵茶山艾府', technique='word_len 次定长滑动窗口 · 入-更新-出',
    tags=['面试经典150'],
    code='''
class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        word_len = len(words[0])  # 一个单词的长度
        window_len = word_len * len(words)  # 所有单词的总长度，即窗口大小

        # 目标：窗口中的单词出现次数必须与 target_cnt 完全一致
        target_cnt = Counter(words)

        ans = []
        # 枚举第一个窗口的左端点，做 word_len 次起点不同的滑动窗口
        for start in range(word_len):
            cnt = defaultdict(int)
            overload = 0  # 统计过多的单词个数（包括不在 words 中的单词）
            # 枚举窗口最后一个单词的右开端点
            for right in range(start + word_len, len(s) + 1, word_len):
                # 1. in_word 进入窗口
                in_word = s[right - word_len: right]
                # 下面 cnt[in_word] += 1 后，in_word 的出现次数过多
                if cnt[in_word] == target_cnt[in_word]:
                    overload += 1
                cnt[in_word] += 1

                left = right - window_len  # 窗口第一个单词的左端点
                if left < 0:  # 窗口大小不足 window_len
                    continue

                # 2. 更新答案
                # 如果没有超出 target_cnt 的单词，那么也不会有少于 target_cnt 的单词
                if overload == 0:
                    ans.append(left)

                # 3. 窗口最左边的单词 out_word 离开窗口，为下一轮循环做准备
                out_word = s[left: left + word_len]
                cnt[out_word] -= 1
                if cnt[out_word] == target_cnt[out_word]:
                    overload -= 1

        return ans
''',
    call=f'Solution().findSubstring({S_IN!r}, {WORDS!r})',
    expect=[0, 2],
    views=[
        dict(type='text', fn=_win_text, size=26, h=64),
        dict(type='string', var='s', label='s（框 = 窗口，蓝 = 进入的单词，红 = 离开的单词）', cell=90, h=200,
             window=(lambda S: _win(S)[0] if _win(S) else None, lambda S: _win(S)[1] - 1 if _win(S) else None),
             color=_color, pointers={'start': 'purple'}),
        dict(type='map', var='target_cnt', label='target_cnt（目标次数）', h=100, font=26, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='map', var=lambda S: dict(S['cnt']) if 'cnt' in S else None, label='cnt（窗口内次数）', h=110, font=26,
             fmt=lambda k, v: f'{k}: {v}'),
    ],
    watch=[('start', 'start', 'purple'), ('right', 'right'), ('left', 'left'), ('overload', 'overload', 'red'),
           ('ans', 'ans', 'green')],
    skip=['ans = []', 'left = right - window_len', 'out_word = s[left', 'cnt = defaultdict', 'overload = 0',
          'in_word = s[', '                    continue', 'cnt[in_word] += 1'],
    captions={
        'word_len = len': '一个单词长 `word_len = {word_len}`',
        'window_len = word_len': '窗口长 `window_len = {word_len} × {len(words)} = {window_len}`',
        'target_cnt = Counter': '目标：窗口里每个单词的次数要和 `target_cnt` ==完全一致==',
        'for start in range': lambda S, B, ret: (f'第 `{S.start + 1}` 次滑窗：从 `start = {S.start}` 起每 `{S.word_len}` 个字母切一刀；`cnt`、`overload` 清零'
                                                 if S.get('start') != B.get('start') or 'start' not in B else '所有起点都滑完了'),
        'cnt = defaultdict': '换了起点，窗口清空：`cnt` 重新统计',
        'overload = 0': '`overload`：窗口里==次数过多==的单词个数（包括不在 words 里的）',
        'for right in range': lambda S, B, ret: (f'`right = {S.right}`，① 入：`in_word = s[{S.right - S.word_len}:{S.right}] = "{S.s[S.right - S.word_len:S.right]}"`'
                                                 if S.get('right') != B.get('right') or 'right' not in B else '这个起点滑到头了'),
        'in_word = s[': '① 入：`in_word = "{in_word}"`',
        'if cnt[in_word] ==': _cap_if_in,
        '                    overload += 1': '`overload` += 1 → {overload}；然后 `cnt["{in_word}"]` 加一',
        'cnt[in_word] += 1': '`cnt["{in_word}"]` → {cnt[in_word]}',
        'if left < 0': lambda S, B, ret: (f'`left = {S.right} − {S.window_len} = {S.left} < 0`：窗口还不满 `{S.window_len}` → `continue`'
                                          if S.left < 0 else f'窗口满了：左端点 `left = {S.left}`'),
        '                    continue': '继续往右扩',
        'if overload == 0': lambda S, B, ret: (
            (f'② 更新：`overload = 0`，没有过多的单词 → ==也就不会有少的==，窗口合法' if not S.ans
             else '② 更新：`overload = 0` → 合法') if S.overload == 0
            else f'② 更新：`overload = {S.overload} > 0` → 不合法'),
        'ans.append(left)': '记录答案 `left = {left}`：`ans = {ans}`',
        'cnt[out_word] -= 1': '③ 出：`"{out_word}"` 离开窗口，`cnt["{out_word}"]` → {cnt[out_word]}',
        'if cnt[out_word] ==': _cap_if_out,
        '                    overload -= 1': '`overload` −= 1 → {overload}',
        'return ans': '返回所有合法窗口的左端点 =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='把单词当成元素，做 word_len 次起点不同的定长滑动窗口',
        complexity='时间 `O((n + m)·wordLen)`，空间 `O(m·wordLen)`',
        problem=['`words` 里的单词==长度相同==；`s` 中由所有单词（任意顺序）拼成的子串叫「串联子串」',
                 '返回所有串联子串在 `s` 中的起始下标',
                 '示例：`s = "barfoothefoobarman"`，`words = ["foo","bar"]` → `[0,9]`',
                 f'本视频：`s = "{S_IN}"`，`words = {WORDS}` → `[0,2]`'],
        quote='从第一个子串 barfoo 到另一个子串 foothe，少了一个 bar，多了一个 the，中间的 foo 是不变的，不需要重复统计。这种场景非常适合==定长滑动窗口==算法。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只需枚举起点 `0..word_len-1`：起点 `word_len` 的情况已经在起点 0 的滑窗里算过',
              '每次滑动==进一个单词、出一个单词==，套「入 - 更新 - 出」三步',
              '`overload` 记过多的单词个数；窗口长度固定，`overload = 0` 就说明次数完全一致'],
        result='起点 0 的滑窗找到 `[0,4)`、`[2,6)`；起点 1 被 `bb`、`aa` 卡住 → `[0,2]` ✓',
        summary=['时间 `O((n + m)·wordLen)`：做 `wordLen` 次滑窗，每次 `O(n)`',
                 '`overload` 要把==不在 words 里的单词==也算进去（目标次数为 0）',
                 '为什么 `overload = 0` 就合法？窗口总单词数等于 `len(words)`，没有多的就没有少的'],
    ),
)
