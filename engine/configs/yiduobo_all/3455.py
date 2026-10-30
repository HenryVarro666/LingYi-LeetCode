def _cols(S, i, v):
    for h, nx, c in (('first_hit', 'first_next', 'blue'), ('second_hit', 'second_next', 'green'), ('third_hit', 'third_next', 'orange')):
        hs, nn = S.get(h), S.get(nx)
        if hs and nn and 'third_hit' in S:
            if any(q <= i < q + len(nn) for q in hs):
                return c
    return None


def _idx(S):
    return S['index'] if 'pos_first' in S and 'first_index' not in S else None


def _info(S):
    if 'third_hit' in S and 'pos_third' in S:
        return f"`first_hit = {S['first_hit']}`  `second_hit = {S['second_hit']}`  `third_hit = {S['third_hit']}`"
    if 'first_hit' in S:
        return f"`first_hit = {S['first_hit']}`"
    if 'first_index' in S:
        return f"first_index = {S['first_index']}  second_index = {S['second_index']}  third_index = {S['third_index']}  res = ==%s==" % S['res']
    return ''


def _text(S):
    if 'third_hit' in S and 'first_index' in S:
        return f"`first_hit = {S['first_hit']}`  `second_hit = {S['second_hit']}`  `third_hit = {S['third_hit']}`"
    if 'third_hit' in S:
        return f"`first_hit = {S['first_hit']}`  `second_hit = {S['second_hit']}`  `third_hit = {S['third_hit']}`"
    return f"各段已找到的命中位置：`first_hit = {S.get('first_hit')}`  `second_hit = {S.get('second_hit')}`" if 'first_hit' in S else ''


