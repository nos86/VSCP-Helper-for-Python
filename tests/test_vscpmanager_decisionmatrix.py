import unittest
import logging
from vscphelper.VSCPManager import DecisionMatrixRow


class decisionMatrixRowMalfunctionTests(unittest.TestCase):
    def test_malformedInit(self, ):
        p = [1,2,3,4,5,6,7,8]
        for i in range(8):
            for k in range(3):
                if k==0:
                    p[i] = 0.1
                    with self.assertRaises(TypeError):
                        DecisionMatrixRow(p[0],p[1],p[2],p[3],
                                          p[4],p[5],p[6],p[7])
                else:
                    if k==1:
                        p[i] = -1
                    else:
                        p[i] = 256
                    with self.assertRaises(ValueError):
                       DecisionMatrixRow(p[0],p[1],p[2],p[3],
                                         p[4],p[5],p[6],p[7])
            p[i]=i+1
            
class decisionMatrixRowFlagTests(unittest.TestCase):        
    def setUp(self, ):
        self.DMRow = DecisionMatrixRow(0,3,10,15,0,0,0,0)
    
    def test_isEnabled(self, ):
        self.assertFalse(self.DMRow.isEnabled())
        self.DMRow.flags = 0x80
        self.assertTrue(self.DMRow.isEnabled())        
    def test_isAddressMatchRequired(self, ):
        self.assertFalse(self.DMRow.isAddressMatchRequired())
        self.DMRow.flags = 0x40
        self.assertTrue(self.DMRow.isAddressMatchRequired())    
    def test_isAddressHardCoded(self, ):
        self.assertFalse(self.DMRow.isAddressHardCoded())
        self.DMRow.flags = 0x20
        self.assertTrue(self.DMRow.isAddressHardCoded())
    def test_matchZoneRequired(self, ):
        self.assertFalse(self.DMRow.matchZoneRequired())
        self.DMRow.flags = 0x10
        self.assertTrue(self.DMRow.matchZoneRequired()) 
    def test_matchSubzoneRequired(self, ):
        self.assertFalse(self.DMRow.matchSubzoneRequired())
        self.DMRow.flags = 0x08
        self.assertTrue(self.DMRow.matchSubzoneRequired())
    def test_checkClassValue(self, ):
        self.assertEqual(self.DMRow.class_mask,266)
        self.assertEqual(self.DMRow.class_filter, 271)
    def test_checkFlagEncoder(self, ):
        self.assertEqual(0x80, DecisionMatrixRow.makeFlagsByte(True, False, False, False, False, 0, 0))
        self.assertEqual(0x40, DecisionMatrixRow.makeFlagsByte(False, True, False, False, False, 0, 0))
        self.assertEqual(0x20, DecisionMatrixRow.makeFlagsByte(False, False, True, False, False, 0, 0))
        self.assertEqual(0x10, DecisionMatrixRow.makeFlagsByte(False, False, False, True, False, 0, 0))
        self.assertEqual(0x08, DecisionMatrixRow.makeFlagsByte(False, False, False, False, True, 0, 0))
        self.assertEqual(0x02, DecisionMatrixRow.makeFlagsByte(False, False, False, False, False, 256, 0))
        self.assertEqual(0x01, DecisionMatrixRow.makeFlagsByte(False, False, False, False, False, 0, 256))
        self.assertEqual(0x00, DecisionMatrixRow.makeFlagsByte(False, False, False, False, False, 255, 255))
    
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
    
