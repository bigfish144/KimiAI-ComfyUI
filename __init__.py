from .kimiai_node import KimiAINode
NODE_CLASS_MAPPINGS = {
    "KimiAI Text Generator": KimiAINode,
}

NODE_DISPLAY_NAMES_MAPPINGS = {
    "KimiAI Text Generator": "KimiAI Text Generator",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAMES_MAPPINGS']