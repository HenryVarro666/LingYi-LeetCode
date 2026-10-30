CONFIG = dict(
    num=767, title='重构字符串', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='最大堆 · 每轮取次数最多的两个字母',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1681'],
    code='''
import heapq

class Solution(object):
    def reorganizeString(self, S):

        count_dict = {}
        for char in S:
            count_dict[char] = count_dict.get(char, 0) + 1
        
        if max(count_dict.values()) > (len(S) + 1) // 2:
            return ''

        heap = []
        for key, value in count_dict.items():
            heapq.heappush(heap, (-value, key))
        
        res = []
        while heap:
            cnt1, char1 = heapq.heappop(heap)
            cnt1 += 1
            res.append(char1)

            if heap:
                cnt2, char2 = heapq.heappop(heap)
                cnt2 += 1
                res.append(char2)
            
            if cnt1:
                heapq.heappush(heap, (cnt1, char1))
                if cnt2:
                    heapq.heappush(heap, (cnt2, char2))
            
        return ''.join(res)
''',
    call='Solution().reorganizeString("aaabbc")',
    expect='ababac',
    views=[
        dict(type='string', var='S', label='S', h=115),
        dict(type='map', var='count_dict', label='每个字母出现的次数', h=110),
        dict(type='heap', var='heap', label='heap（次数取负，堆顶 = 次数最多）', fmt=lambda x: f'{x[1]}×{-x[0]}', top_color='blue', h=130),
        dict(type='array', var='res', label='res（已排好的字母）', h=130),
    ],
    watch=[('char1', 'char1', 'blue'), ('cnt1', 'cnt1', 'blue'), ('char2', 'char2', 'pink'), ('cnt2', 'cnt2', 'pink'), ('堆里还剩', lambda S: len(S['heap']) if 'heap' in S else 0, 'cyan')],
    captions={
        'count_dict = {}': '先数一数每个字母出现几次',
        'for char in S': lambda S, B, r: ('数完了' if len(S.get('count_dict', {})) and sum(S.count_dict.values()) == len(S.S) else '看下一个字母'),
        'count_dict[char] =': '`{char}` 的次数 → {count_dict[char]}',
        'if max(count_dict.values())': lambda S, B, r: (
            f'最多的字母 {max(S.count_dict.values())} 次 > 长度的一半向上取整 {(len(S.S) + 1) // 2}：==必有两个相邻== → 无解'
            if max(S.count_dict.values()) > (len(S.S) + 1) // 2 else
            f'最多的字母 {max(S.count_dict.values())} 次 ≤ 一半向上取整 {(len(S.S) + 1) // 2}：有解，用堆来构造'),
        'heap = []': '用堆维护每个字母剩余次数，次数取负变成最大堆',
        'heapq.heappush(heap, (-value, key))': '放入 `({-value}, {key!r})`：次数取负，堆顶就是次数最多的',
        'res = []': '`res` 存答案',
        'while heap': lambda S, B, r: (f'堆里还有 {len(S.heap)} 种字母，开始新一轮' if S.heap else '堆空了，全部排完'),
        'cnt1, char1 = heapq.heappop(heap)': '取出==次数最多==的字母 `{char1}`（还剩 {-cnt1} 次）',
        'cnt1 += 1': '用掉一个 `{char1}`：负次数加 1 → 还剩 {-cnt1} 次',
        'res.append(char1)': '`{char1}` 排到答案末尾',
        'if heap:': lambda S, B, r: ('堆里还有字母，再取==次数第二多==的' if S.heap else '堆空了，这一轮只能放一个字母'),
        'cnt2, char2 = heapq.heappop(heap)': '取出第二多的 `{char2}`（还剩 {-cnt2} 次）：它和 `{char1}` 不同，所以挨着放不会重复',
        'cnt2 += 1': '用掉一个 `{char2}`：还剩 {-cnt2} 次',
        'res.append(char2)': '`{char2}` 紧跟在后面',
        'if cnt1:': lambda S, B, r: (f'`{S.char1}` 还有 {-S.cnt1} 次，放回堆里' if S.cnt1 else f'`{S.char1}` 用完了，不放回'),
        'heapq.heappush(heap, (cnt1, char1))': '`{char1}` 放回堆',
        'if cnt2:': lambda S, B, r: (f'`{S.char2}` 还有 {-S.cnt2} 次，放回堆里' if S.cnt2 else f'`{S.char2}` 用完了，不放回'),
        'heapq.heappush(heap, (cnt2, char2))': '`{char2}` 放回堆',
        "return ''.join": '拼起来 =={ret}==，相邻都不同',
    },
    max_steps=90,
    cards=dict(
        one_liner='每一轮从堆里取次数最多的两个字母，各用一次再放回',
        complexity='时间 `O(n + |Σ|log|Σ|)`，空间 `O(n)`',
        problem=['重排字符串 `s`，使任意两个相邻字符不同；不行就返回空串',
                 '`aab` → `aba`；`aaab` → `""`',
                 '本视频：`aaabbc` → `ababac`'],
        quote='若某个字符出现的次数超过所有字符数量的一半，那么就肯定构造不出来。这里的一半对于字符数量为奇数的情况应该向上取整。',
        quote_src='—— yiduobo 题解原文',
        idea=['先判无解：最多的字母次数 `>` `(n+1)//2`',
              '作者说自己用的是比较暴力的做法：堆里放 `(-次数, 字母)`',
              '每一轮==弹出次数最多和第二多==的两个字母，各用一次，还有剩余就放回堆里'],
        summary=['时间 `O(n + |Σ|log|Σ|)`，空间 `O(n)`',
                 '原文为 Python 2 写法，`(len(S) + 1) / 2` 已改为 `//`',
                 '原理：这一轮的第一多下一轮仍不少于第二多，同次数按字母序，保证不会连续取同一个',
                 '对比灵神：灵神用奇偶位置直接填，yiduobo 用堆每轮取两个'],
    ),
)
