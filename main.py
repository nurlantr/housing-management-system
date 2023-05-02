from models import Dormitory
from populator import Populator

nu = Dormitory()
populator = Populator("input.csv", nu)

populator.pair()

populator.populate([], [], randomize = True)

populator.to_csv("output", "test_output.csv")
populator.upload_csv("upload", "test_upload.csv")








