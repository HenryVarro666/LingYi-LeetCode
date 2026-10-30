CONFIG = dict(
    num=1794, title='统计距离最小的子串对个数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='只看单字符 · 哈希表首末位置',
    tags=[],
    code='''
class Solution(object):
    def countQuadruples(self, firstString, secondString):

        min_dis = 10 ** 6
        first = {}
        last = {}
        for index, char in enumerate(firstString):
            if char not in first:
                first[char] = index
        
        for index, char in enumerate(secondString):
            last[char] = index
        
        res = 0
        for char in first:
            if char in last:
                dis = first[char] - last[char]
                if dis < min_dis:
                    min_dis = dis
                    res = 1
                elif dis == min_dis:
                    res += 1
        
        return res
''',
    call="Solution().countQuadruples('abcab', 'cbbc')",
    expect=2,
    views=[
        dict(type='string', var='firstString', label='firstString', cell=80, h=200, pointers={'index': 'blue'}),
        dict(type='string', var='secondString', label='secondString', cell=80, h=200, pointers={'index': 'pink'}),
        dict(type='map', var='first', label='first：字符在 firstString 中第一次出现的下标', fmt=lambda k, v: f"'{k}': {v}", h=120, font=30),
        dict(type='map', var='last', label='last：字符在 secondString 中最后一次出现的下标', fmt=lambda k, v: f"'{k}': {v}", h=120, font=30),
    ],
    watch=['char', 'dis', ('min_dis', 'min_dis', 'orange'), ('res', 'res', 'green')],
    captions={
        'min_dis = 10 ** 6': '`min_dis` 记最小的 `j − a`，先设成很大的数',
        'if char not in first': '`{char}` 在 first 里吗？=={"还没有，是第一次出现" if char not in B.first else "已有，跳过"}==',
        'first[char] = index': '只记第一次：`first[{char!r}] = {index}`（j 越小越好）',
        'last[char] = index': '一路覆盖，最后留下最后一次：`last[{char!r}] = {index}`（a 越大越好）',
        'if char in last': '`{char}` 两个字符串都有吗？=={"有，可以配对" if char in last else "没有，跳过"}==',
        'dis = first[char]': '`dis = j − a = {first[char]} − {last[char]}` = =={dis}==',
        'if dis < min_dis': '`dis = {dis}` 对比 `min_dis = {min_dis}`：=={"更小，刷新" if dis < min_dis else "不更小"}==',
        'res = 1': '出现更小的距离，`min_dis = {min_dis}`，计数重置为 =={res}==',
        'elif dis == min_dis': '`dis = {dis}` 是否等于 `min_dis = {min_dis}`：=={"相等，再多一个" if dis == min_dis else "更大，忽略"}==',
        'res += 1': '距离相同，`res` → =={res}==',
        'return res': '最小距离 `{min_dis}` 共出现 =={ret}== 次',
    },
    cards=dict(
        one_liner='最优一定是单个字符：首次出现的下标 − 最后出现的下标',
        complexity='时间 `O(n + m)`，空间 `O(字符集)`',
        problem=['给两个字符串，选 `firstString[i..j]` 与 `secondString[a..b]`，两段子串==相同==',
                 '要求 `j − a` ==最小==，统计满足条件的四元组 `(i,j,a,b)` 个数',
                 '示例：`abcab`、`cbbc` → `2`'],
        quote='最终答案的子串长度必然为1……为了使得j - a最小，就应该选择s1中char第一次出现的下标作为j，同时选择s2中char最后一次出现的下标作为a。',
        quote_src='—— yiduobo 题解原文',
        idea=['子串变长，`i < j` 但起点仍对应 `a`：`i − a < j − a`，所以长度 1 才最优',
              '对每个字符：`j` 取 first 中第一次出现，`a` 取 last 中最后一次出现',
              '遍历字符，统计最小 `j − a` 出现几次'],
        summary=['时间 `O(n + m)`，空间 `O(字符集)`',
                 '易错点：`first` 只记第一次（要判断 `not in`），`last` 一路覆盖',
                 '距离更小要把计数重置为 1，相等才累加',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行'],
    ),
)