CONFIG = dict(
    num=3455, title='最短匹配子字符串', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='KMP 求三段命中位置 · 三个下标同向移动', tags=['字符串', '难度分 2303'],
    code='''
class Solution(object):
    def shortestMatchingSubstring(self, s, p):
        
        first_next = []
        second_next = []
        third_next = []
        
        def get_next(start, f):
            if start == len(p) or p[start] == '*':
                return start
            f.append(0)
            pos = 0
            now = start + 1
            while now < len(p) and p[now] != '*':
                while pos > 0 and p[pos + start] != p[now]:
                    pos = f[pos - 1]
                
                if p[pos + start] == p[now]:
                    pos += 1
                f.append(pos)
                now += 1
            
            return now

        start = -1
        start = get_next(start + 1, first_next)
        start = get_next(start + 1, second_next)
        start = get_next(start + 1, third_next)

        first_hit = []
        second_hit = []
        third_hit = []

        pos_first = 0
        pos_second = 0
        pos_third = 0

        for index, char in enumerate(s):
            if first_next:
                while pos_first > 0 and p[pos_first] != char:
                    pos_first = first_next[pos_first - 1]
                if p[pos_first] == char:
                    pos_first += 1
                    if pos_first == len(first_next):
                        first_hit.append(index - pos_first + 1)
                        pos_first = first_next[pos_first - 1]
            
            if second_next:
                while pos_second > 0 and p[pos_second + len(first_next) + 1] != char:
                    pos_second = second_next[pos_second - 1]
                if p[pos_second + len(first_next) + 1] == char:
                    pos_second += 1
                    if pos_second == len(second_next):
                        second_hit.append(index - pos_second + 1)
                        pos_second = second_next[pos_second - 1]
            
            if third_next:
                while pos_third > 0 and p[pos_third + len(first_next) + 1 + len(second_next) + 1] != char:
                    pos_third = third_next[pos_third - 1]
                if p[pos_third + len(first_next) + 1 + len(second_next) + 1] == char:
                    pos_third += 1
                    if pos_third == len(third_next):
                        third_hit.append(index - pos_third + 1)
                        pos_third = third_next[pos_third - 1]
        
        res = -1
        if first_next and second_next and third_next:
            first_index = 0
            second_index = 0
            third_index = 0
            while first_index < len(first_hit):
                while second_index < len(second_hit) and first_hit[first_index] + len(first_next) > second_hit[second_index]:
                    second_index += 1
                if second_index < len(second_hit):
                    while third_index < len(third_hit) and second_hit[second_index] + len(second_next) > third_hit[third_index]:
                        third_index += 1
                    
                    if third_index < len(third_hit):
                        length = third_hit[third_index] + len(third_next) - 1 - first_hit[first_index] + 1
                        if res == -1 or res > length:
                            res = length
                
                first_index += 1
        
        else:
            if first_next:
                left_part = first_hit
                left_length = len(first_next)
                if second_next:
                    right_part = second_hit
                    right_length = len(second_next)
                elif third_next:
                    right_part = third_hit
                    right_length = len(third_next)
                else:
                    right_part = None
                    right_length = 0
            
            elif second_next:
                left_part = second_hit
                left_length = len(second_next)
                if third_next:
                    right_part = third_hit
                    right_length = len(third_next)
                else:
                    right_part = None
                    right_length = 0
            
            else:
                if third_next:
                    left_part = third_hit
                    left_length = len(third_next)
                else:
                    left_part = None
                    left_length = 0
                right_part = None
                right_length = 0

            if right_part is None:
                if left_part is not None and len(left_part) == 0:
                    res = -1
                else:
                    res = left_length
            else:
                left_index = 0
                right_index = 0
                while left_index < len(left_part):
                    while right_index < len(right_part) and left_part[left_index] + left_length > right_part[right_index]:
                        right_index += 1
                
                    if right_index < len(right_part):
                        length = right_part[right_index] + right_length - 1 - left_part[left_index] + 1
                        if res == -1 or res > length:
                            res = length

                    left_index += 1
            
        return res
''',
    call="Solution().shortestMatchingSubstring('abbc', 'a*b*c')",
    expect=4,
    views=[
        dict(type='string', var='s', h=250, label='s（蓝 = first，绿 = second，橙 = third 的命中位置）',
             color=_cols, pointers={_idx: 'yellow'}, pointer_labels={_idx: 'index'}, cell=90),
        dict(type='text', fn=_text, h=90),
    ],
    watch=[('first_index', 'first_index', 'blue'), ('second_index', 'second_index', 'green'), ('third_index', 'third_index', 'orange'), ('res', 'res', 'yellow')],
    skip=['first_next = []', 'second_next = []', 'third_next = []', 'start = -1', 'if start == len(p)', 'f.append(0)', 'pos = 0', 'now = start + 1',
          'first_hit = []', 'second_hit = []', 'third_hit = []', 'pos_first = 0', 'pos_second = 0', 'pos_third = 0',
          'if first_next:', 'if second_next:', 'if third_next:', 'while pos_first > 0', 'while pos_second > 0', 'while pos_third > 0',
          'pos_first += 1', 'pos_second += 1', 'pos_third += 1', 'pos_first = first_next[', 'pos_second = second_next[', 'pos_third = third_next[',
          'first_index = 0', 'second_index = 0', 'third_index = 0', 'res = -1', 'now < len(p) and p[now]'],
    max_steps=80,
    captions={
        'start = get_next(start + 1, first_next)': '`get_next` 算第一段的 next 数组（KMP 的失配回退表），返回这一段结束的位置',
        'start = get_next(start + 1, second_next)': '同样切出第二段，算它的 next 数组',
        'start = get_next(start + 1, third_next)': '第三段也算一份 next 数组',
        'return now': '这一段的 next 数组长度 `{len(f)}`，这一段到 p 的下标 `{now}` 为止（`*` 或结尾）',
        'for index, char in enumerate(s)': lambda S, B, r: ('`s` 扫描完了，三个命中数组都有了' if getattr(B, 'index', None) == S.index else f"一趟扫描 `s`：读入 `s[{S.index}] = '{S.char}'`，三段同时往后匹配"),
        'if p[pos_first] == char': lambda S, B, r: f"first 段：`'{S.p[S.pos_first]}'` 对 `'{S.char}'` → " + ('==匹配，pos_first 加 1==' if S.p[S.pos_first] == S.char else '失配'),
        'if pos_first == len(first_next)': lambda S, B, r: ('first 段整段匹配完！' if S.pos_first == len(S.first_next) else 'first 段还没匹配完'),
        'first_hit.append': '记下 first 的命中起点 `{index - pos_first + 1}` → `first_hit = {first_hit}`',
        'if p[pos_second + len(first_next) + 1] == char': lambda S, B, r: f"second 段：`'{S.p[S.pos_second + len(S.first_next) + 1]}'` 对 `'{S.char}'` → " + ('==匹配==' if S.p[S.pos_second + len(S.first_next) + 1] == S.char else '失配'),
        'if pos_second == len(second_next)': lambda S, B, r: ('second 段整段匹配完！' if S.pos_second == len(S.second_next) else 'second 段还没匹配完'),
        'second_hit.append': '记下 second 的命中起点 `{index - pos_second + 1}` → `second_hit = {second_hit}`',
        'if p[pos_third + len(first_next)': lambda S, B, r: f"third 段：`'{S.p[S.pos_third + len(S.first_next) + 1 + len(S.second_next) + 1]}'` 对 `'{S.char}'` → " + ('==匹配==' if S.p[S.pos_third + len(S.first_next) + 1 + len(S.second_next) + 1] == S.char else '失配'),
        'if pos_third == len(third_next)': lambda S, B, r: ('third 段整段匹配完！' if S.pos_third == len(S.third_next) else 'third 段还没匹配完'),
        'third_hit.append': '记下 third 的命中起点 `{index - pos_third + 1}` → `third_hit = {third_hit}`',
        'if first_next and second_next and third_next': '三段都非空：走“三个下标”的主流程；有空段的话走后面的 else 分支',
        'while first_index < len(first_hit)': lambda S, B, r: ('`first_index` 遍历 first 的每个命中位置' + (f'：现在是 `{S.first_hit[S.first_index]}`' if S.first_index < len(S.first_hit) else '，已遍历完')),
        'first_hit[first_index] + len(first_next) > second_hit[second_index]': lambda S, B, r: ('条件1：second 的起点必须 >= first 命中位置 + 长度，否则重叠 → ' + ('second_index 右移' if S.second_index < len(S.second_hit) and S.first_hit[S.first_index] + len(S.first_next) > S.second_hit[S.second_index] else '`second_hit[%d] = %d` 满足，不重叠' % (S.second_index, S.second_hit[S.second_index])) if S.second_index < len(S.second_hit) else '`second_hit` 用完'),
        'if second_index < len(second_hit)': lambda S, B, r: ('找到了不重叠的 second' if S.second_index < len(S.second_hit) else 'second 没有了，这个 first 无解'),
        'second_hit[second_index] + len(second_next) > third_hit[third_index]': lambda S, B, r: ('条件2：third 的起点必须 >= second 命中位置 + 长度 → ' + ('third_index 右移' if S.third_index < len(S.third_hit) and S.second_hit[S.second_index] + len(S.second_next) > S.third_hit[S.third_index] else '`third_hit[%d] = %d` 满足' % (S.third_index, S.third_hit[S.third_index]))) if S.third_index < len(S.third_hit) else '`third_hit` 用完',
        'if third_index < len(third_hit)': lambda S, B, r: ('找到了不重叠的 third' if S.third_index < len(S.third_hit) else 'third 没有了'),
        'length = third_hit': '条件3：长度 = third 最后一个字母的下标 − first 首字母下标 + 1 = `{third_hit[third_index]} + {len(third_next)} − 1 − {first_hit[first_index]} + 1` = =={length}==',
        'if res == -1 or res > length': '`res = {res}`，当前长度 `{length}`：还没有答案或者更短就更新',
        'res = length': '最短长度更新为 =={res}==',
        'first_index += 1': '换下一个 first，`second_index`、`third_index` 不回退（位置有序，只增不减）',
        'return res': '答案 `{res}`（`-1` 表示没有匹配）',
    },
    cards=dict(
        one_liner='三段命中位置各自有序，first_index、second_index、third_index 只往后走',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['`p` 恰好有两个 `*`，`*` 能匹配任意个字符',
                 '要在 `s` 里找与 `p` 匹配的最短子串，返回长度，没有返回 `-1`',
                 '本视频：`s = "abbc"`，`p = "a*b*c"` → `4`'],
        quote='随着 first_index 的向后移动，first_hit[first_index] + len(first) 也会跟着向后移动，因此 second_index 也必然会在之前的基础上向后移动；同理，third_index 也会随着 second_index 的移动而移动。',
        quote_src='—— yiduobo 题解原文',
        idea=['星号切出 `first`、`second`、`third`，用 KMP 一趟扫描 `s` 同时得到三个命中数组',
              '要求 `first` 在前、`second` 居中、`third` 在后，三者互不重叠，三个命中数组都是升序',
              '遍历 `first_index`，`second_index` 找刚好不重叠的那个，`third_index` 同理，长度取最小',
              '星号在开头、末尾或相邻（出现空段）时，在 `else` 里另算'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '易错：不重叠的条件是 `first_hit + len(first) <= second_hit`，不是 `<`',
                 '易错：长度是 `third_hit + len(third) - 1 - first_hit + 1`',
                 '原文是 Python 3 可直接运行的写法，没有改动；演示输入没有空段，不会走 `else`',
                 '对比灵神：灵神把空串看作匹配所有位置，省掉了 `else` 里的分类讨论'],
    ),
)
