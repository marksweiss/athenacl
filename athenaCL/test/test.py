#!/usr/bin/python
#-------------------------------------------------------------------------------
# Name:         test.py
# Purpose:      Controller for all tests.
#
# Authors:      Christopher Ariza
#
# License:      GPL
#-------------------------------------------------------------------------------


import unittest, doctest
import os, time, imp, sys
import traceback


from athenaCL.libATH import athenaObj



#-------------------------------------------------------------------------------
class ModuleGather(object):
    '''Utility class for gathering and importing all modules in the music21
    package. 
    '''
    def __init__(self):

        self.dirParent = os.path.dirname(athenaObj.__file__)
        self.modulePaths = []    
        # skip interactive loader application
        self.moduleSkip = ['athenacl.py', 'test.py', '__init__.py']
        self.pathSkip = []
        self._walk()

    def _visitFunc(self, args, dirname, names):
        for file in names:
            if file.endswith('py'):
                fp = os.path.join(dirname, file)
                if not os.path.isdir(fp):
                    self.modulePaths.append(fp)

    def _walk(self):
        # the results of this are stored in self.curFiles, self.dirList
        os.path.walk(self.dirParent, self._visitFunc, '')
        self.modulePaths.sort()
        self.modulePaths.reverse()

    def _getName(self, fp):
        '''Given full file path, find a name for the module
        '''
        fn = fp.replace(self.dirParent, '') # remove parent
        if fn.startswith(os.sep):
            fn = fn[1:]
        fn = fn.replace(os.sep, ':') # replace w/ dots
        fn = fn.replace('.py', '')
        return fn

     
    def load(self):
        loadPass = []
        loadFail = []
        modules = []
        for fp in self.modulePaths:
            skip = False
            for fnSkip in self.moduleSkip:
                if fp.endswith(fnSkip):
                    skip = True   
                    break    
            for dirSkip in self.pathSkip:
                if dirSkip in fp:
                    skip = True  
                    break
            if skip:
                continue

            name = self._getName(fp)

            try:
                mod = imp.load_source(name, fp)
            except Exception as excp: # this takes all exceptions!
                msg = ['failed import:', fp, '\n', 
                    '\tEXCEPTION:', str(excp).strip()]
                print(' '.join(msg))
                continue
            modules.append(mod)

#         from athenaCL.libATH import unit
#         from athenaCL.libATH import prefTools
# 
#         from athenaCL.libATH.omde import oscillator
# 
#         modules = []
#         modules.append(unit)
#         modules.append(oscillator)
#         modules.append(prefTools)


        return modules





def main(testGroup=['test']):
    '''Run all tests. Group can be test and external

    >>> print None
    None
    '''    

    # in case there are any tests here, get a suite to load up later
    s1 = doctest.DocTestSuite(__name__, 
        optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE))

    modGather = ModuleGather()
    modules = modGather.load()

    for module in modules:
        #print _MOD, timeStr, module
        unitTestCases = []
    
        if not hasattr(module, 'Test'):
            print('%s has no Test class' % module)
        else:
            if 'test' in testGroup:
                unitTestCases.append(module.Test)

#         if not hasattr(module, 'TestExternal'):
#             pass
#         else:
#             if 'external' in testGroup or 'testExternal' in testGroup:
#                 unitTestCases.append(module.TestExternal)

        for testCase in unitTestCases:
            s2 = unittest.defaultTestLoader.loadTestsFromTestCase(testCase)
            s1.addTests(s2)

        try:
            s3 = doctest.DocTestSuite(module, 
                optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE))
            s1.addTests(s3)
        except ValueError:
            print('%s cannot load Doctests' % module)
            continue

    print('running Tests...\n')

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(s1)  
                 

#-------------------------------------------------------------------------------
if __name__ == '__main__':

    # if optional command line args are given, assume they are  
    # test group arguments
    if len(sys.argv) >= 2:
        main(sys.argv[1:])
    else:
        main()


