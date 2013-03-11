import codecs
import re

from coverage.report import Reporter


def read_file_lines(filename):
    with open(filename, "r") as opened_file:
        encoding_line = opened_file.readline()

    encoding_regex = re.compile('# -\*- coding:(.*) -\*-')
    results = re.search(encoding_regex, encoding_line)
    if results:
        encoding = results.groups()[0]
    else:
        encoding = 'utf-8'
    with codecs.open(filename, "r", encoding) as fp:
        source = fp.readlines()
    return source


class CoverallsReporter(Reporter):
    def report(self, base_dir):
        self.find_code_units(None)
        ret = []
        for cu in self.code_units:
            source = read_file_lines(cu.filename)
            analysis = self.coverage._analyze(cu)
            coverage_list = [None for _ in source]
            for lineno, line in enumerate(source):
                if lineno + 1 in analysis.statements:
                    coverage_list[lineno] = int(lineno + 1 not in analysis.missing)
            ret.append({
                'name': cu.filename.replace(base_dir, '').lstrip('/'),
                'source': ''.join(source).rstrip(),
                'coverage': coverage_list,
            })
        return ret
