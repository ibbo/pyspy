import pyspy
import unittest

tests = [pyspy.unittest.database.DatabaseTest,
         pyspy.unittest.database.DatabaseBuilderTest,]

suite = unittest.TestSuite([unittest.TestLoader().loadTestsFromTestCase(i) for i in tests])
unittest.TextTestRunner(verbosity=2).run(suite)
