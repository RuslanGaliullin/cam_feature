#!/usr/bin/env python3
# The MIT License (MIT)
#
# Copyright (c) 2021-2023 Yegor Bugayenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import javalang


def ahf(tlist) -> int:
    """Ratio of private/protected attributes to all attributes in a class.
    :rtype: float
    """
    declaration = tlist[0][1].filter(javalang.tree.FieldDeclaration)
    fields = list(field for field in declaration)
    hidden = 0
    total = 0
    for path, node in fields:
        del path
        if 'private' in node.modifiers or 'protected' in node.modifiers:
            hidden += 1
        total += 1
    if total == 0:
        return 0
    return hidden / total


def sahf(tlist) -> int:
    """Ratio of private/protected attributes to static attributes in a class.
    :rtype: float
    """
    declaration = tlist[0][1].filter(javalang.tree.FieldDeclaration)
    fields = list(field for field in declaration)
    hidden = 0
    total = 0
    for path, node in fields:
        del path
        if 'static' not in node.modifiers:
            continue
        if 'private' in node.modifiers or 'protected' in node.modifiers:
            hidden += 1
        total += 1
    if total == 0:
        return 0
    return hidden / total


def nomp(tlist) -> int:
    """Total number of parameters in all class methods.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.MethodDeclaration)
    mlist = list(method for method in declaration)
    total = 0
    for path, node in mlist:
        del path
        total += len(node.parameters)
    return total


def nosmp(tlist) -> int:
    """Total number of parameters in static class methods.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.MethodDeclaration)
    mlist = list(method for method in declaration)
    total = 0
    for path, node in mlist:
        del path
        if 'static' not in node.modifiers:
            continue
        total += len(node.parameters)
    return total


def mxnomp(tlist) -> int:
    """Maximum number of parameters in all class methods.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.MethodDeclaration)
    mlist = list(method for method in declaration)
    maximum = 0
    for path, node in mlist:
        del path
        maximum = max(maximum, len(node.parameters))
    return maximum


def mxnosmp(tlist) -> int:
    """Maximum number of parameters in static class methods.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.MethodDeclaration)
    mlist = list(method for method in declaration)
    maximum = 0
    for path, node in mlist:
        del path
        if 'static' not in node.modifiers:
            continue
        maximum = max(maximum, len(node.parameters))
    return maximum


def nom(tlist) -> int:
    """Number of methods that are annotated with @Override.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.MethodDeclaration)
    mlist = list(method for method in declaration)
    total = 0
    for path, node in mlist:
        del path
        annotations = list(annotation.name for annotation in node.annotations)
        if 'Override' in annotations:
            total += 1
            continue
    return total


def attrs(tlist) -> int:
    """Count non-static attributes.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.FieldDeclaration)
    fields = list(field for field in declaration)
    found = 0
    for path, node in fields:
        del path
        if 'static' not in node.modifiers:
            found += 1
    return found


def sattrs(tlist) -> int:
    """Count static attributes.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.FieldDeclaration)
    fields = list(field for field in declaration)
    found = 0
    for path, node in fields:
        del path
        if 'static' in node.modifiers:
            found += 1
    return found


def ctors(tlist) -> int:
    """Count constructors.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.ConstructorDeclaration)
    clist = list(method for method in declaration)
    return len(clist)


def methods(tlist) -> int:
    """Count non-static methods.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.MethodDeclaration)
    mlist = list(method for method in declaration)
    found = 0
    for path, node in mlist:
        del path
        if 'static' not in node.modifiers:
            found += 1
    return found


def smethods(tlist) -> int:
    """Count static methods.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.MethodDeclaration)
    mlist = list(method for method in declaration)
    found = 0
    for path, node in mlist:
        del path
        if 'static' in node.modifiers:
            found += 1
    return found


def mhf(tlist) -> int:
    """Calculate Method Hiding Factor (MHF), which is the ratio
    between private+protected methods and all methods.
    :rtype: float
    """
    declaration = tlist[0][1].filter(javalang.tree.MethodDeclaration)
    mlist = list(method for method in declaration)
    hidden = 0
    total = 0
    for path, node in mlist:
        del path
        if 'public' not in node.modifiers:
            hidden += 1
        total += 1
    if total == 0:
        return 0
    return hidden / total


def smhf(tlist) -> int:
    """Calculate Static Method Hiding Factor (MHF), which is the ratio
    between private+protected methods and all methods (which are static).
    :rtype: float
    """
    declaration = tlist[0][1].filter(javalang.tree.MethodDeclaration)
    mlist = list(method for method in declaration)
    hidden = 0
    total = 0
    for path, node in mlist:
        del path
        if 'static' not in node.modifiers:
            continue
        if 'public' not in node.modifiers:
            hidden += 1
        total += 1
    if total == 0:
        return 0
    return hidden / total


