from multimetric.cls.base import MetricBase

# ABC Rules:
# A) Add 1 to A with assignment operators (=, +=, -=, *=, /=, %=, //=, **=, &=, |=, ^=, >>=, <<=)
#
# B) Add 1 to B with each function call (Also once when a function is declared. Wrong?)
#
# C) Add 1 to C with conditional operators (>, <, <=, >=, ==, !=, &&, ||)
# C) Add 1 to C with the following keywords (else, elif, try, except)
# C) Add 1 for each unary conditional operator

class MetricBaseABC(MetricBase):
    _assignments = [
        "=",
        "+=",
        "-=",
        "*=",
        "/=",
        "%=",
        "//=",
        "**=",
        "&=",
        "|=",
        "^=",
        ">>=",
        "<<="
    ]
    _branches = [
        "Token.Name.Function",
        "Token.Name.Function.Magic",
        "Token.Name.Label",
    ]
    _conditionals = [
        ">",
        "<",
        "<=",
        ">=",
        "==",
        "!=",
        "&&",
        "||",
        "else",
        "elif",
        "if",
        "else",
        "elif",
        "case",
        "default",
        "for",
        "while",
        "and",
        "or"
    ]

    METRIC_ABC_ASSIGNMENTS = "ABC_Assignments"
    METRIC_ABC_BRANCHES = "ABC_Branches"
    METRIC_ABC_CONDITIONALS = "ABC_Conditionals"

    def __init__(self, args, **kwargs):
        super().__init__(args, **kwargs)
        self.__ABC_Assignments = []
        self.__ABC_Branches = []
        self.__ABC_Conditionals = []

    def parse_tokens(self, language, tokens):
        super().parse_tokens(language, [])
        for x in tokens:
            if str(x[1]) in MetricBaseABC._assignments:
                self.__ABC_Assignments.append(str(x[1]))
            if str(x[0]) in MetricBaseABC._branches:
                self.__ABC_Branches.append(str(x[1]))
            if str(x[1]) in MetricBaseABC._conditionals:
                self.__ABC_Conditionals.append(str(x[1]))

    def get_results(self):
        self._metrics[MetricBaseABC.METRIC_ABC_ASSIGNMENTS] = len(self.__ABC_Assignments)
        self._metrics[MetricBaseABC.METRIC_ABC_BRANCHES] = len(self.__ABC_Branches)
        self._metrics[MetricBaseABC.METRIC_ABC_CONDITIONALS] = len(list(set(self.__ABC_Conditionals)))
        return self._metrics
