"""pgtree tests"""
import os
import sys
import unittest
from unittest.mock import patch
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pgtree
#from unittest.mock import MagicMock, Mock, patch

class ProctreeTest(unittest.TestCase):
    """tests for pgtree"""
    @patch('os.kill')
    @patch('pgtree.runcmd')
    def test_tree1(self, mock_runcmd, mock_kill):
        """test"""
        print("tree: =======")
        ps_out = """  PID  PPID STIME USER     COMMAND         COMMAND
    1     0 Aug12 root     init            /init
   10     1 Aug12 joknarf  bash            -bash
   20    10 10:10 joknarf  sleep           /bin/sleep 60
   30    10 10:10 joknarf  top             /bin/top
   40     1 11:01 root     bash            -bash"""
        mock_runcmd.return_value = ps_out
        mock_kill.return_value = True
        ptree = pgtree.Proctree(pids=['10'])

        children = {
                '0': ['1'],
                '1': ['10','40'],
                '10': ['20','30'],
        }
        ps_info = {
                '1': {
                    'ppid': '0',
                    'stime': 'Aug12',
                    'user': 'root',
                    'comm': 'init',
                    'args': '/init',
                },
                '10': {
                    'ppid': '1',
                    'stime': 'Aug12',
                    'user': 'joknarf',
                    'comm': 'bash',
                    'args': '-bash',
                },
                '20': {
                    'ppid': '10',
                    'stime': '10:10',
                    'user': 'joknarf',
                    'comm': 'sleep',
                    'args': '/bin/sleep 60',
                },
                '30': {
                    'ppid': '10',
                    'stime': '10:10',
                    'user': 'joknarf',
                    'comm': 'top',
                    'args': '/bin/top',
                },
                '40': {
                    'ppid': '1',
                    'stime': '11:01',
                    'user': 'root',
                    'comm': 'bash',
                    'args': '-bash',
                },
        }
        pids_tree = {
                '10': ['20', '30'],
                '1': ['10'],
                '0': ['1'],
        }
        selected_pids = [ '30', '20', '10' ]
        print(ptree.pids_tree)
        ptree.print_tree(True)
        self.assertEqual(ptree.children, children)
        self.assertEqual(ptree.ps_info, ps_info)
        self.assertEqual(ptree.pids_tree, pids_tree)
        self.assertEqual(ptree.selected_pids, selected_pids)
        ptree.print_tree(True, sig=15, confirmed=True)

    def test_main(self):
        """test"""
        print('main =========')
        pgtree.main([])

    def test_main2(self):
        """test"""
        print('main2 ========')
        pgtree.main(['-c', '-u', 'root', '-f', 'sshd'])
        pgtree.main(['sshd', '-cf', '-u', 'root'])

    @patch('os.kill')
    def test_main3(self, mock_kill):
        """test"""
        print('main3 ========')
        mock_kill.return_value = True
        pgtree.main(['-k','-p','1111'])
        pgtree.main(['-K','-p','1111'])

    def test_main4(self):
        """test"""
        print('main4 ========')
        try:
            pgtree.main(['-h'])
        except SystemExit:
            pass

    @patch('builtins.input')
    def test_main5(self, mock_input):
        """test"""
        print('main5 ========')
        mock_input.return_value = 'n'
        pgtree.main(['-k','sshd'])

    def test_main6(self):
        """test"""
        print('main6 ========')
        pgtree.main(['-a'])

if __name__ == "__main__":
    unittest.main(failfast=True)
