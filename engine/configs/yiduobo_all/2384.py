def _top(S):
    if 'mid' not in S:
        return ''
    m = S['mid']
    return '中心 `mid` 还没确定（None）' if m is None else f'中心 `mid = {m}`（出现奇数次的最大数字）'


CONFIG = dict(
    num=2384, title='最大回文数字', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='计数 · 从大到小成对放置',
    tags=['灵神题单', '难度分 1636'],
    code='''
class Solution(object):
    def largestPalindromic(self, num):

        cnt_list = [0] * 10
        for digit in num:
            cnt_list[int(digit)] += 1
        
        mid = None
        res = []
        for digit in range(9, -1, -1):
            res.extend([digit] * (cnt_list[digit] // 2))
            if cnt_list[digit] % 2 == 1 and mid is None:
                mid = digit
        
        if not res:
            return str(mid)
        elif res[0] == 0:
            if mid is None:
                return '0'
            else:
                return str(mid)
        else:
            if mid is None:
                res = res + res[::-1]
            else:
                res = res + [mid] + res[::-1]
            
            return ''.join([str(x) for x in res])
''',
    call='Solution().largestPalindromic("4449470013")',
    expect='4409044',
    views=[
        dict(type='string', var='num', label='num', cell=64, h=140,
             color=lambda S, i, v: 'yellow' if S.get('_line') == 6 and S.get('digit') == v else None),
        dict(type='array', var='cnt_list', label='cnt_list（下标 = 数字，值 = 出现次数）', cell=72, h=170,
             pointers={'digit': 'blue'},
             color=lambda S, i, v: 'green' if v >= 2 and 'mid' in S and S.get('_line', 0) >= 11 else None),
        dict(type='text', fn=_top, size=26),
        dict(type='array', var='res', label='res（回文串的左半边，从大到小）', cell=64, h=150),
    ],
    watch=[('digit', 'digit', 'blue'), ('mid', 'mid', 'orange'), ('res', 'res', 'green')],
    captions={
        'cnt_list = [0]': '`cnt_list[d]` 记录数字 `d` 出现几次',
        'for digit in num': lambda S, B, r: ('num 里的数字都数完了' if sum(B.cnt_list) == len(S.num) else f'取下一个字符 `{S.digit}`'),
        'cnt_list[int(digit)] += 1': '数字 `{digit}` 又出现一次 → `cnt_list[{digit}] = {cnt_list[int(digit)]}`',
        'mid = None': '`mid`：落单数字里最大的那个，放回文串中心；还没有',
        'res = []': '`res` 存左半边：成对数字从大到小，每对取一个',
        'for digit in range(9': lambda S, B, r: ('9 到 0 都安排完了' if 'digit' in B and B.digit == S.digit == 0
                                                  else f'从大到小安排数字 `{S.digit}`'),
        'res.extend': '`{digit}` 有 `{cnt_list[digit]}` 个 → `{cnt_list[digit] // 2}` 对，左半边加 `{cnt_list[digit] // 2}` 个 → `res = {res}`',
        'if cnt_list[digit] % 2 == 1': lambda S, B, r: (
            f'`{S.digit}` 出现 `{S.cnt_list[S.digit]}` 次是奇数，且 `mid` 还没定 → ==最大的落单数字，当中心==' if S.cnt_list[S.digit] % 2 == 1 and B.mid is None
            else (f'`{S.digit}` 出现奇数次，但 `mid = {B.mid}` 已经有更大的了 → 忽略' if S.cnt_list[S.digit] % 2 == 1
                  else f'`{S.digit}` 出现 `{S.cnt_list[S.digit]}` 次，没有落单')),
        'mid = digit': '`mid = {mid}`',
        'if not res': lambda S, B, r: ('`res` 为空：没有任何成对数字' if not S.res else '`res` 不为空，继续检查开头'),
        'return str(mid)': '只能用单个数字 `{mid}`（成对的全是 0 或没有）→ 返回 `"{mid}"`',
        'elif res[0] == 0': lambda S, B, r: (f'`res[0] = {S.res[0]}`：从大到小排的，开头是 0 说明成对的只有 0 → 会有前导零' if S.res[0] == 0
                                              else f'`res[0] = {S.res[0]}` 不是 0 → 没有前导零问题'),
        "return '0'": '没有落单数字，只剩 0 → 答案 `"0"`',
        'if mid is None': lambda S, B, r: ('没有落单数字 → 左半边 + 镜像' if S.mid is None
                                           else f'有落单数字 `{S.mid}` → 左半边 + 中心 + 镜像'),
        'res = res + res[::-1]': '偶回文：`res` 接上自己的镜像 → `{res}`',
        'res = res + [mid]': '奇回文：左半边 + 中心 `{mid}` + 镜像 → `{res}`',
        'return \'\'.join': '拼成字符串 =={ret}==',
    },
    cards=dict(
        one_liner='成对数字从大到小从外向内排，落单的最大数字放中心',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给一串数字 `num`，任选并重排，拼成==最大的回文整数==（字符串返回）',
                 '不能有前导零，至少用一个数字',
                 '示例：`"444947137"` → `"7449447"`；`"00009"` → `"9"`',
                 '本视频：`"4449470013"` → `"4409044"`'],
        quote='应该按从大到小的顺序，从外向内一组一组地安排数字。除此之外，如果还有落单的数字，那么可以选择其中最大的那个放在中间。',
        quote_src='—— yiduobo 题解原文',
        idea=['计数后，数字按 9 到 0 的顺序，每 2 个一组放在对称位置，==大数在高位==',
              '落单数字里只记最大的一个，放中心',
              '最后检查开头是不是 0，避免前导零'],
        result='成对：`4×2`、`0×1`；落单最大的是 `9` → `440` + `9` + `044` = `4409044`',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '前导零：`res` 是从大到小排的，开头是 0 说明成对的只有 0 → 只能用 `mid`，没有就返回 `"0"`',
                 '`mid` 只在第一次遇到奇数个时赋值，所以就是落单数字里最大的',
                 '原文为 Python 2 写法，计数 `cnt_list[digit] / 2` 已改为 `//`（整数除法）',
                 '对比灵神：灵神拼字符串，先特判全 0；yiduobo 用列表，事后检查开头是否为 0'],
    ),
)
