"""
Vinh-Trung Luu for Sentiance Technical test
"""
import unittest
import TechnicalTest


class TechnicalTest_UnitTest(unittest.TestCase):
    """Tests for 'TechnicalTest.py'."""

    def testCalculateListMedian(self):
        self.assertEqual(TechnicalTest.calculateListMedian([1,3,2]),2)
        self.assertEqual(TechnicalTest.calculateListMedian([1]),1)
        self.assertEqual(TechnicalTest.calculateListMedian([1,3,2,4]),2.5)

    def testCalculateListConfidenceInterval(self):
        self.assertEqual(TechnicalTest.confidenceInterval([1,3,5,7,9],0.95),2.7718076486993555)
        self.assertEqual(TechnicalTest.confidenceInterval([4,4,4,4],0.95),0)

    def testDow(self):
        self.assertEqual(TechnicalTest.dow(TechnicalTest.getDateTimeFromString('201809160036+0100')),"Sunday")
        self.assertEqual(TechnicalTest.dow(TechnicalTest.getDateTimeFromString('201809170036+0100')),"Monday")
        self.assertEqual(TechnicalTest.dow(TechnicalTest.getDateTimeFromString('201809150036+0100')),"Saturday")

if __name__ == '__main__':
    unittest.main()