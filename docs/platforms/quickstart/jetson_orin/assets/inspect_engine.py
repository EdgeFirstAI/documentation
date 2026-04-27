import tensorrt as trt
import io
import zipfile

logger = trt.Logger(trt.Logger.WARNING)

def find_zip_start(data: bytes):
    """Return the first local ZIP header offset if a ZIP is embedded."""
    if len(data) < 22:
        return None
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            infos = zf.infolist()
            if not infos:
                return None
            return min(info.header_offset for info in infos)
    except zipfile.BadZipFile:
        return None

def extract_engine_bytes(data: bytes) -> bytes:
    """Strip ZIP trailer or extract engine payload when input is a ZIP."""
    zip_start = find_zip_start(data)
    if zip_start is None:
        return data
    if zip_start > 0:
        return data[:zip_start]

    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        names = [
            info.filename for info in zf.infolist()
            if not info.is_dir()
        ]
        engine_names = [
            name for name in names
            if name.lower().endswith((".engine", ".trt", ".plan"))
        ]
        candidate = engine_names[0] if engine_names else max(
            names,
            key=lambda name: zf.getinfo(name).file_size,
        )
        return zf.read(candidate)

with open("/path/to/model.engine", "rb") as f:
    runtime = trt.Runtime(logger)
    file = f.read()
    engine_blob = extract_engine_bytes(file)
    engine = runtime.deserialize_cuda_engine(engine_blob)

num_tensors = engine.num_io_tensors

for i in range(num_tensors):
    name = engine.get_tensor_name(i)
    dtype = engine.get_tensor_dtype(name)
    shape = engine.get_tensor_shape(name)
    mode = engine.get_tensor_mode(name)  # INPUT or OUTPUT

    print(f"{i}: {name}")
    print(f"   mode: {mode}")
    print(f"   dtype: {dtype}")
    print(f"   shape: {shape}")

fp16 = False

for i in range(engine.num_io_tensors):
    name = engine.get_tensor_name(i)
    if engine.get_tensor_dtype(name) == trt.DataType.HALF:
        fp16 = True

print("Engine uses FP16 I/O:", fp16)
