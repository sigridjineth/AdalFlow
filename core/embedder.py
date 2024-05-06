from typing import Optional, Any, Dict, Union, Sequence
from core.data_classes import ModelType
from core.api_client import APIClient

from core.component import Component
import core.functional as F


class Embedder(Component):
    model_type: ModelType = ModelType.EMBEDDER
    model_client: APIClient
    output_processors: Optional[Component]

    def __init__(
        self,
        *,
        model_client: APIClient,
        model_kwargs: Dict = {},
        output_processors: Optional[Component] = None,
    ) -> None:
        super().__init__()
        self.model_kwargs = model_kwargs.copy()
        if "model" not in model_kwargs:
            raise ValueError(
                f"{type(self).__name__} requires a 'model' to be passed in the model_kwargs"
            )
        self.model_client = model_client
        self.output_processors = output_processors
        self.model_client._init_sync_client()

    def update_default_model_kwargs(self, **model_kwargs) -> Dict:
        return F.compose_model_kwargs(self.model_kwargs, model_kwargs)

    def call(
        self,
        *,
        input: Union[str, Sequence[str]],
        model_kwargs: Optional[Dict] = {},
    ) -> Any:
        composed_model_kwargs = self.update_default_model_kwargs(**model_kwargs)
        response = self.model_client.call(
            input=input, model_kwargs=composed_model_kwargs, model_type=self.model_type
        )
        if self.output_processors:
            return self.output_processors(response)

    def extra_repr(self) -> str:
        s = f"model_kwargs={self.model_kwargs}, model_client={self.model_client}"
        return s
