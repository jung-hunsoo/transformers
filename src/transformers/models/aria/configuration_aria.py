#                🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
#           This file was automatically generated from src/transformers/models/aria/modular_aria.py.
#               Do NOT edit this file manually as any edits will be overwritten by the generation of
#             the file from the modular. If any change should be done, please apply the change to the
#                          modular_aria.py file directly. One of our CI enforces this.
#                🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
import logging
import os
from typing import Union

from ...configuration_utils import PretrainedConfig
from ...modeling_rope_utils import rope_config_validation
from ...utils import logging


logger = logging.get_logger(__name__)


class AriaVisionConfig(PretrainedConfig):
    r"""
        This is the configuration class to store the configuration of a [`AriaVisionModel`]. It is used to instantiate a
        Aria vision encoder according to the specified arguments, defining the model architecture. Instantiating a
        configuration with the defaults will yield a similar configuration to that of the vision encoder of the Aria
        [google/aria-base-patch16-224](https://huggingface.co/google/aria-base-patch16-224) architecture.

        Configuration objects inherit from [`PretrainedConfig`] and can be used to control the model outputs. Read the
        documentation from [`PretrainedConfig`] for more information.

        Args:
            hidden_size (`int`, *optional*, defaults to 768):
                Dimensionality of the encoder layers and the pooler layer.
            intermediate_size (`int`, *optional*, defaults to 3072):
                Dimensionality of the "intermediate" (i.e., feed-forward) layer in the Transformer encoder.
            num_hidden_layers (`int`, *optional*, defaults to 12):
                Number of hidden layers in the Transformer encoder.
            num_attention_heads (`int`, *optional*, defaults to 12):
                Number of attention heads for each attention layer in the Transformer encoder.
            num_channels (`int`, *optional*, defaults to 3):
                Number of channels in the input images.
            image_size (`int`, *optional*, defaults to 224):
                The size (resolution) of each image.
            patch_size (`int`, *optional*, defaults to 16):
                The size (resolution) of each patch.
            hidden_act (`str` or `function`, *optional*, defaults to `"gelu_pytorch_tanh"`):
                The non-linear activation function (function or string) in the encoder and pooler. If string, `"gelu"`,
                `"relu"`, `"selu"` and `"gelu_new"` `"quick_gelu"` are supported.
            layer_norm_eps (`float`, *optional*, defaults to 1e-06):
                The epsilon used by the layer normalization layers.
            attention_dropout (`float`, *optional*, defaults to 0.0):
                The dropout ratio for the attention probabilities.

        Example:

        ```python
        >>> from transformers import AriaVisionConfig, AriaVisionModel

        >>> # Initializing a AriaVisionConfig with google/aria-base-patch16-224 style configuration
        >>> configuration = AriaVisionConfig()

        >>> # Initializing a AriaVisionModel (with random weights) from the google/aria-base-patch16-224 style configuration
        >>> model = AriaVisionModel(configuration)

        >>> # Accessing the model configuration
        >>> configuration = model.config
        ```
    Configuration class for AriaVisionModel."""

    model_type = "aria_vision_model"

    def __init__(
        self,
        hidden_size=768,
        intermediate_size=3072,
        num_hidden_layers=12,
        num_attention_heads=12,
        num_channels=3,
        image_size=224,
        patch_size=16,
        hidden_act="gelu_pytorch_tanh",
        layer_norm_eps=1e-6,
        attention_dropout=0.0,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.hidden_size = hidden_size
        self.intermediate_size = intermediate_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.num_channels = num_channels
        self.patch_size = patch_size
        self.image_size = image_size
        self.attention_dropout = attention_dropout
        self.layer_norm_eps = layer_norm_eps
        self._attn_implementation = "flash_attention_2"
        self.hidden_act = hidden_act

    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path: Union[str, os.PathLike], **kwargs) -> "PretrainedConfig":
        cls._set_token_in_kwargs(kwargs)

        config_dict, kwargs = cls.get_config_dict(pretrained_model_name_or_path, **kwargs)

        # get the vision config dict if we are loading from AriaConfig
        if config_dict.get("model_type") == "aria":
            config_dict = config_dict["vision_config"]

        if "model_type" in config_dict and hasattr(cls, "model_type") and config_dict["model_type"] != cls.model_type:
            logger.warning(
                f"You are using a model of type {config_dict['model_type']} to instantiate a model of type "
                f"{cls.model_type}. This is not supported for all configurations of models and can yield errors."
            )

        return cls.from_dict(config_dict, **kwargs)


