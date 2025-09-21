"""
Multi-model configuration for IONOS AI Model Hub
Optimizes model selection based on task type and complexity
"""
import os
from enum import Enum
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

class TaskType(Enum):
    PLANNING = "planning"
    ARCHITECTURE = "architecture"
    CODING = "coding"
    REVIEW = "review"

class ModelTier(Enum):
    FAST = "fast"          # For simple tasks, quick responses
    BALANCED = "balanced"   # Good balance of speed and capability
    POWERFUL = "powerful"   # For complex reasoning and large codebases

# IONOS Model Configuration based on your available models
IONOS_MODELS = {
    # Fast models - for simple tasks
    ModelTier.FAST: {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "description": "Fast 8B model - good for simple coding tasks",
        "max_tokens": 4096,
        "temperature": 0.3
    },

    # Balanced models - for most tasks
    ModelTier.BALANCED: {
        "model": "mistralai/Mistral-Nemo-Instruct-2407",
        "description": "Balanced model - good reasoning and coding",
        "max_tokens": 8192,
        "temperature": 0.4
    },

    # Powerful models - for complex tasks
    ModelTier.POWERFUL: {
        "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-FP8",
        "description": "Large 405B model - best reasoning and complex coding",
        "max_tokens": 16384,
        "temperature": 0.2
    }
}

# Task-specific model recommendations
TASK_MODEL_MAPPING = {
    TaskType.PLANNING: ModelTier.BALANCED,     # Planning needs good reasoning
    TaskType.ARCHITECTURE: ModelTier.POWERFUL, # Architecture needs deep thinking
    TaskType.CODING: ModelTier.FAST,           # Coding can be fast for most tasks
    TaskType.REVIEW: ModelTier.BALANCED        # Review needs balanced approach
}

class MultiModelManager:
    """Manages multiple IONOS models for optimal task performance"""

    def __init__(self):
        self.base_url = os.getenv("OPENAI_BASE_URL")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self._model_cache = {}

    def get_model_for_task(self, task_type: TaskType, complexity: str = "medium") -> ChatOpenAI:
        """
        Get the optimal model for a specific task type and complexity

        Args:
            task_type: Type of task (planning, architecture, coding, review)
            complexity: "simple", "medium", "complex"
        """
        # Adjust model tier based on complexity
        base_tier = TASK_MODEL_MAPPING[task_type]

        if complexity == "simple" and base_tier != ModelTier.FAST:
            tier = ModelTier.FAST
        elif complexity == "complex":
            tier = ModelTier.POWERFUL
        else:
            tier = base_tier

        return self._get_or_create_model(tier)

    def get_model_by_tier(self, tier: ModelTier) -> ChatOpenAI:
        """Get model by specific tier"""
        return self._get_or_create_model(tier)

    def _get_or_create_model(self, tier: ModelTier) -> ChatOpenAI:
        """Cache and return model instances"""
        if tier not in self._model_cache:
            config = IONOS_MODELS[tier]

            self._model_cache[tier] = ChatOpenAI(
                model=config["model"],
                openai_api_key=self.api_key,
                openai_api_base=self.base_url,
                temperature=config["temperature"],
                max_tokens=config["max_tokens"]
            )

            print(f"🤖 Initialized {tier.value} model: {config['model']}")

        return self._model_cache[tier]

    def list_available_models(self):
        """List all configured models with descriptions"""
        print("🚀 Available IONOS Models:")
        for tier, config in IONOS_MODELS.items():
            print(f"  {tier.value.upper()}: {config['model']}")
            print(f"    {config['description']}")
            print(f"    Max tokens: {config['max_tokens']}, Temperature: {config['temperature']}")
            print()

# Global instance
model_manager = MultiModelManager()

def get_optimized_llm(task_type: TaskType = TaskType.CODING, complexity: str = "medium") -> ChatOpenAI:
    """
    Get the optimal LLM for a task

    Usage examples:
    - get_optimized_llm(TaskType.PLANNING, "complex")
    - get_optimized_llm(TaskType.CODING, "simple")
    - get_optimized_llm(TaskType.ARCHITECTURE, "medium")
    """
    return model_manager.get_model_for_task(task_type, complexity)

# Quick access functions
def get_planner_llm(complexity: str = "medium") -> ChatOpenAI:
    """Get LLM optimized for planning tasks"""
    return get_optimized_llm(TaskType.PLANNING, complexity)

def get_architect_llm(complexity: str = "medium") -> ChatOpenAI:
    """Get LLM optimized for architecture tasks"""
    return get_optimized_llm(TaskType.ARCHITECTURE, complexity)

def get_coder_llm(complexity: str = "medium") -> ChatOpenAI:
    """Get LLM optimized for coding tasks"""
    return get_optimized_llm(TaskType.CODING, complexity)

if __name__ == "__main__":
    # Test the multi-model system
    model_manager.list_available_models()

    print("🧪 Testing model selection:")
    planner = get_planner_llm("complex")
    architect = get_architect_llm("complex")
    coder = get_coder_llm("simple")

    print(f"Planner model: {planner.model_name}")
    print(f"Architect model: {architect.model_name}")
    print(f"Coder model: {coder.model_name}")