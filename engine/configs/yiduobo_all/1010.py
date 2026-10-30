_P = 'sum(rem_dict.values()) - (_line == 13) if _line != 15 else None'


def _dim(S, i, v):
    if 'rem_dict' not in S or S.get('_line') == 15:
        return False
    return i > sum(S['rem_dict'].values()) - (S.get('_line') == 13)


CONFIG = dict(
    num=1010, title='总持续时间可被 60 整除的歌曲', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='余数分类讨论 · dict 计数',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def numPairsDivisibleBy60(self, time):

        rem_dict = {}
        res = 0
        for num in time:
            num %= 60
            if num > 0:
                res += rem_dict.get(60 - num, 0)
            else:
                res += rem_dict.get(num, 0)

            rem_dict[num] = rem_dict.get(num, 0) + 1

        return res
''',
    call='Solution().numPairsDivisibleBy60([60,20,100,40,120,30,90])',
    expect=4,
    views=[
        dict(type='array', var='time', label='time（当前歌曲 = 歌曲 j）', pointers={_P: 'blue'}, pointer_labels={_P: 'j'}, h=210,
             dim=_dim),
        dict(type='map', var='rem_dict', label='rem_dict：余数 → 已出现次数', fmt=lambda k, v: f'余{k}: {v}', h=170, font=34),
        dict(type='text', h=90, size=30,
             fn=lambda S: ('`k = time[j] % 60`：==k = 0== 配余 0，==k > 0== 配余 `60 − k`' if 'num' not in S
                           else (f"`k = {S['num']}` → 情况 2：找余数 =={60 - S['num']}==" if S['num'] > 0
                                 else '`k = 0` → 情况 1：找余数 ==0==')) if S.get('_line') not in (6,) else '取下一首歌'),
    ],
    watch=[('num', 'num', 'blue'), ('res', 'res', 'green')],
    captions={
        'rem_dict = {}': '`rem_dict` 统计已遍历歌曲 `time[i] % 60` 的余数',
        'res = 0': '`res` 统计配对数',
        'for num in time': lambda S, B, r: (f'下一首歌 `num = {S.num}`' if sum(S.rem_dict.values()) < len(S.time) else '遍历结束'),
        'num %= 60': '只关心余数：`k = {B.num} % 60 = {num}`',
        'if num > 0': lambda S, B, r: (f'`k = {S.num} > 0`：要和余数 `60 − {S.num}` 的歌配对' if S.num > 0
                                       else '`k = 0`：只能和==余数也是 0== 的歌配对（不是余 60）'),
        'res += rem_dict.get(60 - num': '前面余 `{60 - num}` 的有 `{rem_dict.get(60 - num, 0)}` 首 → `res = {res}`',
        'res += rem_dict.get(num, 0)': '前面余 0 的有 `{rem_dict.get(0, 0)}` 首 → `res = {res}`',
        'rem_dict[num] = ': '用当前余数更新 dict：`rem_dict[{num}] = {rem_dict[num]}`',
        'return res': '一共 `{res}` 对',
    },
    cards=dict(
        one_liner='按余数 k 是否为 0 分两种情况，dict 统计前面的余数',
        complexity='时间 `O(n)`，空间 `O(60)`',
        problem=['第 i 首歌长 `time[i]` 秒，求 `i < j` 且 `time[i] + time[j]` 能被 60 整除的对数',
                 '示例：`[30,20,150,100,40]` → `3`',
                 '本视频：`[60,20,100,40,120,30,90]` → `4`'],
        quote='对于歌曲j而言，设k = time[j] % 60：1、当k=0时，需要找到满足time[i] % 60 = 0的所有i；2、当k>0时，需要找到满足time[i] % 60 = 60 - k的所有i',
        quote_src='—— yiduobo 题解原文',
        idea=['两首歌之和被 60 整除 ⇔ ==余数之和是 0 或 60==',
              '用 dict 统计前面每种余数的次数，一趟遍历',
              '先累加答案，再把当前余数放进 dict'],
        summary=['时间 `O(n)`，空间 `O(60)`',
                 '易错：`k = 0` 要找余 0，不能找 `60 − 0 = 60`',
                 '`num %= 60` 直接改写循环变量，后面都用余数',
                 '原文代码在 Python 3 下可直接运行，未做修改'],
    ),
)
