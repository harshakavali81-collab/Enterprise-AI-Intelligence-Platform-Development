import json
import unittest
import engine
class SmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.result=engine.train()
    def test_metrics_are_recorded(self):
        self.assertTrue((engine.ART/'metrics.json').exists())
        self.assertEqual(self.result['mode'],engine.MODE)
        self.assertTrue((engine.ART/'model_manifest.json').exists())
    def test_figure_created(self):
        self.assertTrue((engine.FIG/'evaluation.png').exists())
    def test_predictions_and_validation(self):
        if engine.MODE=='recommend': self.assertEqual(len(engine.recommend(0,5)['item_ids']),5)
        elif engine.MODE=='search':self.assertTrue(engine.retrieve('Fraud alerts need human review.'))
        elif engine.MODE=='retail':self.assertGreaterEqual(engine.infer([30,35,1,0,410])['demand_units'],0)
        elif engine.MODE=='mlops':
            self.assertIn('predicted_class',engine.infer([5.1,3.5,1.4,.2]));self.assertIn('drift_alert',engine.drift_alert([5,3,1,.2]))
        elif engine.MODE in ('medical','vision'):
            self.assertGreaterEqual(engine.infer([.35,.1,.45,.55,.1,.1,.35,.02])['positive_probability'],0)
        else:
            self.assertTrue(0<=engine.infer({'fraud':[4,2,0,0],'churn':[30,1,1,80],'maintenance':[68,2,100,2000],'credit':[60000,.2,0,18]}[engine.MODE])['positive_probability']<=1)
if __name__=='__main__':unittest.main()
