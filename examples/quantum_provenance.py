from cstlib import MeasurementArchive,MeasurementEntropy
from cstlib.adapters import IBMCountsAdapter
measurement=IBMCountsAdapter.measurement({"000":40,"111":60},backend="example-fixture",job_id="example-job",hardware=False);archive=MeasurementArchive(".cst-quantum/measurements.jsonl");archive.append(measurement);packet=MeasurementEntropy(measurement).sample(32);print(measurement.receipt());print(packet.to_dict())
