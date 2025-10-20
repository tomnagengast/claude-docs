# What's new in Claude 4.5

Claude 4.5 introduces two models designed for different use cases:

* **Claude Sonnet 4.5**: Our best model for complex agents and coding, with the highest intelligence across most tasks
* **Claude Haiku 4.5**: Our fastest and most intelligent Haiku model with near-frontier performance. The first Haiku model with extended thinking

## Key improvements in Sonnet 4.5 over Sonnet 4

### Coding excellence

Claude Sonnet 4.5 is our best coding model to date, with significant improvements across the entire development lifecycle:

* **SWE-bench Verified performance**: Advanced state-of-the-art on coding benchmarks
* **Enhanced planning and system design**: Better architectural decisions and code organization
* **Improved security engineering**: More robust security practices and vulnerability detection
* **Better instruction following**: More precise adherence to coding specifications and requirements

<Note>
  Claude Sonnet 4.5 performs significantly better on coding tasks when [extended thinking](/en/docs/build-with-claude/extended-thinking) is enabled. Extended thinking is disabled by default, but we recommend enabling it for complex coding work. Be aware that extended thinking impacts [prompt caching efficiency](/en/docs/build-with-claude/prompt-caching#caching-with-thinking-blocks). See the [migration guide](/en/docs/about-claude/models/migrating-to-claude-4#extended-thinking-recommendations) for configuration details.
</Note>

### Agent capabilities

Claude Sonnet 4.5 introduces major advances in agent capabilities:

* **Extended autonomous operation**: Sonnet 4.5 can work independently for hours while maintaining clarity and focus on incremental progress. The model makes steady advances on a few tasks at a time rather than attempting everything at once. It provides fact-based progress updates that accurately reflect what has been accomplished.
* **Context awareness**: Claude now tracks its token usage throughout conversations, receiving updates after each tool call. This awareness helps prevent premature task abandonment and enables more effective execution on long-running tasks. See [Context awareness](/en/docs/build-with-claude/context-windows#context-awareness-in-claude-sonnet-4-5) for technical details and [prompting guidance](/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices#context-awareness-and-multi-window-workflows).
* **Enhanced tool usage**: The model more effectively uses parallel tool calls, firing off multiple speculative searches simultaneously during research and reading several files at once to build context faster. Improved coordination across multiple tools and information sources enables the model to effectively leverage a wide range of capabilities in agentic search and coding workflows.
* **Advanced context management**: Sonnet 4.5 maintains exceptional state tracking in external files, preserving goal-orientation across sessions. Combined with more effective context window usage and our new context management API features, the model optimally handles information across extended sessions to maintain coherence over time.

<Note>Context awareness is available in Claude Sonnet 4, Sonnet 4.5, Haiku 4.5, Opus 4, and Opus 4.1.</Note>

### Communication and interaction style

Claude Sonnet 4.5 has a refined communication approach that is concise, direct, and natural. It provides fact-based progress updates and may skip verbose summaries after tool calls to maintain workflow momentum (though this can be adjusted with prompting).

For detailed guidance on working with this communication style, see [Claude 4 best practices](/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices).

### Creative content generation

Claude Sonnet 4.5 excels at creative content tasks:

* **Presentations and animations**: Matches or exceeds Claude Opus 4.1 for creating slides and visual content
* **Creative flair**: Produces polished, professional output with strong instruction following
* **First-try quality**: Generates usable, well-designed content in initial attempts

## Key improvements in Haiku 4.5 over Haiku 3.5

Claude Haiku 4.5 represents a transformative leap for the Haiku model family, bringing frontier capabilities to our fastest model class:

### Near-frontier intelligence with blazing speed

Claude Haiku 4.5 delivers near-frontier performance matching Sonnet 4 at significantly lower cost and faster speed:

* **Near-frontier intelligence**: Matches Sonnet 4 performance across reasoning, coding, and complex tasks
* **Enhanced speed**: More than twice the speed of Sonnet 4, with optimizations for output tokens per second (OTPS)
* **Optimal cost-performance**: Near-frontier intelligence at one-third the cost, ideal for high-volume deployments

### Extended thinking capabilities

Claude Haiku 4.5 is the **first Haiku model** to support extended thinking, bringing advanced reasoning capabilities to the Haiku family:

* **Reasoning at speed**: Access to Claude's internal reasoning process for complex problem-solving
* **Thinking Summarization**: Summarized thinking output for production-ready deployments
* **Interleaved thinking**: Think between tool calls for more sophisticated multi-step workflows
* **Budget control**: Configure thinking token budgets to balance reasoning depth with speed

Extended thinking must be enabled explicitly by adding a `thinking` parameter to your API requests. See the [Extended thinking documentation](/en/docs/build-with-claude/extended-thinking) for implementation details.

<Note>
  Claude Haiku 4.5 performs significantly better on coding and reasoning tasks when [extended thinking](/en/docs/build-with-claude/extended-thinking) is enabled. Extended thinking is disabled by default, but we recommend enabling it for complex problem-solving, coding work, and multi-step reasoning. Be aware that extended thinking impacts [prompt caching efficiency](/en/docs/build-with-claude/prompt-caching#caching-with-thinking-blocks). See the [migration guide](/en/docs/about-claude/models/migrating-to-claude-4#extended-thinking-recommendations) for configuration details.
</Note>

<Note>Available in Claude Sonnet 3.7, Sonnet 4, Sonnet 4.5, Haiku 4.5, Opus 4, and Opus 4.1.</Note>

### Context awareness

Claude Haiku 4.5 features **context awareness**, enabling the model to track its remaining context window throughout a conversation:

* **Token budget tracking**: Claude receives real-time updates on remaining context capacity after each tool call
* **Better task persistence**: The model can execute tasks more effectively by understanding available working space
* **Multi-context-window workflows**: Improved handling of state transitions across extended sessions

This is the first Haiku model with native context awareness capabilities. For prompting guidance, see [Claude 4 best practices](/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices#context-awareness-and-multi-window-workflows).

<Note>Available in Claude Sonnet 4, Sonnet 4.5, Haiku 4.5, Opus 4, and Opus 4.1.</Note>

### Strong coding and tool use

Claude Haiku 4.5 delivers robust coding capabilities expected from modern Claude models:

* **Coding proficiency**: Strong performance across code generation, debugging, and refactoring tasks
* **Full tool support**: Compatible with all Claude 4 tools including bash, code execution, text editor, web search, and computer use
* **Enhanced computer use**: Optimized for autonomous desktop interaction and browser automation workflows
* **Parallel tool execution**: Efficient coordination across multiple tools for complex workflows

Haiku 4.5 is designed for use cases that demand both intelligence and efficiency:

* **Real-time applications**: Fast response times for interactive user experiences
* **High-volume processing**: Cost-effective intelligence for large-scale deployments
* **Free tier implementations**: Premium model quality at accessible pricing
* **Sub-agent architectures**: Fast, intelligent agents for multi-agent systems
* **Computer use at scale**: Cost-effective autonomous desktop and browser automation

## New API features

### Memory tool (Beta)

The new [memory tool](/en/docs/agents-and-tools/tool-use/memory-tool) enables Claude to store and retrieve information outside the context window:

```python  theme={null}
tools=[
    {
        "type": "memory_20250818",
        "name": "memory"
    }
]
```

This allows for:

* Building knowledge bases over time
* Maintaining project state across sessions
* Preserving effectively unlimited context through file-based storage

<Note>Available in Claude Sonnet 4, Sonnet 4.5, Haiku 4.5, Opus 4, and Opus 4.1. Requires [beta header](/en/api/beta-headers): `context-management-2025-06-27`</Note>

### Context editing

Use [context editing](/en/docs/build-with-claude/context-editing) for intelligent context management through automatic tool call clearing:

```python  theme={null}
response = client.beta.messages.create(
    betas=["context-management-2025-06-27"],
    model="claude-sonnet-4-5",  # or claude-haiku-4-5
    max_tokens=4096,
    messages=[{"role": "user", "content": "..."}],
    context_management={
        "edits": [
            {
                "type": "clear_tool_uses_20250919",
                "trigger": {"type": "input_tokens", "value": 500},
                "keep": {"type": "tool_uses", "value": 2},
                "clear_at_least": {"type": "input_tokens", "value": 100}
            }
        ]
    },
    tools=[...]
)
```

This feature automatically removes older tool calls and results when approaching token limits, helping manage context in long-running agent sessions.

<Note>Available in Claude Sonnet 4, Sonnet 4.5, Haiku 4.5, Opus 4, and Opus 4.1. Requires [beta header](/en/api/beta-headers): `context-management-2025-06-27`</Note>

### Enhanced stop reasons

Claude 4.5 models introduce a new `model_context_window_exceeded` stop reason that explicitly indicates when generation stopped due to hitting the context window limit, rather than the requested `max_tokens` limit. This makes it easier to handle context window limits in your application logic.

```json  theme={null}
{
  "stop_reason": "model_context_window_exceeded",
  "usage": {
    "input_tokens": 150000,
    "output_tokens": 49950
  }
}
```

### Improved tool parameter handling

Claude 4.5 models include a bug fix that preserves intentional formatting in tool call string parameters. Previously, trailing newlines in string parameters were sometimes incorrectly stripped. This fix ensures that tools requiring precise formatting (like text editors) receive parameters exactly as intended.

<Note>
  This is a behind-the-scenes improvement with no API changes required. However, tools with string parameters may now receive values with trailing newlines that were previously stripped.
</Note>

**Example:**

```json  theme={null}
// Before: Final newline accidentally stripped
{
  "type": "tool_use",
  "id": "toolu_01A09q90qw90lq917835lq9",
  "name": "edit_todo",
  "input": {
    "file": "todo.txt",
    "contents": "1. Chop onions.\n2. ???\n3. Profit"
  }
}

// After: Trailing newline preserved as intended
{
  "type": "tool_use",
  "id": "toolu_01A09q90qw90lq917835lq9",
  "name": "edit_todo",
  "input": {
    "file": "todo.txt",
    "contents": "1. Chop onions.\n2. ???\n3. Profit\n"
  }
}
```

### Token count optimizations

Claude 4.5 models include automatic optimizations to improve model performance. These optimizations may add small amounts of tokens to requests, but **you are not billed for these system-added tokens**.

## Features introduced in Claude 4

The following features were introduced in Claude 4 and are available across Claude 4 models, including Claude Sonnet 4.5 and Claude Haiku 4.5.

### New refusal stop reason

Claude 4 models introduce a new `refusal` stop reason for content that the model declines to generate for safety reasons:

```json  theme={null}
{"id":"msg_014XEDjypDjFzgKVWdFUXxZP",
"type":"message",
"role":"assistant",
"model":"claude-sonnet-4-5",
"content":[{"type":"text","text":"I would be happy to assist you. You can "}],
"stop_reason":"refusal",
"stop_sequence":null,
"usage":{"input_tokens":564,"cache_creation_input_tokens":0,"cache_read_input_tokens":0,"output_tokens":22}
}
```

When using Claude 4 models, you should update your application to [handle `refusal` stop reasons](/en/docs/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

### Summarized thinking

With extended thinking enabled, the Messages API for Claude 4 models returns a summary of Claude's full thinking process. Summarized thinking provides the full intelligence benefits of extended thinking, while preventing misuse.

While the API is consistent across Claude 3.7 and 4 models, streaming responses for extended thinking might return in a "chunky" delivery pattern, with possible delays between streaming events.

<Note>
  Summarization is processed by a different model than the one you target in your requests. The thinking model does not see the summarized output.
</Note>

For more information, see the [Extended thinking documentation](/en/docs/build-with-claude/extended-thinking#summarized-thinking).

### Interleaved thinking

Claude 4 models support interleaving tool use with extended thinking, allowing for more natural conversations where tool uses and responses can be mixed with regular messages.

<Note>
  Interleaved thinking is in beta. To enable interleaved thinking, add [the beta header](/en/api/beta-headers) `interleaved-thinking-2025-05-14` to your API request.
</Note>

For more information, see the [Extended thinking documentation](/en/docs/build-with-claude/extended-thinking#interleaved-thinking).

### Behavioral differences

Claude 4 models have notable behavioral changes that may affect how you structure prompts:

#### Communication style changes

* **More concise and direct**: Claude 4 models communicate more efficiently, with less verbose explanations
* **More natural tone**: Responses are slightly more conversational and less machine-like
* **Efficiency-focused**: May skip detailed summaries after completing actions to maintain workflow momentum (you can prompt for more detail if needed)

#### Instruction following

Claude 4 models are trained for precise instruction following and require more explicit direction:

* **Be explicit about actions**: Use direct language like "Make these changes" or "Implement this feature" rather than "Can you suggest changes" if you want Claude to take action
* **State desired behaviors clearly**: Claude will follow instructions precisely, so being specific about what you want helps achieve better results

For comprehensive guidance on working with these models, see [Claude 4 prompt engineering best practices](/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices).

### Updated text editor tool

The text editor tool has been updated for Claude 4 models with the following changes:

* **Tool type**: `text_editor_20250728`
* **Tool name**: `str_replace_based_edit_tool`
* The `undo_edit` command is no longer supported

<Note>
  The `str_replace_editor` text editor tool remains the same for Claude Sonnet 3.7.
</Note>

If you're migrating from Claude Sonnet 3.7 and using the text editor tool:

```python  theme={null}
# Claude Sonnet 3.7
tools=[
    {
        "type": "text_editor_20250124",
        "name": "str_replace_editor"
    }
]

# Claude 4 models
tools=[
    {
        "type": "text_editor_20250728",
        "name": "str_replace_based_edit_tool"
    }
]
```

For more information, see the [Text editor tool documentation](/en/docs/agents-and-tools/tool-use/text-editor-tool).

### Updated code execution tool

If you're using the code execution tool, ensure you're using the latest version `code_execution_20250825`, which adds Bash commands and file manipulation capabilities.

The legacy version `code_execution_20250522` (Python only) is still available but not recommended for new implementations.

For migration instructions, see the [Code execution tool documentation](/en/docs/agents-and-tools/tool-use/code-execution-tool#upgrade-to-latest-tool-version).

## Pricing and availability

### Pricing

Claude 4.5 models maintain competitive pricing:

| Model             | Input                  | Output                  |
| ----------------- | ---------------------- | ----------------------- |
| Claude Sonnet 4.5 | \$3 per million tokens | \$15 per million tokens |
| Claude Haiku 4.5  | \$1 per million tokens | \$5 per million tokens  |

For more details, see the [pricing documentation](/en/docs/about-claude/pricing).

### Third-party platform pricing

Starting with Claude 4.5 models (Sonnet 4.5 and Haiku 4.5), AWS Bedrock and Google Vertex AI offer two endpoint types:

* **Global endpoints**: Dynamic routing for maximum availability
* **Regional endpoints**: Guaranteed data routing through specific geographic regions with a **10% pricing premium**

**This regional pricing applies to both Claude Sonnet 4.5 and Claude Haiku 4.5.**

**The Claude API (1P) is global by default and unaffected by this change.** The Claude API is global-only (equivalent to the global endpoint offering and pricing from other providers).

For implementation details and migration guidance:

* [AWS Bedrock global vs regional endpoints](/en/api/claude-on-amazon-bedrock#global-vs-regional-endpoints)
* [Google Vertex AI global vs regional endpoints](/en/api/claude-on-vertex-ai#global-vs-regional-endpoints)

### Availability

Claude 4.5 models are available on:

| Model             | Claude API                   | Amazon Bedrock                              | Google Cloud Vertex AI       |
| ----------------- | ---------------------------- | ------------------------------------------- | ---------------------------- |
| Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929` | `anthropic.claude-sonnet-4-5-20250929-v1:0` | `claude-sonnet-4-5@20250929` |
| Claude Haiku 4.5  | `claude-haiku-4-5-20251001`  | `anthropic.claude-haiku-4-5-20251001-v1:0`  | `claude-haiku-4-5@20251001`  |

Also available through Claude.ai and Claude Code platforms.

## Migration guide

Breaking changes and migration requirements vary depending on which model you're upgrading from. For detailed migration instructions, including step-by-step guides, breaking changes, and migration checklists, see [Migrating to Claude 4.5](/en/docs/about-claude/models/migrating-to-claude-4).

The migration guide covers the following scenarios:

* **Claude Sonnet 3.7 → Sonnet 4.5**: Complete migration path with breaking changes
* **Claude Haiku 3.5 → Haiku 4.5**: Complete migration path with breaking changes
* **Claude Sonnet 4 → Sonnet 4.5**: Quick upgrade with minimal changes
* **Claude Opus 4.1 → Sonnet 4.5**: Seamless upgrade with no breaking changes

## Next steps

<CardGroup cols={3}>
  <Card title="Best practices" icon="lightbulb" href="/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices">
    Learn prompt engineering techniques for Claude 4.5 models
  </Card>

  <Card title="Model overview" icon="table" href="/en/docs/about-claude/models/overview">
    Compare Claude 4.5 models with other Claude models
  </Card>

  <Card title="Migration guide" icon="arrow-right-arrow-left" href="/en/docs/about-claude/models/migrating-to-claude-4">
    Upgrade from previous models
  </Card>
</CardGroup>
