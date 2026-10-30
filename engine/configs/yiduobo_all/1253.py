CONFIG = dict(
    num=1253, title='重构 2 行二进制矩阵', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='按列贪心 · 优先补较大的一行',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def reconstructMatrix(self, upper, lower, colsum):

        res = [[], []]
        for s in colsum:
            if s == 0:
                res[0].append(0)
                res[1].append(0)
            elif s == 2:
                if upper == 0 or lower == 0:
                    return []
                res[0].append(1)
                res[1].append(1)
                upper -= 1
                lower -= 1
            elif upper == 0 and lower == 0:
                return []
            else:
                if upper > lower:
                    res[0].append(1)
                    res[1].append(0)
                    upper -= 1
                else:
                    res[0].append(0)
                    res[1].append(1)
                    lower -= 1
        
        if upper > 0 or lower > 0:
            return []
        return res
''',
    call='Solution().reconstructMatrix(3, 2, [2, 1, 1, 0, 1])',
    expect=[[1, 1, 0, 0, 1], [1, 0, 1, 0, 0]],
    views=[
        dict(type='text', fn=lambda S: (f"还需第 0 行放 `{S['upper']}` 个 1，第 1 行放 `{S['lower']}` 个 1" if 'upper' in S else '')),
        dict(type='array', var='colsum', pointers={'len(res[0])': 'blue'}, h=170, label='colsum'),
        dict(type='grid', var=lambda S: [S['res'][0] + [''] * (len(S['colsum']) - len(S['res'][0])), S['res'][1] + [''] * (len(S['colsum']) - len(S['res'][1]))] if 'res' in S else [], h=230, label='res',
             rows=['上', '下'], color=lambda S, i, j, v: 'green' if v == 1 else None),
    ],
    watch=['upper', 'lower', 's'],
    captions={
        'res = [[], []]': '`res[0]` 是上行，`res[1]` 是下行，逐列往后填',
        'for s in colsum': '第 `{len(res[0])}` 列，列和 `s = {s}`',
        'if s == 0': '列和 `s = {s}`：' + '{"两格都是 0，没有选择" if s == 0 else "不是 0，继续判断"}',
        'elif s == 2': '`s = {s}`：' + '{"两格都必须是 1" if s == 2 else "只剩 s = 1：一个 0 一个 1，可以灵活安排"}',
        'upper == 0 or lower == 0': '`upper = {upper}`，`lower = {lower}`：' + '{"某一行没有 1 可用了 → 无解" if upper == 0 or lower == 0 else "两行都还有名额，继续"}',
        'res[0].append(1)': lambda S, B, r: f'这一格放 1：上行 `{S.res[0][-1]}`',
        'upper -= 1': '上行还需 `upper = {upper}` 个 1',
        'lower -= 1': '下行还需 `lower = {lower}` 个 1',
        'elif upper == 0 and lower == 0': '`s = 1` 需要一个 1，`upper = {upper}`，`lower = {lower}`：' + '{"两行名额都用完 → 无解" if upper == 0 and lower == 0 else "还有名额，继续"}',
        'if upper > lower': '`upper = {upper}` vs `lower = {lower}`：' + '{"上行缺得更多 → 把 1 放上行" if upper > lower else "下行缺得不少于上行 → 把 1 放下行"}',
        'if upper > 0 or lower > 0': '扫完后 `upper = {upper}`，`lower = {lower}`：' + '{"还有名额没用完 → 无解" if upper > 0 or lower > 0 else "名额恰好用完 → 合法"}',
        'return res': '得到一个合法矩阵 `{res}`',
    },
    cards=dict(
        one_liner='列和 1 的列，把 1 给缺得更多的那一行',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计入）',
        problem=['2 行 `n` 列的 0/1 矩阵：上行和为 `upper`，下行和为 `lower`，第 `i` 列和为 `colsum[i]`',
                 '返回任意一个满足的矩阵，不存在返回空数组',
                 '本视频：`upper=3, lower=2, colsum=[2,1,1,0,1]`'],
        quote='若colsum[i]为1，说明这一列中有一个0和一个1，可以灵活调配。为了适配upper和lower，若当前upper > lower，那么我们将1安排在第0行，将0安排在第1行，并将upper减去1。',
        quote_src='—— yiduobo 题解原文',
        idea=['列和 0 → 两格 0；列和 2 → 两格 1，没有选择',
              '列和 1 → 灵活：哪行剩的名额多，1 就放哪行',
              '扫完后 `upper`、`lower` 必须都归零，否则无解'],
        summary=['时间 `O(n)`，空间 `O(1)`（返回值不计入）',
                 '易错：列和为 2 时要先检查 `upper`、`lower` 是否都还有名额',
                 '易错：最后要检查 `upper`、`lower` 都为 0，不能只看过程没出错'],
    ),
)
