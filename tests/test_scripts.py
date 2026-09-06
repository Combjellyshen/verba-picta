import copy, io, json, tempfile, unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import sys
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]/'canva-abstract-portrait'
sys.path.insert(0,str(ROOT/'scripts'))
import select_artist as sel
import reference_assets as refs
import verify_delivery as delivery
CAT=sel.read_json(ROOT/'references/artist-catalog.json')

class ScriptTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=Path(__file__).parent,prefix='portrait-test-')
        self.dir=Path(self.temp.name)
    def tearDown(self): self.temp.cleanup()
    def test_01_catalog(self):
        self.assertEqual(refs.validate(CAT,ROOT),[])
        self.assertEqual(len(CAT['artists']),14)
    def test_02_alias_and_exclusions(self):
        state={}; result,_=sel.choose(CAT,state,artist='Joan Miro',excluded=['毕加索','赵无极'])
        self.assertEqual(result['artist_id'],'joan-miro')
        self.assertNotIn('pablo-picasso',result['eligible_artist_ids'])
        self.assertEqual(len(result['eligible_artist_ids']),12)
    def test_03_empty_pool_and_typo(self):
        with self.assertRaises(ValueError): sel.choose(CAT,{},excluded=[a['id'] for a in CAT['artists']])
        with self.assertRaises(ValueError): sel.choose(CAT,{},excluded=['not-an-artist'])
    def test_04_resume_and_conflict(self):
        state={}; first,_=sel.choose(CAT,state,artist='蒙德里安'); snapshot=copy.deepcopy(state)
        second,reused=sel.choose(CAT,state,seed=42)
        self.assertTrue(reused); self.assertEqual(first,second); self.assertEqual(state,snapshot)
        with self.assertRaises(ValueError): sel.choose(CAT,state,artist='克利')
        self.assertEqual(state,snapshot)
    def test_05_uniform_artist_population(self):
        captured=[]
        class RNG:
            def choice(self,pool): captured.extend(pool); return pool[0]
        modified=copy.deepcopy(CAT); modified['artworks']*=3
        with patch.object(sel.random,'SystemRandom',return_value=RNG()):
            result,_=sel.choose(modified,{})
        self.assertEqual(len(captured),14)
        self.assertEqual(len({a['id'] for a in captured}),14)
        self.assertEqual(result['probability'],'1/14')
    def test_06_redraw_preserves_evidence_invalidates_checks(self):
        state={'core_observations':[{'id':'E1'}],'quality_checks':[{'scale':'detail'}],'export_review':{'viewed_at':'old'},'canva':{'design_url':'https://www.canva.com/design/TEST/edit','save_observation':'old'}}
        sel.choose(CAT,state,artist='克利'); state['direction_id']='old-direction'
        sel.choose(CAT,state,artist='赵无极',redraw=True)
        self.assertEqual(state['core_observations'],[{'id':'E1'}])
        self.assertNotIn('quality_checks',state);self.assertNotIn('save_observation',state['canva'])
        self.assertNotIn('direction_id',state)
        self.assertEqual(state['selection_history'][0]['artist_id'],'paul-klee')
        self.assertTrue(state['revision_history'])
    def prepare_args(self):
        return SimpleNamespace(session=self.dir/'session.json',out=self.dir/'references.json',direction=None,works=None,replace=False)
    def test_07_prepare_all_defaults(self):
        for artist in CAT['artists']:
            args=self.prepare_args();args.replace=True
            state={};sel.choose(CAT,state,artist=artist['id']);sel.write_json(args.session,state)
            refs.prepare(args,CAT); manifest=sel.read_json(args.out)
            self.assertTrue(3<=len(manifest['artworks'])<=5)
            self.assertTrue(all(w['artist_id']==artist['id'] for w in manifest['artworks']))
    def test_08_prepare_resume_keeps_notes(self):
        args=self.prepare_args();state={};sel.choose(CAT,state,artist='克利');sel.write_json(args.session,state)
        refs.prepare(args,CAT);m=sel.read_json(args.out);m['viewed_notes']='actual reference notes';sel.write_json(args.out,m)
        self.assertTrue(refs.prepare(args,CAT)['reused'])
        self.assertEqual(sel.read_json(args.out)['viewed_notes'],'actual reference notes')
        args.direction='color-architecture'
        with self.assertRaises(ValueError): refs.prepare(args,CAT)
    def test_09_reject_bad_membership(self):
        c=copy.deepcopy(CAT); c['artists'][0]['directions'][0]['work_ids'][0]='moma_78311'
        self.assertTrue(refs.validate(c,ROOT))
    def test_10_download_rejects_html(self):
        manifest=self.dir/'manifest.json';sel.write_json(manifest,{'artworks':[{'id':'test_ref','collection_url':'https://museum.example/item','image':{'url':'https://museum.example/image'}}]})
        class Response(io.BytesIO):
            def geturl(self): return 'https://museum.example/image'
        args=SimpleNamespace(manifest=manifest,out_dir=self.dir/'cache',refresh=False,timeout=1,max_mb=1,contact_sheet=None)
        with patch.object(refs.urllib.request,'urlopen',return_value=Response(b'<html>not an image</html>')),patch.object(refs.time,'sleep'):
            result=refs.fetch(args)
        self.assertFalse(result['all_available']);self.assertEqual(sel.read_json(manifest)['artworks'][0]['fetch_result']['status'],'unavailable')
    def test_11_valid_export_missing_reviews(self):
        p=self.dir/'decoder-fixture.png';Image.new('RGB',(1600,2000),'white').save(p)
        state={'canvas':{'width':1600,'height':2000},'canva':{'design_url':'https://www.canva.com/design/TEST/edit'}}
        report=delivery.verify(state,p)
        self.assertTrue(report['mechanical_checks_passed']);self.assertFalse(report['manual_records_present'])
        self.assertTrue(any('detail' in v for v in report['missing_manual_records']))
    def test_12_corrupt_and_wrong_ratio(self):
        p=self.dir/'invalid.png';p.write_bytes(b'not PNG')
        with self.assertRaises(OSError):delivery.verify({},p)
        p=self.dir/'ratio-fixture.png';Image.new('RGB',(2000,1000),'white').save(p)
        r=delivery.verify({'canvas':{'width':1600,'height':2000},'canva':{'design_url':'https://www.canva.com/design/TEST/edit'}},p)
        self.assertTrue(any('aspect ratio' in e for e in r['errors']))
    def test_13_complete_records_are_only_reports(self):
        p=self.dir/'decoder-fixture.png';Image.new('RGB',(1600,2000),'white').save(p)
        state={'canvas':{'width':1600,'height':2000},'canva':{'design_url':'https://www.canva.com/design/TEST/edit','save_observed_at':'test','save_observation':'test fixture, not a real Canva save','editable_elements':['test'],'reference_underlay_status':'not_used'},'quality_checks':[{'scale':s,'checked_at':'test','observation':'fixture'} for s in ('thumbnail','normal','detail')],'export_review':{'viewed_at':'test','observation':'fixture'}}
        r=delivery.verify(state,p)
        self.assertTrue(r['manual_records_present']);self.assertIn('Does not verify Canva save',r['scope'])
    def test_14_atomic_write_retries_transient_lock(self):
        target=self.dir/'state.json';real=sel.os.replace; calls=[]
        def transient(src,dst):
            calls.append(1)
            if len(calls)==1:raise PermissionError('temporary sharing lock')
            return real(src,dst)
        with patch.object(sel.os,'replace',side_effect=transient),patch.object(sel.time,'sleep'):
            sel.write_json(target,{'preserved':True})
        self.assertEqual(sel.read_json(target),{'preserved':True});self.assertEqual(len(calls),2)

if __name__=='__main__':unittest.main(verbosity=2)
