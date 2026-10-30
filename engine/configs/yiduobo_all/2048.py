def _status(S):
    if 'base' in S and 'res' in S:
        return f"`generate` 在列举 `{S['base']}` 的全排列，已得到 `{len(S['res'])}` 个数"
    if 'num_list' in S:
        return f"`num_list` 已有 `{len(S['num_list'])}` 个数值平衡数；排序后找第一个大于 `n = {S.get('n')}` 的"
    return '先手动列出每种“数位组合”，再用全排列生成所有数值平衡数'


CONFIG = dict(
    num=2048, title='下一个更大的数值平衡数', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='打表 · 全排列生成',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def nextBeautifulNumber(self, n):

        def generate(base):
            n = len(base)
            res = []
            now = 0
            for index in range(n):
                now = now * 10 + base[index]
            res.append(now)

            while True:
                p = None
                for index in range(n - 2, -1, -1):
                    if base[index] < base[index + 1]:
                        p = index
                        break
                if p is None:
                    break
                
                q = n - 1
                for index in range(p + 1, n):
                    if base[index] <= base[p]:
                        q = index - 1
                        break
                
                base[p], base[q] = base[q], base[p]
                l = p + 1
                r = n - 1
                while l < r:
                    base[l], base[r] = base[r], base[l]
                    l += 1
                    r -= 1
                
                now = 0
                for index in range(n):
                    now = now * 10 + base[index]
                res.append(now)

            
            return res

        num_list = [1, 22, 333, 4444, 55555, 666666, 1224444]
        num_list.extend(generate([1, 2, 2]))
        num_list.extend(generate([1, 3, 3, 3]))
        num_list.extend(generate([1, 4, 4, 4, 4]))
        num_list.extend(generate([1, 5, 5, 5, 5, 5]))
        num_list.extend(generate([1, 2, 2, 3, 3, 3]))
        num_list.extend(generate([2, 2, 3, 3, 3]))
        num_list.extend(generate([2, 2, 4, 4, 4, 4]))
        for num in sorted(num_list):
            if n < num:
                return num
''',
    call='Solution().nextBeautifulNumber(1000)',
    expect=1333,
    skip=['n = len(base)', 'res = []', 'now = 0', 'for index in range', 'now = now * 10', 'if base[index] < base[index + 1]',
          'p = index', 'break', 'if p is None', 'if base[index] <= base[p]', 'q = index - 1', 'l = p + 1', 'r = n - 1',
          'while l < r', 'p = None', 'q = n - 1', 'base[p], base[q]', 'for num in sorted', 'base[l], base[r]', 'l += 1', 'r -= 1', 'while True'],
    max_steps=40,
    views=[
        dict(type='text', fn=_status, size=24, h=60),
        dict(type='array', var='base', label='base：当前排列（p 是下降处，q 是要交换的位置）', pointers={'p': 'pink', 'q': 'blue'}, h=200, cell=70),
        dict(type='array', var='res', label='res：已生成的数', h=200, cell=130),
        dict(type='array', var='num_list', label='num_list：全部候选', h=200, cell=110),
    ],
    watch=['n', 'p', 'q', ('now', 'now', 'green')],
    captions={
        'res.append(now)': '“下一个排列”（找 p、找 q、交换、反转）得到 `{base}` → 拼成数字 `{now}`，放进 `res`',
        'return res': '这个组合的全排列生成完毕，共 `{len(res)}` 个数，并入 num_list',
        'num_list = [': '先手动写入只有一种排列的数：`1, 22, 333, 4444, ...`',
        'generate([1, 2, 2])': '`122` 的全排列：`122, 212, 221`，都是数值平衡数（1 个 1，2 个 2）',
        'generate([1, 3, 3, 3])': '`1333` 的全排列：1 个 1 + 3 个 3',
        'generate([1, 4': '1 个 1 + 4 个 4 的全排列',
        'generate([1, 5': '1 个 1 + 5 个 5 的全排列',
        'generate([1, 2, 2, 3': '1 个 1 + 2 个 2 + 3 个 3 的全排列（共 60 个）',
        'generate([2, 2, 3': '2 个 2 + 3 个 3 的全排列',
        'generate([2, 2, 4': '2 个 2 + 4 个 4 的全排列',
        'if n < num': lambda S, B, r: (f'`n = {S.n} < {S.num}` → ==第一个比 n 大的==，就是答案' if S.n < S.num
                                       else f'排序后的表从小到大扫描：`n = {S.n} >= {S.num}`，还不够大，看下一个'),
        'return num': '答案 `{num}`',
    },
    cards=dict(
        one_liner='范围小，先打表：用全排列生成所有数值平衡数',
        complexity='时间 `O(1)`（表是固定的），空间 `O(1)`',
        problem=['数位 `d` 恰好出现 `d` 次的整数叫==数值平衡数==',
                 '给定 `n`，返回严格大于 `n` 的最小数值平衡数',
                 '示例：`n = 1` → `22`；`n = 1000` → `1333`'],
        quote='乍一看感觉是数位动态规划的问题，不过在这里n的范围比较小，在这个范围内的数值平衡数应该是比较少的，完全可以暴力计算或者打表。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n ≤ 10^6`，平衡数很少：手动写出各种“数位组合”',
              '用字典序==下一个排列==的写法，把每个组合的全排列都列出来',
              '汇总、排序，再一趟扫描找第一个大于 `n` 的'],
        summary=['打表思路：枚举组合 → 全排列 → 排序 → 扫描',
                 '`generate` 是“下一个排列”：找 `p`、找 `q`、交换、反转 `p` 右边',
                 '易错：表里要有 `1224444`（7 位），否则 `n = 999999` 时找不到',
                 '原文本来就能在 Python 3 运行，代码未改动',
                 '对比灵神：灵神倒序贪心 + 背包，不依赖打表'],
    ),
)
