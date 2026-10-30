def _cover(S, i, v):
    for a, b in S.get('intervals', []):
        if a <= i <= b:
            return 'cyan'
    return None


def _win_color(S, i, v):
    if 'lastx' in S and S['lastx'] <= i <= S['lasty']:
        return 'yellow'
    return _cover(S, i, v)


def _res(S):
    r = S.get('res')
    if r is None:
        return ''
    return '已拼好：`' + ''.join(r) + '`'


CONFIG = dict(
    num=616, title='给字符串添加粗标签', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='暴力 find + 区间合并',
    code='''
class Solution(object):
    def addBoldTag(self, s, words):

        n = len(s)
        intervals = []

        for word in words:
            start_pos = 0
            while True:
                p = s.find(word, start_pos)
                if p == -1:
                    break
                
                intervals.append([p, p + len(word) - 1])
                start_pos = p + 1
        
        if not intervals:
            return s

        intervals.sort(key = lambda d:d[0])
        lastx, lasty = intervals[0]
        res = []
        p = 0
        for x, y in intervals[1:]:
            if x <= lasty + 1:
                lasty = max(y, lasty)
            else:
                res.append(s[p : lastx])
                res.append('<b>')
                res.append(s[lastx : lasty + 1])
                res.append('</b>')
                p = lasty + 1
                lastx, lasty = x, y

        res.append(s[p : lastx])
        res.append('<b>')
        res.append(s[lastx : lasty + 1])
        res.append('</b>')
        res.append(s[lasty + 1:])
        return ''.join(res)
''',
    call='Solution().addBoldTag("abcxyz123", ["abc", "123", "bc"])',
    expect='<b>abc</b>xyz<b>123</b>',
    views=[
        dict(type='string', var='s', label='s（青 = 被某个单词盖住，黄 = 正在合并的区间）',
             pointers={'p': 'pink'}, pointer_labels={'p': 'p'}, color=_win_color, h=200),
        dict(type='text', fn=lambda S: ('区间（闭）：' + '  '.join(f'`[{a},{b}]`' for a, b in S['intervals'])) if S.get('intervals') else '', size=26),
        dict(type='text', fn=_res, size=26),
    ],
    watch=['word', 'p', 'lastx', 'lasty', ('intervals', 'intervals', 'cyan')],
    skip=['n = len(s)', 'intervals = []', 'res = []'],
    captions={
        'for word in words': lambda S, B, r: (f'处理单词 `{S.word}`：找出它在 `s` 里的所有出现位置' if S.word != B.get('word') or 'word' not in B else '所有单词都找完了'),
        'start_pos = 0': '从下标 `0` 开始找 `{word}`',
        'p = s.find': lambda S, B, r: (f'`s.find("{S.word}", {S.start_pos})` = `{S.p}`' + ('：没有更多了' if S.p == -1 else '：找到一处')),
        'if p == -1': lambda S, B, r: ('`p == -1` → 这个单词找完了，==break==' if S.p == -1 else '`p != -1` → 记下这一处'),
        'intervals.append': '记下闭区间 `[{p}, {p + len(word) - 1}]`',
        'start_pos = p + 1': '从 `p + 1` 继续找：==出现可以重叠==，不能跳过整个单词',
        'if not intervals': lambda S, B, r: ('没有任何匹配，原样返回 `s`' if not S.intervals else '有 `{}` 个区间，继续合并'.format(len(S.intervals))),
        'intervals.sort': '按起点排序，这样合并时只需看当前区间和上一个',
        'lastx, lasty = intervals[0]': '当前合并区间 = 第一个区间 `[{lastx}, {lasty}]`',
        'p = 0': '`p` = 已经输出到的位置',
        'for x, y in intervals[1:]': lambda S, B, r: (f'看下一个区间 `[{S.x}, {S.y}]`' if (S.x, S.y) != (B.get('x'), B.get('y')) else '区间都处理完了，收尾'),
        'if x <= lasty + 1': lambda S, B, r: (f'`{S.x} <= {S.lasty} + 1` → 重叠或紧挨着，==合并=='
                                               if S.x <= S.lasty + 1 else f'`{S.x} > {S.lasty} + 1` → 中间有空隙，上一段合并完成'),
        'lasty = max(y, lasty)': '右端点取较大者：`lasty = {lasty}`（被包含时不变）',
        "res.append(s[p : lastx])": '先放下粗体区间前面没加粗的部分 `s[{p}:{lastx}]`',
        "res.append('<b>')": '加上 `<b>`',
        'res.append(s[lastx : lasty + 1])': '放入被加粗的部分 `s[{lastx}:{lasty + 1}]`',
        "res.append('</b>')": '加上 `</b>`',
        'p = lasty + 1': '`p` 移到这一段之后：`{p}`',
        'lastx, lasty = x, y': '新的合并区间从 `[{x}, {y}]` 开始',
        's[lasty + 1:]': '最后一段粗体之后剩下的部分也要放进去（可能为空）',
        'return': '拼接得到 `{ret}`',
    },
    cards=dict(
        one_liner='先把所有出现位置找出来，再合并重叠区间',
        complexity='时间 `O(Σ|word|·n)`，空间 `O(n)`',
        problem=['给字符串 `s` 和单词列表 `words`，把 `s` 中出现的 `words` 子串用 `<b>` `</b>` 加粗',
                 '重叠或相邻的加粗区间要合并成一对标签',
                 '本视频：`s = "abcxyz123"`，`words = ["abc","123","bc"]` → `<b>abc</b>xyz<b>123</b>`'],
        quote='直接遍历words中的所有单词，使用字符串的find函数找出其出现的所有位置，并将对应的区间记录下来。……将这些区间按起点从小到大排序后进行合并。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模小：每个单词用 `find` 暴力找出所有出现位置，得到闭区间 `[p, p+len-1]`',
              '按起点排序后扫描：`x <= lasty + 1`（重叠或紧挨）就合并，否则把上一段输出',
              '`p` 记录已输出的位置，加粗区间之间的部分原样放入答案'],
        summary=['时间 `O(Σ|word|·n)`，空间 `O(n)`',
                 '易错：`start_pos = p + 1`，不能 `p + len(word)`，否则漏掉重叠出现',
                 '易错：合并条件是 `x <= lasty + 1`，相邻（如 `[0,1]` 和 `[2,3]`）也要合并',
                 '最后一段要在循环外手动输出，别忘了尾部 `s[lasty + 1:]`',
                 '原文本就能在 Python 3 运行，代码无改动'],
    ),
)
