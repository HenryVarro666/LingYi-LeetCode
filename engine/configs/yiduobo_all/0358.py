CONFIG = dict(
    num=358, title='K距离间隔重排字符串', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='最大堆 + 上次出现位置',
    tags=['常用数据结构', '贪心与思维'],
    code='''
class Solution(object):
    def rearrangeString(self, s, k):

        cnt_dict = {}
        for char in s:
            cnt_dict[char] = cnt_dict.get(char, 0) + 1
        
        heap = []
        for char, cnt in cnt_dict.items():
            heapq.heappush(heap, [-cnt, char])

        res = []
        last_pos = {}
        for index in range(len(s)):
            tmp = []
            while heap and (heap[0][1] in last_pos and index - last_pos[heap[0][1]] < k):
                tmp.append(heapq.heappop(heap))
            
            if not heap:
                return ""

            cnt, char = heapq.heappop(heap)
            res.append(char)
            last_pos[char] = index
            if cnt + 1 != 0:
                heapq.heappush(heap, [cnt + 1, char])
            

            for cnt, char in tmp:
                heapq.heappush(heap, [cnt, char])

        return "".join(res)
''',
    call='Solution().rearrangeString("aaabbc", 2)',
    expect='ababac',
    views=[
        dict(type='string', var='s', label='s', h=150),
        dict(type='map', var='last_pos', label='last_pos（字符 → 上次放的位置）', fmt=lambda k, v: f'{k}: {v}', h=110),
        dict(type='heap', var='heap', label='heap', fmt=lambda x: f'{x[1]}×{-x[0]}', h=130),
        dict(type='heap', var='tmp', label='tmp（暂时冷却，稍后放回）', fmt=lambda x: f'{x[1]}×{-x[0]}', h=110),
        dict(type='string', var=lambda S: ''.join(S.get('res') or []), label='res', h=150),
    ],
    watch=['index', 'k', 'char', ('res', lambda S: ''.join(S.get('res') or []), 'green')],
    captions={
        'cnt_dict[char] =': '统计次数：`{char}` 出现 =={cnt_dict[char]}== 次',
        'heapq.heappush(heap, [-cnt, char])': '`{char}` 剩 `{cnt}` 个入堆（取负）→ ==堆顶永远是剩余最多的==',
        'for index in range': '{"==所有位置都填完了==" if "index" in B and B["index"] == index and len(res) == len(s) else "填第 `" + str(index) + "` 个位置：选剩余最多、且离上次出现 >= `" + str(k) + "` 的字符"}',
        'while heap and': '{"堆顶 `" + heap[0][1] + "` 还没用过 → 可以用" if heap and heap[0][1] not in last_pos else ("堆顶 `" + heap[0][1] + "` 上次在位置 `" + str(last_pos[heap[0][1]]) + "`，距今 `" + str(index - last_pos[heap[0][1]]) + "`，是否 < `" + str(k) + "`？" + ("==太近，先拿出来放进 tmp==" if index - last_pos[heap[0][1]] < k else "够远了，可以用它")) if heap else "堆已空 → 没有可用字符"}',
        'tmp.append': '`{tmp[-1][1]}` 还在冷却期，先放进 `tmp`，等放完当前位置再放回',
        'if not heap': '堆空了吗？{"==是：所有字符都太近 → 无解，返回空串==" if not heap else "否，堆里还有可用字符"}',
        'cnt, char = heapq.heappop': '取出可用字符里剩余最多的：`{char}`（剩 `{-cnt}` 个）',
        'res.append(char)': '位置 `{index}` 放 `{char}`，res = `{"".join(res)}`',
        'last_pos[char] = index': '记下 `{char}` 最近放在位置 `{index}`，之后 `{k}` 步内不能再用',
        'if cnt + 1 != 0': '`{char}` 用掉一个后还剩 `{-(cnt + 1)}` 个 → {"==放回堆里=="if cnt + 1 != 0 else "用完了，不再放回"}',
        'for cnt, char in tmp': '{"位置 `" + str(index) + "` 填完了，把 `tmp` 里躲开的字符放回堆里" if tmp else "位置 `" + str(index) + "` 填完了，`tmp` 是空的，没有要放回的"}',
        'heapq.heappush(heap, [cnt, char])': '`{char}` 重新入堆（剩 `{-cnt}` 个）',
    },
    cards=dict(
        one_liner='每个位置选剩余最多、且离上次够远的字符',
        complexity='时间 `O(n log k)`，空间 `O(n)`',
        problem=['字符串 `s` 和整数 `k`：重排字符，使 ==相同字符之间至少隔 k 个位置==',
                 '做不到就返回空串 `""`',
                 '示例：`s="aaabbc", k=2` → `"ababac"`'],
        quote='对于每个位置都应该填充当前剩余数量最多，且上一次出现位置在k个字符之前的字符。为了高效取出剩余次数最多的字符，可以使用一个堆来维护……另外还需要使用一个哈希表来记录每种字符上一次使用的下标位置。',
        quote_src='—— yiduobo 题解',
        idea=['剩得多的字符最难安排，所以每个位置优先用它',
              '`last_pos` 记录每个字符上次放的位置，距离 `< k` 的先放进 `tmp` 躲一躲',
              '放完当前位置再把 `tmp` 放回堆；堆里没有可用字符就无解'],
        summary=['时间 `O(n log k)`，空间 `O(n)`（k 为字符种类数）',
                 '易错：被跳过的字符要放回堆里，否则会丢字符',
                 '`k <= 1` 时任意排列都满足；本写法对此也成立',
                 '原文为 Python 2 写法，本题代码无需修改即可在 Python 3 运行'],
    ),
)
