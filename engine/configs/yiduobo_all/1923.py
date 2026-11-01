def _paths(S):
    if 'paths' not in S:
        return ''
    cur = S.get('path')
    parts = []
    for p in S['paths']:
        t = '[' + ','.join(str(x) for x in p) + ']'
        parts.append('==%s==' % t if cur is not None and p is cur else t)
    return '`paths` = ' + '  '.join(parts)


CONFIG = dict(
    num=1923, title='最长公共子路径', difficulty='Hard', category='字符串',
    author='yiduobo', technique='二分答案 + 滚动哈希（Rabin-Karp）',
    tags=['灵神题单·字符串', '难度分 2661'],
    code='''
class Solution(object):
    def longestCommonSubpath(self, n, paths):

        base = 100003
        mod1 = 10 ** 9 + 7
        mod2 = 2147483647

        l = 0
        r = 100000
        for path in paths:
            r = min(r, len(path))
        
        remove_base1 = [1]
        remove_base2 = [1]
        for _ in range(r + 1):
            remove_base1.append(remove_base1[-1] * base % mod1)
            remove_base2.append(remove_base2[-1] * base % mod2)

        while l < r:
            mid = (l + r + 1) >> 1

            common1 = set()
            common2 = set()
            flag = True
            first_flag = True
            for path in paths:
                now1 = 0
                now2 = 0
                for index in range(mid):
                    now1 = now1 * base + path[index]
                    now1 %= mod1
                    now2 = now2 * base + path[index]
                    now2 %= mod2
                
                h = set([(now1, now2)])
                for index in range(mid, len(path)):
                    now1 = now1 * base + path[index] - (remove_base1[mid] * path[index - mid] % mod1)
                    if now1 < 0:
                        now1 += mod1
                    now1 %= mod1

                    now2 = now2 * base + path[index] - (remove_base2[mid] * path[index - mid] % mod2)
                    if now2 < 0:
                        now2 += mod2
                    now2 %= mod2
                    
                    h.add((now1, now2))

                if first_flag:
                    common = h.copy()
                    first_flag = False
                else:
                    tuple_list = list(common)
                    for t in tuple_list:
                        if t not in h:
                            common.remove(t)

                if not common:
                    flag = False
                    break
            
            if flag:
                l = mid
            else:
                r = mid - 1
        
        return l
''',
    call='Solution().longestCommonSubpath(3, [[0,1,2],[1,2,0]])',
    expect=2,
    views=[
        dict(type='text', fn=_paths, size=30, h=60),
        dict(type='text', fn=lambda S: ('二分区间 `[l, r] = [%s, %s]`，这一轮试长度 `mid = %s`' % (S['l'], S['r'], S['mid'])) if 'mid' in S else (('二分区间 `[l, r] = [%s, %s]`' % (S['l'], S['r'])) if 'r' in S and 'l' in S else ''), size=28, h=60),
        dict(type='array', var=lambda S: S['path'] if 'path' in S else [], label='当前路径 path（框 = 当前长度 mid 的窗口）', h=170, cell=90,
             window=('max(0, index - mid + 1)', 'index')),
        dict(type='set', var=lambda S: S['h'] if 'h' in S else set(), label='h：当前路径所有长度 mid 子路径的哈希（只显示第一个模数）', fmt=lambda t: str(t[0]), h=130),
        dict(type='set', var=lambda S: S['common'] if 'common' in S else set(), label='common：到目前为止每条路径都有的哈希', fmt=lambda t: str(t[0]), h=130),
    ],
    watch=['l', 'r', 'mid', 'flag', 'now1', 'index'],
    captions={
        'base = 100003': '用进制 `base` 把一段子路径编码成一个数，再取模得到哈希',
        'mod2 = ': '一个模数容易被卡，所以用了两个模数 `mod1`、`mod2` 同时做哈希',
        'l = 0': '二分答案的下界 `l = 0`（长度 0 一定存在）',
        'r = min': '上界不会超过最短路径长度：`r = {r}`',
        'remove_base1.append': '预处理 `base^k`：滑动窗口时用来去掉最左边那一项（`mod2` 同理）',
        'while l < r': lambda S, B, r_: (f'`l = {S.l} < r = {S.r}`：答案还没确定，继续二分' if S.l < S.r else f'`l = {S.l} == r`：二分结束，答案就是 `l`'),
        'mid = (l + r + 1) >> 1': '试长度 `mid = ({l} + {r} + 1) >> 1 = {mid}`：==向上取整==，否则 `l = mid` 时会死循环',
        'common1 = set()': '这一轮开始前，先清空公共哈希集合',
        'flag = True': '`flag` 表示这个长度 `mid` 是否存在所有路径的公共子路径',
        'for path in paths': lambda S, B, r_: (f'处理下一条路径：`path = {S.path}`' if S.get('path') is not B.get('path') else '所有路径都处理完了，没有被淘汰'),
        'h = set(': '先把前 `{mid}` 个数按 `base` 进制编码，得到第一个窗口的哈希，放进集合 `h`',
        37: '窗口右移：先 ×`base`，加上新进窗口的 `path[{index}]`，再减去滑出的 `path[{index - mid}]`，再取模（`now2` 同理）',
        'h.add': '这个窗口的哈希加入 `h`，`h` 现在有 `{len(h)}` 个不同的子路径',
        'common = h.copy()': '第一条路径：它的所有子路径哈希就是目前的公共集合',
        'first_flag = False': '之后的路径都要和 `common` 求交集',
        'tuple_list = list(common)': '把 `common` 拷一份，边遍历边删除',
        'if t not in h': lambda S, B, r_: (f'哈希 `{S.t[0]}` 不在这条路径里 → 不是公共的，要删掉' if S.t not in S.h else f'哈希 `{S.t[0]}` 这条路径也有 → 保留'),
        'common.remove(t)': '从 `common` 删掉，现在剩 `{len(common)}` 个',
        'if not common': lambda S, B, r_: ('`common` 空了：没有任何子路径所有路径都有 → 这个长度不行' if not S.common else f'`common` 还有 `{len(S.common)}` 个哈希，继续处理下一条路径'),
        'flag = False': '`flag = False`：长度 `{mid}` 不可行，不用再看后面的路径',
        'if flag': lambda S, B, r_: (f'`flag = True`：长度 `{S.mid}` 可行，答案至少是 `{S.mid}`' if S.flag else f'`flag = False`：长度 `{S.mid}` 不可行，答案小于它'),
        'l = mid': '可行 → 往更长的找：`l = {l}`',
        'r = mid - 1': '不可行 → 往更短的找：`r = {r}`',
        'return l': '二分结束，最长公共子路径长度 =={l}==',
    },
    skip=['now2 = ', 'now2 %= ', 'now2 < 0', 'now2 += ', 'remove_base2', 'common2', 'now1 %= mod1', 'now1 += mod1', 'for _ in range', 29, 30, 38, 'first_flag = False', 'tuple_list = list', 'now1 = 0', 'flag = True', 'first_flag = True', 'for t in tuple_list'],
    max_steps=110,
    cards=dict(
        one_liner='二分长度，用滚动哈希判断有没有所有路径共有的子路径',
        complexity='时间 `O(L log L)`（`L` 为路径总长），空间 `O(L)`',
        problem=['`m` 个朋友各走一条路径（城市编号序列），求所有人都走过的最长公共子路径长度',
                 '子路径是路径中连续的一段',
                 '本视频：`[[0,1,2],[1,2,0]]` → `2`（公共子路径 `[1,2]`）'],
        quote='先二分答案，设当前处理的字符串长度为mid，那么就对每个字符串中所有长度为mid的子串按照某个base进制进行编码。',
        quote_src='—— yiduobo 题解原文',
        idea=['后缀数组难写，所以改用 rk（Rabin-Karp）：二分长度 `mid`，把每个长度 `mid` 的子路径编码成哈希',
              '窗口右移时：`新哈希 = 旧哈希 × base + 新数 − base^mid × 滑出的数`，均摊 `O(1)`',
              '每条路径的哈希集合依次求交集：不为空说明 `mid` 可行，`l = mid`；否则 `r = mid - 1`'],
        summary=['时间 `O(L log L)`，空间 `O(L)`；二分向上取整 `(l + r + 1) >> 1`，否则 `l = mid` 会死循环',
                 '原文本题的 Python 代码无需修改（没有整数除法、`xrange` 等 Python 2 写法）',
                 '为减少视频步数，两个模数中 `now2` 那一套的计算行与 `now1` 完全对称，动画里没有逐行展示',
                 '易错点：数据强，单模数哈希会被卡，所以用了两个模数；减法出负数要补 `mod`',
                 '对比灵神：灵神拼接路径建后缀数组 + 高度数组，这里用滚动哈希，不用后缀数组'],
    ),
)
