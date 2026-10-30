import heapq as _hq

WORDS = ["code", "love", "i", "love", "code", "you", "i", "love"]
K = 3


def _pos(S):
    ln = S.get('_line')
    d = S.get('word_dict')
    if d is None:
        return None
    tot = sum(d.values())
    if ln == 5:
        return tot
    if ln == 6:
        return tot - 1
    return None


def _words(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ws = S.get('words') or WORDS
    p = _pos(S)
    ln = S.get('_line') or 0
    cv.text((x0 + 18, y0 + 4), 'words', 22, T['muted'], bold=True)
    X, Y = x0 + 20, y0 + 40
    for k, w in enumerate(ws):
        wd = cv.tlen(w, 24, True, True) + 28
        if k == p:
            fill, tc = T['blue'], T['bg']
        elif (p is not None and k < p) or ln >= 8:
            fill, tc = T['green'], T['bg']
        else:
            fill, tc = T['panel2'], T['text']
        cv.rect((X, Y, X + wd, Y + 46), fill=fill, r=8, outline=T['border'])
        cv.text((X + wd / 2, Y + 23), w, 24, tc, anchor='mm', bold=True, mono=True)
        cv.text((X + wd / 2, Y + 52), k, 16, T['dim'], anchor='mt', mono=True)
        X += wd + 10


def _node_xy(i, box):
    x0, y0, x1, y1 = box
    depth = (i + 1).bit_length() - 1
    first = (1 << depth) - 1
    cnt = 1 << depth
    slot = (x1 - x0) / cnt
    return x0 + slot * (i - first + 0.5), y0 + 84 + depth * 92


def _draw_heap(cv, h, box, T, hl=None, title=''):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    for i in range(1, len(h)):
        a, b = _node_xy((i - 1) // 2, box), _node_xy(i, box)
        cv.line([a, b], T['border'], 3)
    for i, (nf, w) in enumerate(h):
        X, Y = _node_xy(i, box)
        txt = f'{w}:{-nf}'
        wd = cv.tlen(txt, 24, True, True) + 28
        c = T['purple'] if i == 0 else T['panel2']
        if hl is not None and i in hl:
            c = T['yellow']
        cv.rect((X - wd / 2, Y - 24, X + wd / 2, Y + 24), fill=c, r=12, outline=T['border'])
        cv.text((X, Y), txt, 24, T['bg'] if c != T['panel2'] else T['text'], anchor='mm', bold=True, mono=True)


def _heap(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ln = S.get('_line')
    h = S.get('heap')
    if h is None:
        return
    if ln == 11:
        # the inlined list comprehension collapses into one step, so rebuild the heap right after heapify
        hb = [[-f, w] for w, f in S['word_dict'].items()]
        _hq.heapify(hb)
        half = (x1 - x0) * 0.55
        _draw_heap(cv, hb, (x0, y0, x0 + half, y1), T, title='heapify 后的堆（紫 = 堆顶）')
        cv.text((x0 + half + 10, y0 + 4), f'弹出 k = {S["k"]} 次堆顶', 22, T['muted'], bold=True)
        tmp = [list(x) for x in hb]
        for r in range(S['k']):
            nf, w = _hq.heappop(tmp)
            Y = y0 + 60 + r * 64
            cv.rect((x0 + half + 20, Y, x1 - 20, Y + 50), fill=T['green'], r=10)
            cv.text((x0 + half + 36, Y + 25), f'第 {r + 1} 次：[{nf}, "{w}"] → "{w}"', 24, T['bg'], anchor='lm', bold=True, mono=True)
        return
    bh = B.get('heap')
    hl = None
    if ln == 9 and bh is not None:
        hl = {i for i in range(len(h)) if bh[i] != h[i]}
    title = 'heap：[-频率, 单词] 的小根堆（节点写成 单词:频率，紫 = 堆顶）' if ln != 8 else 'heap（刚建好的列表，还不是堆）'
    _draw_heap(cv, [list(x) for x in h], box, T, hl=hl, title=title)


CONFIG = dict(
    num=692, title='前K个高频单词', difficulty='Medium', category='堆',
    author='yiduobo', technique='计数 + heapify + 弹出 k 次',
    tags=['字节30天'],
    code='''
import heapq
class Solution(object):
    def topKFrequent(self, words, k):
        word_dict = {}
        for word in words:
            word_dict[word] = word_dict.get(word, 0) + 1

        heap = [[-freq, word] for word, freq in word_dict.items()]
        heapq.heapify(heap)

        return [heapq.heappop(heap)[1] for index in range(k)]
''',
    call=f'Solution().topKFrequent({WORDS!r}, {K})',
    expect=['love', 'code', 'i'],
    views=[
        dict(type='custom', draw=_words, h=110),
        dict(type='map', var='word_dict', label='word_dict（单词 → 出现次数）', h=110, font=26,
             fmt=lambda k, v: f'{k}: {v}'),
        dict(type='custom', draw=_heap, h=330),
    ],
    watch=[('word', 'word', 'blue'), ('k', 'k')],
    captions={
        'word_dict = {}': '先统计每个单词的出现次数',
        'for word in words': lambda S, B, ret: (f'下一个单词 `"{S.word}"`' if _pos(S) < len(S.words) else '统计完毕'),
        'word_dict[word] = word_dict.get': '`word_dict["{word}"]` → =={word_dict[word]}==',
        'heap = [[-freq, word]': '每个单词变成 `[-频率, 单词]`：==频率取负==，小根堆的堆顶就是频率最高的',
        'heapq.heapify(heap)': '`heapify` 原地建堆，`O(n)`：堆顶 `[{heap[0][0]}, "{heap[0][1]}"]`',
        'return [heapq.heappop': '弹出 `k = {k}` 次堆顶：频率相同时 `[-f, word]` 按==单词字典序==比较 → `{ret}`',
    },
    cards=dict(
        one_liner='把 [-频率, 单词] 建成小根堆，弹出 k 次就是答案',
        complexity='时间 `O(n + k log n)`，空间 `O(n)`',
        problem=['给定单词列表 `words` 和整数 `k`，返回出现次数==最多==的 `k` 个单词',
                 '按频率从高到低；频率相同时按==字典序==从小到大',
                 '示例：`["i","love","leetcode","i","love","coding"]`，`k = 2` → `["i","love"]`',
                 f'本视频：`k = {K}`，答案 `["love","code","i"]`（code 和 i 都出现 2 次）'],
        quote='看到这里的logk自然就想到了维护一个大小为k的堆。建堆的时间复杂度为O(n)，每次弹出元素的时间复杂度为O(logk)，一共需要弹出k次，因此最终的时间复杂度为O(n + klogk)。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用字典统计每个单词的频率',
              '`[-freq, word]` 放进列表直接 `heapify`：取负让小根堆变成「频率大的在上」',
              '列表比较先比 `-freq`，再比 `word` → 频率相同自动按字典序，==正好符合题意==',
              '最后弹出 `k` 次堆顶'],
        summary=['时间 `O(n + k log n)`：建堆 `O(n)` + 弹出 `k` 次',
                 '取负 + 列表比较，一次解决「频率降序、字典序升序」两个排序要求',
                 '注意：这里堆里放的是全部单词（大小为 m），弹出代价是 `log m`',
                 '想做到严格的 `O(n log k)`：维护大小为 `k` 的堆，但比较规则要反过来写',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
