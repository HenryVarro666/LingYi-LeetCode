def _fmt(lst):
    return ' '.join(f'{c}×{n}' for c, n in lst)


def _top(S):
    if 'cnt_list' not in S:
        return ''
    t = f"S 收缩：`{_fmt(S['cnt_list'])}`"
    if 'word' in S and 'pos' in S:
        t += f"　　word=`{S['word']}`，已匹配 `{S['pos']}` 段"
    return t


def _wcolor(S, i, v):
    if 'word' not in S or 'pos' not in S or 'flag' not in S:
        return None
    return None


def _scol(S, i, v):
    """S 里属于已匹配段的字符标绿"""
    if 'cnt_list' not in S or 'word' not in S or 'pos' not in S:
        return None
    k = sum(n for _, n in S['cnt_list'][:S['pos']])
    return 'green' if i < k else None


CONFIG = dict(
    num=809, title='情感丰富的文字', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='连续字符分组 + 逐段比较次数',
    tags=['滑动窗口与双指针'],
    code='''
class Solution(object):
    def expressiveWords(self, S, words):

        cnt_list = []
        now = ''
        cnt = 0
        for char in S + ' ':
            if char == now:
                cnt += 1
            else:
                if cnt > 0:
                    cnt_list.append([now, cnt])
                now = char
                cnt = 1

        res = 0
        for word in words:
            now = ''
            cnt = 0
            pos = 0
            flag = True
            for char in word + ' ':
                if char == now:
                    cnt += 1
                else:
                    if cnt > 0:
                        if pos == len(cnt_list):
                            flag = False
                            break
                        if cnt_list[pos][0] != now:
                            flag = False
                            break
                        if cnt_list[pos][1] < cnt or (cnt_list[pos][1] < 3 and cnt_list[pos][1] > cnt):
                            flag = False
                            break
                        pos += 1
                    now = char
                    cnt = 1
            
            if flag and pos == len(cnt_list):
                res += 1
        
        return res
''',
    call="Solution().expressiveWords('heeellooo', ['hello', 'helo'])",
    expect=1,
    views=[
        dict(type='text', fn=_top, size=24),
        dict(type='string', var='S', label='S', h=190, cell=70, color=_scol),
        dict(type='array', var='words', label='words', h=200, cell=130,
             color=lambda S, i, v: ('blue' if 'word' in S and S['word'] == v else None),
             dim=lambda S, i, v: 'res' in S and 'word' in S and i < S['words'].index(S['word'])),
    ],
    skip=['now = char', 'cnt = 1', 'cnt += 1', 'flag = True', 'pos = 0', "now = ''", 'cnt = 0'],
    max_steps=110,
    watch=['now', 'cnt', 'pos', ('flag', 'flag', 'pink'), ('res', 'res', 'green')],
    captions={
        'cnt_list = []': '`cnt_list` 存 S 收缩后的 ==[字符, 连续次数]==',
        'now = \'\'': '`now` 当前这一段的字符',
        'cnt = 0': '`cnt` 当前这一段的长度',
        'for char in S': lambda S_, B, r: ('S 末尾加了个空格当哨兵：让最后一段也能被收进列表' if S_.char == ' ' else f'扫描 S 的字符 `{S_.char}`'),
        'if char == now': lambda S_, B, r: (f"`'{S_.char}' == '{S_.now}'`：同一段继续" if S_.char == S_.now
                                            else f"`'{S_.char}' != '{S_.now}'`：换字符了，上一段结束"),
        'cnt += 1': '这一段长度 +1：`cnt` = {cnt}',
        'if cnt > 0': lambda S_, B, r: ('`cnt > 0`：上一段有内容，要登记' if S_.cnt > 0 else '`cnt = 0`：还没有上一段'),
        'cnt_list.append': '登记 S 的一段：`{now}×{cnt}`',
        'now = char': '开始新的一段：`now = {now!r}`',
        'cnt = 1': '新一段先算 1 个',
        'res = 0': '`res` 统计能扩展成 S 的单词数',
        'for word in words': '检查单词 `{word}`：把它同样收缩，再和 S 的段逐段对比',
        'pos = 0': '`pos`：已经和 S 的第几段对上了',
        'flag = True': '`flag`：目前没发现不匹配',
        'for char in word': lambda S_, B, r: ('word 末尾也加哨兵空格，最后一段才会被检查' if S_.char == ' ' else f'扫描 word 的字符 `{S_.char}`'),
        'if pos == len': lambda S_, B, r: ('word 的段比 S 还多 → ==不匹配==' if S_.pos == len(S_.cnt_list)
                                           else f'`pos = {S_.pos}` 还没超出 S 的段数 {len(S_.cnt_list)}'),
        'if cnt_list[pos][0] != now': lambda S_, B, r: (f"S 第 {S_.pos} 段是 `{S_.cnt_list[S_.pos][0]}`，word 这段是 `{S_.now}`：字符不同 → ==不匹配==" if S_.cnt_list[S_.pos][0] != S_.now
                                                        else f"字符相同 `{S_.now}`，再比次数"),
        'if cnt_list[pos][1] < cnt': lambda S_, B, r: (
            f"S 里 `{S_.now}` 只有 {S_.cnt_list[S_.pos][1]} 个，word 有 {S_.cnt} 个：S 更少，扩展不出来 → ==不匹配==" if S_.cnt_list[S_.pos][1] < S_.cnt
            else (f"S 里 {S_.cnt_list[S_.pos][1]} 个 < 3 且 ≠ word 的 {S_.cnt} 个：不够 3 个不是扩展来的，必须相等 → ==不匹配==" if S_.cnt_list[S_.pos][1] < 3 and S_.cnt_list[S_.pos][1] > S_.cnt
                  else (f"S 里 {S_.cnt_list[S_.pos][1]} 个，word 里 {S_.cnt} 个：次数相等 → 这段匹配" if S_.cnt_list[S_.pos][1] == S_.cnt else f"S 里 {S_.cnt_list[S_.pos][1]} 个 >= 3，可由 word 的 {S_.cnt} 个扩展出来 → 这段匹配"))),
        'flag = False': '`flag = False`：这个单词不行了',
        'break': '直接 break，不用再看后面',
        'pos += 1': '这一段匹配，`pos` → {pos}',
        'if flag and pos': lambda S_, B, r: ('`flag` 成立且 S 的所有段都对上了 → ==这个单词可以==' if S_.flag and S_.pos == len(S_.cnt_list)
                                             else f'不满足（`flag = {S_.flag}`，`pos = {S_.pos}`，S 共 {len(S_.cnt_list)} 段）→ 这个单词不行'),
        'res += 1': '`res` → {res}',
        'return res': '一共有 `{res}` 个单词能扩展成 S',
    },
    cards=dict(
        one_liner='把连续字符缩成「字符×次数」，S 的段 >= 3 才能比 word 多',
        complexity='时间 `O(|S| + 所有 word 长度)`，空间 `O(|S|)`',
        problem=['单词里某组相邻相同字母可以扩展：扩展后该组字母 ==至少 3 个==',
                 '统计 `words` 中有多少个单词能扩展成 `S`',
                 '本视频：`S = heeellooo`，`words = [hello, helo]` → `1`'],
        quote='对于每个word，进行同样的操作，那么缩短后得到的字符串必须与s缩短后得到的字符串完全一致，且出现次数要么一致，要么比s中对应出现的次数要少，且s中出现的次数大于等于3次。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把 S 缩成 `[字符, 次数]`：`h×1 e×3 l×2 o×3`',
              'word 也缩一遍，字符序列必须和 S 完全相同',
              '每段：次数相等；或 word 更少且 ==S 里该段 >= 3=='],
        summary=['时间 `O(|S| + Σ|word|)`，空间 `O(|S|)`',
                 '字符串末尾加空格做哨兵，最后一段才会被登记',
                 '`S` 里次数 < 3 的段必须和 word 完全相等（本例 `ll` 只有 2 个）',
                 '`word` 段数比 S 多、或少于 S，都要判不匹配（最后检查 `pos == len(cnt_list)`）',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
