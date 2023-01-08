# importing all the necessary libs
import argparse
import ast
import pathlib


# parser for input in the command line
parser = argparse.ArgumentParser(description = 'takes your input.txt and scores.txt files')
parser.add_argument('input', metavar='input', type=str, help = 'enter the name of the file, which consists of paths')
parser.add_argument('scores', metavar='scores', type=str, help = 'enter the name of the file, where the scores will be')
args = parser.parse_args()

# filenames
input_file = args.input
scores_file = args.scores

# class Visitor for ast tree

class Visitor(ast.NodeVisitor):

    def visit(self, node: ast.AST):
        self.generic_visit(node)

# class compare to put all the methods in one place

class FileCompartor():
    # here we turn the files into the tree and clean them
    def cleanTheCode(self, dir1, dir2):
        #create the trees
        with open(dir1) as source:
            ast_tree_1 = ast.parse(source.read())
        with open(dir2) as source:
            ast_tree_2 = ast.parse(source.read())
        # here should be some code with renaming variables and ignoring docstrings
        # I should go through each and every node and encode or somehow ignore the names of variables


        # unparse the trees back into the code

        code_1 = str(ast.unparse(ast_tree_1))
        code_2 = str(ast.unparse(ast_tree_2))


        return code_1, code_2
    # finding paths and making it easy to work with
    def parseCommandLine(self, input, scores):

        paths = []
        with open(str(input)) as input:
            for line in input.readlines():
                filename1, filename2 = line.split()
                paths.append([filename1, filename2])

        return paths
    
    def levenstein(self, str_1, str_2):

        n, m = len(str_1), len(str_2)
        if n > m:
            str_1, str_2 = str_2, str_1
            n, m = m, n

        current_row = range(n + 1)
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                if str_1[j - 1] != str_2[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)

        percentage = (len(str_1) - current_row[n] )/ len(str_1) 

        return percentage

    def comparator(self, input_file, scores_file):
        paths = self.parseCommandLine(input_file, scores_file)

        scores_file = open(scores_file, 'w')

        for i in paths:
            file_1, file_2 = self.cleanTheCode(i[0], i[1])

            scores_file.write(str(self.levenstein(file_1, file_2)))
            scores_file.write('\n')
        
#str_1, str_2 = FileCompartor.cleanTheCode('files/__main__.py', 'plagiat1/__init__.py')

# str_1, str_2 = FileCompartor.cleanTheCode('files/__main__.py', 'plagiat1/__main__.py')

# print(FileCompartor.levenstein(str_1, str_2))

#print(FileCompartor.parseCommandLine(input_file, scores_file))

obj = FileCompartor()

FileCompartor.comparator(obj, input_file, scores_file)
#print(input_file)
print('All Done!')