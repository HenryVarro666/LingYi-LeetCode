CONFIG = dict(
    num=541, title='反转字符串 II', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='一趟扫描 · cnt 计数 · 对称交换',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution(object):
    def reverseStr(self, s, k):

        s_list = list(s)

        cnt = 0
        for index in range(len(s_list)):
            cnt += 1
            if cnt == k:
                start_pos = index - k + 1
                for pos in range(k // 2):
                    s_list[start_pos + pos], s_list[index - pos] = s_list[index - pos], s_list[start_pos + pos]
            elif cnt == k * 2:
                cnt = 0

        if cnt > 0 and cnt < k:
            start_pos = index - cnt + 1
            for pos in range(cnt // 2):
                s_list[start_pos + pos], s_list[index - pos] = s_list[index - pos], s_list[start_pos + pos]

        return ''.join(s_list)
''',
    call='Solution().reverseStr("abcdefgh", 3)',
    expect='cbadefhg',
    views=[
        dict(type='text', fn=lambda S: (f"`cnt = {S['cnt']}`，k = {S['k']}，2k = {S['k'] * 2}" if 'cnt' in S else ''), size=28),
        dict(type='array', var='s_list', label='s_list（粉 = index 当前扫描位置，蓝 = 正在交换的一对）', cell=84,
             pointers={'index': 'pink'},
             color=lambda S, i, v: ('blue' if ('pos' in S and 'start_pos' in S and S['_line'] in (11, 18) and i in (S['start_pos'] + S['pos'], (S['index'] - S['pos']))) else None),
             h=260),
    ],
    watch=[('index', 'index', 'pink'), ('cnt', 'cnt', 'yellow'), ('start_pos', 'start_pos', 'blue'), ('pos', 'pos')],
    captions={
        's_list = list(s)': '先把字符串变成字符列表 `{s_list}`，方便交换',
        'for index': lambda S, B, r: ('扫描结束' if 'index' in B and S.index == B.index else f'扫描第 `{S.index}` 个字符 `{S.s_list[S.index]}`'),
        'cnt += 1': '`cnt` → `{cnt}`',
        9: lambda S, B, r: (f'`cnt = {S.cnt} == k = {S.k}` → ==累积到 k 位，翻转这 k 个==' if S.cnt == S.k else f'`cnt = {S.cnt} ≠ k = {S.k}`，先不翻转'),
        'start_pos = index - k + 1': '这一段从 `start_pos = {start_pos}` 到 `index = {index}`',
        'for pos in range(k': '对称交换，只需交换 `k // 2 = {k // 2}` 对',
        's_list[start_pos + pos], s_list[index - pos] =': lambda S, B, r: f'交换下标 `{S.start_pos + S.pos}` 与 `{S.index - S.pos}` → `{S.s_list}`',
        13: lambda S, B, r: (f'`cnt = {S.cnt} == 2k` → ==累积到 2k 位，cnt 归零==，重新计数' if S.cnt == S.k * 2 else f'`cnt = {S.cnt}` 还没到 `2k = {S.k * 2}`'),
        6: '`cnt` 累积当前这一段已扫过的字符数，从 0 开始',
        14: '`cnt` 归零，下一段从头数',
        'if cnt > 0 and cnt < k': lambda S, B, r: (f'扫描完 `cnt = {S.cnt}`，`0 < cnt < k` → ==最后这 cnt 个也要翻转==' if 0 < S.cnt < S.k else f'扫描完 `cnt = {S.cnt}`，不需要处理尾段'),
        'start_pos = index - cnt + 1': '尾段从 `start_pos = {start_pos}` 到末尾 `{index}`',
        'for pos in range(cnt': '尾段 `{cnt}` 个字符，交换 `{cnt // 2}` 对',
        'return': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='cnt 数到 k 就翻转，数到 2k 就归零',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每 `2k` 个字符，反转其中前 `k` 个；剩余不足 `k` 个则全部反转',
                 '示例：`"abcdefg"`，`k = 2` → `"bacdfeg"`',
                 '本视频：`"abcdefgh"`，`k = 3` → `"cbadefhg"`'],
        quote='使用一个cnt累积当前字符数量，累积到k位进行翻转，然后累积到2k位将cnt归零。需要注意的是，当扫描完成，cnt大于0且cnt小于k，说明最后的这cnt个字符也需要进行翻转。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟扫描：`cnt == k` 时把刚扫过的 k 个字符翻转',
              '`cnt == 2k` 时归零，开始下一段',
              '翻转用对称交换：第 `pos` 个与倒数第 `pos` 个互换，共 `k // 2` 次'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`，并删去了类型文档字符串',
                 '易错：扫描结束后 `cnt` 在 `(0, k)` 之间时，尾段还要再翻转一次',
                 '`cnt` 恰好等于 k 的尾段已在循环里翻转过，不会重复',
                 '对比灵神：灵神用 `range(0, n, 2k)` 直接枚举起点 + 切片反转'],
    ),
)
