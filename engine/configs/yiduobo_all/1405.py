CONFIG = dict(
    num=1405, title='最长快乐字符串', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='最大堆 · 最多的连放两个，次多的做间隔',
    tags=['常用数据结构', '贪心与思维'],
    code='''
class Solution(object):
    def longestDiverseString(self, a, b, c):

        res = []
        heap = []
        if a > 0:
            heapq.heappush(heap, [-a, 'a'])
        if b > 0:
            heapq.heappush(heap, [-b, 'b'])
        if c > 0:
            heapq.heappush(heap, [-c, 'c'])
        while heap:
            if len(heap) == 1:
                cnt, char = heap[0]
                res.append(char)
                if cnt <= -2:
                    res.append(char)
                
                break
            
            else:
                cnt1, char1 = heapq.heappop(heap)
                cnt2, char2 = heapq.heappop(heap)
                if cnt1 == cnt2:
                    res.append(char1)
                    res.append(char2)
                    if cnt1 <= -2:
                        res.append(char1)
                        res.append(char2)
                        cnt1 += 1
                        cnt2 += 1
                    cnt1 += 1
                    cnt2 += 1
                else:
                    res.append(char1)
                    if cnt1 <= -2:
                        res.append(char1)
                        cnt1 += 1
                    cnt1 += 1
                    res.append(char2)
                    cnt2 += 1
        
                if cnt1 < 0:
                    heapq.heappush(heap, [cnt1, char1])
                if cnt2 < 0:
                    heapq.heappush(heap, [cnt2, char2])
            

        return ''.join(res)
''',
    call='Solution().longestDiverseString(4, 2, 1)',
    expect='aabaabc',
    views=[
        dict(type='heap', var='heap', label='heap', fmt=lambda x: f'{x[1]}×{-x[0]}', h=170),
        dict(type='string', var=lambda S: ''.join(S.get('res') or []), label='res（已拼好的字符串）', h=190),
        dict(type='text', fn=lambda S: '规则：==最多的字符连放两个==，再放一个次多的做间隔 → 不会出现三连', size=26, h=70),
    ],
    watch=['cnt1', 'char1', 'cnt2', 'char2', ('len(res)', 'len(res)', 'green')],
    captions={
        'heapq.heappush(heap, [-a': '`a` 有 `{a}` 个，入堆（次数取负）',
        'heapq.heappush(heap, [-b': '`b` 有 `{b}` 个，入堆',
        'heapq.heappush(heap, [-c': '`c` 有 `{c}` 个，入堆',
        'if len(heap) == 1': '堆里还有 `{len(heap)}` 种字符：{"==只剩一种，没有间隔字符了==" if len(heap) == 1 else "至少两种，可以最多的配次多的"}',
        'cnt, char = heap[0]': '只剩 `{char}`，还有 `{-cnt}` 个',
        'if cnt <= -2': '只剩一种，至多再放 2 个（不能三连）：{"==放两个==" if cnt <= -2 else "放一个"}，然后结束',
        'cnt1, char1 = heapq.heappop': '弹出最多的 `{char1}`（剩 `{-cnt1}` 个）',
        'cnt2, char2 = heapq.heappop': '弹出次多的 `{char2}`（剩 `{-cnt2}` 个）',
        'if cnt1 == cnt2': '最多与次多{"==一样多=="if cnt1 == cnt2 else "==不一样多=="}（`{-cnt1}` vs `{-cnt2}`）→ {"间隔要放两个，免得之后一方独大" if cnt1 == cnt2 else "间隔只放一个"}',
        'if cnt1 <= -2': '`{char1}` 剩 `{-cnt1}` 个，{"==够两个，连放两个=="if cnt1 <= -2 else "只够放一个"}',
        'cnt1 += 1': '`{char1}` 又用掉一个，剩 `{-cnt1}` 个',
        'cnt2 += 1': '`{char2}` 用掉一个，剩 `{-cnt2}` 个',
        'res.append(char2)': '放 `{char2}` 作间隔，当前 res = `{"".join(res)}`',
        'if cnt1 < 0': '`{char1}` 还剩 `{-cnt1}` 个 → {"==放回堆里=="if cnt1 < 0 else "用完，不再放回"}',
        'if cnt2 < 0': '`{char2}` 还剩 `{-cnt2}` 个 → {"==放回堆里=="if cnt2 < 0 else "用完，不再放回"}',
    },
    cards=dict(
        one_liner='最多的连放两个，次多的当间隔',
        complexity='时间 `O(n log 3)`≈`O(n)`，空间 `O(1)`',
        problem=['给 `a`、`b`、`c`：最多可用多少个 `a`、`b`、`c`，拼成字符串',
                 '要求 ==不能出现三个连续相同字符==，求最长的快乐字符串',
                 '示例：`a=4, b=2, c=1` → 一个长度为 7 的字符串，如 `aabaabc`'],
        quote='每次都使用两个当前余下最多的那种字符f，然后选择次多的字符s作为间隔。当出现f与s出现的次数一致时，这里的间隔使用两个s，否则使用一个s。',
        quote_src='—— yiduobo 题解',
        idea=['最多的字符最容易被卡住，所以每轮先连放它两个',
              '次多的放一个当间隔，打断连续；一样多就两个 s，尽快拉平',
              '最少的 t 暂时不管，极限时它会多出两个，后面的轮次能消化掉'],
        summary=['时间 `O(n)`（字符种类固定为 3），空间 `O(1)`',
                 '堆里存 `[-次数, 字符]`，次数取负得最大堆',
                 '易错：只剩一种字符时最多再放 2 个，放完就 `break`',
                 '原文为 Python 2 写法，本题代码无需修改即可在 Python 3 运行'],
    ),
)
