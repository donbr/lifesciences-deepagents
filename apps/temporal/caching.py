"""Prompt caching under the Temporal plugin.

The plugin swaps every chat model for a ``TemporalModel`` stub, so the stock
``AnthropicPromptCachingMiddleware`` (which gates on ``isinstance(model,
ChatAnthropic)``) never fires. The middleware's ``cache_control`` model setting
does survive the hop: ``TemporalModel`` forwards it as ``bind_kwargs`` and the
activity binds it onto the real ``ChatAnthropic``. Only the gate needs relaxing.
"""

from langchain.agents.middleware.types import ModelRequest
from langchain_anthropic.middleware import AnthropicPromptCachingMiddleware
from temporalio.deepagents import TemporalModel


class TemporalAnthropicPromptCachingMiddleware(AnthropicPromptCachingMiddleware):
    def __init__(self) -> None:
        super().__init__(unsupported_model_behavior="ignore")

    def _should_apply_caching(self, request: ModelRequest) -> bool:
        model = request.model
        if isinstance(model, TemporalModel) and model.model.startswith("anthropic:"):
            messages = len(request.messages) + (1 if request.system_message else 0)
            return messages >= self.min_messages_to_cache
        return super()._should_apply_caching(request)