def ncss(parser_class) -> int:
    """Count the NCSS (non-commenting source statement) lines.
    :rtype: int
    """
    value = 0
    for path, node in parser_class:
        del path
        node_type = str(type(node))
        if 'Statement' in node_type:
            value += 1
        elif node_type == 'VariableDeclarator':
            value += 1
        elif node_type == 'Assignment':
            value += 1
        elif 'Declaration' in node_type \
                and 'LocalVariableDeclaration' not in node_type \
                and 'PackageDeclaration' not in node_type:
            value += 1
    return value


def impls(tlist) -> int:
    """Count the number of interfaces the class implements.
    r:type: int
    """
    return len(tlist[0][1].implements or [])


def extnds(tlist) -> int:
    """Count the number of classes this class extends (0 or 1).
    r:type: int
    """
    return 0 if tlist[0][1].extends is None else 1


def final(tlist) -> int:
    """Return 1 if the class is final, zero otherwise.
    r:type: int
    """
    return 1 if 'final' in tlist[0][1].modifiers else 0


def gnrcs(tlist) -> int:
    """Return number of type parameters (generics).
    r:type: int
    """
    return len(tlist[0][1].type_parameters or [])


def annts(tlist) -> int:
    """Return number of annotations of the class.
    r:type: int
    """
    return len(tlist[0][1].annotations or [])


def varcomp(tlist) -> float:
    """Return average number of parts in variable names in class.
    r:type: float
    """
    parts, variables = 0, 0
    for _, node in tlist[0][1].filter(javalang.tree.VariableDeclarator):
        if (name := node.name) != '':
            variables += 1
            parts += 1
            for letter in name[1:]:
                if letter == letter.upper():
                    parts += 1

    if variables == 0:
        return 0
    return parts / variables


class NotClassError(Exception):
    """If it's not a class"""


if __name__ == '__main__':
    JAVA = sys.argv[1]
    METRICS = sys.argv[2]
    with open(JAVA, encoding='utf-8', errors='ignore') as file:
        try:
            raw = javalang.parse.parse(file.read())
            tree = raw.filter(javalang.tree.ClassDeclaration)
            if not (tree_class := list((value for value in tree))):
                raise NotClassError('This is not a class')
            with open(METRICS, 'a', encoding='utf-8') as metric:
                metric.write(f'nooa {attrs(tree_class)} '
                             f'Number of Non-Static (Object) Attributes\n')
                metric.write(f'nosa {sattrs(tree_class)} '
                             f'Number of Static Attributes\n')
                metric.write(f'nocc {ctors(tree_class)} '
                             f'Number of Class Constructors\n')
                metric.write(f'noom {methods(tree_class)} '
                             f'Number of Non-Static (Object) Methods\n')
                metric.write(f'nocm {smethods(tree_class)} '
                             f'Number of Static (Class) Methods\n')
                metric.write(f'ncss {ncss(raw)} '
                             f'Non-Commenting Source Statements (NCSS)\n')
                metric.write(f'noii {impls(tree_class)} '
                             f'Number of Implemented Interfaces\n')
                metric.write(f'napc {extnds(tree_class)} '
                             f'Number of Ancestor (Parent) Classes\n')
                metric.write(f'notp {gnrcs(tree_class)} '
                             f'Number of Type Parameters (Generics)\n')
                metric.write(f'final {final(tree_class)} '
                             f'Class is Final\n')
                metric.write(f'noca {annts(tree_class)} '
                             f'Number of Class Annotations\n')
                metric.write(f'varcomp {varcomp(tree_class)} '
                             f'Average number of parts in variable names\n')
                metric.write(f'mhf {mhf(tree_class)} '
                             f'Method Hiding Factor (MHF)\n')
                metric.write(f'smhf {smhf(tree_class)} '
                             f'Static Method Hiding Factor (MHF)\n')
                metric.write(f'ahf {ahf(tree_class)} '
                             f'Method Attribute Factor (AHF)\n')
                metric.write(f'sahf {sahf(tree_class)} '
                             f'Static Attribute Hiding Factor (SAHF)\n')
                metric.write(f'nomp {nomp(tree_class)} '
                             f'Number of Method Parameters (NOMP)\n')
                metric.write(f'nosmp {nosmp(tree_class)} '
                             f'Number of Static Method Parameters (NOSMP)\n')
                metric.write(f'mxnomp {mxnomp(tree_class)} '
                             f'Maximum of Method Parameters (MxNOMP)\n')
                metric.write(f'mxnosmp {mxnosmp(tree_class)} '
                             f'Maximum of Static Method Parameters (MxNOSMP)\n')
                metric.write(f'nom {nom(tree_class)} '
                             f'Number of Overriding Methods (NOM)\n')
        except FileNotFoundError as exception:
            message = f"{type(exception).__name__} {str(exception)}: {JAVA}"
            sys.exit(message)
