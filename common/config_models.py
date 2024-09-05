from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import List, Optional, Union, get_type_hints

from common.utils import unwrap


class config_config_model(BaseModel):
    config: Optional[str] = Field(
        None, description="Path to an overriding config.yml file"
    )


class network_config_model(BaseModel):
    host: Optional[str] = Field("127.0.0.1", description="The IP to host on")
    port: Optional[int] = Field(5000, description="The port to host on")
    disable_auth: Optional[bool] = Field(
        False, description="Disable HTTP token authentication with requests"
    )
    send_tracebacks: Optional[bool] = Field(
        False, description="Decide whether to send error tracebacks over the API"
    )
    api_servers: Optional[List[str]] = Field(
        [
            "OAI",
        ],
        description="API servers to enable. Options: (OAI, Kobold)",
    )


class logging_config_model(BaseModel):
    log_prompt: Optional[bool] = Field(False, description="Enable prompt logging")
    log_generation_params: Optional[bool] = Field(
        False, description="Enable generation parameter logging"
    )
    log_requests: Optional[bool] = Field(False, description="Enable request logging")


class model_config_model(BaseModel):
    model_dir: str = Field(
        "models",
        description="Overrides the directory to look for models (default: models). Windows users, do NOT put this path in quotes.",
    )
    use_dummy_models: Optional[bool] = Field(
        False,
        description="Sends dummy model names when the models endpoint is queried. Enable this if looking for specific OAI models.",
    )
    model_name: Optional[str] = Field(
        None,
        description="An initial model to load. Make sure the model is located in the model directory! REQUIRED: This must be filled out to load a model on startup.",
    )
    use_as_default: List[str] = Field(
        default_factory=list,
        description="Names of args to use as a default fallback for API load requests (default: []). Example: ['max_seq_len', 'cache_mode']",
    )
    max_seq_len: Optional[int] = Field(
        None,
        description="Max sequence length. Fetched from the model's base sequence length in config.json by default.",
    )
    override_base_seq_len: Optional[int] = Field(
        None,
        description="Overrides base model context length. WARNING: Only use this if the model's base sequence length is incorrect.",
    )
    tensor_parallel: Optional[bool] = Field(
        False,
        description="Load model with tensor parallelism. Fallback to autosplit if GPU split isn't provided.",
    )
    gpu_split_auto: Optional[bool] = Field(
        True,
        description="Automatically allocate resources to GPUs (default: True). Not parsed for single GPU users.",
    )
    autosplit_reserve: List[int] = Field(
        [96],
        description="Reserve VRAM used for autosplit loading (default: 96 MB on GPU 0). Represented as an array of MB per GPU.",
    )
    gpu_split: List[float] = Field(
        default_factory=list,
        description="An integer array of GBs of VRAM to split between GPUs (default: []). Used with tensor parallelism.",
    )
    rope_scale: Optional[float] = Field(
        1.0,
        description="Rope scale (default: 1.0). Same as compress_pos_emb. Only use if the model was trained on long context with rope.",
    )
    rope_alpha: Optional[Union[float, str]] = Field(
        1.0,
        description="Rope alpha (default: 1.0). Same as alpha_value. Set to 'auto' to auto-calculate.",
    )
    cache_mode: Optional[str] = Field(
        "FP16",
        description="Enable different cache modes for VRAM savings (default: FP16). Possible values: FP16, Q8, Q6, Q4.",
    )
    cache_size: Optional[int] = Field(
        None,
        description="Size of the prompt cache to allocate (default: max_seq_len). Must be a multiple of 256.",
    )
    chunk_size: Optional[int] = Field(
        2048,
        description="Chunk size for prompt ingestion (default: 2048). A lower value reduces VRAM usage but decreases ingestion speed.",
    )
    max_batch_size: Optional[int] = Field(
        None,
        description="Set the maximum number of prompts to process at one time (default: None/Automatic). Automatically calculated if left blank.",
    )
    prompt_template: Optional[str] = Field(
        None,
        description="Set the prompt template for this model. If empty, attempts to look for the model's chat template.",
    )
    num_experts_per_token: Optional[int] = Field(
        None,
        description="Number of experts to use per token. Fetched from the model's config.json. For MoE models only.",
    )
    fasttensors: Optional[bool] = Field(
        False,
        description="Enables fasttensors to possibly increase model loading speeds (default: False).",
    )


