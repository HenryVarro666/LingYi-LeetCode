CONFIG = dict(
    num=1625, title='执行操作后字典序最小的字符串', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='预处理累加轮次 + 枚举轮转', tags=['灵神题单', '数学算法', '难度分 1992'],
    code='''
class Solution(object):
    def findLexSmallestString(self, s, a, b):
        rnd = [0] * 10
        for num in range(10):
            now = num
            min_num = num
            min_rnd = 0
            now_rnd = 0
            while True:
                now = (now + a) % 10
                if now == num:
                    break
                now_rnd += 1
                if now < min_num:
                    min_num = now
                    min_rnd = now_rnd

            rnd[num] = min_rnd

        offset = 0
        now_list = [int(x) for x in list(s)]
        res = now_list[:]
        n = len(s)
        while True:
            tmp = now_list[:]
            if b & 1:
                self.adjust(tmp, 0, n, a, rnd)
            self.adjust(tmp, 1, n, a, rnd)

            flag = False
            for index in range(n):
                if tmp[index] != res[index]:
                    flag = tmp[index] < res[index]
                    break

            if flag:
                res = tmp[:]

            offset = (offset + b) % n
            if offset == 0:
                break

            tmp = [0] * n
            for index in range(n):
                tmp[(index + b) % n] = now_list[index]
            now_list = tmp[:]

        return ''.join(str(x) for x in res)

    def adjust(self, tmp, start_pos, n, a, rnd):
        add_rnd = rnd[tmp[start_pos]]
        for index in range(start_pos, n, 2):
            tmp[index] = (tmp[index] + a * add_rnd) % 10
''',
    call='Solution().findLexSmallestString("5525", 5, 2)',
    expect='2050',
    views=[
        dict(type='array', var='rnd', h=170, label='rnd[d] = 数字 d 变最小需累加的次数', cell=60),
        dict(type='array', var='now_list', h=170, label='now_list（当前轮转状态）', cell=70),
        dict(type='array', var='tmp', h=170, label='tmp（累加后）', cell=70),
        dict(type='array', var='res', h=170, label='res（目前最小）', cell=70),
    ],
    watch=['num', 'now', 'min_num', 'min_rnd', 'offset', 'b'],
    max_steps=85,
    skip=['while True', 'now_rnd += 1', 'min_num = now', 'min_rnd = now_rnd', 'min_rnd = 0', 'now_rnd = 0', 'min_num = num', 'now = num'],
    captions={
        'rnd = [0]': '先预处理：对每个数字 `d`，反复加 `a`（模 10），记下变得最小要加几次',
        'for num in range(10)': '看数字 `{num}`',
        'now = (now + a)': '加一次 `a`：`now = {now}`',
        'if now == num': lambda S, B, r: (f'`now` 回到 `{S.num}`，一圈走完，停' if S.now == S.num else f'`now = {S.now}` 还没回到 `{S.num}`，继续'),
        'if now < min_num': lambda S, B, r: f'`{S.now} < {S.min_num}` → ' + ('成立，更新最小值和轮次' if S.now < S.min_num else '不成立'),
        'rnd[num] = ': '`rnd[{num}] = {min_rnd}`：数字 `{num}` 加 `{min_rnd}` 次 `a` 后最小是 `{min_num}`',
        'now_list = [int': '把字符串转成数字列表，`res` 先取原串',
        'tmp = now_list[:]': '拿当前轮转状态复制一份 `tmp`，做累加',
        'if b & 1': lambda S, B, r: ('`b` 是奇数：轮转后奇偶互换，偶数位也能被累加' if S.b & 1 else '`b` 是偶数：奇偶位不变，只能累加奇数位'),
        'self.adjust(tmp, 0': '先把第 0 位变最小，偶数位一起加',
        'self.adjust(tmp, 1': '再把第 1 位变最小，奇数位一起加',
        'add_rnd = ': '`tmp[{start_pos}] = {tmp[start_pos]}` 要加 `{add_rnd}` 次 `a`',
        'tmp[index] = (tmp[index]': '`tmp[{index}]` 变成 `{tmp[index]}`',
        'if tmp[index] != res[index]': lambda S, B, r: (f'第 `{S.index}` 位 `{S.tmp[S.index]}` 与 `{S.res[S.index]}` 不同，由它决定大小' if S.tmp[S.index] != S.res[S.index] else f'第 `{S.index}` 位相同，看下一位'),
        'if flag': lambda S, B, r: ('`tmp` 更小，替换 `res`' if S.flag else '`tmp` 不更小，保留 `res`'),
        'res = tmp[:]': '`res = {res}`',
        'offset = (offset + b) % n': '已轮转 `offset = {offset}` 位；回到 0 就枚举完了',
        'if offset == 0': lambda S, B, r: ('`offset == 0`：转了一整圈，枚举结束' if S.offset == 0 else f'`offset = {S.offset}`，继续轮转'),
        'tmp[(index + b) % n]': '右移 `b` 位：`now_list[{index}]` 放到位置 `{(index + b) % n}`',
        'now_list = tmp[:]': '得到新的轮转状态 `{now_list}`',
        'return': '最小字符串：=={ret}==',
    },
    cards=dict(
        one_liner='先预处理每个数字最优累加次数，再枚举全部轮转',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['数字串 `s`（偶数长），操作：奇数下标都加 `a`（模 10）、整体右移 `b` 位',
                 '可任意次、任意顺序，求字典序最小的结果',
                 '示例：`s="5525", a=9, b=2` → `"2050"`'],
        quote='因为每次操作是对所有奇数位上的数同时执行，因此为了使得字典序最小，实际上只需要考虑让最高位上的数最小即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`b` 为奇数：轮转一次奇偶互换，奇偶位都能累加；`b` 为偶数：只有奇数位能累加',
              '字典序只看最高位，所以只需把第 0 位和第 1 位变到最小',
              '轮转最多 `n` 次回到原串，直接枚举每个轮转状态，取字典序最小的'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '`rnd[d]` 是数字 `d` 变最小需累加 `a` 的次数，预处理一次反复用',
                 '易错：`b` 为奇数时两个位置都要调整，而且先调偶数位再调奇数位互不影响',
                 '对比灵神：灵神用 `gcd` 直接算最小值，yiduobo 模拟一圈找最小值'],
    ),
)
