CONFIG = dict(
    num=2055, title='蜡烛之间的盘子', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='最近蜡烛 + 蜡烛前缀和',
    tags=['一、前缀和', '§1.5 进阶', '难度分 1819'],
    code='''
class Solution(object):
    def platesBetweenCandles(self, s, queries):

        n = len(s)

        left = []
        for index in range(n):
            if s[index] == '|':
                left.append(index)
            elif index == 0:
                left.append(-1)
            else:
                left.append(left[-1])
        
        right = []
        for index in range(n - 1, -1, -1):
            if s[index] == '|':
                right.append(index)
            elif index == n - 1:
                right.append(-1)
            else:
                right.append(right[-1])
        right.reverse()

        if s[0] == '|':
            cnt = [1]
        else:
            cnt = [0]
        
        for char in s[1:]:
            cnt.append(cnt[-1])
            if char == '|':
                cnt[-1] += 1
        
        res = []
        for x, y in queries:
            now = cnt[y]
            if x > 0:
                now -= cnt[x - 1]
            
            if now < 2:
                res.append(0)
            else:
                res.append(left[y] - right[x] + 1 - now)
        
        return res
''',
    call='Solution().platesBetweenCandles("*|*|*|", [[0,5],[2,4]])',
    expect=[2, 0],
    views=[
        dict(type='string', var='s', label='s（* 盘子，| 蜡烛）', h=150,
             color=lambda S, i, v: 'yellow' if v == '|' else None),
        dict(type='array', var='left', label='left：左侧第一根蜡烛', h=125),
        dict(type='array', var='right', label='right：右侧第一根蜡烛', h=125),
        dict(type='array', var='cnt', label='cnt：蜡烛前缀和', h=125),
        dict(type='array', var='res', label='res', h=150),
    ],
    watch=['x', 'y', 'now', ('res', 'res', 'green')],
    captions={
        'left = []': '`left[y]`：`y` 左侧第一根蜡烛的位置，从左往右一趟求',
        "if s[index] == '|'": '`s[{index}] = {s[index]}`：{"是蜡烛，最近蜡烛就是自己" if s[index] == "|" else "是盘子，沿用旁边的结果"}',
        'left.append(index)': '`left` 追加 `{index}`',
        'right = []': '`right[x]`：`x` 右侧第一根蜡烛的位置，从右往左求，最后翻转',
        'right.reverse()': '倒着构造的，翻转后 `right[x]` 才对应下标 x',
        "if s[0] == '|'": '`cnt[i]`：s[0..i] 里蜡烛的个数（前缀和），先处理第一个字符',
        'for char in s[1:]': '依次往后累计蜡烛数',
        'cnt.append(cnt[-1])': '先继承前一个前缀和',
        "cnt[-1] += 1": '这个字符是蜡烛，前缀和加 1 → `{cnt}`',
        'res = []': '开始处理每个询问',
        'for x, y in queries': '处理下一个询问',
        'for index in range(n - 1, -1, -1)': '从右往左扫描，算每个位置右侧第一根蜡烛',
        'now = cnt[y]': '`now = cnt[{y}] = {cnt[y]}`：先取到 y 为止的蜡烛数',
        'if x > 0': '左端点不是 0，要减去 x 之前的蜡烛数',
        'now -= cnt[x - 1]': '`now` 减去 `cnt[{x - 1}] = {cnt[x - 1]}` → 区间内蜡烛数 =={now}==',
        'if now < 2': '区间内蜡烛 `{now}` 根：{"不足两根，答案为 0" if now < 2 else "至少两根，可以计算"}',
        'res.append(0)': '答案 0',
        'res.append(left[y] - right[x]': '`left[{y}] - right[{x}] + 1 - now = {left[y]} - {right[x]} + 1 - {now}` = =={left[y] - right[x] + 1 - now}==：两蜡烛之间的物件数减去蜡烛数',
    },
    max_steps=100,
    cards=dict(
        one_liner='两根最外侧蜡烛之间的物件数，减去蜡烛数，就是盘子数',
        complexity='时间 `O(n + q)`，空间 `O(n)`',
        problem=['`s` 里 `*` 是盘子，`|` 是蜡烛；每次询问 `[x, y]`',
                 '数出子串中处于两根蜡烛之间的盘子',
                 '示例：`"*|*|*|"`，`[[0,5],[2,4]]` → `[2,0]`'],
        quote='从right[x]到left[y]之间一共有left[y] - right[x] + 1个物件，设其中有cnt个蜡烛，那么剩下的盘子数量就是left[y] - right[x] + 1 - cnt。',
        quote_src='—— yiduobo 题解原文',
        idea=['`right[x]`：x 右侧第一根蜡烛，`left[y]`：y 左侧第一根蜡烛',
              '这两根之间的物件数 `left[y] - right[x] + 1`，里面有 `now` 根蜡烛',
              '用蜡烛前缀和求 `now`；不到 2 根就是 0'],
        summary=['时间 `O(n + q)`，空间 `O(n)`',
                 '`right` 是倒着 append 的，别忘了 `reverse()`',
                 '易错点：`x = 0` 时不能减 `cnt[x-1]`；区间蜡烛不足 2 根要直接答 0',
                 '对比灵神：灵神前缀和数盘子，yiduobo 前缀和数蜡烛再用长度扣除'],
    ),
)