class draft_model_config_model(BaseModel):
    draft_model_dir: Optional[str] = Field(
        "models",
        description="Overrides the directory to look for draft models (default: models)",
    )
    draft_model_name: Optional[str] = Field(
        None,
        description="An initial draft model to load. Ensure the model is in the model directory.",
    )
    draft_rope_scale: Optional[float] = Field(
        1.0,
        description="Rope scale for draft models (default: 1.0). Same as compress_pos_emb. Use if the draft model was trained on long context with rope.",
    )
    draft_rope_alpha: Optional[float] = Field(
        None,
        description="Rope alpha for draft models (default: None). Same as alpha_value. Leave blank to auto-calculate the alpha value.",
    )
    draft_cache_mode: Optional[str] = Field(
        "FP16",
        description="Cache mode for draft models to save VRAM (default: FP16). Possible values: FP16, Q8, Q6, Q4.",
    )


class lora_instance_model(BaseModel):
    name: str = Field(..., description="Name of the LoRA model")
    scaling: float = Field(
        1.0, description="Scaling factor for the LoRA model (default: 1.0)"
    )


class lora_config_model(BaseModel):
    lora_dir: Optional[str] = Field(
        "loras", description="Directory to look for LoRAs (default: 'loras')"
    )
    loras: Optional[List[lora_instance_model]] = Field(
        None,
        description="List of LoRAs to load and associated scaling factors (default scaling: 1.0)",
    )


class sampling_config_model(BaseModel):
    override_preset: Optional[str] = Field(
        None, description="Select a sampler override preset"
    )


class developer_config_model(BaseModel):
    unsafe_launch: Optional[bool] = Field(
        False, description="Skip Exllamav2 version check"
    )
    disable_request_streaming: Optional[bool] = Field(
        False, description="Disables API request streaming"
    )
    cuda_malloc_backend: Optional[bool] = Field(
        False, description="Runs with the pytorch CUDA malloc backend"
    )
    uvloop: Optional[bool] = Field(
        False, description="Run asyncio using Uvloop or Winloop"
    )
    realtime_process_priority: Optional[bool] = Field(
        False,
        description="Set process to use a higher priority For realtime process priority, run as administrator or sudo Otherwise, the priority will be set to high",
    )


class embeddings_config_model(BaseModel):
    embedding_model_dir: Optional[str] = Field(
        "models",
        description="Overrides directory to look for embedding models (default: models)",
    )
    embeddings_device: Optional[str] = Field(
        "cpu",
        description="Device to load embedding models on (default: cpu). Possible values: cpu, auto, cuda. If using an AMD GPU, set this value to 'cuda'.",
    )
    embedding_model_name: Optional[str] = Field(
        None, description="The embeddings model to load"
    )


class tabby_config_model(BaseModel):
    config: config_config_model = Field(default_factory=config_config_model)
    network: network_config_model = Field(default_factory=network_config_model)
    logging: logging_config_model = Field(default_factory=logging_config_model)
    model: model_config_model = Field(default_factory=model_config_model)
    draft_model: draft_model_config_model = Field(
        default_factory=draft_model_config_model
    )
    lora: lora_config_model = Field(default_factory=lora_config_model)
    sampling: sampling_config_model = Field(default_factory=sampling_config_model)
    developer: developer_config_model = Field(default_factory=developer_config_model)
    embeddings: embeddings_config_model = Field(default_factory=embeddings_config_model)

    @model_validator(mode="before")
    def set_defaults(cls, values):
        for field_name, field_value in values.items():
            if field_value is None:
                default_instance = cls.__annotations__[field_name]().dict()
                values[field_name] = cls.__annotations__[field_name](**default_instance)
        return values

    model_config = ConfigDict(validate_assignment=True)


def generate_config_file(filename="config_sample.yml", indentation=2):
    schema = tabby_config_model.model_json_schema()

    def dump_def(id: str, indent=2):
        yaml = ""
        indent = " " * indentation * indent
        id = id.split("/")[-1]

        section = schema["$defs"][id]["properties"]
        for property in section.keys():  # get type
            comment = section[property]["description"]
            yaml += f"{indent}# {comment}\n"

            value = unwrap(section[property].get("default"), "")
            yaml += f"{indent}{property}: {value}\n\n"

        return yaml + "\n"

    yaml = ""
    for section in schema["properties"].keys():
        yaml += f"{section}:\n"
        yaml += dump_def(schema["properties"][section]["$ref"])
        yaml += "\n"

    with open(filename, "w") as f:
        f.write(yaml)


# generate_config_file("test.yml")