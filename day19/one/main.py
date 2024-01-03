
import inspect
from collections import namedtuple

puzzle_test = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""
class WorkFlow(namedtuple('WorkFlow', ['x', 'm', 'a', 's'])):

    @property
    def sum(self) -> int:
        return sum([self.x, self.m, self.a, self.s])

class Rule:
    
    def __init__(self, rule: str):
        self.name = None
        self.rules = []
        self.parse_rule(rule)
    
    def parse_rule(self, rule: str) -> None:
        idx = rule.index('{')
        self.name = rule[:idx]

        for r in rule[idx + 1:-1].split(','):
            if ':' not in r:
                self.rules.append(r)
                continue

            qual, name = r.split(':')
            
            if '<' in qual:
                idx = qual.index('<') + 1
                self.rules.append((qual[0], int(qual[idx:]), lambda x, y: x < y, name))
            else:
                idx = qual.index('>') + 1
                self.rules.append((qual[0], int(qual[idx:]), lambda a, b: a > b, name))
    
    def eval_rule(self, wf: WorkFlow) -> str:
        for rule in self.rules:
            if isinstance(rule, str):
                return rule
            
            attr, comp, qual, res = rule

            if qual(getattr(wf, attr), comp):
                return res
    
class RuleSet(dict[str, Rule]):

    def __init__(self, rules: str) -> None:
        super().__init__()
        for r in rules.strip().split():
            parsed = Rule(r)
            self[parsed.name] = parsed
    
    def eval_wf(self, wf: WorkFlow) -> bool:
        
        res = self['in'].eval_rule(wf)
        flow = [res]

        while res not in ['A', 'R']:
            res = self[res].eval_rule(wf)
            flow.append(res)
        
        return res == 'A'




if __name__ == '__main__':
    with open('day19/one/puzzle.txt') as f:
        puzzle = f.read().strip()
    # puzzle = puzzle_test

    rules, wf = puzzle.split('\n\n')

    
    workflows: list[WorkFlow] = [WorkFlow(*[int(f[2:]) for f in w[1:-1].split(',')]) for w in wf.strip().split('\n')]
    rule_set = RuleSet(rules)

    total = 0

    for w in workflows:
        if rule_set.eval_wf(w):
            total += w.sum

    
    print(total)
    workflows[0]