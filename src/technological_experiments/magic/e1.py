import sys
import os

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '../../img', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.processor.faces.face_detector.insightface_face_detector import InsightfaceFaceDetector
from src.img.processor.types import DictStorable

o = InsightfaceFaceDetector(model_name='retinaface_mnet025_v2', color=(0, 200, 50))

from pprint import pprint

print('+' * 80)
pprint(o.to_dict())

in_dict = {'class': 'InsightfaceFaceDetector',
 'description': 'Insightface face detector as img processor.\n'
                '@credit https://github.com/deepinsight/insightface',
 'module': 'src.img.processor.face_detector.insightface_face_detector',
 'params': [{'1.name': 'model_name',
             '2.value': 'retinaface_mnet025_v2',
             '3.default': 'retinaface_mnet025_v2',
             '4.type': {'class': 'StrType',
                        'description': 'String value',
                        'module': 'src.img.processor.dict_storable',
                        'params': [{'1.name': 'decr',
                                    '2.value': 'Name of the model'}]}},
            {'1.name': 'find_best',
             '2.value': False,
             '3.default': False,
             '4.type': {'class': 'BoolType',
                        'description': 'Boolean value',
                        'module': 'src.img.processor.dict_storable',
                        'params': [{'1.name': 'decr',
                                    '2.value': 'True for only one best '
                                               'face'}]}},
            {'1.name': 'ctx_id',
             '2.value': -1,
             '3.default': -1,
             '4.type': {'class': 'IntType',
                        'description': 'Integer value',
                        'module': 'src.img.processor.dict_storable',
                        'params': [{'1.name': 'decr',
                                    '2.value': 'Index of GPU, ctx_id < 0 for '
                                               'CPU'}]}},
            {'1.name': 'color',
             '2.value': (0, 200, 50),
             '3.default': (123, 41, 87),
             '4.type': {'class': 'BGRColorType',
                        'description': 'Color BGR value',
                        'module': 'src.img.processor.dict_storable',
                        'params': [{'1.name': 'decr',
                                    '2.value': 'Color for face frame'}]}}]}

f = DictStorable.from_dict(in_dict=in_dict)
print(f)
print('#'*80)
pprint(f.to_dict())