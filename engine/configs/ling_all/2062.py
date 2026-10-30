W = 'cuaieuouac'


def _color(S, i, v):
    if 'i' not in S:
        return None
    if S.get('_line') == 20 and S['start'] <= i < S['left']:
        return 'green'
    return None


def _dim(S, i, v):
    return v not in 'aeiou'


def _top(S):
    if 'i' not in S:
        return '辅音把字符串切成几段；每段内部就是 1358 题：==越长越合法=='
    st, l, i = S['start'], S['left'], S['i']
    if S.get('_line') == 20:
        if l == st:
            return f'左端点范围 `[start, left−1]` 为空：本轮 ==0== 个'
        return f'右端点 {i}：左端点取 `{st}..{l - 1}` 都合法 → 本轮 =={l - st}== 个'
    return f'`start = {st}`：左端点不能越过前面的辅音'


def _while(S, B, ret):
    n = len(S.cnt)
    w = S.word[S.left:S.i + 1]
    if n == 5:
        return f'`len(cnt) == 5`：`{w}` 含全部元音，==合法== → 右移 left'
    if S.left > S.start and len(set(S.word[S.left - 1:S.i + 1])) == 5:
        return f'`len(cnt) = {n}`：`{w}` 不合法，但再往左一位就==合法==（恰好不合法）'
    return f'`len(cnt) = {n}`：还没凑齐五种元音'


CONFIG = dict(
    num=2062, title='统计字符串中的元音子字符串', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='越长越合法 · 辅音处重置 start',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution:
    def countVowelSubstrings(self, word: str) -> int:
        cnt = defaultdict(int)
        ans = start = left = 0

        for i, ch in enumerate(word):
            if ch not in "aeiou":
                cnt.clear()  # 重置
                start = left = i + 1
                continue

            # 做法类似 1358. 包含所有三种字符的子字符串数目（哈希表写法）
            cnt[ch] += 1
            while len(cnt) == 5:  # 窗口包含所有元音
                out = word[left]
                cnt[out] -= 1
                if cnt[out] == 0:
                    del cnt[out]
                left += 1
            ans += left - start

        return ans
''',
    call=f'Solution().countVowelSubstrings({W!r})',
    expect=7,
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='string', var='word', label='word（暗 = 辅音，框 = [left, i]，绿 = 合法左端点 start..left−1）',
             pointers={'start': 'orange', 'left': 'blue', 'i': 'pink'}, window=('left', 'i'),
             color=_color, dim=_dim, cell=96, h=300),
        dict(type='map', var='cnt', label='cnt（窗口内每种元音的次数）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=34),
    ],
    watch=[('start', 'start', 'orange'), ('left', 'left', 'blue'), ('i', 'i', 'pink'), 'ch', ('ans', 'ans', 'green')],
    skip=['out = word[left]'],
    captions={
        'cnt = defaultdict': '`cnt` 统计窗口内每种元音的次数',
        'ans = start = left = 0': '`start`：左端点的==下界==（不能包含辅音）；`left`：窗口左端点',
        'for i, ch': lambda S, B, r: ('遍历结束' if 'i' in B and B.i == S.i else f'右端点 `i = {S.i}`，`ch = {S.ch!r}`'),
        'if ch not in': lambda S, B, r: (f'{S.ch!r} 是==辅音==：任何包含它的子串都不合法' if S.ch not in 'aeiou'
                                         else f'{S.ch!r} 是元音，按 1358 的方法处理'),
        'cnt.clear()': '清空窗口',
        'start = left = i + 1': '后面的子串左端点至少是 `{start}` → `start = left = {start}`',
        'continue': '跳过本轮',
        'cnt[ch] += 1': '`cnt[{ch!r}]` → {cnt[ch]}',
        'while len(cnt) == 5': _while,
        'cnt[out] -= 1': '左端 `{out!r}` 离开窗口：`cnt[{out!r}]` → {cnt[out]}',
        'if cnt[out] == 0': lambda S, B, r: (f'窗口里没有 {S.out!r} 了' if S.cnt[S.out] == 0 else f'窗口里还有 {S.out!r}'),
        'del cnt[out]': '删掉 `{out!r}` → 只剩 {len(cnt)} 种',
        'left += 1': '`left` → {left}',
        'ans += left - start': lambda S, B, r: ('左端点范围为空，`ans` 不变' if S.left == S.start
                                                else f'左端点 `{S.start}..{S.left - 1}` 都合法：`ans += {S.left} − {S.start}` = =={S.ans}=='),
        'return ans': '一共 =={ret}== 个元音子字符串',
    },
    max_steps=80,
    cards=dict(
        one_liner='1358 的滑窗 + 辅音处重置：合法左端点在 [start, left−1]',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`（|Σ| = 5）',
        problem=['==元音子串==：只由元音组成，且五种元音都出现',
                 '统计 `word` 中元音子串的个数',
                 '示例：`"aeiouu"` → `2`；`"cuaieuouac"` → `7`'],
        quote='当遍历到辅音 word[i] 时，更新 start = i + 1……满足要求的子串左端点的范围是 [start, left−1]，这有 left−start 个，加到答案中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先想全是元音的情况：和 1358 一样，`ans += left`',
              '遇到辅音：清空窗口，`start = left = i + 1`',
              '左端点不能小于 start，所以改成 `ans += left − start`'],
        summary=['时间 `O(n)`：left 总共最多右移 n 次',
                 '遇到辅音要==同时==重置 cnt、start、left',
                 '`cnt[out]` 到 0 要 `del`，`len(cnt)` 才是种数',
                 '同类：1358、2799、3325（越长越合法）'],
    ),
)
