CONFIG = dict(
    num=244, title='最短单词距离II', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='位置数组 + 二分 + 缓存',
    tags=['灵神题单'],
    code='''
class WordDistance(object):

    def __init__(self, wordsDict):
        self.words_pos = {}
        self.pair_cache = {}

        for index, word in enumerate(wordsDict):
            if word not in self.words_pos:
                self.words_pos[word] = []
            self.words_pos[word].append(index)

    def shortest(self, word1, word2):
        if word1 < word2:
            key = word1 + '|' + word2
        else:
            key = word2 + '|' + word1

        if key in self.pair_cache:
            return self.pair_cache[key]

        if len(self.words_pos[word1]) <= len(self.words_pos[word2]):
            pos_list1 = self.words_pos[word1]
            pos_list2 = self.words_pos[word2]
        else:
            pos_list1 = self.words_pos[word2]
            pos_list2 = self.words_pos[word1]

        res = None

        for p in pos_list1:
            if p <= pos_list2[0]:
                tmp = pos_list2[0] - p
            elif p >= pos_list2[-1]:
                tmp = p - pos_list2[-1]
            else:
                left = 0
                right = len(pos_list2) - 1
                while left < right:
                    mid = (left + right) >> 1
                    if pos_list2[mid] >= p:
                        right = mid
                    else:
                        left = mid + 1

                tmp = min(pos_list2[left] - p, p - pos_list2[left - 1])

            if res is None or res > tmp:
                res = tmp

        self.pair_cache[key] = res
        return res
''',
    call='''d = WordDistance(['a', 'c', 'b', 'c', 'a'])
r = [d.shortest('b', 'c'), d.shortest('a', 'b'), d.shortest('c', 'b')]
r''',
    expect=[1, 2, 1],
    views=[
        dict(type='map', var='self.words_pos', label='words_pos（单词 → 出现下标，天然有序）', fmt=lambda k, v: f"'{k}': {v}", font=26, h=200),
        dict(type='array', var='pos_list1', label='pos_list1（较短的一个，逐个枚举 p）', pointers={}, h=150,
             color=lambda S, i, v: 'blue' if 'p' in S and v == S['p'] else None),
        dict(type='array', var='pos_list2', label='pos_list2（较长的一个，在里面二分）', h=150,
             pointers={'left': 'blue', 'right': 'pink'}),
        dict(type='map', var='self.pair_cache', label='pair_cache（查过的单词对 → 答案）', fmt=lambda k, v: f"'{k}': {v}", font=28, h=120),
        dict(type='text', size=30, h=70, fn=lambda S: (f"当前 p = ==`{S['p']}`==，目前最近距离 res = ==`{S['res']}`==" if 'p' in S and 'res' in S else '')),
    ],
    skip=['if word not in self.words_pos', 'self.words_pos[word] = []'],
    watch=[('p', 'p', 'blue'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'cyan'), ('tmp', 'tmp', 'orange'), ('res', 'res', 'green')],
    captions={
        'self.words_pos[word].append(index)': '`{word}` 出现在下标 {index}，下标按从小到大追加，所以每个数组天然有序',
        'if word1 < word2': '先把两个词排好序再拼成 key，`(a, c)` 和 `(c, a)` 就是同一个缓存条目',
        'if key in self.pair_cache': lambda S, B, r: ('`{}` 查过了 → 直接返回缓存，不再扫描'.format(S.key) if S.key in S['self'].pair_cache else '`{}` 没查过，继续算'.format(S.key)),
        'if len(self.words_pos[word1])': '比较两个位置数组长度：==枚举短的==，在长的里二分，代价更小',
        'res = None': '`res` 记录目前最近距离，还没有',
        'for p in pos_list1': '枚举短数组里的下标 `p = {p}`：找长数组中离它最近的位置',
        'if p <= pos_list2[0]': lambda S, B, r: (f'`p = {S.p} <= {S.pos_list2[0]}`：在长数组最左边或更左，最近的只能是第一个位置' if S.p <= S.pos_list2[0] else f'`p = {S.p} > {S.pos_list2[0]}`：不在最左边，再看右边'),
        'tmp = pos_list2[0] - p': '`p` 不比 `pos_list2[0]` 大 → 距离 `{pos_list2[0]} − {p} = {tmp}`',
        'elif p >= pos_list2[-1]': lambda S, B, r: (f'`p = {S.p} >= {S.pos_list2[-1]}`：在长数组最右边或更右，最近的只能是最后一个位置' if S.p >= S.pos_list2[-1] else f'`p = {S.p} < {S.pos_list2[-1]}`：落在中间，需要二分'),
        'tmp = p - pos_list2[-1]': '`p` 不比最后一个位置小 → 距离 `{p} − {pos_list2[-1]} = {tmp}`',
        'left = 0': 'p 落在中间：二分找第一个 `>= p` 的位置，区间 `[0, {right}]`',
        'while left < right': lambda S, B, r: (f'`left={S.left} < right={S.right}`，继续二分' if S.left < S.right else f'`left == right == {S.left}`：找到第一个 `>= {S.p}` 的位置'),
        'mid = (left + right)': '取中点 `mid = {mid}`',
        'if pos_list2[mid] >= p': '`pos_list2[{mid}] = {pos_list2[mid]}` 与 `p = {p}` 比较 → ' + '{"够大，答案在左半（含 mid）" if pos_list2[mid] >= p else "太小，答案在右半"}',
        'right = mid': '`mid` 够大，可能就是答案 → `right = {right}`',
        'left = mid + 1': '`mid` 太小，排除 → `left = {left}`',
        'tmp = min(': '`p` 夹在 `pos_list2[{left-1}]={pos_list2[left-1]}` 和 `pos_list2[{left}]={pos_list2[left]}` 之间，取近的一个：`tmp = {tmp}`',
        'if res is None or res > tmp': lambda S, B, r: (f'`tmp = {S.tmp}` 比 `res = {S.res}` 小？→ 更新' if S.res is not None and S.res > S.tmp else ('`res` 还是空 → 直接取 tmp' if S.res is None else f'`tmp = {S.tmp}` 不比 `res = {S.res}` 小 → 不更新')),
        'res = tmp': '`res` 更新为 =={res}==',
        'self.pair_cache[key] = res': '把答案存进缓存：`pair_cache[{key!r}] = {res}`',
        'return res': '返回最近距离 `{res}`',
    },
    cards=dict(
        one_liner='位置数组有序，枚举短的、二分长的，再缓存答案',
        complexity='每次查询 `O(短 · log 长)`，空间 `O(n)`',
        problem=['`WordDistance(wordsDict)` 构造一次，之后多次 `shortest(word1, word2)`',
                 '求两个不同单词在数组中的最近下标距离',
                 '本视频：`[a,c,b,c,a]`，查 (b,c)、(a,b)、(c,b)'],
        quote='遍历出现次数较少的单词的所有下标位置p，然后在另一个单词出现位置数组中二分这个p，找到与p最接近的1个或2个位置然后计算距离。',
        quote_src='—— yiduobo 题解原文',
        idea=['初始化时记下每个词出现的下标：天然升序，可以二分',
              '查询时只枚举较短的数组，对每个 `p` 在较长数组里二分找最近的',
              '用排序后拼成的 key 缓存，同一对词不会重复算'],
        summary=['初始化 `O(n)`；单次查询 `O(短 · log 长)`，缓存命中 `O(1)`',
                 '原文用 `>> 1` 取中点，`while left < right` 找第一个 `>= p` 的位置',
                 '二分前先单独处理 p 在两端的情况，否则 `left - 1` 会越界',
                 'key 要把两个词排序再拼，否则 (a,c) 与 (c,a) 缓存不共享',
                 '代码为 Python 2 风格但无需修改，仅去掉了多余的空白行'],
    ),
)