class AriaModelConfig(PretrainedConfig):
    """
    Configuration class for Aria language model.

    This class extends the LlamaConfig to include additional parameters specific to the Mixture of Experts (MoE) architecture.

    Args:
        moe_intermediate_size (`int`): The intermediate size for MoE layers. Default is 4096.
        moe_num_experts (int): The number of experts in the MoE layer. Default is 8.
        moe_topk (int): The number of top experts to route to for each token. Default is 2.
        moe_z_loss_coeff (float): The coefficient for the auxiliary z-loss. Default is 1e-5.
        moe_aux_loss_coeff (float): The coefficient for the auxiliary load balancing loss. Default is 1e-3.
        moe_num_shared_experts (int): The number of shared experts. Default is 2.
        **kwargs: Additional keyword arguments to be passed to the parent LlamaConfig.
    """

    model_type = "aria"
    keys_to_ignore_at_inference = ["past_key_values"]

    def __init__(
        self,
        vocab_size=32000,
        hidden_size=4096,
        intermediate_size=11008,
        num_hidden_layers=32,
        num_attention_heads=32,
        num_key_value_heads=None,
        hidden_act="silu",
        max_position_embeddings=2048,
        initializer_range=0.02,
        rms_norm_eps=1e-6,
        use_cache=True,
        pad_token_id=None,
        bos_token_id=1,
        eos_token_id=2,
        pretraining_tp=1,
        tie_word_embeddings=False,
        rope_theta=10000.0,
        rope_scaling=None,
        attention_bias=False,
        attention_dropout=0.0,
        mlp_bias=False,
        head_dim=None,
        moe_intermediate_size: int = 4096,
        moe_num_experts: int = 8,
        moe_topk: int = 2,
        moe_z_loss_coeff: float = 1e-5,
        moe_aux_loss_coeff: float = 1e-3,
        moe_num_shared_experts: int = 2,
        **kwargs,
    ):
        self.vocab_size = vocab_size
        self.max_position_embeddings = max_position_embeddings
        self.hidden_size = hidden_size
        self.intermediate_size = intermediate_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads

        # for backward compatibility
        if num_key_value_heads is None:
            num_key_value_heads = num_attention_heads

        self.num_key_value_heads = num_key_value_heads
        self.hidden_act = hidden_act
        self.initializer_range = initializer_range
        self.rms_norm_eps = rms_norm_eps
        self.pretraining_tp = pretraining_tp
        self.use_cache = use_cache
        self.rope_theta = rope_theta
        self.rope_scaling = rope_scaling
        self.attention_bias = attention_bias
        self.attention_dropout = attention_dropout
        self.mlp_bias = mlp_bias
        self.head_dim = head_dim if head_dim is not None else self.hidden_size // self.num_attention_heads
        # Validate the correctness of rotary position embeddings parameters
        # BC: if there is a 'type' field, copy it it to 'rope_type'.
        if self.rope_scaling is not None and "type" in self.rope_scaling:
            self.rope_scaling["rope_type"] = self.rope_scaling["type"]
        rope_config_validation(self)
        self.moe_intermediate_size = moe_intermediate_size
        self.moe_num_experts = moe_num_experts
        self.moe_topk = moe_topk
        self.moe_z_loss_coeff = moe_z_loss_coeff
        self.moe_aux_loss_coeff = moe_aux_loss_coeff
        self.moe_num_shared_experts = moe_num_shared_experts

        super().__init__(
            pad_token_id=pad_token_id,
            bos_token_id=bos_token_id,
            eos_token_id=eos_token_id,
            tie_word_embeddings=tie_word_embeddings,
            **kwargs,
        )


class AriaConfig(PretrainedConfig):
    """
    Configuration class for Aria model.

    This class handles the configuration for both vision and text components of the Aria model,
    as well as additional parameters for image token handling and projector mapping.

    Args:
        vision_config (AriaVisionConfig or dict): Configuration for the vision component.
        text_config (AriaMoELMConfig or dict): Configuration for the text component.
        projector_patch_to_query_dict (dict): Mapping of patch sizes to query dimensions.
        ignore_index (int): Index to ignore in loss calculation.
        image_token_index (int): Index used to represent image tokens.
        **kwargs: Additional keyword arguments passed to the parent class.

    Attributes:
        model_type (str): Type of the model, set to "aria".
        is_composition (bool): Whether the model is a composition of multiple components.
        ignore_index (int): Index to ignore in loss calculation.
        image_token_index (int): Index used to represent image tokens.
        projector_patch_to_query_dict (dict): Mapping of patch sizes to query dimensions.
        vision_config (AriaVisionConfig): Configuration for the vision component.
        text_config (AriaMoELMConfig): Configuration for the text component.
    """

    model_type = "aria"
    is_composition = False

    def __init__(
        self,
        vision_config=None,
        text_config=None,
        projector_patch_to_query_dict={
            1225: 128,
            4900: 256,
        },
        ignore_index=-100,
        image_token_index=32000,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.ignore_index = ignore_index
        self.image_token_index = image_token_index

        # Convert the keys and values of projector_patch_to_query_dict to integers
        # This ensures consistency even if they were provided as strings
        self.projector_patch_to_query_dict = {int(k): int(v) for k, v in projector_patch_to_query_dict.items()}
        if vision_config is None:
            vision_config = AriaVisionConfig()
        if text_config is None:
            text_config = AriaModelConfig()

        if isinstance(vision_config, dict) and "model_type" in vision_config:
            vision_config = AriaVisionConfig(**vision_config)

        self.vision_config = vision_config

        if isinstance(text_config, dict) and "model_type" in text_config:
            text_config = AriaModelConfig(**text_config)

        self.text_config = text_config
